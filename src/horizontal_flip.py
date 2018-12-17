import numpy as np
import cv2
from augmentation_api import BaseAugmentation

class HorizontalFlip(BaseAugmentation):
    """horizontally flips the Image with the probability *p*
    Parameters
    ----------
    
    Returns
    -------
    
    numpy.ndaaray
        Flipped image in the numpy format of shape `HxWxC`
    
    numpy.ndarray
        Tranformed bounding box co-ordinates of the format `n x 4` where n is 
        number of bounding boxes and 4 represents `xmin,ymin,xmax,ymax` of the box
    """
    def __call__(self, img, bboxes):
        img_center = np.array(img.shape[:2])[::-1]/2
        img_center = np.hstack((img_center, img_center))
        img =  img[:,::-1,:]
        
        bboxes[:,[0,2]] += 2*(img_center[[0,2]] - bboxes[:,[0,2]])
        
        box_w = abs(bboxes[:,0] - bboxes[:,2])
         
        bboxes[:,0] -= box_w
        bboxes[:,2] += box_w
        
        return img, bboxes