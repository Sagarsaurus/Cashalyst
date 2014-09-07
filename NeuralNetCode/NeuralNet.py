import copy
import sys
import math
from datetime import datetime
from math import exp
from random import random, randint, choice

class Perceptron(object):
    """
    Class to represent a single Perceptron in the net.
    """
    def __init__(self, inSize=1, weights=None):
        self.inSize = inSize+1#number of perceptrons feeding into this one; add one for bias
        if weights is None:
            #weights of previous layers into this one, random if passed in as None
            self.weights = [1.0]*self.inSize
            self.setRandomWeights()
        else:
            self.weights = weights
    
    def getWeightedSum(self, inActs):
        """
        Returns the sum of the input weighted by the weights.
        
        Inputs:
            inActs (list<float/int>): input values, same as length as inSize
        Returns:
            float
            The weighted sum
        """
        return sum([inAct*inWt for inAct,inWt in zip(inActs,self.weights)])
    
    def sigmoid(self, value):
        """
        Return the value of a sigmoid function.
        
        Args:
            value (float): the value to get sigmoid for
        Returns:
            float
            The output of the sigmoid function parametrized by 
            the value.
        """
        return 1 / (1 + math.exp(-value)) 
    def sigmoidActivation(self, inActs):                                       
        """
        Returns the activation value of this Perceptron with the given input.
        Same as rounded g(z) in book.
        Remember to add 1 to the start of inActs for the bias input.
        
        Inputs:
            inActs (list<float/int>): input values, not including bias
        Returns:
            int
            The rounded value of the sigmoid of the weighted input
        """
        totalAct = self.getWeightedSum([1] + inActs)
        return self.sigmoid(totalAct)

    def sigmoidDeriv(self, value):
        """
        Return the value of the derivative of a sigmoid function.
        
        Args:
            value (float): the value to get sigmoid for
        Returns:
            float
            The output of the derivative of a sigmoid function
            parametrized by the value.
        """
        return math.exp(value) / ((1 + math.exp(value))**2)
         
    def sigmoidActivationDeriv(self, inActs):
        """
        Returns the derivative of the activation of this Perceptron with the
        given input. Same as g'(z) in book (note that this is not rounded.
        Remember to add 1 to the start of inActs for the bias input.
        
        Inputs:
            inActs (list<float/int>): input values, not including bias
        Returns:
            int
            The derivative of the sigmoid of the weighted input
        """
        totalAct = self.getWeightedSum([1] + inActs)
        return self.sigmoidDeriv(totalAct)
    
    def updateWeights(self, inActs, alpha, delta, previousWeights):
        """
        Updates the weights for this Perceptron given the input delta.
        Remember to add 1 to the start of inActs for the bias input.
        
        Inputs:
            inActs (list<float/int>): input values, not including bias
            alpha (float): The learning rate
            delta (float): If this is an output, then g'(z)*error
                           If this is a hidden unit, then the as defined-
                           g'(z)*sum over weight*delta for the next layer
        Returns:
            float
            Return the total modification of all the weights (absolute total)
        """
        totalModification = 0
        """YOUR CODE"""
        newList = list(inActs)
        newList.insert(0, 1.0)
        weights = []
        update = 0
        for i in range(len(newList)):
            
            if len(previousWeights) == 0:
                update = alpha * delta * newList[i]
            else:
                update = alpha * delta * newList[i] + 0.7 * previousWeights[i]
         #       print 0.8 * previousWeights[i]
            weights.append(update)
            totalModification += abs(update)
            self.weights[i] += update
        return weights, totalModification   
    def setRandomWeights(self):
        """
        Generates random input weights that vary from -1.0 to 1.0
        """
        for i in range(self.inSize):
            self.weights[i] = (random() + .0001) * (choice([-1,1]))
        
    def __str__(self):
        """ toString """
        outStr = ''
        outStr += 'Perceptron with %d inputs\n'%self.inSize
        outStr += 'Node input weights %s\n'%str(self.weights)
        return outStr

