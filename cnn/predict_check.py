# predict and check
import numpy as np
import cv2
test_num = 2
test_imgs = {}
for root, dirs, files in os.walk(data_path):
    if len(files) > test_num:
        imgs = []
        for img in np.random.choice(files, test_num, replace=False):
            path = root+'/'+img
            #print(path.replace('\\','/'))
            imgs.append(np.expand_dims(cv2.imread(path.replace('\\','/')), axis=0))
        test_imgs[root.split('\\')[-1]] = imgs

result = {}
for c in test_imgs:
    result[c] = []
    for img in test_imgs[c]:
        prediction = model.predict(img)
        top_2 = [(inv_indices[i], prediction[0][i]) for i in sorted(range(len(prediction[0])), key=lambda i: prediction[0][i])[-2:]]
        result[c].append(top_2)

true = 0
false = 0
for gem in result.keys():
    for pred in result[gem]:
        if pred[-1][0] == gem:
            true += 1
        else:
            false += 1


image = np.expand_dims(cv2.resize(cv2.imread(r"C:\Users\david\Downloads\smaragd.jpg"), (224,224)), 0)
prediction = model.predict(image)
[(inv_indices[i], prediction[0][i]) for i in sorted(range(len(prediction[0])), key=lambda i: prediction[0][i])[-5:]]