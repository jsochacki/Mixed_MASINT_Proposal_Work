#!/root/base/anaconda4p2/bin/python3
# %%
import cv2
import os

# %%
input_video_file_name = 'Final_In'
temporary_file_extension = '_Temporary_File.avi'
output_video_file_name = 'Final_Out'
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
while(camera.isOpened()): # and success):
    ret, inframe = camera.read()
    if ret==True:
        inframe = cv2.flip(inframe,0)
        # write the flipped frame
        out.write(inframe)
        cv2.imshow('frame',inframe)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
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
# Convert to mp4 for viewing on other computer like windows