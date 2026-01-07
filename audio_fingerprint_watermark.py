# =====================================================
# Secure Audio Fingerprinting & Tamper Detection
# Mini Project - Full Working Code (Single File)
# =====================================================

import librosa
import numpy as np
import soundfile as sf
import hashlib
import matplotlib.pyplot as plt

# -----------------------------------------------------
# STEP 1: Load Input Audio
# -----------------------------------------------------
audio, sr = librosa.load("input.wav", sr=None)

print("Audio loaded successfully")
print("Sampling Rate:", sr)
print("Number of Samples:", len(audio))

# -----------------------------------------------------
# STEP 2: Extract MFCC Features
# -----------------------------------------------------
mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=20)
print("MFCC features extracted")

# -----------------------------------------------------
# STEP 3: Generate Audio Fingerprint (Hash)
# -----------------------------------------------------
mfcc_mean = np.mean(mfcc, axis=1)
fingerprint = hashlib.sha256(mfcc_mean.tobytes()).hexdigest()

print("Audio Fingerprint:")
print(fingerprint)

# -----------------------------------------------------
# STEP 4: Convert Fingerprint to Binary
# -----------------------------------------------------
binary_fp = ''.join(format(ord(c), '08b') for c in fingerprint[:16])
print("Binary Fingerprint Length:", len(binary_fp))

# -----------------------------------------------------
# STEP 5: Embed Watermark into Audio
# -----------------------------------------------------
watermarked_audio = audio.copy()

for i, bit in enumerate(binary_fp):
    if bit == '1':
        watermarked_audio[i] += 0.0001
    else:
        watermarked_audio[i] -= 0.0001

print("Watermark embedded into audio")

# -----------------------------------------------------
# STEP 6: Save Watermarked Audio
# -----------------------------------------------------
sf.write("watermarked.wav", watermarked_audio, sr)
print("Watermarked audio saved as watermarked.wav")

# -----------------------------------------------------
# STEP 7: Tampering Simulation (Noise Addition)
# -----------------------------------------------------
noise = np.random.normal(0, 0.0002, len(watermarked_audio))
tampered_audio = watermarked_audio + noise

sf.write("tampered.wav", tampered_audio, sr)
print("Tampered audio saved as tampered.wav")

# -----------------------------------------------------
# STEP 8: Watermark Extraction
# -----------------------------------------------------
extracted_bits = ""

for i in range(len(binary_fp)):
    if tampered_audio[i] > audio[i]:
        extracted_bits += '1'
    else:
        extracted_bits += '0'

print("Watermark extracted")

# -----------------------------------------------------
# STEP 9: Compare Fingerprints
# -----------------------------------------------------
match_count = 0

for b1, b2 in zip(binary_fp, extracted_bits):
    if b1 == b2:
        match_count += 1

accuracy = (match_count / len(binary_fp)) * 100
print("Fingerprint Matching Accuracy:", accuracy, "%")

# -----------------------------------------------------
# STEP 10: Final Decision
# -----------------------------------------------------
if accuracy > 80:
    print("✅ RESULT: Audio is AUTHENTIC")
else:
    print("❌ RESULT: Audio is TAMPERED")

# -----------------------------------------------------
# STEP 11: Plot Audio Waveforms
# -----------------------------------------------------
plt.figure(figsize=(10, 7))

plt.subplot(3, 1, 1)
plt.title("Original Audio")
plt.plot(audio)
plt.ylabel("Amplitude")

plt.subplot(3, 1, 2)
plt.title("Watermarked Audio")
plt.plot(watermarked_audio)
plt.ylabel("Amplitude")

plt.subplot(3, 1, 3)
plt.title("Tampered Audio")
plt.plot(tampered_audio)
plt.ylabel("Amplitude")

plt.xlabel("Samples")
plt.tight_layout()
plt.show()
