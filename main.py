import streamlit as st
from PIL import Image
import random
import time


st.set_page_config(layout="wide")


# Function to simulate processing
def simulate_processing(duration=10):
    """
    Simulates a process with a progress bar.
    """
    with st.spinner("Generating colored variations..."):
        progress_bar = st.progress(0)
        progress = 0
        while progress < 100:
            time_increment = random.uniform(0.1, 0.3)
            progress_increment = random.randint(5, 15)
            time.sleep(time_increment)
            progress = min(progress + progress_increment, 100)
            progress_bar.progress(progress)


# Function to mock the generation of colored images
def generate_colored_variations(image, num_variations=3):
    """
    Generates multiple colored variations of a hand-drawn image.
    For now, it simply applies random color tints as placeholders.
    """
    variations = []
    for _ in range(num_variations):
        colored_image = image.convert("RGB")  # Convert to RGB
        # Apply random tint by modifying pixel values (placeholder logic)
        tinted_image = colored_image.copy()
        pixels = tinted_image.load()
        for i in range(tinted_image.size[0]):
            for j in range(tinted_image.size[1]):
                r, g, b = pixels[i, j]
                pixels[i, j] = (
                    min(r + random.randint(0, 50), 255),
                    min(g + random.randint(0, 50), 255),
                    min(b + random.randint(0, 50), 255),
                )
        variations.append(tinted_image)
    return variations


# Function to resize images for display
def resize_image(image, max_width):
    """
    Resizes the image to fit within a specified width while maintaining the aspect ratio.
    """
    aspect_ratio = image.size[1] / image.size[0]
    new_width = max_width
    new_height = int(new_width * aspect_ratio)
    return image.resize((new_width, new_height))


# Main Streamlit app
def main():
    # Header
    st.header("Hand-Drawn to Colored Images", divider="gray")

    # Split the layout into two columns
    left_col, right_col = st.columns(
        [1, 2]
    )  # Left column is 1x, right column is 2x wider

    # Left column: Input and display the hand-drawn image
    with left_col:
        st.markdown("### Upload Your Hand-Drawn Image")
        uploaded_file = st.file_uploader(
            "Supported file types: JPG, JPEG, PNG", type=["jpg", "jpeg", "png"]
        )
        if uploaded_file is not None:
            hand_drawn_image = Image.open(uploaded_file)
            resized_hand_drawn = resize_image(hand_drawn_image, max_width=300)
            file_name = uploaded_file.name[0]
            st.markdown("#### Uploaded Image")
            st.image(
                resized_hand_drawn,
                caption="Hand-Drawn Image",
                use_container_width=False,
            )

    # Right column: Display colored variations
    with right_col:
        if uploaded_file is not None:
            # Simulate processing
            simulate_processing()

            # Generate multiple colored variations
            num_variations = 4
            colored_variations = generate_colored_variations(
                hand_drawn_image, num_variations=num_variations
            )

            # Display results in a grid layout
            st.markdown("### Colored Variations")
            cols = st.columns(4)  # Display two variations per row
            for idx, _ in enumerate(colored_variations):
                with cols[idx]:
                    image = Image.open(f"./{file_name}/image_{idx}.png")
                    width, height = image.size
                    image = image.crop((width // 2, 0, width, height))
                    image = resize_image(image, max_width=200)
                    st.image(
                        image,
                        caption=f"Variation {idx + 1}",
                        # use_container_width=True,
                    )

        else:
            st.info("Upload an image on the left to see the colored variations here.")

    # Footer
    st.markdown(
        """
        <hr style='border: 1px solid #ddd;'>
        <p style='text-align: center; font-size: 14px; color: #888;'>Built with ❤️ using Streamlit</p>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
