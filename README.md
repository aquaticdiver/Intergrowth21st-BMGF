ReadME is a work in progress 08/07/18

UltrasoundClassifier

Model Weights can be found under the weights section, with the code located in UltrasoundClassifier.ipynb 
Labeled Training Set data, can be found at https://www.synapse.org/#!Synapse:syn15588818
Labeled CSV can be found at https://www.synapse.org/#!Synapse:syn15589307
The classifier takes in a dataset, and a csv with ground truth values of labels for training. In exploring validation set, the plots take the different classes as the input.

UltrasoundSizer

Takes a directory as an input and calculates the pixel distance between the ruler markings and creates a csv with path and metric. The true distances between each tick mark is 1 centimeter. This is the resolution in def find_distance(y, resolution = 1.0).

DicomReader

Takes a directory as an input and produces a manifest of annotations, paths, and a new filename to be uploaded to synapse via fileview csv upload.
