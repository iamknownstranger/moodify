import streamlit.components.v1 as components
import streamlit as st
from spotify_client import track_meta_data, data, plt
# st.set_page_config(page_title="Moodify", layout="wide")
st.title("**Sekhar's recently played songs**")
# st.dataframe(track_meta_data)
# st.dataframe(data)


url = 'https://open.spotify.com/embed/track/'
for index, track in data.iterrows():
    with st.container():
        images, track_data = st.columns([2, 6])
        images.image(track.images)
        with track_data:
            # track_name, album_name = st.columns([3, 3])
            st.header(f'**{track.track_name}**')
            st.subheader(f'from **{track.album_name}**')

            with st.expander("Play on Spotify"):
                components.iframe(url + track.track_id)
 
st.header("Sekhar's **moodify** chart")
st.pyplot(plt)


hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                content:"Built with 💓 by Chandra Sekhar Mullu"; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 5px;
                top: 2px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
