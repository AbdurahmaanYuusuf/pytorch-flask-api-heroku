import torch
from torchvision.transforms import transforms
import numpy as np
from torch.autograd import Variable
from io import open
import os
from PIL import Image
import glob
from torchvision import models


def get_model():
    model = models.densenet121(pretrained=True)
    model.eval()
    return model


def transform_image(image_bytes):
    transformer = transforms.Compose([transforms.Resize(256),
                                        transforms.CenterCrop(224),
                                        transforms.ToTensor(),
                                        transforms.Normalize(
                                            [0.485, 0.456, 0.406],
                                            [0.229, 0.224, 0.225])])
    
    image = Image.open(image_bytes)    
    if image.mode!="RGB":
        image.convert("RGB")
    image_tensor=transformer(image).float()
    image_tensor=image_tensor.unsqueeze_(0)   
    input=Variable(image_tensor)
    return input


# ImageNet classes are often of the form `can_opener` or `Egyptian_cat`
# will use this method to properly format it so that we get
# `Can Opener` or `Egyptian Cat`
def format_class_name(class_name):
    class_name = class_name.replace('_', ' ')
    class_name = class_name.title()
    return class_name
