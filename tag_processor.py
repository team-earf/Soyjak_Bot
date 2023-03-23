"""
This module makes a unique list of all tags in the database. 
Other functions are available after this, such as searching by tag and comparing post IDs.
"""

import os
import json
import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")


def create_unique_tag_list():
    # Directories
    tag_library_directory = "soyjak_tags"

    tag_libraries = [file for file in os.listdir(
        tag_library_directory) if file.endswith(".json")]

    unique_tag_list_filepath = os.path.join(
        tag_library_directory, "unique_tag_list.json")

    # Loading the unique_tag_list if it already exists; else, creating it
    if os.path.exists("unique_tag_list.json"):
        logging.info("Loading unique tag list from file.")
        with open(unique_tag_list_filepath, "r") as unique_tag_list_file:
            unique_tag_list = json.load(unique_tag_list_file)
    else:
        logging.info(
            "Creating unique tag list from all tag libraries."
        )
        unique_tag_list = []

    # Combing through each tag library
    for tag_library in tag_libraries:
        logging.info(f"Processing tag library: {tag_library}")

        tag_library_path = os.path.join(tag_library_directory, tag_library)
        with open(tag_library_path, "r") as tag_library_file:
            tag_library_data = json.load(tag_library_file)
            for post_id, post_tag_list in tag_library_data.items():
                for tag in post_tag_list:
                    if tag not in unique_tag_list:
                        unique_tag_list.append(tag)

    logging.info("Saving unique tag list to file.")

    # Alphabetizing unique tags
    unique_tag_list.sort()

    # Saving it to a file
    with open(unique_tag_list_filepath, "w") as unique_tag_list_file:
        json.dump(unique_tag_list, unique_tag_list_file, indent=4)

    return unique_tag_list


unique_tag_list = create_unique_tag_list()
