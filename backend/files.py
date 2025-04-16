import os
import shutil
import error as error

month_dict = {
    "01": "Janeiro",
    "02": "Fevereiro",
    "03": "Março",
    "04": "Abril",
    "05": "Maio",
    "06": "Junho",
    "07": "Julho",
    "08": "Agosto",
    "09": "Setembro",
    "10": "Outubro",
    "11": "Novembro",
    "12": "Dezembro"
}

def get_month_name(date_str):
    # Converts month number to month name
    month_num = date_str[3:5]
    return month_dict.get(month_num, "Invalid month")

def move_files(download_dir, classe, date, quantityOfFiles):
    try:
        # Handle special case for "Usucapião"
        if classe == "Usucapião":
            classe = "Usucapião Especial Coletiva"

        # Create the directory for the current date and class if it doesn't exist
        dateDir = os.path.join(download_dir, str(classe), date.split("/")[2], get_month_name(date), date.replace("/", "-"))
        if not os.path.exists(dateDir):
            os.makedirs(dateDir)

        # Get the most recent downloaded files based on the counter
        files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
        most_recent_files = sorted(files, key=os.path.getctime, reverse=True)[:quantityOfFiles]

        # Move the most recent files to the current date directory
        for file in most_recent_files:
            destination = os.path.join(dateDir, os.path.basename(file))
            if not os.path.exists(destination):
                shutil.move(file, destination)
                print(f"-> Moved {file} to {destination}")
            else:
                print(f"-> File {destination} already exists. Deleting it")
                os.remove(file)

    except FileNotFoundError as e:
        error.log_error(classe, date, "move_files: File not found")
        print(f"FileNotFoundError: {e}")
    except PermissionError as e:
        error.log_error(classe, date, "move_files: Permission error")
        print(f"PermissionError: {e}")
    except Exception as e:
        error.log_error(classe, date, "move_files: General error")
        print(f"Error while moving files: {e}")