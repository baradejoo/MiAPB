import streamlit as st
from proces_mining import adv_modify_w_net_task_dur
import graphviz
import pydot
import io


def user_input_features():
    alg = st.sidebar.selectbox('Algorithm', ('Alpha', 'AlphaOneLoop'))
    if alg == "AlphaOneLoop":
        thresh_direct_followers = st.sidebar.slider('Threshold direct followers', 0.0, 1.0, 0.5)
        thresh_parallel = st.sidebar.slider('Threshold parallel', 0.0, 1.0, 0.5)
        thresh_oneloop = st.sidebar.slider('Threshold one-loop', 0.0, 1.0, 0.5)
        data = {'alg': 'AlphaOneLoop',
                'th_d_followers': thresh_direct_followers,
                'th_par': thresh_parallel,
                'th_oneloop': thresh_oneloop}
    else:
        data = {'alg': 'Alpha',
                'th_d_followers': None,
                'th_par': None,
                'th_oneloop': None}

    return data


def project1():
    st.sidebar.header('User Input Features')

    st.sidebar.markdown("""
    [Example CSV input file](https://facebook.pl)
    """) #wrzucic jakis na gita csv przykladowa

    input_df = {'alg': None,
            'th_d_followers': None,
            'th_par': None,
            'th_oneloop': None}
    # Collects user input features into dataframe
    uploaded_file = st.sidebar.file_uploader("Upload your input CSV file (Only one !)", type=["csv"])
    if uploaded_file is not None:
        input_df = user_input_features()

    # Displays the user input features
    st.subheader('User Output - image')
    graph_ = 'Awaiting CSV file to be uploaded...'
    if input_df['alg'] is None:
        st.write('Awaiting CSV file to be uploaded...')
    elif input_df['alg'] == 'Alpha':

        G = adv_modify_w_net_task_dur(10,300, uploaded_file)
        sio = io.BytesIO()
        sio.write(G)
        sio.seek(0)
        st.image(sio)
    else:
        pass
