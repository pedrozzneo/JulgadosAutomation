from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import re
import os
import error as error

files_properly_downloaded = 0

def get_download_links(driver, previousValue):
    try:
        # Locate all the download links
        downloadLinks = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@title='Visualizar Inteiro Teor']"))
        )
        print(f"-> Found {len(downloadLinks)} links")
        return downloadLinks
    except:
        error.log_error(None, None, context="Unable to locate download links")
        return []

def get_expected_downloads(driver, previousValue):
    def valid_text_changed(d):
        try:
            text = d.find_element(By.XPATH, xpath).text
            if text == previousValue:
                print("🟡 Texto ainda não mudou.")
            elif not re.search(pattern, text):
                print(f"🟠 Texto novo detectado, mas não bate com o padrão: {text}")
            else:
                print("✅ Texto novo detectado e válido!")
            return text != previousValue and re.search(pattern, text)
        except Exception as e:
            print(f"🔴 Erro ao verificar o texto: {e}")
            return False

    try:
        # Define the xpath of the download message and how its supposed to be once its fully loaded in pattern
        xpath = "//td[@bgcolor='#EEEEEE' and contains(text(), 'Resultados')]"
        pattern = r"Resultados (\d+) a (\d+) de (\d+)"

        # Give the driver some time to fully load the message and makes sure its different from the previous one
        WebDriverWait(driver, 10).until(valid_text_changed)

        # Rebusca o elemento final, agora garantido como válido
        fullDownloadsMessage = driver.find_element(By.XPATH, xpath)
        text = fullDownloadsMessage.text
        print(f"-> Texto final: {text}")

        match = re.search(pattern, text)
        if match:
            expectedDownloads = int(match.group(2)) - int(match.group(1)) + 1
            return expectedDownloads, text  # retorna também o texto novo
        else:
            error.log_error("Regex", "Failed to extract numbers", context="expected_downloads")
            return None, text

    except Exception as e:
        error.log_error(None, None, context=f"Error in get_expected_downloads: {str(e)}")
        return None, previousValue

def found_matches_expected(downloadLinks, expectedDownloads, classe, date):
    try:
        if len(downloadLinks) != expectedDownloads:
            error.log_error(classe, date, context=f"-> Mismatch: Found {len(downloadLinks)} links, but expected {expectedDownloads}.")
            print("-> Download links DON'T match expected downloads.")
            return
        print("-> Download links match expected downloads.")
    except Exception:
        error.log_error(classe, date, context=f"Error in found_matches_expected:")

# ///////////////////////////////////////////////
def download_each_link(driver, downloadLinks, download_dir, classe, date):
    try:
        if len(downloadLinks) != 0:
            for index, link in enumerate(downloadLinks, start=1):
                link.click()
                print(f"Link {index} clicked")

                # It opens up a new window, so go to that window
                driver.switch_to.window(driver.window_handles[-1])
                print(f"Switched to new window")

                # Store how many files I have before downloading to check later if the download that is about to happen was successful
                initialSize = count_files(download_dir)
                print(f"-> size before clicking the download button: {initialSize} files")
                
                # Find and click the download button
                download_button = getDownloadButton(driver, classe, date)
                download_button.click()
                print(f"Download button clicked")
                
                # Wait for the file to be downloaded
                if not is_file_downloaded(download_dir, sizeBeforeDownload=initialSize, timeout=30, classe=classe, date=date):
                    error.log_error(classe, date, context="is_file_downloaded")

                # Close the current window and switch back to the main window to access other links
                reset_window_and_frame(driver)
    except Exception:
        error.log_error(classe, date, context=f"Error in download_each_link")

def count_files(download_dir):
    return sum(len(files) for _, _, files in os.walk(download_dir))

def getDownloadButton(driver, classe, date):
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
        error.log_error(classe, date, context= "Unable to assign the download button")
        reset_window_and_frame(driver)

def is_file_downloaded(download_dir, sizeBeforeDownload, timeout=30, classe=None, date=None):
    # Track how long its been since I start comparing, so I can stop if it takes too long
    start_time = time.time()
   
    while time.time() - start_time < timeout:
        if count_files(download_dir) == sizeBeforeDownload + 1:
            global files_properly_downloaded
            files_properly_downloaded += 1
            print(f"-> files_properly_downloaded: {files_properly_downloaded}")
            return True
    
    # Log error if the file is not downloaded within the timeout
    context = "is_file_downloaded: File expected to be download but it wasnt"
    error.log_error(classe, date, context)
    return False

def reset_window_and_frame(driver):
    driver.switch_to.default_content()
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
# ///////////////////////////////////////////////

def more_download_links_pages(driver):
    try:
        time.sleep(5)
        # Try to locate the "Próxima página" link
        next_page_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[@title='Próxima página' and contains(@class, 'esajLinkLogin')]"))
        )
        print("-> Found 'Próxima página' link.")
        next_page_link.click()
        print("-> advance to the next page")
        return True
    except:
        print("-> 'Próxima página' link not found.")
        return False

def download(driver, download_dir, classe, date):
    global files_properly_downloaded
    files_properly_downloaded = 0 # Resets counter for each different class/date
    downloadLinks = None
    expectedDownloads = None
    
    while True:
        downloadLinks = get_download_links(driver, downloadLinks)
        expectedDownloads = get_expected_downloads(driver, expectedDownloads)

        found_matches_expected(downloadLinks, expectedDownloads, classe, date)

        #download_each_link(driver, downloadLinks, download_dir, classe, date)

        if more_download_links_pages(driver): 
            # Resets some stuffs
            continue

        # Just exit the whole loop if there aren't any other download link pages
        break
        

       