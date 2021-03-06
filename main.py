from numpy import exp, array, random, dot
import numpy as np
import xlrd
workbook = xlrd.open_workbook('weatherdata.xls')
worksheet = workbook.sheet_by_name('weatherdata')
num_rows = worksheet.nrows - 1
curr_row = 1

#creates an array to store all the rows
row_array = np.array([])
out_array = np.array([])
row_list = np.array([])
#print(worksheet.row(1))
print(len(worksheet.row(1)))


while curr_row < num_rows:
    row = worksheet.row(curr_row)[:16]
    for j in range(len(row)):
        element = np.float(row[j].value)
        row_list = np.append(row_list,element)
    row_array = np.concatenate([row_list,row_list],axis=0)
    curr_row += 1


# print(row_array)
row_array = np.resize(row_array,(8646,16))
# row_array = np.array(row_array).T

#Column 16 = Beginning of Electrical Consumption
out_array = worksheet.col(16)
for k in range(1,len(out_array)):
    out_array[k] = np.float(out_array[k].value)
out_array.pop(0)
out_array = np.resize(out_array,(8646,1))
print(np.shape(row_array))
print(np.shape(out_array))


class NeuralNetwork():
    def __init__(self):
        # Seed the random number generator, so it generates the same numbers
        # every time the program runs.
        random.seed(1)

        # We model a single neuron, with 16 input connections and 1 output connection.
        # We assign random weights to a 16 x 1 matrix, with values loosely bounded
        self.synaptic_weights = 2 * random.random((16,1)) - 1

    # The Sigmoid function, which describes an S shaped curve.
    # We pass the weighted sum of the inputs through this function to
    # normalise them between 0 and 1.
    def __sigmoid(self, x):
        return 1 / (1 + exp(-x))

    # The derivative of the Sigmoid function.
    # This is the gradient of the Sigmoid curve.
    # It indicates how confident we are about the existing weight.
    def __sigmoid_derivative(self, x):
        return x * (1 - x)

    # We train the neural network through a process of trial and error.
    # Adjusting the synaptic weights each time.
    def train(self, training_set_inputs, training_set_outputs, number_of_training_iterations):
        for iteration in range(number_of_training_iterations):
            # Pass the training set through our neural network (a single neuron).
            output = self.think(training_set_inputs)

            # Calculate the error (The difference between the desired output
            # and the predicted output).
            error = training_set_outputs - output

            # Multiply the error by the input and again by the gradient of the Sigmoid curve.
            # This means less confident weights are adjusted more.
            # This means inputs, which are zero, do not cause changes to the weights.
            adjustment = dot(training_set_inputs.T, error * self.__sigmoid_derivative(output))

            # Adjust the weights.
            self.synaptic_weights += adjustment

    # The neural network thinks.
    def think(self, inputs):
        # Pass inputs through our neural network (our single neuron).
        return self.__sigmoid(dot(inputs, self.synaptic_weights))


if __name__ == "__main__":

    #Intialise a single neuron neural network.
    neural_network = NeuralNetwork()

    print("Random starting synaptic weights: ")
    print(neural_network.synaptic_weights)

    # The training set. We have 4 examples, each consisting of 3 input values
    # and 1 output value.
    training_set_inputs = row_array
    training_set_outputs = out_array

    # Train the neural network using a training set.
    # Do it 10,000 times and make small adjustments each time.
    neural_network.train(training_set_inputs, training_set_outputs, 10000)

    print("New synaptic weights after training: ")
    print(neural_network.synaptic_weights)

    # Test the neural network with a new situation.
    print("Considering new situation [1,0,0,3,86,9,0,55.1,0.22,95.3,54.59,54.29,3.219043,22.72,59.21,0.006] -> ?: ")
    print(array([1,0,0,3,86,9,0,55.1,0.22,95.3,54.59,54.29,3.219043,22.72,59.21,0.006])*neural_network.synaptic_weights.T)
