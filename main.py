import requests
from bs4 import BeautifulSoup
from pageParse import *
from util import download_page


DOWNLOAD_URL = 'http://movie.douban.com/top250'

def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    movie_list_soup = soup.find('ol',attrs={'class':'grid_view'})
    movie_list = []
    
    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div',attrs={'class':'hd'})
        movie_url = detail.find('a', href=True)
        info_dictionary = get_movie_info(movie_url['href'])
        movie_name = detail.find('span', attrs={'class':'title'}).getText()
        movie_list.append((movie_name,info_dictionary))
    
    next_page = soup.find('span', attrs={'class':'next'}).find('a')
    if next_page:
        return movie_list, DOWNLOAD_URL+next_page['href']
    return movie_list,None

def main():
    url = DOWNLOAD_URL
    
    file = open("movies.txt", 'w',encoding = 'utf-8');
    file.write('');
    file.close();
    
    while url:
        html = download_page(url)
        movies, url = parse_html(html)
        file = open('movies.txt', 'a', encoding = 'utf8')
        for movie in movies:   
            file.write(movie[0] + '\n')
            for key in movie[1]:
                file.write(key +': ' + movie[1].get(key) + '\n')
            file.write('------------------separate line----------------------\n')
        file.close()
            
    
if __name__ == '__main__':
    main()
