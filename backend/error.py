import app

error_log = []

def log(classe, date, context):
    # Logs an error with details about the class and date.
    error_log.append(f"Class: {classe}, Date: {date}, Context: {context}")
    print(f"⚠️ {context}")

def display():
    # Displays the error log in a numbered format.
    if not error_log:
        print("No errors logged.")
    else:
        print("\nError Log:")
        for i, error in enumerate(error_log, start=1):
            print(f"{i}- {error}")

def solve(driver, download_dir):
    try:
        # Display the error log
        display()

        # Give it 3 times the len of error log to solve the errors
        for i in range(len(error_log) * 3):
            # Display the error log 
            display()
            
            # Remove the first item to try to solve it and also recycle the error log
            entry = error_log.pop(0) 
            
            # Split to extract class and date
            parts = entry.split(", ")
            classe = parts[0].split(": ")[1]
            date = parts[1].split(": ")[1]
            print(f"Trying to solve: {classe} on {date}")

            # Try to solve
            app.scrape(driver, classe, date, download_dir)
    except:
       raise