from functions import *
import os

st.set_page_config(
    page_title="PRIZMOID",
    page_icon="🎈",
)

page = st.sidebar.radio('Choose action',
                        ('transfer_style', 'upload_style'))

if page == 'upload_style':
    st.header('Upload new style')
    style_file_name = st.text_input("Name your style", 'My perfect style')
    original_image_url = st.text_input("Upload your style image from URL", )

    if st.button("Upload"):
        style_file = download_style_file(original_image_url, style_file_name)
        new_file_name = save_new_image_style(style_file, style_file_name)
        st.success("Done!")
        st.success(f"File Saved in {new_file_name}")

elif page == "transfer_style":
    images_glob = os.listdir("styles/")
    images_glob = set([x for x in images_glob if x.endswith(("jpg", "jpeg", "png"))])
    style_img = st.radio('Choose style', images_glob)
    style_image_url = "styles/" + style_img

    menu = ["Upload", "Web link"]
    choice = st.sidebar.selectbox("Upload/Use link", menu)

    if choice == "Upload":
        downloaded_user_image_file = st.file_uploader("Upload Images", type=["jpg", "jpeg", "png"])
        if downloaded_user_image_file:
            st.image(show_image(downloaded_user_image_file))
            restyle_downloaded(style_image_url, downloaded_user_image_file)

    if choice == "Web link":
        original_image_url = st.text_input("Upload your image from URL", )
        if original_image_url:
            user_image_from_url = get_user_image_from_url(original_image_url)
            st.image(user_image_from_url)
            if st.button('Restyle'):
                user_image = prepare_image_url(user_image_from_url)
                style_image = prepare_image_uploader(style_image_url)
                final_img = transfer_style(user_image, style_image)
                st.image(final_img)

    st.header('Styles gallery')
    show_gallery_of_styles()

    if st.button('system_info'):
        pwd = os.getcwd()
        listing = os.listdir(pwd)
        st.write(listing)
        st.write(os.listdir(pwd + '/styles/'))
