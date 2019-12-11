import cv2
import numpy as np 
import copy
import argparse

parser = argparse.ArgumentParser(description='Kmeans Algorithm.')

parser.add_argument('--image', type=str,help='image path')

args = parser.parse_args()

path = args.image

image = cv2.imread(path)
h,w,c = image.shape
X = image.reshape(-1,3)/255.

mean_vector = np.mean(X,axis=0) # mean should be 0
X = X - mean_vector
X_t_X = np.matmul(X.transpose(),X)/len(X) # covariance matrix

w,v =  np.linalg.eig(X_t_X)

X_r = np.matmul(X,v)+ mean_vector # project on subspace
X_r = (X_r*255.).astype(int)
image_r =  X_r.reshape(image.shape)

cv2.imwrite('./pca.jpg',image_r)

