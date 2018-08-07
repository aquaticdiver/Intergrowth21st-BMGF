#!/usr/bin/env python

# Copyright 2017-present, Bill & Melinda Gates Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
import csv
from PIL import Image
import numpy as np

PATH = "path/to/file/"
OUTFILE = "measures.csv"

def find_images(root, suffix='bmp'):
    '''
    Search the folder named root for images of the type given in suffix.
    Returns a list of file paths. 
    '''
    images = []
    for path, dirs, files in os.walk(root):
        for file in files:
            if file.lower().endswith("bmp"):
                images.append("{0}\{1}".format(path, file))
                
    return images
    

def preprocess(path):
    '''
    Reads the image from the given path and applies preprocessing tasks on it.
    
    Returns the processed image and the collection of pixels that are of 
    interest.
    '''
    img = Image.open(path)
    box = (100,100,200,400)
    cropimg = img.crop(box)
    
    found_pixels = []
    for i, pixel in enumerate(cropimg.getdata()):
        if pixel == (119, 119, 119):
            found_pixels.append(i)
    
    return cropimg, found_pixels

def find_heights(cropimg, pixels):
    '''
    Fine the heights of each line in the ruler.
    
    Takes the processed image and the pixels of interest as parameters.
    '''
    width, height = cropimg.size
    found_pixels_coords = [divmod(index, width) for index in pixels]
    y, x = zip(*found_pixels_coords)
    
    return x, y


def find_distance(y, resolution=1.0):
    '''
    Find the distance between two lines in the rule. 
    
    The lines may only be approximately equally spaced. There for the
    modal distance is returned.
    '''
    unique_heights = np.unique(y)
    mid_tup = zip(*[iter(unique_heights)]*3)
    pixel_mid_height = [x[1] for x in mid_tup] 
    distances = [abs(y-x)/resolution for x, y in zip(pixel_mid_height, pixel_mid_height[1:])]
    
    return max(set(distances), key=distances.count)



def main(outfile):
    with open(outfile,'w') as fp:
        writer = csv.writer(fp)
        for p in find_images(PATH):
            cropimg, found_pixels = preprocess(p)
            x, y = find_heights(cropimg, found_pixels)
            dist = find_distance(y)
            writer.writerow([p, dist])

main(OUTFILE)
