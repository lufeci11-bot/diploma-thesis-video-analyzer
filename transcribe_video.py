import assemblyai as aai

aai.settings.api_key = ""

# For larger segments, use paragraphs instead
def get_paragraph_segments(transcript):
   """
   Get paragraph-level segments for longer captions
   """
   paragraphs = transcript.get_paragraphs()
   
   segments = []
   for paragraph in paragraphs:
       segment = {
           "start": paragraph.start,
           "end": paragraph.end,
           "text": paragraph.text,
           "confidence": paragraph.confidence
       }
       segments.append(segment)
   
   return segments

def export_txt_with_speakers(segments, output_file="output_speakers.txt"):
   def format_srt_time(milliseconds):
       seconds = milliseconds / 1000
       hours = int(seconds // 3600)
       minutes = int((seconds % 3600) // 60)
       secs = int(seconds % 60)
       millis = int((milliseconds % 1000))
       return f"{hours:02d}:{minutes:02d}:{secs:02d},{millis:03d}"
   
   with open(output_file, "w", encoding="utf-8") as f:
       for i, segment in enumerate(segments, 1):
           f.write(f"{i}\n")
           start = format_srt_time(segment["start"])
           end = format_srt_time(segment["end"])
           f.write(f"{start} --> {end}\n")
           f.write(f"[Speaker {segment['speaker']}]: {segment['text'].strip()}\n\n")

audio_file = "./The Four Horsemen HD_ Hour 1 of 2 - Discussions with Richard Dawkins, Ep 1.mp3"
config = aai.TranscriptionConfig(speech_models=["universal-3-pro", "universal-2"], language_detection=True, speaker_labels=True)

transcript = aai.Transcriber(config=config).transcribe(audio_file)

segments_with_speakers = []

for utterance in transcript.utterances:
    segment = {
        "speaker": utterance.speaker,
        "start": utterance.start,
        "end": utterance.end,
        "text": utterance.text,
        "confidence": utterance.confidence
    }
    segments_with_speakers.append(segment)


export_txt_with_speakers(segments_with_speakers)
