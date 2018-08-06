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


import dicom
import os
import numpy as np
import re
print("RUNNING")
EXCLUDED_KEYS = ["AccessionNumber",'PixelData','SamplesPerPixel', 'BitsAllocated','BitsStored',
              'Columns','HighBit','ImageType','LossyImageCompression','Manufacturer', 'ManufacturerModelName',
              'PatientName','PatientOrientation','PatientSex','ReferencedPerformedProcedureStepSequence',
              'PixelRepresentation','PlanarConfiguration', 'RefdPerformedProcedureStepSequence','ReferencedPerformedProcedureStepSequence',
              'ReferringPhysicianName','Rows','SoftwareVersions','StationName','WindowCenter','WindowWidth','PhotometricInterpretation',]

path_file = #path/to/file

''' Used to add the .dcm extension to files without the extension and end in a number '''

#def DCMcreater():
#    for dirName, subdirList, fileList in os.walk(path_file):
#        for filename in fileList:
#            if re.match(r'\w*\d$', filename): # check whether the filename ends in a number
#                lstFilesDCM.append(os.path.join(dirName, filename))
#                full_path = os.path.join(dirName, filename)
#                os.rename(full_path, full_path + '.dcm')
             
''' grabs a list of all files if they end in .dcm '''

def getlstFilesDCM():
    lstFilesDCM = [os.path.join(dirName, x) for dirName, subDirList, files in os.walk(path_file)
                   for x in files if x.endswith('.dcm')]
    return lstFilesDCM

''' grabs patientID's and other values to be used in creation of unique names for files '''

def get_values_and_patient_id(ds, header_keys):
    valuelst = []
    for key in header_keys:
        try:
            dataElement = ds.data_element(key)
            if dataElement is not None:
                if "\n" in str(dataElement.value):
                    val = str(dataElement.value).replace("\n", "||")
                else:
                    val = dataElement.value
                valuelst.append(val)
                # print("got something")
            else:
                valuelst.append(np.NaN)
        except KeyError:
            valuelst.append("None")
    return valuelst, ds.data_element("PatientID").value

''' grabs important path information to be used in creation of unique names for files '''

def pathInfo(path):
    chunks = path.split('\\')
    prefix = chunks[2]
    date = chunks[5]
    imgnum = chunks[7]
    return prefix,date,imgnum

''' creates manifest with new filenames, path, and metadata values except those in EXCLDUED_KEYS '''

def write_file(lstFilesDCM, prefixes, dates, imgnums):
    with open(r"C:/Users/danielti/Desktop/image_01.txt", mode='w') as f:
        header_keys = [k for k in dicom.read_file(lstFilesDCM[0]).dir() if k not in EXCLUDED_KEYS]
        f.write("filename,file_string," + ",".join(map(str, header_keys)) + "\n")
        for file, prefix, date, imgnum in zip(lstFilesDCM, prefixes, dates, imgnums):
            open_file = dicom.read_file(file)
            value_list, patient_id = get_values_and_patient_id(open_file, header_keys)
            file_string = f"{patient_id}_{prefix}_{date}_{imgnum}"
            f.write(f"{file},{file_string}," + ",".join(map(str, value_list)) + "\n")

            
lstFilesDCM = getlstFilesDCM()
pathInfos = zip(*list(map(pathInfo,lstFilesDCM)))
prefixes,dates,imgnums = zip(*list(map(pathInfo,lstFilesDCM)))
write_file(lstFilesDCM, prefixes, dates, imgnums)
