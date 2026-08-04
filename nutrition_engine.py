def assess_malnutrition(muac):
    if muac < 11.5:
        return "Severe Acute Malnutrition", True
    elif 11.5 <= muac < 12.5:
        return "Moderate Acute Malnutrition", True
    else:
        return "Normal", False


def generate_nutrition_guidance(age_months, muac, weight_loss=False, poor_appetite=False):
    # Added 'poor_appetite' to function definition ^^^

    malnutrition_level, referral_needed = assess_malnutrition(muac)

    advice = []

    if age_months < 6:
        advice.append("Exclusive breastfeeding is recommended.")
    else:
        advice.append("Continue breastfeeding + complementary feeding.")

    if weight_loss:
        advice.append("Child is losing weight. Monitor closely.")
    
    # ✅ Handle poor appetite here
    if poor_appetite:
        advice.append("Child has poor appetite. Encourage small, frequent, nutrient-dense meals.")

    advice.append(f"MUAC Assessment: {malnutrition_level}")

    local_foods = [
        "Beans",
        "Groundnuts (peanut paste)",
        "Eggs",
        "Orange-fleshed sweet potatoes",
        "Millet porridge with groundnut paste",
        "Soybeans",
        "Green leafy vegetables"
    ]

    advice.append("Recommended Local Foods:")
    for food in local_foods:
        advice.append(f"- {food}")

    if referral_needed:
        advice.append("⚠️ Refer to nearest health facility immediately.")

    return {
        "malnutrition_level": malnutrition_level,
        "referral_needed": referral_needed,
        "advice": advice
    }