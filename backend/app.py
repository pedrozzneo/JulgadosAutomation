from datetime import datetime, timedelta
import form 
import link
import files
import error 
import driver as d
import time

def scrape_errors(driver, download_dir):
    try:
        # Display the error log 
        # error.display()

        # Know how many errors are in the error log
        quantity = len(error.errors)
        print(f"Number of errors to solve: {quantity}")
        
        # If there are no errors, just return
        if quantity == 0:
            return
        
        # Give it 3 times the len of error log to solve the errors
        for i in range(quantity):
            # Remove the first item to try to solve it and also recycle the error log
            classe = error.errors[i].get("classe")
            date = error.errors[i].get("date")
            
            # Split to extract class and date
            print(f"Trying to solve: {classe} on {date}")

            # Try to solve
            scrape(driver, classe, date, download_dir)
            time.sleep(5)  # Sleep for a second to avoid overwhelming the server
    except:
        raise

def scrape(driver, classe, date, download_dir):
    try:
        # Fill out forms's fillters
        form.fill_filters(driver, classe, date)  

        # Check if there are links for download
        if link.present(driver, classe, date): 
            # Download each found link
            link.download(driver, download_dir, classe, date)

            # Move the downloaded files to the respective folder or delete them if they already exist
            files.move_files(download_dir, classe, date, link.files_properly_downloaded)

    except Exception as e:
        print(f"⚠️ Error while scraping {classe} on {date}: {e}")
        raise

def main():
    # List all classes to be searched
    classes = ["Ação Civil Pública", "Ação Civil de Improbidade Administrativa", "Ação Civil Coletiva", "Ação Popular", "Mandado de Segurança Coletivo", "Usucapião"]
    #classes = ["Ação Civil Coletiva", "Ação Popular", "Mandado de Segurança Coletivo", "Usucapião"]
    print(f"classes: {classes}")

    # List all dates to be searched
    startingDate = datetime.strptime("08/01/2019", "%d/%m/%Y")
    endDate = datetime.strptime("31/12/2019", "%d/%m/%Y")
    interval = (endDate - startingDate).days
    print(f"dates: from {startingDate} to {endDate}")

    # Set the download directory
    download_dir = r"G:\Meu Drive\Julgados"

    # Set the WebDriver
    driver = d.set(download_dir)
    driver.get("https://esaj.tjsp.jus.br/cjpg")
    #driver.maximize_window()

    # Loop through each class and date
    for classe in classes:
        for i in range(interval + 1):
            try:
                # Calculate the date for the current iteration and format it
                date = (startingDate + timedelta(days=i)).strftime("%d/%m/%Y")
                
                # Display the class and date being scraped
                print(f"\n{classe.upper()} ON {date.upper()}: \n")

                # Scrape the current class and date
                scrape(driver, classe, date, download_dir)
            except Exception:
                # Reset everything
                driver = d.reset(driver, download_dir)
            finally:
                # Display the error log 
                error.display()
                
        try:
            # Try to solve the errors in the error log 
            scrape_errors(driver, download_dir)
        except Exception:
            # Reset everything
            driver = d.reset(driver, download_dir)

    # # Clean up empty folders (needs checking if it works)
    # files.delete_empty_dirs(download_dir)

main()