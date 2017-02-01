#!/root/base/anaconda4p2/bin/python3

import numpy as np
import cv2
import os
import v4l2capture
import select

# %%
os.chdir('/root/base/development/MASINT_Proposal_Work/Media_Files/Initial/Video/')
# %%
output_video_file_name = 'Final_Out'
script_name = 'v4l2captutre_test.py'
set_fps = 30
# %%
def decode_fourcc(v):
    v = int(v)
    return "".join([chr((v >> 8 * i) & 0xFF) for i in range(4)])
# %%

#cap = cv2.VideoCapture(0)
#cap.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 1920)      # <-- this doesn't work. OpenCV tries to set VIDIO_S_CROP instead of the frame format
#cap.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 1080)

# The following is from: https://github.com/gebart/python-v4l2capture

# Open the video device.
video = v4l2capture.Video_device("/dev/video0")

# Suggest an image size to the device. The device may choose and
# return another size if it doesn't support the suggested one.
size_x, size_y = video.set_format(640, 480, fourcc='MJPG')

print("device chose {0}x{1} res".format(size_x, size_y))

# Create a buffer to store image data in. This must be done before
# calling 'start' if v4l2capture is compiled with libv4l2. Otherwise
# raises IOError.
video.create_buffers(90)

# Send the buffer to the device. Some devices require this to be done
# before calling 'start'.
video.queue_all_buffers()
video.set_fps(set_fps)
# %%

os.chdir('/root/base/development/MASINT_Proposal_Work/Media_Files/Initial/Video')

fourccCode = cv2.VideoWriter_fourcc(*'MJPG')
out = cv2.VideoWriter(
                      './{0}.avi'.format(output_video_file_name),
                      fourccCode,
                      set_fps,
                      (640,480),
                      isColor=True)
print(out.isOpened())
# %%
# Start the device. This lights the LED if it's a camera that has one.
print("start capture")
video.start()

# %%
while(True):
    #We used to do the following, but it doesn't work :(
    #ret, frame = cap.read()
    
    #Instead...
    
    # Wait for the device to fill the buffer.
    select.select((video,), (), ())

    # The rest is easy :-)
    image_data = video.read_and_queue()
    
    print("decode")
    frame = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)

    cv2.putText(frame, 'Set Frames Per Second = {0}'.format(set_fps),
                         (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
    cv2.imshow('frame', frame)
    out.write(frame)
    key = cv2.waitKey(1)
    if key & 0xFF == ord('q'):
        break

# %%
#cap.release()
video.close()
del video
out.release()
del out
cv2.destroyAllWindows()

# %%
%%bash -s $output_video_file_name
ffmpeg -i ./$1.avi -r 25 -pix_fmt yuv420p -strict -2 -acodec aac -b:a 128k -vcodec libx264 -crf 21 -rc-lookahead 250 ./$1.mp4
# %%
%%bash
cp * /mnt/hgfs/BHD/L64/Source_Files/Video/

# %%
os.chdir('/root/base/development/MASINT_Proposal_Work/Proposal_Scripts')
# %%
%%bash -s $script_name
cp ./$1 /mnt/hgfs/BHD/L64/Source_Files/Video/
# Convert to mp4 for viewing on other computer like windows