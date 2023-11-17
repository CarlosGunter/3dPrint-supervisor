from skimage import *
from matplotlib import pyplot
import cv2
import numpy as np

model = cv2.imread('images/model_g.jpg')
kernel = np.ones((8,8), np.float32)/36

# model_dns = cv2.filter2D(model, -1, kernel)
model_dns = cv2.fastNlMeansDenoising(model, 15, 7, 21)
pyplot.figure()
pyplot.imshow(model_dns)
pyplot.axis('off')
pyplot.savefig('images/model_dns.jpg', format='jpg', bbox_inches='tight', pad_inches=0)
pyplot.close()