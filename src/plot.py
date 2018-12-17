import cv2
import numpy as np
def draw_rect(im, cords, color = None):
    """Draw the rectangle on the image
    Usage:
    >>>im = np.array(Image.open('./data/raw/img_000001.jpg'), dtype=np.uint8)
    >>>ano_reader = PascalVocReader('./data/raw/img_000001.xml')
    >>>boxes = np.array([[shape[1][0][0],shape[1][0][1], shape[1][1][0],shape[1][1][1]] for shape in ano_reader.getShapes()])
    >>>plt.figure(figsize=(17,14))
    >>>plt.imshow(draw_rect(im,boxes))

    Parameters
    ----------
    
    im : numpy.ndarray
        numpy image 
    
    cords: numpy.ndarray
        Numpy array containing bounding boxes of shape `N X 4` where N is the 
        number of bounding boxes and the bounding boxes are represented in the
        format `x1 y1 x2 y2`
        
    Returns
    -------
    
    numpy.ndarray
        numpy image with bounding boxes drawn on it
        
    """
    im = im.copy()
    cords = cords.reshape(-1,4)
    if not color:
        color = [255,255,255]
    for cord in cords:
        
        pt1, pt2 = (cord[0], cord[1]) , (cord[2], cord[3])
                
        pt1 = int(pt1[0]), int(pt1[1])
        pt2 = int(pt2[0]), int(pt2[1])
    
        im = cv2.rectangle(im.copy(), pt1, pt2, color, int(max(im.shape[:2])/400))
    return im