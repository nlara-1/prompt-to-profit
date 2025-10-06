# P2P.py
import time
import streamlit as st
from content import ROUNDS
from scoring import score_prompt, kpi_delta
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
    ss.setdefault("last_score", None)
    ss.setdefault("assistant_msg", "")
    ss.setdefault("hard_fail", False)
    ss.setdefault("start_time", time.time())
    ss.setdefault("choice_clicked", None)
    ss.setdefault("prompt_text", "")
    ss.setdefault("timer_running", True)
    ss.setdefault("round_submitted", False)
    ss.setdefault("_last_tick", 0.0)

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
left, right = st.columns([2, 1])
with left:
    st.title("Prompt to Profit (P2P)")
    st.caption("Test your business instincts and AI skills across Finance, Marketing, Management, and Analytics.")
with right:
    started = (get_start_now() == 1)
    ended = (get_end_now() == 1)
    tl = seconds_left() if started and not ended else TOTAL_SECONDS
    st.metric("⏱ Time Left", f"{tl//60:02d}:{tl%60:02d}")
    st.metric("Total Score", st.session_state.score)

st.divider()

# ---------- Join ----------
if not st.session_state.joined:
    st.subheader("Join the Game")
    st.session_state.player_name = st.text_input("Enter your display name to join", placeholder="e.g., Jordan", max_chars=32)
    if st.button("Join"):
        if st.session_state.player_name.strip():
            st.session_state.joined = True
            st.success(f"Welcome, {st.session_state.player_name}!")
            st.rerun()
        else:
            st.error("Please enter a name to join.")
    st.stop()

# Lobby waiting screen
if get_start_now() == 0 and get_end_now() == 0:
    st.info("Waiting for the admin to start the game…")
    st.button("Refresh", on_click=lambda: st.rerun())
    st.stop()

# Admin has ended game
if get_end_now() == 1:
    st.warning("The admin has ended the game.")
    st.session_state.timer_running = False

time_left = seconds_left() if get_end_now() == 0 else 0
in_rounds = st.session_state.round_index < len(ROUNDS)


def apply(score: int, delta: dict, msg: str, hard_fail: bool):
    st.session_state.score += score
    for k, v in delta.items():
        st.session_state.kpis[k] += v
    st.session_state.last_score = score
    st.session_state.assistant_msg = msg
    st.session_state.hard_fail = hard_fail
    st.session_state.round_submitted = True


# ---------- GAMEPLAY ----------
if (time_left > 0) and in_rounds:
    round_obj = ROUNDS[st.session_state.round_index]

    st.subheader(f"Round {round_obj['id']}: {round_obj['department']}")
    st.markdown(f"**Scenario:** {round_obj['scenario']}")
    st.write(f"**Objective:** {round_obj['objective']}")

    st.markdown("### Quick Options")
    cols = st.columns(3)
    for i, ch in enumerate(round_obj["choices"]):
        with cols[i]:
            st.caption(ch["text"])
            disabled = st.session_state.round_submitted
            if st.button(f"Option {ch['key']}", key=f"opt_{round_obj['id']}_{ch['key']}", disabled=disabled):
                if not st.session_state.round_submitted:
                    total = ch["presetScore"]
                    hard_fail = total <= -8
                    msg = (
                        f"Rowdy gives you {total} points. "
                        f"That’s because this choice {'balances insight and clarity well' if total >= 6 else 'shows effort but misses some key reasoning' if total >= 3 else 'is too surface-level for a confident business decision'}."
                    )
                    delta = kpi_delta(total, round_obj["weights"])
                    apply(total, delta, msg, hard_fail)
                    st.rerun()

    st.markdown("### Or Write Your Own Prompt")
    st.session_state.prompt_text = st.text_area(
        "Your custom prompt",
        key=f"prompt_{round_obj['id']}",
        height=160,
        placeholder="Write a detailed and professional AI prompt here...",
        value=st.session_state.prompt_text,
        disabled=st.session_state.round_submitted,
    )

    c1, c2 = st.columns([1, 1])
    with c1:
        if st.button(
            "Submit Prompt",
            type="primary",
            use_container_width=True,
            disabled=(len(st.session_state.prompt_text.strip()) == 0) or st.session_state.round_submitted,
        ):
            if not st.session_state.round_submitted:
                used_text = st.session_state.prompt_text.strip()
                total, _, hard_fail, tips, explanation = score_prompt(used_text)
                msg = (
                    f"Rowdy gives you {total} points. "
                    f"{explanation} {' '.join(tips) if tips else ''}"
                )
                delta = kpi_delta(total, round_obj["weights"])
                apply(total, delta, msg, hard_fail)
                st.rerun()

    with c2:
        if st.button(
            "Next Round",
            use_container_width=True,
            disabled=st.session_state.hard_fail or (not st.session_state.round_submitted),
        ):
            st.session_state.round_index += 1
            st.session_state.assistant_msg = ""
            st.session_state.last_score = None
            st.session_state.hard_fail = False
            st.session_state.choice_clicked = None
            st.session_state.prompt_text = ""
            st.session_state.round_submitted = False
            st.rerun()

    st.divider()
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Revenue", st.session_state.kpis["revenue"])
    m2.metric("Efficiency", st.session_state.kpis["efficiency"])
    m3.metric("Reputation", st.session_state.kpis["reputation"])
    m4.metric("Innovation", st.session_state.kpis["innovation"])

    st.info(f"**Rowdy says:** {st.session_state.assistant_msg or 'Ready when you are!'}")

else:
    st.warning("Time’s up or you’ve completed all rounds.")
    st.divider()
    st.subheader("Finish & Save Score")
    name = st.session_state.player_name.strip() or "Anonymous"
    if st.button(f"Save {name} to Leaderboard", type="primary"):
        add_leaderboard(name, st.session_state.score)
        st.success("Saved! Visit the Leaderboard to view rankings.")
        st.page_link("pages/2_Leaderboard.py", label="Go to Leaderboard →")
    st.button("Play Again", on_click=lambda: reset_game(keep_name=True))


# ---------- SAFE AUTO-REFRESH ----------
started = (get_start_now() == 1)
ended = (get_end_now() == 1)
if started and not ended and st.session_state.timer_running:
    now = time.time()
    if now - st.session_state._last_tick >= 1.0:
        st.session_state._last_tick = now
        st.rerun()
