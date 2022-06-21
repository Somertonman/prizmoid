import numpy as np

import streamlit as st

import tensorflow as tf
import tensorflow_hub as hub
from io import BytesIO

from PIL import Image
import os
import requests
import pathlib

os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

hub_handle = 'model/magenta_arbitrary-image-stylization-v1-256_2'
hub_model = hub.load(hub_handle)


def resize(img):
    """
    resize image
    :param img:
    :return:
    """
    max_dim = 512
    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img


def prepare_image_uploader(path_to_img: str):
    """
    prepare image to transfer style
    :param path_to_img:
    :return:
    """
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)
    img = resize(img)
    return img


def test_prepare_image_uploader():
    t_img = 'styles/test_img.jpg'
    assert np.sum(prepare_image_uploader(t_img)) == 702898.5


def tensor_to_image(tensor):
    """
    prepare image to tensorflow restyle algorithm
    :param tensor:
    :return:
    """
    tensor = tensor * 255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor) > 3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
    return Image.fromarray(tensor)


def prepare_image_url(user_image_from_url):
    """
    resizing image
    :param user_image_from_url: jpeg file
    :return:
    """
    img = np.array(user_image_from_url)
    img = resize(img)
    return img


def transfer_style(content_image, style_image):
    """
    transforming image to style
    :param content_image:
    :param style_image:
    :return:
    """
    stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
    final_img = tensor_to_image(stylized_image)
    return final_img


def get_user_image_from_url(url: str):
    '''
    get user image from url
    :param url:
    :return:
    '''
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img

        
def test_restyle_from_url():
    link = "https://klike.net/uploads/posts/2020-04/1587719791_1.jpg"
    style_img = "Василий Кандинский, Композиция 4.jpg"
    style_image_url = "styles/" + style_img
    user_image_from_url = get_user_image_from_url(link)
    
    user_image = prepare_image_url(user_image_from_url)
    style_image = prepare_image_uploader(style_image_url)
    final_img = transfer_style(user_image, style_image)
    assert np.sum(final_img) == 115081674
