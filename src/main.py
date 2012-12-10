# We run two threads:
# Thread 1 will take videos
# Thread 2 will check the videos and upload with appropriate flag

import os
import calendar
import time
from multiprocessing import Process
import sys
sys.path.append('./video')
import video_util
sys.path.append('./cloud')
import dropbox_util
import logging

# Mainly for profiling logging
# FIXME: We may want to make it prettier... (or making this in another file)
FORMAT = '%(asctime)-15s %(message)s'
logging.basicConfig(format=FORMAT)
Log = logging.getLogger('video')

def Record(filename):
    Log.warning('process 1 started recording')
    os.system('ffmpeg -loglevel quiet -v quiet -t 0:00:10 -f video4linux2' +
              ' -s 160x120 -i /dev/video0 ' + filename)
    Log.warning('process 1 stopped recording')

def CheckAndUpload(cloud_filename, local_filename):
    while not os.path.exists(local_filename):
	# This sleep is for waiting recording to be finished
	time.sleep(15)
        continue
    flag = video_util.IsGoodVideo(local_filename)
    if flag == False:
        cloud_filename += '_bad'
    cloud_filename += '.mpeg'
    dropbox_util.upload(cloud_filename, local_filename)
   

if __name__ == '__main__':
    while 1:
        gmtime = time.gmtime()
        strtime = str(gmtime.tm_year) + '-' + str(gmtime.tm_mon) + '-' + str(gmtime.tm_mday) + '-' + str(gmtime.tm_hour) + ':' + str(gmtime.tm_min) + ':' + str(gmtime.tm_sec)
        local_filename = '/tmp/record' + '_' + strtime + '.mpeg'
        name = 'cameraA'
        cloud_filename = name + '_' + strtime

        p = Process(target=Record, args=(local_filename,))
        p.start()
        p2 = Process(target=CheckAndUpload, args=(cloud_filename, local_filename,))
        p2.start()
	# We should wait Process p(, which records the video,) to finish 
	p.join()
