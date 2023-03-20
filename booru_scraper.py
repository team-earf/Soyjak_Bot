"""
This module scrapes every available soyjak file from 'booru.soy'. It saves the files to '/soyjaks/' and
the posts' tags to '/soyjak_tags/'.
"""

import requests
import logging
from bs4 import BeautifulSoup
import os
import json

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')


class BooruPost:
    """
    Everything you'd need for a single post.
    """

    def __init__(self, post_id):
        self.post_id = post_id
        self.page_url = "http://booru.soy/post/view/" + str(post_id)
        self.page = requests.get(self.page_url)
        self.page_soup = BeautifulSoup(self.page.text, "html.parser")
        self.image_url = self.page_soup.find("input", {"id": "text_image-src"}).get("value")
        self.file_ext = self.image_url.split(".")[-1]
        self.post_tags = self.page_soup.find("span", {"class": "view"}).text.split(" ")  # splits string into list

    def download(self):
        """
        Downloads the image of the post to the 'soyjaks' folder.
        """
        logging.info(f"Trying #{self.post_id} at {self.page_url}")

        response = requests.get(self.image_url)

        with open(f'soyjaks/Soyjak #{self.post_id}.{self.file_ext}', 'wb') as f:
            f.write(response.content)

    def save_tags(self):
        """
        Saves the tags of the post to a JSON file. If the file doesn't exist, it creates it, then saves it.
        Each post's tags are saved as a dictionary with the post ID as the key and the tags as the list of values.
        Saved in batches of 5,000.
        """

        tag_library_number = int(self.post_id / 5000)
        tag_filepath = f"soyjak_tags/tags{tag_library_number}.json"

        if not os.path.exists(tag_filepath):
            tags = {f"{self.post_id}": self.post_tags}

            with open(tag_filepath, 'w') as f:
                json.dump(tags, f, indent=4)

        else:
            with open(tag_filepath, 'r') as f:
                tags = json.load(f)

            tags[f"{self.post_id}"] = self.post_tags

            with open(tag_filepath, 'w') as f:
                json.dump(tags, f, indent=4)


def get_latest_booru_post():
    """
    Returns the highest post number from booru. soy by finding the latest file uploaded to the catalog.
    :return: int
    """

    catalog_page_url = "http://booru.soy/post/list"
    catalog_page = requests.get(catalog_page_url)
    catalog_page_soup = BeautifulSoup(catalog_page.text, "html.parser")
    catalog_image_list = catalog_page_soup.find("div", {"class": "shm-image-list"})
    catalog_images = catalog_image_list.findChildren("a")
    latest_post_number = int(catalog_images[0]["data-post-id"])

    logging.info(f"Maximum amount of soyjaks: {latest_post_number:,d}")

    return latest_post_number


def number_to_start_off():
    """
    Looks at soyjaks that were already downloaded (if any) to determing where to start back on the booru.
    :return: int
    """
    downloaded_soyjaks = os.listdir("soyjaks")

    if not downloaded_soyjaks:
        logging.info("No soyjaks were previously downloaded!")
        soyjak_to_start_with = 1
        return soyjak_to_start_with
    else:
        logging.info(f"{len(downloaded_soyjaks):,d} already downloaded.")
        downloaded_soyjak_numbers = [int(file.split("#")[1].split(".")[0]) for file in downloaded_soyjaks]
        last_downloaded_soyjak_number = max(downloaded_soyjak_numbers)
        soyjak_to_start_with = last_downloaded_soyjak_number + 1

        soyjaks_unavailable = soyjak_to_start_with - last_downloaded_soyjak_number
        logging.info(f"Due to various circumstances, {soyjaks_unavailable} are missing.")
        logging.info("This is either due to local or Booru deletion.")

        logging.info(f"Starting with #{soyjak_to_start_with}")
        return soyjak_to_start_with


def recheck_bad_soyjaks():
    pass


# Script starts here if traditionally ran.
if __name__ == "__main__":
    post_limit = get_latest_booru_post()
    current_post_id = number_to_start_off()

    while current_post_id <= post_limit:
        try:
            BooruPost(current_post_id).download()
            logging.info(f"Download successful!")

            BooruPost(current_post_id).save_tags()
            logging.info(f"Saved tags successfully!")

        except:
            logging.error(f"Something wrong with #{current_post_id}, skipping...")

        current_post_id += 1
