from sklearn.datasets import load_digits
import matplotlib.pyplot as plt  # showing digits
from PIL import Image           # loading from file

from abc import abstractmethod, ABC
from typing import List
import numpy as np

np.random.seed(1)

mnist = load_digits()

XOR_x = np.array([[[0, 0]], [[0, 1]], [[1, 0]], [[1, 1]]])
XOR_y = np.array([[[0]], [[1]], [[1]], [[0]]])

# parameters

learningRate = 0.1
epochs = 100

epsilonXOR = 0.000001  # only for XOR
architectureXOR = [3, 3]
# MNIST
architectureMNIST = [50, 20, 10]
epsilonMNIST = 0.002  # 99%


class Layer(ABC):
    """Basic building block of the Neural Network"""

    def __init__(self) -> None:
        self._learning_rate = 0.01

    @abstractmethod
    def forward(self, x: np.ndarray) -> np.ndarray:
        """Forward propagation of x through layer"""
        pass

    @abstractmethod
    def backward(self, output_error_derivative) -> np.ndarray:
        """Backward propagation of output_error_derivative through layer"""
        pass

    @property
    def learning_rate(self):
        return self._learning_rate

    @learning_rate.setter
    def learning_rate(self, learning_rate):
        assert learning_rate < 1, f"Given learning_rate={learning_rate} is larger than 1"
        assert learning_rate > 0, f"Given learning_rate={learning_rate} is smaller than 0"
        self._learning_rate = learning_rate


class FullyConnected(Layer):
    def __init__(self, input_size: int, output_size: int) -> None:
        super().__init__()
        self.input_size = input_size
        self.output_size = output_size

        # tanh is symmetrical around 0, so let's roll random values
        # around 0 too
        # [-1,1), mxn matrix
        self.weights = (np.random.rand(input_size, output_size)-0.5)/2
        # [-1,1) x input_size array
        self.bias = (np.random.rand(1, output_size)-0.5)/2

        self.inputs = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        '''
        Multiplies incoming values by weights and adds bias.
        X⋅weights+bias
         ^ dot product
        '''
        # remember this for backprop later
        self.inputs = np.array(x)  # @TODO: Copy needed?

        return x@self.weights+self.bias

    def backward(self, output_error_derivative: np.ndarray, learningRate) -> np.ndarray:
        '''
        From layer point of view, I am interested in
        how weights and biases influence error, and we want
        to minimise that. so we need dy/dw and dy/db, then follow the gradient.

        but other layers want the derivative too, so tell them how their
        data that is being fed here (input) changes the error.
        Therefore return dy/dx.
        '''
        wGradient = self.inputs.T@output_error_derivative

        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # this must be calculated before updating weights...
        # siedziałem do 3 w nocy żeby ten błąd znaleźć :)
        result = output_error_derivative@self.weights.T

        # subtract from weights, but not fully
        self.weights -= wGradient*learningRate

        # same for biases
        self.bias -= learningRate * output_error_derivative

        # return dy/dx

        return result


class Tanh(Layer):
    def __init__(self) -> None:
        super().__init__()
        self.inputs = None

    def forward(self, x: np.ndarray) -> np.ndarray:
        self.inputs = x
        return np.tanh(x)

    def backward(self, output_error_derivative, l) -> np.ndarray:
        # no weights to update here, pass back the derivative
        # from chain rule (?):
        # f(x) - our function (tanh)
        # y - error
        # x - our layer input
        # dy/dx = dy/df * df/dx
        return (1-np.tanh(self.inputs)**2) * output_error_derivative


class Loss:
    def __init__(self, loss_function: callable, loss_function_derivative: callable) -> None:
        self.loss_function = loss_function
        self.loss_function_derivative = loss_function_derivative

    def loss(self, x: np.ndarray, y: np.ndarray) -> float:
        """Loss function for a particular x """
        return self.loss_function(x, y)

    def loss_derivative(self, x: np.ndarray, y: np.ndarray) -> np.ndarray:
        """Loss function derivative for a particular x and y"""
        return self.loss_function_derivative(x, y)


