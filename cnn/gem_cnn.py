# requires tensorflow<2.11
# pillow, scipy, cv2, numpy
import os
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, AveragePooling2D
from tensorflow.keras.layers import Activation, Dropout, Flatten, Dense
from tensorflow.keras import optimizers
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tqdm.keras import TqdmCallback

data_path = r"C:/Users/david/Documents/projects/Gemstone_CNN/data0/data/gempundit_nohands_crop_1k"
model_path = r"C:/Users/david/Documents/projects/Gemstone_CNN/models/gempundit_nohands_crop_1k_5ep01"

img_w, img_h = 224, 224
batch_size = 96                              # number of training samples using in each mini batch during GD (gradient descent) 


image_generator = ImageDataGenerator(validation_split=0.2)             # this is the augmentation configuration used for training
#        rotation_range=25,
#        zoom_range=0.1,
#        width_shift_range=0.1,
#        height_shift_range=0.1,
#        shear_range=0.2,
#        horizontal_flip=True
#        )

train_generator = image_generator.flow_from_directory(
    directory=data_path,
    target_size=(img_w, img_h),
    color_mode="rgb",
    batch_size=batch_size,
    class_mode="categorical",
    shuffle=True,
    seed=42,
    subset="training"
)
valid_generator = image_generator.flow_from_directory(
    directory=data_path,
    target_size=(img_w, img_h),
    color_mode="rgb",
    batch_size=batch_size,
    class_mode="categorical",
    shuffle=True,
    seed=42,
    subset="validation"
)


CLASSES = len(os.listdir(data_path))
filters = 32      # the dimensionality of the output space
kernel_size = 3   # length of the 2D convolution window
max_pool = 2      # size of the max pooling windows
EPOCHS = 5                                  # while testing you can change it
STEP_SIZE_TRAIN = train_generator.n//train_generator.batch_size  # each sample will be passed [STEP_SIZE_TRAIN] times during training
STEP_SIZE_VAL = valid_generator.n//valid_generator.batch_size     # each sample will be passed [STEP_SIZE_VAL] times during validation

model = Sequential()
# first layer
model.add(Conv2D(32, (kernel_size, kernel_size), activation='relu', padding='same', input_shape=(img_w, img_h, 3))) # 32
model.add(MaxPooling2D((max_pool, max_pool))) #reduce the spatial size of incoming features
# second layer
model.add(Conv2D(64, (kernel_size, kernel_size), activation='relu', padding='same')) # 64
model.add(MaxPooling2D((max_pool, max_pool))) 
# third layer
model.add(Conv2D(128, (kernel_size, kernel_size), activation='relu', padding='same')) # 128
model.add(MaxPooling2D((max_pool, max_pool))) 
# fourth layer
model.add(Conv2D(128, (kernel_size, kernel_size), activation='relu', padding='same')) # 128
model.add(AveragePooling2D(pool_size= (2, 2), strides= (2, 2))) 
# fifth layer
model.add(Conv2D(128, (kernel_size, kernel_size), activation='relu', padding='same')) # 128
model.add(MaxPooling2D((max_pool, max_pool))) 
model.add(Flatten())
model.add(Dense(512, activation='relu'))                                             # 512
model.add(Dropout(0.5))
model.add(Dense(CLASSES, activation='softmax'))
#model.summary()
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy'])


m2 = model.fit(
      x=train_generator,
      steps_per_epoch = STEP_SIZE_TRAIN,
      epochs=EPOCHS,
      validation_data = valid_generator,
      validation_steps = STEP_SIZE_VAL,
      verbose=1, #callbacks=[TqdmCallback(verbose=2)],
      use_multiprocessing = False,  
      workers = 4)

# m = model.fit_generator(
#       generator=train_generator,
#       steps_per_epoch = STEP_SIZE_TRAIN,
#       epochs=EPOCHS, 
#       validation_data = valid_generator,
#       validation_steps = STEP_SIZE_VAL,
#       verbose = 1, # Verbosity mode. 0 = silent, 1 = progress bar, 2 = one line per epoch.
#       use_multiprocessing = True,  
#       workers = 8)

model.save(model_path)
print(m.history)
