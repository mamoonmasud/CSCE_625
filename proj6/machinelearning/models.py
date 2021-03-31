import nn

class PerceptronModel(object):
    def __init__(self, dimensions):
        """
        Initialize a new Perceptron instance.

        A perceptron classifies data points as either belonging to a particular
        class (+1) or not (-1). `dimensions` is the dimensionality of the data.
        For example, dimensions=2 would mean that the perceptron must classify
        2D points.
        """
        self.w = nn.Parameter(1, dimensions)

    def get_weights(self):
        """
        Return a Parameter instance with the current weights of the perceptron.
        """
        return self.w

    def run(self, x):
        """
        Calculates the score assigned by the perceptron to a data point x.

        Inputs:
            x: a node with shape (1 x dimensions)
        Returns: a node containing a single number (the score)
        """
        "*** YOUR CODE HERE ***"

        return nn.DotProduct( self.w, x)

    def get_prediction(self, x):
        """
        Calculates the predicted class for a single data point `x`.

        Returns: 1 or -1
        """
        "*** YOUR CODE HERE ***"
        pred = nn.as_scalar(self.run(x))
        if pred >= 0:
        	return 1
        else:
        	return -1

    def train(self, dataset):
        """
        Train the perceptron until convergence.
        """
        "*** YOUR CODE HERE ***"
        mistakes= 1
        #print("I Ran")
        
        while(mistakes >0):
        	mistakes = 0
        	for x,y in dataset.iterate_once(1):
        		if nn.as_scalar(y) != self.get_prediction(x):
        			mistakes += 1
        			weight = self.w
        			weight.update(x, nn.as_scalar(y))

class RegressionModel(object):
    """
    A neural network model for approximating a function that maps from real
    numbers to real numbers. The network should be sufficiently large to be able
    to approximate sin(x) on the interval [-2pi, 2pi] to reasonable precision.
    """
    def __init__(self):
        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 1
        # Building 1st layer of the neural network
        l1_nodes = 20
        l2_nodes = 20

        self.w_0 = nn.Parameter(1,l1_nodes )
        self.b_0 = nn.Parameter(1,l1_nodes )

        self.w_1 = nn.Parameter(l1_nodes, l2_nodes)
        self.b_1 = nn.Parameter(1, l2_nodes)
        
        self.w_2 = nn.Parameter(l2_nodes, 1)
        self.b_2 = nn.Parameter(1, 1)



    def run(self, x):
        """
        Runs the model for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
        Returns:
            A node with shape (batch_size x 1) containing predicted y-values
        """
        "*** YOUR CODE HERE ***"
        #First Layer Computations
        w0 = nn.Linear(x, self.w_0)
        w0 = nn.AddBias(w0, self.b_0)
        # Activation Function
        w1 = nn.ReLU(w0)

        #Layer 2 Computations
        w1 = nn.Linear(w1, self.w_1)
        w1 = nn.AddBias(w1, self.b_1)
        w1 = nn.ReLU(w1)
		
		#Layer 3 Computations
        w2 = nn.Linear(w1, self.w_2)
        w2 = nn.AddBias(w2, self.b_2)

        return w2


    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        Inputs:
            x: a node with shape (batch_size x 1)
            y: a node with shape (batch_size x 1), containing the true y-values
                to be used for training
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"

        loss_node = nn.SquareLoss(self.run(x), y)
        return loss_node

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        learn_rate = -0.01
        a = 1
        while(a>0):
        	# print("Dataset Dimensions")
        	# print(nn.Constant(dataset.x))
        	# print(nn.Constant(dataset.y))
        	for x, y in dataset.iterate_once(self.batch_size):
        		loss_node = self.get_loss(x, y)
        		gradient = nn.gradients(loss_node, [self.w_0, self.b_0, self.w_1, self.b_1,self.w_2, self.b_2])

        		self.w_0.update(gradient[0], learn_rate)
        		self.b_0.update(gradient[1], learn_rate)
        		self.w_1.update(gradient[2], learn_rate)
        		self.b_1.update(gradient[3], learn_rate)
        		self.w_2.update(gradient[4], learn_rate)
        		self.b_2.update(gradient[5], learn_rate)

        	if nn.as_scalar(self.get_loss(nn.Constant(dataset.x), nn.Constant(dataset.y))) < 0.02:
        		a =0

        		

