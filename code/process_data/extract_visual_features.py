# coding=utf-8
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

"""Extract visual features of objects in image for every frame using VGG16"""

import argparse
from tensorflow.keras.applications.vgg16 import VGG16
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import Model
import xml.etree.ElementTree as ET
import numpy as np
import os
import time
import PIL
from tqdm import tqdm
from pathlib import Path

parser = argparse.ArgumentParser()

parser.add_argument('--annot_path', default='data/cv_annotations', type=str)
parser.add_argument('--frames_path', default='data/frames', type=str)
parser.add_argument('--results_path', default='data/visual_features', type=str)

def load_model(layer, weights='imagenet'):
    '''Loads VGG model with first fully connected layer as the output'''

    base_model = VGG16(weights=weights)
    model = Model(inputs=base_model.input, outputs=base_model.get_layer(layer).output)

    return model

def load_xml(video, args, root_dir, model):
    #Loads XML file and gets bbox coordinates and creates id for each bbox in the XML file

    tree = ET.parse(os.path.join(root_dir, args.annot_path, video, 'annotations.xml'))
    root = tree.getroot()
    #finds all track nodes
    for obj in tqdm(root.findall('track')):
        #print(obj.get('label'))
        label = obj.get('label')
        #for the found track node, list out bbox attributes
        for box in obj.findall('box'):
            if box.get('outside') == '1':
                continue
            else:
                framenum = box.get('frame')
                framenum = framenum.zfill(3)
                bbox = (float(box.get('xtl')),
                        float(box.get('ytl')),
                        float(box.get('xbr')),
                        float(box.get('ybr'))
                        )
                #Check whether 'ID' field is filled
                for attribute in box.iter('attribute'):
                    if attribute.get('name') == 'ID':
                        #No ID
                        if attribute.text == 'n/a':
                            id = obj.get('id')
                            file_name = video + '_' + 'f' + framenum + '_' + label + id + '.npz'
                            file_location = os.path.join(root_dir, args.results_path, video)
                        #Specified ID
                        else:
                            id = (attribute.text)
                            file_name = video + '_' + 'f' + framenum + '_' + label + id + '.npz'
                            file_location = os.path.join(root_dir, args.results_path, video)

                if not os.path.exists(file_location):
                    os.makedirs(file_location)
                if not os.path.exists(os.path.join(file_location, file_name)):
                    features = load_process_image(args, root_dir, video, framenum, bbox, model)
                    save_path = os.path.join(file_location, file_name)
                    np.savez_compressed(save_path, features)

def load_process_image(args, root_dir, video, framenum, bbox, model):
    # loads and processes image according to object bbox
    frame_name = framenum + '.jpg'
    img_path = os.path.join(root_dir, args.frames_path, video, frame_name)
    img = image.load_img(img_path)
    img_cropped = img.crop(bbox)
    img_resized = resize_image(img_cropped)

    features = extract_feature(img_resized, model)
    return features


def resize_image(img, size=224):
    # Resizing cropped image to maintain original cropped image aspect ratio, but with
    # padded zeros. From PIE_predict utils.py code
    img_size = img.size
    ratio = float(size) / max(img_size)

    if img_size[0] > size or img_size[1] > size:
        img_size = tuple([int(img_size[0] * ratio), int(img_size[1] * ratio)])
        img = img.resize(img_size, PIL.Image.NEAREST)
    img_padded = PIL.Image.new('RGB', (size, size))
    img_padded.paste(img, ((size - img_size[0]) // 2, (size - img_size[1]) // 2))
    return img_padded


def extract_feature(img, model):
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0)
    img_array = preprocess_input(img_array)

    features = model.predict(img_array)
    return features

if __name__ == "__main__":
    args = parser.parse_args()
    parent_dir = Path(os.getcwd()).parents[1]

    try:
        model = load_model('fc1')
        print("VGG16 model successfully loaded.")
    except:
        print("VGG16 model unsuccessfully loaded!")

    for video in os.listdir(os.path.join(parent_dir,args.annot_path)):
        print(f'Processing {video}.')
        load_xml(video, args, parent_dir, model)