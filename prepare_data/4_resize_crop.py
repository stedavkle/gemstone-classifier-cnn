#%%
import numpy as np
import cv2
import os
import matplotlib.pyplot as plt

img_w, img_h = 224, 224
def edge_and_cut(img):
    try:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (2,2), 0)
        edges = cv2.Canny(img, img_w, img_h)            
        
        if(np.count_nonzero(edges)>edges.size/10000):
            pts = np.argwhere(edges>0)
            y1,x1 = pts.min(axis=0)
            y2,x2 = pts.max(axis=0)
            # crop the region but let it be a square
            if (y2-y1)>(x2-x1):
                x1 = x1-(y2-y1-x2+x1)//2
                x2 = x2+(y2-y1-x2+x1)//2
            else:
                y1 = y1-(x2-x1-y2+y1)//2
                y2 = y2+(x2-x1-y2+y1)//2

            new_img = img[y1:y2, x1:x2]  

            edge_size = 1 #replace it with bigger size for larger images            

            new_img = cv2.resize(new_img,(img_w, img_h))  # Convert to primary size  
            
        else:
            new_img = cv2.resize(img,(img_w, img_h))

    except Exception as e:
        print(e)
        new_img = cv2.resize(img,(img_w, img_h))
    
    return new_img
#%%
def read_imgs_lbls(_dir):
    Images, Labels = [], []
    for root, dirs, files in os.walk(_dir):
        f = os.path.basename(root)                             # get class name - Amethyst, Onyx, etc       
        for file in files:
            if not 'crop' in file:
                Labels.append(f)
                try:
                    image = cv2.imread(root+'/'+file)              # read the image (OpenCV)
                    # crop the image to a square
                    h, w, _ = image.shape
                    if h > w:
                        image = image[(h-w)//2:(h-w)//2+w, :, :]
                    else:
                        image = image[:, (w-h)//2:(w-h)//2+h, :]
                    image = cv2.resize(image,(int(img_w*1.5), int(img_h*1.5)))  # resize the image (images are different sizes)
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)              # converts an image from BGR color space to RGB
                    #image = edge_and_cut(image)
                    # save the image with 'crop' in the name
                    #cv2.imwrite(root+'/'+file[:-4]+'_crop'+file[-4:], image)
                    Images.append(image)
                except Exception as e:
                    print(e)
    Images = np.array(Images)
    return (Images, Labels)
#%%
def show_cropped(img):
    emb_img = img.copy()
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #blur = cv2.GaussianBlur(gray, (3,3), 0)

    edges = cv2.Canny(emb_img, img_w, img_h)
    
    if(np.count_nonzero(edges)>edges.size/10000):
        pts = np.argwhere(edges>0)
        y1,x1 = pts.min(axis=0)
        y2,x2 = pts.max(axis=0)
        # crop the region but let it be a square
        if (y2-y1)>(x2-x1):
            x1 = x1-(y2-y1-x2+x1)//2
            x2 = x2+(y2-y1-x2+x1)//2
        else:
            y1 = y1-(x2-x1-y2+y1)//2
            y2 = y2+(x2-x1-y2+y1)//2

        new_img = img[y1:y2, x1:x2]  

        edge_size = 1 #replace it with bigger size for larger images            

        emb_img[y1-edge_size:y1+edge_size, x1:x2] = [255, 0, 0]
        emb_img[y2-edge_size:y2+edge_size, x1:x2] = [255, 0, 0]
        emb_img[y1:y2, x1-edge_size:x1+edge_size] = [255, 0, 0]
        emb_img[y1:y2, x2-edge_size:x2+edge_size] = [255, 0, 0]

        new_img = cv2.resize(new_img,(img_w, img_h))  # Convert to primary size  
        return new_img
    else:
        new_img = cv2.resize(img,(img_w, img_h))
    
    fig, ax = plt.subplots(nrows=1, ncols=4, figsize=(10, 10))
    ax[0].imshow(img, cmap='gray')
    ax[0].set_title('Original Image', fontsize=14)
    ax[1].imshow(edges, cmap='gray')
    ax[1].set_title('Canny Edges', fontsize=14)
    ax[2].imshow(emb_img, cmap='gray')
    ax[2].set_title('Bounding Box', fontsize=14)       
    ax[3].imshow(new_img, cmap='gray')
    ax[3].set_title('Cropped', fontsize=14)
#%%
images, labels = read_imgs_lbls('../test')
# %%
for i in images:
    show_cropped(i)
# %%
# crop not inplace
for root, dirs, files in os.walk('/home/david/projects/Gemstones-Convolutional-Neural-Network/1_Fetch_data/pictures2'):
    f = os.path.basename(root)                             # get class name - Amethyst, Onyx, etc       
    for file in files:
        try:
            if os.path.exists(root.replace('pictures2', 'pictures2_crop_orig')+'/'+file):
                continue
            img = cv2.imread(root+'/'+file)

            crop = show_cropped(img)
            cv2.imwrite(root.replace('pictures2', 'pictures2_crop_orig')+'/'+file, crop)
            print('.', end=' ')
        except Exception as e:
            #print(e)
            pass
# %%
print('done')
# %%
# crop inplace
for root, dirs, files in os.walk('/home/david/projects/Gemstones-Convolutional-Neural-Network/1_Fetch_data/data/gempundit_nohands_crop_1k'):
    print(root.split('/')[-1])
    for file in files:
        if file.endswith('.jpg'):
            try:
                img = cv2.imread(root+'/'+file)
                crop = show_cropped(img)
                cv2.imwrite(root+'/'+file, crop)
            except Exception as e:
                print(e)

# %%
