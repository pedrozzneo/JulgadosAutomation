from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import error as error

def fill_classe(driver, classe, current_date_str):
    try:
        # All steps to fill the "Classe" field
        clearButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "botaoLimpar_classe"))
        )
        clearButton.click()
        print("-> Clicked on the 'Clear' button")

        searchButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "botaoProcurar_classe"))
        )
        searchButton.click()
        print("-> Clicked on the 'Search' button")

        search_input = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.ID, "classe_treeSelectFilter"))
        )
        search_input.send_keys(classe)
        search_input.send_keys(Keys.RETURN)
        print(f"-> Searched for the class: {classe}")

        checkboxClass = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'checkable') and text()='{classe}']"))
        )
        checkboxClass.click()
        print(f"-> Selected the checkbox for class: {classe}")

        selecionarButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Selecionar' and contains(@class, 'spwBotaoDefaultGrid')]"))
        )
        selecionarButton.click()
        print("-> Clicked on the 'Selecionar' button")

    except:
        context = "search_classe"
        error.log_error(classe, current_date_str, context)
        print(f"Error while searching and selecting the class '{classe}'.")
        error.reset(driver)

def fill_date(driver, current_date_str):
    try:   
        start_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "iddadosConsulta.dtInicio"))
        )
        start_date.clear()
        start_date.send_keys(current_date_str)
        print(f"-> Filled the start date: {current_date_str}")

        end_date = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "iddadosConsulta.dtFim"))
        )
        end_date.clear()
        end_date.send_keys(current_date_str)
        print(f"-> Filled the end date: {current_date_str}")
    
    except:
        context = "search_Date"
        log_error("Date", current_date_str, context)
        print(f"Error while filling the date fields.")
        reset(driver)

def submit(driver):
    try:
        consultar_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "pbSubmit"))
        )
        consultar_button.click()
        print(f"-> Consultar button clicked")
    
    except:
        context = "submit"
        error.log_error("Submit", "Failed to click the submit button", context)
        print(f"Error while clicking the submit button.")
        error.reset(driver)

def fill_assunto(classe, driver):
    clearButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "botaoLimpar_assunto"))
    )
    clearButton.click()
    print("-> Clicked on the 'Clear' button for 'assunto'")

    searchButton = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.ID, "botaoProcurar_assunto"))
    )
    searchButton.click()
    print("-> Clicked on the 'Search' button for 'assunto'")

    search_input = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.ID, "assunto_treeSelectFilter"))
    )
    search_input.send_keys("especial coletiva")
    search_input.send_keys(Keys.RETURN)
    print("-> Searched for 'especial coletiva' in 'assunto'")

    checkboxAssunto = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//span[@id='assunto_tree_node_10460' and contains(@class, 'checkable')]"))
    )
    checkboxAssunto.click()
    print("-> Selected the checkbox for 'Usucapião Especial Coletiva'")

    selecionarButtonAssunto = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//div[@id='assunto_treeSelectContainer']//input[@type='button' and @value='Selecionar' and contains(@class, 'spwBotaoDefaultGrid')]"))
    )
    print("-> Found the 'Selecionar' button for 'assunto'")
    selecionarButtonAssunto.click()
    print("-> Clicked on the 'Selecionar' button for 'assunto'")
    
def fill_filters(driver, classe, current_date_str):
    fill_classe(driver, classe, current_date_str)
    #fill_date(driver, current_date_str)
    if(classe == "Usucapião"): # Only for "Usucapião" class We gotta fill out the "assunto" field too
        fill_assunto(classe, driver) 
    submit(driver)