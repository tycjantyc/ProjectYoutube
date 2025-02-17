import ffmpeg
import whisper
import os

def make_transcript(mp4_file, audio_file, sub_title, word_timestamps = True):

    ffmpeg.input(mp4_file).output(audio_file).run()

    model = whisper.load_model("base")  #optional 'tiny'
    try:
        result = model.transcribe(audio_file, language="english", word_timestamps=word_timestamps, verbose = True)
        f = open(f"transcripts_bad/transcript_{sub_title}.txt", "w")
        f.write(result['text'])
        f.close()

    except Exception:
        pass
        
    os.remove(mp4_file)
    os.remove(audio_file)