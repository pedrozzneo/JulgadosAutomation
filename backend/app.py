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

# Global list to store error logs
error_log = []

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
    month_num = date_str[3:5]
    return month_dict.get(month_num, "Invalid month")

def log_error(classe, date, error_message):
    """Logs an error with details about the class, date, and error message."""
    error_log.append({
        "class": classe,
        "date": date,
        "error": error_message
    })

def search_and_select_popup(driver, classe):
    try:
        clear = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "botaoLimpar_classe"))
        )
        clear.click()

        popup = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "botaoProcurar_classe"))
        )
        popup.click()

        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "classe_treeSelectFilter"))
        )
        search_input.clear()
        search_input.send_keys(classe)
        search_input.send_keys(Keys.RETURN)
        print(f"-> Searched for the class: {classe}")

        checkbox = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'checkable') and text()='{classe}']"))
        )
        checkbox.click()
        print(f"-> Selected the checkbox for class: {classe}")

        selecionar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Selecionar' and contains(@class, 'spwBotaoDefaultGrid')]"))
        )
        selecionar_button.click()
        print("-> Clicked on the 'Selecionar' button")

    except Exception as e:
        log_error(classe, None, f"Error in search_and_select_popup: {e}")
        print(f"Error while searching and selecting the class '{classe}': {e}")

def fill(driver, classe, current_date_str):
    try:
        search_and_select_popup(driver, classe)

        start_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "iddadosConsulta.dtInicio"))
        )
        start_date.clear()
        start_date.send_keys(current_date_str)
        print(f"-> Filled the start date: {current_date_str}\n")

        end_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "iddadosConsulta.dtFim"))
        )
        end_date.clear()
        end_date.send_keys(current_date_str)
        print(f"-> Filled the end date {current_date_str}\n")

        consultar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "pbSubmit"))
        )
        consultar_button.click()
        print(f"-> Searched\n")

    except Exception as e:
        log_error(classe, current_date_str, f"Error in fill function: {e}")
        print(f"Error while filling the form or searching: {e}")

def download(driver, download_dir, classe, current_date_str):
    # Check if there are no results for the search, this is a faster way to evaluate and move on with the program
    try:
        no_results_message = WebDriverWait(driver, 1).until(
            EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'aviso espacamentoCimaBaixo centralizado fonteNegrito') and contains(text(), 'Não foi encontrado nenhum resultado correspondente à busca realizada.')]"))
        )
        if no_results_message:
            print("No results found for the search.")
            return
        
    except Exception:
        pass

    try:
        all_a_tags = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//a[@title='Visualizar Inteiro Teor']"))
        )
        print(f"-> Found {len(all_a_tags)} links\n on this page")
        counter = 0

        for a in all_a_tags:
            a.click()
            driver.switch_to.window(driver.window_handles[-1])

            iframe = driver.find_element(By.TAG_NAME, "iframe")
            driver.switch_to.frame(iframe)

            download_button = driver.find_element(By.ID, "download")
            download_button.click()
            print(f"✅ Download button clicked")

            driver.switch_to.default_content()
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            counter += 1

        if counter != 0:
            print(f"-> Downloaded {counter} files.")
            move_files(download_dir, classe, current_date_str, counter)

    except Exception as e:
        log_error(classe, current_date_str, f"Error in download function: {e}")
        print(f"Error while downloading files: {e}")

def move_files(download_dir, classe, current_date_str, counter):
    try:
        # Create the directory for the current date and class if it doesn't exist
        current_date_dir = os.path.join(download_dir, str(classe), current_date_str.replace("/", "-"))
        if not os.path.exists(current_date_dir):
            os.makedirs(current_date_dir)
            time.sleep(2)

        # Get the most recent downloaded files based on the counter
        files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
        most_recent_files = sorted(files, key=os.path.getctime, reverse=True)[:counter]

        # Move the most recent files to the current date directory
        for file in most_recent_files:
            destination = os.path.join(current_date_dir, os.path.basename(file))
            if not os.path.exists(destination):
                shutil.move(file, destination)
                print(f"-> Moved {file} to {destination}")
                time.sleep(2)
            else:
                print(f"-> File {destination} already exists. Deleting it")
                os.remove(file)

    except Exception as e:
        log_error(classe, current_date_str, f"Error in move_files function: {e}")
        print(f"Error while moving files: {e}")

def main():
    URL = "https://esaj.tjsp.jus.br/cjpg"

    # Extract the first column into the classes list
    classes = ["Ação Civil de Improbidade Administrativa"]
    print(f"classes: {classes}")

    dataInicio = datetime.strptime("27/01/2025", "%d/%m/%Y")
    dataFinal = datetime.strptime("02/02/2025", "%d/%m/%Y")

    # Calculate the interval between start_date and end_date
    interval =  dataFinal - dataInicio

    # Temporary download directory before being moved to the specific date folder
    download_dir = r"C:\Users\nikao\Desktop\TJ\docs\pdfs"
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    # Set Chrome options
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "plugins.always_open_pdf_externally": True
    })

    # Start WebDriver 
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    driver.get(URL)
    driver.implicitly_wait(20)
    driver.maximize_window()

    # Loop through each class and date range
    for classe in classes:
        # Loop through each date in the range
        for i in range(interval.days + 1):
            current_date_str = (dataInicio + timedelta(days=i)).strftime("%d/%m/%Y")
            print(f"{classe} on {current_date_str}: \n")
            fill(driver, classe, current_date_str)
            download(driver, download_dir, classe, current_date_str)

if __name__ == "__main__":
    main()