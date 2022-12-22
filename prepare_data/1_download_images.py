#%%
import concurrent.futures as cf
import os
from time import sleep, time
import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import os
import numpy as np
import shutil
#%%
def download_images(data):
    #print('.', end='')
    gem = data[0]
    link = data[1]
    #print(gem, link)
    path = img_path + gem
    if not os.path.exists(path):
        os.mkdir(path)
    filename = link.split('/p')[-1].split('/')[1].split('?')[0]
    if "hand" in filename:
        return
    if not filename.endswith('.jpg'):
        filename += '.jpg'
    #print(filename)
    if not os.path.exists(path + '/' + filename):
        img = requests.get(link, stream=True)
        if img.status_code == 200:    # OK
            with open(path+'/'+filename, 'wb') as f:
                img.raw.decode_content = True
                shutil.copyfileobj(img.raw, f)
                #print('Image sucessfully Downloaded: ', filename)
#%%
executor = cf.ThreadPoolExecutor(256)
#%%
link_path = "1_Fetch_data/links/gempundit_img_links/"
img_path = "1_Fetch_data/data/gempundit_nohands/"

for file in os.listdir(link_path):
    data = pd.read_csv(link_path+file, index_col=0)
    gem = file.split('.')[0]
    links = np.array(data.values).flatten()
    print(gem)
    futures = [executor.submit(download_images, (gem, link)) for link in links]
    cf.wait(futures)
    #print(gem)
    #print(len(links))
    #print(links[1]
# %%
