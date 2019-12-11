import cv2
import numpy as np 
import copy
import argparse

parser = argparse.ArgumentParser(description='Kmeans Algorithm.')

parser.add_argument('--image', type=str,help='image path')
parser.add_argument('--k', type=int,default=10,help= 'Number of clusters')
parser.add_argument('--e', type=float,default=1.,help= 'Threshold')

args = parser.parse_args()

path = args.image
k = args.k
e = args.e

image = cv2.imread(path)
h,w,c = image.shape
X = image.reshape(-1,3)
means = np.random.randint(0,255,size=(k,c)) # sample random means
# colours = np.random.randint(0,255,size=(k,c)) 
prev_means = np.zeros(means.shape)
iteration=0
print('Printing Loss')
while np.linalg.norm(means-prev_means,axis=None) > e: # stopping criteria
	clusters =  [[] for _ in range(k)]
	indices =  [[] for _ in range(k)]
	for i in range(len(X)):
		distances = np.linalg.norm(X[i]-means,axis=1)
		cluster = np.argmin(distances) # assign xluster
		# print(cluster)
		clusters[cluster].append(X[i])
		indices[cluster].append(i)
	prev_means = copy.deepcopy(means)
	means = np.asarray([np.mean(clusters[i],axis=0) if len(clusters[i]) > 0 else prev_means[i] for i in range(k)]) # update means
	print('Iteration {}'.format(iteration),np.linalg.norm(means-prev_means,axis=None))
	iteration +=1

print('Centroids are :')
print(means.astype(int))
X_cluster = np.zeros(X.shape) # assign commmon colour
for i in range(k):
	for j in indices[i]:
		X_cluster[j] = means[i]

image_cluster =  X_cluster.reshape(h,w,c)
print('Image clustered with pixels saved as kmeans.jpg')
cv2.imwrite('./kmeans.jpg',image_cluster)