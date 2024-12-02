import streamlit as st
from PIL import Image
import time
import os
import random

# Path to the predefined output image
OUTPUT_IMAGE_PATH = "./image(1).png"  # Replace with the actual file path


def resize_image(image, max_width):
    """
    Resizes the image to have a maximum width while maintaining aspect ratio.
    """
    aspect_ratio = image.size[1] / image.size[0]
    new_width = max_width
    new_height = int(new_width * aspect_ratio)
    image.thumbnail((new_width, new_height))
    return image


def simulate_processing(duration=10):
    """
    Simulates processing by updating the progress bar with random time increments.
    """
    progress_bar = st.progress(0)
    progress = 0
    while progress < 100:
        time_increment = random.uniform(
            0.1, 0.5
        )  # Random time step between 0.1 and 0.5 seconds
        progress_increment = random.randint(
            1, 3
        )  # Random progress step between 5% and 15%
        time.sleep(time_increment)
        progress = min(
            progress + progress_increment, 100
        )  # Ensure progress doesn't exceed 100
        progress_bar.progress(progress)


def main():
    st.title("Image Viewer: Hand-drawn to Real")

    # Step 1: Upload the hand-drawn image
    uploaded_file = st.file_uploader(
        "Upload a Hand-drawn Image", type=["jpg", "jpeg", "png"]
    )

    if uploaded_file is not None:
        # Load and resize the uploaded image
        hand_drawn_image = Image.open(uploaded_file)
        hand_drawn_image = resize_image(
            hand_drawn_image, max_width=300
        )  # Adjust width as needed for display

        # Display the resized uploaded image immediately
        st.subheader("Your Hand-drawn Image")
        st.image(
            hand_drawn_image, caption="Hand-drawn Image", use_container_width=False
        )

        # Step 2: Simulate processing with a realistic progress bar
        st.subheader("Processing your hand-drawn image...")
        simulate_processing()

        # Load and resize the predefined real image after processing
        real_image = Image.open(OUTPUT_IMAGE_PATH)
        real_image = resize_image(real_image, max_width=300)  # Adjust width as needed

        # Step 3: Display images side by side in a row
        st.subheader("Real Image Based on Your Drawing")
        cols = st.columns(2)  # Create two equal-width columns
        with cols[0]:
            st.image(
                hand_drawn_image, caption="Hand-drawn Image", use_container_width=False
            )
        with cols[1]:
            st.image(real_image, caption="Real Image", use_container_width=False)


if __name__ == "__main__":
    main()
