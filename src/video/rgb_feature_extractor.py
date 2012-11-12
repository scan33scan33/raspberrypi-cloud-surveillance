import sys
from PIL import Image
from matplotlib import pyplot

# Given an image filename, this function will extract the feature vector of the image
def Extract(filename):
    feature_vector = [] # feature vector to return
    im = Image.open(filename)
    # Fill `feature_vector'
    for tup in list(im.getdata()):
	for x in tup:
            feature_vector.append(x)
    return feature_vector

if __name__ == '__main__':
    feature_vector = Extract(sys.argv[1])
    pyplot.figure()
    pyplot.plot(feature_vector, 'r')
    pyplot.show()
