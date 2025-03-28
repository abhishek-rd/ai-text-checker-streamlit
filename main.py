import requests
import streamlit as st

# Configure the page
st.set_page_config(
    page_title="AI Text Detector",
    page_icon="🤖",
    layout="centered"
)


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
    # Initialize session state for history if it doesn't exist
    if 'history' not in st.session_state:
        st.session_state.history = []

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

            # Store the result in history
            st.session_state.history.append({
                'text': text_input[:100] + "..." if len(text_input) > 100 else text_input,
                'prediction': prediction,
                'human_prob': result['human_probability'],
                'ai_prob': result['ai_probability']
            })

    # Display history section
    if st.session_state.history:
        st.markdown("---")
        st.subheader("Previous Analysis Results")
        for i, entry in enumerate(st.session_state.history, 1):
            with st.expander(f"Analysis #{i}"):
                st.text(f"Text: {entry['text']}")
                st.text(f"Verdict: {entry['prediction']}")
                col1, col2 = st.columns(2)
                with col1:
                    st.text(f"Human Probability: {entry['human_prob']}%")
                with col2:
                    st.text(f"AI Probability: {entry['ai_prob']}%")


if __name__ == "__main__":
    main()
