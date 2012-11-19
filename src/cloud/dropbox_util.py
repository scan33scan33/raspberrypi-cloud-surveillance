import time
import calendar

# Include the Dropbox SDK libraries
from dropbox import client, rest, session
# Get your app key and secret from the Dropbox developer website
APP_KEY = '0yi6d1p7onapbog'
APP_SECRET = 'nnrt56ff6773bp5'
# ACCESS_TYPE should be 'dropbox' or 'app_folder' as configured for your app
ACCESS_TYPE = 'app_folder'
sess = session.DropboxSession(APP_KEY, APP_SECRET, ACCESS_TYPE)
### Don't move statements above. It works for every file.

def upload(cloud_filename, local_filename):
    request_token = sess.obtain_request_token()
    # Make the user sign in and authorize this token
    url = sess.build_authorize_url(request_token)
    # This will fail if the user didn't visit the above URL and hit 'Allow'
    #access_token = sess.obtain_access_token(request_token)
    #print access_token.key
    #print access_token.secret
    sess.set_token("fezg51eqni5efux", "aoerdh2dal7o3e6")
    dropbox_client = client.DropboxClient(sess)
    # Application specific
    # print 'Making Dir: ' + dirname
    # client.file_create_folder(dirname)
    f = open(local_filename, 'r')
    dirname = "./"
    response = dropbox_client.put_file(dirname + cloud_filename, f)
    print "uploaded:", response

