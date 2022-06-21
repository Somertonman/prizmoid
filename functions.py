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


def show_image(image_file):
    """
    show_image
    :param image_file:
    :return:
    """
    img = Image.open(image_file)
    return img


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


def prepare_image_url(user_image_from_url):
    """
    resizing image
    :param user_image_from_url: jpeg file
    :return:
    """
    img = np.array(user_image_from_url)
    img = resize(img)
    return img


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


def save_new_image_style(style_file, style_file_name):
    """
    add new style image to gallery
    :param style_file:
    :param style_file_name:
    :return:
    """
    for filename in os.listdir('styles'):
        if filename == style_file_name:
            st.write(f'A style named "{style_file_name}" already exists')

    image = Image.open(pathlib.Path(f"styles/{style_file}"))
    rgb_im = image.convert('RGB')
    new_file_name = os.path.join("styles/", style_file_name + '.jpg')
    rgb_im.save(new_file_name, format="JPEG")
    return new_file_name


def save_user_image(image):
    """
    save_user_image to restyle
    :param image:
    :return:
    """
    image = Image.open(image)
    rgb_im = image.convert('RGB')
    new_file_name = os.path.join("/", "user_file" + '.jpg')
    rgb_im.save(new_file_name, format="JPEG")
    return new_file_name


def download_style_file(url, local_filename):
    """
    download new style image to gallery
    :param url:
    :param local_filename:
    :return:
    """
    r = requests.get(url)
    with open(os.path.join("styles", local_filename + '.jpg'), 'wb') as f:
        for chunk in r.iter_content(chunk_size=512 * 1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
    local_filename = local_filename + '.jpg'
    return local_filename


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


def show_gallery_of_styles():
    """
    show gallery of styles application
    :return:
    """
    images_glob = os.listdir("styles/")
    images_glob = [x for x in images_glob if x.endswith(("jpg", "jpeg", "png"))]

    for i in range(len(images_glob)):
        cols = st.columns(2)
        cols[0].image("styles/" + images_glob[i], width=200)
        cols[1].write(images_glob[i].rsplit('.', 1)[0])


def get_user_image_from_url(url: str):
    '''
    get user image from url
    :param url:
    :return:
    '''
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    return img


def restyle_downloaded(style_image_url, image_file):
    """
    restyle user downloaded image by style image
    :param style_image_url:
    :param image_file:
    :return:
    """
    if st.button('Restyle'):
        file_user_path = save_user_image(image_file)
        user_image = prepare_image_uploader(file_user_path)
        style_image = prepare_image_uploader(style_image_url)
        final_img = transfer_style(user_image, style_image)
        st.image(final_img)


def restyle_from_url(style_image_url, user_image_from_url):
    """
    restyle user image from URL by style image
    :param style_image_url:
    :param user_image_from_url:
    :return:
    """
    if st.button('Restyle'):
        user_image = prepare_image_url(user_image_from_url)
        style_image = prepare_image_uploader(style_image_url)
        final_img = transfer_style(user_image, style_image)
        st.image(final_img)
