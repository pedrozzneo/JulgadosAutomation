
-> on any except, call the " display error log"

-> DELETS ONE PAGED PDFS:

import PyPDF2
import os

def count_pdf_pages(file_path):
                    try:
                        with open(file_path, 'rb') as pdf_file:
                            reader = PyPDF2.PdfReader(pdf_file)
                            return len(reader.pages)
                    except Exception as e:
                        print(f"Error while counting pages in {file_path}: {e}")
                        return 0


base_dir = "C:\\Users\\nikao\\Documents\\Julgados"

for root, dirs, Classefiles in os.walk(base_dir):
    for Classefile in Classefiles:
        for moreFile in file:
            if file.endswith(".pdf"):
                path = os.path.join(root, file)
                print(f"Processing file: {path}")
                count_pdf_pages(path)


-> resets the page in fill

def reset(driver):
    try:
        print("-> Resetting the WebDriver...")
        URL = "https://esaj.tjsp.jus.br/cjpg"
        driver.get(URL)
        driver.maximize_window()
    except Exception as e:
        print(f"Error during WebDriver reset: {e}")

check if im not deleting files that werent present on the directody that was interrupted, see if it compares the value of the file and not only the existance of the directory
store the all info from the last run of the program to handle accordingly: what classes were supposed to run, their dates, where it stoped, a flag if I downloaded all of the files, If I didnt how many...
when they dont find the element, just skip it and (wrap it in a try catch)
also wait for everything to load

<a name="2" title="Próxima página" class="esajLinkLogin">
				&gt;
			</a>


  # After downloading the file, count its pages
                # downloaded_file_path = os.path.join(download_dir, os.listdir(download_dir)[-1])  # Assuming the last file is the downloaded one
                # page_count = count_pdf_pages(downloaded_file_path)
                # print(f"✅ PDF has {page_count} pages")