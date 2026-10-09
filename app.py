"""
75 HARD — PyWebIO Tracker
=========================

A clean, minimal 75 Hard tracker with AdvaitAI branding.

SETUP
-----
    pip install pywebio

FILES
-----
    75hard_pywebio.py
    AdvaitAI_logo_trans(4).jpg

RUN
---
    python 75hard_pywebio.py

Then open:
    http://localhost:8080
"""

import json
import os
import base64

from pywebio import start_server
from pywebio.input import checkbox, textarea, input_group, actions
from pywebio.output import (
    put_html,
    put_markdown,
    put_buttons,
    put_scope,
    use_scope,
    clear_scope,
    toast,
    put_table,
    put_text,
)


# ============================================================
# FILES
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STATE_FILE = os.path.join(
    BASE_DIR,
    "75hard_state.json"
)

LOGO_FILE = os.path.join(
    BASE_DIR,
    "AdvaitAI_logo_trans.jpg"
)


# ============================================================
# TASKS
# ============================================================

TASK_DEFS = [
    (
        "diet",
        "Follow your diet",
        "No comfort meals."
    ),
    (
        "exercise",
        "Exercise — 1.5 hours",
        "Any form of exercise; choose what works for you."
    ),
    (
        "water",
        "Drink 1 gallon of water",
        "≈ 3.8 liters."
    ),
    (
        "read",
        "Read 10 pages",
        "Non-fiction / self-development."
    ),
]

# ============================================================
# STATE
# ============================================================

def default_state():

    return {
        "currentDay": 1,
        "attemptNumber": 1,
        "longestStreak": 0,
        "totalRestarts": 0,

        "todayTasks": {
            key: False
            for key, _, _ in TASK_DEFS
        },

        "todayNote": "",

        "history": [],
    }


def load_state():

    if not os.path.exists(STATE_FILE):
        return default_state()

    try:

        with open(
            STATE_FILE,
            "r",
            encoding="utf-8"
        ) as f:

            data = json.load(f)

        state = default_state()

        state.update(data)

        state["todayTasks"] = {
            **{
                key: False
                for key, _, _ in TASK_DEFS
            },
            **data.get("todayTasks", {}),
        }

        return state

    except Exception:

        return default_state()


def save_state(state):

    with open(
        STATE_FILE,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            state,
            f,
            indent=2
        )


# ============================================================
# LOGO
# ============================================================

def get_logo_html():

    """
    Converts the local logo into a base64 data URL.

    This means the browser doesn't need direct access
    to the local filesystem.
    """

    if not os.path.exists(LOGO_FILE):
        return ""

    try:

        with open(
            LOGO_FILE,
            "rb"
        ) as f:

            encoded = base64.b64encode(
                f.read()
            ).decode("utf-8")

        return f"""
        <img
            src="data:image/jpeg;base64,{encoded}"
            class="logo"
            alt="AdvaitAI"
        />
        """

    except Exception:

        return ""


# ============================================================
# CSS
# ============================================================

