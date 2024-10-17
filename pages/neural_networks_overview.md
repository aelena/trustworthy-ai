# Brief overview of FNN, RNN, CNN, and LSTM

This can only be the most cursory overview of this complex topic. Excellent references exist elsewhere, and it is not really in the scope of a programme for AI Auditors based on Trustworthy AI to explore this topic in any depth.


<br/>


| Network Type | Full Name | Key Characteristics | Typical Applications |
|--------------|-----------|---------------------|----------------------|
| FNN | Feedforward Neural Network | - Simplest type of artificial neural network<br>- Information flows in one direction from input to output<br>- No loops or cycles in the network<br>- Frequently arranged in layers with units receiving inputs onlu from the immediately preceding layer | - Classification tasks<br>- Regression problems<br>- Pattern recognition |
| RNN | Recurrent Neural Network | - Designed for sequential data<br>- Has loops allowing information persistence<br>- Can process inputs of variable length | - Natural language processing<br>- Speech recognition<br>- Time series prediction |
| CNN | Convolutional Neural Network | - Inspired by the visual cortex<br>- Uses convolutional layers to detect patterns<br>- Effective at spatial feature extraction | - Image and video recognition<br>- Object detection<br>- Medical image analysis |
| LSTM | Long Short-Term Memory | - Special type of RNN<br>- Designed to handle long-term dependencies<br>- Uses memory cells and gates to control information flow | - Machine translation<br>- Speech synthesis<br>- Complex sequence generation |

## Key Differences

## Architectures
- **FNNs** have a simple layered structure with no feedback connections, therefore it forms a directed acyclic graph (no loops) with every node receiving their input from upstream and delivering its output to another node downstream. It has no other internal states than the weights. Frequently arranged in layers with units receiving inputs onlu from the immediately preceding layer. Multi-layer FNNs will have layers of hidden units not connected to the output of the network. Single-layer FNNs were the original [perceptrons](https://en.wikipedia.org/wiki/Perceptron). That is, a network with all inputs connected directly to the output is a perceptron network.
- **RNNs** in turn are different from FNNs in that they have feedback loops, feeding outputs back to inputs, allowing them to maintain internal states. This enables them to have short memory, making them more interesting and more similar to how the human brain works. Hidden Layers process the inputs and maintain a "memory" of previous inputs. Therefore the response of the network is influenced by its initial or previous states, and at the same time can either exhibit stable states as well as oscillations or chaotic behavior. [This](https://www.scaler.com/topics/rnn-architecture/) offers a visual explanation of this architecture. 
- **CNNs** enable powerful deep learning based techniques for processing, generating, and sensemaking of visual information. CNNs use convolutional and pooling layers for feature extraction. A CNN consists of multiple layers, including convolutional layers (which are the core component, hence the name), pooling layers, and fully connected layers. The convolutional layers apply a set of filters to the input image, detecting local features such as edges, textures, and shapes. The pooling layers reduce the spatial dimensions of the data, aggregating information and reducing computational complexity. The fully connected layers process the high-level features extracted by the convolutional and pooling layers to make predictions.
- **LSTMs** are a specialized form of RNN with memory cells and gating mechanisms[4]. This allows them to learn long-term dependencies in data, and are used in various fields such as customer service, content creation, and coding. They are designed to handle the [vanishing gradient problem](https://deepai.org/machine-learning-glossary-and-terms/vanishing-gradient-problem) that occurs in traditional RNNs, by using a memory cell that can store information for long periods of time, and three gates that control the flow of information into and out of the cell.

**Data Handling:**
- FNNs work well with fixed-size inputs[1].
- RNNs and LSTMs excel at processing sequential data of varying lengths[2][4].
- CNNs are particularly effective for data with spatial relationships, like images[1][4].

**Memory:**
- FNNs have no memory of previous inputs[1].
- RNNs have short-term memory capabilities[2].
- LSTMs can capture long-term dependencies in data[4].
- CNNs don't have explicit memory but can learn spatial hierarchies[1].

**Applications:**
- FNNs are versatile and used in various classification and regression tasks[1].
- RNNs and LSTMs are often used in natural language processing and time series analysis[2][3]. More specifically, there are several types of RNN:
  - One-to-One: Standard feedforward neural network
  - One-to-Many: e.g., Image captioning
  - Many-to-One: e.g., Sentiment analysis
  - Many-to-Many: e.g., Machine translation, speech recognition
- CNNs dominate in computer vision tasks and have been adapted for text and time series data[1][4].

This comparison highlights the unique strengths of each neural network type, showing how they are suited for different types of data and problem domains[1][2][3][4].

## Citations
- [1] https://levity.ai/blog/neural-networks-cnn-ann-rnn
- [2] https://www.techtarget.com/searchenterpriseai/feature/CNN-vs-RNN-How-they-differ-and-where-they-overlap
- [3] https://training.galaxyproject.org/training-material/topics/statistics/tutorials/RNN/tutorial.html
- [4] https://viso.ai/deep-learning/deep-neural-network-three-popular-types/
- [5] https://machinelearningmastery.com/when-to-use-mlp-cnn-and-rnn-neural-networks/
- [6] https://www.deeplearningwizard.com/deep_learning/practical_pytorch/pytorch_recurrent_neuralnetwork/
- [7] https://www.scaler.com/topics/rnn-architecture/

- Also from **Artificial Intelligence, A Modern Approach, 3rd Edition**, by Peter Norvig and Stuart Russell.