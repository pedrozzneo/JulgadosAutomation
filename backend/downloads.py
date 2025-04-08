from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
import shutil

error_log = []
def log_error(classe, date, context):
    # Logs an error with details about the class and date.
    error_log.append(f"Class: {classe}, Date: {date}, Context: {context}")
    print(context)
def display_error_log():
    # Displays the error log in a numbered format.
    if not error_log:
        print("No errors logged.")
    else:
        print("\nError Log:")
        for i, error in enumerate(error_log, start=1):
            print(f"{i}- {error}")

def reset(driver):
    print("-> Resetting the WebDriver...")
    URL = "https://esaj.tjsp.jus.br/cjpg"
    driver.get(URL)
    driver.maximize_window()
def reset_window_and_frame(driver):
    driver.switch_to.default_content()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])

def move_files(download_dir, classe, current_date_str, counter):
    try:
        # Being more specific with this particular example
        if(classe == "Usucapião"):
            classe = "Usucapião Especial Coletiva"

        # Create the directory for the current date and class if it doesn't exist
        current_date_dir = os.path.join(download_dir, str(classe), current_date_str.replace("/", "-"))
        if not os.path.exists(current_date_dir):
            os.makedirs(current_date_dir)

        # Get the most recent downloaded files based on the counter
        files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
        most_recent_files = sorted(files, key=os.path.getctime, reverse=True)[:counter]

        # Move the most recent files to the current date directory
        for file in most_recent_files:
            destination = os.path.join(current_date_dir, os.path.basename(file))
            if not os.path.exists(destination):
                shutil.move(file, destination)
                print(f"-> Moved {file} to {destination}")
            else:
                print(f"-> File {destination} already exists. Deleting it")
                os.remove(file)

    except:
        context = "move_files"
        log_error(classe, current_date_str, context)
        print(f"Error while moving files.")

def expected_downloads(driver):
    # Locate the element containing all the info about downloads
    fullDownloadsMessage = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//td[@bgcolor='#EEEEEE' and contains(text(), 'Resultados')]"))
    )
    print(f"-> Found results element: {fullDownloadsMessage.text}")
    # Extract the expected number of downloads using regex
    padrao = r"Resultados (\d+) a (\d+) de (\d+)"
    match = re.search(padrao, fullDownloadsMessage.text)
    
    if match:
        primeiro_numero = int(match.group(2))
        return primeiro_numero
    else:
        context = "expected_downloads"
        log_error("Regex", "Failed to extract numbers", context)
        return None, None 

def count_files(download_dir):
    return sum(len(files) for _, _, files in os.walk(download_dir))
def is_file_downloaded(download_dir, counter, sizeBeforeDownload, timeout=30, classe=None, date=None):
    # Track how long its been since I start comparing, so I can stop if it takes too long
    start_time = time.time()
   
    while time.time() - start_time < timeout:
        if count_files(download_dir) == sizeBeforeDownload + 1:
            print(f"-> File downloaded successfully.")
            return True
    
    # Log error if the file is not downloaded within the timeout
    context = "is_file_downloaded: File expected to be download but it wasnt"
    log_error(classe, date, context)
    return False

def areThereFileLinks(driver):
     # Check if there are no results for the search without throwing an error
        try:
            print("checking if there are file links")
            no_results_message = driver.find_element(By.XPATH, "//div[contains(@class, 'aviso espacamentoCimaBaixo centralizado fonteNegrito') and contains(text(), 'Não foi encontrado nenhum resultado correspondente à busca realizada.')]")
            if no_results_message:
                print("-> 'No results message' found.")
                return False
        except Exception:
            print("-> There isnt any 'No results message'.")
            return True

def getDownloadButton(driver):
    try:
        # Switch to the iframe that contains the download button
        iframe = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "iframe"))
        )
        driver.switch_to.frame(iframe)
        
        # Locate the download button within the iframe
        download_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "download"))
        )
        return download_button
    except:
        log_error(None, None, context= "Unable to assign the download button")
        reset_window_and_frame(driver)
def getDownload_links(driver):
    # Locate all the download links
    downloadLinks = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.XPATH, "//a[@title='Visualizar Inteiro Teor']"))
    )
    print(f"-> Found {len(downloadLinks)} links")
    return downloadLinks
 
def download(driver, download_dir, classe, current_date_str):
    try:
       if areThereFileLinks(driver):
            # Get the number of download links and expected downloads from the website info
            downloadLinks = getDownload_links(driver)
            expectedDownloads = expected_downloads(driver)
            
            # Check if the number of download links matches the expected number
            if len(downloadLinks) != expectedDownloads:
                log_error(classe, current_date_str, context = f"-> Mismatch: Found {len(downloadLinks)} links, but expected {expectedDownloads}." )
                return
            print("-> Download links match expected downloads.")

            # Properly download each link
            if len(downloadLinks) != 0:
                for index, link in enumerate(downloadLinks):
                    # Click the link to open the download page
                    link.click()
                    print(f"Link {index} clicked")

                    # It opens up a new window, so go to that window
                    driver.switch_to.window(driver.window_handles[-1])
                    print(f"Switched to new window")

                     # Store how many files I have before downloading to check later if the download that is about to happen was succesful
                    initialSize = count_files(download_dir)
                    print(f"-> size before clicking the download button: {initialSize} files")
                    
                    # Find and click the download button
                    download_button = getDownloadButton(driver)
                    download_button.click()
                    print(f"Download button clicked")
                    
                    # Wait for the file to be downloaded
                    if not is_file_downloaded(download_dir, counter=len(downloadLinks), sizeBeforeDownload=initialSize, timeout=30, classe=classe, date=current_date_str):
                        log_error(classe, current_date_str, context = "is_file_downloaded")

                    reset_window_and_frame(driver)
                move_files(download_dir, classe, current_date_str, counter=len(downloadLinks))
          
    except:
        log_error(classe, current_date_str, context = "download")
        #reset(driver)
