#%%
from skimage import transform
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import concurrent.futures as cf
from math import ceil

rotations = [90, 180, 270]
root_dir = r"/home/david/projects/Gemstones-Convolutional-Neural-Network/1_Fetch_data/data/gempundit_nohands_crop_1k"


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
        print(root.split('/')[-1], size, num_to_edit)
        #print('num_to_edit', num_to_edit)
        data = np.random.choice(files, min(max(num_to_edit,0), size), replace=False)
        futures = [executor.submit(performTransformation, img, root, flip) for img in data]
        cf.wait(futures)
        #for file in files:
        #    performTransformation(file, root, flip)

        #for file in np.random.choice(files, min(num_to_edit, size), replace=False):

def performTransformation(file, root, flip):
    #print('file', file)
    if file.endswith('.jpg'):
        image = load_image(root+'/'+file)
        if flip: plt.imsave(root+'/'+file[:-4]+'_flip'+file[-4:], np.fliplr(image))
        # apply different rotations
        for angle in rotations:
            # save image
            rot_img = transform.rotate(image, angle=angle)
            plt.imsave(root+'/'+file[:-4]+'_'+'rot_'+str(angle)+file[-4:], rot_img)
            if flip:
                plt.imsave(root+'/'+file[:-4]+'_'+str(angle)+'_flip'+file[-4:], np.fliplr(rot_img))


if __name__ == '__main__':
    executor = cf.ThreadPoolExecutor(max_workers=8)

    goal = int(input("Goal amount of pictures per class: "))
    transform_images(root_dir, goal)