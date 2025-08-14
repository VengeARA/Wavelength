# %% PHASE 1: Menu & Mode Selection (+ Category Support)
import streamlit as st
import matplotlib.pyplot as plt
import random

st.set_page_config(page_title="Wavelength", page_icon="📶", layout="centered")
# -------------------------
# SESSION STATE INIT
# -------------------------
if "phase" not in st.session_state:
    st.session_state.phase = "menu"
if "mode" not in st.session_state:
    st.session_state.mode = None
if "mode_color" not in st.session_state:
    st.session_state.mode_color = None
if "win_points" not in st.session_state:
    st.session_state.win_points = None
if "scores" not in st.session_state:
    st.session_state.scores = {"Team": 0, "Team 1": 0, "Team 2": 0}
if "topic" not in st.session_state:
    st.session_state.topic = None  # (left, right)
if "current_team" not in st.session_state:
    st.session_state.current_team = "Team 1"  # First turn defaults to Team 1
if "points_awarded" not in st.session_state:
    st.session_state.points_awarded = False

# -------------------------
# TITLE
# -------------------------
st.markdown("<h1 style='color:cyan; text-align:center;'>Wavelength</h1>", unsafe_allow_html=True)

# -------------------------
# SCORE + MODE + TOPIC DISPLAY
# -------------------------
if st.session_state.mode:
    # Mode label color
    st.markdown(
        f"<p style='font-size:18px; color:{'lime' if st.session_state.mode=='Co-op' else 'orange'}; margin:0;'>"
        f"{st.session_state.mode}</p>",
        unsafe_allow_html=True
    )
    # Score display
    if st.session_state.mode == "Co-op":
        st.markdown(
            f"<p style='font-size:18px; color:lime; margin:0;'>Score: {st.session_state.scores['Team']}"
            f"{'' if not st.session_state.win_points else f' / {st.session_state.win_points}'}</p>",
            unsafe_allow_html=True
        )
    elif st.session_state.mode == "Team Battle":
        score_text = f"Team 1: {st.session_state.scores['Team 1']} | Team 2: {st.session_state.scores['Team 2']}"
        st.markdown(
            f"<p style='font-size:18px; color:orange; margin:0;'>{score_text}"
            f"{'' if not st.session_state.win_points else f'  (to {st.session_state.win_points})'}</p>",
            unsafe_allow_html=True
        )
        st.caption(f"Current Turn: {st.session_state.current_team}")

    # Topic label (if chosen)
    if st.session_state.topic:
        left_extreme, right_extreme = st.session_state.topic
        st.markdown(
            f"<p style='font-size:16px; color:#777; margin:4px 0 12px 0;'>"
            f"Topic: <strong>{left_extreme}</strong> ↔ <strong>{right_extreme}</strong></p>",
            unsafe_allow_html=True
        )

# -------------------------
# PHASE: MENU SCREEN
# -------------------------
if st.session_state.phase == "menu":
    if st.button("Start Game"):
        st.session_state.phase = "mode_select"
        st.rerun()

# -------------------------
# PHASE: MODE SELECTION
# -------------------------
elif st.session_state.phase == "mode_select":
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Co-op", key="co_op", use_container_width=True):
            st.session_state.mode = "Co-op"
            st.session_state.mode_color = "lime"
            st.session_state.scores = {"Team": 0}
            st.session_state.topic = None
            st.session_state.phase = "win_points"
            st.rerun()
    with col2:
        if st.button("Team Battle", key="team_battle", use_container_width=True):
            st.session_state.mode = "Team Battle"
            st.session_state.mode_color = "orange"
            st.session_state.scores = {"Team 1": 0, "Team 2": 0}
            st.session_state.topic = None
            st.session_state.current_team = "Team 1"
            st.session_state.phase = "win_points"
            st.rerun()

# -------------------------
# PHASE: WINNING POINTS
# -------------------------
elif st.session_state.phase == "win_points":
    win_points = st.number_input("Points to Win", min_value=10, value=10, step=1)
    if st.button("Confirm Winning Points"):
        st.session_state.win_points = win_points
        st.session_state.phase = "category_select"
        st.rerun()

# -------------------------
# PHASE 2: CATEGORY SELECTION
# -------------------------
elif st.session_state.phase == "category_select":
    st.subheader("Choose a Topic:")
    topics = [
        ("Disgusting food", "Delicious food"),
        ("Unhealthy habits", "Healthy habits"),
        ("Unnecessary activities", "Necessary activities"),
        ("Common", "Rare"),
        ("Risky", "Safe"),
    ]

    cols = st.columns(2)
    for i, (left, right) in enumerate(topics):
        with cols[i % 2]:
            if st.button(f"{left} ↔ {right}", use_container_width=True):
                st.session_state.topic = (left, right)
                st.session_state.phase = "topic_select"
                st.rerun()

# %% PHASE 3: Select Target & Generate Segments
elif st.session_state.phase == "topic_select":
    four_left_boundary = random.randint(4, 174)
    points_pattern = [2, 3, 4, 3, 2]
    segments = []
    start = four_left_boundary - 4
    for p in points_pattern:
        seg_start = max(0, start)
        seg_end = min(180, start + 2)
        segments.append((seg_start, seg_end, p))
        start += 2

    st.session_state.segments = segments
    st.session_state.points_awarded = False
    st.session_state.phase = "leader_view"
    st.rerun()

