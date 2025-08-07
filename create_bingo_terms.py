import random

random.seed(0)

def extract_bingo_terms(keyword_dict, top_n = 20):
    frequent_terms = [keyword_item for keyword_item in keyword_dict.items() if keyword_item[1]["count"] > 1]
    one_off_terms = [keyword_item for keyword_item in keyword_dict.items() if keyword_item[1]["count"] == 1]

    sorted_terms = sorted(frequent_terms, key=lambda x: x[1]["count"], reverse=True)
    top_terms = sorted_terms[:top_n]

    print("Top terms")

    for i, term in enumerate(top_terms):
        print(f"{i+1}. {term[0]}: {term[1]['count']}")

    sampled_terms = random.sample(one_off_terms, min(top_n-len(top_terms), len(one_off_terms)))
    print("Sampled rare terms")

    for i, term in enumerate(sampled_terms):
        print(f"{i+len(top_terms)+1}. {term[0]}: {term[1]['count']}")

    result_terms = top_terms + sampled_terms
    terms_array = [term[0] for term in result_terms]
    print(terms_array)


if __name__ == "__main__":
    import json
    with open("output.json", "r") as f:
        data = json.load(f)
        extract_bingo_terms(data)
