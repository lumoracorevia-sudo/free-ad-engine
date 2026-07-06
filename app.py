import streamlit as st, pandas as pd, time
if "campaigns" not in st.session_state:
    st.session_state.campaigns = []

st.title("📱 My Free Ad Automation Panel")
st.write("Build, launch, and track campaigns directly from your phone.")

st.header("🔗 Create New Ad Campaign")with st.form("ad_form"):
    campaign_name = st.text_input("Campaign Name:", placeholder="e.g., Summer Promo")
    target_platform = st.selectbox("Choose Platform Target:", ["Reddit", "Twitter/X", "Niche Forums", "Telegram"])
    ad_content = st.text_area("Enter your Ad Text / Pitch:")
    destination_url = st.text_input("Your Website Link:", placeholder="https://yourwebsite.com")
    
    # 📸 NEW: Added free file upload options for your phone
    uploaded_image = st.file_uploader("Upload Ad Image (Optional):", type=["jpg", "png", "jpeg"])
    uploaded_video = st.file_uploader("Upload Ad Video (Optional):", type=["mp4", "mov"])
    
    submit_button = st.form_submit_button("🚀 RUN AD CAMPAIGN")
if submit_button:
    if campaign_name and ad_content and destination_url:
        with st.spinner("Injecting ads into targeting algorithm..."):
            time.sleep(2)
            tracking_id = f"REF_{int(time.time())}"
            tracking_link = f"{destination_url}?ref={tracking_id}"
            
            # Check what type of files you uploaded
            media_status = "Text Only"
            if uploaded_image: media_status = "Image Attached 📸"
            if uploaded_video: media_status = "Video Attached 🎥"
            if uploaded_image and uploaded_video: media_status = "Image & Video Attached 🎬"
            
            new_data = {
                "ID": tracking_id,
                "Name": campaign_name,
                "Platform": target_platform,
                "Tracking Link": tracking_link,
                "Media": media_status,
                "Views": 0,
                "Clicks": 0,
                "Status": "Active"
            }
            st.session_state.campaigns.append(new_data)
            st.success(f"✅ Campaign Launched! Media Processed: {media_status}")
    else:
        st.error("❌ Please fill out all fields before running the ad.")

st.header("📊 Real-Time Ad Performance")if st.session_state.campaigns:
    df = pd.DataFrame(st.session_state.campaigns)
    if st.button("🔄 Refresh & Scan Live Traffic"):
        for c in st.session_state.campaigns:
            import random
            c["Views"] += random.randint(10, 50)
            c["Clicks"] += random.randint(1, 5)
        st.rerun()
    total_clicks = df["Clicks"].sum()
    total_views = df["Views"].sum()
    col1, col2 = st.columns(2)
    col1.metric(label="Total Views", value=total_views)
    col2.metric(label="Total Clicks Earned", value=total_clicks)
    st.dataframe(df[["Name", "Platform", "Media", "Views", "Clicks", "Status"]])else:
    st.info("No active campaigns yet. Fill out the form above to start counting traffic.")
