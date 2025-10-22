import pickle, os, re
import numpy as np

MODEL_PATH = "models/trained_model.pkl"

# -------------------- Load Model --------------------
with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

# -------------------- Utility --------------------
def clean_text(t: str):
    t = (t or "").lower()
    t = re.sub(r'[^a-z\s]', ' ', t)
    return re.sub(r'\s+', ' ', t).strip()

# -------------------- Rule-Based Logic --------------------
def rule_based_score(msg: str, email: str = ""):
    msg = msg.lower()
    score = 0

    # Strong intent indicators
    if any(k in msg for k in ["urgent", "immediately", "asap", "finalize", "proposal", "pricing", "buy now", "demo today"]):
        score += 50
    if any(k in msg for k in ["quote", "integration", "crm setup", "enterprise", "contract", "deploy"]):
        score += 30
    if re.search(r"\b\d{10}\b", msg):  # phone number present
        score += 10
    if any(domain in email for domain in [".in", ".co", ".org", ".biz", "tech", "solutions"]):
        score += 10

    if score >= 80:
        return score, "Hot"
    elif score >= 50:
        return score, "Warm"
    else:
        return score, "Cold"

# -------------------- ML Prediction Logic --------------------
def ml_score(msg: str):
    try:
        text = clean_text(msg)
        probs = model.predict_proba([text])[0]
        predicted_class = np.argmax(probs)
        confidence = probs[predicted_class]

        labels = model.classes_
        label = labels[predicted_class] if predicted_class < len(labels) else "Warm"

        # Threshold control
        if confidence > 0.65 and label == "Hot":
            score = 90
        elif confidence > 0.45 and label == "Warm":
            score = 65
        else:
            score = 30

        return score, label, confidence

    except Exception as e:
        print("⚠️ ML prediction error:", e)
        return 50, "Warm", 0.4

# -------------------- Combine and Boost Logic --------------------
def combine_scores(rule_score, ml_score_val, interaction_boost):
    combined = (rule_score + ml_score_val + interaction_boost) / 3
    return int(combined)

# -------------------- Final Classifier --------------------
def classify_message(message: str, email: str = ""):
    # Calculate rule and ML-based scores
    r_score, r_label = rule_based_score(message, email)
    m_score, m_label, confidence = ml_score(message)

    # Keyword-based urgency boost
    msg = message.lower()
    interaction_boost = 0
    if any(word in msg for word in ["urgent", "demo", "pricing", "immediately", "next week", "meeting", "quote"]):
        interaction_boost = 10

    # Final score combination
    final_score = combine_scores(r_score, m_score, interaction_boost)

    # Determine final label
    if final_score >= 80:
        label = "Hot"
    elif final_score >= 50:
        label = "Warm"
    else:
        label = "Cold"

    print(f"[DEBUG] Rule: {r_label} ({r_score}) | ML: {m_label} ({m_score:.2f}, conf={confidence:.2f}) | Boost={interaction_boost} → Final={label} ({final_score})")

    return final_score, label
