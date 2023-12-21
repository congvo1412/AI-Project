import streamlit as st

from backend import (
    meta,
    images,
    model,
    _dress_in_order,
    convert_to_pil,
)

from backend.model import combine_result

from components import image_selector

from constants import RESULT_IMAGE_SIZE


def handle_try_on_click(upload, jacket, pant):
    upload_name = upload.name.split('.')[0]
    class_id, index = upload_name.split("_")
    index = int(index)

    class_id_jacket, index_jacket = meta[jacket].split("_")
    index_jacket = int(index_jacket)

    class_id_pant, index_pant = meta[pant].split("_")
    index_pant = int(index_pant)

    pid = (class_id, index, None)

    jacket_id = (class_id_jacket, index_jacket, 5)
    pant_id = (class_id_pant, index_pant, 1)

    gids = (jacket_id, pant_id)

    pimg, gimgs, oimgs, gen_img, pose = _dress_in_order(
        model, pid, gids=gids, order=[2, 5, 1]
    )

    result = combine_result(pimg, gimgs, oimgs, gen_img, pose)

    return convert_to_pil(result)


def vỉtual_try_on(base_model, submit):
    with st.container():
        dummt, right, left = st.columns([2, 9, 3])

        with right:
            base, select = st.columns([6, 3])

            with base:
                st.subheader("SHIRT")
                jacket = image_selector(
                    images, "jacket", {"width": "90%", "left": "30px"}
                )
                
                st.subheader("PANT")
                pant = image_selector(
                    images, "pant", {"width": "90%", "left": "30px"}
                )
                
            with select:
                if jacket:
                    st.subheader("Selected SHIRT")                    
                    image_selector([images[jacket]], "jacket_r", {"border": "solid 3px #FFD700", "justify-content": "center"})
                    
                st.text("")
                
                if pant:
                    st.subheader("Selected PANT")
                    image_selector([images[pant]], "pant_r", {"border": "solid 3px #FFD700", "justify-content": "center"})
                    
    dummt, right, left = st.columns([2, 9, 3])

    with right:
        st.subheader("Result")

        if submit:
            if base_model:
                prediction = handle_try_on_click(base_model, jacket, pant)

                st.image(prediction, width=RESULT_IMAGE_SIZE)
            else:
                st.error("Please upload model photos")