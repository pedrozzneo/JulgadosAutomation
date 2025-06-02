from fill_filters import fill_filters
from download import download
from files import move_files
from error import errors, display, log
from app import ThereAreFileLinks
from error import error

counter = 0
while error.error_log:
    counter += 1
    if counter % 20 == 0:
        # Display all errors
        try:
            error.display_error_log()
        except Exception as e:
            print(f"Error displaying error log: {e}")
                
    entry = errors.pop(0)  # Remove the first item
    # Example format: "Class: Usucapiao, Date: 2025-04-15, Context: fill_filters: TimeOutException"
    
    # Split and extract
    parts = entry.split(", ")
    classe = parts[0].split(": ")[1]
    date = parts[1].split(": ")[1]

    # Use them
    print("Class:", classe)
    print("Date:", date)

    # Fill out all the filters
    try:
        fill_filters(driver, classe, date)
    except Exception as e:
        print(f"Error while filling filters for class '{classe}' and date '{date}': {e}")
        log(classe, date, "fill_filters")
        continue
        
    # Check if there are links for download before starting the whole process
    try:
        if ThereAreFileLinks(driver):
            download(driver, download_dir, classe, date)
            try:
                move_files(download_dir, classe, date, files_properly_downloaded)
            except Exception as e:
                print(f"Error while moving files for class '{classe}' and date '{date}': {e}")
                log(classe, date, "move_files")
                continue
    except Exception as e:
        print(f"Error while checking for file links or downloading files for class '{classe}' and date '{date}': {e}")
        log(classe, date, "ThereAreFileLinks or download")
        continue
