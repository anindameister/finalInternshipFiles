import requests
from pathlib import Path
import argparse
import subprocess
import numpy as np
import os
import io
# download2yolo2excel
import requests
from rdflib import Graph
import urllib.request

import glob
from PIL import Image
import numpy as np
import pandas as pd
import time
import math
import os
import shutil
from pandas import DataFrame, read_excel, merge
from pandas import DataFrame


readingTheTextFile = open("H:\\just files from internship\\yolov3-master\\class number class name QID modified.txt", "r")
allQIDs=[]
justWantObjectNames=[]
wikidataURLofALLqids=[]
for contentsLineByLine in readingTheTextFile:
#   print(contentsLineByLine)
  attemptingContentModification = contentsLineByLine.split('-')

  attemptingContentModification2= contentsLineByLine.split('.')
  # print(attemptingContentModification2)
  justWantObjectNamesss=attemptingContentModification2[1]
  justWantObjectNamesss = justWantObjectNamesss.split('-')
  justWantObjectNamess=justWantObjectNamesss[0]
  justWantObjectNames.append(justWantObjectNamess)
  justWantQIDs=attemptingContentModification[1]
  justWantQIDs=justWantQIDs.split('\n')
  QIDs=justWantQIDs[0]

  allQIDs.append(QIDs)
# print(justWantObjectNames)
# [s + mystring for s in mylist] , https://stackoverflow.com/questions/2050637/appending-the-same-string-to-a-list-of-strings-in-python
wikidataURL=['wikidata.org/wiki/'+s for s in allQIDs]
# print(wikidataURL)

excelQID=pd.DataFrame(data={"object name":justWantObjectNames,"all_QIDs":allQIDs,"wikidata_URL":wikidataURL})
excelQID.to_csv("H:\\just files from internship\\yolov3-master\\excels\\excelQID.csv",sep=',',index=False)

readingTheTextFile2 = open("H:\\just files from internship\\yolov3-master\\class number class name QID modified.txt", "r")
allQIDs2=[]
for contentsLineByLine2 in readingTheTextFile2:
#   print(contentsLineByLine)
  attemptingContentModification2 = contentsLineByLine2.split('-')
  justWantQIDs2=attemptingContentModification2[1]
  justWantQIDs2=justWantQIDs2.split('\n')
  QIDs2=justWantQIDs2[0]
  allQIDs2.append(QIDs2)


url_list = []

#?action=query&list=search&srsearch=haswbstatement:P180=Q7378&srnamespace=6&format=json


filename_list=[]
url_to_img = 'https://commons.wikimedia.org/w/thumb.php?f={image_name}&w=200'
path_dir = Path('test')
mpageid=[]
sList=[]
for individualQID in allQIDs2:
    print(individualQID)
    i = 10
    while i <= 3000:
        i = i + 10
        URL = "https://commons.wikimedia.org/w/api.php"
        PARAMS = {
            'action': 'query',
            'list': 'search',
            'srsearch': 'haswbstatement:P180=' + individualQID,
            'srlimit': '10',
            'srnamespace': '6',
            'sroffset': i,

            'format': 'json',
            # continue=-||
            'continue': '-||'
        }

        r = requests.get(url=URL, params=PARAMS)

        for image in r.json()['query']['search']:
            mid = image['pageid']
            img_name = ':'.join(image['title'].split(':')[1:])
            r = requests.get(url_to_img.format(image_name=img_name))
            print(url_to_img.format(image_name=img_name))
            print(r.ok)
            if r.ok:
                img = r.content
                path_file = path_dir.joinpath(f'M{str(mid)}.{img_name.split(".")[-1]}')
                path_file.write_bytes(img)

doingYolo1 = time.time()

os.chdir(r"H:\just files from internship\yolov3-master")
# subprocess.run('dir', shell=True)
# subprocess.run('python detect.py --cfg cfg\yolov3.cfg --weights weights\yolov3.pt --source test --save-txt', shell=True)
subprocess.run(
    'python detect.py --cfg cfg\yolov3.cfg --weights weights\yolov3.pt --source test --save-txt --conf-thres 0.8',
    shell=True)
doingYolo2 = time.time()

imageDimentionList = []
ImageFilenameList = []

images = glob.glob("output/*.*")
imagess = images.copy()
for i in imagess:
    if i.endswith(".txt") or i.endswith(".svg"):
        print(i)
        images.remove(i)
