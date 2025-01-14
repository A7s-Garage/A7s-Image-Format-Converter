import streamlit as st
from PIL import Image
import io


st.set_page_config(page_title="A7's Iamge Format Converter", page_icon="🖼️️", layout="wide")


SUPPORTED_FORMATS = ['png', 'jpg', 'jpeg', 'bmp', 'gif', 'tiff', 'ico']

def convert_image(image, target_format):
    if target_format == "ico":

        icon_sizes = [(16, 16), (32, 32), (64, 64)]
        icon_images = [image.resize(size) for size in icon_sizes]

        with io.BytesIO() as output:

            image.save(output, format='ICO', sizes=icon_sizes)
            return output.getvalue()
    else:
        with io.BytesIO() as output:
            image.save(output, format=target_format.upper())
            return output.getvalue()

st.title("A7's Image Format Converter")

if 'converted' not in st.session_state:
    st.session_state.converted = False
if 'converted_image' not in st.session_state:
    st.session_state.converted_image = None
if 'previous_format' not in st.session_state:
    st.session_state.previous_format = None

uploaded_image = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg", "bmp", "gif", "tiff"])

if uploaded_image:
    image = Image.open(uploaded_image)
    
    st.image(image, caption="Uploaded Image", use_container_width=True)  
    
    file_name = uploaded_image.name
    file_size = uploaded_image.size  
    file_format = image.format
    
    st.write(f"**File:** {file_name}")
    st.write(f"**Size:** {file_size / 1024:.2f} KB")  
    st.write(f"**Format:** {file_format}")
    

    target_format = st.selectbox("Select target format", SUPPORTED_FORMATS)

    if st.session_state.previous_format != target_format:
        st.session_state.converted = False  
        st.session_state.converted_image = None  
        st.session_state.previous_format = target_format

    col1, col2 = st.columns([1, 1])
    
    with col1:
        if st.button("Convert"):

            try:
                converted_image = convert_image(image, target_format)
                st.session_state.converted_image = converted_image
                st.session_state.converted_format = target_format
                st.session_state.converted = True
                st.success(f"Image successfully converted to {target_format.upper()} format!")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    

    with col2:
        if st.session_state.converted:
            st.download_button(
                label=f"Download {st.session_state.converted_format.upper()} file",
                data=st.session_state.converted_image,
                file_name=f"converted_image.{st.session_state.converted_format}",
                mime=f"image/{st.session_state.converted_format}"
            )

st.write("---")
st.write(
    "Any suggestions or bugs?\nContact us at:\n"
    "[patnamkannabhiram@gmail.com](mailto:patnamkannabhiram@gmail.com)\n\n"
    "[a7sgarage@gmail.com](mailto:a7sgarage@gmail.com)\n\n"
    "Made by A7 Nostalgic under A7's Garage"
)
