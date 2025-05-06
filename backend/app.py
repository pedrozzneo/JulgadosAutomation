from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import os
import form as form
import link as link
import files as files
import error as error
        
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
        
        # Split and extract
        parts = entry.split(", ")
        classe = parts[0].split(": ")[1]
        date = parts[1].split(": ")[1]

        # Use them
        print("Class:", classe)
        print("Date:", date)

        # Fill out all the fillters
        try:
            form.fill_filters(driver, classe, date)
        except Exception as e:
            print(f"Error while filling filters for class '{classe}' and date '{date}': {e}")
            error.log_error(classe, date, "fill_filters")
            continue
          
        # Check if there are links for download before starting the whole process
        try:
            if link.present(driver):
                link.download(driver, download_dir, classe, date)
                try:
                    files.move_files(download_dir, classe, date, link.files_properly_downloaded)
                except Exception as e:
                    print(f"Error while moving files for class '{classe}' and date '{date}': {e}")
                    error.log_error(classe, date, "move_files")
                    continue
        except Exception as e:
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
    download_dir = r"C:\Users\nikao\Desktop\julgados\pdfs"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Set Chrome options
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
    })
    #options.add_argument("--headless")

    # Start WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    #driver.maximize_window()

    # Loop through each class and date
    for classe in classes:
        for i in range(interval.days + 1):
            
            # Calculate the date for the current iteration and show importanto information
            date = (startingDate + timedelta(days=i)).strftime("%d/%m/%Y")
            print(f"\n{classe.upper()} ON {date.upper()}: \n")
            
            # Fill out forms's fillters
            try:
                form.fill_filters(driver, classe, date)  
            except Exception as e:
                print(f"Error while filling filters for class '{classe}' and date '{date}': {e}")
                error.log_error(classe, date, "fill_filters")
                continue

            # First check if there are links for download
            try:
                if link.present(driver, classe, date):    
                    # Download each found link
                    try:
                        link.download(driver, download_dir, classe, date)
                    except Exception:
                        print("app -> link.download()")
                        continue
                    
                    # Move the downloaded files to the respective folder or delete them if they already exist
                    try:
                        files.move_files(download_dir, classe, date, link.files_properly_downloaded)
                    except Exception:
                        print("app -> files.move_files()")
                        continue
            except Exception:
                print("app -> link.present()")
                continue

    # Display all errors
    try:
        error.display_error_log()
    except Exception as e:
        print(f"Error displaying error log: {e}")


    iterate_error_log(driver, download_dir)

main()