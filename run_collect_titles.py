from tqdm import tqdm
import re
from get_cristin_titles import get_titles_2020_2025

if __name__ == "__main__":
    with open("input/names.txt",'r') as f:
        names = f.readlines()
        for name in tqdm(names):
            name = name.replace('\n', ' ').strip()
            titles = get_titles_2020_2025(name)
            with open(f"output/titles/{name}.txt", 'w') as out_f:
                for title in titles:
                    clean_title = re.sub(r'[\r\n]+', ' ', title)
                    out_f.write(clean_title+"\n")
