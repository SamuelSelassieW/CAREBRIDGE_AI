def generate_chatbot_response(result, patient_name="Client"):

    risk = result["risk_level"]
    reasons = result["reasons"]
    action = result["action"]

    response = f"Assessment for {patient_name}:\n\n"

    if risk == "EMERGENCY":
        response += "🚨 High Risk Detected.\n"
        response += "The following danger signs were identified:\n"

    elif risk == "WARNING":
        response += "⚠️ Moderate Risk Detected.\n"
        response += "The following warning signs were identified:\n"

    else:
        response += "✅ No immediate danger signs detected.\n"

    for r in reasons:
        response += f"- {r}\n"

    response += f"\nRecommended Action: {action}\n"
    response += "\nThis tool supports clinical judgment and does not replace a qualified health professional."

    return response