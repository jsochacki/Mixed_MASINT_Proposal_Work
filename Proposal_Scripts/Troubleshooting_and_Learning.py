#!python3

import cv2
import numpy as np
from matplotlib import pyplot as plt

import os

os.chdir('/root/base/development/MASINT_Proposal_Work/Proposal_Scripts')
file_path = '/root/base/development/MASINT_Proposal_Work'\
            '/Media_Files/Initial/Bottle/'
jpg_files = os.listdir(file_path)

img = cv2.imread(file_path+'/Untitled.jpg')
h, w = img.shape[:2]
# %%
img2 = img.copy()
img3 = img.copy()
img4 = img.copy()
img2 = cv2.rectangle(img2, (555, 415), (575, 432), (0, 0, 255), 2)
cv2.imshow("rectange", img2)

rsh = 100.0
rsd = (int(rsh), int(img.shape[0] * (rsh / img.shape[1])))
img4 = cv2.resize(img, rsd, interpolation = cv2.INTER_AREA)
cv2.imshow("original", img)
cv2.imshow("resized", img4)

# %%
(h, w) = img.shape[:2]
center = (w / 2, h / 2)
 
# rotate the image by 180 degrees
M = cv2.getRotationMatrix2D(center, 180, 1.0)
rotated = cv2.warpAffine(img, M, (w, h))
cv2.imshow("rotated", rotated)
alpha = 0.5
beta = 1 - alpha
gamma = 0.0
img5 = cv2.addWeighted(rotated, alpha, img, beta, gamma)
cv2.putText(img5, "Linear Blend of two images \n with zero gamma (DC offset)"
                     ": gamma={0}".format(gamma),
                     (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
cv2.imshow('linear blend', img5)
# %%
# All the 6 methods for comparison in a list
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 
            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF']#, 'cv2.TM_SQDIFF_NORMED']

img = img3.copy()
method = eval(methods[0])

# Apply template Matching
res = cv2.matchTemplate(img,img2,method)
cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, -1)
min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

# If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    top_left = min_loc
else:
    top_left = max_loc
bottom_right = (top_left[0] + w, top_left[1] + h)

cv2.rectangle(img,top_left, bottom_right, 255, 2)

plt.subplot(121),plt.imshow(res,cmap = 'gray')
plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(img,cmap = 'gray')
plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
plt.suptitle(meth)

plt.show()  
    
# %%
import cv2
import numpy as np
from matplotlib import pyplot as plt

img_rgb = cv2.imread('mario.png')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
template = cv2.imread('mario_coin.png',0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(img_gray,template,cv2.TM_CCOEFF_NORMED)
threshold = 0.8
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

cv2.imwrite('res.png',img_rgb)
