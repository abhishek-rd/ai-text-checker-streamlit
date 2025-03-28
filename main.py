import requests
import streamlit as st

# Configure the page
st.set_page_config(
    page_title="AI Text Detector",
    page_icon="🤖",
    layout="centered"
)


# # Custom CSS
# def load_css():
#     with open("static/style.css") as f:
#         st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def detect_ai_text(text):
    # Replace with your actual API endpoint
    api_url = "https://shakii-textdetectextension.hf.space/predict"

    try:
        response = requests.post(
            api_url,
            json={"text": text},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to API: {str(e)}")
        return None


def main():
    # Load custom CSS
    # load_css()

    st.title("🤖 AI Text Detector")
    st.write("Detect whether text is AI-generated or human-written")

    # Text input area
    text_input = st.text_area(
        "Enter your text here:",
        height=200,
        placeholder="Paste your text here to analyze..."
    )

    # Analysis button
    if st.button("Analyze Text"):
        if not text_input.strip():
            st.warning("Please enter some text to analyze.")
            return

        with st.spinner("Analyzing text..."):
            result = detect_ai_text(text_input)

        if result:
            # Create columns for results
            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    label="Human Probability",
                    value=f"{result['human_probability']}%"
                )

            with col2:
                st.metric(
                    label="AI Probability",
                    value=f"{result['ai_probability']}%"
                )

            # Display the final prediction
            prediction = result['prediction']
            if prediction == "AI-generated":
                st.warning(f"📊 Verdict: {prediction}")
            else:
                st.success(f"📊 Verdict: {prediction}")


if __name__ == "__main__":
    main()