class Network:
    def __init__(self, layers: List[Layer], learning_rate: float) -> None:
        self.layers = layers
        self.learning_rate = learning_rate
        self.loss = None

    def compile(self, loss: Loss) -> None:
        """Define the loss function and loss function derivative"""
        self.loss = loss

    def __call__(self, x: np.ndarray) -> np.ndarray:
        """Forward propagation of x through all layers"""
        current_input = x
        for layer in self.layers:
            current_input = layer.forward(current_input)
        return current_input

    def fit(self,
            x_train: np.ndarray,
            y_train: np.ndarray,
            epochs: int,
            epsilon: float,
            verbose: int = 0) -> None:
        """Fit the network to the training data"""

        for e in range(epochs):
            print("epoch", e+1)
            errorsum = 0
            for sample_x, target in zip(x_train, y_train):
                # forward pass
                result = self(sample_x)

                errorsum += self.loss.loss_function(result, target)

                derivative = self.loss.loss_derivative(result, target)
                for layer in self.layers[::-1]:
                    derivative = layer.backward(derivative, self.learning_rate)
            # sometimes it excells in some samples and is atricious at others,
            # therefore sum the errors of all samples and print this
            print("epoch error sum:", errorsum/len(x_train))
            if errorsum/len(x_train) < epsilon:
                return


def CreateNetwork(inputSize, networkShape, outputSize, rate):
    networkShape.append(outputSize)  # easier looping
    inputLayer = FullyConnected(inputSize, networkShape[0])
    inputTanh = Tanh()
    hiddenLayers = []
    for i in range(len(networkShape)-1):
        hiddenLayers.append(FullyConnected(networkShape[i], networkShape[i+1]))
        hiddenLayers.append(Tanh())

    # remove last tanh? Or no difference?
    allLayers = [inputLayer, inputTanh]+hiddenLayers

    return Network(allLayers, rate)


# Mean Squared Error
def msefunc(result, target):
    return np.mean(np.power(result-target, 2))


def msederivative(result, target):
    return 2*(result-target)/result.size


MSE = Loss(msefunc, msederivative)


# expects two training arrays of samples vs outputs
def FittedNetwork(inputs, outputs, networkShape, learningRate, epochCount, epsilon):

    inputSize = inputs[0].size
    outputSize = outputs[0].size

    # driver code
    net = CreateNetwork(inputSize, networkShape,
                        outputSize, learningRate)

    net.compile(MSE)

    net.fit(inputs, outputs, epochCount, epsilon)

    return net


# turns 0-9 numbers into 0,1 array
def NumbersToVectors(classes: np.ndarray):
    def AsVector(n, k):
        return np.array([[1 if x == n else 0 for x in range(k)]])

    biggest = classes.max()
    out = []
    for num in classes:
        out.append(AsVector(num, biggest+1))  # 0-9, not 1-9
    return out


def doXOR(epsilon, architecture):
    network = FittedNetwork(XOR_x, XOR_y, architecture,
                            learningRate, epochs, epsilon)

    result1 = network([0, 0])
    result2 = network([0, 1])
    result3 = network([1, 0])
    result4 = network([1, 1])

    print("results:", result1, result2, result3, result4)


def doMNIST(epsilon, architecture):
    # 5th index image is labeled as 5
    # but it looks like 9, can't blame the network
    # plt.imshow(mnist.images[5], cmap='binary')
    # plt.show()

    flattenedImages = np.array([[np.ndarray.flatten(img)]
                               for img in mnist.images])
    targetVectors = NumbersToVectors(mnist.target)
    network = FittedNetwork(flattenedImages,  targetVectors,
                            architecture, learningRate, epochs, epsilon)
    counter = 0
    for x, y in zip(flattenedImages, mnist.target):
        if np.argmax(network(x)) == y:
            counter += 1
    print(f"Train efficiency: {100*counter/len(targetVectors):.2f}%")

    while True:
        i = input(f"\nType index (max {len(flattenedImages)-1}) or 'file':")
        if i == "file":
            userImage = np.asarray(Image.open(
                'image.bmp').convert('L'), dtype='float64')/16
            plt.imshow(userImage, cmap='binary')
            plt.show()
            flattened = np.array([np.ndarray.flatten(userImage)])
            result = network(flattened)
        else:
            i = int(i)
            plt.imshow(mnist.images[i], cmap='binary')
            plt.show()
            img = Image.fromarray(mnist.images[i]*16).convert('L')
            img.save('image.bmp')
            print("target: ", mnist.target[i])
            result = network(flattenedImages[i])
        print("result: ", result.round(2))
        print(f"Guess: {np.argmax(result)}")


doMNIST(epsilonMNIST, architectureMNIST)
#doXOR(epsilonXOR, architectureXOR)
