
#------------------------------------------------------*
# PROJECT:Automated file organizer and cleanup utility. |
# INTERNSHIP: datheon AI system and automation studio . |
# FILE NAME: organizer.py                               |
#------------------------------------------------------*

#step 1: Import the required python libraries.

import os
import shutil
import logging 
from pathlib import Path


# step 2: Select the folder we want to organize ,

# this uses the test_file folder beside organizer.py.
# later, you can change it to another folder you choose.


TARGET_FOLDER=Path(__file__).parent / "test_files"


#step 3: Map file extentions to category folders.


EXTENSION_MAP= {

    #documents
    ".pdf":"documents",
    ".txt":"documents",
    ".doc":"documents",
    ".docx":"documents",
    ".rtf":"documents",
    ".odt":"documents",

    #images
    ".jpg":"images",
    ".jpeg":"images",
    ".png":"images",
    ".gif":"images",
    ".bmp":"images",
    ".webp":"images",

    #videos
    ".mp4":"videos",
    ".mkv":"videos",
    ".mov":"videos",
    ".avi":"videos",

    #audio
    ".mp3":"audio",
    ".wav":"audio",
    ".aac":"audio",

    #archives
    ".zip":"archives",
    ".rar":"archives",
    ".7z":"archives",
    ".tar":"archives",

    #programming files
    ".py":"code",
    ".java":"code",
    ".css":"code",
    ".c":"code",
    ".js":"code",
    ".cpp":"code",
    ".html":"code",
}


#step 4 :Set up logging ,

# the log file is stored beside organizer.py,
# not inside the folder being organized.


LOG_FILE=Path(__file__).parent / "organizer.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE, encoding = "utf-8"),
        logging.StreamHandler()
    ]
)

#step 5 : Prevent duplicate filenames.

def get_unique_path(destination):

    #if the file name is not already present , use it.

    if not destination.exists():
        return destination

    #otherwise , try names such as photo_1.jpg,
    #photo_2.jpg, photo_3.jpg, and so on.

    counter = 1

    while True:
        new_name=(
            f"{destination.stem}_{counter}"
            f"{destination.suffix}"
        )

        new_path= destination.with_name(new_name)

        if not new_path.exists():
            return new_path

        counter += 1


# step 6 :Log errors encountered while scanning directories.

def log_scan_error(error):
    logging.error("Could not scan a directory: %s",error)

#step 7 : Create the main file-organizing function.    

def organize_files():
    moved=0
    skipped=0
    errors=0

    #Check whether the selected folder exists.

    if not TARGET_FOLDER.is_dir():
        logging.error(
            "Target folder does not exist : %s",
            TARGET_FOLDER
        )
        return

    logging.info("Starting file organization.")
    logging.info("Target folder: %s",TARGET_FOLDER)

    # Get the name of all the category folders.
    # These folders are created directly inside TARGET_FOLDER.

    category_names=set(EXTENSION_MAP.values())
    category_names.add("Other")


    #step 8 : Scan the directory tree recursively.
    # os.walk visits the target folder and its nested folders.


    for current_folder , subfolders, filenames in os.walk(
        TARGET_FOLDER,
        topdown=True,
        followlinks=False,
        onerror=log_scan_error
    ):
        current_path=Path(current_folder)


        #At the root only, skip the category folders that already exist,
        #this prevents repeated processing.


        if current_path==TARGET_FOLDER:
            subfolders[:]=[
                folder for folder in subfolders
                if folder not in category_names
                and not (current_path / folder).is_symlink()
            ]

        #step 9 : Process each file in the current folder.

        for filename in filenames:

            source = current_path / filename

            try:
                #skip symbolic links instead of moving them.
            
                if source.is_symlink():
                    skipped+=1
                    logging.info(
                        "Skipped symbolic links: %s",
                        source
                    )
                    continue

                #step 10: Identify the file extension.


                extension = source.suffix.lower()

                # Choose a category . unknown extensions are 
                # placed in the other folder.


                category = EXTENSION_MAP.get(
                    extension,
                    "Other"
                )
            

                #step 11: Create the destination folder
                #  directly inside the main target folder.

                category_folder= TARGET_FOLDER / category

                category_folder.mkdir(
                    parents=True,
                    exist_ok = True
                )

                #step 12:Generate a safe destination path.

                destination= get_unique_path(
                    category_folder / source.name
                )

                #step 13: Move the files.

                shutil.move(
                    str(source),
                    str(destination)
                )

                moved+=1

                logging.info(
                    "Moved %s -> %s",
                    source,
                    destination
                )

            except (
                PermissionError,
                FileNotFoundError,
                OSError,
                shutil.Error

            ) as error:

                errors+=1

                logging.error(
                    "Could not move %s : %s",
                    source,
                    error
                )   

    #step 14: Print the final execution summary.

    print("\n==============ORGANIZATION  SUMMARY=============")
    print(f"Target folder :{TARGET_FOLDER}")     
    print(f"Files moved   :{moved}")       
    print(f"Files skipped :{skipped}")
    print(f"Errors        :{errors}")
    print(f"Log files     :{LOG_FILE}")
    print("====================================================")


    logging.info("File organization completed.")
    logging.info("Files moved : %d", moved)
    logging.info("Files skipped : %d",skipped)
    logging.info("Errors : %d",errors)


#step 15: Run the program.

if __name__ == "__main__":
    organize_files()    