class NeuralNet(object):                                    
    """
    Class to hold the net of perceptrons and implement functions for it.
    """          
    def __init__(self, layerSize):#default 3 layer, 1 percep per layer
        """
        Initiates the NN with the given sizes.
        
        Args:
            layerSize (list<int>): the number of perceptrons in each layer 
        """
        self.layerSize = layerSize #Holds number of inputs and percepetrons in each layer
        self.outputLayer = []
        self.numHiddenLayers = len(layerSize)-2
        self.hiddenLayers = [[] for x in range(self.numHiddenLayers)]
        self.numLayers =  self.numHiddenLayers+1
        
        #build hidden layer(s)        
        for h in range(self.numHiddenLayers):
            for p in range(layerSize[h+1]):
                percep = Perceptron(layerSize[h]) # num of perceps feeding into this one
                self.hiddenLayers[h].append(percep)
 
        #build output layer
        for i in range(layerSize[-1]):
            percep = Perceptron(layerSize[-2]) # num of perceps feeding into this one
            self.outputLayer.append(percep)
            
        #build layers list that holds all layers in order - use this structure
        # to implement back propagation
        self.layers = [self.hiddenLayers[h] for h in xrange(self.numHiddenLayers)] + [self.outputLayer]
  
    def __str__(self):
        """toString"""
        outStr = ''
        outStr +='\n'
        for hiddenIndex in range(self.numHiddenLayers):
            outStr += '\nHidden Layer #%d'%hiddenIndex
            for index in range(len(self.hiddenLayers[hiddenIndex])):
                outStr += 'Percep #%d: %s'%(index,str(self.hiddenLayers[hiddenIndex][index]))
            outStr +='\n'
        for i in range(len(self.outputLayer)):
            outStr += 'Output Percep #%d:%s'%(i,str(self.outputLayer[i]))
        return outStr
    
    def feedForward(self, inActs):
        """
        Propagate input vector forward to calculate outputs.
        
        Args:
            inActs (list<float>): the input to the NN (an example) 
        Returns:
            list<list<float/int>>
            A list of lists. The first list is the input list, and the others are
            lists of the output values 0f all perceptrons in each layer.
        """
        returnLists = []
        returnLists.append(inActs)

        layerList = inActs

        for layer in self.layers:
            oldLayerList = layerList
            layerList = []
            for perc in layer:
                layerList.append(perc.sigmoidActivation(oldLayerList))
            returnLists.append(layerList)
        return returnLists
    
    def backPropLearning(self, examples, alpha):
        """
        Run a single iteration of backward propagation learning algorithm.
        See the text and slides for pseudo code.
        NOTE : the pseudo code in the book has an error - 
        you should not update the weights while backpropagating; 
        follow the comments below or the description in lecture.
        
        Args: 
            examples (list<tuple<list,list>>):for each tuple first element is input(feature) "vector" (list)
                                                             second element is output "vector" (list)
            alpha (float): the alpha to training with
        Returns
           tuple<float,float>
           
           A tuple of averageError and averageWeightChange, to be used as stopping conditions. 
           averageError is the summed error^2/2 of all examples, divided by numExamples*numOutputs.
           averageWeightChange is the summed weight change of all perceptrons, divided by the sum of 
               their input sizes.
        """
        #keep track of output
        averageError = 0
        averageWeightChange = 0
        numWeights = 0
        previousWeightChanges = [] 
        
        for layerIndex in range(len(self.layers)):
            previousWeightChanges.append([])
            layer = self.layers[layerIndex]
            for nodeIndex in range(len(layer)):
                previousWeightChanges[layerIndex].append([]) 
        
        for example in examples:#for each example
            for layer in self.layers:
                for node in layer:
                    numWeights += len(node.weights)
        
            deltas = []
            allDeltas = []
            """YOUR CODE"""
            """Get output of all layers"""
            netOutputs = self.feedForward(example[0])
            exampleInputs = example[0]
            exampleOutputs = example[1]
            outputLayer = self.layers[len(self.layers) - 1]
            
            delta = []
            for nodeIndex in range(len(outputLayer)):
                error = exampleOutputs[nodeIndex] - netOutputs[len(netOutputs) - 1][nodeIndex]
                ini = netOutputs[len(netOutputs) - 2]
                deriv = outputLayer[nodeIndex].sigmoidActivationDeriv(ini)
                deltas.append(deriv * error)
                averageError += (error**2)/2
            allDeltas.append(deltas)
            deltas = []

             
            for iLayerIndex in range(self.numHiddenLayers):
                layerIndex = self.numHiddenLayers - iLayerIndex - 1
                jLayerIndex = layerIndex + 1
                iLayer = self.layers[layerIndex]
                jLayer = self.layers[jLayerIndex]
                for iIndex in range(len(iLayer)):
                    summation = 0
                    for jIndex in range(len(jLayer)):
                        summation += allDeltas[0][jIndex] * jLayer[jIndex].weights[iIndex + 1]
                    deriv = iLayer[iIndex].sigmoidActivationDeriv(netOutputs[layerIndex])
                    deltas.append(deriv * summation)
                allDeltas.insert(0, deltas)
               
            for layerIndex in range(len(self.layers)):
                layer = self.layers[layerIndex]
                for nodeIndex in range(len(layer)):
                    newWeightsUpdate, averageChange = layer[nodeIndex].updateWeights(netOutputs[layerIndex], alpha, allDeltas[layerIndex][nodeIndex], previousWeightChanges[layerIndex][nodeIndex])
                    averageWeightChange += averageChange
                    previousWeightChanges[layerIndex][nodeIndex] = newWeightsUpdate
            """
            Calculate output errors for each output perceptron and keep track 
            of error sum. Add error delta values to list.
            """
           
            """
            Backpropagate through all hidden layers, calculating and storing
            the deltas for each perceptron layer.
            """

            """
            Having aggregated all deltas, update the weights of the 
            hidden and output layers accordingly.
            """ 
        #end for each example
        
        """Calculate final output"""
        averageWeightChange /= numWeights
        averageError /= len(examples) * len(self.layers[len(self.layers) - 1])
        return averageError, averageWeightChange
    
