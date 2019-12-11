=======================================================
  Homework Assignment 1
  	-Puneet Mangla (CS17BTECH11029)
=======================================================

# Question 3 : Expectation Maximization
- Command line arguments :
	--k : Number of mixtures
	--d : Dimension of input
	--iterations : Number of iterations
	--points : number of points
	--input : Input file .npy required (n,d) shape. if not specified it will draw on its own

- Example : python gmm.py --k=3 --d=1 --points=1000 --iterations=100 
			python gmm.py --k=3 --d=1 --points=1000 --iterations=100 --input input.npy

- Output : gmm.jpg
- Shown examples : k=1, k=3, k=5, k=10
- Convergence issues : For large k, it becomes very difficult to converge . More datapoints are required to achieve reasonable convergence.
=======================================================

