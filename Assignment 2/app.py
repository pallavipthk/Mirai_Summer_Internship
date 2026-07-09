
import streamlit as st
import pandas as pd
import re
from datetime import datetime
 
st.set_page_config(page_title="The Identity Echo", page_icon="📡", layout="centered")
 
st.title("📡 The Identity Echo")
st.write(
    "Send your identity across the network. "
    "Fill in your name and message, then click **Send**."
)
st.caption("This application validates user input and estimates AI token usage.")
 
st.divider()
 
# ---------------- SESSION STATE ----------------
if "history" not in st.session_state:
    st.session_state.history = []
 
# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.header("⚙️ Settings")
    max_len = st.slider("Max message length", 20, 500, 280)
    chars_per_token = st.select_slider(
        "Chars per token (tokenizer estimate)", options=[3, 3.5, 4], value=4
    )
    st.divider()
    st.metric("Transmissions this session", len(st.session_state.history))
    if st.session_state.history:
        total_tokens = round(sum(e["tokens"] for e in st.session_state.history), 2)
        st.metric("Total tokens used", total_tokens)
    if st.button("🗑️ Clear History"):
        st.session_state.history = []
        st.rerun()
 
# ---------------- INPUT ----------------
user_name = st.text_input("👤 Enter Your Name")
user_message = st.text_area("💬 Enter Your Message", max_chars=max_len, height=100)
 
# ---------------- SEND ----------------
if st.button("🚀 Send Transmission"):
 
    if not user_name or not user_name.strip():
        st.error("Please provide your name.")
 
    elif not user_message or not user_message.strip():
        st.warning("Please type a message to transmit.")
 
    else:
        st.divider()
 
        st.success(
            f"""
✅ **Transmission Successful!**
 
Greetings, **{user_name}**
 
We received your message:
 
> {user_message}
            """
        )
 
        # ---------------- ANALYSIS ----------------
        characters = len(user_message)
        words = len(user_message.split())
        sentences = max(1, len(re.findall(r"[.!?]+", user_message)))
        token_count = round(characters / chars_per_token, 2)
 
        col1, col2, col3 = st.columns(3)
        col1.metric("Characters", characters)
        col2.metric("Words", words)
        col3.metric("Est. Tokens", token_count)
 
        st.progress(min(characters / max_len, 1.0), text=f"{characters}/{max_len} characters used")
 
        # ---------------- SAVE ----------------
        st.session_state.history.append(
            {
                "time": datetime.now().strftime("%H:%M:%S"),
                "name": user_name,
                "message": user_message,
                "characters": characters,
                "words": words,
                "tokens": token_count,
            }
        )
 
st.divider()
 
# ---------------- HISTORY / LOG ----------------
if st.session_state.history:
    st.subheader("📜 Transmission Log")
    df = pd.DataFrame(st.session_state.history)
    st.dataframe(df, use_container_width=True, hide_index=True)
 
    st.bar_chart(df.set_index("time")["tokens"])
 
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Download Log as CSV", data=csv, file_name="transmission_log.csv", mime="text/csv")
else:
    st.caption("No transmissions yet — send your first message above! 👆")
 
st.divider()
st.caption("Built with ❤️ using Streamlit • MirAI Summer Internship 2026")