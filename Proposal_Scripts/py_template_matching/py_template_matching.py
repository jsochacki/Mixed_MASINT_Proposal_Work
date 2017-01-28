#!python3

import cv2
import numpy as np
from matplotlib import pyplot as plt

step = 'OFF'
image_name = '0027.jpg'
template_name = 'Bottle_Template.jpg'
image_name = '0020.jpg'
template_name = '0017.jpg'
img = cv2.imread(image_name, 1)
img_gray = cv2.imread(image_name, 0)
img2 = img.copy()
template = cv2.imread(template_name, 1)
template_gray = cv2.imread(template_name, 0)
template_scale = 3
if template_scale >= 3:
    StartLevel = 4
else:
    StartLeve = 0
if len(template.shape) == 3:
    template = cv2.resize(template,
                          (int(template.shape[-2:-4:-1][0]/template_scale),
                           int(template.shape[-2:-4:-1][1]/template_scale)),
                           interpolation = cv2.INTER_AREA)
    h, w = template.shape[:2]
else:
    template = cv2.resize(template,
                          (int(template.shape[::-1][0]/template_scale),
                           int(template.shape[::-1][1]/template_scale)),
                           interpolation = cv2.INTER_AREA)
    h, w = template.shape[:2]

template = cv2.Canny(template, 50, 200)


# All the 6 methods for comparison in a list
#methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR', 
#            'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF']#, 'cv2.TM_SQDIFF_NORMED']
# Best Methods Below
methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCORR'] #, 'cv2.TM_CCORR_NORMED']

for meth in methods:
    image = img2.copy()
    method = eval(meth)
    scale_values = [value/20 for value in range(20, 0, -1)]
    current_local_value = None
    for Test, scale in enumerate(scale_values):
        img = image.copy()
        rsd = (int(img.shape[1] * scale), int(img.shape[0] * scale))
        #print(scale, rsd, img.shape)
        img = cv2.resize(img, rsd, interpolation = cv2.INTER_AREA)
        if (img.shape[0] < h) | (img.shape[1] < w):
            break
        edge_detected_image = cv2.Canny(img, 50, 200)
        result = cv2.matchTemplate(edge_detected_image, template, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            local_loc = min_loc
            local_value = min_val
            if current_local_value is None or local_value < current_local_value[0]:
                current_local_value = (local_value, local_loc, scale)
        else:
            local_loc = max_loc
            local_value = max_val
            if Test > StartLevel and (current_local_value is None or \
                local_value > current_local_value[0]):
                current_local_value = (local_value, local_loc, scale)
        # for visualization
        if step == 'ON':
            clone = np.dstack([edge_detected_image, edge_detected_image, edge_detected_image])
            cv2.rectangle(clone,
                          local_loc,
                          (local_loc[0] + w, local_loc[1] + h),
                          (0, 0, 255),
                          2)
            cv2.imshow('clone', clone)
            cv2.waitKey(0)
        print(local_value, current_local_value, Test)
    (_, top_left, scale) = current_local_value
    bottom_right = (int((top_left[0] + w) / scale),
                    int((top_left[1] + h) / scale))
    top_left = (int(top_left[0] / scale), int(top_left[1] / scale))
## %%
#    # Apply template Matching
#    res = cv2.matchTemplate(img,template,method)
#    #res = cv2.matchTemplate(cv2.Canny(img, 50, 200),template,method)
#    # cv2.normalize(res, res, 0, 1, cv2.NORM_MINMAX, -1)
#    # SUPER IMPORTANT NOTE THAT THIS GIVES ITS LOC IN
#    # (X, Y) TUPLES AND NOT (Y, X) LIKE EVERYTHING ELSE
#    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
#    
#    # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
#    if method not in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
#        top_left = min_loc
#    else:
#        top_left = max_loc
#    bottom_right = (top_left[0] + w, top_left[1] + int(h/2))
    cv2.rectangle(image,top_left, bottom_right, 255, 2)
#    if len(image.shape) == 3:
#        cv2.rectangle(image,(0, 0), image.shape[-2:-4:-1], 255, 2)
#    else:
#        cv2.rectangle(image,(0, 0), image.shape[::-1], 255, 2)
    cv2.putText(image, '{0}'.format(top_left),
                     top_left, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
    cv2.putText(image, '{0}'.format(bottom_right),
                     bottom_right, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
    cv2.putText(image, '{0}'.format(meth),
                     (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
    cv2.imshow(meth, image)
# %%
cv2.destroyAllWindows()
    # %%
    plt.subplot(121),plt.imshow(res)
    plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    plt.subplot(122),plt.imshow(img)
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
