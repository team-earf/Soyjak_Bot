"""
This module makes a unique list of all tags in the database. 
Other functions are available after this, such as searching by tag and comparing post IDs.
"""

import os
import json
import logging
import re

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s")

# global filepaths
tag_library_directory = "soyjak_tags"

tag_libraries = [file for file in os.listdir(
    tag_library_directory) if file.endswith(".json")]

unique_tag_list_file = os.path.join(
    tag_library_directory, "unique_tag_list.json")

sorted_tags_directory = os.path.join(tag_library_directory, "sorted_by_tags")


def create_unique_tag_list():
    logging.info(
        "Creating unique tag list from all tag libraries."
    )

    # Making the unique tag list
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
    with open(unique_tag_list_file, "w") as unique_tag_list_file:
        json.dump(unique_tag_list, unique_tag_list_file, indent=4)

    return unique_tag_list


if os.path.exists(unique_tag_list_file):
    with open(unique_tag_list_file, "r") as unique_tag_list_file:
        unique_tag_list = json.load(unique_tag_list_file)
else:
    unique_tag_list = create_unique_tag_list()


# getting every relevant post ID for a tag
def sort_all_tags():
    logging.info('sorting all tags')

    # for tag in unique_tag_list:
    for tag in unique_tag_list:
        logging.info(f"sorting {tag}")
        tag = re.sub(r'[^a-zA-Z0-9]+', ' ', tag)
        
        if tag == '':
            tag = 'other'
        
        related_post_ids = []

        for library in tag_libraries:
            if library != "unique_tag_list.json":

                with open(os.path.join(tag_library_directory, library), 'r') as f:
                    tag_library_data = json.load(f)

                for post_id, post_tag_list in tag_library_data.items():
                    if tag in post_tag_list:
                        print(f"{tag} is in {post_id}")

                        related_post_ids.append(post_id)

        # sorting the list of post IDs
        related_post_ids.sort()
        
        # saving the list of post IDs to a file
        if not os.path.exists(sorted_tags_directory):
            os.makedirs(sorted_tags_directory)
        
        with open(os.path.join(sorted_tags_directory, f"{tag}.json"), 'w') as f:
            json.dump(related_post_ids, f, indent=4)
        
        logging.info(f"saved {tag} to file")


sort_all_tags()
