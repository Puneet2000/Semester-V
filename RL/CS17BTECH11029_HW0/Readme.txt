=======================================================
  Homework Assignment 0
  	-Puneet Mangla (CS17BTECH11029)
=======================================================

# Question 1 : K-means clustering
- Command line arguments :
	--image : Specify image path
	--k : Specify number of clusters, default=10
	--e : Threshold, default=1

- Example : python kmeans.py --image dogs.jpg --k 10 --e 1.0
- Output : kmeans.jpg, segmented image
- Shown examples : dogs.jpg, vegetables.jpg
=======================================================

# Question 2 : PCA
- Command line arguments :
	--image : Specify image path

- Example : python pca.py --image dogs.jpg
- Output : pca.jpg, decorrelated-image
- Shown examples : dogs.jpg, vegetables.jpg
- Where PCA fails : When data is uncorrelated. Eg: fail.jpg is drawn from spherical gaussian and its PCA gives same output (pca_fail.jpg).
========================================================

# Question 3 : MLE
- Command line arguments :
	--dist : Specify distribution
	--points : number of points to sample, default=20000

- Example : python mle.py --dist binomial
- Output : Plot for actual and estimated distribution
- Shown examples : poisson, binomial, exponential, gaussian, laplacian
========================================================

