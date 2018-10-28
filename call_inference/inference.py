from __future__ import print_function, division

import torch
import torch.nn as nn
import numpy as np
from torchvision import datasets, models, transforms
from PIL import Image


def image_loader(path_to_image):
    """
    load image, returns tensor
    :param: path_to_image: type: str | path to the image
    :return: image: type: torch.float | torch representation of the image
    """
    loader = transforms.Compose([
            transforms.Resize(256),
            transforms.CenterCrop(224),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])

    image = Image.open(path_to_image)
    image = loader(image).float()
    image = image[None, ...]
    return image

def call_inference(path_to_model, image_tensor, classes):
    """
    Call inference (make a prediction) on the class of an image with a given model
    :param path_to_model: type: str | path to model so the model can be loaded for inference
    :param path_to_image: type: torch.float | torch tensor representing the image that inference will be called on
    :param classes: type: list | list of strings corresponding to the model classes
    :return: prediction: type: str| the predicted class of the image with the associated probability
    """
    # load model
    # Initialize it
    model = models.resnet18()
    num_ftrs = model.fc.in_features
    model.fc = nn.Linear(num_ftrs, 3)

    # load it
    model.load_state_dict(torch.load(path_to_model))
    model.eval()

    with torch.no_grad():

        # Run image through model:
        outputs = model(image_tensor)

        # Convert results into a numpy array of probabilities and find max index
        probabilities = nn.functional.softmax(outputs).numpy()
        max_prob = np.max(probabilities)
        ind = np.argmax(probabilities)

    ret = 'Prediction: {0} with probability: {1:.2f}%'.format(classes[ind], max_prob*100)
    return ret


if __name__ == '__main__':
    image = image_loader('/Users/danielwilentz/Desktop/get_profesh/test_images/washington_sample_2.jpg')
    classes_list = ['Arizona', 'Hawaii', 'Washington']
    print(call_inference(path_to_model='/Users/danielwilentz/Desktop/get_profesh/my_ml/my_models/ft_model_1.pt',
                   image_tensor=image,
                   classes=classes_list))
