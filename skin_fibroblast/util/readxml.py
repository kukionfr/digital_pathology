import xml.etree.ElementTree as ET
from time import time
import numpy as np
from scipy import io
import os
import pandas as pd

# xml_path = absolute filepath of xml
# mdict = 2D coordinates of annotation by class and object
def readxml(xml_path):
    start = time()
    print(os.path.basename(xml_path))
    tree = ET.parse(xml_path)
    root = tree.getroot()
    x = np.array([])
    y = np.array([])
    obj = np.array([])
    classID = np.array([])
    classname = np.array([])

    classlut = []
    for Annotation in root.iter('Annotation'):
        for Attrib in Annotation.iter('Attribute'):
            classlut.append(Attrib.attrib.get('Name'))
    classlut = sorted(classlut)

    LUT = ['corneum', 'basale', 'hairroot', 'hairfollicle', 'smoothmuscle', 'oil', 'sweat', 'nerve', 'bloodvessel',
           'collagen', 'fat', 'white', 'noisebio', 'noisephy']
    LUT = sorted(LUT)


    if not classlut==LUT:
        print(classlut)
        print('check name')
        return classlut,None


    for idx, Annotation in enumerate(root.iter('Annotation')):
        for Region in Annotation.iter('Region'):
            xx = np.array([float(Vertex.get('X')) for Vertex in Region.iter('Vertex')])
            yy = np.array([float(Vertex.get('Y')) for Vertex in Region.iter('Vertex')])
            objj = np.array([float(Region.get('Id'))] * len(xx))
            classIDD = np.array([float(Annotation.get('Id'))] * len(xx))
            classnamee = np.array([classlut[idx]] * len(xx))

            x = np.concatenate((x, xx), axis=None)
            y = np.concatenate((y, yy), axis=None)
            obj = np.concatenate((obj, objj), axis=None)
            classID = np.concatenate((classID, classIDD), axis=None)
            classname = np.concatenate((classname, classnamee), axis=None)

    # print('number of coordinates in annotation : ',len(x))
    x = x.astype(int)
    y = y.astype(int)
    obj = obj.astype(int)
    classID = classID.astype(int)
    mdict = {'x': x, 'y': y, 'objID': obj, 'classID': classID, 'className': classname}
    print('readxml took {:.2f} sec'.format(time() - start))
    io.savemat(xml_path.replace('xml','mat'),mdict=mdict)
    return classlut,pd.DataFrame(mdict)

# src = r'\\kukissd\Kyu_Sync\Research\Active\Aging_organized\svs\svs_back'
# [readxml(os.path.join(src,xml_path)) for xml_path in os.listdir(src) if xml_path.endswith('xml') ]
# [readxml(os.path.join(src,xml_path)) for xml_path in os.listdir(src) if xml_path.endswith('xml') and xml_path.startswith('wm')]