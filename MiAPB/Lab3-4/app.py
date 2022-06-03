import streamlit as st
from project2_app import project2
from project1_app import project1
from streamlit_option_menu import option_menu


def main():
    # 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
    EXAMPLE_NO = 2

    def streamlit_menu(example=3):
        if example == 1:
            # 1. as sidebar menu
            with st.sidebar:
                selected = option_menu(
                    menu_title="Main Menu",  # required
                    options=["Home", "Project 1", "Project 2"],  # required
                    icons=["house", "book", "book"],  # optional
                    menu_icon="cast",  # optional
                    default_index=0,  # optional
                )
            return selected

        if example == 2:
            # 2. horizontal menu w/o custom style
            selected = option_menu(
                menu_title=None,  # required
                options=["Home", "Project 1", "Project 2"],  # required
                icons=["house", "book", "book"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal",
            )
            return selected

        if example == 3:
            # 2. horizontal menu with custom style
            selected = option_menu(
                menu_title=None,  # required
                options=["Home", "Project 1", "Project 2"],  # required
                icons=["house", "book", "book"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal",
                styles={
                    "container": {"padding": "0!important", "background-color": "#fafafa"},
                    "icon": {"color": "orange", "font-size": "25px"},
                    "nav-link": {
                        "font-size": "25px",
                        "text-align": "left",
                        "margin": "0px",
                        "--hover-color": "#eee",
                    },
                    "nav-link-selected": {"background-color": "green"},
                },
            )
            return selected

    selected = streamlit_menu(example=EXAMPLE_NO)

    if selected == "Home":
        st.markdown("<h3 style='text-align: left; color: white; margin-right: -50%;'>Wykonane przez:</h3>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: left; color: white; margin-right: -50%;'>Kamil Baradziej</h5>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: left; color: white; margin-right: -50%;'>Iga Chudzikiewicz</h5>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: left; color: white; margin-right: -50%;'>Nicolas Duc</h5>", unsafe_allow_html=True)

    if selected == "Project 1":
        st.markdown("<h1 style='text-align: center; color: red;'>Process mining</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: white; margin-right: -50%;'>Choose configuration and have fun with process mining!</h3>",unsafe_allow_html=True)
        project1()
    if selected == "Project 2":
        st.markdown("<h1 style='text-align: center; color: red;'>Alpha Algorithm</h1>", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: left; color: white; margin-right: -50%;'>Choose configuration and have fun with making modern graph models!</h3>", unsafe_allow_html=True)
        project2()


if __name__=="__main__":
    main()





