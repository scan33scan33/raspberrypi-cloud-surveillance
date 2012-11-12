import rgb_feature_extractor
import sys
import os

# Compute the difference of two images(, involving different feature extractors.)
def DiffImage(image1_filename, image2_filename):
    feature_vector1 = rgb_feature_extractor.Extract(image1_filename)
    feature_vector2 = rgb_feature_extractor.Extract(image2_filename)
    diff = 0
    for i in range(len(feature_vector1)):
        diff += abs(feature_vector1[i] - feature_vector2[i])
    diff /= float(len(feature_vector1))
    return diff

def CompareImage(image1_filename, image2_filename):
    if DiffImage(image1_filename, image2_filename) > 20:
        return -1
    else:
        return 1

def IsGoodVideo(video_filename):
    is_good_video = True
    os.system('rm /tmp/*.png')
    os.system('ffmpeg -i ' + video_filename + ' /tmp/%d.png')
    for i in range(2,100000):
        image1_filename = '/tmp/' + str(i-1) + '.png'
        image2_filename = '/tmp/' + str(i) + '.png'
	if not os.path.exists(image2_filename):
	    break
        if CompareImage(image1_filename, image2_filename) < 0:
	    is_good_video = False # TODO: This will modify the folder name later...
    return is_good_video 


if __name__ == '__main__':
    print IsGoodVideo(sys.argv[1])
    pass
