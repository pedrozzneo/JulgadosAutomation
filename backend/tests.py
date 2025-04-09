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
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def more_download_links_pages(driver):
    try:
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


def find_element_in_all_frames(driver):
    driver.switch_to.default_content()
    frames = driver.find_elements(By.TAG_NAME, "frame") 
    print(f"🔍 Found {len(frames)} iframe(s). Trying each...")

    # Try each iframe
    for index, iframe in enumerate(frames):
        try:
            driver.switch_to.default_content()
            driver.switch_to.frame(iframe)
            print(f"🔎 Searching in iframe index {index}...")
             # Locate the element containing all the info about downloads
            fullDownloadsMessage = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//td[@bgcolor='#EEEEEE' and contains(text(), 'Resultados')]"))
            )
            print(f"✅ Element found in iframe index {index}")
            return fullDownloadsMessage
        
        except TimeoutException:
            print(f"❌ Not found in iframe index {index}")
            continue

    driver.switch_to.default_content()
    print("🚫 Element not found in any frame.")
    return None
        
def main():
    URL = "http://esaj.tjsp.jus.br/cjpg/pesquisar.do?conversationId=&dadosConsulta.pesquisaLivre=&tipoNumero=UNIFICADO&numeroDigitoAnoUnificado=&foroNumeroUnificado=&dadosConsulta.nuProcesso=&dadosConsulta.nuProcessoAntigo=&classeTreeSelection.values=8537&classeTreeSelection.text=A%C3%A7%C3%A3o+Civil+P%C3%BAblica&assuntoTreeSelection.values=&assuntoTreeSelection.text=&agenteSelectedEntitiesList=&contadoragente=0&contadorMaioragente=0&cdAgente=&nmAgente=&dadosConsulta.dtInicio=01%2F01%2F2025&dadosConsulta.dtFim=15%2F01%2F2025&varasTreeSelection.values=&varasTreeSelection.text=&dadosConsulta.ordenacao=DESC"

    # Start WebDriver
    driver = webdriver.Chrome()
    driver.get(URL)
    driver.maximize_window()

    while more_download_links_pages(driver):
        element = find_element_in_all_frames(driver)
        print(element)
        time.sleep(5)

main()