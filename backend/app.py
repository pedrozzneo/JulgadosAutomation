from datetime import datetime, timedelta
import form 
import link
import files
import error 
import driver as d

def scrape_errors(driver, download_dir):
    try:
        # Display the error log
        error.display()

        # Give it 3 times the len of error log to solve the errors
        for i in range(len(error.error_log) * 3):
            # Display the error log 
            error.display()
            
            # Remove the first item to try to solve it and also recycle the error log
            entry =  error.error_log.pop(0) 
            
            # Split to extract class and date
            parts = entry.split(", ")
            classe = parts[0].split(": ")[1]
            date = parts[1].split(": ")[1]
            print(f"Trying to solve: {classe} on {date}")

            # Try to solve
            scrape(driver, classe, date, download_dir)
    except:
       raise

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

    except Exception as e:
        print(f"⚠️ Error while scraping {classe} on {date}: {e}")
        raise

def main():
    # List all classes to be searched
    classes = ["Ação Civil Pública", "Ação Civil de Improbidade Administrativa", "Ação Civil Coletiva", "Ação Popular", "Mandado de Segurança Coletivo", "Usucapião"]
    print(f"classes: {classes}")

    # List all dates to be searched
    startingDate = datetime.strptime("01/01/2019", "%d/%m/%Y")
    endDate = datetime.strptime("30/06/2019", "%d/%m/%Y")
    interval = (endDate - startingDate).days
    print(f"dates: from {startingDate} to {endDate}")

    # Set the download directory
    download_dir = r"C:\Users\nikao\Documents\Code\JulgadosAutomation\others\pdfs"

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
                
                # Scrape the current class and date
                scrape(driver, classe, date, download_dir)

                # Display the error log 
                error.display()

            except Exception:
                # Reset everything
                driver = d.reset(driver, download_dir)
                
        # Try to solve the errors in the error log
        try:
            scrape_errors(driver, download_dir)
        except:
            # Reset everything
            driver = d.reset(driver, download_dir)
    
    # Clean up empty folders (needs checking if it works)
    # files.delete_empty_dirs(download_dir)

main()