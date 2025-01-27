"""
Created on 29.01.2020, by Nicole Hölzl
"""

import tensorflow as tf
from tensorflow.python.keras.layers import  Input, Embedding, Dot, Reshape, Dense
from tensorflow.python.keras.models import Model
import yolo
import glob

print(tf.__version__)
# tf_upgrade_v2 --infile=yolo.py --outfile=yolov2.py

# ----- VARIABLES -------
_BATCH_NORM_DECAY = 0.9
_BATCH_NORM_EPSILON = 1e-05
_LEAKY_RELU = 0.1
_ANCHORS = [(10, 13), (16, 30), (33, 23),
            (30, 61), (62, 45), (59, 119),
            (116, 90), (156, 198), (373, 326)]
_MODEL_SIZE = (416, 416)

# define path of input images
PATH = 'data/samples_singleperson/'
img_names = glob.glob(PATH + '*.jpg')

batch_size = len(img_names)
batch = yolo.load_images(img_names, model_size=_MODEL_SIZE)
class_names = yolo.load_class_names('data/files/coco.names')
n_classes = len(class_names)
max_output_size = 10
iou_threshold = 0.5
confidence_threshold = 0.5

model = yolo.Yolo_v3(n_classes=n_classes, model_size=_MODEL_SIZE,
                     max_output_size=max_output_size,
                     iou_threshold=iou_threshold,
                     confidence_threshold=confidence_threshold)

inputs = tf.placeholder(tf.float32, [batch_size, 416, 416, 3])

detections = model(inputs, training=False)

model_vars = tf.global_variables(scope='yolo_v3_model')
assign_ops = yolo.load_weights(model_vars, 'data/files/yolov3.weights')

with tf.Session() as sess:
    sess.run(assign_ops)
    detection_result = sess.run(detections, feed_dict={inputs: batch})

yolo.draw_boxes(img_names, detection_result, class_names, _MODEL_SIZE)
