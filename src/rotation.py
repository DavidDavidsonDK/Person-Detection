import numpy as np
import cv2
from augmentation_api import BaseAugmentation
from utils import rotate_im,get_corners,rotate_box,get_enclosing_box,clip_box
import random
class Rotation(BaseAugmentation):

	def __init__(self, angle = 10):
		self.angle = angle
		
		if type(self.angle) == tuple:
			assert len(self.angle) == 2, "Invalid range"   
		else:
			self.angle = (-self.angle, self.angle)

	def __call__(self, img, bboxes):


		angle = random.uniform(*self.angle)

		w,h = img.shape[1], img.shape[0]
		cx, cy = w//2, h//2

		img = rotate_im(img, angle)
		corners = get_corners(bboxes)
		corners = np.hstack((corners, bboxes[:,4:]))
		corners[:,:8] = rotate_box(corners[:,:8], angle, cx, cy, h, w)
		new_bbox = get_enclosing_box(corners).astype(np.float64)


		scale_factor_x = img.shape[1] / w

		scale_factor_y = img.shape[0] / h

		img = cv2.resize(img, (w,h))
		new_bbox[:,:4] /= np.array([scale_factor_x, scale_factor_y, scale_factor_x, scale_factor_y] )

		bboxes  = new_bbox

		bboxes = clip_box(bboxes, [0,0,w, h], 0.25)

		return img, bboxes

