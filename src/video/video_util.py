import rgb_feature_extractor
import dsift_feature_extractor
import sys
import os
import logging

RGBDiffWarning = 20
SIFTDiffWarning = 100


# Mainly for profiling logging
# FIXME: We may want to make it prettier... (or making this in another file)
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
Log = logging.getLogger('video')

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
    if DiffImage(image1_filename, image2_filename) > RGBDiffWarning:
        return -1
    else:
        return 1

def CompareImageSIFT(image1_filename, image2_filename):
    from scipy import misc
    # set up extractor 
    extractor = dsift_feature_extractor.DsiftExtractor(32, 64, 1)
    # extractor = dsift_feature_extractor.DsiftExtractor(8, 16, 1)
    # read images
    image1 = misc.imread(image1_filename)
    image2 = misc.imread(image2_filename)
    # feature extraction
    feaArr1, positions1 = extractor.process_image(image1)
    feaArr2, positions2 = extractor.process_image(image2)
    
    # Match the feature points
    n_match = 0
    for i in range(len(feaArr1)):
        for j in range(len(feaArr2)):
            if sum(abs(feaArr1[i] - feaArr2[j])) < 1:
                n_match += 1
                break
    Log.info("Number of matched keypoints by SIFT: " + str(n_match))
    # Compute the similarity of two images by an ad-hoc function
    if len(feaArr1) + len(feaArr2) - 2 * n_match < SIFTDiffWarning:
        return True
    return False

def IsGoodVideo(video_filename):
    video_filename_prefix = video_filename.split('.')[0].split('/')[2]
    Log.warning('video: ' + video_filename_prefix)
    is_good_video = True
    Log.warning('ffmpeg began decoding videos to images')
    os.system('ffmpeg -i ' + video_filename + ' /tmp/' + video_filename_prefix + '_%d.png')
    Log.warning('ffmpeg has decoded videos to images')
    Log.warning('abnormal video checking began')
    # We jump 'jump_frame' frames each check to make the process faster
    # FIXME: we can make the interval parameter somewhere outside and remove '100000'
    jump_frame = 5
    for i in range(1 + jump_frame, 100000, jump_frame):
        image1_filename = '/tmp/' + video_filename_prefix + '_' + str(i - jump_frame) + '.png'
        image2_filename = '/tmp/' + video_filename_prefix + '_' + str(i) + '.png'
	if not os.path.exists(image2_filename):
	    break
        if CompareImage(image1_filename, image2_filename) < 0:
	    is_good_video = False # TODO: This will modify the folder name later...
    os.system('rm -f /tmp/' + video_filename + '*.png')
    Log.warning('abnormal video checking ended')
    return is_good_video 

def TestDsiftFeatureExtractor():
    # TODO: change to assert...
    # expect -1
    print CompareImageSIFT('./data/lena.png', './data/tux.png')
    # expect 1
    print CompareImageSIFT('./data/lena.png', './data/lena_greyscale.png')

if __name__ == '__main__':
    # TODO: move the test out of this file.
    TestDsiftFeatureExtractor()
    # print IsGoodVideo(sys.argv[1])
    pass
