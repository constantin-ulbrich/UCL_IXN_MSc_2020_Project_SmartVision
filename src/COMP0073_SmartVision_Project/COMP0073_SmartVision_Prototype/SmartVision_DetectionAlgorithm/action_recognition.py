# Module Description: This module should have been developed to recognise gestures and other actions from short videos.
# However, due to the time constrain of the project, this could not be developed. 
# For future development, follow this source, it has very insightful information: https://github.com/microsoft/computervision-recipes/tree/1bb489af757fde7c773e16fab87b24305cff4457

#Here are the necessary libraries:
# Regular Python libraries
import sys
from collections import deque #
import io
import requests
import os
from time import sleep, time
from threading import Thread
from IPython.display import Video

# Third party tools
import decord #
import IPython.display #
from ipywebrtc import CameraStream, ImageRecorder
from ipywidgets import HBox, HTML, Layout, VBox, Widget, Label
import numpy as np
from PIL import Image
import torch
import torch.cuda as cuda
import torch.nn as nn
from torchvision.transforms import Compose

# utils_cv
sys.path.append("../../")
from utils_cv.action_recognition.data import KINETICS, Urls
from utils_cv.action_recognition.dataset import get_transforms
from utils_cv.action_recognition.model import VideoLearner
from utils_cv.action_recognition.references import transforms_video as transforms
from utils_cv.common.gpu import system_info, torch_device
from utils_cv.common.data import data_path

system_info()