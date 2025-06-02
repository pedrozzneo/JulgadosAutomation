from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import re
import error as error
import files

files_properly_downloaded = 0

def message_or_link(driver):   
    # Look for message reference
    try:
        driver.find_element(By.XPATH, "//div[contains(@class, 'aviso espacamentoCimaBaixo centralizado fonteNegrito') and contains(text(), 'Não foi encontrado nenhum resultado correspondente à busca realizada.')]") 
        return "message"
    except:
        pass
    
    # Look for link reference
    try:
        driver.find_element(By.XPATH, "//a[@title='Visualizar Inteiro Teor']") 
        return "link"
    except:
        return None

def present(driver, classe, date):
    try:
        # Find out if we have links or message (represents absence of links)
        result = WebDriverWait(driver, 80).until(message_or_link)

        # Treat each possibility
        if result == "link":
            print("✅ Links to download")  
            return True
        if result == "message":
            print("❌ Links to download")  
            return False
    except Exception as e:
        error.log(classe, date, context=f"link -> present: {e}")   
        raise

def get_download_links_and_names(driver, previousNames, classe, date):
    def valid_links_changed(driver):
        try:
            currentLinks = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//a[@title='Visualizar Inteiro Teor']"))
            )
            currentNames = [link.get_attribute("name") for link in currentLinks]

            if previousNames == currentNames:
                print("🟡 Link ainda presente, nada novo.")
                return False
            else:
                print("✅ Link novo detectado!")
                return currentLinks, currentNames
        except Exception:
            print("🟡 Link ainda nao mudou")
            return False

    try:
        # Locate all the download links again (they might be stale otherwise)
        downloadLinks, currentNames = WebDriverWait(driver, 80).until(valid_links_changed)
        return downloadLinks, currentNames
    except Exception as e:
        error.log(classe, date, context=f"get_download_links: {e}")
        raise

def get_expected_downloads(driver, previousValue, classe, date):
    def valid_text_changed(driver):
        try:
            fullDownloadsMessage = driver.find_element(By.XPATH, "//td[@bgcolor='#EEEEEE' and contains(text(), 'Resultados')]").text
            if fullDownloadsMessage == previousValue:
                print("🟡 Texto ainda não mudou.")
            elif not re.search(pattern, fullDownloadsMessage):
                print(f"🟠 Texto novo detectado, mas não bate com o padrão: {fullDownloadsMessage}")
            else:
                return fullDownloadsMessage 
        except Exception as e:
            print(f"🔴 Erro ao verificar o texto: {e}")
            return False

    try:
        pattern = r"Resultados (\d+) a (\d+) de (\d+)"
        # Give the driver some time to fully load the message and makes sure its different from the previous one
        fullDownloadsMessage = WebDriverWait(driver, 30).until(valid_text_changed)

        # Define the xpath of the download message and how its supposed to be once its fully loaded in pattern
        match = re.search(pattern, fullDownloadsMessage)
        if match:
            expectedDownloads = int(match.group(2)) - int(match.group(1)) + 1
            return expectedDownloads, fullDownloadsMessage
        else:
            error.log("Regex", "Failed to extract numbers", context="expected_downloads")
            raise Exception("Failed to extract numbers from download message")

    except Exception as e:
        error.log(classe, date, context=f"Error in get_expected_downloads: {str(e)}")
        raise

def download_each_link(driver, downloadLinks, download_dir, classe, date):
    def getDownloadButton(driver, classe, date):
        try:
            # Switch to the iframe that contains the download button
            iframe = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "iframe"))
            )
            driver.switch_to.frame(iframe)
            
            # Locate the download button within the iframe
            download_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.ID, "download"))
            )
            return download_button
        
        except Exception as e:
            error.log(classe, date, context=f"getDownloadButton: {e}")  # Fixed context name
            reset_window_and_frame(driver)
            raise

    def is_file_downloaded(download_dir, sizeBeforeDownload, classe, date):
        # Track how long its been since I start comparing, so I can stop if it takes too long
        start_time = time.time()
        
        # Set a timeout for the download check
        timeout = 30

        while time.time() - start_time < timeout:
            if files.count_files(download_dir) == sizeBeforeDownload + 1:
                global files_properly_downloaded
                files_properly_downloaded += 1
                print(f"{files_properly_downloaded} files downloaded")
                return True
        
        # Log error if the file is not downloaded within the timeout
        error.log(classe, date, context= "is_file_downloaded")
        return False

    def reset_window_and_frame(driver):
        driver.switch_to.default_content()
        driver.close()
        driver.switch_to.window(driver.window_handles[0])

    try:
        if len(downloadLinks) != 0:
            success = True
            for index, link in enumerate(downloadLinks, start=1):
                link.click()
                #print(f"Link {index} clicked")

                # It opens up a new window, so go to that window
                driver.switch_to.window(driver.window_handles[-1])

                # Store how many files I have before downloading to check later if the download that is about to happen was successful
                initialSize = files.count_files(download_dir)
                
                # Find and click the download button
                download_button = getDownloadButton(driver, classe, date)
                download_button.click()
                
                # Wait for the file to be downloaded
                if not is_file_downloaded(download_dir, initialSize, classe, date):
                    success = False
                    print("-> Some files failed to download.")

                # Close the current window and switch back to the main window to access other links
                reset_window_and_frame(driver)
            if success:
                print("-> ✅ All page's files downloaded.")
    except Exception:
        reset_window_and_frame(driver)
        raise

def more_download_links_pages(driver):
    try:
        # Try to locate the "Próxima página" link
        next_page_link = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "//a[@title='Próxima página' and contains(@class, 'esajLinkLogin')]"))
        )
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
    # This is an array cause the first value is whats useful and the second is just to compare wether the text changed or not
    expectedDownloads = [None, None]
    linkNames = []
    
    while True:
        try:
            # Get the download links and names
            downloadLinks, linkNames = get_download_links_and_names(driver, linkNames, classe, date)
            #print(f"found {len(linkNames)} links: {linkNames}")
            
            # Get the number of expected downloads and the full message text
            expectedDownloads = get_expected_downloads(driver, expectedDownloads[1], classe, date)
            print(f"-> Expected downloads: {expectedDownloads[0]}")

            # Check if the expected number of downloads matches the actual number of links found
            if len(downloadLinks) != expectedDownloads[0]:
                error.log(classe, date, context="download -> found links dont match expected")

            # Download each link
            download_each_link(driver, downloadLinks, download_dir, classe, date)
            
            # If there`s another page with download links, continue the loop
            if more_download_links_pages(driver): 
                continue

            # Just exit the whole loop if there isn't any other download link pages
            break
        except Exception as e:
            raise


