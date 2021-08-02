import xml.etree.ElementTree as ET
from time import time
import numpy as np
from scipy import io
import os
import pandas as pd

# xml_path = absolute filepath of xml
# mdict = 2D coordinates of annotation by class and object

def xml2feather(xml_path,LUT=None):
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
    classluts = sorted(classlut)

    if LUT:
        LUTs = sorted(LUT)

        if not classluts==LUTs:
            print(classluts)
            print('check name')
            return

    dfs = []
    for idx, Annotation in enumerate(root.iter('Annotation')):
        for Region in Annotation.iter('Region'):
            x = np.array([float(Vertex.get('X')) for Vertex in Region.iter('Vertex')]).astype('int')
            y = np.array([float(Vertex.get('Y')) for Vertex in Region.iter('Vertex')]).astype('int')
            objid = np.array([int(Region.get('Id'))])
            classname = np.array([classlut[idx]])
            df = pd.DataFrame({'classname': classname,
                               'objid': objid,
                               'x': [x],
                               'y': [y], })
            dfs.append(df)
    dff = pd.concat(dfs).reset_index(drop=True)

    mdict = {'x': x, 'y': y, 'objID': obj, 'classID': classID, 'className': classname}
    print('readxml took {:.2f} sec'.format(time() - start))
    io.savemat(xml_path.replace('xml', 'mat'), mdict=mdict)
    return dff
src = r'\\kukissd\Kyu_Sync\Research\Active\Aging_organized\svs\roi_annotation'
[xml2feather(os.path.join(src,xmlpth)) for xmlpth in os.listdir(src) if xmlpth.endswith('xml')]