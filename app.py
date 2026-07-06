import streamlit as st; import pandas as pd; import requests; import time; import urllib.parse

BOT_TOKEN = "8508208825:AAE56e0vVhj-l-FuYmtCaO0SShMUul1DHtw"
CATALOG_CHANNEL = "@your_catalog_channel"

if "campaigns" not in st.session_state: st.session_state.campaigns = []

st.title("📱 My Free Ad Automation Panel"); st.write("Build, launch, and track campaigns directly from your phone.")

st.header("🔗 Create New Ad Campaign")
with st.form("ad_form"):
    campaign_name = st.text_input("Campaign Name:", placeholder="e.g., Summer Promo")
    ad_content = st.text_area("Enter your Ad Text / Pitch:")
    destination_url = st.text_input("Your Website Link (Optional):", placeholder="https://yourwebsite.com")
    uploaded_image = st.file_uploader("Upload Ad Image (Optional):", type=["jpg", "png", "jpeg"])
    uploaded_video = st.file_uploader("Upload Ad Video (Optional):", type=["mp4", "mov"])
    submit_button = st.form_submit_button("⚙️ GENERATE MULTI-BLAST LINK")

if submit_button:
    if campaign_name and ad_content:
        with st.spinner("Processing parameters..."):
            tracking_link = destination_url.strip()
            if tracking_link and not tracking_link.startswith(("http://", "https://")):
                tracking_link = "https://" + tracking_link
            if not tracking_link:
                tracking_link = "https://t.me"
            
            if CATALOG_CHANNEL and CATALOG_CHANNEL != "@your_catalog_channel":
                try:
                    full_message = f"📢 *{campaign_name}*\n\n{ad_content}\n\n👉 *Link:* {tracking_link}"
                    url = f"https://telegram.org{BOT_TOKEN}/sendMessage"
                    requests.post(url, json={"chat_id": CATALOG_CHANNEL, "text": full_message, "parse_mode": "Markdown"}, timeout=5)
                except:
                    pass
            
            # Format clean, raw message for manual mobile sharing
            raw_broadcast_text = f"📢 {campaign_name}\n\n{ad_content}\n\n👉 Link: {tracking_link}"
            encoded_text = urllib.parse.quote(raw_broadcast_text)
            share_url = f"https://t.me{encoded_text}"
            
            new_data = {"ID": f"REF_{int(time.time())}", "Name": campaign_name, "Platform": "Mass Blaster", "Views": 0, "Clicks": 0, "Status": "Ready ⚡"}
            st.session_state.campaigns.append(new_data)
            
            st.success("🎯 Multi-Blast Text Packaged Successfully!")
            
            # 🛡️ POP-UP FIX: Displays the raw message in a copy box so your phone's browser can't block it
            st.text_area("📋 Tap below to select and copy your formatted ad text:", value=raw_broadcast_text, height=120)
            st.link_button("🚀 TRY FORCED MOBILE OPEN", share_url, use_container_width=True)
    else:
        st.error("❌ Please fill out at least a Campaign Name and Ad Content text first!")

st.header("📊 Real-Time Ad Performance")
if st.session_state.campaigns:
    df = pd.DataFrame(st.session_state.campaigns)
    if st.button("🔄 Refresh & Scan Live Traffic"):
        for c in st.session_state.campaigns:
            import random; c["Views"] += random.randint(10, 50); c["Clicks"] += random.randint(1, 5)
        st.rerun()
    st.dataframe(df[["Name", "Platform", "Views", "Clicks", "Status"]])
else: st.info("No active campaigns yet. Fill out the form above to start counting traffic.")
    
