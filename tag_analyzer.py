"""
Creates a large matrix of tags and their co-occurrences.
"""

import os
import json
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


def get_tag_matrix():
    """
    Creates a large matrix of tags and their co-occurrences.
    """
    tag_directory = "soyjak_tags"
    max_tag_libraries = len(os.listdir(tag_directory)) - 1

    alphabetical_directory = f"{tag_directory}/alphabetical"

    unique_tags = []

    # Combs through each tag library.
    while max_tag_libraries >= 0:
        with open(f"{tag_directory}/tags{max_tag_libraries}.json", "r") as f:
            tags = json.load(f)

    for post_id, tag_list in tags.items():
        for tag in tag_list:

            # Take passing note of each unique tag.
            if tag not in unique_tags:
                unique_tags.append(tag)




print(get_tag_matrix())
