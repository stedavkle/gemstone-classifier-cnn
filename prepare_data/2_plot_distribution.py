#%%
import os
import matplotlib.pyplot as plt
import seaborn as sn

import cv2
from random import randint

import numpy as np

root_path = r"C:\Users\david\Documents\projects\gemstone-classifier-cnn\data\archive"
#%%
number_of_pictures = {}
for root, dirs, files in os.walk(root_path):
    f = os.path.basename(root)    # get class name - Amethyst, Onyx, etc    
    
    if len(files) > 0:
        number_of_pictures[f] = len(files)
    
    # uncomment this block if you want a text output about each subfolder
    #count_dirs = 0
    #for f in dirs:           # count subfolders
        #count_dirs += 1
    #depth = root.split(os.sep)
    #print((len(depth) - 2) * '--'+'>', '{}:\t {} folders, {} imgs'.format(os.path.basename(root), count_dirs, gems[-1] if gems!=[] else 0)) 
number_of_pictures = dict(sorted(number_of_pictures.items(), key=lambda item: item[1]))
TOTAL_CLASSES = len(number_of_pictures.keys())
TOTAL_IMAGES = sum(number_of_pictures.values())
print('{} classes with {} images in total'.format(TOTAL_CLASSES, TOTAL_IMAGES))
#%%
f, ax = plt.subplots(figsize=(15,6))
# set y axis limit to 2000
ax.set_ylim(0, 400)
plt.bar(range(TOTAL_CLASSES), [int(x*0.8) for x in number_of_pictures.values()], label = 'Train data')
plt.bar(range(TOTAL_CLASSES), [int(x*0.2) for x in number_of_pictures.values()], label = 'Test data')
ax.grid()
ax.legend(fontsize = 12)
# %%
# get the 10 classes with the least images
least_images = {k: v for k, v in sorted(number_of_pictures.items(), key=lambda item: item[1])[:50]}
least_images
# %%
