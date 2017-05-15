import requests
from bs4 import BeautifulSoup
from util import download_page 

# Find div named info get detail and rating
def parse_page(html):
    soup = BeautifulSoup(html,'html.parser')
    if soup.find('title').getText() == '页面不存在':
        return dict()
    info_soup = soup.find_all('div', attrs = {'id':'info'})
    dictionary = get_info(info_soup)
    rating = soup.find('strong', property="v:average").getText()
    dictionary['评分'] = rating
    return dictionary

# Fetch detail
def get_info(info_soup):
    dictionary = dict()
    for sub_soup in info_soup:
        pl_list = sub_soup.find_all("span", class_="pl")
        for pl in pl_list:
            if pl.next_sibling != ": " and pl.next_sibling is not None:
                dictionary[pl.getText().replace(':','')] = pl.next_sibling
            else:
                dictionary[pl.getText()] = pl.next_sibling.next_sibling.getText()
        genre_list = sub_soup.find_all("span", property="v:genre")
        genre = genre_list[0].getText() + ''
        for x in range(1,len(genre_list)):
            genre = genre +'/' + genre_list[x].getText()
        dictionary['类型'] = genre
        if sub_soup.find('span', property="v:runtime") == None:
            dictionary['片长'] = ''
        else:
            dictionary['片长'] = sub_soup.find('span', property="v:runtime").getText()
        dictionary['上映日期'] = sub_soup.find('span', property="v:initialReleaseDate").getText()
    
    return dictionary        

# Return dictionary
def get_movie_info(url):
    html = download_page(url)
    dictionary = parse_page(html)
    return dictionary
    
    
    