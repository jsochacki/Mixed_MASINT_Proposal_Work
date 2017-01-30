#!/root/base/anaconda4p2/bin/python3
# %%
import cv2
import os
import numpy as np
from matplotlib import pyplot as plt

# %%
os.chdir('/root/base/development/MASINT_Proposal_Work/Media_Files/Initial/Video/')
# %%
%%bash
cp /mnt/hgfs/BHD/L64/Source_Files/Video/* ./
# %%
input_video_file_name = 'Final_In'
temporary_file_extension = '_Temporary_File.avi'
output_video_file_name = 'Final_Out'
script_name = 'Template_Tracking_2.py'
# %%
%%bash -s $input_video_file_name $temporary_file_extension
#echo ${1::-4}
ffmpeg -i ./$1.mp4 -c:v mjpeg -q:v 3 -an ./$1$2
# Take video recorded in windows in mp4 format and make it a mjpeg format for
# OpenCV processing
# %%
def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])
# %%
    
step = 'OFF'
template_name = 'cup.jpg'
template = cv2.imread(template_name, 1)
template_gray = cv2.imread(template_name, 0)
template_scale = 1
if template_scale >= 3:
    StartLevel = 4
else:
    StartLevel = 0
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

methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCORR'] #, 'cv2.TM_CCORR_NORMED']
# Select a method
meth = methods[0]
# %%

os.chdir('/root/base/development/MASINT_Proposal_Work/Media_Files/Initial/Video')

camera = cv2.VideoCapture('./{0}{1}'.format(input_video_file_name,temporary_file_extension))
fourcctext = decode_fourcc(camera.get(cv2.CAP_PROP_FOURCC))
fourccCode = cv2.VideoWriter_fourcc(*fourcctext)
out = cv2.VideoWriter(
                      './{0}{1}'.format(output_video_file_name,
                                        temporary_file_extension),
                      fourccCode,
                      30.0,
                      (640,480),
                      isColor=True)
print(out.isOpened())
# %%

while(camera.isOpened()): # and success):
    ret, inframe = camera.read()
    if ret==True:
        # inframe = cv2.flip(inframe,0)
        image = inframe.copy()
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

        cv2.rectangle(image,top_left, bottom_right, 255, 2)

        cv2.putText(image, '{0}'.format(top_left),
                         top_left, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
        cv2.putText(image, '{0}'.format(bottom_right),
                         bottom_right, cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
        cv2.putText(image, '{0}'.format(meth),
                         (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
        cv2.imshow(meth, image)
        out.write(image)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# %%
camera.release()
out.release()
del camera
del out
cv2.destroyAllWindows()

# %%
%%bash -s $output_video_file_name $temporary_file_extension
ffmpeg -i ./$1$2 -r 25 -pix_fmt yuv420p -strict -2 -acodec aac -b:a 128k -vcodec libx264 -crf 21 -rc-lookahead 250 ./$1.mp4
# %%
%%bash
cp * /mnt/hgfs/BHD/L64/Source_Files/Video/

# %%
os.chdir('/root/base/development/MASINT_Proposal_Work/Proposal_Scripts')
# %%
%%bash -s $script_name
cp ./$1 /mnt/hgfs/BHD/L64/Source_Files/Video/
# Convert to mp4 for viewing on other computer like windows