from datetime import datetime, timedelta
import form 
import link
import files
import error 
import driver as d

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

def main():
    # List all classes to be searched
    classes = ["Ação Civil Pública", "Ação Civil de Improbidade Administrativa", "Ação Civil Coletiva", "Ação Popular", "Mandado de Segurança Coletivo", "Usucapião"]
    print(f"classes: {classes}")

    # List all dates to be searched
    startingDate = datetime.strptime("12/01/2017", "%d/%m/%Y")
    endDate = datetime.strptime("30/06/2017", "%d/%m/%Y")
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
            error.solve(driver, download_dir)
        except:
            # Reset everything
            driver = d.reset(driver, download_dir)
    
    # Clean up empty folders (needs checking if it works)
    # files.delete_empty_dirs(download_dir)

main()