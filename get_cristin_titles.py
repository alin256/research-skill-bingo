from urllib.parse import urlencode
import requests
import json

baseurl = 'https://api.cristin.no/v2'

def get_entries(author, year):
    name_year_dict = {
        'contributor': author,
        'published_since': year,
        'published_before': year
    }
    url_part = urlencode(name_year_dict)
    responce = requests.get(f'{baseurl}/results?{url_part}')

    results_data = json.loads(responce.content)
    print(results_data)

    return results_data

def get_titles(entries):
    titles = [result['title'][result['original_language']] for result in entries]
    return titles


if __name__ == "__main__":
    results_data = get_entries('Sergey Alyaev', 2022)
    titles = get_titles(results_data)
    for i, title in enumerate(titles):
        print(f'{i+1}. {title}')

    # for result in results_data:
    #     print(result['title'][result['original_language']])


