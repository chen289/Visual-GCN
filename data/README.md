# Preprocess Data
Follow the below steps to parse the raw data, create the right folder hierarchy, and extract necesssary
features.

## Download/Parse Raw Data
1. Download CVATdata and videoAndTextData from Onedrive into <mark>Visual-GCN/data/</mark>.
2. Rename CVATdata -> cv_annotations
3. Rename videoAndTextData -> nlp_annotations
4. Run <mark>Visual-GCN/code/process_data/reorder_data.py</mark>

## Split Video to Frames
1. Double check videos are now under <mark>Visual-GCN/data/videos</mark>
2. Run <mark>Visual-GCN/code/process_data/get_frames.py</mark>

## Extract Visual Features
Visual features extracted using VGG16.
1. Run <mark>Visual-GCN/code/process_data/extract_visual_features.py</mark>

## Get Human Key-Point Estimation
Estimating human pose using HRNet.