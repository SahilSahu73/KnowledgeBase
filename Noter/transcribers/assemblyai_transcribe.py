import requests
import time
import os
from dotenv import load_dotenv

# ========Config========
BASE_URL = "https://api.assemblyai.com"

load_dotenv()
HEADERS = {
    "authorization": os.getenv("ASSEMBLYAI_API_KEY")
}
# folder containing audio files
AUDIO_FOLDER = "../audio_knowledge"
TRANSCRIPTS_FOLDER = "../transcripts"
os.makedirs(TRANSCRIPTS_FOLDER, exist_ok=True)
# ========================


def upload_audio_file(file_path):
    """
    Uploads a local file to AssemblyAI and returns the upload_url.
    """
    with open(file_path, "rb") as f:
        response = requests.post(
            BASE_URL + "/v2/upload",
            headers=HEADERS,
            data=f
        )
    return response.json()["upload_url"]


def transcribe(audio_url):
    """
    Send audio url to AssemblyAI for transcription and return transcript text.
    """
    data = {
        "audio_url": audio_url,
        "speech_model": "universal",
        "auto_chapters": True,
        "punctuate": True,
        "format_text": True,
        "speaker_labels": True,  # uncomment if want to do diarization
    }
    url = BASE_URL + "/v2/transcript"
    response = requests.post(url, json=data, headers=HEADERS)
    transcript_id = response.json()['id']

    polling_endpoint = BASE_URL + "/v2/transcript/" + transcript_id

    while True:
        transcription_result = requests.get(polling_endpoint, headers=HEADERS).json()

        if transcription_result["status"] == "completed":
            return transcription_result["text"]

        elif transcription_result["status"] == "error":
            raise RuntimeError(f"Transcription failed: {transcription_result["error"]}")

        else:
            time.sleep(3)


def save_transcripts(text, audio_filename):
    """
    save transcript text into a .txt file in TRANSCRIPTS_FOLDER
    """
    base_name, _ = os.path.splitext(audio_filename)
    transcript_file = os.path.join(TRANSCRIPTS_FOLDER, base_name + ".txt")
    with open(transcript_file, "w", encoding="utf-8") as f:
        f.write(text)
    print(f"Transcript saved at: {transcript_file}")


def main():
    # List all audio files in folder
    audio_files = [f for f in os.listdir(AUDIO_FOLDER)
                   if f.lower().endswith((".mp3", ".wav"))]

    if not audio_files:
        print("No audio files found in the folder.")
        return

    print("Available audio files:")
    for idx, file in enumerate(audio_files, start=1):
        print(f"{idx}. {file}")

    choice = int(input("Enter the number of the file you want to transcribe: ")) - 1

    if 0 <= choice < len(audio_files):
        file_path = os.path.join(AUDIO_FOLDER, audio_files[choice])
        print(f"Selected file: {file_path}")

        try:
            audio_url = upload_audio_file(file_path)
            print(f"Uploaded to AssemblyAI: {audio_url}")
            transcript_text = transcribe(audio_url)
            save_transcripts(transcript_text, audio_files[choice])

        except Exception as e:
            print(f"Error processing {file_path}: {e}")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()
