import io

import streamlit as st
from PIL import Image

from processors.background import remove_background


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Image Processor",
    page_icon="🖼️",
    layout="centered",
)


# =========================================================
# CUSTOM STYLE
# =========================================================

st.markdown(
    """
    <style>
        .block-container {
            max-width: 1000px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        .app-header {
            text-align: center;
            margin-bottom: 2rem;
        }

        .app-title {
            font-size: 2.4rem;
            font-weight: 700;
            margin-bottom: 0.4rem;
        }

        .app-subtitle {
            color: #6b7280;
            font-size: 1rem;
        }

        .section-title {
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 0.8rem;
        }

        .image-card {
            border: 1px solid #e5e7eb;
            border-radius: 12px;
            padding: 1rem;
            background: #ffffff;
            margin-bottom: 1rem;
        }

        .image-label {
            font-weight: 600;
            margin-bottom: 0.8rem;
        }

        .image-info {
            color: #6b7280;
            font-size: 0.85rem;
            margin-top: 0.5rem;
        }

        .result-info {
            padding: 0.8rem 1rem;
            border-radius: 8px;
            background: #f3f4f6;
            color: #4b5563;
            font-size: 0.9rem;
            margin-top: 0.5rem;
        }

        div.stButton > button {
            width: 100%;
            height: 2.8rem;
            border-radius: 8px;
            font-weight: 600;
        }

        div.stDownloadButton > button {
            width: 100%;
            border-radius: 8px;
            font-weight: 600;
        }
    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER
# =========================================================

def create_preview(image: Image.Image, max_size=(400, 400)):
    """
    Membuat versi kecil gambar hanya untuk preview.
    Gambar asli tidak diubah.
    """
    preview = image.copy()
    preview.thumbnail(max_size)
    return preview


def image_to_bytes(image: Image.Image) -> bytes:
    """
    Mengubah PIL Image menjadi bytes PNG untuk download.
    """
    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    return buffer.getvalue()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    """
    <div class="app-header">
        <div class="app-title">Image Processor</div>
        <div class="app-subtitle">
            Simple AI image processing for background removal and enhancement.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# UPLOAD
# =========================================================

st.markdown(
    '<div class="section-title">Upload Image</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=["jpg", "jpeg", "png", "webp"],
    label_visibility="collapsed",
)


# =========================================================
# IMAGE PROCESSING
# =========================================================

if uploaded_file:

    image = Image.open(uploaded_file).convert("RGBA")

    width, height = image.size

    # Preview hanya untuk tampilan
    preview = create_preview(image)

    st.markdown(
        f"""
        <div class="image-info">
            Original size: {width} × {height} px
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.write("")

    # =====================================================
    # ACTION
    # =====================================================

    st.markdown(
        '<div class="section-title">Background Removal</div>',
        unsafe_allow_html=True,
    )

    st.write(
        "Remove the background from your image using U²-NetP."
    )

    process_button = st.button(
        "Remove Background",
        type="primary",
    )

    # =====================================================
    # RESULT
    # =====================================================

    if process_button:

        with st.spinner("Removing background..."):

            result = remove_background(image)

        st.session_state["result"] = result

    # =====================================================
    # PREVIEW
    # =====================================================

    result = st.session_state.get("result")

    col1, col2 = st.columns(2)

    with col1:

        st.markdown(
            """
            <div class="image-card">
                <div class="image-label">Original</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Gunakan preview, bukan gambar asli
        st.image(
            preview,
            width=400,
        )

        st.caption(
            f"{width} × {height} px"
        )

    with col2:

        st.markdown(
            """
            <div class="image-card">
                <div class="image-label">Result</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if result is not None:

            result_preview = create_preview(result)

            st.image(
                result_preview,
                width=400,
            )

            result_width, result_height = result.size

            st.caption(
                f"{result_width} × {result_height} px"
            )

        else:

            st.info(
                "Processed image will appear here."
            )

    # =====================================================
    # DOWNLOAD
    # =====================================================

    if result is not None:

        st.write("")

        st.download_button(
            label="Download PNG",
            data=image_to_bytes(result),
            file_name="background_removed.png",
            mime="image/png",
        )