STYLE = """
<style>

/* -------------------------------------------
   GLOBAL
------------------------------------------- */

body {
    background: #f7f6f4;
    color: #252321;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        sans-serif;
}

.app {
    max-width: 720px;
    margin: 0 auto;
    padding: 28px 18px 60px;
}


/* -------------------------------------------
   ADVaitAI LOGO
------------------------------------------- */

.brand {
    margin-bottom: 26px;
}

.logo {
    width: 135px;
    height: auto;
    display: block;
}


/* -------------------------------------------
   HEADER
------------------------------------------- */

.header {
    margin-bottom: 25px;
}

.brand-label {
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    color: #918981;
    margin-bottom: 4px;
}

.day {
    font-size: 42px;
    font-weight: 800;
    letter-spacing: -1.8px;
    line-height: 1.1;
}

.attempt {
    color: #918981;
    font-size: 14px;
    margin-top: 5px;
}


/* -------------------------------------------
   PROGRESS BAR
------------------------------------------- */

.progress {
    margin-top: 19px;
}

.progress-track {
    width: 100%;
    height: 7px;
    background: #dedbd7;
    border-radius: 20px;
    overflow: hidden;
}

.progress-value {
    height: 100%;
    background: #b7472a;
    border-radius: 20px;
    transition: width 0.3s ease;
}

.progress-text {
    display: flex;
    justify-content: space-between;
    margin-top: 7px;
    font-size: 12px;
    color: #918981;
}


/* -------------------------------------------
   STATS
------------------------------------------- */

.stats {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    margin-bottom: 24px;
}

.stat {
    background: #ffffff;
    border: 1px solid #e5e1dc;
    border-radius: 12px;
    padding: 15px;
}

.stat-number {
    font-size: 23px;
    font-weight: 750;
    color: #252321;
}

.stat-label {
    font-size: 11px;
    color: #918981;
    margin-top: 3px;
}


/* -------------------------------------------
   SECTIONS
------------------------------------------- */

.section {
    background: #ffffff;
    border: 1px solid #e5e1dc;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 16px;
}

.section-title {
    font-size: 12px;
    font-weight: 750;
    letter-spacing: 1px;
    color: #746d66;
    margin-bottom: 15px;
}


/* -------------------------------------------
   PROGRESS WALL
------------------------------------------- */

.wall-75 {
    display: grid;
    grid-template-columns: repeat(15, 1fr);
    gap: 4px;
}

.brick {
    aspect-ratio: 2 / 1;
    background: #e3dfda;
    border-radius: 2px;
}

.brick.done {
    background: #b7472a;
}

.brick.today {
    background: #e8a33d;
}


/* -------------------------------------------
   COMPLETION
------------------------------------------- */

.complete {
    text-align: center;
    padding: 15px 5px;
}

.complete-icon {
    font-size: 34px;
    margin-bottom: 8px;
}

.complete-title {
    font-size: 22px;
    font-weight: 750;
}

.complete-sub {
    color: #918981;
    font-size: 14px;
    margin-top: 5px;
}


/* -------------------------------------------
   RESET
------------------------------------------- */

.reset-area {
    text-align: center;
    margin-top: 24px;
    padding-bottom: 10px;
}


/* -------------------------------------------
   MOBILE
------------------------------------------- */

@media (max-width: 600px) {

    .app {
        padding: 22px 14px 45px;
    }

    .logo {
        width: 115px;
    }

    .day {
        font-size: 34px;
    }

    .stats {
        gap: 7px;
    }

    .stat {
        padding: 12px 9px;
    }

    .stat-number {
        font-size: 19px;
    }

    .wall-75 {
        grid-template-columns: repeat(10, 1fr);
        gap: 4px;
    }
}

</style>
"""


# ============================================================
# PROGRESS WALL
# ============================================================

def render_wall(state):

    cells = ""

    for day in range(1, 76):

        if day < state["currentDay"]:

            css_class = "brick done"

        elif (
            day == state["currentDay"]
            and state["currentDay"] <= 75
        ):

            css_class = "brick today"

        else:

            css_class = "brick"

        cells += (
            f'<div '
            f'class="{css_class}" '
            f'title="Day {day}"'
            f'></div>'
        )

    return f"""
        <div class="wall-75">
            {cells}
        </div>
    """


# ============================================================
# HEADER
# ============================================================

def render_header(state):

    completed = min(
        state["currentDay"] - 1,
        75
    )

    percentage = round(
        (completed / 75) * 100
    )

    if state["currentDay"] > 75:

        day_text = "CHALLENGE COMPLETE"

    else:

        day_text = (
            f"DAY {state['currentDay']} / 75"
        )

    put_html(
        f"""
        <div class="header">

            <div class="brand">
                {get_logo_html()}
            </div>

            <div class="brand-label" style="
    font-size: 32px;
    font-weight: 800;
    letter-spacing: 2px;
    color: #252321;
    margin-bottom: 8px;
">
    PROTOCOL 75
</div>

<div style="
    font-size: 15px;
    font-weight: 500;
    color: #918981;
    letter-spacing: 0.3px;
    margin-bottom: 18px;
">
    Building discipline one day at a time.
</div>

            <div class="day">
                {day_text}
            </div>

            <div class="attempt">
                Attempt #{state["attemptNumber"]}
            </div>

            <div class="progress">

                <div class="progress-track">

                    <div
                        class="progress-value"
                        style="width:{percentage}%"
                    ></div>

                </div>

                <div class="progress-text">

                    <span>
                        {completed} of 75 days
                    </span>

                    <span>
                        {percentage}%
                    </span>

                </div>

            </div>

        </div>
        """
    )


