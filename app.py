import random
import time

import streamlit as st

from randselect.selector import random_selection, selection_without_repeats

FLASH_SECONDS = 3.0
FLASH_INTERVAL = 0.1

state = st.session_state
state.setdefault("names", [])
state.setdefault("questions", [])
state.setdefault("history", [])  # every (name, question) drawn this session
state.setdefault("current", None)  # the pick currently on screen
state.setdefault("animate", False)  # flash before revealing `current`
state.setdefault("message", None)
state.setdefault("rng", random.Random())

st.title("Random Question Picker")


def add_item(list_key, text):
    item = text.strip()
    if not item:
        state.message = ("warning", "Enter something before clicking Add.")
    elif item in state[list_key]:
        state.message = ("warning", f"'{item}' is already in the list.")
    else:
        state[list_key].append(item)


def item_list(title, list_key, form_key):
    st.subheader(title)
    with st.form(form_key, clear_on_submit=True):
        text = st.text_input(f"New {title.lower()[:-1]}")
        if st.form_submit_button("Add"):
            add_item(list_key, text)
    if state[list_key]:
        for item in state[list_key]:
            st.markdown(f"- {item}")
    else:
        st.caption("Nothing added yet.")


left, right = st.columns(2)
with left:
    item_list("Names", "names", "add_name")
with right:
    item_list("Questions", "questions", "add_question")

st.divider()

no_repeats = st.checkbox("No repeats (this session)", value=False)
draw_col, reset_col = st.columns(2)

if draw_col.button("Draw", type="primary"):
    if not state.names or not state.questions:
        state.message = ("error", "Add at least one name and one question first.")
    else:
        if no_repeats:
            used_names = {n for n, _ in state.history}
            used_questions = {q for _, q in state.history}
            pick = selection_without_repeats(
                state.names, state.questions, used_names, used_questions, state.rng
            )
        else:
            pick = random_selection(state.names, state.questions, state.rng)

        if pick is None:
            state.message = (
                "warning",
                "Everyone or every question has already been drawn. "
                "Add more, reset history, or turn off 'No repeats'.",
            )
        else:
            state.current = pick
            state.history.append(pick)
            state.animate = True

if reset_col.button("Reset history"):
    state.history = []
    state.current = None

# --- Rendering: reads session state only ---

if state.message:
    kind, text = state.message
    getattr(st, kind)(text)
    state.message = None

result = st.empty()


def show_pair(name, question):
    result.markdown(f"### {name}, please answer:\n\n## {question}")


if state.current:
    if state.animate:
        state.animate = False
        end = time.monotonic() + FLASH_SECONDS
        while time.monotonic() < end:
            show_pair(*random_selection(state.names, state.questions, state.rng))
            time.sleep(FLASH_INTERVAL)
    show_pair(*state.current)

if state.history:
    with st.expander(f"Draw history ({len(state.history)})"):
        for i, (name, question) in enumerate(state.history, 1):
            st.markdown(f"{i}. **{name}** — {question}")
