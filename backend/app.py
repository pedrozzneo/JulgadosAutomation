from datetime import datetime, timedelta
import form 
import link
import files
import error 
import driver as d

result = None
download_dir = r"G:\Meu Drive\JulgadosBackup\moveDir"
driver = d.set(download_dir)

def solve_errors(driver, download_dir):
    try:
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
            scrape(classe, date, download_dir)
    except:
        raise

def scrape(classe, date, download_dir):
    try:
        # alawys keep track of this WebElement to tell wheter we have or not downloadLinks to process
        global result

        # alawys keep track of the driver because the resets (changes it) can be perpetuated across functions
        global driver

        # Track the time from filling the forms to processing the results
        timeBeforeForms = datetime.now()

        # Fill out forms's fillters
        form.fill_filters(driver, classe, date)  

        # Collect the result if we have or not download links to process
        result = link.present(driver, classe, date, result)
        
        # Finally find out the time it took to process the forms
        timeAfterResult = datetime.now()
        timeTaken = timeAfterResult - timeBeforeForms

        # If it took too long, reset the driver and try again untill it works out as it causes bug
        if timeTaken > timedelta(seconds=10) and classe != "Usucapião":
            print(f"-> Forms took too long to process: {timeTaken}. Resetting driver.")
            driver = d.reset(driver, download_dir)
            scrape(classe, date, download_dir) 
            return
        else:
            print(f"-> Forms processed in {timeTaken}")
        
        # Situation with links to download
        if result.tag_name == "a":
            # Download the links
            link.download(driver, download_dir, classe, date)

            # Move the downloaded files to the respective folder or delete them if they already exist
            files.move_files(download_dir, classe, date, link.files_properly_downloaded)
        else:
            print("NO download links")

    except Exception as e:
        result = None
        raise

def main():
    # List all classes to be searched
    classes = ["Ação Civil Pública", "Ação Civil de Improbidade Administrativa", "Ação Civil Coletiva", "Ação Popular", "Mandado de Segurança Coletivo", "Usucapião"]
    
    print(f"classes: {classes}")

    # List all dates to be searched
    startingDate = datetime.strptime("30/09/2025", "%d/%m/%Y")
    endDate = datetime.strptime("31/10/2025", "%d/%m/%Y")
    interval = (endDate - startingDate).days
    print(f"dates: from {startingDate} to {endDate}")

    # Set the download directory
    download_dir = r"G:\Meu Drive\JulgadosBackup\moveDir"

    # Acess the main page
    global driver
    driver.get("https://esaj.tjsp.jus.br/cjpg/")

    # Loop through each class and date
    for classe in classes:
        for i in range(interval + 1):
            try:
                # Calculate the date for the current iteration and format it
                date = (startingDate + timedelta(days=i)).strftime("%d/%m/%Y")

                # Display the class and date being scraped
                print(f"\n{classe.upper()} ON {date.upper()}: \n")

                # Scrape the current class and date
                scrape(classe, date, download_dir)
                
            except Exception:
                # Reset everything
                driver = d.reset(driver, download_dir)

            finally:
                # Clear the download dir and display the errors so far
                files.clear_directory(download_dir)
                error.display()
        try:
            # Try to solve the errors in the error log 
            solve_errors(driver, download_dir)
        except Exception:
            # Reset everything
            driver = d.reset(driver, download_dir)
main()