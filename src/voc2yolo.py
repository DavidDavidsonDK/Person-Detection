import numpy as np
import xml.etree.ElementTree as ET
import os

classes = ["aeroplane", "bicycle", "bird", "boat", "bottle", "bus", "car", "cat", "chair", "cow", 
           "diningtable", "dog", "horse", "motorbike", "person", "pottedplant", "sheep", "sofa", "train", "tvmonitor"]

def convert_voc_to_yolo(xml_anotation_file, yolo_writer, coco=False):
    in_file = open(xml_anotation_file)
    tree = ET.parse(in_file)
    for obj in tree.iter('object'):
        difficult = obj.find('difficult').text
        cls = obj.find('name').text
        if cls not in classes or int(difficult)==1:
            continue
        cls_id = classes.index(cls)
        xmlbox = obj.find('bndbox')
        b = (int(xmlbox.find('xmin').text), int(xmlbox.find('ymin').text), int(xmlbox.find('xmax').text), int(xmlbox.find('ymax').text))
        if coco:
            cls_id = 0
    
        yolo_writer.write(" " + ",".join([str(a) for a in b]) + ',' + str(cls_id))
        
def voc2yolo(data_set_path):
    
    yolo_writer = open('../data/yolo_anchors/citycams_1.txt', 'wt')
    for img_or_xml in os.listdir(path=data_set_path):
        if img_or_xml.endswith('.xml'):
            yolo_writer.write(data_set_path+img_or_xml.split('.')[0]+'.jpg')
            convert_voc_to_yolo(data_set_path+img_or_xml,yolo_writer)
            yolo_writer.write('\n')
    yolo_writer.close()

if __name__ == '__main__':
	voc2yolo('../data/raw/citycams_1/')
