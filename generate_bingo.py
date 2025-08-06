import random
import numpy as np

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
    ypos = (5 - y) * cellheight  # still assuming 5 rows
    contents = rf"""  \draw[thick] ({xpos},{ypos}) rectangle ++({cellwidth},{cellheight});
  \node at ({xpos + cellwidth/2},{ypos + cellheight/2}) {{{tex_size_modifier} {value}}};
"""
    return contents


def latex_page_end():
    end_page = r"""\end{tikzpicture}
This bingo card has been miticulously crafted by LLMs based on keywords from your recent publication titles.
\end{center}

"""
    return end_page


def generate_bingo(frequent_keywords: list):
    bingo_text = latex_page_start()
    for x in range(5):
        for y in range(5):
            bingo_text += latex_cell(x, y, f"{x},{y}: {permutation[x*bingo_size + y]}")
    bingo_text += latex_page_end()
    return bingo_text


if __name__ == "__main__":
    with open('output/tex/bingo.tex', 'w') as f:
        f.write(latex_header())
        f.write(generate_bingo([]))
        f.write(latex_footer())
