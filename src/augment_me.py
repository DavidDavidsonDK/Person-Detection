import numpy as np
import cv2
from ano_parser import PascalVocWriter,PascalVocReader
from plot import draw_rect
from PIL import Image
import matplotlib.pyplot as plt
import math
from tqdm import  tqdm
from rotation import Rotation
from random_translation import Translate
from random_scale import Scale
from horizontal_flip import HorizontalFlip
import os


class Augmentation(object):
    def __init__(self,rotation=True,translate=True,scale=True,horizontal_flip=True,**kwargs):
        self.augmentators = {}
        if rotation:
            ag = kwargs['ag'] if 'ag' in kwargs else 30
            self.rotation = Rotation(ag)
            self.augmentators['rotation'] = self.rotation
        if translate:
            tr = kwargs['tr'] if 'tr' in kwargs else 0.2
            self.translate = Translate(tr)
            self.augmentators['translate'] = self.translate

        if scale:
            sc_lower = kwargs['sc_lower'] if 'sc_lower' in kwargs else 0.2
            sc_upper = kwargs['sc_upper'] if 'sc_upper' in kwargs else 0.2

            self.scale = Scale((sc_lower,sc_upper))
            self.augmentators['scale'] = self.scale

        if horizontal_flip:
            self.horizontal_flip = HorizontalFlip()
            self.augmentators['horizontal_flip'] = self.horizontal_flip
     
    def __augment(self,im_path,im_name,ano_reader,dest_path):
        
        im = np.array(Image.open(im_path+im_name+'.jpg'), dtype=np.uint8)
        boxes = np.array([[shape[1][0][0],shape[1][0][1], shape[1][1][0],shape[1][1][1]] for shape in ano_reader.getShapes()])
        d_flags = [int(shape[4]) for shape in ano_reader.getShapes()]
        
        i = 0
        for key,transformer in self.augmentators.items():
            name_like = dest_path + im_name + '_'+key
            ano_writer = PascalVocWriter('augmented', im_name + '_'+key+'.jpg', im.shape,localImgPath=name_like+'.jpg')

            a_im,a_boxes = transformer(im,boxes.astype(np.float64)) 
            for box in a_boxes:
                ano_writer.addBndBox(math.ceil(box[0]),math.ceil(box[1]),math.ceil(box[2]),math.ceil(box[3]),'person',d_flags[i]) #the last 0 means dificult
                i+=1
            ano_writer.save(name_like+'.xml')
            cv2.imwrite(name_like+'.jpg',a_im)
            i = 0
        
    def augment(self, file_path='../data/raw/citycams_1/', dest_path='../data/augmented/'):
        for img_or_xml in tqdm(os.listdir(file_path)):
            if img_or_xml.endswith('.jpg'): 
                main_part_of_name = img_or_xml.split('.')[0]
                ano_reader = PascalVocReader(file_path+main_part_of_name+'.xml')
                self.__augment(file_path,main_part_of_name,ano_reader,dest_path)
if __name__ == '__main__':
	print('Augmantation start...')
	aug = Augmentation(rotation=True, translate=True, scale=True, horizontal_flip=True,ag = 20,tr=0.2,sc_lower=0.2,sc_upper=0.6)
	aug.augment()
	print('Augmantation finish')
	                	