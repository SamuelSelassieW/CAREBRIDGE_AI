def check_maternal_risk(data):

    emergency_reasons = []
    warning_reasons = []
    risk_score = 0

    # 🔴 EMERGENCY CHECKS
    if data["severe_bleeding"]:
        emergency_reasons.append("Severe vaginal bleeding")

    if data["convulsions"]:
        emergency_reasons.append("Convulsions")

    if data["severe_headache_blur"]:
        emergency_reasons.append("Severe headache with blurred vision")

    if data["severe_abdominal_pain"]:
        emergency_reasons.append("Severe abdominal pain")

    if data["fever_weak"]:
        emergency_reasons.append("Severe infection symptoms")

    if data["difficulty_breathing"]:
        emergency_reasons.append("Difficulty breathing")

    if data["systolic_bp"] >= 160 or data["diastolic_bp"] >= 110:
        emergency_reasons.append("Severe hypertension (≥160/110)")

    # ✅ EMERGENCY OVERRIDE
    if emergency_reasons:
        return {
            "risk_level": "EMERGENCY",
            "risk_score": 100,  # ✅ Always include this
            "action": "Immediate referral required.",
            "reasons": emergency_reasons
        }

    # 🟡 SCORING
    if data["systolic_bp"] >= 140 or data["diastolic_bp"] >= 90:
        warning_reasons.append("High blood pressure (≥140/90)")
        risk_score += 3

    if data.get("face_and_or_hand_swelling", False):
        warning_reasons.append("Swelling of face or hands")
        risk_score += 2

    if data["reduced_fetal_movement"]:
        warning_reasons.append("Reduced fetal movement")
        risk_score += 3

    if data["leaking_fluid"]:
        warning_reasons.append("Possible leaking amniotic fluid")
        risk_score += 3

    if data["severe_anemia_signs"]:
        warning_reasons.append("Signs of severe anemia")
        risk_score += 2

    if data["persistent_vomiting"]:
        warning_reasons.append("Persistent vomiting")
        risk_score += 1

    # ✅ Risk classification
    if risk_score >= 6:
        level = "HIGH RISK"
        action = "Urgent clinical review required."
    elif risk_score >= 3:
        level = "MODERATE RISK"
        action = "Same-day monitoring and follow-up."
    else:
        level = "LOW RISK"
        action = "Continue routine antenatal care."

    return {
        "risk_level": level,
        "risk_score": risk_score,  # ✅ Always returned
        "action": action,
        "reasons": warning_reasons if warning_reasons else ["No danger signs detected"]
    }