import streamlit as st
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import tempfile
import io


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

.info-box {
    padding: 12px;
    border-radius: 10px;
    background-color: #f0f7ff;
    border: 1px solid #c9def5;
    margin-bottom: 15px;
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
# SPEECH RECOGNITION LANGUAGE CODES
# -------------------------------------------------

speech_languages = {
    "English": "en-US",
    "Telugu": "te-IN",
    "Hindi": "hi-IN",
    "Tamil": "ta-IN",
    "Kannada": "kn-IN",
    "Malayalam": "ml-IN",
    "Bengali": "bn-IN",
    "Marathi": "mr-IN",
    "Gujarati": "gu-IN",
    "Punjabi": "pa-IN",
    "Urdu": "ur-PK",
    "French": "fr-FR",
    "German": "de-DE",
    "Spanish": "es-ES",
    "Italian": "it-IT",
    "Portuguese": "pt-PT",
    "Russian": "ru-RU",
    "Japanese": "ja-JP",
    "Korean": "ko-KR",
    "Chinese": "zh-CN",
    "Arabic": "ar-SA"
}


# -------------------------------------------------
# EXAMPLES FOR NATIVE LANGUAGE INPUT
# -------------------------------------------------

language_examples = {
    "English": "Hello, how are you?",
    "Telugu": "నమస్కారం, మీరు ఎలా ఉన్నారు?",
    "Hindi": "नमस्ते, आप कैसे हैं?",
    "Tamil": "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?",
    "Kannada": "ನಮಸ್ಕಾರ, ನೀವು ಹೇಗಿದ್ದೀರಿ?",
    "Malayalam": "നമസ്കാരം, നിങ്ങൾക്ക് എങ്ങനെയുണ്ട്?",
    "Bengali": "নমস্কার, আপনি কেমন আছেন?",
    "Marathi": "नमस्कार, तुम्ही कसे आहात?",
    "Gujarati": "નમસ્તે, તમે કેમ છો?",
    "Punjabi": "ਸਤ ਸ੍ਰੀ ਅਕਾਲ, ਤੁਸੀਂ ਕਿਵੇਂ ਹੋ?",
    "Urdu": "السلام علیکم، آپ کیسے ہیں؟",
    "French": "Bonjour, comment allez-vous ?",
    "German": "Hallo, wie geht es Ihnen?",
    "Spanish": "Hola, ¿cómo estás?",
    "Italian": "Ciao, come stai?",
    "Portuguese": "Olá, como você está?",
    "Russian": "Здравствуйте, как вы?",
    "Japanese": "こんにちは、お元気ですか？",
    "Korean": "안녕하세요, 어떻게 지내세요?",
    "Chinese": "你好，你怎么样？",
    "Arabic": "مرحباً، كيف حالك؟"
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
    'Translate text instantly between multiple languages using '
    'text or voice input.'
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
# INPUT METHOD
# -------------------------------------------------

st.subheader("📥 Choose Input Method")

input_method = st.radio(
    "How would you like to provide your text?",
    ["⌨️ Type / Paste Text", "🎤 Record Voice"],
    horizontal=True
)


# -------------------------------------------------
# TEXT INPUT
# -------------------------------------------------

text = ""

if input_method == "⌨️ Type / Paste Text":

    st.subheader("📝 Enter Your Text")

    # Information message
    if source_language == "Auto Detect":

        st.markdown(
            '<div class="info-box">'
            '💡 <b>Auto Detect:</b> You can type or paste text '
            'in any supported language. The application will '
            'automatically detect the source language.'
            '</div>',
            unsafe_allow_html=True
        )

    else:

        example = language_examples[source_language]

        st.markdown(
            f'<div class="info-box">'
            f'💡 <b>Input language:</b> {source_language}<br>'
            f'You can type or paste text using the '
            f'{source_language} script.<br><br>'
            f'<b>Example:</b> {example}'
            f'</div>',
            unsafe_allow_html=True
        )

    text = st.text_area(
        "Type or paste text in your selected source language:",
        height=180,
        placeholder=(
            "Type or paste text here..."
        )
    )

    if text:

        st.caption(
            f"Characters: {len(text)}"
        )


# -------------------------------------------------
# VOICE INPUT
# -------------------------------------------------

elif input_method == "🎤 Record Voice":

    st.subheader("🎤 Record Your Voice")

    if source_language == "Auto Detect":

        st.warning(
            "⚠️ For voice input, please select the "
            "language you are going to speak. "
            "Auto Detect is currently available for "
            "typed/pasted text."
        )

    else:

        st.info(
            f"🎤 Speak in {source_language}. "
            f"The recording will be converted into "
            f"{source_language} text before translation."
        )

    audio_value = st.audio_input(
        "Click the microphone to record"
    )

    if audio_value is not None:

        st.audio(
            audio_value,
            format="audio/wav"
        )

        recognizer = sr.Recognizer()

        try:

            audio_bytes = audio_value.getvalue()

            audio_file = io.BytesIO(audio_bytes)

            with sr.AudioFile(audio_file) as source:

                audio_data = recognizer.record(source)

            if source_language == "Auto Detect":

                text = ""

            else:

                recognition_language = speech_languages[
                    source_language
                ]

                with st.spinner(
                    f"Converting {source_language} speech to text..."
                ):

                    text = recognizer.recognize_google(
                        audio_data,
                        language=recognition_language
                    )

                st.success(
                    "✅ Speech converted to text successfully!"
                )

                st.subheader("📝 Recognized Text")

                st.text_area(
                    "Your recorded speech:",
                    value=text,
                    height=120,
                    disabled=True
                )

        except sr.UnknownValueError:

            st.error(
                "❌ Sorry, I could not understand the audio. "
                "Please speak clearly and try again."
            )

            text = ""

        except sr.RequestError:

            st.error(
                "❌ Speech recognition service is unavailable. "
                "Please check your internet connection."
            )

            text = ""

        except Exception as e:

            st.error(
                f"❌ Could not process the audio: {str(e)}"
            )

            text = ""


# -------------------------------------------------
# TRANSLATE BUTTON
# -------------------------------------------------

if st.button(
    "🚀 Translate",
    use_container_width=True
):

    # Empty input
    if not text.strip():

        st.warning(
            "⚠️ Please enter text or record your voice "
            "before translating."
        )

    # Same language
    elif (
        source_language != "Auto Detect"
        and source_language == target_language
    ):

        st.info(
            "ℹ️ Source and target languages are the same."
        )

    # Voice + Auto Detect
    elif (
        input_method == "🎤 Record Voice"
        and source_language == "Auto Detect"
    ):

        st.warning(
            "⚠️ Please select the language you are "
            "speaking before using voice input."
        )

    else:

        try:

            with st.spinner("Translating..."):

                # Auto detection for typed text
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

            st.success(
                "✅ Translation completed successfully!"
            )

            st.subheader("🔄 Translated Text")

            st.markdown(
                f'<div class="result-box">'
                f'{translated_text}'
                f'</div>',
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

                tts_language = languages[target_language]

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


        except Exception:

            st.error(
                "❌ Translation failed. "
                "Please check your internet connection "
                "and try again."
            )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------

st.markdown(
    '<div class="footer">'
    'CodeAlpha AI Internship • Task 1 • '
    'Language Translation Tool'
    '</div>',
    unsafe_allow_html=True
)