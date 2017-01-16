#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# version 11.01.2016

import os
import re
import pandas as pd
import subprocess
from argparse import ArgumentParser

#IrradianceSensitivitiesGolden csv file
goldenValuesPath = "D:\Code_Python\write_irradianceSensitiveGolden\\PI040378AC6K002004_IrradianceSentisitvesGolden.csv"


#imageDirectory = "D:\\Project_data\\Ecublens\\2016.07.20\\sequoia_eMotion\\img\\flight_tagged_klaus"
imageDirectory = "D:\\Project_data\\Rolex\\2017.01.06\\img\\6K002004"

#tag_characterisation.tagFilesInDir(goldenValuesPath,imageDirectory)

def tagCharacterisation(imagePath, model):

    modelstring = ",".join(format(x, '.3f') for x in model)
    cmd = ['exiv2',
           '-Mreg Camera http://pix4d.com/camera/1.0',
           '-Mdel Xmp.Camera.IrradianceSensitivitiesGolden',
           '-Mset Xmp.Camera.IrradianceSensitivitiesGolden ' + modelstring,
           imagePath]
    subprocess.call(cmd)

def paramConvert(paramdata, band):
    values = paramdata[paramdata['bandName'] == band]
    param_num = values[['No-IR', 'IR']].convert_objects(convert_numeric=True).values[0]
#    param_num = paramdata.ix[band_index+1,1:2].convert_objects(convert_numeric=True)
    
    return param_num

def tagFilesInDir(goldenValuesPath, imageDirectory):
    paramdata = pd.read_csv(goldenValuesPath)
    
    #convert the first colum into a list ['GRE', 'NIR', 'RED', 'REG']
#    band_name = paramdata.ix[1:(len(paramdata)-1),0].tolist()
    
    # convert the list to dictionary below with list elements as index
#    band_indices = {'GRE': 0, 'RED': 1, 'REG': 2, 'NIR': 3}
#    band_indices = {item:index for index,item in enumerate(band_name)}   
    band_regex = re.compile('.*_([A-Z]{3})\.TIF')

    for (dirpath, dirnames, filenames) in os.walk(imageDirectory):
        for f in filenames:
            imagepath = os.path.join(dirpath, f)
            band_match = band_regex.match(f)
            if band_match and os.path.isfile(imagepath):
                band = band_match.group(1)
#                band_index = band_indices[band]
                print('Tagging {} (band {})'.format(imagepath, band))
                tagCharacterisation(imagepath, paramConvert(paramdata, band))

if __name__ == "__main__":
    parser = ArgumentParser(
        description='Tag Sequoia characterisation into existing images'
    )
    parser.add_argument(
        'datafile',
        help='radiometric_correction.csv input file'
    )
    parser.add_argument(
        'imagedir',
        help='directory containing the images'
    )
    args = parser.parse_args()
    tagFilesInDir(args.datafile, args.imagedir)
