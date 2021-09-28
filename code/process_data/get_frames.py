# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

'''Given video path, extract frames for all videos. Check if frames exist first.'''

import os
import argparse
from pathlib import Path
import cv2
from tqdm import tqdm

parser = argparse.ArgumentParser()

parser.add_argument("--video_path", default="data/videos", type=str)
parser.add_argument("--frames_path", default="data/frames", type=str)

def video_to_frames(root_path, args):
    """
    Goes through all the videos in "videos" folder and splits them into frames in the "frames" folder. "frames" folder
    created here.
    """
    #create 'data/frames' folder
    if not os.path.exists(os.path.join(root_path, args.frames_path)):
        os.makedirs(os.path.join(root_path, args.frames_path))
        print("Created 'frames' folder.")


    for video in tqdm(os.listdir(os.path.join(root_path, args.video_path))):
        name = "video" + video[7:12]
        video_target = os.path.join(root_path, args.video_path, video)
        frames_target = os.path.join(root_path, args.frames_path, name)

        if not os.path.exists(frames_target):
            os.makedirs(frames_target)
            print(f'Created frames folder for video {name}')

        try:
            vidcap = cv2.VideoCapture(video_target)
            if not vidcap.isOpened():
                raise Exception(f'Cannot open file {video_target}')
        except Exception as e:
            raise e

        cur_frame = 0
        while(True):
            success, frame = vidcap.read()
            if success:
                frame_num = str(cur_frame).zfill(3)
                cv2.imwrite(os.path.join(frames_target, f'{frame_num}.jpg'), frame)
            else:
                break
            cur_frame += 1
        vidcap.release()

if __name__ == "__main__":
    args = parser.parse_args()
    parent_dir =  Path(os.getcwd()).parents[1]

    video_to_frames(parent_dir, args)

