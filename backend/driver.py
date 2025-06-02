from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

def set(download_dir):
    # Set Chrome options
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
    })
    #options.add_argument("--headless")

    # Start WebDriver
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    return driver

def reset(driver, download_dir):
    # Reset the driver and navigate to the main page
    driver.quit()
    driver = set(download_dir)
    driver.get("https://esaj.tjsp.jus.br/cjpg")
    print("reset")
    return driver