print("ok")
for image in images:
    with open(image, 'rb') as file:
        img = Image.open(file)
        imageSize = img.size
        imageDimentionList.append(imageSize)
        image = image[7:]
        ImageFilenameList.append(image)

lengthDimention = [item[1] for item in imageDimentionList]
breadthDimention = [item[0] for item in imageDimentionList]
wikiDimention = {'dimention': imageDimentionList, 'mpageid': ImageFilenameList,
                 'Y-Image Dimentions': lengthDimention, 'X-Image Dimentions': breadthDimention}

df = pd.DataFrame(wikiDimention, columns=['dimention', 'mpageid', 'Y-Image Dimentions', 'X-Image Dimentions'])

print(df)
df.to_csv('H:\\just files from internship\\yolov3-master\\excels\\output.csv', encoding='utf-8', index=False)
print(ImageFilenameList, imageDimentionList)

dir_path = 'H:\\just files from internship\\yolov3-master\\output'
os.chdir(dir_path)
src_files = os.listdir(dir_path)
for file_name in src_files:
    if file_name.endswith(".txt"):
        full_file_name = os.path.join(dir_path, file_name)
        if os.path.isfile(full_file_name):
            shutil.copy(full_file_name, 'H:\\just files from internship\\yolov3-master\\texts')

dir_path = 'H:\\just files from internship\\yolov3-master\\texts'  # Put the path to the texts directory here
os.chdir(dir_path)
file_name = []
for f in os.listdir():
    f_name, f_ext = os.path.splitext(f)

    file_name.append(f_name)

file_content = {
    'X1': [],
    'Y1': [],
    'X2': [],
    'Y2': [],
    'object name': [],
    'mpageid': []
}

for i in os.listdir():
    f_name, f_ext = os.path.splitext(i)
    file1 = open(i, "r+")
    txt = file1.readlines()

    for line in txt:
        l = line.split(' ')
        if l[-1] == '\n':
            l = l[:-1]
        file_content['X1'].append(l[0])
        file_content['Y1'].append(l[1])
        file_content['X2'].append(l[2])
        file_content['Y2'].append(l[3])
        file_content['object name'].append(l[4])
        a = np.array(file_content['X1'], dtype=np.float)
        b = np.array(file_content['X2'], dtype=np.float)
        c = np.array(file_content['Y1'], dtype=np.float)
        d = np.array(file_content['Y2'], dtype=np.float)
        file_content['X-centre'] = ((a + b) / 2)
        file_content['Y-centre'] = ((c + d) / 2)
        file_content['mpageid'].append(f_name)

df = DataFrame(data=file_content)
print(df)
df.to_csv('H:\\just files from internship\\yolov3-master\\excels\\imageNameBoundingBoxesObjectNameXYcenter.csv',
          index=False)

df4 = pd.read_csv(
    'H:\\just files from internship\\yolov3-master\\excels\\imageNameBoundingBoxesObjectNameXYcenter.csv')

df5 = pd.read_csv('H:\\just files from internship\\yolov3-master\\excels\\output.csv')

df6 = df4.merge(df5, on='mpageid', how='left')

df6.to_csv(
    'H:\\just files from internship\\yolov3-master\\excels\\imageNameBoundingBoxesObjectNameXYcenterImageDim.csv',
    encoding='utf-8', index=False)

dddf = pd.read_csv(
    'H:\just files from internship\yolov3-master\excels\imageNameBoundingBoxesObjectNameXYcenterImageDim.csv')

# automationUrl2downloadPhoto2yolo2ioRel&ooRelexcel

hasinthecenter = []


def center_object(image, object, x_dim, y_dim, x_centre, y_centre):
    if x_centre > 0.3 * x_dim and x_centre < 0.66 * x_dim and y_centre > 0.3 * y_dim and y_centre < 0.66 * y_dim:
        hasinthecenter.append(object)
    else:
        hasinthecenter.append('na')


for _, row in dddf.iterrows():
    center_object(row['mpageid'], row['object name'], row['X-Image Dimentions'], row['Y-Image Dimentions'],
                  row['X-centre'], row['Y-centre'])

hasintheleft = []


def center_object(image, object, x_dim, y_dim, x_centre, y_centre):
    if x_centre < 0.3 * x_dim:
        hasintheleft.append(object)
    else:
        hasintheleft.append('na')


