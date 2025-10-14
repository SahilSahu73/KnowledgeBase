import os
from pydub import AudioSegment


# Folder containing your audio files
AUDIO_FOLDER = "../audio_knowledge"


def convert_ogg_to_wav(file_path):
    """Convert a single .ogg file to .wav format and remove the .ogg"""
    base_name, _ = os.path.splitext(file_path)
    wav_path = base_name + ".wav"

    # Load .ogg and export as .wav
    audio = AudioSegment.from_ogg(file_path)
    audio.export(wav_path, format="wav")

    # Delete the original .ogg file
    os.remove(file_path)

    print(f"Converted {os.path.basename(file_path)} -> {os.path.basename(wav_path)}")


def main():
    for filename in os.listdir(AUDIO_FOLDER):
        if filename.lower().endswith(".ogg"):
            file_path = os.path.join(AUDIO_FOLDER, filename)
            convert_ogg_to_wav(file_path)

    print("All .ogg files converted and originals deleted!")


if __name__ == "__main__":
    main()