class DigitClassificationModel(object):
    """
    A model for handwritten digit classification using the MNIST dataset.

    Each handwritten digit is a 28x28 pixel grayscale image, which is flattened
    into a 784-dimensional vector for the purposes of this model. Each entry in
    the vector is a floating point number between 0 and 1.

    The goal is to sort each digit into one of 10 classes (number 0 through 9).

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Initialize your model parameters here
        
        "*** YOUR CODE HERE ***"
        
        self.batch_size = 50
        
        # Building 1st layer of the neural network
        l1_nodes = 70
        l2_nodes = 45

        self.w_0 = nn.Parameter(784,l1_nodes )
        self.b_0 = nn.Parameter(1,l1_nodes )

        self.w_1 = nn.Parameter(l1_nodes, l2_nodes)
        self.b_1 = nn.Parameter(1, l2_nodes)
        
        self.w_2 = nn.Parameter(l2_nodes, 10)
        self.b_2 = nn.Parameter(1, 10)
    

    def run(self, x):
        """
        Runs the model for a batch of examples.

        Your model should predict a node with shape (batch_size x 10),
        containing scores. Higher scores correspond to greater probability of
        the image belonging to a particular class.

        Inputs:
            x: a node with shape (batch_size x 784)
        Output:
            A node with shape (batch_size x 10) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"

        #First Layer Computations
        w0 = nn.Linear(x, self.w_0)
        w0 = nn.AddBias(w0, self.b_0)
        # Activation Function
        w1 = nn.ReLU(w0)

        #Layer 2 Computations
        w1 = nn.Linear(w1, self.w_1)
        w1 = nn.AddBias(w1, self.b_1)
        w1 = nn.ReLU(w1)
		
		#Layer 3 Computations
        w2 = nn.Linear(w1, self.w_2)
        w2 = nn.AddBias(w2, self.b_2)

        return w2        

    def get_loss(self, x, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 10). Each row is a one-hot vector encoding the correct
        digit class (0-9).

        Inputs:
            x: a node with shape (batch_size x 784)
            y: a node with shape (batch_size x 10)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        
        loss_node = nn.SoftmaxLoss (self.run(x), y)
        return loss_node

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"

        learn_rate = -0.01
        a = 1
        while(a>0):
        	for x, y in dataset.iterate_once(self.batch_size):
        		loss_node = self.get_loss(x, y)
        		gradient = nn.gradients(loss_node, [self.w_0, self.b_0, self.w_1, self.b_1,self.w_2, self.b_2])

        		self.w_0.update(gradient[0], learn_rate)
        		self.b_0.update(gradient[1], learn_rate)
        		self.w_1.update(gradient[2], learn_rate)
        		self.b_1.update(gradient[3], learn_rate)
        		self.w_2.update(gradient[4], learn_rate)
        		self.b_2.update(gradient[5], learn_rate)

        	val_acc = dataset.get_validation_accuracy()
        	#print(val_acc)
        	
        	if val_acc > 0.975:
        		a =0