for _, row in dddf.iterrows():
    center_object(row['mpageid'], row['object name'], row['X-Image Dimentions'], row['Y-Image Dimentions'],
                  row['X-centre'], row['Y-centre'])

hasinthetop = []


def center_object(image, object, x_dim, y_dim, x_centre, y_centre):
    if y_centre < 0.3 * y_dim:
        hasinthetop.append(object)
    else:
        hasinthetop.append('na')


for _, row in dddf.iterrows():
    center_object(row['mpageid'], row['object name'], row['X-Image Dimentions'], row['Y-Image Dimentions'],
                  row['X-centre'], row['Y-centre'])

hasintheright = []


def center_object(image, object, x_dim, y_dim, x_centre, y_centre):
    if x_centre > 0.66 * x_dim:
        hasintheright.append(object)
    else:
        hasintheright.append('na')


for _, row in dddf.iterrows():
    center_object(row['mpageid'], row['object name'], row['X-Image Dimentions'], row['Y-Image Dimentions'],
                  row['X-centre'], row['Y-centre'])

hasinthebottom = []


def center_object(image, object, x_dim, y_dim, x_centre, y_centre):
    if y_centre > 0.66 * y_dim:
        hasinthebottom.append(object)
    else:
        hasinthebottom.append('na')


for _, row in dddf.iterrows():
    center_object(row['mpageid'], row['object name'], row['X-Image Dimentions'], row['Y-Image Dimentions'],
                  row['X-centre'], row['Y-centre'])

ddf = dddf.assign(has_on_the_left=hasintheleft, has_on_the_right=hasintheright, has_on_the_top=hasinthetop,
                  has_on_the_bottom=hasinthebottom, has_in_the_center=hasinthecenter)

ddf.columns = [c.replace('_', ' ') for c in ddf.columns]
print(ddf)
ddf.to_csv("H:\\just files from internship\\yolov3-master\\excels\\imageHasOnLeftRightCenterTopBotto.csv", sep=',',
           index=False)

df7 = pd.read_csv('H:\\just files from internship\\yolov3-master\\excels\\imageHasOnLeftRightCenterTopBotto.csv')
df8 = pd.read_csv('H:\\just files from internship\\yolov3-master\\excels\\excelQID.csv')

df9 = df7.merge(df8, on='object name', how='left')
df9.to_csv('H:\\just files from internship\\yolov3-master\\excels\\imageHasOnLeftRightCenterTopBott.csv',
           encoding='utf-8', index=False)

df10 = pd.read_csv('H:\\just files from internship\\yolov3-master\\excels\\imageHasOnLeftRightCenterTopBott.csv')
df11 = pd.read_csv('H:\\just files from internship\\yolov3-master\\excels\\hasontheleft.csv')

df12 = df10.merge(df11, on='has on the left', how='left')
df12.to_csv('H:\\just files from internship\\yolov3-master\\excels\\hasontheleftimageHasOnLeftRightCenterTopBott.csv',
            encoding='utf-8', index=False)

df13 = pd.read_csv(
    'H:\\just files from internship\\yolov3-master\\excels\\hasontheleftimageHasOnLeftRightCenterTopBott.csv')
df14 = pd.read_csv('H:\\just files from internship\\yolov3-master\\excels\\hasontheright.csv')

df15 = df13.merge(df14, on='has on the right', how='left')
df15.to_csv(
    'H:\\just files from internship\\yolov3-master\\excels\\hasontherightimageHasOnLeftRightCenterTopBottom.csv',
    encoding='utf-8', index=False)

df16 = pd.read_csv(
    'H:\\just files from internship\\yolov3-master\\excels\\hasontherightimageHasOnLeftRightCenterTopBottom.csv')
df17 = pd.read_csv('H:\\just files from internship\\yolov3-master\\excels\\hasonthetop.csv')

df18 = df16.merge(df17, on='has on the top', how='left')
df18.to_csv('H:\\just files from internship\\yolov3-master\\excels\\hasonthetopimageHasOnLeftRightCenterTopBottom.csv',
            encoding='utf-8', index=False)

df19 = pd.read_csv(
    'H:\\just files from internship\\yolov3-master\\excels\\hasonthetopimageHasOnLeftRightCenterTopBottom.csv')
df20 = pd.read_csv('H:\\just files from internship\\yolov3-master\\excels\\hasonthebottom.csv')

