reorder_data.py
"""After downloading data, ensure the folder hierarchy and names are correct"""
Download videos, CV, and NLP annotations from OneDrive location to Visual-GCN->data
    1. Name cv annotation folder "cv_annotations"
    2. Name nlp/intention annotation folder "nlp_annotations" w/ the videos in them as downloaded.

get_frames.py
'''Given video path, extract frames for all videos. Check if frames exist first.'''
All video files should be under Visual-GCN->data->video