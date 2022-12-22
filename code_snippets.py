# %%
# remove transformed images
import os
for root, dirs, files in os.walk('/home/david/projects/Gemstones-Convolutional-Neural-Network/1_Fetch_data/data/gempundit_nohands_crop_1k'):
    for file in files:
        if 'flip' in file or 'rot' in file:
            os.remove(os.path.join(root, file))
# %%
# remove images with less than 1000 pictures
import os
for root, dirs, files in os.walk('/home/david/projects/Gemstones-Convolutional-Neural-Network/1_Fetch_data/data/gempundit_nohands_crop_1k'):
    if len(files) < 600:
        for file in files:
            os.remove(os.path.join(root, file))
# %%
# remove empty folders
import os
for root, dirs, files in os.walk('/home/david/projects/Gemstones-Convolutional-Neural-Network/1_Fetch_data/data/gempundit_nohands_crop_1k'):
    if len(files) == 0:
        os.rmdir(root)
# %%
