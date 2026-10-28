import os
import subprocess
import imageio_ffmpeg

output_file = "sample.wav"

# Find the WhatsApp AAC audio file automatically
input_file = None

for file in os.listdir("."):
    if file.lower().endswith(".aac"):
        input_file = file
        break

if input_file is None:
    print("ERROR: No .aac audio file found.")
    print("Please keep your WhatsApp dog audio in this folder.")
    exit()

print("Original audio found:")
print(input_file)

# Get FFmpeg executable
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

print("\nConverting original dog audio...")
print("Please wait...")

command = [
    ffmpeg,
    "-y",
    "-i", input_file,
    "-ac", "1",
    "-ar", "16000",
    "-sample_fmt", "s16",
    output_file
]

subprocess.run(command, check=True)

print("\nConversion completed successfully!")
print("Created:", output_file)
print("Format: WAV")
print("Channels: Mono")
print("Sample Width: 16-bit")
print("Sample Rate: 16000 Hz")