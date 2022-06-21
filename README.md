# prizmoid API + web-app
Fast Style Transfer for given images

## Web-app
https://prizmoid-xoqsf.ondigitalocean.app/

## Description

Project uses deep learning to compose one image in the style of another image. This is known as neural style transer.

<img width="400" alt="image" src="https://user-images.githubusercontent.com/8521878/174752202-620c2559-1724-4567-b2dd-efb15077d20c.png">

## How to use this app

1. Open https://prizmoid-xoqsf.ondigitalocean.app/
2. Choose one of the existing styles (pre-uploaded earlier).
 <img width="400" alt="image" src="https://user-images.githubusercontent.com/8521878/174752616-4456e622-38f1-4958-8680-f158b3300cda.png">
3. You can upload your own style selecting 'upload_style' option on the left sidebar, choosing name for your style and clicking 'Upload' button.
4. To transfer style to your image you can either use web url or upload your image directly and clicking 'Transfer style' button.
<img width="400" alt="image" src="https://user-images.githubusercontent.com/8521878/174753800-ba6fe2d4-68b2-48f2-9677-6ef0faa495ce.png">


## What you can do with the app

* upload your custom image to transfer style from
* view all image styles available
* upload your image and select one of the existing image styles to transfer style from
* use it as a full-feature web-app
* use API services to serve your requests

## Code

* Python functions: https://github.com/Somertonman/prizmoid/blob/main/functions.py
* Streamlit app code: https://github.com/Somertonman/prizmoid/blob/main/streamlit_app.py
* FastAPI - TBD

## API specification

TBD

## References

* https://www.tensorflow.org/tutorials/generative/style_transfer
* 
