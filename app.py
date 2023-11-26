import streamlit as st

from backend import (
    meta,
    pil_images,
)


from screen.pose_transform import pose_transform

from screen.vitural_try_on import vỉtual_try_on
from screen.layer_try_on import layer_try_on
from screen.layer_try_on_multi import layer_try_on_multi


screen_dict = {
    "Pose transfrom": pose_transform,
    "Virtual Try-on": vỉtual_try_on,
    "Virtual Try-on (Layer)": layer_try_on,
    "Virtual Try-on (Multi-Layer)": layer_try_on_multi,
}

st.set_page_config(layout="wide")


def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def main():
    local_css("style.css")
    with st.sidebar:
        feature = st.selectbox(
            "Select feature",
            (
                "Pose transfrom",
                "Virtual Try-on",
                "Virtual Try-on (Layer)",
                "Virtual Try-on (Multi-Layer)",
            ),
        )

        base_model = st.file_uploader("Upload ảnh mẫu")

        if base_model:
            filename = base_model.name.split(".")[0]
            try:
                index = meta.index(filename)
                st.image(pil_images[index])
            except Exception:
                pass

        submit = st.button("Try on")

    screen = screen_dict.get(feature)

    if screen:
        screen(base_model, submit)
    else:
        st.text("Feature is not implementd yet")


if __name__ == "__main__":
    main()
