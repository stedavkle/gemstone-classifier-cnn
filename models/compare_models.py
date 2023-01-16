#%%
#import seaborn
import matplotlib.pyplot as plt
#import pandas as pd
import pickle
import os


#%%
historys = {}

for root, dirs, files in os.walk(r"C:\Users\David Kleindiek\Documents\Projects\gemstone-classifier-cnn\models"):
    for file in files:
        if not file.endswith("history"):
            continue
        with open(os.path.join(root, file), "rb") as f:
            h = pickle.load(f)
            historys[root.split('\\')[-1] + '-' + file] = h

# %%
# plot model loss, 2k
labels = []
for h in historys:
    if not '2k' in h:
        continue
    print(h)
    print(historys[h]['val_accuracy'])
    #print(historys[h].keys())
    #plt.plot(historys[h]['top_3_acc'])
    labels.append(h.split('-')[0])
    plt.plot(historys[h]['loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.ylim(0, 2)
plt.xlim(0, 10)
plt.legend(labels, loc='upper right')
plt.show()
# %%
# plot model accuracy, 2k
labels = []
for h in historys:
    if not '2k' in h:
        continue
    print(h)
    #print(historys[h].keys())
    plt.plot(historys[h]['val_accuracy'])
    labels.append(h.split('-')[0])
    #plt.plot(historys[h]['loss'])
plt.title('model accuracy')
plt.ylabel('val_accuracy')
plt.xlabel('epoch')
plt.ylim(0, 1)
plt.xlim(0, 5)
plt.legend(labels, loc='lower right')
plt.show()
# %%
# mobilenet accuracys
labels = []
for h in historys:
    if not 'mobile' in h or '1k' in h:
        continue
    print(h)
    #print(historys[h].keys())
    plt.plot(historys[h]['val_accuracy'])
    plt.plot(historys[h]['val_top_3_acc'])
    plt.plot(historys[h]['val_top_5_acc'])
    labels.append(h.split('-')[0]+h.split('_')[3])
    #plt.plot(historys[h]['loss'])
plt.title('mobilenet accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.ylim(0.4, 1)
plt.xlim(0, 5)
plt.legend(['val_accuracy', 'val_top_3_acc', 'val_top_5_acc'], loc='lower right')
plt.show()

# %%
import pandas as pd

df = pd.DataFrame()
for h in historys:
    if not '2k' in h or not 'mobile' in h:
        continue
    print(h)
    accuracy = historys[h]['val_accuracy']
    top_3_acc = historys[h]['val_top_3_acc']
    top_5_acc = historys[h]['val_top_5_acc']
    loss = historys[h]['loss']


    # create dataframe and add val_accuracy as a row to the dataframe
    
    # add h as a column to the dataframe
    
    df['loss'] = loss
    df['accuracy'] = historys[h]['accuracy']
    df['val_accuracy'] = accuracy
    
    
    df.to_excel('mobilenet_2k_loss_acc.xlsx')
    


    
    #df = pd.DataFrame({'val_accuracy': accuracy, 'val_top_3_acc': top_3_acc, 'val_top_5_acc': top_5_acc})
print(df)
# %%
