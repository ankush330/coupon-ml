
import streamlit as st
import joblib
import re
import pandas as pd

# Load models
clf = joblib.load("coupon_classifier.pkl")
reg = joblib.load("coupon_regressor.pkl")
le  = joblib.load("label_encoder.pkl")

def get_amount(text):
    amounts = re.findall(r"rs\.?\s*(\d+)", text)
    return int(amounts[0]) if amounts else 0

def get_min_order(text):
    match = re.findall(r"(?:above|over|minimum|min)\s*rs\.?\s*(\d+)", text)
    return int(match[0]) if match else 0

def get_percent(text):
    match = re.findall(r"(\d+)\s*%", text)
    return int(match[0]) if match else 0

def extract_features(text):
    t = text.lower()
    is_upto    = int(bool(re.search(r"\bupto\b|up to|maximum|max\b", t)))
    is_flat    = int(bool(re.search(r"\bflat\b|\binstant\b|\bguaranteed\b", t)))
    is_percent = int(bool(re.search(r"\d+\s*%", t)))
    max_amount  = get_amount(t)
    max_percent = get_percent(t)
    min_order   = get_min_order(t)
    value_ratio = round(max_amount / min_order, 4) if min_order > 0 else 0
    return [is_upto, is_flat, is_percent, max_amount, max_percent, min_order, value_ratio]

def rank_coupons(coupon_list):
    results = []
    for text in coupon_list:
        feats       = extract_features(text)
        coupon_type = le.inverse_transform(clf.predict([feats]))[0]
        exp_value   = reg.predict([feats])[0]
        results.append({
            "Coupon":       text,
            "Type":         coupon_type,
            "Expected Rs.": round(float(exp_value), 2)
        })
    ranked = pd.DataFrame(results).sort_values("Expected Rs.", ascending=False)
    ranked.index = range(1, len(ranked) + 1)
    return ranked

# ── UI ──
st.title("🎟️ Coupon Ranker")
st.write("Enter your coupons below (one per line) and get them ranked best to worst!")

user_input = st.text_area(
    "Paste your coupons here:",
    height=200,
    placeholder="Flat Rs.150 cashback on orders above Rs.500\nUpto Rs.500 cashback on first order\nFlat 10% cashback on all orders"
)

if st.button("🏆 Rank My Coupons"):
    coupons = [c.strip() for c in user_input.strip().split("\n") if c.strip()]
    if len(coupons) == 0:
        st.warning("Please enter at least one coupon!")
    else:
        result = rank_coupons(coupons)
        st.success(f"Ranked {len(coupons)} coupons!")
        st.dataframe(result, use_container_width=True)
        st.markdown("### 🥇 Best Coupon:")
        st.info(result.iloc[0]["Coupon"])
