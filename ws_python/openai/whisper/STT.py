import os

from openai import OpenAI
with open("./GPT_Key.txt", "r") as f:
  api_key = f.read().strip()
client = OpenAI(
  api_key=api_key
)

# MP3
# -----------------------------------------------------------------------------
# 한국어
# audio_file= open("./숲.mp3", "rb") 
# transcript = client.audio.transcriptions.create(model='whisper-1', 
#                                      language='ko',
#                                      file=audio_file)

# 영어
# audio_file= open("./somewhere.mp3", "rb")
# transcript = client.audio.transcriptions.create(model='whisper-1', 
#                                      language='en',
#                                      file=audio_file)

# MP4
# -----------------------------------------------------------------------------
# 한국어 크기가 너무 큼
# audio_file= open("kimchi.mp4", "rb")
# transcript = client.audio.transcriptions.create(model='whisper-1', 
#                                      language='ko',
#                                      file=audio_file)

# 영어
audio_file= open("Mind-blowing.mp4", "rb")
transcript = client.audio.transcriptions.create(model='whisper-1', 
                                     language='en',
                                     file=audio_file)

print(type(transcript)) # <class 'openai.types.audio.transcription.Transcription'>
print(transcript.text)

'''
activate ai
cd whisper
python whisper1.py
'''
 
 