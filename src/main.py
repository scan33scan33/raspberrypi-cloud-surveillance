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

def Record(filename):
    os.system('ffmpeg -loglevel quiet -v quiet -t 0:00:01 -f video4linux2 -s 160x120 -i /dev/video0 ' + filename)

def CheckAndUpload(cloud_filename, local_filename):
    while not os.path.exists(local_filename):
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
        p.join()
        p2.join()