# %% PHASE 4: Leader Views the Dial
elif st.session_state.phase == "leader_view":
    st.subheader("Leader: Look at the dial and give your hint!")
    if st.session_state.topic:
        left_extreme, right_extreme = st.session_state.topic
        st.caption(f"Scale: {left_extreme} ↔ {right_extreme}")

    fig, ax = plt.subplots(figsize=(8, 2))
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 1)
    ax.axis("off")

    for start, end, points in st.session_state.segments:
        color = "#fff4b3" if points == 2 else "#ffb3b3" if points == 3 else "#b3c6ff"
        ax.fill_betweenx([0, 1], start, end, color=color)
        ax.text((start + end) / 2, 0.5, str(points),
                ha="center", va="center", fontsize=14, fontweight="bold")

    st.pyplot(fig)

    if st.button("I've seen it"):
        st.session_state.phase = "co_op_guess"
        st.rerun()

# %% PHASE 5: Guess
elif st.session_state.phase == "co_op_guess":
    st.subheader("Move the hand to where you think the target is!")
    if st.session_state.topic:
        left_extreme, right_extreme = st.session_state.topic
        st.caption(f"Scale: {left_extreme} ↔ {right_extreme}")

    slider_val = st.slider("Move hand", 0.0, 10.0, 5.0, 0.1)
    hand_angle = (slider_val / 10) * 180
    st.session_state.hand_angle = hand_angle

    fig, ax = plt.subplots(figsize=(8, 2))
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.plot([hand_angle, hand_angle], [0, 1], color="black", linewidth=2)
    st.pyplot(fig)

    if st.button("Confirm Guess"):
        st.session_state.phase = "co_op_reveal"
        st.rerun()

# %% PHASE 6: Reveal & Score
elif st.session_state.phase == "co_op_reveal":
    if st.session_state.topic:
        left_extreme, right_extreme = st.session_state.topic
        st.caption(f"Scale: {left_extreme} ↔ {right_extreme}")

    fig, ax = plt.subplots(figsize=(8, 2))
    ax.set_xlim(0, 180)
    ax.set_ylim(0, 1)
    ax.axis("off")

    for start, end, points in st.session_state.segments:
        color = "#fff4b3" if points == 2 else "#ffb3b3" if points == 3 else "#b3c6ff"
        ax.fill_betweenx([0, 1], start, end, color=color)
        ax.text((start + end) / 2, 0.5, str(points),
                ha="center", va="center", fontsize=14, fontweight="bold")

    hand_angle = st.session_state.hand_angle
    ax.plot([hand_angle, hand_angle], [0, 1], color="black", linewidth=2)
    st.pyplot(fig)

    if not st.session_state.points_awarded:
        earned = 0
        for start, end, p in st.session_state.segments:
            if start <= hand_angle <= end:
                earned = p
                break

        if earned == 0:
            st.warning("Oof, tough luck!")
        elif earned == 2:
            st.success("Nice shot! +2 points")
        elif earned == 3:
            st.success("Great guess! +3 points")
        elif earned == 4:
            st.success("Perfect hit! +4 points")

        if st.session_state.mode == "Co-op":
            st.session_state.scores["Team"] += earned
        elif st.session_state.mode == "Team Battle":
            st.session_state.scores[st.session_state.current_team] += earned
            st.session_state.current_team = "Team 2" if st.session_state.current_team == "Team 1" else "Team 1"

        st.session_state.points_awarded = True

    # Win check
    if st.session_state.mode == "Co-op":
        if st.session_state.scores["Team"] >= st.session_state.win_points:
            st.balloons()
            st.success(f"🎉 Congratulations! You reached {st.session_state.win_points} points!")
            st.session_state.phase = "game_over"
    elif st.session_state.mode == "Team Battle":
        for team in ["Team 1", "Team 2"]:
            if st.session_state.scores[team] >= st.session_state.win_points:
                st.balloons()
                st.success(f"🎉 {team} wins with {st.session_state.scores[team]} points!")
                st.session_state.phase = "game_over"
                break

    if st.session_state.phase != "game_over" and st.button("Next Round"):
        st.session_state.phase = "topic_select"
        st.rerun()

# PHASE: GAME OVER
elif st.session_state.phase == "game_over":
    st.markdown("<h2 style='color:cyan; text-align:center;'>Game Over</h2>", unsafe_allow_html=True)
    if st.session_state.mode == "Co-op":
        st.write(f"Final Score: {st.session_state.scores['Team']} points")
    else:
        st.write(f"Final Scores - Team 1: {st.session_state.scores['Team 1']} | Team 2: {st.session_state.scores['Team 2']}")
    if st.button("Play Again"):
        st.session_state.phase = "menu"
        st.session_state.mode = None
        st.session_state.mode_color = None
        st.session_state.win_points = None
        st.session_state.scores = {"Team": 0, "Team 1": 0, "Team 2": 0}
        st.session_state.topic = None
        st.session_state.points_awarded = False
        st.session_state.current_team = "Team 1"
        st.rerun()
