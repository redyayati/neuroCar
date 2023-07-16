from matrix import Matrix 
import math 
import random
def sigmoid(x): 
    return 1 / (1 + math.exp(-x))
def dsigmoid(y) : 
    return y*(1-y)
class NeuralNetwork(): 
    # a is num_inputs
    # b is numJ_hidden 
    # c is num_outputs
    def __init__(self, a , b=1, c=1) : 
        if type(a) == type(self) : 
            self.numI = a.numI
            self.numH = a.numH
            self.numO = a.numO
            self.weights_HI = a.weights_HI.copy()
            self.bias_HI = a.bias_HI.copy()
            self.weights_OH = a.weights_OH.copy()
            self.bias_OH = a.bias_OH.copy()
        else : 
            self.numI = a
            self.numH = b 
            self.numO = c 
            self.weights_HI = Matrix(self.numH,self.numI)
            self.bias_HI = Matrix(self.numH, 1)
            self.weights_HI.randomize()
            self.bias_HI.randomize()
            self.weights_OH = Matrix(self.numO,self.numH)
            self.bias_OH = Matrix(self.numO,1)
            self.weights_OH.randomize()
            self.bias_OH.randomize()
        self.setLearningRate(.1)
    def predict(self , inputs) :  
        #  Convert user input in array form to Matrix object
        input = Matrix.toMatrix(inputs)
        # creating hidden layer = {weight matrix * input vector}
        hidden = Matrix.multiply(self.weights_HI , input)
        # adding bias 
        hidden.add(self.bias_HI)
        # appying sigmoid function to each element of the matrix to normalize
        hidden.zap(sigmoid)
        # Applying same procedure to next layer 
        output = Matrix.multiply(self.weights_OH , hidden)
        output.add(self.bias_OH) 
        output.zap(sigmoid)                     
        output = Matrix.fromMatrix(output)
        return output 

    def train(self,inputs,targets) :
        # copied from feed forward just to keep the intermidiate variables
        input = Matrix.toMatrix(inputs)
        hidden = Matrix.multiply(self.weights_HI , input)
        hidden.add(self.bias_HI)
        hidden.zap(sigmoid)
        output = Matrix.multiply(self.weights_OH , hidden)
        output.add(self.bias_OH) 
        output.zap(sigmoid)

        # Calculating error matrix
        # Error = Target - Outputs
        target = Matrix.toMatrix(targets)
        error_output = Matrix.substract(target , output)
        
        # let gradient = ouput * (1 - output)
        # calculate gradient between hidden and output 
        gradient = Matrix.zapn(output,dsigmoid)
        # Multiply element-wise by error and then by learning rate
        gradient.multiplyn(error_output)
        gradient.multiplyn(self.learning_rate)
        
        # calculate deltas
        # delta weights = lr * out(1-out) * Hidden_T
        hidden_T = Matrix.transpose(hidden)
        weights_HO_deltas = Matrix.multiply(gradient , hidden_T)

        # Adjudt the weights by its deltas
        self.weights_OH.add(weights_HO_deltas)
        # Adjust the bias with deltas (which is just the gradients)
        self.bias_OH.add(gradient)

        # Calculating hidden layer errors as done above for output layer
        weights_HO_T = Matrix.transpose(self.weights_OH)
        error_hidden = Matrix.multiply(weights_HO_T , error_output)
        # calculate hidden gradient
        hidden_gradient = Matrix.zapn(hidden,dsigmoid)
        hidden_gradient.multiplyn(error_hidden)
        hidden_gradient.multiplyn(self.learning_rate)
        # calculate input to hidden deltas
        inputs_T = Matrix.transpose(input)
        weights_IH_deltas = Matrix.multiply(hidden_gradient,inputs_T)
        self.weights_HI.add(weights_IH_deltas)
        self.bias_HI.add(hidden_gradient)
        
    def setLearningRate(self,lr) : 
        self.learning_rate = lr
    def mutate(self,rate) :  
        def mutate(val) : 
            if random.random() < rate : 
                return val + random.gauss(0,.5)
            else : return val
        self.weights_HI.zap(mutate)
        self.weights_OH.zap(mutate)
        self.bias_HI.zap(mutate)
        self.bias_OH.zap(mutate)
        
    def copy(self) : 
        return NeuralNetwork(self)

