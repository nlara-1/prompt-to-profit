# pages/2_Leaderboard.py
import time
import streamlit as st
from db import init_db, top10, standings

st.set_page_config(page_title="Leaderboard • P2P", page_icon="🏆", layout="wide")
init_db()

st.title("Leaderboard")

mode = st.radio("View Mode", ["Top 10", "Full Standings", "Podium"], horizontal=True)
auto = st.checkbox("Auto-refresh every 2 seconds", value=True)

def render_top10():
    rows = top10()
    st.table(rows if rows else [{"playerName":"—","totalScore":0,"createdAt":"—"}])

def render_full():
    rows = standings(200)
    st.dataframe(rows, use_container_width=True, hide_index=True)

def render_podium():
    rows = standings(3)
    st.markdown(
        """
        <style>
        .podium { display:flex; gap:24px; justify-content:center; align-items:flex-end; margin-top:24px; }
        .podium .card { background:#111; color:#fff; padding:24px; border-radius:16px; text-align:center; width:260px; }
        .podium .first { height:260px; }
        .podium .second { height:220px; opacity:0.9; }
        .podium .third { height:200px; opacity:0.85; }
        .name { font-size:1.25rem; font-weight:700; margin-top:8px; }
        .score { font-size:2rem; font-weight:800; }
        </style>
        """, unsafe_allow_html=True
    )
    names = [r["playerName"] for r in rows] if rows else []
    scores = [r["totalScore"] for r in rows] if rows else []

    def card(place_class, place, name, score):
        return f"""
        <div class="card {place_class}">
          <div style="font-size:1rem;opacity:0.8;">{place}</div>
          <div class="score">{score if name else "—"}</div>
          <div class="name">{name or "—"}</div>
        </div>
        """

    first = card("first", "1st", names[0] if len(names)>0 else "", scores[0] if len(scores)>0 else "")
    second = card("second", "2nd", names[1] if len(names)>1 else "", scores[1] if len(scores)>1 else "")
    third = card("third", "3rd", names[2] if len(names)>2 else "", scores[2] if len(scores)>2 else "")

    st.markdown(f"""<div class="podium">{second}{first}{third}</div>""", unsafe_allow_html=True)

placeholder = st.empty()

def render_once():
    with placeholder.container():
        if mode == "Top 10":
            render_top10()
        elif mode == "Full Standings":
            render_full()
        else:
            render_podium()

render_once()

# Optional auto-refresh loop (no deprecated APIs)
if auto:
    for _ in range(300):  # ~10 minutes max of auto-refresh
        time.sleep(2)
        render_once()
