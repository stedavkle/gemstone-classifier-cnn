#%%
from skimage import transform
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
from math import ceil

def load_image(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image

    
def transform_images(root_dir, goal):
    for root, dirs, files in os.walk(root_dir):
        flip = False
        size = len(files)
        num_to_edit = ceil((goal-size) / 3)
        if num_to_edit > size:
            flip = True
            num_to_edit = ceil((goal-size) / 7)
        print(root.split('\\')[-1], max(0, min(num_to_edit, size)))
        for file in np.random.choice(files, max(0, min(num_to_edit, size)), replace=False):
            try:
                image = load_image(root+'/'+file)
                if flip: plt.imsave(root+'/'+file[:-4]+'_flip'+file[-4:], np.fliplr(image))
                # apply different rotations
                for angle in rotations:
                    # save image
                    rot_img = transform.rotate(image, angle=angle)
                    plt.imsave(root+'/'+file[:-4]+'_rot'+str(angle)+file[-4:], rot_img)
                    if flip:
                        plt.imsave(root+'/'+file[:-4]+'_'+str(angle)+'_flip'+file[-4:], np.fliplr(rot_img))
            except:
                pass



root_dir = r'C:\Users\david\Documents\projects\gemstone-classifier-cnn\data\archive'
rotations = [90, 180, 270]
goal = 2000
transform_images(root_dir, goal)

#root_dir = r"C:/Users/david/Documents/projects/Gemstone_CNN/data/pictures2_crop_orig_aug"
#for root, dirs, files in os.walk(root_dir):
#    for file in files:
#        if 'flip' in file or 'rot' in file:
#            os.remove(root+'/'+file)
#            print(file)

#root_dir = r"C:/Users/david/Documents/projects/Gemstone_CNN/data/pictures2_crop_orig_aug"
#for root, dirs, files in os.walk(root_dir):
#    if len(files) > 0 and len(files < 500)
#        print(root)