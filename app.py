import io

import streamlit as st
from PIL import Image

from processors.background import remove_background
from processors.replacement import (
    create_solid_background,
    replace_background,
)
from processors.upscale import upscale_image


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Process That Image",
    page_icon="🖼️",
    layout="centered",
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
    <style>

    /* Main container */
    .block-container {
        max-width: 900px;
        padding-top: 1.5rem;
        padding-bottom: 2.5rem;
    }

    /* Header */
    .app-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .app-subtitle {
        text-align: center;
        color: #6b7280;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
    }

    /* Section title */
    .section-title {
        font-size: 1.05rem;
        font-weight: 600;
        margin-top: 1.2rem;
        margin-bottom: 0.6rem;
    }

    /* Preview labels */
    .preview-title {
        font-size: 0.9rem;
        font-weight: 600;
        margin-bottom: 0.3rem;
    }

    /* Result information */
    .result-info {
        padding: 0.65rem 0.8rem;
        border-radius: 8px;
        background-color: #f3f4f6;
        font-size: 0.8rem;
        margin-top: 0.5rem;
        margin-bottom: 0.8rem;
    }

    /* Mobile */
    @media (max-width: 640px) {

        .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
            padding-top: 1rem;
        }

        .app-title {
            font-size: 1.6rem;
        }

        .app-subtitle {
            font-size: 0.78rem;
            margin-bottom: 1.2rem;
        }

        .section-title {
            font-size: 0.95rem;
        }

    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def create_preview(
    image: Image.Image,
    max_size=(500, 500),
):
    """
    Membatasi ukuran preview tanpa mengubah ukuran
    gambar sebenarnya.
    """
    preview = image.copy()
    preview.thumbnail(max_size)
    return preview


def image_to_bytes(
    image: Image.Image,
    format="PNG",
):
    """
    Convert PIL Image menjadi bytes.
    """
    buffer = io.BytesIO()

    image.save(
        buffer,
        format=format,
    )

    return buffer.getvalue()


# =========================================================
# HEADER
# =========================================================

