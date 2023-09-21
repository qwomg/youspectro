```python
import asyncio
from spectrogram_generation import generate_spectrogram
from video_creation import create_video
from youtube_upload import upload_youtube
from error_handling_feedback import handle_error, show_feedback

async def process_audio_file(m4a_file):
    try:
        # Generate spectrogram
        spectrogram_image = await generate_spectrogram(m4a_file)
        show_feedback('spectrogram_success')

        # Create video
        mp4_video = await create_video(m4a_file, spectrogram_image)
        show_feedback('video_creation_success')

        # Upload to YouTube
        youtube_video_id, playlist_id = await upload_youtube(mp4_video)
        show_feedback('youtube_upload_success')

        return youtube_video_id, playlist_id

    except Exception as e:
        handle_error(e)

def run_async_tasks(m4a_file):
    loop = asyncio.get_event_loop()
    return loop.run_until_complete(process_audio_file(m4a_file))
```