# Installing required libraries
!pip install yt-dlp
!pip install faster-whisper
!pip install transformers torch gradio
!pip install pytube
!pip install pydub

# Loading libraries
from transformers import pipeline
import gradio as gr
import os
from faster_whisper import WhisperModel
import yt_dlp
import torch
import gc
from pytube import YouTube
from IPython.display import display, HTML

# Function to clear GPU memory (if using CUDA)
def clear_gpu_memory():
    if torch.cuda.is_available():
        torch.cuda.empty_cache()
    gc.collect()

# Function to download audio
def download_audio(url):
    try:
         # Cleaning up old files
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': 'temp_audio',  
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
            }],
            'quiet': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # yt-dlp creates the file with .mp3 extension
        if not os.path.exists("temp_audio.mp3"):
            raise Exception("Failed to create audio file")

        return "temp_audio.mp3"
    except Exception as e:
        if os.path.exists("temp_audio.mp3"):
            os.remove("temp_audio.mp3")
        raise Exception(f"Download error: {str(e)}")

# Transcription with Whisper refreshed each time
def transcribe_audio(audio_path):
    try:
        clear_gpu_memory()
        model = WhisperModel("medium", device="cuda")  
        segments, _ = model.transcribe(audio_path)
        lyrics = " ".join([s.text for s in segments])

        # Cleaning
        del model
        clear_gpu_memory()
        return lyrics
    except Exception as e:
        raise Exception(f"Transcription error: {str(e)}")
    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)

 # Emotion analysis with classifier refreshed each time
def analyze_emotion(text):
    try:
        clear_gpu_memory()
        classifier = pipeline("text-classification", model="bhadresh-savani/distilbert-base-uncased-emotion")

        result = classifier(text[:512])[0]
        emotion = result['label']
        confidence = round(result['score'] * 100)
        del classifier
        clear_gpu_memory()
        return f"{emotion} (confidence: {confidence}%)"
    except Exception as e:
        raise Exception(f"Emotion analysis error: {str(e)}")

def get_video_title(url):
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            return info.get('title', 'Uknown title')
    except Exception as e:
        return f"Erros in the title: {str(e)}"


