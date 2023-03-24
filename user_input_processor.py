import os
import json

soyjak_tag_list = [file for file in os.listdir(
    "soyjak_tags/sorted_by_tags") if file.endswith(".json")]

print(soyjak_tag_list)