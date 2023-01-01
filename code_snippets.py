# %%
root_dir = r'C:\Users\david\Documents\projects\gemstone-classifier-cnn\data\gempundit_nohands_crop_2k'


# remove transformed images
import os
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if 'flip' in file or 'rot' in file:
            os.remove(os.path.join(root, file))
# %%
# remove folders with less than 0.75*goal amount of pictures
import os
goal_num = 2000
for root, dirs, files in os.walk(root_dir):
    if len(files) < 0.75*goal_num:
        print(root.split('\\')[-1])
        for file in files:
            os.remove(os.path.join(root, file))
        try:
            os.rmdir(root)
        except Exception as e:
            print(e)
# %%
## delete files wich are not an image
import os
import imghdr
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if not imghdr.what(root+"/"+file) == 'jpeg':
            os.remove(root+"/"+file)
            print(root+"/"+file)
# %%
# convert all webp to jpeg
import os
import imghdr
from PIL import Image
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if imghdr.what(root+"/"+file) == 'webp':
            im = Image.open(root+"/"+file).convert("RGB")
            im.save(root+"/"+file, "jpeg")
            print(root+"/"+file)
# list all files not an jpeg
import os
import imghdr
for root, dirs, files in os.walk(root_dir):
    for file in files:
        if not imghdr.what(root+"/"+file) == 'jpeg':
            print(root+"/"+file)
            print(imghdr.what(root+"/"+file))

# %%
# make sure in no folder are miore than 1000 images
import os
import numpy as np
goal_num = 2000
for root, dirs, files in os.walk(root_dir):
    if len(files) > goal_num:
        unnecerary_pictures = np.random.choice(files, len(files)-goal_num, replace=False)
        print(root.split('\\')[-1], len(unnecerary_pictures))
        for file in unnecerary_pictures:
            os.remove(root+"/"+file)
