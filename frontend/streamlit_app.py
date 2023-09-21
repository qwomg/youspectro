```python
import streamlit as st
from streamlit_oauth import OAuth
from backend import spectrogram_generation, video_creation, youtube_upload, authentication, async_tasks
from frontend import error_handling_feedback

# Initialize OAuth
oauth = OAuth(
    client_id=st.secrets["client_id"],
    client_secret=st.secrets["client_secret"],
    base_url="https://accounts.google.com/o/oauth2/auth",
    redirect_uri="http://localhost:8501",
    authorization_url="https://accounts.google.com/o/oauth2/auth",
    token_url="https://accounts.google.com/o/oauth2/token",
    scopes=["https://www.googleapis.com/auth/youtube.upload"]
)

def main():
    st.title("Audio to YouTube")
    auth_token = oauth.authorize()
    if auth_token:
        st.success("Authorization successful!")
        m4a_file = st.file_uploader("Upload your M4A file", type="m4a")
        if m4a_file:
            st.success("File upload successful!")
            spectrogram_image = spectrogram_generation.generate_spectrogram(m4a_file)
            if spectrogram_image:
                st.image(spectrogram_image, caption="Spectrogram", use_column_width=True)
                st.success("Spectrogram generation successful!")
                mp4_video = video_creation.create_video(spectrogram_image, m4a_file)
                if mp4_video:
                    st.video(mp4_video)
                    st.success("Video creation successful!")
                    youtube_video_id, playlist_id = youtube_upload.upload_youtube(mp4_video, auth_token)
                    if youtube_video_id and playlist_id:
                        st.success("YouTube upload successful!")
                    else:
                        st.error("YouTube upload failed.")
                else:
                    st.error("Video creation failed.")
            else:
                st.error("Spectrogram generation failed.")
        else:
            st.error("File upload failed.")
    else:
        st.error("Authorization failed.")

if __name__ == "__main__":
    main()
```