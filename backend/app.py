from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import os
import fill_filters as fill_filters
import download as download
import files as files
import error as error

def ThereAreFileLinks(driver):
     # The "no_results_message" tells whether we have avaiable file's links, if its found, then we skip, but if its not, it throws an error, meaning we have links  to download
        try:
            no_results_message = driver.find_element(By.XPATH, "//div[contains(@class, 'aviso espacamentoCimaBaixo centralizado fonteNegrito') and contains(text(), 'Não foi encontrado nenhum resultado correspondente à busca realizada.')]")
            if no_results_message:
                print("NO files for download")
                return False
        except Exception:
            print("-> There are files for download'.")
            return True
        
def main():
    URL = "https://esaj.tjsp.jus.br/cjpg"

    # List all classes to be searched
    classes = ["Ação Civil Pública", "Ação Civil de Improbidade Administrativa", "Ação Civil Coletiva", "Ação Popular", "Mandado de Segurança Coletivo", "Usucapião"]
    print(f"classes: {classes}")

    startingDate = datetime.strptime("07/01/2025", "%d/%m/%Y")
    endDate = datetime.now()
    print(f"dates: from {startingDate} to {endDate}")

    # Calculate the interval between start_date and end_date
    interval = endDate - startingDate

    # Temporary download directory before being moved to the specific date folder
    download_dir = r"C:\Users\nikao\Desktop\Julgados"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Set Chrome options
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
    })

    # Start WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    driver.maximize_window()

    # Loop through each class and date range
    for classe in classes:
        # Loop through each date in the range
        for i in range(interval.days + 1):
            date = (startingDate + timedelta(days=i)).strftime("%d/%m/%Y")
            print(f"\n{classe.upper()} ON {date.upper()}: \n")
            
            # fill out all the fillters
            fill_filters.fill_filters(driver, classe, date)
            
            # Check if there are links for download before starting the whole process
            if ThereAreFileLinks(driver):
                download.download(driver, download_dir, classe, date)
                files.move_files(download_dir, classe, date, download.files_properly_downloaded)

    # Display all errors
    error.display_error_log()

main()