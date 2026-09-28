import random
import time

import streamlit as st

from randselect.selector import available_choices, random_selection

st.title("Random Name & Question Picker")

if "names" not in st.session_state:
    st.session_state.names = []
if "questions" not in st.session_state:
    st.session_state.questions = []
if "used_names" not in st.session_state:
    st.session_state.used_names = set()
if "used_questions" not in st.session_state:
    st.session_state.used_questions = set()
if "last_pick" not in st.session_state:
    st.session_state.last_pick = None

col1, col2 = st.columns(2)

with col1:
    st.subheader("Names")
    with st.form("add_name_form", clear_on_submit=True):
        new_name = st.text_input("New name")
        add_name = st.form_submit_button("Add name")
        if add_name:
            new_name = new_name.strip()
            if new_name and new_name not in st.session_state.names:
                st.session_state.names.append(new_name)
    st.write(st.session_state.names or "_No names yet._")

with col2:
    st.subheader("Questions")
    with st.form("add_question_form", clear_on_submit=True):
        new_question = st.text_input("New question")
        add_question = st.form_submit_button("Add question")
        if add_question:
            new_question = new_question.strip()
            if new_question and new_question not in st.session_state.questions:
                st.session_state.questions.append(new_question)
    st.write(st.session_state.questions or "_No questions yet._")

no_repeats = st.checkbox("No repeats")

available_names = available_choices(
    st.session_state.names,
    st.session_state.used_names if no_repeats else (),
)
available_questions = available_choices(
    st.session_state.questions,
    st.session_state.used_questions if no_repeats else (),
)

if no_repeats and st.session_state.names and not available_names:
    st.warning("All names are selected!")
if no_repeats and st.session_state.questions and not available_questions:
    st.warning("All questions are selected!")

draw_disabled = (
    not st.session_state.names
    or not st.session_state.questions
    or not available_names
    or not available_questions
)

if st.button("Draw", disabled=draw_disabled):
    placeholder = st.empty()
    end_time = time.time() + 3
    while time.time() < end_time:
        flash_name, flash_question = random_selection(
            st.session_state.names, st.session_state.questions, random
        )
        placeholder.markdown(f"**{flash_name}**, please answer: {flash_question}")
        time.sleep(0.1)
    placeholder.empty()

    kwargs = {}
    if no_repeats:
        kwargs["used_names"] = st.session_state.used_names
        kwargs["used_questions"] = st.session_state.used_questions
    chosen_name, chosen_question = random_selection(
        st.session_state.names, st.session_state.questions, random, **kwargs
    )
    st.session_state.last_pick = (chosen_name, chosen_question)
    if no_repeats:
        st.session_state.used_names.add(chosen_name)
        st.session_state.used_questions.add(chosen_question)

if st.session_state.last_pick:
    name, question = st.session_state.last_pick
    st.success(f"{name}, please answer: {question}")
