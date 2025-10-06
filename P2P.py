# P2P.py
import streamlit as st
st.set_page_config(page_title="Prompt to Profit (P2P)", page_icon="💼", layout="wide")

import time, random
from content import ROUNDS
from scoring import interpret_kpis
from db import init_db, add_leaderboard, get_end_now, get_start_now

init_db()

def _init_state():
    ss = st.session_state
    ss.setdefault("joined", False)
    ss.setdefault("player_name", "")
    ss.setdefault("round_index", 0)
    ss.setdefault("score", 0)
    ss.setdefault("kpis", {"revenue": 0, "efficiency": 0, "reputation": 0, "innovation": 0})
    ss.setdefault("assistant_msg", "")
    ss.setdefault("round_submitted", False)
    ss.setdefault("_last_tick", time.time())
    ss.setdefault("weights", {k: random.uniform(0.8, 1.2) for k in ["revenue","efficiency","reputation","innovation"]})

_init_state()

TOTAL_SECONDS = 20 * 60

def seconds_left():
    spent = int(time.time() - st.session_state._last_tick)
    return max(0, TOTAL_SECONDS - spent)

# Layout
left, right = st.columns([2,1])
with left:
    st.title("Prompt to Profit (P2P)")
    st.caption("Strategize with AI — balance your priorities and trade-offs.")
with right:
    started = get_start_now() == 1
    ended = get_end_now() == 1
    tl = seconds_left() if started and not ended else TOTAL_SECONDS
    st.metric("⏱ Time Left", f"{tl//60:02d}:{tl%60:02d}")
    st.metric("Total Score", st.session_state.score)

st.divider()

# Join
if not st.session_state.joined:
    name = st.text_input("Enter your name", max_chars=32)
    if st.button("Join"):
        if name.strip():
            st.session_state.player_name = name.strip()
            st.session_state.joined = True
            st.rerun()
    st.stop()

if get_start_now() == 0 and get_end_now() == 0:
    st.info("Waiting for the admin to start the game…")
    st.stop()
if get_end_now() == 1:
    st.warning("Game ended by admin.")
    st.stop()

# Gameplay
if st.session_state.round_index < len(ROUNDS):
    r = ROUNDS[st.session_state.round_index]
    st.subheader(f"Round {r['id']}: {r['department']}")
    st.markdown(f"**Scenario:** {r['scenario']}")
    st.markdown(f"**Objective:** {r['objective']}")
    st.markdown(f"**This round’s priority:** `{r['priority'].capitalize()}`")
    st.divider()

    cols = st.columns(3)
    for i, ch in enumerate(r["choices"]):
        with cols[i]:
            st.caption(ch["text"])
            if st.button(f"Option {ch['key']}", key=f"opt_{r['id']}_{ch['key']}", disabled=st.session_state.round_submitted):
                delta = ch["kpi_effects"]
                weights = st.session_state.weights
                weighted_total = sum(v * weights.get(k, 1.0) for k, v in delta.items())
                st.session_state.score += int(weighted_total)
                for k, v in delta.items():
                    st.session_state.kpis[k] += v
                desc = interpret_kpis(delta, r["priority"], weights)
                st.session_state.assistant_msg = (
                    f"Rowdy gives you **{int(weighted_total)} points.** {desc.capitalize()}."
                )
                st.session_state.round_submitted = True
                st.rerun()

    if st.button("Next Round", disabled=not st.session_state.round_submitted):
        st.session_state.round_index += 1
        st.session_state.round_submitted = False
        st.session_state.assistant_msg = ""
        st.rerun()

    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Revenue", st.session_state.kpis["revenue"])
    m2.metric("Efficiency", st.session_state.kpis["efficiency"])
    m3.metric("Reputation", st.session_state.kpis["reputation"])
    m4.metric("Innovation", st.session_state.kpis["innovation"])
    st.info(f"**Rowdy says:** {st.session_state.assistant_msg or 'Ready when you are!'}")

else:
    st.success("You’ve completed all rounds!")
    name = st.session_state.player_name.strip() or "Anonymous"
    if st.button("Save Score", type="primary"):
        add_leaderboard(name, st.session_state.score)
        st.success("Score saved to leaderboard.")
