import PyPDF2
import os
import shutil 

# Checks if a PDF has a specific word in its text.
def check_pdf_for_word(pdf_path, word_to_find):
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            num_pages = len(reader.pages)

            for page_num in range(num_pages):
                page = reader.pages[page_num]
                text = page.extract_text().lower()

            #print(text)

            if text and word_to_find.lower() in text:
                return True 
            else:
                return False
    except Exception as e:
        print(f"Error processing '{pdf_path}': {e}")
        return False 

# Directory where the script will look for PDF files.
download_dir = r"C:\Users\nikao\Documents\Code\JulgadosAutomation\others\pdfs"

# Dir where the results will be stored.
key_dir = r"C:\Users\nikao\Documents\save"

# Keys to look for in the PDFs
words_to_find = ["estrutural", "estruturais"]

print(f"Starting search for words {words_to_find} in PDFs under: {download_dir}\n")

# Walk through the directory tree to find all PDF files
for root, dirs, files in os.walk(download_dir):
    for file_name in files:
        if file_name.lower().endswith(".pdf"):
            pdf_full_path = os.path.join(root, file_name)

            print(f"Checking PDF: {file_name}")

            # For each PDF, check for each word in your list
            for word in words_to_find:
                if check_pdf_for_word(pdf_full_path, word):
                    print(f"  '{word}': ✅ Found")

                    # Define the destination directory for this specific keyword
                    destination_keyword_dir = os.path.join(key_dir, word)

                    # Create the keyword-specific directory if it doesn't exist
                    try:
                        os.makedirs(destination_keyword_dir, exist_ok=True)
                    except Exception as e:
                        print(f"    Error creating keyword directory '{destination_keyword_dir}': {e}")
                        continue # Skip copying for this word if directory creation fails

                    # Define the full destination path for the copied file
                    dest_file_path = os.path.join(destination_keyword_dir, file_name)

                    # Copy the PDF file
                    try:
                        shutil.copy2(pdf_full_path, dest_file_path)
                        print(f"    Copied to: {dest_file_path}")
                    except shutil.SameFileError:
                        print(f"    Skipped: '{pdf_full_path}' is already at '{dest_file_path}'")
                    except Exception as copy_e:
                        print(f"    Error copying '{pdf_full_path}' to '{dest_file_path}': {copy_e}")

                else: 
                    print(f"-> {word}': ❌ Found")

            # Visual separator
            print("-" * (len(pdf_full_path) + 20))