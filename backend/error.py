error_log = []

def log_error(classe, date, context):
    # Logs an error with details about the class and date.
    error_log.append(f"Class: {classe}, Date: {date}, Context: {context}")
    print(f"⚠️ {context}")

def display_error_log():
    # Displays the error log in a numbered format.
    if not error_log:
        print("No errors logged.")
    else:
        print("\nError Log:")
        for i, error in enumerate(error_log, start=1):
            print(f"{i}- {error}")

