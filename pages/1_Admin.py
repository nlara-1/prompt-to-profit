# pages/1_Admin.py  (replace file)
import streamlit as st
from db import (
    init_db, top10, standings,
    set_end_now, get_end_now,
    set_admin_code_hash, get_admin_code_hash,
    set_start_now, get_start_now,
    migrate_db, wipe_leaderboard
)
from utils import hash_code, check_code

st.set_page_config(page_title="Admin • P2P", page_icon="🛠️", layout="wide")
init_db()

st.title("Admin Dashboard")
st.caption("Control game start/end, view live standings, project podium.")

# ---- Admin code management (never display the code) ----
with st.expander("Admin Security", expanded=True):
    stored_hash = get_admin_code_hash()
    if stored_hash:
        st.success("Admin code is configured.")
        with st.form("change_code_form", clear_on_submit=True):
            st.write("To change the admin code, verify with the current code.")
            current = st.text_input("Current admin code", type="password")
            new_code = st.text_input("New admin code", type="password")
            submitted = st.form_submit_button("Update Admin Code")
            if submitted:
                if not current or not new_code:
                    st.error("Both fields are required.")
                elif not check_code(current.strip(), stored_hash):
                    st.error("Current code is incorrect.")
                else:
                    set_admin_code_hash(hash_code(new_code.strip()))
                    st.success("Admin code updated.")
    else:
        st.warning("No admin code set. Create one now.")
        with st.form("set_code_form", clear_on_submit=True):
            new_code = st.text_input("Set admin code", type="password")
            submitted = st.form_submit_button("Save Admin Code")
            if submitted:
                if not new_code.strip():
                    st.error("Code cannot be empty.")
                else:
                    set_admin_code_hash(hash_code(new_code.strip()))
                    st.success("Admin code saved.")

# ---- Start / End controls ----
st.subheader("Start / End Game")
start_flag = get_start_now()
end_flag = get_end_now()

c1, c2 = st.columns(2)
with c1:
    st.metric("Game Start Flag", "ENABLED" if start_flag == 1 else "DISABLED")
    code_start = st.text_input("Enter admin code to toggle START", type="password", key="start_code")
    if st.button("Toggle Start"):
        if not check_code(code_start.strip(), get_admin_code_hash()):
            st.error("Invalid admin code.")
        else:
            set_start_now(0 if get_start_now() == 1 else 1)
            st.success("Start flag toggled.")
            st.rerun()

with c2:
    st.metric("Game End Flag", "ENABLED" if end_flag == 1 else "DISABLED")
    code_end = st.text_input("Enter admin code to toggle END", type="password", key="end_code")
    if st.button("Toggle End"):
        if not check_code(code_end.strip(), get_admin_code_hash()):
            st.error("Invalid admin code.")
        else:
            set_end_now(0 if get_end_now() == 1 else 1)
            st.success("End flag toggled.")
            st.rerun()

st.divider()

# ---- Live standings ----
st.subheader("Live Standings")
limit = st.slider("Show top N", min_value=10, max_value=200, value=60, step=10)
rows = standings(limit)
if rows:
    st.dataframe(rows, use_container_width=True, hide_index=True)
else:
    st.info("No players yet.")

# ---- Podium view link ----
st.subheader("Project Podium")
st.page_link("pages/2_Leaderboard.py", label="Open Leaderboard / Podium →")

# ---- Maintenance ----
st.divider()
st.subheader("Maintenance")
if st.button("Migrate/Repair DB"):
    try:
        migrate_db()
        st.success("Database migrated/repaired successfully.")
    except Exception as e:
        st.error(f"Migration failed: {e}")

with st.expander("Danger Zone: Wipe Leaderboard"):
    st.write("This permanently deletes all leaderboard entries.")
    code = st.text_input("Enter admin code to confirm", type="password", key="wipe_code")
    confirm = st.text_input('Type **WIPE** to confirm', key="wipe_text")
    if st.button("Wipe Leaderboard"):
        if not (confirm.strip().upper() == "WIPE"):
            st.error("Type WIPE to confirm.")
        elif not check_code(code.strip(), get_admin_code_hash()):
            st.error("Invalid admin code.")
        else:
            wipe_leaderboard()
            st.success("Leaderboard wiped.")
