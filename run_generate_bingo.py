import os
from tqdm import tqdm
import json
import numpy as np

from create_bingo_terms import extract_bingo_terms

bingo_size = 5
np.random.seed(0)
permutation = list(np.random.permutation(bingo_size**2 - bingo_size))
for i in range(bingo_size):
    j = (i + 3) % bingo_size
    index = i * bingo_size + j
    permutation.insert(index, -1)

def latex_header():
    header = r"""
\documentclass{article}
\renewcommand{\familydefault}{\sfdefault}
\usepackage[margin=1in, landscape]{geometry}
\usepackage{tikz}
\usepackage{pdflscape}
\begin{document}
"""
    return header

def latex_footer():
    footer = r"""
\end{document}
"""
    return footer

def latex_page_start(name="Sample Name"):
    start_page = r"""
\newpage
\begin{center}
\textbf{\Huge """ + name + r"""}\\
\vspace{0.5cm}
\begin{tikzpicture}
"""
    return start_page


def latex_cell(x, y, value, cellwidth=4.5, cellheight=2.75, tex_size_modifier=''):
    xpos = (x - 1) * cellwidth
    ypos = (5 - y) * cellheight
    contents = rf"""  \draw[thick] ({xpos},{ypos}) rectangle ++({cellwidth},{cellheight});
  \node[align=center, text width={cellwidth - 0.4}cm] at ({xpos + cellwidth/2},{ypos + cellheight/2}) {{{tex_size_modifier} {value}}};
"""
    return contents



def latex_page_end(additional_text=''):
    end_page = r"""\end{tikzpicture}
This bingo card has been meticulously crafted by LLMs based on keywords from your recent publication titles.

""" + additional_text + r"""
\end{center}

"""
    return end_page


def generate_bingo(frequent_keywords: list, name: str = "Sample Name", tex_size_modifier: str = ''):
    bingo_text = latex_page_start(name)
    for x in range(5):
        for y in range(5):
            index = permutation[x*bingo_size + y]
            if 0 <= index < len(frequent_keywords):
                bingo_text += latex_cell(x, y,
                    # f"{x},{y}: {permutation[x*bingo_size + y]} data assimilation and optimization",
                    value=f'{frequent_keywords[index]}',
                    tex_size_modifier=tex_size_modifier)
            else:
                bingo_text += latex_cell(x, y,
                    # f"{x},{y}: {permutation[x*bingo_size + y]} data assimilation and optimization",
                    value='',
                    tex_size_modifier=tex_size_modifier)
    additional_text = ''
    if len(frequent_keywords) > 20:
        additional_text = f'Suggestions: {", ".join(frequent_keywords[20:27])}'
    bingo_text += latex_page_end(additional_text=additional_text)
    return bingo_text


if __name__ == "__main__":
    folder_path = 'output/person_dicts'
    file_contents = []
    insufficient_terms_names = []
    with open('output/tex/bingo.tex', 'w') as f:
        f.write(latex_header())
        for filename in tqdm(os.listdir(folder_path)):
            full_path = os.path.join(folder_path, filename)
            if os.path.isfile(full_path) and filename.lower().endswith('.json'):
                name = os.path.splitext(filename)[0].replace('\n', ' ').strip()
                print(f'\nProcessing {name}\n')
                with open(full_path, 'r') as in_f:
                    keyword_dict = json.load(in_f)
                    terms = extract_bingo_terms(keyword_dict, top_n=27)
                    if len(terms) < 20:
                        insufficient_terms_names.append(name)
                    f.write(generate_bingo(terms, name=name, tex_size_modifier='\\large'))
        f.write(latex_footer())
    print(f'Insufficient terms for: {insufficient_terms_names}')
