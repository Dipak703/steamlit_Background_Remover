import sys
import types
import warnings

# Suppress specific timm warning
warnings.filterwarnings("ignore", category=FutureWarning, module="timm.models.layers")

# Monkey-patch torch.classes path issue
if not hasattr(sys.modules.get("torch"), "__path__"):
    torch_classes = types.SimpleNamespace(_path=[])
    sys.modules["torch.classes"] = torch_classes

import streamlit as st
import cv2
import numpy as np
from io import BytesIO
from PIL import Image
from transparent_background import Remover

def process_image(image):
    try:
        remover = Remover()
        img = Image.open(image).convert("RGB")

        with st.spinner("Processing image..."):
            out = remover.process(img, type="rgba")

        return out  # `out` is already a PIL Image

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        return None

def main():
    st.title("Image Upload and Processing App")

    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "tif", "tiff"])

    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)

            # Convert unsupported image modes
            if image.mode == 'I;16':
                image = image.point(lambda i: i * (1.0 / 256)).convert('RGB')

            st.image(image, caption="Uploaded Image", use_container_width=True)

            processed_pil = process_image(uploaded_file)

            if processed_pil:
                st.image(processed_pil, caption="Processed Image", use_container_width=True)

                buf = BytesIO()
                processed_pil.save(buf, format="PNG")
                byte_im = buf.getvalue()

                st.download_button(
                    label="Download Processed Image",
                    data=byte_im,
                    file_name="processed_image.png",
                    mime="image/png"
                )

        except Exception as e:
            st.error(f"Error loading image: {e}")

if __name__ == "__main__":
    main()
