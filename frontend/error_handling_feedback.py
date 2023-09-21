```python
import streamlit as st

def show_feedback(message_name, message_content):
    if "success" in message_name:
        st.success(message_content)
    elif "failure" in message_name:
        st.error(message_content)

def handle_error(error):
    st.error(f"An error occurred: {error}")

def update_progress(progress, message):
    with st.spinner(message):
        st.progress(progress)
```
