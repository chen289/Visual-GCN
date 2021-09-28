# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""After downloading data, ensure the folder hierarchy and names are correct"""

import os
import argparse
from pathlib import Path
import glob
import pandas as pd

parser = argparse.ArgumentParser()

parser.add_argument("--data_path", default="data", type=str)
parser.add_argument("--cv_path", default="cv_annotations", type=str)
parser.add_argument("--nlp_path", default="nlp_annotations", type=str)
parser.add_argument("--video_path", default="videos", type=str)

def check_folders(root_path, args):
    """
    Check the correct folder names exist, create "video" folder, and read file name mapping file.
    """

    if os.path.exists(os.path.join(root_path, args.data_path, args.cv_path)):
        print("CV annotations folder exist.")
    else:
        print("CV annotations folder DOES NOT exist!")

    if os.path.exists(os.path.join(root_path, args.data_path, args.nlp_path)):
        print("NLP annotations folder exist.")
    else:
        print("NLP annotations folder DOES NOT exist!")

    if not os.path.exists(os.path.join(root_path, args.data_path, args.video_path)):
        os.makedirs(os.path.join(root_path, args.data_path, args.video_path))
        print("Created video folder.")
    else:
        print("Video folder exists.")

    #read in video name mapping file's name (excel file)
    mapping_file = glob.glob(os.path.join(root_path, args.data_path, "*.x*"))
    args.mapping_file = os.path.basename(mapping_file[0])

    return args

def reorg_videos(root_path, args):
    """
    Reorganizes video files to the correct folders.
    """

    #move video files in nlp_annotations into videos
    nlp_path = os.path.join(root_path, args.data_path, args.nlp_path)
    video_path = os.path.join(root_path, args.data_path, args.video_path)
    for video_file in os.listdir(nlp_path):
        video_num = video_file[-5:]
        video = "rawCase" + video_num + ".mp4"
        try:
            os.rename(os.path.join(nlp_path, video_file, video), os.path.join(video_path, video))
        except:
            print(f'Could not move {video} or it does not exist in the source folder.')

def rename_cv_annts(root_path, args):
    """
    Renames the CV annotation files to the same name as the NLP files using the name mapping excel sheet
    """

    name_df = pd.read_excel(os.path.join(root_path, args.data_path, args.mapping_file))
    for index, row in name_df.iterrows():
        video_folder = row["video_name"][:-8]
        #pad 0 in the video name if necessary
        if len(video_folder) == 33:
            left = video_folder[:24]
            right = video_folder[-6:]
            middle = video_folder[24:27].zfill(4)
            video_folder = left + middle + right
        video_id = "video_" + str(row["video_id"]).zfill(4)
        annt_path = os.path.join(root_path, args.data_path, args.cv_path)

        try:
            os.rename(os.path.join(annt_path, video_folder), os.path.join(annt_path, video_id))
        except:
            print(f'Unable able to rename video {video_folder} to {video_id}')


if __name__ == "__main__":
    args = parser.parse_args()
    parent_dir = Path(os.getcwd()).parents[1]

    args = check_folders(parent_dir, args)

    reorg_videos(parent_dir, args)
    rename_cv_annts(parent_dir, args)