# Dictionary with suggested songs
emotion_songs = {
    "anger": [
        {"title": "Three Days Grace - I Hate Everything About You", "url": "https://www.youtube.com/watch?v=d8ekz_CSBVg"},
        {"title": "Eminem - The Way I Am", "url": "https://www.youtube.com/watch?v=YVkUvmDQ3HY"},
        {"title": "Linkin Park - Given Up", "url": "https://www.youtube.com/watch?v=0xyxtzD54rM"},
        {"title": "Rage Against The Machine - Killing In The Name", "url": "https://www.youtube.com/watch?v=bWXazVhlyxQ"},
        {"title": "System Of A Down - Toxicity", "url": "https://www.youtube.com/watch?v=iywaBOMvYLI"}
    ],
    "fear": [
        {"title": "Radiohead - Climbing Up The Walls", "url": "https://www.youtube.com/watch?v=R5X7HKxpiQA"},
        {"title": "Björk - All Is Full of Love", "url": "https://www.youtube.com/watch?v=AjI2J2SQ528"},
        {"title": "Johnny Cash - Hurt", "url": "https://www.youtube.com/watch?v=vt1Pwfnh5pc"},
        {"title": "Portishead - Roads", "url": "https://www.youtube.com/watch?v=Vg1jyL3cr60"},
        {"title": "Pink Floyd - Welcome to the Machine", "url": "https://www.youtube.com/watch?v=lt-udg9zQSE"}
    ],
    "joy": [
        {"title": "Pharrell Williams - Happy", "url": "https://www.youtube.com/watch?v=ZbZSe6N_BXs"},
        {"title": "Justin Timberlake - Can't Stop The Feeling", "url": "https://www.youtube.com/watch?v=ru0K8uYEZWw"},
        {"title": "Katrina and the Waves - Walking on Sunshine", "url": "https://www.youtube.com/watch?v=iPUmE-tne5U"},
        {"title": "Shakira - Waka Waka", "url": "https://www.youtube.com/watch?v=pRpeEdMmmQ0"},
        {"title": "Bobby McFerrin - Don't Worry Be Happy", "url": "https://www.youtube.com/watch?v=d-diB65scQU"}
    ],
    "love": [
        {"title": "Ed Sheeran - Perfect", "url": "https://www.youtube.com/watch?v=2Vv-BfVoq4g"},
        {"title": "John Legend - All of Me", "url": "https://www.youtube.com/watch?v=450p7goxZqg"},
        {"title": "Elvis Presley - Can't Help Falling in Love", "url": "https://www.youtube.com/watch?v=vGJTaP6anOU"},
        {"title": "Alicia Keys - If I Ain't Got You", "url": "https://www.youtube.com/watch?v=Ju8Hr50Ckwk"},
        {"title": "Christina Perri - A Thousand Years", "url": "https://www.youtube.com/watch?v=rtOvBOTyX00"}
    ],
    "sadness": [
        {"title": "Adele - Someone Like You", "url": "https://www.youtube.com/watch?v=hLQl3WQQoQ0"},
        {"title": "Sam Smith - Too Good at Goodbyes", "url": "https://www.youtube.com/watch?v=J_ub7Etch2U"},
        {"title": "James Blunt - Goodbye My Lover", "url": "https://www.youtube.com/watch?v=wVyggTKDcOE"},
        {"title": "Coldplay - Fix You", "url": "https://www.youtube.com/watch?v=k4V3Mo61fJM"},
        {"title": "Lewis Capaldi - Someone You Loved", "url": "https://www.youtube.com/watch?v=bCuhuePlP8o"}
    ],
    "surprise": [
        {"title": "Imogen Heap - Hide and Seek", "url": "https://www.youtube.com/watch?v=UYIAfiVGluk"},
        {"title": "Gotye - Somebody That I Used To Know", "url": "https://www.youtube.com/watch?v=8UVNT4wvIGY"},
        {"title": "Sia - Chandelier", "url": "https://www.youtube.com/watch?v=2vjPBrBU-TM"},
        {"title": "MGMT - Time to Pretend", "url": "https://www.youtube.com/watch?v=B9dSYgd5Elk"},
        {"title": "David Bowie - Life on Mars?", "url": "https://www.youtube.com/watch?v=v--IqqusnNQ"}
    ]
}


import json

with open("emotion_songs.json", "w", encoding="utf-8") as f:
    json.dump(emotion_songs, f, ensure_ascii=False, indent=4)

print("✅ The file emotion_songs.json has been created.")

def suggest_songs(emotion_label):
    print(f"Suggest songs for emotion: '{emotion_label}'")  # Debug print
    songs = emotion_songs.get(emotion_label.lower(), [])
    print(f"Found {len(songs)} songs")  # Debug print
    if not songs:
        return "<div style='border:1px solid #ddd; padding:10px;'>No suggestions found for this emotion.</div>"

    # Adding a heading above the links
    links_html = """
    <div style='border:1px solid #ddd; padding:10px;'>
        <h4>🎵 Suggested Songs based on the Emotion of the song</h4>
        <ul style='list-style-type:none; padding-left:0;'>
    """
    for song in songs:
        title = song.get("title", "Uknown Song")
        url = song.get("url", "#")
        links_html += f'<li><a href="{url}" target="_blank" rel="noopener noreferrer">{title}</a></li>'
    links_html += "</ul></div>"
    return links_html

# Main workflow
def process_url(url):
    try:
        title = get_video_title(url)
        audio_path = download_audio(url)
        lyrics = transcribe_audio(audio_path)
        emotion = analyze_emotion(lyrics)

        # Clean and extract the first word of the emotion
        emotion_label = emotion.lower().strip().split()[0]
        print(f"Emotion detected: '{emotion_label}'")  # Debug print

        suggestions_html = suggest_songs(emotion_label)
        return title, lyrics, emotion, suggestions_html
    except Exception as e:
        return f"Σφάλμα: {str(e)}", "", "", ""



interface = gr.Interface(
    fn=process_url,
    inputs=gr.Textbox(label="YouTube URL (English Songs)"),
    outputs=[
        gr.Textbox(label="Title"),
        gr.Textbox(label="Lyrics"),
        gr.Textbox(label="Emotions"),
        gr.HTML(label="Suggested Songs")
    ],
    title="🎶 Music Emotion Analyzer",
    theme="soft"
)

# Launch
interface.launch(share=True)