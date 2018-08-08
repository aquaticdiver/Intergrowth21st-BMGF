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
from PIL import Image
import numpy as np
import csv
import pandas as pd

PATH = "path/to/file/"
OUTFILE = "measures.csv"

def find_images(root, suffix='bmp'):
    images = []
    for path, dirs, files in os.walk(root):
        for file in files:
            if file.lower().endswith("bmp"):
                images.append("{0}\{1}".format(path, file))
    return images

def imcrop(img, bbox):
    x1,y1,x2,y2 = bbox
    if x1 < 0 or y1 < 0 or x2 > img.shape[1] or y2 > img.shape[0]:
        img, x1, x2, y1, y2 = pad_img_to_fit_bbox(img, x1, x2, y1, y2)
    return img[y1:y2, x1:x2, :]

def preprocess(path):
    img = cv2.imread(path)
    bbox = (100, 100, 200, 400)
    cropped_image = imcrop(img, bbox)
    return cropped_image


def find_contours(cropped_image):
    lower = np.array([100,100, 100])
    upper = np.array([130,130,130])
    shapeMask = cv2.inRange(cropped_image, lower, upper) 
    cnt, contours, hierarchy = cv2.findContours(shapeMask.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    lst = [0,1,2,3,4]
    result = [cv2.minAreaRect(contours[x]) for x in lst]
    box = [cv2.boxPoints(y) for y in result]
    box = np.array(box)
    return box

def column(matrix, i)
    return [row[:,i] for row in matrix]

def find_distances(box, lst, resolution=1.0):
    lst = [0,1,2,3,4]
    heights = column(box, 1)
    avg = [np.mean(heights[i]) for i in lst]
    distances = [abs(y-x)/resolution for x, y in zip(avg, avg[1:])]
    return np.mean(distances)

def main(outfile):
    lst = [0,1,2,4]
    with open(outfile, 'w') as fp:
        writer = csv.writer(fp)
        for p in find_images(PATH):
            cropped_image = preprocess(p)
            box_array = find_contours(cropped_image)
            distance = find_distances(box_array, lst)
            writer.writerow([p, distance])
