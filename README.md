This is a Raspberrypi based surveillance system.
Everything is written with considering Debian-dependency
for ease of developing on Raspberrypi.

Functionality: Now, this program can record videos in short
periods, does uncommon clip detection on them, and finally
upload everything to Dropbox with bad videos flagged.

We include the feature by the paper:
Y. Jia and T. Darrell. ``Heavy-tailed Distances for Gradient 
Based Image Descriptors''. NIPS 2011, for feature extraction.

Please see ./src/README for more details.
