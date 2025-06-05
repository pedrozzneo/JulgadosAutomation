import os
import shutil
import error as error

moveDir = r"C:\Users\nikao\Documents\Code\JulgadosAutomation\others\pdfs"

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

def count_files(download_dir):
    return sum(len(files) for _, _, files in os.walk(download_dir))

def get_month_name(date_str):
    # Converts month number to month name
    month_num = date_str[3:5]
    return month_dict.get(month_num, "Invalid month")

def move_files(download_dir, classe, date, quantityOfFiles):
    global moveDir
    print("moving the files...")
    
    try:
        # Handle special case for "Usucapião"
        if classe == "Usucapião":
            classe = "Usucapião Especial Coletiva"

        # Get the most recent downloaded files based on the counter
        files = [os.path.join(download_dir, f) for f in os.listdir(download_dir) if os.path.isfile(os.path.join(download_dir, f))]
        most_recent_files = sorted(files, key=os.path.getctime, reverse=True)[:quantityOfFiles]

        # Create the directory for the current date and class if it doesn't exist
        dateDir = os.path.join(moveDir, str(classe), date.split("/")[2], get_month_name(date), date.replace("/", "-"))
        if not os.path.exists(dateDir):
            os.makedirs(dateDir)

        # Move the most recent files to the current date directory
        for file in most_recent_files:
            destination = os.path.join(dateDir, os.path.basename(file))
            if not os.path.exists(destination):
                shutil.move(file, destination)
                print(f"-> Move {file} to {destination}")
            else:
                print(f"-> File {destination} already exists. Deleting it")
                os.remove(file)

    except FileNotFoundError as e:
        error.log(classe, date, "move_files: File not found")
        print(f"FileNotFoundError")
    except PermissionError as e:
        error.log(classe, date, "move_files: Permission error")
        print(f"PermissionError")
    except Exception as e:
        error.log(classe, date, "move_files: General error")
        print(f"Error while moving files")

# def delete_empty_dirs(download_dir, current_level=1, max_level=5):
#     if current_level > max_level:
#         return
#     # List all entries in the current directory
#     for entry in os.listdir(download_dir):
#         full_path = os.path.join(download_dir, entry)
#         if os.path.isdir(full_path):
#             delete_empty_dirs(full_path, current_level + 1, max_level)
#     # After processing subdirectories, check if current directory is empty
#     if current_level > 1 and not os.listdir(download_dir):
#         os.rmdir(download_dir)
#         print(f"Deleted empty directory: {download_dir}")
