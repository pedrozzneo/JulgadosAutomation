errors = []

def log(classe, date, context):
    # Show what went wrong
    print(f"⚠️ {context}")

    # Create a new error dict
    newError = {'classe': classe, 'date': date, 'context': [context]}

    # Check if we already have an error for the same class and date
    for error in errors:
        if error["classe"] == newError["classe"] and error["date"] == newError["date"]:
            error["context"].extend(newError["context"])
            return 

    # Insert completly new error
    errors.append(newError)

def display():
    # Displays the error log in a numbered format.
    if not errors:
        print("No errors logged.")
    else:
        print("\n❕❕Error Log❕❕:")
        for i, error in enumerate(errors, start=1):
            print(f"{i}- {error}")