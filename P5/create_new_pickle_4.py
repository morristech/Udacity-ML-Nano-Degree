# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 10:48:44 2016

@author: s6324900
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:35:26 2016

@author: priyankadwivedi
"""
from six.moves import cPickle as pickle
import glob
from scipy import ndimage
import numpy as np
import os

image_size = 56
pixel_depth = 255
image_files = 25000
dataset = np.ndarray(shape= (image_files, image_size, image_size), dtype= np.float32)
target = np.ndarray(shape= (image_files), dtype= np.int_)
num_images = 0
for filename in glob.glob("/Users/priyankadwivedi/Documents/Kaggle/CatvsDogs/train/*.small"):                         
  
  if num_images%5000 == 0: print(num_images)
  try:
      #image_data = (ndimage.imread(filename, flatten = True).astype(float)) 
      image_data = (ndimage.imread(filename, flatten = True).astype(float))
      if image_data.shape != (image_size, image_size):
        raise Exception('Unexpected image shape: %s' % str(image_data.shape))
      dataset[num_images, :, :] = image_data
      name = os.path.basename(filename)
      if name.split(".")[0] == "dog":
          target[num_images] = 1
      else:
          target[num_images] = 0
      num_images = num_images + 1
  except IOError as e:
      print('Could not read:', filename, ':', e, '- it\'s ok, skipping.')


#Randomize dataset and target
def randomize(dataset, labels):
  permutation = np.random.permutation(labels.shape[0])
  shuffled_dataset = dataset[permutation,:,:]
  shuffled_labels = labels[permutation]
  return shuffled_dataset, shuffled_labels
all_dataset, all_labels = randomize(dataset, target)

# split the full dataset of 25k images into train - 20k images and test - 5k images 
from sklearn import cross_validation 
X_train, X_valid, y_train, y_valid = cross_validation.train_test_split(
all_dataset, all_labels, test_size=0.2, random_state=207)

print("train dataset", X_train.shape, y_train.shape)
print("Validation dataset", X_valid.shape, y_valid.shape)

#Split training again into test dataset
from sklearn import cross_validation 
X_valid, X_test, y_valid, y_test = cross_validation.train_test_split(
X_valid, y_valid, test_size=0.2, random_state=387)

print("valid dataset", X_valid.shape, y_valid.shape)
print("test dataset", X_test.shape, y_test.shape)


# Pickle again
os.chdir(r"/Users/priyankadwivedi/Desktop/tensor/P5/param_op")
pickle_file = 'catdog59.pickle'

try:
  f = open(pickle_file, 'wb')
  save = {
    'X_valid': X_valid,
    'y_valid': y_valid,
    'X_test': X_test,
    'y_test': y_test,
    'X_train': X_train,
    'y_train': y_train,
    }
  pickle.dump(save, f, pickle.HIGHEST_PROTOCOL)
  f.close()
except Exception as e:
  print('Unable to save data to', pickle_file, ':', e)
  raise

    
    