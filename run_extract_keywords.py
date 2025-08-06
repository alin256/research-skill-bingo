import os
import json
from tqdm import tqdm

from extract_keywords import generate_keyword_dict

folder_path = 'output/titles'
file_contents = []

for filename in tqdm(os.listdir(folder_path)):
    full_path = os.path.join(folder_path, filename)
    if os.path.isfile(full_path) and filename.lower().endswith('.txt'):
        name = os.path.splitext(filename)[0].replace('\n', ' ').strip()

        output_path = f"output/person_dicts/{name}.json"
        if os.path.exists(output_path):
            print(f"\nSkipping {name}")
            continue

        print(f"\nProcessing {name}")

        with open(full_path, 'r', encoding='utf-8') as f:
            # get the lines
            lines = f.read().splitlines()
            # process the titles to keywords
            keywords_dict = generate_keyword_dict(lines, name=name)

            with open(output_path, "w") as out_f:
                json.dump(keywords_dict, out_f)


