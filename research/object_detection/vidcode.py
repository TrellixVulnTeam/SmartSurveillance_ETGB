
import os
import cv2
import numpy as np
import tensorflow as tf
import sys
sys.path.append("C:\tensorflow1\models\research")

# Import utilites
from utils import label_map_util
from utils import visualization_utils as vis_util

def vid():
    MODEL_NAME = 'inference_graph'
    VIDEO_NAME = 'test.h264'

    CWD_PATH = os.getcwd()

    PATH_TO_CKPT = os.path.join(CWD_PATH,MODEL_NAME,'frozen_inference_graph.pb')

    PATH_TO_LABELS = os.path.join(CWD_PATH,'training','labelmap.pbtxt')

    PATH_TO_VIDEO = os.path.join(CWD_PATH,VIDEO_NAME)

    NUM_CLASSES = 6


    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)

    detection_graph = tf.Graph()
    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')

            sess = tf.Session(graph=detection_graph)

            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')

            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')

            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            video = cv2.VideoCapture(PATH_TO_VIDEO)
            return video,sess,detection_boxes,detection_scores,detection_classes,num_detections,image_tensor,category_index
