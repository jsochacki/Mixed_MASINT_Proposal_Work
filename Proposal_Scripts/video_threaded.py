#!/usr/bin/env python

'''
Multithreaded video processing sample.
Usage:
   video_threaded.py {<video device number>|<video file name>}

   Shows how python threading capabilities can be used
   to organize parallel captured frame processing pipeline
   for smoother playback.

Keyboard shortcuts:

   ESC - exit
   space - switch between multi and single threaded processing
'''

# Python 2/3 compatibility
from __future__ import print_function

import numpy as np
import cv2
import sys
from multiprocessing.pool import ThreadPool
from collections import deque

import time

# %%
class DummyTask:
    def __init__(self, data):
        self.data = data
    def ready(self):
        return True
    def get(self):
        return self.data

# %%
print(__doc__)

cap = cv2.VideoCapture(0)

print(cap.isOpened())

def process_frame(frame, t0):
    # some intensive computation...
    frame = cv2.medianBlur(frame, 19)
    frame = cv2.medianBlur(frame, 19)
    return frame, t0

threadn = cv2.getNumberOfCPUs()
pool = ThreadPool(processes = threadn)
pending = deque()

# %%
threaded_mode = True
ret, frame = cap.read()
last_frame_time = time.clock()
while True:
    while len(pending) > 0 and pending[0].ready():
        res, t0 = pending.popleft().get()
        cv2.putText(res, "threaded = {0}".format(str(threaded_mode)),(20, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
        cv2.putText(res, "Cores = {0}".format(str(threadn)),(20, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 0, 255), 1)
        cv2.imshow('threaded video', res)
    if len(pending) < threadn:
        ret, frame = cap.read()
        t = time.clock()
        last_frame_time = t
        if threaded_mode:
            #task = pool.apply_async(process_frame, (frame.copy(), t))
            task = pool.apply_async(process_frame, (frame.copy(), t))
        else:
            task = DummyTask(process_frame(frame, t))
        pending.append(task)
    ch = 0xFF & cv2.waitKey(1)
    if ch == ord(' '):
        threaded_mode = not threaded_mode
    if ch == 27:
        break
# %%l
cap.release()
del cap
cv2.destroyAllWindows()