def buildNeuralNet(examples, alpha=0.1, weightChangeThreshold = 0.00008,hiddenLayerList = [1], maxItr = sys.maxint, startNNet = None):
    """
    Train a neural net for the given input.
    
    Args: 
        examples (tuple<list<tuple<list,list>>,
                        list<tuple<list,list>>>): A tuple of training and test examples
        alpha (float): the alpha to train with
        weightChangeThreshold (float):           The threshold to stop training at
        maxItr (int):                            Maximum number of iterations to run
        hiddenLayerList (list<int>):             The list of numbers of Perceptrons 
                                                 for the hidden layer(s). 
        startNNet (NeuralNet):                   A NeuralNet to train, or none if a new NeuralNet
                                                 can be trained from random weights.
    Returns
       tuple<NeuralNet,float>
       
       A tuple of the trained Neural Network and the accuracy that it achieved 
       once the weight modification reached the threshold, or the iteration 
       exceeds the maximum iteration.
    """

    
    examplesTrain,examplesTest = examples       
    numIn = len(examplesTrain[0][0])
    numOut = len(examplesTest[0][1])     
    time = datetime.now().time()
    if startNNet is not None:
        hiddenLayerList = [len(layer) for layer in startNNet.hiddenLayers]
    print "Starting training at time %s with %d inputs, %d outputs, %s hidden layers, size of training set %d, and size of test set %d"\
                                                    %(str(time),numIn,numOut,str(hiddenLayerList),len(examplesTrain),len(examplesTest))
    layerList = [numIn]+hiddenLayerList+[numOut]
    nnet = NeuralNet(layerList)                                                    
    if startNNet is not None:
        nnet =startNNet
    """
    YOUR CODE
    """
    iteration=0
    trainError=0
    weightMod=1
    error = 1.0 
    while iteration < maxItr and weightMod > weightChangeThreshold  and error > 0.00010: #0.0035 for 5 day
        iteration+=1
        error, weightMod = nnet.backPropLearning(examplesTrain, alpha)
        trainError += error
        if iteration%1000==0:
            print '! on iteration %d; training error %f and weight change %f'%(iteration,error,weightMod)
        #else :
            #print '.',
        
          
    time = datetime.now().time()
    print 'Finished after %d iterations at time %s with training error %f and weight change %f'%(iteration,str(time),trainError,weightMod)
                
    """
    Get the accuracy of your Neural Network on the test examples.
    """ 
    
    testError = 0
    testGood = 0     
    
    thresh = 0.03
    testAccuracy=0#num correct/num total
    results = [] 
    for example in examplesTest:
        feedForwardResult = nnet.feedForward(example[0])
        results.append((example[1][0], feedForwardResult[len(feedForwardResult)-1][0]))
        if(example[1][0] + thresh > feedForwardResult[len(feedForwardResult)-1][0] and example[1][0] - thresh < feedForwardResult[len(feedForwardResult)-1][0]):
            testGood += 1
        else:
            testError += 1
    testAccuracy = float(testGood) / (testGood + testError)


    print 'Feed Forward Test correctly classified %d, incorrectly classified %d, test percent correct  %f\n'%(testGood,testError,testAccuracy)
    
    """return something"""
    return results, nnet, testAccuracy

