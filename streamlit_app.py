import streamlit as st
from functions import *
import os

st.set_page_config(
    page_title="PRIZMOID",
    page_icon="🎈",
)


# 'Screens'
# Upload style image and save file in /styles

def upload_style_image():
    """

    :return:
    """
    style_file_name = st.text_input("Name your style", 'My perfect style')
    original_image_url = st.text_input("Upload your style image from URL", )

    if st.button("Upload"):
        style_file = download_style_file(original_image_url, style_file_name)
        new_file_name = save_new_image_style(style_file, style_file_name)
        st.success("Done!")
        st.success(f"File Saved in {new_file_name}")

def get_user_image_from_url(url):
  response = requests.get(url)
  img = Image.open(BytesIO(response.content))
  return img

def restyle_downloaded(image_file):
    if st.button('Restyle'):
        file_user_path = save_user_image(image_file)
        user_image = load_img(file_user_path)
        style_image = load_img(style_image_url)
        final_img = transfer_style(user_image, style_image)
        st.image(final_img)


def uploader_user_image():
    pass
    """

    :return:
    """


    # if choice == "Web link":
    #     st.write('This feature in progress')
    # original_image_url = st.text_input("Style image from URL", )
    # if st.button('Restyle'):
    #     uploaded_image = download_file(original_image_url, "original.jpg")
    #     st.image(uploaded_image)
    #     content_image = load_img("original.jpg")
    #     style_image = load_img(style_image_url)
    #     final_img = transfer_style(content_image, style_image)
    #     st.image(final_img)

# def get_user_image_from_url(url):


def show_gallery_of_styles():
    """

    :return:
    """
    images_glob = os.listdir("styles/")
    images_glob = [x for x in images_glob if x.endswith(("jpg", "jpeg", "png"))]

    for i in range(len(images_glob)):
        cols = st.columns(2)
        cols[0].image("styles/" + images_glob[i], width=200)
        cols[1].write(images_glob[i].rsplit('.', 1)[0])


page = st.sidebar.radio('Choose action',
                        ('transfer_style', 'upload_style'))

if page == 'upload_style':
    st.header('Upload new style')
    upload_style_image()

elif page == "transfer_style":
    images_glob = os.listdir("styles/")
    images_glob = set([x for x in images_glob if x.endswith(("jpg", "jpeg", "png"))])
    style_img = st.radio('Choose style', images_glob)
    style_image_url = "styles/" + style_img

    # original_image = upload_your_image()
    menu = ["Upload", "Web link"]
    choice = st.sidebar.selectbox("Upload/Use link", menu)

    if choice == "Upload":
        downloaded_user_image_file = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"])
        if downloaded_user_image_file:
            st.image(show_image(downloaded_user_image_file))
            restyle_downloaded(downloaded_user_image_file)

    if choice == "Web link":
        original_image_url = st.text_input("Upload your image from URL", )
        if original_image_url:
            user_image_from_url = get_user_image_from_url(original_image_url)
            st.image(user_image_from_url)
            if st.button('Restyle'):
                user_image = load_img_from_url(user_image_from_url)
                style_image = load_img(style_image_url)
                final_img = transfer_style(user_image, style_image)
                st.image(final_img)

    st.header('Styles gallery')
    show_gallery_of_styles()

    if st.button('system_info'):
        pwd = os.getcwd()
        listing = os.listdir(pwd)
        st.write(listing)
        st.write(os.listdir(pwd + '/styles/'))
