import streamlit as st
def update_first():
    st.session_state.second = st.session_state.first

def update_second():
    st.session_state.first = st.session_state.second

st.title('🪞 Mirrored Widgets using Session State')

st.text_input(label='Textbox 1', key='first', on_change=update_first)
st.text_input(label='Textbox 2', key='second', on_change=update_second)