import re
import speech_recognition as sr
from gtts import gTTS
import tempfile
import os



# =====================================================
# 🎤 VOICE CAPTURE
# =====================================================

def capture_voice_input():
    """
    Captures speech and converts to text.
    Uses English engine but supports Dagbani keyword detection later.
    """

    recognizer = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=15)

        text = recognizer.recognize_google(audio, language="en-US")
        return text.lower().strip()

    except (
        sr.WaitTimeoutError,
        sr.UnknownValueError,
        sr.RequestError,
        OSError
    ):
        return ""


# =====================================================
# 🌍 SIMPLE LANGUAGE DETECTION (Heuristic)
# =====================================================

def detect_language(text):
    """
    Simple heuristic detection:
    If Dagbani keywords are present → return 'dag'
    Else → return 'en'
    """

    dagbani_keywords = [
        "zim", "tuuli", "nyɔŋi", "pam", "ka dii suŋ",
        "biihi", "laafi", "chahi"
    ]

    for word in dagbani_keywords:
        if word in text:
            return "dag"

    return "en"


# =====================================================
# 🔢 BLOOD PRESSURE PARSING
# =====================================================

def extract_blood_pressure(text):

    numeric_pattern = r"\b(\d{2,3})\s*(?:over|/|by)\s*(\d{2,3})\b"
    numeric_match = re.search(numeric_pattern, text)

    if numeric_match:
        systolic = int(numeric_match.group(1))
        diastolic = int(numeric_match.group(2))
        return systolic, diastolic

    return None, None


# =====================================================
# 🧠 SYMPTOM EXTRACTION (ENGLISH + DAGBANI)
# =====================================================

def extract_symptoms_from_text(text):

    text = (text or "").lower().strip()

    extracted_data = {
        # Maternal
        "severe_bleeding": False,
        "convulsions": False,
        "persistent_vomiting": False,
        "face_and_or_hand_swelling": False,

        # Newborn
        "not_feeding": False,
        "fast_breathing": False,
        "chest_indrawing": False,
        "lethargic": False,
        "fever": False,

        # Nutrition
        "weight_loss": False,
        "poor_appetite": False,
        "muac": None,

        # BP
        "systolic_bp": None,
        "diastolic_bp": None
    }

    if not text:
        return extracted_data

    # -------------------------
    # ENGLISH MATERNAL
    # -------------------------

    if "bleeding" in text:
        extracted_data["severe_bleeding"] = True

    if "convulsion" in text or "fit" in text:
        extracted_data["convulsions"] = True

    if "vomiting" in text:
        extracted_data["persistent_vomiting"] = True

    if "swelling" in text:
        extracted_data["face_and_or_hand_swelling"] = True

    # -------------------------
    # DAGBANI MATERNAL
    # -------------------------

    if "zim" in text:
        extracted_data["severe_bleeding"] = True

    if "tuuli" in text:
        extracted_data["persistent_vomiting"] = True

    if "nyɔŋi" in text or "nyongi" in text:
        extracted_data["face_and_or_hand_swelling"] = True

    # -------------------------
    # NEWBORN ENGLISH
    # -------------------------

    if "not feeding" in text:
        extracted_data["not_feeding"] = True

    if "fast breathing" in text:
        extracted_data["fast_breathing"] = True

    if "chest indrawing" in text:
        extracted_data["chest_indrawing"] = True

    if "lethargic" in text or "unconscious" in text:
        extracted_data["lethargic"] = True

    if "fever" in text:
        extracted_data["fever"] = True

    # -------------------------
    # NEWBORN DAGBANI
    # -------------------------

    if "biihi ka dii" in text:
        extracted_data["not_feeding"] = True

    if "biihi ka nɔŋ" in text:
        extracted_data["lethargic"] = True

    if "laafi niŋ pam" in text:
        extracted_data["fever"] = True

    # -------------------------
    # NUTRITION
    # -------------------------

    if "losing weight" in text or "pam" in text:
        extracted_data["weight_loss"] = True

    if "poor appetite" in text or "ka dii suŋ" in text:
        extracted_data["poor_appetite"] = True

    muac_match = re.search(r"\b(\d{1,2}\.?\d?)\b", text)
    if muac_match:
        muac_value = float(muac_match.group(1))
        if 5 <= muac_value <= 20:
            extracted_data["muac"] = muac_value

    # -------------------------
    # BP
    # -------------------------

    systolic, diastolic = extract_blood_pressure(text)

    if systolic and diastolic:
        extracted_data["systolic_bp"] = systolic
        extracted_data["diastolic_bp"] = diastolic

    return extracted_data


# =====================================================
# 🔊 TEXT TO SPEECH
# =====================================================

def speak_text(text, language="en"):
    """
    Converts text to speech using gTTS.
    """

    try:
        lang_code = "en"

        # gTTS does not officially support Dagbani
        # So we fallback to English voice for now
        if language == "dag":
            lang_code = "en"

        tts = gTTS(text=text, lang=lang_code)

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            temp_path = fp.name

        tts.save(temp_path)

        return temp_path

    except Exception:
        return None