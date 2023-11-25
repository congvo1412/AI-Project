import streamlit as st
from st_clickable_images import clickable_images

from constants import IMAGE_SELECTOR_HEIGHT


def image_selector(images, key, styles={}):
    return clickable_images(
        images,
        titles=[f"Image #{str(i)}" for i in range(8)],
        div_style={
            "display": "flex",
            "justify-content": "flex-start",
            "position": "relative",
            "width": "100%",
            "overflow-y": "hidden",
            **styles,
        },
        img_style={
            "margin": "5px", "height": IMAGE_SELECTOR_HEIGHT, "z-index": "1"
        },
        key=key,
    )


def preview_image(image, caption=""):
    return st.image(
        image,
        caption=caption,
    )