# ============================================================
# STATS
# ============================================================

def render_stats(state):

    completed = min(
        state["currentDay"] - 1,
        75
    )

    longest = max(
        state["longestStreak"],
        completed
    )

    put_html(
        f"""
        <div class="stats">

            <div class="stat">

                <div class="stat-number">
                    {completed}
                </div>

                <div class="stat-label">
                    Completed
                </div>

            </div>


            <div class="stat">

                <div class="stat-number">
                    {longest}
                </div>

                <div class="stat-label">
                    Best Streak
                </div>

            </div>


            <div class="stat">

                <div class="stat-number">
                    {state["totalRestarts"]}
                </div>

                <div class="stat-label">
                    Restarts
                </div>

            </div>

        </div>
        """
    )


# ============================================================
# JOURNAL
# ============================================================

def render_log(state):

    if not state["history"]:

        put_text(
            "Your completed days will appear here."
        )

        return

    rows = [
        ["Day", "Attempt", "Note"]
    ]

    for item in state["history"][:20]:

        rows.append(
            [
                f'Day {item["day"]}',
                f'#{item["attempt"]}',
                item.get("note") or "—",
            ]
        )

    put_table(rows)


# ============================================================
# MAIN APP
# ============================================================

def main():

    state = load_state()


    # ========================================================
    # REDRAW
    # ========================================================

    def redraw():

        clear_scope("main")

        with use_scope("main"):

            put_html(
                '<div class="app">'
            )


            # HEADER
            render_header(state)


            # STATS
            render_stats(state)


            # =================================================
            # PROGRESS
            # =================================================

            put_html(
                """
                <div class="section">

                    <div class="section-title">
                        PROGRESS
                    </div>
                """
            )

            put_html(
                render_wall(state)
            )

            put_html(
                "</div>"
            )


            # =================================================
            # TODAY
            # =================================================

            if state["currentDay"] <= 75:

                put_html(
                    """
                    <div class="section">

                        <div class="section-title">
                            TODAY
                        </div>
                    """
                )

                put_buttons(
                    [
                        "Update Checklist"
                    ],
                    onclick=[
                        open_checklist
                    ],
                )

                put_html(
                    "</div>"
                )


            # =================================================
            # COMPLETE
            # =================================================

            else:

                put_html(
                    """
                    <div class="section">

                        <div class="complete">

                            <div class="complete-icon">
                                🏆
                            </div>

                            <div class="complete-title">
                                75 days complete.
                            </div>

                            <div class="complete-sub">
                                You actually did it.
                            </div>

                        </div>
                    """
                )

                put_buttons(
                    [
                        "Start New Round"
                    ],
                    onclick=[
                        start_new_round
                    ],
                )

                put_html(
                    "</div>"
                )


            # =================================================
            # JOURNAL
            # =================================================

            put_html(
                """
                <div class="section">

                    <div class="section-title">
                        JOURNAL
                    </div>
                """
            )

            render_log(state)

            put_html(
                "</div>"
            )


            # =================================================
            # RESET
            # =================================================

            put_html(
                """
                <div class="reset-area">
                """
            )

            put_buttons(
                [
                    "Reset Challenge"
                ],
                onclick=[
                    reset_challenge
                ],
            )

            put_html(
                "</div>"
            )


            put_html(
                "</div>"
            )


    # ========================================================
    # CHECKLIST
    # ========================================================

    def open_checklist():

        options = []

        for key, title, sub in TASK_DEFS:

            options.append(
                {
                    "label": (
                        f"{title} — {sub}"
                    ),

                    "value": key,

                    "selected": (
                        state["todayTasks"]
                        .get(key, False)
                    ),
                }
            )


        result = input_group(
            "Today's Rules",
            [

                checkbox(
                    "Completed today",
                    options=options,
                    name="tasks",
                ),

                textarea(
                    "Note (optional)",
                    name="note",
                    value=state["todayNote"],
                    rows=3,
                ),

            ],
        )


        checked = set(
            result["tasks"]
        )


        for key, _, _ in TASK_DEFS:

            state["todayTasks"][key] = (
                key in checked
            )


        state["todayNote"] = (
            result["note"]
        )


        save_state(state)


        # =====================================================
        # ALL TASKS COMPLETE
        # =====================================================

        if all(
            state["todayTasks"].values()
        ):

            choice = actions(
                "All rules are complete. Lock in today?",
                [
                    "Complete Day",
                    "Cancel",
                ],
            )

            if choice == "Complete Day":

                complete_day()


        # =====================================================
        # SOMETHING MISSED
        # =====================================================

        else:

            choice = actions(
                "Not all rules are complete.",
                [
                    "I Missed A Rule — Restart",
                    "Keep Going",
                    "Cancel",
                ],
            )

            if (
                choice
                == "I Missed A Rule — Restart"
            ):

                confirm = actions(
                    "This will reset you to Day 1. Are you sure?",
                    [
                        "Yes, restart",
                        "Cancel",
                    ],
                )

                if confirm == "Yes, restart":

                    restart_challenge()


        redraw()


    # ========================================================
    # COMPLETE DAY
    # ========================================================

    def complete_day():

        day = state["currentDay"]


        state["history"].insert(
            0,
            {
                "day": day,

                "attempt": (
                    state["attemptNumber"]
                ),

                "note": (
                    state["todayNote"]
                    .strip()
                ),
            },
        )


        state["longestStreak"] = max(
            state["longestStreak"],
            day,
        )


        # MOVE TO NEXT DAY
        state["currentDay"] += 1


        # RESET TODAY
        state["todayTasks"] = {
            key: False
            for key, _, _ in TASK_DEFS
        }

        state["todayNote"] = ""


        save_state(state)


        if day == 75:

            toast(
                "🏆 75 HARD COMPLETE!",
                color="success",
            )

        else:

            toast(
                f"Day {day} complete.",
                color="success",
            )


    # ========================================================
    # RESTART AFTER MISSED RULE
    # ========================================================

    def restart_challenge():

        state["longestStreak"] = max(
            state["longestStreak"],
            state["currentDay"] - 1,
        )


        state["history"].insert(
            0,
            {
                "day": state["currentDay"],

                "attempt": (
                    state["attemptNumber"]
                ),

                "note": (
                    "⚠ Restarted — missed a rule."
                    + (
                        " "
                        + state["todayNote"].strip()
                        if state["todayNote"].strip()
                        else ""
                    )
                ),
            },
        )


        state["totalRestarts"] += 1

        state["attemptNumber"] += 1

        state["currentDay"] = 1


        state["todayTasks"] = {
            key: False
            for key, _, _ in TASK_DEFS
        }

        state["todayNote"] = ""


        save_state(state)


        toast(
            f"Restarted — Attempt #{state['attemptNumber']}",
            color="warn",
        )


    # ========================================================
    # RESET EVERYTHING
    # ========================================================

    def reset_challenge():

        confirm = actions(
            "⚠ Reset the entire challenge?",
            [
                "Yes, Reset Everything",
                "Cancel",
            ],
        )


        if confirm != "Yes, Reset Everything":

            return


        # Completely reset state
        state.clear()

        state.update(
            default_state()
        )


        save_state(state)


        toast(
            "Challenge reset.",
            color="warn",
        )


        # IMPORTANT:
        # Redraw immediately so all numbers
        # update on screen.
        redraw()


    # ========================================================
    # START NEW ROUND
    # ========================================================

    def start_new_round():

        state["attemptNumber"] += 1

        state["currentDay"] = 1

        state["todayTasks"] = {
            key: False
            for key, _, _ in TASK_DEFS
        }

        state["todayNote"] = ""


        save_state(state)


        toast(
            f"Attempt #{state['attemptNumber']} started.",
            color="success",
        )


        redraw()


    # ========================================================
    # START
    # ========================================================

    put_html(STYLE)

    put_scope("main")

    redraw()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":

    start_server(
        main,
        port=8080,
        debug=True,
    )
