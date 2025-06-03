from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import error as error

def fill_classe(driver, classe, date):
    try:
        clearButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "botaoLimpar_classe"))
        )
        clearButton.click()
        
        searchButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "botaoProcurar_classe"))
        )
        searchButton.click()

        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "classe_treeSelectFilter"))
        )
        search_input.send_keys(classe)
        search_input.send_keys(Keys.RETURN)

        checkboxClass = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'checkable') and text()='{classe}']"))
        )
        checkboxClass.click()

        selecionarButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Selecionar' and contains(@class, 'spwBotaoDefaultGrid')]"))
        )
        selecionarButton.click()

    except Exception as e:
        error.log(classe, date, context= "forms -> fill_classe")
        raise

def fill_date(driver, classe, date):
    try:   
        start_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "iddadosConsulta.dtInicio"))
        )
        start_date.clear()
        start_date.send_keys(date)

        end_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "iddadosConsulta.dtFim"))
        )
        end_date.clear()
        end_date.send_keys(date)
    
    except Exception as e:
        error.log(classe, date, context= "forms -> fill_date")
        raise

def submit(driver, classe, date):
    try:
        consultar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "pbSubmit"))
        )
        consultar_button.click()
    
    except Exception as e: 
        error.log(classe, date, context= "forms -> submit")
        raise

def fill_assunto(driver, classe, date):
    try:
        clearButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "botaoLimpar_assunto"))
        )
        clearButton.click()

        searchButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "botaoProcurar_assunto"))
        )
        searchButton.click()

        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "assunto_treeSelectFilter"))
        )
        search_input.send_keys("especial coletiva")
        search_input.send_keys(Keys.RETURN)

        checkboxAssunto = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[@id='assunto_tree_node_10460' and contains(@class, 'checkable')]"))
        )
        checkboxAssunto.click()

        selecionarButtonAssunto = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[@id='assunto_treeSelectContainer']//input[@type='button' and @value='Selecionar' and contains(@class, 'spwBotaoDefaultGrid')]"))
        )
        selecionarButtonAssunto.click()
    
    except Exception as e: 
        error.log(classe, date, context= "forms -> fill_assunto")
        raise

def fill_filters(driver, classe, date):
    try:
        print("-> Filling form...")
        fill_classe(driver, classe, date)
        fill_date(driver, classe, date)
        if classe == "Usucapião":  # Only for "Usucapião" class
            fill_assunto(driver, classe, date)
        submit(driver, classe, date)
        print("✅ Fill form")
    except Exception:
        raise

