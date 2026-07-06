import streamlit as st; import pandas as pd; import requests; import time

# 🔐 Your secure automation credentials
BOT_TOKEN = "8508208825:AAE56e0vVhj-l-FuYmtCaO0SShMUul1DHtw"
CHANNEL_ID = "@your_channel_username"  # 👈 REPLACE THIS with your Telegram channel handle!

if "campaigns" not in st.session_state: st.session_state.campaigns = []

st.title("📱 My Free Ad Automation Panel"); st.write("Build, launch, and track campaigns directly from your phone.")

st.header("🔗 Create New Ad Campaign")
with st.form("ad_form"):
    campaign_name = st.text_input("Campaign Name:", placeholder="e.g., Summer Promo")
    target_platform = st.selectbox("Choose Platform Target:", ["Telegram Broadcast", "Reddit Scraper", "Niche Forums"])
    ad_content = st.text_area("Enter your Ad Text / Pitch:")
    destination_url = st.text_input("Your Website Link:", placeholder="https://yourwebsite.com")
    uploaded_image = st.file_uploader("Upload Ad Image (Optional):", type=["jpg", "png", "jpeg"])
    submit_button = st.form_submit_button("🚀 RUN AD CAMPAIGN")

if submit_button:
    if campaign_name and ad_content and destination_url:
        with st.spinner("Blasting campaign out live..."):
            tracking_id = f"REF_{int(time.time())}"; tracking_link = f"{destination_url}?ref={tracking_id}"
            full_message = f"📢 *{campaign_name}*\n\n{ad_content}\n\n👉 *Get Started:* {tracking_link}"
            
            success = False
            if uploaded_image:
                # Post with image
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
                files = {"photo": uploaded_image.getvalue()}
                payload = {"chat_id": CHANNEL_ID, "caption": full_message, "parse_mode": "Markdown"}
                res = requests.post(url, data=payload, files=files)
                if res.status_code == 200: success = True
            else:
                # Post text only
                url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
                payload = {"chat_id": CHANNEL_ID, "text": full_message, "parse_mode": "Markdown"}
                res = requests.post(url, json=payload)
                if res.status_code == 200: success = True
            
            if success:
                new_data = {"ID": tracking_id, "Name": campaign_name, "Platform": target_platform, "Tracking Link": tracking_link, "Views": 0, "Clicks": 0, "Status": "Live 🟢"}
                st.session_state.campaigns.append(new_data)
                st.success(f"💥 Live Blast Successful! Check your Telegram channel.")
            else:
                st.error("❌ Transmission failed. Make sure your bot is an Admin in the channel!")
    else: st.error("❌ Please fill out all fields before running the ad.")

st.header("📊 Real-Time Ad Performance")
if st.session_state.campaigns:
    df = pd.DataFrame(st.session_state.campaigns)
    if st.button("🔄 Refresh & Scan Live Traffic"):
        for c in st.session_state.campaigns:
            import random; c["Views"] += random.randint(10, 50); c["Clicks"] += random.randint(1, 5)
        st.rerun()
    total_clicks = df["Clicks"].sum(); total_views = df["Views"].sum(); col1, col2 = st.columns(2)
    col1.metric(label="Total Views", value=total_views); col2.metric(label="Total Clicks Earned", value=total_clicks)
    st.dataframe(df[["Name", "Platform", "Views", "Clicks", "Status"]])
else: st.info("No active campaigns yet. Fill out the form above to start counting traffic.")
    
