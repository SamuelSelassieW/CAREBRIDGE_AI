import streamlit as st
from nutrition_engine import generate_nutrition_guidance
from maternal_risk_engine import check_maternal_risk
from child_risk_engine import assess_child_risk
from chatbot_layer import generate_chatbot_response
from database import init_db, save_patient, save_nutrition
from referral import generate_referral_message
from voice_input import capture_voice_input, extract_symptoms_from_text
from translations import translations


# ==================================================
# PAGE CONFIG
# ==================================================

st.set_page_config(
    page_title="CareBridge AI",
    page_icon="🏥",
    layout="wide"
)

init_db()


# ==================================================
# TRANSLATION SYSTEM
# ==================================================

if "language" not in st.session_state:
    st.session_state.language = "en"

def t(key):
    lang = st.session_state.get("language", "en")
    return translations.get(lang, {}).get(key, key)


# ==================================================
# LANGUAGE SELECTOR
# ==================================================

selected_language = st.selectbox(
    "🌍 Select Language",
    ["English", "Dagbani"]
)

st.session_state.language = "en" if selected_language == "English" else "dag"


# ==================================================
# SESSION INITIALIZATION
# ==================================================

if "active_module" not in st.session_state:
    st.session_state.active_module = None

maternal_fields = [
    "severe_bleeding",
    "convulsions",
    "severe_headache_blur",
    "severe_abdominal_pain",
    "fever_weak",
    "difficulty_breathing",
    "face_and_or_hand_swelling",
    "reduced_fetal_movement",
    "leaking_fluid",
    "severe_anemia_signs",
    "persistent_vomiting"
]

for field in maternal_fields:
    if field not in st.session_state:
        st.session_state[field] = False

if "systolic_bp" not in st.session_state:
    st.session_state.systolic_bp = 0

if "diastolic_bp" not in st.session_state:
    st.session_state.diastolic_bp = 0

if "weight_loss" not in st.session_state:
    st.session_state.weight_loss = False

if "poor_appetite" not in st.session_state:
    st.session_state.poor_appetite = False

if "muac" not in st.session_state:
    st.session_state.muac = 12.5


# ==================================================
# RESET FUNCTION
# ==================================================

def reset_to_dashboard():
    st.session_state.clear()
    st.session_state.active_module = None
    st.rerun()


# ==================================================
# CLEAN IMAGE STYLE (Rounded Only)
# ==================================================

