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


def handle_try_on_click(upload, select):
    upload_name = upload.name.split(".")[0]
    class_id, index = upload_name.split("_")
    index = int(index)

    class_id_select, index_select = meta[select].split("_")
    index_select = int(index_select)

    pid = (class_id, index, None)
    pose_id = (class_id_select, index_select, None)

    pimg, gimgs, oimgs, gen_img, pose = _dress_in_order(
        model, pid, pose_id=pose_id
    )

    result = combine_result(pimg, gimgs, oimgs, gen_img, pose)

    return convert_to_pil(result)


def pose_transform(base_model, submit):
    with st.container():
        dummt, right, left = st.columns([2, 9, 3])

        with right:
            base, select = st.columns([6, 3])

            with base:
                st.subheader("Chọn tư thế")
                jacket = image_selector(
                    images, "jacket", {"width": "90%", "left": "30px"}
                )

            with select:
                if jacket:
                    st.subheader("Tư thế đã chọn")
                    image_selector([images[jacket]], "pant_r")

    _, right, _ = st.columns([2, 9, 3])

    with right:
        st.subheader("Kết quả")

        if submit:
            if base_model:
                prediction = handle_try_on_click(base_model, jacket)

                st.image(prediction, width=RESULT_IMAGE_SIZE)

            else:
                st.error("Vui lòng upload ảnh người mẫu")