st.markdown(
    '<br>'
    '<div class="app-title">Process That Image</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="app-subtitle">
        Remove background, replace background, and upscale your image.
    </div>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# 1. UPLOAD
# =========================================================

st.markdown(
    '<div class="section-title">1. Upload Image</div>',
    unsafe_allow_html=True,
)

uploaded_file = st.file_uploader(
    "Choose an image",
    type=[
        "jpg",
        "jpeg",
        "png",
        "webp",
    ],
    help="Supported formats: JPG, JPEG, PNG, WEBP",
)


if uploaded_file:

    image = Image.open(uploaded_file).convert("RGBA")

    st.caption(
        f"Original size: {image.width} × {image.height} px"
    )


    # =====================================================
    # 2. PROCESSING
    # =====================================================

    st.markdown(
        '<div class="section-title">2. Processing</div>',
        unsafe_allow_html=True,
    )

    processing_type = st.radio(
        "Choose processing",
        [
            "Background Removal",
            "Background Replacement",
            "Image Upscaling",
        ],
        horizontal=True,
        label_visibility="collapsed",
    )


    # =====================================================
    # BACKGROUND REMOVAL
    # =====================================================

    if processing_type == "Background Removal":

        st.caption(
            "Remove the background and make it transparent."
        )

        process_button = st.button(
            "Remove Background",
            type="primary",
            use_container_width=True,
        )

        if process_button:

            with st.spinner(
                "Removing background..."
            ):

                try:

                    result = remove_background(
                        image
                    )

                    st.session_state[
                        "processed_result"
                    ] = result

                except Exception as e:

                    st.error(
                        f"Failed to remove background: {e}"
                    )


    # =====================================================
    # BACKGROUND REPLACEMENT
    # =====================================================

    elif processing_type == "Background Replacement":

        background_type = st.radio(
            "Background",
            [
                "Solid Color",
                "Custom Image",
                "Transparent",
            ],
            horizontal=True,
        )


        # -------------------------------------------------
        # SOLID COLOR
        # -------------------------------------------------

        if background_type == "Solid Color":

            selected_color = st.color_picker(
                "Background color",
                "#FFFFFF",
            )

            process_button = st.button(
                "Replace Background",
                type="primary",
                use_container_width=True,
            )

            if process_button:

                with st.spinner(
                    "Removing and replacing background..."
                ):

                    try:

                        foreground = remove_background(
                            image
                        )

                        background = create_solid_background(
                            foreground.size,
                            selected_color,
                        )

                        result = replace_background(
                            foreground,
                            background,
                        )

                        st.session_state[
                            "processed_result"
                        ] = result

                    except Exception as e:

                        st.error(
                            f"Failed to process image: {e}"
                        )


        # -------------------------------------------------
        # CUSTOM IMAGE
        # -------------------------------------------------

        elif background_type == "Custom Image":

            background_file = st.file_uploader(
                "Upload background image",
                type=[
                    "jpg",
                    "jpeg",
                    "png",
                    "webp",
                ],
                key="background_upload",
            )

            if background_file:

                background_image = Image.open(
                    background_file
                ).convert("RGBA")

                process_button = st.button(
                    "Replace Background",
                    type="primary",
                    use_container_width=True,
                )

                if process_button:

                    with st.spinner(
                        "Removing and replacing background..."
                    ):

                        try:

                            foreground = remove_background(
                                image
                            )

                            result = replace_background(
                                foreground,
                                background_image,
                            )

                            st.session_state[
                                "processed_result"
                            ] = result

                        except Exception as e:

                            st.error(
                                f"Failed to process image: {e}"
                            )

            else:

                st.info(
                    "Upload a background image first."
                )


        # -------------------------------------------------
        # TRANSPARENT
        # -------------------------------------------------

        elif background_type == "Transparent":

            process_button = st.button(
                "Remove Background",
                type="primary",
                use_container_width=True,
            )

            if process_button:

                with st.spinner(
                    "Removing background..."
                ):

                    try:

                        result = remove_background(
                            image
                        )

                        st.session_state[
                            "processed_result"
                        ] = result

                    except Exception as e:

                        st.error(
                            f"Failed to remove background: {e}"
                        )


    # =====================================================
    # IMAGE UPSCALING
    # =====================================================

    elif processing_type == "Image Upscaling":

        scale = st.selectbox(
            "Upscale factor",
            [2, 4],
            format_func=lambda x: f"{x}×",
        )

        output_width = image.width * scale
        output_height = image.height * scale

        st.caption(
            f"Output size: {output_width} × {output_height} px"
        )

        process_button = st.button(
            "Upscale Image",
            type="primary",
            use_container_width=True,
        )

        if process_button:

            with st.spinner(
                f"Upscaling image {scale}×..."
            ):

                try:

                    result = upscale_image(
                        image,
                        scale,
                    )

                    st.session_state[
                        "processed_result"
                    ] = result

                except Exception as e:

                    st.error(
                        f"Failed to upscale image: {e}"
                    )


    # =====================================================
    # 3. PREVIEW
    # =====================================================

    result = st.session_state.get(
        "processed_result"
    )

    if result is not None:

        st.markdown(
            '<div class="section-title">3. Preview</div>',
            unsafe_allow_html=True,
        )

        # -------------------------------------------------
        # ORIGINAL + RESULT
        # -------------------------------------------------

        col1, col2 = st.columns(
            2,
            gap="medium",
        )

        with col1:

            st.markdown(
                '<div class="preview-title">Original</div>',
                unsafe_allow_html=True,
            )

            st.image(
                create_preview(image),
                width="stretch",
            )

            st.caption(
                f"{image.width} × {image.height} px"
            )


        with col2:

            st.markdown(
                '<div class="preview-title">Result</div>',
                unsafe_allow_html=True,
            )

            st.image(
                create_preview(result),
                width="stretch",
            )

            st.caption(
                f"{result.width} × {result.height} px"
            )


        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------

        st.download_button(
            label="Download Result",
            data=image_to_bytes(
                result,
                "PNG",
            ),
            file_name="processed_image.png",
            mime="image/png",
            type="primary",
            use_container_width=True,
        )