df21 = df19.merge(df20, on='has on the bottom', how='left')
df21.to_csv(
    'H:\\just files from internship\\yolov3-master\\excels\\hasonthebottomimageHasOnLeftRightCenterTopBottom.csv',
    encoding='utf-8', index=False)

df22 = pd.read_csv(
    'H:\\just files from internship\\yolov3-master\\excels\\hasonthebottomimageHasOnLeftRightCenterTopBottom.csv')
df23 = pd.read_csv('H:\\just files from internship\\yolov3-master\\excels\\hasinthecenter.csv')

df24 = df22.merge(df23, on='has in the center', how='left')
df24.to_csv(
    'H:\\just files from internship\\yolov3-master\\excels\\hasinthecenterimageHasOnLeftRightCenterTopBottom.csv',
    encoding='utf-8', index=False)

df25 = pd.read_csv(
    'H:\\just files from internship\\yolov3-master\\excels\\hasinthecenterimageHasOnLeftRightCenterTopBottom.csv')

df26 = df25.drop(
    ['X1', 'Y1', 'X2', 'Y2', 'X-centre', 'Y-centre', 'dimention', 'Y-Image Dimentions', 'X-Image Dimentions',
     'all_QIDs_x', 'all_QIDs_y', 'all_QIDs_x.1', 'all_QIDs_y.1', 'all_QIDs_x.1.1', 'all_QIDs_y.1.1', 'wikidata_URL',
     'has on the left', 'has on the right', 'has on the top', 'has on the bottom', 'has in the center'], axis=1)
# object name	mpageid	URLs	thumbnails	mpageid	wikidata_URL	URI has on the left	URI has on the right	URI has on the top	URI has on the bottom	URI has on the center
df27 = df26.rename(columns={'URI has on the left': 'has on the left',
                            'URI has on the right': 'has on the right',
                            'URI has on the top': 'has on the top',
                            'URI has on the bottom': 'has on the bottom',
                            'URI has on the center': 'has in the center'},
                   inplace=True)
df26['mpageid'] = df26['mpageid'].str.split(".", n=1, expand=True)
df26['mpageid'] = 'http://commons.wikimedia.org/wiki/Special:EntityData/' + df26['mpageid'].astype(str)

# df.drop(columns =['C', 'D'])
# dimention	Y-Image Dimentions	X-Image Dimentions
# all_QIDs_x	wikidata_URL	all_QIDs_y	URI has on the left	all_QIDs_x.1	URI has on the right	all_QIDs_y.1	URI has on the top	all_QIDs_x	URI has on the bottom	all_QIDs_y	URI has on the center
df26.to_csv('H:\\just files from internship\\yolov3-master\\excels\\imageHasOnLeftRightCenterTopBottom.csv',
            encoding='utf-8', index=False)
df26.to_csv(
    'H:\\just files from internship\\data2rdf-master\\src\\main\\resources\\imageHasOnLeftRightCenterTopBottom.csv',
    encoding='utf-8', index=False)

dir_path = 'H:\\just files from internship\\data2rdf-master'
# H:\just files from internship\data2rdf-master
os.chdir(dir_path)
subprocess.run('mvn clean install', shell=True)

dir_path = 'H:\\just files from internship\\data2rdf-master\\target'
# H:\just files from internship\data2rdf-master
os.chdir(dir_path)
subprocess.run(
    'java -jar data2rdf-1.0-SNAPSHOT.jar -f eu.qanswer.data2rdf.mappings.imageannotation.ObjectPosition -o outputfile.nt --file H:\just files from internship\yolov3-master\excels\imageHasOnLeftRightCenterTopBottom.csv ',
    shell=True)
dir_path = 'H:\\just files from internship\\data2rdf-master\\target'
# H:\just files from internship\data2rdf-master
os.chdir(dir_path)

f = open("outputfile.nt", "rb")
f1 = open('ObjectPositionOutput.nt', 'ab')
for x in f.readlines():
    f1.write(x)
f.close()
f1.close()

f2 = open("outputfile.nt_ontology", "rb")
f3 = open('ObjectPositionOutput.nt', 'ab')
for y in f2.readlines():
    f3.write(y)
f2.close()
f3.close()

t2 = time.time()

print("completed the program in", t2 - t1, "seconds")
print("completed the program in", ((t2 - t1) / 60), "minutes")
