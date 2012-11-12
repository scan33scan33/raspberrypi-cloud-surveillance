# We run two threads:
# Thread 1 will take videos
# Thread 2 will check the videos and upload with appropriate flag

import os
import video.video_util
# TODO: Dropbox util...

if __name__ == '__main__':
    filename = '/tmp/record.mpeg'
    os.system('ffmpeg -loglevel quiet -v quiet -t 0:00:5 -f video4linux2 -s 160x120 -i /dev/video0 ' + filename)
    flag = video.video_util.IsGoodVideo(filename)
    
    outfilename = 'time'
    if flag == False:
        outfilename += '_bad'
    # Dropbox upload
