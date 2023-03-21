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
        self.page_url = f"http://booru.soy/post/view/{post_id}"
        self.page = requests.get(self.page_url)
        self.page_soup = BeautifulSoup(self.page.text, "html.parser")
        self.image_url = self.page_soup.find(
            "input", {"id": "text_image-src"}).get("value")
        self.file_ext = self.image_url.split(".")[-1]
        self.post_tags = self.page_soup.find(
            "span", {"class": "view"}).text.split(" ")  # splits string into list

    def download(self):
        """
        Downloads the image of the post to the 'soyjaks' folder.
        """
        logging.info(f"Trying #{self.post_id} at {self.page_url}")

        response = requests.get(self.image_url)

        soyjak_directory = "soyjaks"
        soyjak_filepath = os.path.join(
            soyjak_directory, f"Soyjak #{self.post_id}.{self.file_ext}")

        with open(soyjak_filepath, 'wb') as f:
            f.write(response.content)

    def save_tags(self):
        """
        Saves the tags of the post to a JSON file. If the file doesn't exist, it creates it, then saves it.
        Each post's tags are saved as a dictionary with the post ID as the key and the tags as the list of values.
        Saved in batches of 5,000.
        """

        tag_library_number = int(self.post_id / 5000)
        tag_directory = "soyjak_tags"
        tag_filepath = os.path.join(
            tag_directory, f"tags{tag_library_number}.json")

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

    logging.info("Checking the booru for latest post id...")

    catalog_page_url = "http://booru.soy/post/list"
    catalog_page = requests.get(catalog_page_url)
    catalog_page_soup = BeautifulSoup(catalog_page.text, "html.parser")
    catalog_image_list = catalog_page_soup.find(
        "div", {"class": "shm-image-list"})
    catalog_images = catalog_image_list.findChildren("a")

    latest_post_number = int(catalog_images[0]["data-post-id"])
    logging.info(f"Maximum amount of soyjaks: {latest_post_number:,d}")

    return latest_post_number


def number_to_start_off():
    """
    Looks at soyjaks that were already downloaded (if any) to determing where to start back on the booru.
    """
    logging.info("Checking for previously downloaded soyjaks...")

    downloaded_soyjaks = os.listdir("soyjaks")

    if not downloaded_soyjaks:
        logging.info("No soyjaks were previously downloaded!")
        soyjak_to_start_with = 1
        return soyjak_to_start_with
    else:
        logging.info(f"{len(downloaded_soyjaks):,d} already downloaded.")
        downloaded_soyjak_numbers = [
            int(file.split("#")[1].split(".")[0]) for file in downloaded_soyjaks]
        last_downloaded_soyjak_number = max(downloaded_soyjak_numbers)
        soyjak_to_start_with = last_downloaded_soyjak_number + 1

        logging.info(f"Starting with #{soyjak_to_start_with}")
        return soyjak_to_start_with


def scrape_post(post):
    try:
        booru_post = BooruPost(post)
        booru_post.download()
        logging.info(f"Download successful!")

        booru_post.save_tags()
        logging.info(f"Saved tags successfully!")
    except:
        logging.error(
            f"Something wrong with #{post}, skipping...")


def the_big_scrape():
    post_limit = get_latest_booru_post()
    current_post_id = number_to_start_off()

    while current_post_id <= post_limit:
        scrape_post(current_post_id)
        current_post_id += 1

    logging.info("You have all the soyjaks!")


def recheck_missing_soyjaks():
    """
    If you want to recheck all the missing soyjaks, this function will go through each downloaded soyjak and check if there are any gaps.
    """

    while True:
        recheck_input = input(
            "Would you like to recheck all missing soyjaks? (y/n): ").lower()
        if recheck_input == "y":
            logging.info("Rechecking all missing soyjaks...")

            # Gets numbers of all soyjaks that are downloaded in /soyjaks/
            soyjak_list = os.listdir("soyjaks")
            soyjak_list_numbers = [int(file.split("#")[1].split(".")[0])
                                   for file in soyjak_list]

            # Checks the gaps between each downloaded soyjak.
            for i in range(1, max(soyjak_list_numbers)):
                logging.info(f"Checking #{i}...")

                current_post = soyjak_list_numbers[i]
                next_post = soyjak_list_numbers[i + 1]
                post_gap = next_post - current_post
                logging.info(f"{post_gap} soyjaks missing.")

                if post_gap > 1:
                    posts_to_check = list(range(current_post + 1, next_post))
                    for post in posts_to_check:
                        scrape_post(post)

            logging.info("Recheck complete!")

        elif recheck_input == "n":
            logging.info("Exiting...")
            break

        else:
            logging.error("Invalid input!")


# Script starts here if traditionally ran.
if __name__ == "__main__":
    the_big_scrape()
    recheck_missing_soyjaks()
