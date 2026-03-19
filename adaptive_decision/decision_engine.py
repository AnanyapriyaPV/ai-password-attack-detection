def adaptive_decision(risk_score):

    if risk_score < 0.3:
        return "ALLOW"

    elif risk_score < 0.6:
        return "CAPTCHA"

    elif risk_score < 0.8:
        return "MFA_REQUIRED"

    else:
        return "BLOCK"