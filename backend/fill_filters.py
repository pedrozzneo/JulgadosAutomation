from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import error as error
import time

def wait(driver, id, timeout=10):
    return WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((By.ID, id)))

def fill_classe(driver, classe, date):
    try:
        clearButton = wait(driver, id="botaoLimpar_classe")
        clearButton.click()

        searchButton = wait(driver, id="botaoProcurar_classe")
        searchButton.click()

        search_input = wait(driver, id="classe_treeSelectFilter")
        search_input.send_keys(classe)
        search_input.send_keys(Keys.RETURN)

        # checkboxClass = wait(driver, id="classe_tree_node_10460")
        # checkboxClass.click()

        # selecionarButton = wait(driver, id="botaoSelecionar_classe")
        # selecionarButton.click()

        checkboxClass = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, f"//span[contains(@class, 'checkable') and text()='{classe}']"))
        )
        checkboxClass.click()

        selecionarButton = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='button' and @value='Selecionar' and contains(@class, 'spwBotaoDefaultGrid')]"))
        )
        selecionarButton.click()

    except TimeoutException:
        error.log_error(classe, date, context="fill_filters -> fill_classe: TimeoutException")
        print(f"❌ Timeout in fill_filter -> fill_classe: {classe} on {date}: TimeoutException")
        raise 
    except Exception as e:
        error.log_error(classe, date, context="fill_filters -> fill_classe")
        print(f"❌ Error in fill_filter -> fill_classe: {classe} on {date}: {e}")
        raise

def fill_date(driver, current_date_str):
    try:
        clearButton = wait(driver, id="botaoLimpar_data")
        clearButton.click()

        start_date = wait(driver, id="iddadosConsulta.dtInicio")
        start_date.clear()
        start_date.send_keys(current_date_str)

        end_date = wait(driver, id="iddadosConsulta.dtFim")
        end_date.clear()
        end_date.send_keys(current_date_str)

    except TimeoutException:
        error.log_error("Date", current_date_str, context="fill_filters -> fill_date: TimeoutException")
        print(f"❌ Timeout in fill_filter -> fill_date: {current_date_str}: TimeoutException")
        raise
    except Exception as e:
        error.log_error("Date", current_date_str, context="fill_filters -> fill_date")
        print(f"❌ Error in fill_filter -> fill_date: {current_date_str}: {e}")
        raise

def submit(driver):
    try:
        consultar_button = wait(driver, id="pbSubmit")
        consultar_button.click()

    except TimeoutException:
        error.log_error("Submit", "N/A", context="fill_filters -> submit: TimeoutException")
        print(f"❌ Timeout in fill_filter -> submit: TimeoutException")
        raise
    except Exception as e:
        error.log_error("Submit", "N/A", context="fill_filters -> submit")
        print(f"❌ Error in fill_filter -> submit: {e}")
        raise

def fill_assunto(classe, driver):
    try:
        clearButton = wait(driver, id="botaoLimpar_assunto")
        clearButton.click()

        searchButton = wait(driver, id="botaoProcurar_assunto")
        searchButton.click()

        search_input = wait(driver, id="assunto_treeSelectFilter")
        search_input.send_keys("especial coletiva")
        search_input.send_keys(Keys.RETURN)

        checkboxAssunto = wait(driver, id="assunto_tree_node_10460")
        checkboxAssunto.click()

        selecionarButtonAssunto = wait(driver, id="botaoSelecionar_assunto")
        selecionarButtonAssunto.click()

    except TimeoutException:
        error.log_error(classe, "N/A", context="fill_filters -> fill_assunto: TimeoutException")
        print(f"❌ Timeout in fill_filter -> fill_assunto: {classe}: TimeoutException")
    except Exception as e:
        error.log_error(classe, "N/A", context="fill_filters -> fill_assunto")
        print(f"❌ Error in fill_filter -> fill_assunto: {classe}: {e}")

def fill_filters(driver, classe, date):
    try:
        print(f"Filling filters for class: {classe} and date: {date}")
        fill_classe(driver, classe, date)
        print(f"✅ Fill: {classe}")
        fill_date(driver, date)

        if classe == "Usucapião":  
            fill_assunto(classe, driver)

        submit(driver)
        print(f"✅ Fill: {classe} and {date}")

    except TimeoutException:
        error.log_error(classe, date, context="fill_filters: TimeoutException")
        print(f"❌ Timeout in fill_filters: {classe} and {date}: TimeoutException")
    except Exception as e:
        error.log_error(classe, date, context="fill_filters")
        print(f"❌ Error in fill_filters: {classe} and {date}: {e}")
