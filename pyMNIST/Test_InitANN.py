import FeedforwardNeuralNet as Net

ann = Net.NeuralNet([4, 5, 3])
for i in range(len(ann.weight_matrices)):
    print(ann.weight_matrices[i], "\n\n")
    print(ann.bias_matrices[i], "\n\n")
    print(ann.weight_matrices[i][0], "\n\n", ann.weight_matrices[i][0][0])
