from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timedelta
import fill_form as fill_form
import downloads as downloads
import os

error_log = []
def log_error(classe, date, context):
    # Logs an error with details about the class and date.
    error_log.append(f"Class: {classe}, Date: {date}, Context: {context}")
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

def main():
    URL = "https://esaj.tjsp.jus.br/cjpg"

    # List all classes to be searched
    classes = ["Ação Civil Pública", "Ação Civil de Improbidade Administrativa", "Ação Civil Coletiva", "Ação Popular", "Mandado de Segurança Coletivo", "Usucapião"]
    print(f"classes: {classes}")

    dataInicio = datetime.strptime("01/01/2025", "%d/%m/%Y")
    dataFinal = datetime.now()
    print(f"dates: from {dataInicio} to {dataFinal}")

    # Calculate the interval between start_date and end_date
    interval = dataFinal - dataInicio
    print(interval.days)

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
            current_date_str = (dataInicio + timedelta(days=i)).strftime("%d/%m/%Y")
            print(f"\n{classe.upper()} ON {current_date_str.upper()}: \n")
            fill_form.fill(driver, classe, current_date_str)
            downloads.download(driver, download_dir, classe, current_date_str)

    # Display all errors
    display_error_log()

if __name__ == "__main__":
    main()