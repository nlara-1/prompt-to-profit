# P2P.py
import time
import streamlit as st
from content import ROUNDS
from scoring import score_prompt, interpret_kpis
from db import init_db, add_leaderboard, get_end_now, get_start_now

st.set_page_config(page_title="Prompt to Profit (P2P)", page_icon="💼", layout="wide")
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
    ss.setdefault("prompt_text", "")
    ss.setdefault("_last_tick", 0.0)

_init_state()

TOTAL_SECONDS = 20 * 60
def seconds_left():
    spent = int(time.time() - st.session_state._last_tick)
    return max(0, TOTAL_SECONDS - spent)

def reset_game(keep_name=True):
    name = st.session_state.player_name
    st.session_state.clear()
    _init_state()
    if keep_name:
        st.session_state.player_name = name
        st.session_state.joined = True


# Header
left, right = st.columns([2, 1])
with left:
    st.title("Prompt to Profit (P2P)")
    st.caption("Make smart business decisions with AI — every round is a trade-off.")
with right:
    started = get_start_now() == 1
    ended = get_end_now() == 1
    tl = seconds_left() if started and not ended else TOTAL_SECONDS
    st.metric("⏱ Time Left", f"{tl//60:02d}:{tl%60:02d}")
    st.metric("Total Score", st.session_state.score)

st.divider()

# Join flow
if not st.session_state.joined:
    st.subheader("Join the Game")
    st.session_state.player_name = st.text_input("Enter your name", max_chars=32)
    if st.button("Join"):
        if st.session_state.player_name.strip():
            st.session_state.joined = True
            st.success(f"Welcome, {st.session_state.player_name}!")
            st.rerun()
        else:
            st.error("Please enter a name.")
    st.stop()

if get_start_now() == 0 and get_end_now() == 0:
    st.info("Waiting for the admin to start the game…")
    st.button("Refresh", on_click=lambda: st.rerun())
    st.stop()

if get_end_now() == 1:
    st.warning("The admin has ended the game.")
    st.stop()

# Gameplay
if st.session_state.round_index < len(ROUNDS):
    r = ROUNDS[st.session_state.round_index]

    st.subheader(f"Round {r['id']}: {r['department']}")
    st.markdown(f"**Scenario:** {r['scenario']}")
    st.markdown(f"**Objective:** {r['objective']}")

    st.markdown("### Quick Options")
    cols = st.columns(3)
    for i, ch in enumerate(r["choices"]):
        with cols[i]:
            st.caption(ch["text"])
            disabled = st.session_state.round_submitted
            if st.button(f"Option {ch['key']}", key=f"opt_{r['id']}_{ch['key']}", disabled=disabled):
                if not st.session_state.round_submitted:
                    delta = ch["kpi_effects"]
                    total = sum(delta.values())
                    st.session_state.score += total
                    for k, v in delta.items():
                        st.session_state.kpis[k] += v
                    explanation = interpret_kpis(delta)
                    st.session_state.assistant_msg = (
                        f"Rowdy gives you **{total} points.** "
                        f"You did great in {explanation}"
                    )
                    st.session_state.round_submitted = True
                    st.rerun()

    st.markdown("### Or Write Your Own Prompt")
    st.session_state.prompt_text = st.text_area(
        "Your custom prompt",
        placeholder="Write a creative, detailed AI instruction here...",
        value=st.session_state.prompt_text,
        height=150,
        disabled=st.session_state.round_submitted,
    )

    if st.button("Submit Prompt", type="primary", use_container_width=True, disabled=st.session_state.round_submitted):
        if not st.session_state.round_submitted:
            used_text = st.session_state.prompt_text.strip()
            total, _, hard_fail, _, explanation = score_prompt(used_text)
            st.session_state.score += total
            st.session_state.assistant_msg = f"Rowdy gives you **{total} points.** {explanation}"
            st.session_state.round_submitted = True
            st.rerun()

    if st.button("Next Round", disabled=not st.session_state.round_submitted):
        st.session_state.round_index += 1
        st.session_state.assistant_msg = ""
        st.session_state.round_submitted = False
        st.session_state.prompt_text = ""
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
