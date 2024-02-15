import numpy as np
import PIL
from PIL import Image
import cv2
import random as rd
import math as m
from keras.models import Sequential as sq
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from keras import layers 
from keras import models
import os
#DISCLAIMER:For future me, Yo or anyone else who actually might be good at coding, I'm sorry.

#BEFORE: REPLACE AMOUNT OF IMAGES, DIR NAME AND MAKE ALL IMAGES .JPG FILES
train_dir = r"C:\Users\aokik\pyworks\allimages"
test_dir = r"C:\Users\aokik\pyworks\alltestimages"
#Ab hier habe ich wieder geschrieben 30.1.24 etwa 21:00-23:00)(Den GPT-Code habe ich ein wenig umgeschrieben und zu Übersichtszwecken als Funktion definiert.)
def normalize_images(train_dir):
    normalized_images = []
    naming_scheme= "{}{}"
    amount = 2500
    os.chdir(train_dir)
    for count, f in enumerate(os.listdir()):
        f_name, f_ext = os.path.splitext(f)
        for i in range(1):
            filename = os.path.join(train_dir, naming_scheme.format(f_name, f_ext))
        # Check if the file exists
            if not os.path.exists(filename):
                print(f"Error: File {filename} not found")
                continue

        image = cv2.imread(filename)

        # Convert the image to float32 to perform division
        image = cv2.convertScaleAbs(image, alpha=(1.0/255.0))



        # Append original and normalized images to the list
        normalized_images.append(normalized_images)

    # Convert the list to a NumPy array
    normalized_images = np.array(normalized_images)

    # Save NumPy arrays to files
    np.save('Normalized_Images.npy', normalized_images)

# Beispielaufruf mit einem Verzeichnis für Trainingsdaten
normalize_images(train_dir)

def normalize_test():
 normalized_test = []
 naming_scheme= "{}{}"
 amount=200
 os.chdir(test_dir)
 for count, f in enumerate(os.listdir()):
    f_name, f_ext = os.path.splitext(f)
    for i in range(1):
        filename = os.path.join(train_dir, naming_scheme.format(f_name, f_ext))
        if not os.path.exists(filename):
            print(f"Error: File {filename} not found")
            continue
    image = cv2.imread(filename)
    image = image.astype(np.float32)
    max_intensity = 255.0  # For 8-bit images
    normalized_test = image / max_intensity

    
  # Append original and normalized images to lists GPT
    normalized_test.append(normalized_test)

 # Convert lists to NumPy arrays
 normalized_test = np.array(normalized_test)

 # Save NumPy arrays to files GPT
 np.save('Testdaten.npy', normalized_test)
normalize_test()

#ERSCHAFFUNG DER LABEL
#ERSCHAFFUNG DER LABEL
def create_labels():
 labels=[]
 # Loop through the files in the directory GPT
 for filename in os.listdir(train_dir):
    if filename.endswith('.jpg'):
        # Extract class label from filename
        Wirbeltierklasse = filename.split('_')[0]  # Assumes the class label is the first part before the underscore
    labels.append(Wirbeltierklasse)
 np.array(labels)
 np.save('Labels.npy', labels)
create_labels()
def test_labels():
 test_labels=[]
 # Loop through the files in the directory GPT
 for filename in os.listdir(test_dir):
    if filename.endswith('.jpg'):
        # Extract class label from filename
        Wirbeltierklasse_test = filename.split('_')[0]  # Assumes the class label is the first part before the underscore
    test_labels.append(Wirbeltierklasse_test)
 np.array(test_labels)
 np.save('Test_Labels.npy', test_labels)
test_labels()

#Für Anwendung im Netzwerk muss die Datei wieder als numpy array geladen werden.
Normalisierte_Bilder= np.load('Normalized_Images.npy')
Labels= np.load('Labels.npy')
Testdaten=np.load('Testdaten.npy')
Test_Labels=np.load('Test_Labels.npy')

#CONSTRUCTING MODEL
def apply_Model():
 model = models.Sq([
    #layers.Flatten(input_shape=200, 200, 3),  
    layers.Ds(256, activation='relu'),     
    layers.Ds(256, activation='relu'),  
    layers.Ds(256, activation='relu'),     
    layers.Ds(128, activation='relu'),
    layers.Ds(64, activation='relu'),     
    layers.Ds(32, activation='relu'),
    layers.Ds(5, activation='softmax')  
])
 model.compile(optimizer='adam',
             loss='categorical_crossentropy',  
              metrics=['accuracy'])


#APPLYING NPY ARRAYS TO MODEL

 model.fit(Normalisierte_Bilder,Labels, epochs=10, validation_split=0.2,batch_size=250)
 model.evaluate(Testdaten, Test_Labels, batch_size=100)

 #NAMING AND SAVING THE NN
 filename_given = False
 path = os.getcwd()
 while filename_given == False:
    filename = input("Name der Datei:")
    if os.path.exists(path + "\{filename}.keras"):
        filename_given = True
    else: 
        print("Error, file already exists.")
 model.save(path + "\{filename}.keras")
apply_Model()