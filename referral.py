def generate_referral_message(
    name,
    result,
    facility_name="Nearest designated referral facility",
    facility_contact="Contact not configured"
):
    risk_level = result.get("risk_level", "UNKNOWN")
    risk_score = result.get("risk_score", 0)
    reasons = result.get("reasons", [])

    message_lines = [
        "URGENT MATERNAL REFERRAL",
        "",
        f"Patient: {name or 'Unnamed client'}",
        f"Risk level: {risk_level}",
        f"Risk score: {risk_score}",
        "",
        "Danger signs identified:"
    ]

    for reason in reasons:
        message_lines.append(f"- {reason}")

    message_lines.extend([
        "",
        "Action: Immediate clinical referral required.",
        "",
        f"Receiving facility: {facility_name}",
        f"Facility contact: {facility_contact}"
    ])

    return "\n".join(message_lines)