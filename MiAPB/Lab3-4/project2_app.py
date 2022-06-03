import streamlit as st
from alpha_alg import AlphaAlgorithm
from alpha_loop_alg import AlphaAlgorithm_loop
import graphviz
import copy
import pydot
import io
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

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


def project2():
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
        alpha = AlphaAlgorithm()
        alpha.read_log_file(uploaded_file)
        alpha.build_model()
        graph = alpha.create_graph(filename=None, show=False)
        graph_, = pydot.graph_from_dot_data(graph.source)
        png_str = graph_.create_png(prog='dot')

        # treat the DOT output as an image file
        sio = io.BytesIO()
        sio.write(png_str)
        sio.seek(0)
        st.image(sio)
    else:
        alpha = AlphaAlgorithm_loop(thresh_direct_followers=input_df['th_d_followers'],
                                    thresh_parallel=input_df['th_par'], thresh_oneloop=input_df['th_oneloop'])
        alpha.read_log_file(uploaded_file)
        alpha.build_model()
        graph = alpha.create_graph(filename=None, show=False)
        graph_, = pydot.graph_from_dot_data(graph.source)
        png_str = graph_.create_png(prog='dot')

        # treat the DOT output as an image file
        sio = io.BytesIO()
        sio.write(png_str)
        sio.seek(0)
        st.image(sio)

    st.subheader('User Output - text DOT')
    st.markdown(graph_)