st.markdown("""
<style>
.dashboard-img img {
    border-radius: 24px;
}
.stButton > button {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# HEADER
# ==================================================

st.title("🏥 " + t("app_title"))
st.markdown(
    "AI-powered maternal, newborn and child health decision support system "
    "for CHPS workers in Northern Ghana."
)
st.divider()


# ==================================================
# DASHBOARD (Large Square Images)
# ==================================================

if st.session_state.active_module is None:

    col1, col2, col3 = st.columns(3)

    image_size = 420  # ✅ Bigger square

    # ---------- Maternal ----------
    with col1:
        st.markdown('<div class="dashboard-img">', unsafe_allow_html=True)
        st.image(
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTPNFl9jz4yo965MsXQ2CeklXAs6-PIBpMuV-ZiHClvdQ&s=10",
            width=image_size
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader(" " + t("maternal_module"))

        if st.button(t("open_maternal")):
            st.session_state.active_module = "maternal"
            st.rerun()

    # ---------- Newborn ----------
    with col2:
        st.markdown('<div class="dashboard-img">', unsafe_allow_html=True)
        st.image(
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQyqgtVVF1rj6m5k4XlMJv-ozyZvTa7PJWod6YdvhaHHg&s=10",
            width=image_size
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader("Newborn & Under‑5 Risk")

        if st.button("OPEN CHILD RISK MODULE"):
            st.session_state.active_module = "child"
            st.rerun()

    # ---------- Nutrition ----------
    with col3:
        st.markdown('<div class="dashboard-img">', unsafe_allow_html=True)
        st.image(
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRSSK5a5wqzlZjgV_geg4kZ1D7KSGWQ6i8a_eixYFL51Q&s=10",
            width=image_size
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.subheader(" " + t("nutrition_module"))

        if st.button(t("open_nutrition")):
            st.session_state.active_module = "nutrition"
            st.rerun()


# ==================================================
# MATERNAL MODULE
# ==================================================

elif st.session_state.active_module == "maternal":

    st.button("⬅ " + t("back_dashboard"), on_click=reset_to_dashboard)
    st.header("🤰 " + t("maternal_module"))

    st.subheader("🎤 Voice Input")

    if st.button(t("capture_voice")):
        voice_text = capture_voice_input()

        if voice_text:
            st.info(f"Recognized: {voice_text}")
            extracted = extract_symptoms_from_text(voice_text)

            for key, value in extracted.items():
                if key in maternal_fields and value is True:
                    st.session_state[key] = True

                if key == "systolic_bp" and value:
                    st.session_state.systolic_bp = int(value)

                if key == "diastolic_bp" and value:
                    st.session_state.diastolic_bp = int(value)

            st.rerun()
        else:
            st.warning("No speech recognized.")

    patient_name = st.text_input(t("patient_name"))
    facility_name = st.text_input(t("referral_facility"))
    facility_contact = st.text_input(t("facility_contact"))

    st.number_input(t("systolic_bp"), 0, 300, key="systolic_bp")
    st.number_input(t("diastolic_bp"), 0, 200, key="diastolic_bp")

    st.markdown("### " + t("danger_signs"))

    for field in maternal_fields:
        st.checkbox(field.replace("_", " ").title(), key=field)

    if st.button(t("run_maternal")):

        patient_data = {field: st.session_state[field] for field in maternal_fields}
        patient_data["systolic_bp"] = st.session_state.systolic_bp
        patient_data["diastolic_bp"] = st.session_state.diastolic_bp

        result = check_maternal_risk(patient_data)
        referred = result["risk_level"].upper() == "EMERGENCY"

        referral_message = ""
        if referred:
            referral_message = generate_referral_message(
                name=patient_name,
                result=result,
                facility_name=facility_name,
                facility_contact=facility_contact
            )

        save_patient(
            name=patient_name,
            risk_level=result["risk_level"],
            risk_score=result["risk_score"],
            referred=referred,
            patient_data=patient_data,
            referral_message=referral_message
        )

        response = generate_chatbot_response(result, patient_name)

        risk_level = result["risk_level"].upper()

        if risk_level == "EMERGENCY":
            st.error("🚨 " + t("emergency"))
        elif "HIGH" in risk_level:
            st.error("🔴 " + t("high_risk"))
        elif "MODERATE" in risk_level:
            st.warning("🟡 " + t("moderate_risk"))
        else:
            st.success("🟢 " + t("low_risk"))

        st.markdown(response)

        if referred:
            st.code(referral_message)


# ==================================================
# NUTRITION MODULE
# ==================================================

elif st.session_state.active_module == "nutrition":

    st.button("⬅ " + t("back_dashboard"), on_click=reset_to_dashboard)
    st.header("🥗 " + t("nutrition_module"))

    st.subheader("🎤 Voice Input")

    if st.button(t("capture_voice")):
        voice_text = capture_voice_input()

        if voice_text:
            st.info(f"Recognized: {voice_text}")
            extracted = extract_symptoms_from_text(voice_text)

            if extracted.get("weight_loss"):
                st.session_state.weight_loss = True

            if extracted.get("poor_appetite"):
                st.session_state.poor_appetite = True

            if extracted.get("muac"):
                st.session_state.muac = float(extracted["muac"])

            st.rerun()
        else:
            st.warning("No speech recognized.")

    child_name = st.text_input(t("child_name"))
    age_months = st.number_input(t("child_age"), 0, 60)
    st.number_input(t("muac"), 5.0, 20.0, step=0.1, key="muac")

    st.checkbox(t("weight_loss"), key="weight_loss")
    st.checkbox(t("poor_appetite"), key="poor_appetite")

    if st.button(t("generate_nutrition")):

        nutrition_result = generate_nutrition_guidance(
            age_months=age_months,
            muac=st.session_state.muac,
            weight_loss=st.session_state.weight_loss,
            poor_appetite=st.session_state.poor_appetite
        )

        referral_needed = nutrition_result["referral_needed"]

        for line in nutrition_result["advice"]:
            st.write(line)

        save_nutrition(
            child_name=child_name,
            age_months=age_months,
            muac=st.session_state.muac,
            malnutrition_level=nutrition_result["malnutrition_level"],
            referred=referral_needed
        )

        if referral_needed:
            st.warning("⚠️ " + t("referral_needed"))


# ==================================================
# CHILD RISK MODULE
# ==================================================

elif st.session_state.active_module == "child":

    st.button("⬅ " + t("back_dashboard"), on_click=reset_to_dashboard)
    st.header("👶 Newborn & Under‑5 Risk Assessment")

    age_days = st.number_input("Child Age (days)", 0, 2000)

    not_feeding = st.checkbox("Not feeding well")
    convulsions = st.checkbox("Convulsions")
    fast_breathing = st.checkbox("Fast breathing")
    chest_indrawing = st.checkbox("Chest indrawing")
    fever = st.checkbox("Fever")
    low_temp = st.checkbox("Low body temperature")
    severe_diarrhea = st.checkbox("Severe diarrhea")
    blood_in_stool = st.checkbox("Blood in stool")
    lethargic = st.checkbox("Lethargic / unconscious")

    if st.button("Run Child Risk Assessment"):

        result = assess_child_risk(
            age_days,
            not_feeding,
            convulsions,
            fast_breathing,
            chest_indrawing,
            fever,
            low_temp,
            severe_diarrhea,
            blood_in_stool,
            lethargic
        )

        if result["risk_level"] == "EMERGENCY":
            st.error("🚨 " + t("emergency"))
        else:
            st.success("🟢 " + t("low_risk"))

        for reason in result["reasons"]:
            st.write("- " + reason)

        st.info(result["action"])