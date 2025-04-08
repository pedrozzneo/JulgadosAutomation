from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
from datetime import datetime, timedelta
import shutil
import re
import fill_form as fill_form

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

month_dict = {
    "01": "Janeiro",
    "02": "Fevereiro",
    "03": "Março",
    "04": "Abril",
    "05": "Maio",
    "06": "Junho",
    "07": "Julho",
    "08": "Agosto",
    "09": "Setembro",
    "10": "Outubro",
    "11": "Novembro",
    "12": "Dezembro"
}
def get_month_name(date_str):
    # Converts month number to month name
    month_num = date_str[3:5]
    return month_dict.get(month_num, "Invalid month")

def extract_numbers(texto):
    padrao = r"Resultados (\d+) a (\d+) de (\d+)"
    match = re.search(padrao, texto)
    
    if match:
        primeiro_numero = int(match.group(2))
        ultimo_numero = int(match.group(3))
        return primeiro_numero, ultimo_numero
    else:
        context = "extract_numbers"
        log_error("Regex", "Failed to extract numbers", context)
        return None, None 
def is_file_downloaded(download_dir, timeout=30, file_extension=None):
    start_time = time.time()
    while time.time() - start_time < timeout:
        # Get the list of files in the download directory
        files = [f for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
        
        if files:
            # Sort files by modification time (most recent first)
            files = sorted(files, key=lambda f: os.path.getmtime(os.path.join(download_dir, f)), reverse=True)
            most_recent_file = files[0]
            
            # Check if the most recent file matches the expected extension (if provided)
            if file_extension:
                if most_recent_file.endswith(file_extension):
                    return True
            else:
                return True
        
        # Wait for a short time before checking again
        time.sleep(1)
    
    return False
def download(driver, download_dir, classe, current_date_str):
    try:
        # Check if there are no results for the search without throwing an error
        try:
            no_results_message = driver.find_element(By.XPATH, "//div[contains(@class, 'aviso espacamentoCimaBaixo centralizado fonteNegrito') and contains(text(), 'Não foi encontrado nenhum resultado correspondente à busca realizada.')]")
            if no_results_message:
                print("-> No results found for the search.")
                return
        except Exception:
            pass

        # Otherwise...
        all_a_tags = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@title='Visualizar Inteiro Teor']"))
        )
        print(f"-> Found {len(all_a_tags)} links")

        # Locate the element containing the results information
        results_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//td[@bgcolor='#EEEEEE' and contains(text(), 'Resultados')]"))
        )
        print(f"-> Found results element: {results_element.text}")
        numbers = extract_numbers(results_element.text)
        print(f"-> First number: {numbers[0]}, Last number: {numbers[1]}")

        if len(all_a_tags) != numbers[0]:
            context = "download"
            print(f"-> Mismatch: Found {len(all_a_tags)} links, but expected {numbers[0]}.")
            log_error(classe, current_date_str, context)
            return
        
        for a in all_a_tags:
            a.click()
            driver.switch_to.window(driver.window_handles[-1])

            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)

            download_button = driver.find_element(By.ID, "download")
            download_button.click()
            print(f"✅ Download button clicked")

            # Wait for the file to be downloaded
            # if not is_file_downloaded(download_dir, timeout=30, file_extension=".pdf"):
            #     context = "is_file_downloaded"
            #     print("-> File download timed out.")
            #     log_error(classe, current_date_str, context)

            driver.switch_to.default_content()
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        print(f"-> Downloaded {len(all_a_tags)} files.")
        move_files(download_dir, classe, current_date_str, len(all_a_tags))
    
    except:
        context = "download"
        log_error(classe, current_date_str, context)
        print(f"Error while downloading files.")
        reset(driver)

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
    # if not os.path.exists(download_dir):
    #     os.makedirs(download_dir)

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
            download(driver, download_dir, classe, current_date_str)

    # Display all errors
    display_error_log()

if __name__ == "__main__":
    main()