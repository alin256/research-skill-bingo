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
    # print(results_data)

    return results_data


def get_titles(entries):
    titles = [result['title'][result['original_language']] for result in entries]
    return titles


def get_titles_2020_2025(name):
    results_data = []
    for year in range(2020,2025+1):
        results_data_for_year = get_entries(name, year)
        results_data += results_data_for_year
    titles = get_titles(results_data)
    return titles


if __name__ == "__main__":
    results_data = []
    for year in range(2020,2025+1):
        results_data_for_year = get_entries('Sergey Alyaev', year)
        results_data += results_data_for_year
    titles = get_titles(results_data)
    for i, title in enumerate(titles):
        print(f'{i+1}. {title}')

    # for result in results_data:
    #     print(result['title'][result['original_language']])


