def latex_header():
    header = r"""
\documentclass{article}
\usepackage[margin=1in]{geometry}
\usepackage{tikz}
\begin{document}
"""
    return header

def latex_footer():
    footer = r"""
\end{document}
"""
    return footer

def latex_page_start():
    start_page = r"""
\newpage
\begin{center}
\begin{tikzpicture}
"""
    return start_page

def latex_cell(x, y, value, cellsize=3):
    xpos = (x - 1) * cellsize
    ypos = (5 - y) * cellsize  # assuming 5x5 grid, adjust if needed
    contents = rf"""  \draw[thick] ({xpos},{ypos}) rectangle ++({cellsize},{cellsize});
  \node at ({xpos + cellsize/2},{ypos + cellsize/2}) {{\footnotesize {value}}};
"""
    return contents

def latex_page_end():
    end_page = r"""\end{tikzpicture}
\end{center}

"""
    return end_page


if __name__ == "__main__":
    with open('output/bingo.tex', 'w') as f:
        f.write(latex_header())
        f.write(latex_page_start())
        for x in range(1, 6):
            for y in range(1, 6):
                f.write(latex_cell(x, y, f"Cell {x},{y}"))
        f.write(latex_page_end())
        f.write(latex_footer())
