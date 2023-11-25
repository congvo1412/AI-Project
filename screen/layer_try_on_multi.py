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
    upload_name = upload.name.split(".")[0]
    class_id, index = upload_name.split("_")
    index = int(index)

    class_id_jacket, index_jacket = meta[jacket].split("_")
    index_jacket = int(index_jacket)

    class_id_pant, index_pant = meta[pant].split("_")
    index_pant = int(index_pant)

    pid = (class_id, index, None)

    jacket_id = (class_id_jacket, index_jacket, 5)
    pant_id = (class_id_pant, index_pant, 5)

    gids = (jacket_id, pant_id)

    pimg, gimgs, oimgs, gen_img, pose = _dress_in_order(
        model, pid, ogids=gids, order=[2, 5, 1]
    )

    result = combine_result(pimg, gimgs, oimgs, gen_img, pose)

    return convert_to_pil(result)


def layer_try_on_multi(base_model, submit):
    with st.container():
        dummt, right, left = st.columns([2, 9, 3])

        with right:
            base, select = st.columns([6, 3])

            with base:
                st.subheader("Chọn layer 1")
                jacket = image_selector(
                    images, "jacket", {"width": "90%", "left": "30px"}
                )

                st.subheader("Chọn layer 2")
                pant = image_selector(images, "pant", 
                                      {"width": "90%", "left": "30px"}
                                      )

            with select:
                if jacket:
                    st.subheader("Layer 1 đã chọn")
                    image_selector([images[jacket]], "jacket_r")

                st.text("")

                if pant:
                    st.subheader("Layer 2 đã chọn")
                    image_selector([images[pant]], "pant_r")

    _, right, _ = st.columns([2, 9, 3])

    with right:
        st.subheader("Kết quả")

        if submit:
            if base_model:
                prediction = handle_try_on_click(base_model, jacket, pant)

                st.image(prediction, width=RESULT_IMAGE_SIZE)
            else:
                st.error("Vui lòng upload ảnh người mẫu")
