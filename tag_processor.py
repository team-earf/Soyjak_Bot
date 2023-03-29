import os
import json

tag_library_directory = "soyjak_tags"

def relevant_post_finder(string):
    relevant_posts = []
    
    for tag_library in os.listdir(tag_library_directory):
        if tag_library.startswith("tags"):
            with open(os.path.join(tag_library_directory, tag_library), "r") as f:
                tag_library = json.load(f)
                for post_id, tag_list in tag_library.items():
                    if string in tag_list:
                        relevant_posts.append(post_id)

    for post in relevant_posts:
        print(f"https://booru.soy/post/view/{post}")

relevant_post_finder("autism")