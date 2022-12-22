#%%
from math import prod
from random import randint, random
import numpy as np
import pandas as pd
from time import sleep
from bs4 import BeautifulSoup as bs
import requests
import shutil
import os
import json
import concurrent.futures as cf


#%%
ALL_GEMS_URL = 'https://www.gempundit.com/gemstones'
# request the page with user agent to avoid 403 error
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


def download_images(data):
    print('.', end='')
    gem = data[0]
    link = data[1]
    print(gem, link)
    path = 'test/' + gem
    if not os.path.exists(path):
        os.mkdir(path)
    filename = link.split('/p')[-1].split('/')[1].split('?')[0]
    print(filename)
    if not os.path.exists(path + '/' + filename):
        img = requests.get(link, stream=True)
        if img.status_code == 200:    # OK
            with open(path+'/'+filename, 'wb') as f:
                img.raw.decode_content = True
                shutil.copyfileobj(img.raw, f)
                print('Image sucessfully Downloaded: ', filename)

def save_gem_page_links(gem_page_links):
    with open("gem_page_links.json", "w") as outfile:
        json.dump(gem_page_links, outfile)
def load_gem_page_links():
    with open("gem_page_links.json", "r") as outfile:
        gem_page_links = json.load(outfile)
    return gem_page_links

def get_all_gem_links_website(ALL_GEMS_URL):
    html = requests.get(ALL_GEMS_URL, headers=HEADERS).text
    soup = bs(html, 'html.parser')
    print('succesfully loaded page')
    gem_table = soup.find('div', {'class': 'container'})
    print('succesfully found gem table, now collecting links')
    gem_aClass = gem_table.find_all('a', {'data-category': 'gemstones'})
    gem_links = {}
    for gem in gem_aClass:
        link = gem.get('href')
        title = gem.get('title')
        print(title)
        # add the link to the dictionary
        gem_links[title] = link
    return gem_links
def get_all_gem_links_local_html():
    gem_links = {}
    with open('gemstones.html', 'r') as f:
        html = f.read()
    soup = bs(html, 'html.parser')
    for gem in soup.find_all('li'):
        gem_links[gem.find('img').get('alt')] = gem.find('a').get('href')
    return gem_links


def get_all_gem_pages(gem_links):    
    gem_page_links = {}
    for gem in gem_links:
        try:
            number_of_pages = int(bs(requests.get(gem_links[gem]+'/page/1000', headers=HEADERS).text, 'html.parser').find('li', {'class': 'current'}).text)
        except:
            number_of_pages = 1
        print('')
        print(gem, number_of_pages)
        gem_page_links[gem] = []
        for page_no in range(1, number_of_pages+1):
            gem_page_links[gem].append(gem_links[gem]+'/page/'+str(page_no))
            print(page_no, ', ', end='')
    print('-'*50)
    print('succesfully collected links')
    return gem_page_links
#%%
#for every gem page get the links to the individual gem pages
def get_gem_links(gem_page_links):
    for gem in gem_page_links:
        print(gem, len(gem_page_links[gem]))
        if os.path.exists('prod_links/' + gem + '.csv'):
            print('skip')
            continue
        get_individual_gem_links([gem, gem_page_links[gem]])
    print('-'*50)
    print('succesfully collected all product links')
def get_individual_gem_links(data):
    gem = data[0]
    links = data[1]

    gem_prod_links = []
    # check if csv file exists
    for page in links:
        print('.', end='')
        html = requests.get(page, headers=HEADERS).text
        soup = bs(html, 'html.parser')
        gem_product_pages = soup.find_all('a', {'class': 'product-image dataimage'})
        gem_prod_links.extend([page.get('href') for page in gem_product_pages])
        # sleep for a random time to avoid being blocked
        sleep(random()*2)
        if random() < 0.1:
            sleep(randint(1, 5))
    pd.DataFrame(gem_prod_links, columns=[gem]).to_csv('prod_links/' + gem + '.csv')
    sleep(10)
    return gem_prod_links
def get_all_gem_pages():
    print('loading gem links')
    gem_page_links = load_gem_page_links()
    print(len(gem_page_links))
    print('getting product links')
    futures = [executor.submit(get_individual_gem_links, [gem, gem_page_links[gem]]) for gem in gem_page_links]
    cf.wait(futures)
    print('succesfully collected all product links')
    return
#%%
def read_gem_prod_links():
    gem_prod_links = {}
    for file in os.listdir('prod_links'):
        data = pd.read_csv('prod_links/' + file, index_col=0)
        gem = data.columns[0]
        gem_prod_links[gem] = data[gem].tolist()
    return gem_prod_links
def get_all_gem_image_links():
    for file in os.listdir('prod_links'):
        data = pd.read_csv('prod_links/' + file, index_col=0)
        gem = data.columns[0]
        if not os.path.exists('image_links/' + gem + '.csv'):
            links = data[gem].tolist()
            futures = [executor.submit(get_img_links, link) for link in links]
            cf.wait(futures)
            results = []
            for future in futures:
                results.extend(future.result())
            pd.DataFrame(results, columns=[gem]).to_csv('img_links/' + gem + '.csv')
            print('succesfully collected all image links for ' + gem)
        else:
            print('skipping ' + gem)
    # for gem in gem_prod_links:
    #     get_img_links([gem, gem_prod_links[gem]])
    return
def get_img_links(data):
    gem = data[0]
    links = data[1]
    if not os.path.exists('img_links/' + gem + '.csv'):
        gem_img_links = []
        for link in links:
            # request the page with user agent to avoid 403 error
            gem_page_html = requests.get(link, headers=HEADERS).text
            gem_page_soup = bs(gem_page_html, 'html.parser')
            
            img_divs = gem_page_soup.find_all('div', {'class': 'item img_500'})
            
            gem_img_links.extend([x.find('img').get('src') for x in img_divs if not 'certi' in x.find('img').get('src')])
            sleep(random()*2)
            if random() < 0.1:
                sleep(randint(1, 5))
        pd.DataFrame(gem_img_links, columns=[gem]).to_csv('img_links/' + gem + '.csv')
        sleep(5)
    else:
        print('skip', gem)
    return
#%%
def download_all_pictures(gem_prod_links):
    for gem in gem_prod_links:
        links = gem_prod_links[gem]
        #print(gem, len(links))
        futures = [executor.submit(download_images, [gem, link]) for link in links]
        cf.wait(futures)

#%%
if __name__ == '__main__':
    executor = cf.ProcessPoolExecutor(64)
    #gem_links = get_all_gem_links_local_html()
    #%%
    #all_pages = get_all_gem_pages(gem_links)
    #%%
    #save_gem_page_links(all_pages)
    #%%
    #get_gem_links(all_pages)
    #%%
    get_all_gem_image_links()







    #         # download the images into the folder with the gem name
    #         for img_link in gem_img_links:
    #             download_images(gem, img_link)
    #         link_count += len(gem_img_links)
    #         # print name of gem and number of images
    # print('downloaded: ', link_count)

#%%
# RESET = '\033[0m'
# def get_color_escape(r, g, b, background=False):
#     return '\033[{};2;{};{};{}m'.format(48 if background else 38, r, g, b)
# print(get_color_escape(255, 128, 0) 
#       + get_color_escape(80, 30, 60, True)
#       + 'Fancy colors!' 
#       + RESET)
