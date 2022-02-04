import requests
import pandas as pd
from bs4 import BeautifulSoup as bs

def get_country_links():
    url = "https://evaw-global-database.unwomen.org/en/countries"
    response = requests.get(url)
    soup = bs(response.text, 'html.parser')
    res = {}
    for country in soup.find_all('ul', {'class':'list-unstyled categories'}):
        res[country.a.text] = country.a['href']
    return res

def get_country_data(country, country_link):
    look_for = ['Lifetime Physical and/or Sexual Intimate Partner Violence',
            'Physical and/or Sexual Intimate Partner Violence in the last 12 months',
            'Lifetime Non-Partner Sexual Violence',
            'Gender Gap Index Rank',
            'Child Marriage',
            'Gender Inequality Index Rank']
    
    soup = bs(requests.get(country_link).text, 'html.parser')
    data = soup.find_all('div', {'class':'col-md-8 clearfix'})[0]
    ret = {'country': country,
            'url': country_link}
    # I like looking at things.
    print(country)    
    for p in data.find_all('p'):
        for signal in look_for:
            if signal in p.text:
                text = p.text.replace(signal, '')
                num = "".join(filter(str.isdigit, text[:-7]))
                if num:
                    ret[signal] = int(num)
                else:
                    ret[signal] = None
    
    for signal in look_for:
        if signal not in ret.keys():
            ret[signal] = None

    return ret
if __name__ == '__main__':
    country_links = get_country_links()
    country_data = [get_country_data(k,v) for k,v in country_links.items()]
    df = pd.DataFrame(country_data)
    df.to_csv('women_rights_country_data.csv')
