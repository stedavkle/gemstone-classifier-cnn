# transfer train VGG16
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 
import tensorflow as tf
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras import layers, models
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras import optimizers
import pickle

def create_generator(data_path, batch_size, img_w, img_h):  
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
    return train_generator, valid_generator
def pp_generator(generator):
    for batch_x, batch_y in generator:
        yield preprocess_input(batch_x), batch_y
def create_model(CLASSES, img_w, img_h):
    ## Loading VGG16 model
    base_model = VGG16(weights="imagenet", include_top=False, input_shape=(img_w, img_h, 3))
    base_model.trainable = False ## Not trainable weights

    flatten_layer = layers.Flatten()
    dense_layer_1 = layers.Dense(256, activation='relu')
    prediction_layer = layers.Dense(CLASSES, activation='softmax')

    model = models.Sequential([
        base_model,
        flatten_layer,
        dense_layer_1,
        prediction_layer
    ])
    model.compile(
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy', tf.keras.metrics.TopKCategoricalAccuracy(k=3, name="top_3_acc", dtype=None), tf.keras.metrics.TopKCategoricalAccuracy(k=5, name="top_5_acc", dtype=None)],
    )
    return model


if __name__ == "__main__":
    print('MODEL: v66')
    print('---------------------')
    model_path = r"C:\Users\david\Documents\projects\gemstone-classifier-cnn\models\vgg16"
    
    data_paths = [r'\gempundit_nohands_crop_1k', r'\gempundit_nohands_crop_2k']
    
    img_w, img_h = 224, 224
    batch_size = 96                              # number of training samples using in each mini batch during GD (gradient descent) 

    filters = 32      # the dimensionality of the output space
    kernel_size = 3   # length of the 2D convolution window
    max_pool = 2      # size of the max pooling windows
    EPOCHS = 15                                  # while testing you can change it

    for path in data_paths:
        print("Loading data from: ", path)
        CLASSES = len(os.listdir(r"C:\Users\david\Documents\projects\gemstone-classifier-cnn\data" + path))


        print("Creating generators...")
        train_generator, valid_generator = create_generator(r'C:\Users\david\Documents\projects\gemstone-classifier-cnn\data'+path, batch_size, img_w, img_h)
        print("Creating model...", end=" ")   
        model = create_model(CLASSES, img_w, img_h)
        print("Done")
        STEP_SIZE_TRAIN = train_generator.n//train_generator.batch_size  # each sample will be passed [STEP_SIZE_TRAIN] times during training
        STEP_SIZE_VAL = valid_generator.n//valid_generator.batch_size     # each sample will be passed [STEP_SIZE_VAL] times during validation

        train_generator_pp = pp_generator(train_generator)
        valid_generator_pp = pp_generator(valid_generator)

        print("Training model...")
        m = model.fit(
            x=train_generator_pp,
            steps_per_epoch = STEP_SIZE_TRAIN,
            epochs=EPOCHS,
            validation_data = valid_generator_pp,
            validation_steps = STEP_SIZE_VAL,
            verbose=2, #callbacks=[TqdmCallback(verbose=2)]
            )
        model.save(model_path+path+'_e'+str(EPOCHS)+".h5")

        with open(model_path+path+'_e'+str(EPOCHS)+r'_history', 'wb') as file_pi:
            pickle.dump(m.history, file_pi)
        print("Saved model to disk")