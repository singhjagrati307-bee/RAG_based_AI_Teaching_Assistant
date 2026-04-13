#1)
## chunking all video files with metadata (it take at least 8 hrs )
import whisper
import json
import os

# Load model
model = whisper.load_model("large-v2")

# Path to audio folder
audio_folder = r"C:\Users\BIT\Desktop\Project 2\rag based ai\audios"
# Create output folder if it doesn't exist
json_folder = r"C:\Users\BIT\Desktop\Project 2\rag based ai\jsons"
os.makedirs(json_folder, exist_ok=True)

# List audio files
audios = os.listdir(audio_folder)

for audio in audios:
    if "_" in audio and audio.lower().endswith(".mp3"):
        number = audio.split("_")[0]
        title = audio.split("_")[1][:-4]

        print(number, title)

        audio_path = os.path.join(audio_folder, audio)

        # Transcribe and translate
        result = model.transcribe(
            audio=audio_path,
            language="hi",
            task="translate",
            word_timestamps=False
        )

        # Extract chunks safely
        segments = result.get("segments", [])
        chunks = []
        for segment in segments:
            chunks.append({
                "number": number,
                "title": title,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })

        # Combine chunks with full text
        chunks_with_metadata = {"chunks": chunks, "text": result["text"]}

        # Safe JSON filename
        filename = os.path.splitext(audio)[0] + ".json"
        output_path = os.path.join(json_folder, filename)

        # Save JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks_with_metadata, f, ensure_ascii=False, indent=4)
            
            

# 2)

## limit the batch script to only 2 audio files (chunking two video files)
import whisper
import json
import os

# Load Whisper model
model = whisper.load_model("large-v2")

# Path to audio folder
audio_folder = r"C:\Users\BIT\Desktop\Project 2\rag based ai\audios"
# Create output folder if it doesn't exist
json_folder = r"C:\Users\BIT\Desktop\Project 2\rag based ai\jsons"
os.makedirs(json_folder, exist_ok=True)

# List audio files
audios = os.listdir(audio_folder)

# Limit to only 2 files
audios = audios[:2]

for audio in audios:
    if "_" in audio and audio.lower().endswith(".mp3"):
        number = audio.split("_")[0]
        title = audio.split("_")[1][:-4]

        print(f"Processing: {number} - {title}")

        audio_path = os.path.join(audio_folder, audio)

        # Transcribe and translate
        result = model.transcribe(
            audio=audio_path,
            language="hi",
            task="translate",
            word_timestamps=False
        )

        # Extract chunks safely
        segments = result.get("segments", [])
        chunks = []
        for segment in segments:
            chunks.append({
                "number": number,
                "title": title,
                "start": segment["start"],
                "end": segment["end"],
                "text": segment["text"]
            })

        # Combine chunks with full text
        chunks_with_metadata = {"chunks": chunks, "text": result["text"]}

        # Safe JSON filename
        filename = os.path.splitext(audio)[0] + ".json"
        output_path = os.path.join(json_folder, filename)

        # Save JSON
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(chunks_with_metadata, f, ensure_ascii=False, indent=4)

        print(f"Finished: {title}")

            
            
            
            
            