import wave


def inspect_wav_audio_file(file_path):

    with wave.open(file_path, 'rb') as wav_file:

        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        framerate = wav_file.getframerate()
        n_frames = wav_file.getnframes()

        duration = n_frames / float(framerate)

        print("--- Audio File Properties ---")
        print(f"Channels: {channels} ({'Mono' if channels == 1 else 'Stereo'})")
        print(f"Sample Width: {sample_width * 8}-bit")
        print(f"Sample Rate: {framerate} Hz")
        print(f"Duration: {duration:.2f} seconds")

        if framerate != 16000:
            print("[WARN] Sample rate is not 16000Hz! Resampling recommended.")
        else:
            print("[OK] Sample rate meets 16kHz standard.")


if __name__ == "__main__":
    print("Audio Preprocessing Module Ready.")
    inspect_wav_audio_file("sample.wav")
      