# %%
# remove transformed images
import os
for root, dirs, files in os.walk('/home/david/projects/Gemstones-Convolutional-Neural-Network/1_Fetch_data/data/gempundit_nohands_crop_1k'):
    for file in files:
        if 'flip' in file or 'rot' in file:
            os.remove(os.path.join(root, file))
# %%
# remove folders with less than 0.75*goal amount of pictures
import os
goal_num = 2000
for root, dirs, files in os.walk('/home/david/projects/Gemstones-Convolutional-Neural-Network/1_Fetch_data/data/gempundit_nohands_crop_1k'):
    if len(files) < 0.75*goal_num:
        for file in files:
            os.remove(os.path.join(root, file))
        os.rmdir(root)
# %%
## delete files wich are not an image
import os
import imghdr
for root, dirs, files in os.walk("./"):
    for file in files:
        if not imghdr.what(root+"/"+file) == 'jpeg':
            os.remove(root+"/"+file)
            print(root+"/"+file)
# %%
# make sure in no folder are miore than 1000 images
import os
import numpy as np
goal_num = 2000
for root, dirs, files in os.walk("C:/Users/david/Documents/projects/Gemstone_CNN/data0/data/gempundit_nohands_crop_1k"):
    if len(files) > goal_num:
        unnecerary_pictures = np.random.choice(files, len(files)-goal_num, replace=False)
        print(len(unnecerary_pictures))
        for file in unnecerary_pictures:
            os.remove(root+"/"+file)
