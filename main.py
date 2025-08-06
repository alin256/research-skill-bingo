import requests
import csv

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.3:latest"

def make_determenistic_request(prompt):
    response = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "temperature": 0,
        "stream": False
    })

    if response.status_code == 200:
        result = response.json()
        return result["response"]
    else:
        raise RuntimeError(f"Ollama error: {response.status_code} {response.text}")


def extract_keywords(title):
    prompt = f"""Extract 3–5 key technical self-explanatory terms or phrases from the following publication title:
"{title}"

Return only a comma-separated list of the keywords in lower case, no explanation."""

    result = make_determenistic_request(prompt)

    return [kw.strip() for kw in result.split(",")]


def check_self_explanatory(term):
    prompt = f"""Is "{term}" a clear application or methodological area for a computational researcher. 
    
    Answer without explanation: Yes / No"""

    answer = make_determenistic_request(prompt)

    print(f"Result for term {term}: {answer}")

    if answer[0:3] == "Yes":
        prompt = prompt + "\nAnswer: " + answer + "\nPrompt: How do you understand this area - concise definition?"
        answer = make_determenistic_request(prompt)
        print(answer)
        return True
    elif answer[0:2] == "No":
        prompt = prompt + "\nAnswer: " + answer + "\nPrompt: Why?"
        answer = make_determenistic_request(prompt)
        print(answer)
        return False
    else:
        raise RuntimeError(f"Ollama gives incorrect response: {answer}")


def classify_match_level(phrase1, phrase2):
    prompt = f"""You are an expert in technical concept classification. Classify the semantic relationship between the following two keyword phrases.

Only group concepts if they are used interchangeably or very tightly linked in technical literature. Do not group general terms like "porous media" with specific methods unless they are almost always discussed together in the same technical scope.

Phrase 1: "{phrase1}"
Phrase 2: "{phrase2}"

Choose one of the following levels:

1. Exact match — The phrases are identical or refer to exactly the same technical concept.
2. Synonyms or strong paraphrases — The phrases mean the same thing and can be used interchangeably in technical writing.
3. Tight generalization or specialization — One is a general or specific case of the other, and they are usually discussed together. This only applies if one term *directly defines or contains* the other.
4. Weak or distant generalization — One phrase is broader than the other but not in a tightly linked way. They may appear in the same field, but do not imply each other.
5. No match — The phrases describe different technical concepts, even if used in the same research area. Do not group phrases just because they may be used in the same application domain.


Answer with just the number (1–5)."""

    response = make_determenistic_request(prompt).strip()
    if response[0] in "12345":
        return int(response[0])
    else:
        raise ValueError(f"Unexpected model response: {response}")


def broader_concept(phrase1, phrase2):
    prompt = f"""Which of the phrases is the broader concept

    Phrase 1: "{phrase1}"
    Phrase 2: "{phrase2}"

    Return the phrase with no punctuation numbers or other details"""
    response = make_determenistic_request(prompt).strip().lower()
    if response == phrase1.lower():
        return phrase1
    elif response == phrase2.lower():
        return phrase2
    else:
        raise ValueError(f"Expected: '{phrase1}' or '{phrase2}'. Got: '{response}'")

def same_concept(phrase1, phrase2):
    level = classify_match_level(phrase1, phrase2)

    if level in (1, 2):
        return True, level  # collapse
    elif level in (3, 4, 5):
        return False, level # keep both
    else:
        raise ValueError(f"Unexpected match level: {level}")



# Example usage
titles = ["A decision support system for multi-target geosteering",
          "Modeling extra-deep electromagnetic logs using a deep neural network",
          "An ensemble-based framework for proactive geosteering"]

titles = []
with open("citations.csv", newline='', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        title = row.get("Title")
        if title:
            titles.append(title)

all_keywords_count = {}
for i, title in enumerate(titles):
    print(f"{i}. {title}")
    keywords = extract_keywords(title)

    for new_keyword in keywords:
        matched = False
        for old_keyword in all_keywords_count:
            same_concept_result = same_concept(new_keyword, old_keyword)
            if same_concept_result[0]:
                all_keywords_count[old_keyword] += 1
                print(f"{old_keyword}: {all_keywords_count[old_keyword]}")
                matched = True
                break
            elif same_concept_result[1] == 3:
                cur_count = all_keywords_count[old_keyword]
                del all_keywords_count[old_keyword]
                broader_keyword = broader_concept(new_keyword, old_keyword)
                all_keywords_count[broader_keyword] = cur_count + 1
                print(f"Found broader '{broader_keyword}' that summarizes narrower '{old_keyword}', '{new_keyword}'")
                print(f"{broader_keyword}: {all_keywords_count[broader_keyword]}")
                break
        if not matched:
            all_keywords_count[new_keyword] = 1
            print(f"{new_keyword}: {all_keywords_count[new_keyword]}")


print(all_keywords_count)
