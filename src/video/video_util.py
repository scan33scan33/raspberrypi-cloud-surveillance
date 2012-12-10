import rgb_feature_extractor
import sys
import os
import logging

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
    if DiffImage(image1_filename, image2_filename) > 20:
        return -1
    else:
        return 1

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


if __name__ == '__main__':
    print IsGoodVideo(sys.argv[1])
    pass
