
import streamlit as st
import pandas as pd
from datetime import datetime
import json
import os

# გვერდის კონფიგურაცია
st.set_page_config(page_title="ნიკას ასისტენტი", page_icon="❤️")

# სტილები
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background-color: #262730; color: white; border: 1px solid #464b5d; font-weight: bold; }
    .status-box { padding: 25px; border-radius: 20px; text-align: center; font-size: 22px; font-weight: bold; margin: 15px 0; border: 2px solid #333; }
    .nika-wish { text-align: center; color: #ff4b4b; font-size: 18px; font-style: italic; margin-top: 30px; padding: 20px; border-top: 1px solid #333; }
    h1, h2, h3 { color: white; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# მონაცემების მართვა
def save_data(data):
    with open('readings.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def load_data():
    if os.path.exists('readings.json'):
        with open('readings.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return []

# ნორმების შემოწმება
def check_level(value, context):
    is_fasting = context in ["უზმოზე", "საუზმემდე", "ძილის წინ"]
    if value < 70: return "დაბალი", "🔵", "#e3f2fd", "დედა, შაქარი დაბალია, მიიღე ცოტა ტკბილი! 🍬"
    if is_fasting:
        if value <= 100: return "იდეალური ნორმა", "🟢", "#e8f5e9", "ყველაფერი შესანიშნავადაა! ✨"
        if value <= 125: return "მომატებული", "🟡", "#fffde7", "ყურადღებით იყავი, ცოტა მაღალია. ⚠️"
        return "კრიტიკული", "🔴", "#ffebee", "დედა, შაქარი მაღალია! მიიღე წამალი! 💊"
    else:
        if value <= 140: return "იდეალური ნორმა", "🟢", "#e8f5e9", "ჭამის შემდეგ მშვენიერი შედეგია! ✅"
        if value <= 199: return "მომატებული", "🟡", "#fffde7", "ცოტა მეტი სიფრთხილეა საჭირო. ⚠️"
        return "კრიტიკული", "🔴", "#ffebee", "მაჩვენებელი მაღალია! მიმართე ექიმს! 🛑"

# --- ავტომატური შეხსენებები ---
current_time = datetime.now().strftime("%H:%M")
if current_time in ["09:00", "14:00", "21:00"]:
    st.toast(f"🔔 დედა, ნიკა შეგახსენებს: დროა შაქარი შეიმოწმო! ❤️")
    st.balloons()

st.title("❤️ დედას მზრუნველი ასისტენტი")

# წყლის განყოფილება
st.subheader("💧 წყლის კონტროლი")
if 'water' not in st.session_state: st.session_state.water = 0
w_cols = st.columns(8)
for i in range(8):
    if w_cols[i].button("💧" if i >= st.session_state.water else "🟦", key=f"w_{i}"):
        st.session_state.water = i + 1
st.caption(f"დღეს დალეულია {st.session_state.water} ჭიქა")

st.divider()

# ახალი ჩანაწერი
st.subheader("🩸 მაჩვენებლის შეყვანა")
val = st.number_input("შაქრის დონე (მგ/დლ):", min_value=20, max_value=500, value=110)
ctx = st.selectbox("მდგომარეობა:", ["უზმოზე", "საუზმის შემდეგ", "სადილის შემდეგ", "ვახშმის შემდეგ", "ძილის წინ"])

if st.button("შემოწმება და შენახვა"):
    status, emoji, color, msg = check_level(val, ctx)
    st.markdown(f"<div class='status-box' style='background-color: {color}; color: black;'>{emoji} {status}: {val}<br><small>{msg}</small></div>", unsafe_allow_html=True)
    
    entry = {"თარიღი": datetime.now().strftime("%d/%m %H:%M"), "მაჩვენებელი": val, "კონტექსტი": ctx, "სტატუსი": status}
    history = load_data()
    history.append(entry)
    save_data(history)
    st.success("მონაცემი შენახულია ✅")

st.divider()

# ისტორია
st.subheader("📜 ბოლო ჩანაწერები")
history = load_data()
if history:
    df = pd.DataFrame(history)
    st.dataframe(df.tail(5), use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📄 რეპორტის გადმოწერა ექიმისთვის", csv, "sugar_report.csv", "text/csv")

# --- ნიკას კეთილი სურვილები ---
st.markdown("""
    <div class='nika-wish'>
        ჯანმრთელობას გისურვებ, დე! ❤️<br>
        კეთილი სურვილებით, შენი <b>ნიკა ასისტენტი</b>
    </div>
    """, unsafe_allow_html=True)

with st.sidebar:
    st.write("⚙️ ნიკას მენიუ")
    if st.button("🔔 შეტყობინების ტესტი"):
        st.toast("ნიკა: შეტყობინებები მუშაობს! ❤️")
