from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from datetime import datetime, timedelta
import os
import fill_filters as fill_filters
import download as download
import files as files
import error as error
from concurrent.futures import ThreadPoolExecutor
        
def iterate_error_log(driver, download_dir):
    counter = 0
    while error.error_log:
        if stop_threads:
            return
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

def create_driver(URL, download_dir):
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
    })
    options.add_argument("--headless=new")
    options.add_argument("--disable-logging")  # Disable logging from chrome
  
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def scrape(classe):
    # Setup the driver
    URL = "https://esaj.tjsp.jus.br/cjpg"
    download_dir = r"C:\Users\nikao\Desktop\Julgados"
    driver = create_driver(URL, download_dir)

    driver.get(URL)
    driver.implicitly_wait(10)  # seconds
    #driver.maximize_window()

    # Set the period of time to be searched
    dateTime = datetime.strptime("01/01/2022", "%d/%m/%Y")
    endDateTime = datetime.strptime("31/12/2024", "%d/%m/%Y")

    # Iterates day by day until the end
    while dateTime <= endDateTime:
        # Increment day and format for string use
        dateTime = (dateTime + timedelta(1))
        date = dateTime.strftime("%d/%m/%Y")
        
        # Fill out all the filters
        try:
            fill_filters.fill_filters(driver, classe, date)
        except Exception as e:
            print(f"❌ fill_filters call:  {classe} on {date}: {e}")
            error.log_error(classe, date, "fill_filters")
            continue

        # Download and move the files if there are any
        if download.there_are_download_links(driver):
            download.download(driver, download_dir, classe, date)
            # try:
            #     files.move_files(download_dir, classe, date, download.files_properly_downloaded)
            # except Exception as e:
            #     print(f"Error while moving files for class '{classe}' and date '{date}': {e}")
            #     error.log_error(classe, date, "move_files")
            #     continue

    driver.quit()
            
    # # Display all errors
    # try:
    #     error.display_error_log()
    # except Exception as e:
    #     print(f"Error displaying error log: {e}")


    # iterate_error_log(driver, download_dir)

# List all classes to be searched
classes = [
    "Mandado de Segurança Coletivo", 
    "Ação Civil de Improbidade Administrativa", 
    "Ação Civil Coletiva",
    "Ação Civil Pública", 
    "Ação Popular", 
    "Usucapião"
]

with ThreadPoolExecutor() as executor:
    executor.map(scrape, classes)