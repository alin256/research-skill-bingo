
baseurl = 'https://api.cristin.no/v2/'

def get_entries(url_part=''):
    results = requests.get(baseurl+'results'+'?'+url_part)
    results_data = json.loads(results.content)


find_name = {
    'contributor': 'Sergey Alyaev'
    # 'published_since': '2022'
    # 'published_before': '2021'
}

# find_project = {
#     'title': "distinguish"
# }

url_part = urlencode(find_name)

result = requests.get(baseurl + 'projects' + '?' + url_part)
