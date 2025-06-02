from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import form 
import link
import files
import error 

def set_driver(download_dir):
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

def scrape(driver, classe, date, download_dir):
    try:
        # Calculate the date for the current iteration and show important information
        print(f"\n{classe.upper()} ON {date.upper()}: \n")

        # Fill out forms's fillters
        form.fill_filters(driver, classe, date)  

        # Check if there are links for download
        if link.present(driver, classe, date): 
            # Download each found link
            link.download(driver, download_dir, classe, date)

            # Move the downloaded files to the respective folder or delete them if they already exist
            files.move_files(download_dir, classe, date, link.files_properly_downloaded)

    except Exception:
        raise

def iterate_error_log(driver, download_dir):
    # Display the error log
    error.display_error_log()

    # Give it 3 times the len of error log to solve the errors
    for i in range(len(error.error_log) * 3):
        # Display the error log every 20 iterations
        if i % 20 == 0:
            error.display_error_log()
        
        # Remove the first item to try to solve it and also recycle the error log
        entry = error.error_log.pop(0) 
        
        # Split to extract class and date
        parts = entry.split(", ")
        classe = parts[0].split(": ")[1]
        date = parts[1].split(": ")[1]
        print(f"Trying to solve: {classe} on {date}")

        # Try to solve
        scrape(driver, classe, date, download_dir)

def main():
    # List all classes to be searched
    classes = ["Ação Civil Pública", "Ação Civil de Improbidade Administrativa", "Ação Civil Coletiva", "Ação Popular", "Mandado de Segurança Coletivo", "Usucapião"]
    print(f"classes: {classes}")

    # List all dates to be searched
    startingDate = datetime.strptime("01/01/2020", "%d/%m/%Y")
    endDate = datetime.strptime("31/12/2020", "%d/%m/%Y")
    print(f"dates: from {startingDate} to {endDate}")

    # Calculate the interval between start_date and end_date
    interval = (endDate - startingDate).days
    
    # Temporary download directory before being moved to the specific date folder
    download_dir = r"C:\Users\nikao\Documents\pdfs"

    # Set the WebDriver
    driver = set_driver(download_dir)
    driver.get("https://esaj.tjsp.jus.br/cjpg")
    #driver.maximize_window()

    # Loop through each class and date
    for classe in classes:
        for i in range(interval + 1):
            try:
                # Calculate the date for the current iteration and format it
                date = (startingDate + timedelta(days=i)).strftime("%d/%m/%Y")
                
                # Scrape the current class and date
                scrape(driver, classe, date, download_dir)

                # Display the error log every 20 iterations
                if i % 20 == 0:
                    error.display_error_log()

            except Exception:
                # Reset everything
                driver.quit()
                driver = set_driver(download_dir)
                driver.get("https://esaj.tjsp.jus.br/cjpg")
                print("reset") 
                
        # Try to solve the error in the error log
        iterate_error_log(driver, download_dir)
    
    # Clean up empty folders (needs checking if it works)
    # files.delete_empty_dirs(download_dir)

main()