class LanguageIDModel(object):
    """
    A model for language identification at a single-word granularity.

    (See RegressionModel for more information about the APIs of different
    methods here. We recommend that you implement the RegressionModel before
    working on this part of the project.)
    """
    def __init__(self):
        # Our dataset contains words from five different languages, and the
        # combined alphabets of the five languages contain a total of 47 unique
        # characters.
        # You can refer to self.num_chars or len(self.languages) in your code
        self.num_chars = 47
        self.languages = ["English", "Spanish", "Finnish", "Dutch", "Polish"]

        # Initialize your model parameters here
        "*** YOUR CODE HERE ***"
        self.batch_size = 50
        
        self.out_dim = 5
        self.l1_dim = 400
        self.l2_dim = 100

        self.w1 = nn.Parameter(self.num_chars, self.l1_dim)	 	# 1
        self.w2 = nn.Parameter(self.l1_dim	 , self.l1_dim)		# 2
        
        self.wh = nn.Parameter(self.l1_dim, self.l2_dim )
        self.b_1 = nn.Parameter(1, self.l2_dim)

        self.w3 = nn.Parameter(self.l2_dim, self.out_dim  )		# 3
        self.b_2 = nn.Parameter(1, self.out_dim)


    def run(self, xs):
        """
        Runs the model for a batch of examples.

        Although words have different lengths, our data processing guarantees
        that within a single batch, all words will be of the same length (L).

        Here `xs` will be a list of length L. Each element of `xs` will be a
        node with shape (batch_size x self.num_chars), where every row in the
        array is a one-hot vector encoding of a character. For example, if we
        have a batch of 8 three-letter words where the last word is "cat", then
        xs[1] will be a node that contains a 1 at position (7, 0). Here the
        index 7 reflects the fact that "cat" is the last word in the batch, and
        the index 0 reflects the fact that the letter "a" is the inital (0th)
        letter of our combined alphabet for this task.

        Your model should use a Recurrent Neural Network to summarize the list
        `xs` into a single node of shape (batch_size x hidden_size), for your
        choice of hidden_size. It should then calculate a node of shape
        (batch_size x 5) containing scores, where higher scores correspond to
        greater probability of the word originating from a particular language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
        Returns:
            A node with shape (batch_size x 5) containing predicted scores
                (also called logits)
        """
        "*** YOUR CODE HERE ***"

        h1 = nn.Linear(xs[0], self.w1)
        #print(h1)
        #print(xs)
        h2 = h1
        for i, j in enumerate(xs[1:]):
        	h1 = nn.Add(nn.Linear(j, self.w1),nn.Linear(h1, self.w2)) #)nn.Add(nn.Linear(j, self.w1), 
        
        fn = nn.Linear(h1, self.wh)
        fn = nn.AddBias(fn, self.b_1)
        fn = nn.ReLU(fn)
        
        gn = nn.Linear(fn, self.w3)
        gn = nn.AddBias(gn, self.b_2)
        return gn


    def get_loss(self, xs, y):
        """
        Computes the loss for a batch of examples.

        The correct labels `y` are represented as a node with shape
        (batch_size x 5). Each row is a one-hot vector encoding the correct
        language.

        Inputs:
            xs: a list with L elements (one per character), where each element
                is a node with shape (batch_size x self.num_chars)
            y: a node with shape (batch_size x 5)
        Returns: a loss node
        """
        "*** YOUR CODE HERE ***"
        loss_node = nn.SoftmaxLoss(self.run(xs), y)

        return loss_node

    def train(self, dataset):
        """
        Trains the model.
        """
        "*** YOUR CODE HERE ***"
        val_acc =0
        if val_acc >0.82:
        	learn_rate = -0.001
        else:
        	learn_rate = -0.005
        a = 1
        while(a>0):
        	for x, y in dataset.iterate_once(self.batch_size):
        		loss_node = self.get_loss(x, y)

        		gradient = nn.gradients(loss_node, [self.w1, self.w2, self.w3, self.wh, self.b_1, self.b_2]) # 

        		self.w1.update(gradient[0], learn_rate)
        		self.w2.update(gradient[1], learn_rate)
        		self.w3.update(gradient[2], learn_rate)
        		self.wh.update(gradient[3], learn_rate)
        		self.b_1.update(gradient[4], learn_rate)
        		self.b_2.update(gradient[5], learn_rate)

        	val_acc = dataset.get_validation_accuracy()
        	#print(val_acc)
        	
        	if val_acc > 0.85:
        		a =0