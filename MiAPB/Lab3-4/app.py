import streamlit as st
from alpha_alg import AlphaAlgorithm
from project2_app import project2
def main():
    import streamlit as st
    from streamlit_option_menu import option_menu

    # 1=sidebar menu, 2=horizontal menu, 3=horizontal menu w/ custom menu
    EXAMPLE_NO = 2

    def streamlit_menu(example=3):
        if example == 1:
            # 1. as sidebar menu
            with st.sidebar:
                selected = option_menu(
                    menu_title="Main Menu",  # required
                    options=["Home", "Project 1", "Project 2", "Contact"],  # required
                    icons=["house", "book", "book", "envelope"],  # optional
                    menu_icon="cast",  # optional
                    default_index=0,  # optional
                )
            return selected

        if example == 2:
            # 2. horizontal menu w/o custom style
            selected = option_menu(
                menu_title=None,  # required
                options=["Home", "Project 1", "Project 2", "Contact"],  # required
                icons=["house", "book", "book", "envelope"],  # optional
                menu_icon="cast",  # optional
                default_index=0,  # optional
                orientation="horizontal",
            )
            return selected

        if example == 3:
            # 2. horizontal menu with custom style
            selected = option_menu(
                menu_title=None,  # required
                options=["Home", "Project 1", "Project 2", "Contact"],  # required
                icons=["house", "book", "book", "envelope"],  # optional
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
        st.title(f"You have selected {selected}")
    if selected == "Project 1":
        st.title(f"You have selected {selected}")
    if selected == "Project 2":
        st.markdown("<h1 style='text-align: center; color: red;'>Alpha Algorithm</h1>", unsafe_allow_html=True)
        st.markdown("<h5 style='text-align: left; color: white;'>Choose configuration and have fun with making modern graph models!</h5>", unsafe_allow_html=True)
        project2()
    if selected == "Contact":
        st.title(f"You have selected {selected}")
    # uploaded_files = st.file_uploader("Upload multiple files", accept_multiple_files=True)
    #
    # if uploaded_files:
    #     for uploaded_file in uploaded_files:
    #         st.write("Filename: ", uploaded_file.name)
    #
    #
    # st.sidebar.title("What to do")
    # app_mode = st.sidebar.selectbox("Choose the app mode",
    #     ["Show instructions", "Run the app", "Show the source code"])
    # if app_mode == "Show instructions":
    #     st.sidebar.success('To continue select "Run the app".')
    # elif app_mode == "Show the source code":
    #     pass
    #     # readme_text.empty()
    #     # st.code(get_file_content_as_string("streamlit_app.py"))
    # elif app_mode == "Run the app":
    #     pass
    #     # readme_text.empty()
    #     # run_the_app()

if __name__=="__main__":
    main()
    # show = False
    # alpha = AlphaAlgorithm()
    # alpha.read_log_file(f'benchmark-logs-setA/A3.xes')
    # alpha.build_model()
    # p = alpha.create_graph(filename=None, show=show)
    # print(p)




