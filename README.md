# Research-Skill-Bingo Card Generator

From the author of the Norwegian Research Poker


## Usage 

The bingo cards are generated for names in `input/names.txt` using the Norwegian [Cristin database of research results](https://www.cristin.no/) - ensure the names are searchable there. The cards are created as a single file `output/tex/bingo.tex`. 

*Bug: Currently, the placeholder folders are not generated automatically*

To generate the cards, run the following files in sequence.

1. `run_collect_titles.py` queries the database for recent research entries of researchers (currently years 2020 - 2025).
2. `run_extract_keywords.py` uses an LLM in Ollama to generate and aggregate technical terms based on the research-result titles.
3. `run_generate_bingo.py` uses the most popular terms to generate a bingo card with 20 fields filled out and 5 blank (by default). 
   
