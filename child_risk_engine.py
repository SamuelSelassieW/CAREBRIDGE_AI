def assess_child_risk(age_days,
                      not_feeding,
                      convulsions,
                      fast_breathing,
                      chest_indrawing,
                      fever,
                      low_temp,
                      severe_diarrhea,
                      blood_in_stool,
                      lethargic):

    emergency_reasons = []

    # --------------------------------------------------
    # NEWBORN (0–28 days)
    # --------------------------------------------------
    if age_days <= 28:

        if not_feeding:
            emergency_reasons.append("Not feeding well")

        if convulsions:
            emergency_reasons.append("Convulsions")

        if fast_breathing:
            emergency_reasons.append("Fast breathing")

        if chest_indrawing:
            emergency_reasons.append("Severe chest indrawing")

        if fever:
            emergency_reasons.append("Fever")

        if low_temp:
            emergency_reasons.append("Low body temperature")

        if lethargic:
            emergency_reasons.append("Lethargic or unconscious")

    # --------------------------------------------------
    # UNDER‑5 (Above 28 days)
    # --------------------------------------------------
    else:

        if convulsions:
            emergency_reasons.append("Convulsions")

        if fast_breathing:
            emergency_reasons.append("Possible pneumonia")

        if severe_diarrhea:
            emergency_reasons.append("Severe diarrhea")

        if blood_in_stool:
            emergency_reasons.append("Blood in stool")

        if fever:
            emergency_reasons.append("High fever")

        if lethargic:
            emergency_reasons.append("Lethargic or unconscious")

    # --------------------------------------------------
    # Final Classification
    # --------------------------------------------------

    if emergency_reasons:
        return {
            "risk_level": "EMERGENCY",
            "reasons": emergency_reasons,
            "action": "Immediate referral required."
        }

    return {
        "risk_level": "LOW",
        "reasons": ["No emergency danger signs detected."],
        "action": "Continue monitoring and routine care."
    }