import xml.etree.ElementTree as ET
from time import time
import numpy as np
from scipy import io
import os
import pandas as pd

# xml_path = absolute filepath of xml
# mdict = 2D coordinates of annotation by class and object
def readxml_b(xml_path):
    # print('reading xml:',os.path.basename(xml_path))
    tree = ET.parse(xml_path)
    root = tree.getroot()

    names = []
    coords = []

    classlut = []
    for Annotation in root.iter('Annotation'):
        for Attrib in Annotation.iter('Attribute'):
            classlut.append(Attrib.attrib.get('Name'))
    classluts = sorted(classlut)

    LUT = ['corneum', 'basale', 'hairroot', 'hairfollicle', 'smoothmuscle', 'oil', 'sweat', 'nerve', 'bloodvessel',
           'collagen', 'fat', 'white', 'noisebio', 'noisephy']
    LUTs = sorted(LUT)

    if not classluts==LUTs:
        raise TypeError('check name:',os.path.basename(xml_path),'classes in file:',classlut)

    for Annotation in root.iter('Annotation'):
        for Attrib in Annotation.iter('Attribute'):
            name = Attrib.attrib.get('Name')
        for Region in Annotation.iter('Region'):
            coord = np.array([[int(float(Vertex.get('X'))),int(float(Vertex.get('Y')))] for Vertex in Region.iter('Vertex')])
            coords.append(coord)
            names.append(name)

    coords = np.array(coords)
    names = np.array(names)

    coords = coords[names != 'basale']
    names = names[names != 'basale']

    coords = coords[names != 'corneum']
    names = names[names != 'corneum']

    coords = coords[names != 'noisebio']
    names = names[names != 'noisebio']

    coords = coords[names != 'noisephy']
    names = names[names != 'noisephy']

    return coords.tolist(), names.tolist()
