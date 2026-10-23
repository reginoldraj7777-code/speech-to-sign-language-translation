"""Run with: streamlit run src/app.py"""

import json
import sys
import tempfile
from pathlib import Path

import streamlit as st

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.pipeline import LANGUAGES, Lexicon, SpeechRecognizer

st.set_page_config(
    page_title="Speech to Sign • Research Studio", page_icon="🤟", layout="wide"
)
st.markdown(
    """<style>.stApp {background:#f6f9fb;} h1 {color:#123945;letter-spacing:-1px;} div[data-testid="stMetric"] {background:white;border:1px solid #dce6eb;padding:18px;border-radius:12px;} .stButton>button {border-radius:9px;} </style>""",
    unsafe_allow_html=True,
)
st.caption("SPEECH TO SIGN  /  RESEARCH STUDIO")
st.title("Make a message easier to follow.")
st.write(
    "Turn a short message into an inspectable sequence of concepts. Review the transcript, see every match, and keep unknown words visible."
)
lexicon = Lexicon()
inventory = lexicon.inventory()
a, b, c = st.columns(3)
a.metric("Input languages", len(LANGUAGES))
b.metric("Authored concepts", inventory["concepts"])
c.metric("Registered sign assets", inventory["distinct_usable_assets"])
if not inventory["distinct_usable_assets"]:
    st.info(
        "This version displays glosses. Add licensed, expert-reviewed sign media to enable playback. No gesture collection is bundled."
    )
left, right = st.columns([1, 1.2], gap="large")
with left:
    st.subheader("1 · Prepare your message")
    language = st.selectbox(
        "Input language", list(LANGUAGES), format_func=LANGUAGES.get
    )
    samples = {
        "en": "Hello! Please help. I need water. Thank you.",
        "ta": "வணக்கம் தயவு செய்து உதவி தண்ணீர் நன்றி",
        "de": "Hallo! Bitte Hilfe. Ich brauche Wasser. Danke.",
    }
    text = st.text_area(
        "Message", value=samples[language], height=150, key=f"message_{language}"
    )
    with st.expander("Use your voice"):
        mode = st.radio("Audio source", ["Record a clip", "Upload audio"])
        audio = (
            st.audio_input("Record a short message")
            if mode == "Record a clip"
            else st.file_uploader(
                "Audio file", type=["wav", "mp3", "m4a", "flac", "ogg"]
            )
        )
        model_name = st.selectbox("Transcription model", ["tiny", "base", "small"])
        st.caption(
            "Runs on CPU. The first transcription downloads model weights. Audio stays with this app process; no external transcription API is used."
        )

        @st.cache_resource
        def recognizer(name):
            return SpeechRecognizer(name)

        if st.button("Transcribe audio", disabled=audio is None):
            if audio.size > 20 * 1024 * 1024:
                st.error("Please use an audio file smaller than 20 MB.")
            else:
                try:
                    with (
                        st.spinner("Preparing model and transcribing…"),
                        tempfile.TemporaryDirectory() as folder,
                    ):
                        path = Path(folder) / "input_audio"
                        path.write_bytes(audio.getvalue())
                        result = recognizer(model_name).transcribe(path, language)
                    st.session_state["transcription"] = {**result, "language": language}
                except Exception as exc:
                    st.error(f"Transcription could not complete: {exc}")
        transcript = st.session_state.get("transcription")
        if transcript and transcript["language"] == language:
            st.write(transcript["text"])
            st.caption(
                f"{transcript['processing_seconds']:.2f} seconds processing / {transcript['audio_seconds']:.1f} seconds audio"
            )
            if st.checkbox("Use this transcript for retrieval"):
                text = transcript["text"]
with right:
    st.subheader("2 · Inspect the concept sequence")
    results = lexicon.translate(text, language)
    if not results:
        st.write("Enter a message to begin.")
    for index, result in enumerate(results, 1):
        with st.container(border=True):
            st.markdown(f"**{index:02d} · {result['gloss'] or 'Needs clarification'}**")
            st.caption(result["source"])
            if result["asset"]:
                if Path(result["asset"]).suffix.lower() in {".mp4", ".webm"}:
                    st.video(result["asset"])
                else:
                    st.image(result["asset"])
            elif result["status"] == "unmapped":
                st.warning("No concept matched. Rephrase or add a reviewed mapping.")
            else:
                st.caption("Gloss only · sign media not registered")
    st.download_button(
        "Download retrieval trace",
        json.dumps(
            {"language": language, "message": text, "results": results},
            ensure_ascii=False,
            indent=2,
        ),
        "retrieval_trace.json",
        "application/json",
    )
st.divider()
st.caption(
    "Research prototype · Phrase matching is not sign-language grammar. Concept labels are not validated gestures. The interface records complete clips; the Python chunk protocol is separate from live microphone streaming."
)
