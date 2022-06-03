import streamlit as st
from proces_mining import adv_modify_w_net_task_dur
import graphviz
import pydot
import io


def user_input_features():
    thresh_edge = st.sidebar.slider('Threshold edge filter', 0.0, 100.0, 2000.0)
    thresh_event = st.sidebar.slider('Threshold event filter', 0.0, 100.0, 2000.0)
    data = {'th_edge': thresh_edge,
            'th_event': thresh_event,
            }

    return data


def project1():
    st.sidebar.header('User Input Features')

    st.sidebar.markdown("""
    [Example CSV input file](https://facebook.pl)
    """) #wrzucic jakis na gita csv przykladowa

    input_df = {'th_edge': None,
                'th_event': None,
                }
    # Collects user input features into dataframe
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file (Only one !)", type=["csv"])
    if uploaded_file is not None:
        input_df = user_input_features()

    # Displays the user input features
    st.subheader('User Output - image')
    graph_ = 'Awaiting CSV file to be uploaded...'
    if input_df['th_edge'] is None:
        st.write('Awaiting CSV file to be uploaded...')
    else:
        G = adv_modify_w_net_task_dur(input_df['th_edge'], input_df['th_event'], uploaded_file)
        sio = io.BytesIO()
        sio.write(G)
        sio.seek(0)
        st.image(sio)

