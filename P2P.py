# P2P.py
import time
import streamlit as st
from typing import Dict
from content import ROUNDS
from scoring import score_prompt, kpi_delta
from db import init_db, add_leaderboard, get_end_now, get_start_now

st.set_page_config(page_title="Prompt to Profit", page_icon="💼", layout="wide")
init_db()

# ---------- Session State ----------
def _init_state():
    ss = st.session_state
    ss.setdefault("joined", False)
    ss.setdefault("player_name", "")
    ss.setdefault("round_index", 0)
    ss.setdefault("score", 0)
    ss.setdefault("kpis", {"revenue":0, "efficiency":0, "reputation":0, "innovation":0})
    ss.setdefault("last_score", None)
    ss.setdefault("assistant_msg", "")
    ss.setdefault("hard_fail", False)
    ss.setdefault("start_time", time.time())
    ss.setdefault("choice_clicked", None)   # "A"/"B"/"C" chosen this round
    ss.setdefault("prompt_text", "")        # free prompt
    ss.setdefault("timer_running", True)

_init_state()

TOTAL_SECONDS = 20 * 60

def seconds_left():
    spent = int(time.time() - st.session_state.start_time) if st.session_state.timer_running else 0
    return max(0, TOTAL_SECONDS - spent)

def reset_game(keep_name=True):
    name = st.session_state.player_name
    st.session_state.clear()
    _init_state()
    if keep_name:
        st.session_state.player_name = name
        st.session_state.joined = True

# ---------- Header ----------
left, right = st.columns([2,1])
with left:
    st.title("Prompt to Profit (P2P)")
    st.caption("Join, wait for the admin to start, then optimize KPIs with effective, safe prompts.")

with right:
    # Auto-updating timer (no click required) using a short loop + placeholder
    t_placeholder = st.empty()
    s_placeholder = st.empty()

    # only tick timer if game started and not ended
    started = (get_start_now() == 1)
    ended = (get_end_now() == 1)

    def render_status():
        tl = seconds_left() if started and not ended else TOTAL_SECONDS
        t_placeholder.metric("⏱ Time Left", f"{tl//60:02d}:{tl%60:02d}")
        s_placeholder.metric("Total Score", st.session_state.score)

    render_status()
    # run a very short, non-blocking update so it feels live
    if started and not ended and st.session_state.timer_running:
        # Update once per render; Streamlit re-runs the script on any widget interaction.
        # We emulate live countdown by sleeping a beat and re-running once.
        time.sleep(0.25)
        st.rerun()

st.divider()

# ---------- Join gate ----------
if not st.session_state.joined:
    st.subheader("Join the game")
    st.session_state.player_name = st.text_input("Enter your display name to join", placeholder="e.g., Jordan", max_chars=32)
    if st.button("Join"):
        if st.session_state.player_name.strip():
            st.session_state.joined = True
            st.success(f"Welcome, {st.session_state.player_name}!")
            st.rerun()
        else:
            st.error("Please enter a name to join.")
    st.stop()

# If admin hasn't started, show lobby
if get_start_now() == 0 and get_end_now() == 0:
    st.info("Waiting for admin to start the game…")
    st.button("Refresh", on_click=lambda: st.rerun())
    st.stop()

# If admin ended early, allow saving score
if get_end_now() == 1:
    st.warning("The admin has ended the game.")
    st.session_state.timer_running = False

# ---------- Game or Results ----------
time_left = seconds_left() if get_end_now() == 0 else 0
in_rounds = st.session_state.round_index < len(ROUNDS)
if (time_left > 0) and in_rounds:
    round_obj = ROUNDS[st.session_state.round_index]

    st.subheader(f"Round {round_obj['id']}: {round_obj['department']}")
    st.write(round_obj["objective"])

    st.markdown("**Quick Options**")
    cols = st.columns(3)
    for i, ch in enumerate(round_obj["choices"]):
        with cols[i]:
            label = f"Option {ch['key']}"
            st.caption(ch["text"])
            if st.button(label, key=f"opt_{round_obj['id']}_{ch['key']}"):
                st.session_state.choice_clicked = ch["key"]
                st.session_state.prompt_text = ch["text"]
                # Score immediately for quick options
                total = max(-10, min(10, ch["presetScore"]))
                hard_fail = (total == -10)
                msg = "try again" if hard_fail else ("Nice work!" if total >= 0 else "Consider time range, output format, and explicit KPI targets.")
                delta = kpi_delta(total, round_obj["weights"])
                # apply
                st.session_state.score += total
                for k, v in delta.items():
                    st.session_state.kpis[k] += v
                st.session_state.last_score = total
                st.session_state.assistant_msg = msg
                st.session_state.hard_fail = hard_fail
                st.rerun()

    st.markdown("**Or write your own prompt**")
    st.session_state.prompt_text = st.text_area(
        "Your prompt",
        key=f"prompt_{round_obj['id']}",
        height=160,
        placeholder="Write a high-quality prompt that uses a clear time range for data, a safe approach, explicit constraints, and measurable KPIs…",
        value=st.session_state.prompt_text
    )

    c1, c2 = st.columns([1,1])
    with c1:
        if st.button("Submit Prompt", type="primary", use_container_width=True, disabled=(len(st.session_state.prompt_text.strip()) == 0)):
            used_text = st.session_state.prompt_text.strip()
            total, _, hard_fail, tips = score_prompt(used_text)
            msg = "try again" if hard_fail else ("Nice work!" if total >= 0 and not tips else f"Suggestions: {' · '.join(tips)}")
            delta = kpi_delta(total, round_obj["weights"])
            # apply
            st.session_state.score += total
            for k, v in delta.items():
                st.session_state.kpis[k] += v
            st.session_state.last_score = total
            st.session_state.assistant_msg = msg
            st.session_state.hard_fail = hard_fail
            st.rerun()

    with c2:
        if st.button("Next Round", use_container_width=True, disabled=st.session_state.hard_fail):
            st.session_state.round_index += 1
            st.session_state.assistant_msg = ""
            st.session_state.last_score = None
            st.session_state.hard_fail = False
            st.session_state.choice_clicked = None
            st.session_state.prompt_text = ""
            st.rerun()

    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Revenue", st.session_state.kpis["revenue"])
    m2.metric("Efficiency", st.session_state.kpis["efficiency"])
    m3.metric("Reputation", st.session_state.kpis["reputation"])
    m4.metric("Innovation", st.session_state.kpis["innovation"])

    st.info(f"**AI Assistant**: {st.session_state.assistant_msg or 'Waiting for your prompt…'}")

else:
    st.warning("Time’s up or rounds complete.")

    st.divider()
    st.subheader("Finish & Save Score")
    name = st.session_state.player_name.strip() or "Anonymous"
    if st.button(f"Save {name} to Leaderboard", type="primary"):
        add_leaderboard(name, st.session_state.score)
        st.success("Saved! Open the **Leaderboard** page to see standings.")
        st.page_link("pages/2_Leaderboard.py", label="Go to Leaderboard →")

    st.button("Play Again", on_click=lambda: reset_game(keep_name=True))
