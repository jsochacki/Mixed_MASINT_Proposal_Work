#!/root/base/anaconda4p2/bin/python3

import cv2
import os

# Camera 0 is the integrated web cam on Kali
camera_port = 0
 
#Number of frames to throw away while the camera adjusts to light levels
ramp_frames = 30
 
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)
# %%
#while(True):
#    # Capture frame-by-frame
#    ret, frame = camera.read()
#
#    # Our operations on the frame come here
#    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
#
#    # Display the resulting frame
#    cv2.imshow('frame',gray)
#    if cv2.waitKey(1) & 0xFF == ord('q'):
#        break
#
## When everything done, release the capture
#cap.release()
#cv2.destroyAllWindows()
# %%
camera = cv2.VideoCapture(0)
# Define the codec and create VideoWriter object
fourcc = cv2.VideoWriter_fourcc(*'XVID')
#fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
#fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('/mnt/hgfs/BHD/L64/Video/'+'output.avi',fourcc, 10.0, (640,480), isColor=True)
#out = cv2.VideoWriter()
#success = out.open('./output.avi',fourcc, 5.0, (64,48))
#success = out.open('./output.mp4',fourcc, 10.0, (640,480))
#success = out.open('/mnt/hgfs/BHD/L64/Video/'+'output.mp4',fourcc, 10.0, (640,480), isColor=True)
while(camera.isOpened()): # and success):
    ret, frame = camera.read()
    if ret==True:
        #frame = cv2.flip(frame,0)
        # write the flipped frame
        out.write(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
# %%
# Release everything if job is finished
camera.release()
out.release()
cv2.destroyAllWindows()
# %%
#!/root/base/anaconda4p2/bin/python3

import cv2
import os

#os.chdir('MASINT_Proposal_Work/Media_Files/Initial/Video/')

#camera = cv2.VideoCapture('./0016.mp4')
camera = cv2.VideoCapture(0)
camera.get(cv2.CAP_PROP_GUID)
camera.get(cv2.CAP_PROP_CONVERT_RGB)
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
camera.set(cv2.CAP_PROP_FPS, 30)
# Release everything if job is finished
def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])

fourcctext = decode_fourcc(camera.get(cv2.CAP_PROP_FOURCC))
fourccfloat = cv2.VideoWriter_fourcc(*fourcctext)
out = cv2.VideoWriter('./output.avi',fourccfloat, 10.0, (640,480), isColor=True)
#fourccfloat = cv2.VideoWriter_fourcc(*'x264')
#out = cv2.VideoWriter('./output.mp4',fourccfloat, 30.0, (640,480), isColor=True)
print(out.isOpened())
while(camera.isOpened()): # and success):
    ret, inframe = camera.read()
    if ret==True:
        #frame = cv2.flip(frame,0)
        # write the flipped frame
        out.write(inframe)
        cv2.imshow('frame',inframe)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
camera.release()
out.release()
del out
del camera
cv2.destroyAllWindows()
# %%
%%bash
ffmpeg -i ./output.avi -r 25 -pix_fmt yuv420p -strict -2 -acodec aac -b:a 128k -vcodec libx264 -crf 21 -rc-lookahead 250 ./output.mp4
# Convert to mp4 for viewing on other computer like windows
# %%
%%bash
ffmpeg -i ./0016.mp4 -c:v mjpeg -q:v 3 -an ./output2.avi
# Take video recorded in windows in mp4 format and make it a mjpeg format for
# OpenCV processing
# %%
#!/root/base/anaconda4p2/bin/python3

import cv2
import os

#os.chdir('MASINT_Proposal_Work/Media_Files/Initial/Video/')

camera = cv2.VideoCapture('./output2.avi')
camera.set(cv2.CAP_PROP_FPS, 30)
fourcctext = decode_fourcc(camera.get(cv2.CAP_PROP_FOURCC))
#fourccfloat = cv2.VideoWriter_fourcc(*fourcctext)
#out = cv2.VideoWriter('./output.avi',fourccfloat, 10.0, (640,480), isColor=True)
#print(out.isOpened())
while(camera.isOpened()): # and success):
    ret, inframe = camera.read()
    if ret==True:
        #frame = cv2.flip(frame,0)
        # write the flipped frame
        cv2.imshow('frame',inframe)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
camera.release()
del camera
cv2.destroyAllWindows()
# %%
#!/root/base/anaconda4p2/bin/python3
import imutils
from imutils.video import VideoStream
import cv2
import os

#os.chdir('MASINT_Proposal_Work/Media_Files/Initial/Video/')
vs = VideoStream(0).start()
time.sleep(2.0)
