from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import os
import fill_filters as fill_filters
import download as download
import files as files
import error as error

def ThereAreFileLinks(driver):
    try:
        no_results_message = driver.find_element(By.XPATH, "//div[contains(@class, 'aviso espacamentoCimaBaixo centralizado fonteNegrito') and contains(text(), 'Não foi encontrado nenhum resultado correspondente à busca realizada.')]")
        if no_results_message:
            print(" NO Files avaiable for download")
            return False
    except TimeoutException:
        print("Timeout while checking for file links.")
        return False
    except Exception as e:
        print(f" Files avaiable for download")
        return True
        
def iterate_error_log(driver, download_dir):
    counter = 0
    while error.error_log:
        counter += 1
        if counter % 20 == 0:
              # Display all errors
                try:
                    error.display_error_log()
                except Exception as e:
                    print(f"Error displaying error log: {e}")

        entry = error.error_log.pop(0)  # Remove the first item
        # Example format: "Class: Usucapiao, Date: 2025-04-15, Context: fill_filters: TimeOutException"
        
        # Split and extract
        parts = entry.split(", ")
        classe = parts[0].split(": ")[1]
        date = parts[1].split(": ")[1]

        # Use them
        print("Class:", classe)
        print("Date:", date)

        # Fill out all the fillters
        try:
            fill_filters.fill_filters(driver, classe, date)
        except Exception as e:
            print(f"Error while filling filters for class '{classe}' and date '{date}': {e}")
            error.log_error(classe, date, "fill_filters")
            continue
          
        # Check if there are links for download before starting the whole process
        try:
            if ThereAreFileLinks(driver):
                download.download(driver, download_dir, classe, date)
                try:
                    files.move_files(download_dir, classe, date, download.files_properly_downloaded)
                except Exception as e:
                    print(f"Error while moving files for class '{classe}' and date '{date}': {e}")
                    error.log_error(classe, date, "move_files")
                    continue
        except Exception as e:
            print(f"Error while checking for file links or downloading files for class '{classe}' and date '{date}': {e}")
            error.log_error(classe, date, "ThereAreFileLinks or download")
            continue

def main():
    URL = "https://esaj.tjsp.jus.br/cjpg"

    # List all classes to be searched
    classes = ["Ação Civil Pública", "Ação Civil de Improbidade Administrativa", "Ação Civil Coletiva", "Ação Popular", "Mandado de Segurança Coletivo", "Usucapião"]
    classes = ["Ação Civil Pública"]
    print(f"classes: {classes}")

    startingDate = datetime.strptime("01/01/2022", "%d/%m/%Y")
    endDate = datetime.now()
    endDate = datetime.strptime("31/12/2022", "%d/%m/%Y")
    print(f"dates: from {startingDate} to {endDate}")

    # Calculate the interval between start_date and end_date
    interval = endDate - startingDate

    # Temporary download directory before being moved to the specific date folder
    download_dir = "/home/nikao/Documents/pdfs"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    #Set Firefox options
    options = Options()
    options.set_preference("pdfjs.disabled", True) # Avoid opening many pdp windows
    options.set_preference("browser.download.folderList", 2)  # Use custom download dir
    options.set_preference("browser.download.dir", download_dir)  # Set the download directory
    options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")  # Auto-download PDFs
    #options.set_preference("pdfjs.disabled", True)  # Disable PDF viewer in Firefox

    # Initialize it
    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    driver.get("https://esaj.tjsp.jus.br/cjpg") # Access the desired page
    driver.implicitly_wait(60)

    # Loop through each class and date range
    for classe in classes:
        # Loop through each date in the range
        for i in range(interval.days + 1):
            date = (startingDate + timedelta(days=i)).strftime("%d/%m/%Y")
            print(f"\n{classe.upper()} ON {date.upper()}: \n")
            
            # Fill out all the fillters
            try:
                fill_filters.fill_filters(driver, classe, date)
            except Exception as e:
                print(f"Error while filling filters for class '{classe}' and date '{date}': {e}")
                error.log_error(classe, date, "fill_filters")
                continue
            
            # Check if there are links for download before starting the whole process
            try:
                if ThereAreFileLinks(driver):
                    download.download(driver, download_dir, classe, date)
                    try:
                        files.move_files(download_dir, classe, date, download.files_properly_downloaded)
                    except Exception as e:
                        print(f"Error while moving files for class '{classe}' and date '{date}': {e}")
                        error.log_error(classe, date, "move_files")
                        continue
            except Exception as e:
                print(f"Error while checking for file links or downloading files for class '{classe}' and date '{date}': {e}")
                error.log_error(classe, date, "ThereAreFileLinks or download")
                continue

    # Display all errors
    try:
        error.display_error_log()
    except Exception as e:
        print(f"Error displaying error log: {e}")


    iterate_error_log(driver, download_dir)

main()