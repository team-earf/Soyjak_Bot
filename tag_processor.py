<<<<<<< HEAD
=======
"""
Populates a directory that sorts all tags alphabetically as keys, and populates their lists of values with post ID's that are associated with them.
"""

>>>>>>> 0ed0aff507280978f99ff67615dab2d43edba72a
import os
import json
import logging
import re

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Makes list of all tag libraries, excluding any subdirectories and irrelevant files.
tag_directory = "soyjak_tags"
<<<<<<< HEAD
tag_libraries = [file for file in os.listdir(
    tag_directory) if file.startswith("tags")]
alphabetized_tag_libraries = os.listdir(
    os.path.join(tag_directory, "alphabetized"))
=======
tag_libraries = [file for file in os.listdir(tag_directory) if file.startswith("tags")]
alphabetized_tag_libraries = os.listdir(os.path.join(tag_directory, "alphabetized"))
>>>>>>> 0ed0aff507280978f99ff67615dab2d43edba72a

# Iterates through each tag library.
logging.info("Processing tag libraries...")
for file in tag_libraries:
    logging.info("Processing tag library: " + file)

    # Loads the tag library as "tags".
    file_path = os.path.join(tag_directory, file)
    with open(file_path, "r") as f:
        tags = json.load(f)

    # Iterates through each post in the tag library.
    for post_id, post_tags in tags.items():

        # Iterates through each tag in the post.
        for tag in post_tags:
            logging.info("Processing tag: " + tag)

            # Specifies the path to the alphabetical tag library.
            first_letter = tag[0].lower()
            # Checks if the first letter is a letter or number. If it isn't, it's set to "other".
            pattern = re.compile("[a-zA-Z0-9]")
            if not pattern.match(first_letter):
<<<<<<< HEAD
                logging.info(
                    f"Tag starts with non-alphanumeric character: {tag}\nSorting to 'other'.")
                first_letter = "other"

            alphabetical_tag_library_dir = os.path.join(
                tag_directory, "alphabetized")
            if not os.path.exists(alphabetical_tag_library_dir):
                os.makedirs(alphabetical_tag_library_dir)

            alphabetical_tag_library_filepath = os.path.join(
                alphabetical_tag_library_dir, first_letter + ".json")
=======
                logging.info(f"Tag starts with non-alphanumeric character: {tag}\nSorting to 'other'.")
                first_letter = "other"

            alphabetical_tag_library_dir = os.path.join(tag_directory, "alphabetized")
            if not os.path.exists(alphabetical_tag_library_dir):
                os.makedirs(alphabetical_tag_library_dir)

            alphabetical_tag_library_filepath = os.path.join(alphabetical_tag_library_dir, first_letter + ".json")
>>>>>>> 0ed0aff507280978f99ff67615dab2d43edba72a

            # Checks if the alphabetical tag library exists.
            if os.path.exists(alphabetical_tag_library_filepath):
                with open(alphabetical_tag_library_filepath, "r") as f:
                    alphabetical_tags = json.load(f)

                # Checks if the tag exists in the alphabetical tag library.
                if tag not in alphabetical_tags:
<<<<<<< HEAD
                    logging.info(
                        f"Adding new tag to alphabetical tag library: {tag}")
                    alphabetical_tags[tag] = [post_id]
                else:
                    logging.info(
                        f"Adding post to existing tag in alphabetical tag library: {tag}")
=======
                    logging.info(f"Adding new tag to alphabetical tag library: {tag}")
                    alphabetical_tags[tag] = [post_id]
                else:
                    logging.info(f"Adding post to existing tag in alphabetical tag library: {tag}")
>>>>>>> 0ed0aff507280978f99ff67615dab2d43edba72a
                    alphabetical_tags[tag].append(post_id)

                # Saves the alphabetical tag library.
                with open(alphabetical_tag_library_filepath, "w") as f:
                    json.dump(alphabetical_tags, f, indent=4)

            # If the alphabetical tag library doesn't exist, it's created.
            else:
<<<<<<< HEAD
                logging.info(
                    "Creating new alphabetical tag library: " + first_letter + ".json")
=======
                logging.info("Creating new alphabetical tag library: " + first_letter + ".json")
>>>>>>> 0ed0aff507280978f99ff67615dab2d43edba72a
                with open(alphabetical_tag_library_filepath, "w") as f:
                    alphabetical_tags = {tag: [post_id]}
                    # And saves the alphabetical tag library.
                    json.dump(alphabetical_tags, f, indent=4)
