import numpy as np
import cv2

class BaseAugmentation(object):
    """
    
    Parameters
    ----------
          
    Returns
    -------
    numpy.ndaaray
        Augmented image in the numpy format of shape `HxWxC`
    
    numpy.ndarray
        Tranformed bounding box co-ordinates of the format `n x 4` where n is 
        number of bounding boxes and 4 represents `xmin,ymin,xmax,ymax` of the box
        
    """
    #Override Me,Ara
    def __init__(self):
        pass

    def __call__(self, img, bboxes):
        '''
        Parameters
        ----------
        img - numpy.ndaaray
        bboxes - numpy array of bounding boxes 
        '''
        return img, bboxes