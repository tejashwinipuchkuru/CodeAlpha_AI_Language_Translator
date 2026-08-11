import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile


# -------------------------------------------------
# PAGE CONFIGURATION
# -------------------------------------------------

st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐",
    layout="wide"
)


# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------

st.markdown("""
<style>

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 5px;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #666;
    margin-bottom: 30px;
}

.result-box {
    padding: 20px;
    border-radius: 12px;
    background-color: #f5f7ff;
    border: 1px solid #ddd;
    min-height: 100px;
    font-size: 20px;
}

.footer {
    text-align: center;
    color: #777;
    margin-top: 40px;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# SUPPORTED LANGUAGES
# -------------------------------------------------

languages = {
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "French": "fr",
    "German": "de",
    "Spanish": "es",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh-CN",
    "Arabic": "ar"
}


# -------------------------------------------------
# HEADER
# -------------------------------------------------

st.markdown(
    '<div class="title">🌐 AI Language Translator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Translate text instantly between multiple languages using AI-powered translation.'
    '</div>',
    unsafe_allow_html=True
)


# -------------------------------------------------
# LANGUAGE SELECTION
# -------------------------------------------------

col1, col2 = st.columns(2)

with col1:
    source_language = st.selectbox(
        "🔤 Source Language",
        ["Auto Detect"] + list(languages.keys())
    )

with col2:
    target_language = st.selectbox(
        "🌍 Target Language",
        list(languages.keys())
    )


# -------------------------------------------------
# TEXT INPUT
# -------------------------------------------------

st.subheader("📝 Enter Your Text")

text = st.text_area(
    "Type or paste your text below:",
    height=180,
    placeholder="Example: Hello, how are you?"
)

if text:
    st.caption(f"Characters: {len(text)}")


# -------------------------------------------------
# TRANSLATE BUTTON
# -------------------------------------------------

if st.button("🚀 Translate", use_container_width=True):

    # Check empty input
    if not text.strip():

        st.warning("⚠️ Please enter some text before translating.")

    # Check same language
    elif (
        source_language != "Auto Detect"
        and source_language == target_language
    ):

        st.info("ℹ️ Source and target languages are the same.")

    else:

        try:

            with st.spinner("Translating..."):

                # Auto-detect source language
                if source_language == "Auto Detect":

                    translator = GoogleTranslator(
                        source="auto",
                        target=languages[target_language]
                    )

                # Selected source language
                else:

                    translator = GoogleTranslator(
                        source=languages[source_language],
                        target=languages[target_language]
                    )

                translated_text = translator.translate(text)

            # -------------------------------------------------
            # TRANSLATION RESULT
            # -------------------------------------------------

            st.success("✅ Translation completed successfully!")

            st.subheader("🔄 Translated Text")

            st.markdown(
                f'<div class="result-box">{translated_text}</div>',
                unsafe_allow_html=True
            )

            # -------------------------------------------------
            # COPY FEATURE
            # -------------------------------------------------

            st.write("📋 **Copy Translation**")

            st.code(
                translated_text,
                language=None
            )

            # -------------------------------------------------
            # TEXT TO SPEECH
            # -------------------------------------------------

            st.write("🔊 **Listen to Translation**")

            try:

                # gTTS uses standard language codes
                tts_language = languages[target_language]

                # Some language codes need adjustment
                if tts_language == "zh-CN":
                    tts_language = "zh-CN"

                speech = gTTS(
                    text=translated_text,
                    lang=tts_language
                )

                audio_file = tempfile.NamedTemporaryFile(
                    delete=False,
                    suffix=".mp3"
                )

                speech.save(audio_file.name)

                st.audio(
                    audio_file.name,
                    format="audio/mp3"
                )

            except Exception:

                st.info(
                    "🔊 Text-to-speech is not available "
                    "for this language."
                )

        except Exception as e:

            st.error(
                "❌ Translation failed. "
                "Please check your internet connection and try again."
            )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown(
    '<div class="footer">'
    'CodeAlpha AI Internship • Task 1 • Language Translation Tool'
    '</div>',
    unsafe_allow_html=True
)