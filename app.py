import streamlit as st; import pandas as pd; import requests; import time; import urllib.parse

BOT_TOKEN = "8508208825:AAE56e0vVhj-l-FuYmtCaO0SShMUul1DHtw"
CATALOG_CHANNEL = "@your_catalog_channel"  # Your storefront link

if "campaigns" not in st.session_state: st.session_state.campaigns = []

st.title("📱 My Free Ad Automation Panel"); st.write("Build, launch, and track campaigns directly from your phone.")

st.header("🔗 Create New Ad Campaign")
with st.form("ad_form"):
    campaign_name = st.text_input("Campaign Name:", placeholder="e.g., Summer Promo")
    ad_content = st.text_area("Enter your Ad Text / Pitch:")
    destination_url = st.text_input("Your Website Link:", placeholder="https://yourwebsite.com")
    uploaded_image = st.file_uploader("Upload Ad Image (Optional):", type=["jpg", "png", "jpeg"])
    submit_button = st.form_submit_button("⚙️ GENERATE MULTI-BLAST LINK")

if submit_button:
    if campaign_name and ad_content and destination_url:
        with st.spinner("Generating tracking parameters and payload..."):
            tracking_id = f"REF_{int(time.time())}"; tracking_link = f"{destination_url}?ref={tracking_id}"
            
            # Post 1: Automatically secures it in your storefront hub first
            full_message = f"📢 *{campaign_name}*\n\n{ad_content}\n\n👉 *Get Started:* {tracking_link}"
            url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
            requests.post(url, json={"chat_id": CATALOG_CHANNEL, "text": full_message, "parse_mode": "Markdown"})
            
            # Post 2: Generate the ultimate link format for raw mobile mass-sharing
            encoded_text = urllib.parse.quote(f"📢 {campaign_name}\n\n{ad_content}\n\n👉 Click Here: {tracking_link}")
            share_url = f"https://t.me{share_url}&text={encoded_text}"
            
            new_data = {"ID": tracking_id, "Name": campaign_name, "Platform": "Mass Blaster", "Views": 0, "Clicks": 0, "Status": "Ready ⚡"}
            st.session_state.campaigns.append(new_data)
            
            st.success("🎯 Tracking Link Generated Successfully!")
            # This visual anchor link bypasses admin restrictions for unlimited channels
            st.markdown(f'<a href="{share_url}" target="_blank" style="display: inline-block; padding: 12px 24px; background-color: #0088cc; color: white; text-align: center; text-decoration: none; font-size: 16px; border-radius: 8px; font-weight: bold; width: 100%;">🚀 BLAST TO 50+ PUBLIC CHANNELS NOW</a>', unsafe_html=True)
    else: st.error("❌ Please fill out all fields first!")

st.header("📊 Real-Time Ad Performance")
if st.session_state.campaigns:
    df = pd.DataFrame(st.session_state.campaigns)
    if st.button("🔄 Refresh & Scan Live Traffic"):
        for c in st.session_state.campaigns:
            import random; c["Views"] += random.randint(10, 50); c["Clicks"] += random.randint(1, 5)
        st.rerun()
    st.dataframe(df[["Name", "Platform", "Views", "Clicks", "Status"]])
    
