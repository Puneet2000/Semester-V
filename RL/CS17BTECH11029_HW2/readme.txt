=======================================================
  Homework Assignment 2
  	-Puneet Mangla (CS17BTECH11029)
=======================================================

# Question 1 : Multi-Layer perceptron to learn XOR, AND, OR operations
- Command line arguments :
	--layers : Network layers eg: --layers 2 2 1
	--func : function to learn eg: xor, or, and
	--epochs : Number of iterations
	--batch_size : batch size to train on
	--threshold : threshold to assign label 1 
	--noise : to train on noisy samples

- Example : python q1.py --layers 2 2 1 --func or --epochs 100 --noise

Learning rate is 0.1 throughout training
- Observations :
	1. With increase in N functions like xor becomes harder to approximate due to increase in decision boundaries.
	2. Network length needs to be increased in order to train on large N.
	3. Observed almost same performance with training on noisy samples too.
=======================================================
Download mnist.hdf5 from here : http://data.pymvpa.org/datasets/mnist/

# Question 2 : Auto-Ecoder on MNIST
- Command line arguments :
	--layers : Network layers eg: --layers 784 512 784
	--epochs : Number of iterations
	--batch_size : batch size to train on

- Example : python q2.py --layers 784 512 256 128 256 512 784 --batch_size 256

- Specs :
	1. Network used : 784 512 256 128 256 512 784 
	2. Batch-size :  256
	3. Training epochs : 2000
	4. Learning rate is 0.01 : 0-499 epoch
						0.001 : 500-999 epoch
						0.0001 : 1000-2000 epoch

=======================================================

# Question 3 : Sparse-Auto-Ecoder on MNIST
- Command line arguments :
	--layers : Network layers eg: --layers 784 512 784
	--epochs : Number of iterations
	--batch_size : batch size to train on
	--sparsity : sparsity of bottle-neck layer

- Example : python q3.py --layers 784 512 256 128 256 512 784 --sparsity 0.1 --batch_size 256

- Specs :
	1. Network used : 784 512 256 128 256 512 784 
	2. Batch-size :  256
	3. Training epochs : 2000
	4. Sparsity : 0.1
	5. Learning rate is 0.01 : 0-499 epoch
						0.001 : 500-999 epoch
						0.0001 : 1000-2000 epoch
