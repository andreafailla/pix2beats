"""
Loosely based on
https://github.com/victormurcia/Making-Music-From-Images/blob/main/music_to_images.py
"""

import random
import time
import os
import glob

import numpy as np

# image
from PIL import Image

# audio
from pedalboard import Pedalboard, Chorus, Reverb, Gain, LadderFilter, Delay, Distortion
from pedalboard.io import AudioFile
from scipy.io import wavfile

from constants import *

# reproducibility
random.seed(42)


def clean():
    """ Removes resized images from previous runs """
    torem = ['*_resized.png','*.wav', '*.jpg', '*jpeg']
    for pattern in torem:
        for i in glob.glob(pattern):
            os.remove(i)

    for i in glob.glob('*.png'):
        if i not in SAMPLE_IMAGES:
            os.remove(i)


def rolling_title(placeholder, text, delay=0.05):
    """
    Displays title with rolling effect
    Placeholder is the container where the title will be displayed
    """
    while True:

        for i in range(len(text)):
            time.sleep(delay)
            placeholder.markdown(f'### {text[:i + 1]}')
        time.sleep(1)
        for i in range(len(text)):
            time.sleep(delay)
            placeholder.markdown(f'### {text[:len(text) - i]}')


def resize_and_convert(filename, tmpdir, n_pixels=None):
    """
    Resize the image, convert to hsv, and save as png

    :param filename:
    :param n_pixels:
    :return:
    """
    # Saves
    img = Image.open(filename).convert("RGB")
    if n_pixels is not None:
        # Calculate the aspect ratio
        aspect_ratio = img.width / img.height

        # Calculate the new width based on the desired number of pixels
        new_width = int((n_pixels * aspect_ratio) ** 0.5)

        # Resize the image while maintaining the aspect ratio
        img = img.resize((new_width, int(new_width / aspect_ratio)))
    if not filename.startswith(tmpdir):

        img.save(f"{tmpdir}/{filename.split('.')[0]}_resized.png", "PNG")

    return img


def get_scale(octave, key, scale_name):
    """
    returns the scale as a list of frequencies
    :param octave:
    :param key:
    :param scale_name:
    :return:
    """

    # Find index of desired key
    idx = OCTAVE.index(key)

    # Redefine scale interval so that scale intervals begin with whichKey
    new_scale = OCTAVE[idx:12] + OCTAVE[:idx]

    # Choose scale
    scale = SCALES.get(scale_name)
    if scale is None:
        print('Invalid scale name')
        return

    # Initialize arrays
    freqs = []
    for i in range(len(scale)):
        note = new_scale[scale[i]] + str(octave)
        freqs.append(PIANO_NOTES[note])
    return freqs


def hue2freq(h, scale_freqs):
    """
    convert hue to frequency
    :param h:
    :param scale_freqs:
    :return:
    """

    # hue to note
    for i in range(len(HSV_THRESHOLDS)):
        if i == len(HSV_THRESHOLDS) - 1 or (HSV_THRESHOLDS[i] <= h < HSV_THRESHOLDS[i + 1]):
            note = scale_freqs[i]
            break
    else:
        # Handle the case when hue is greater than the last threshold
        note = scale_freqs[0]

    return note


def get_track_layers(img, scale, t, n_pixels, randomize_octaves, harmonize):
    """
    Get the main track and the harmony layers as numpy arrays

    :param img: image
    :param scale: list of frequencies
    :param t: duration of each note in seconds
    :param n_pixels: number of pixels to sample and convert to notes
    :param randomize_octaves: whether to randomize the octaves of the notes
    :param harmonize:
    :return:
    """

    # Get shape of image
    width, height = img.size

    # Initialize array that will contain Hues for every pixel in image
    hues = []
    img = np.array(img)  # Convert image to numpy array
    for val in range(n_pixels):
        i = random.randint(0, height - 1)
        j = random.randint(0, width - 1)
        hue = abs(img[i][j][0])  # This is the hue value at pixel coordinate (i,j)
        hues.append(hue)

    # Make dataframe containing hues and frequencies
    frequencies = [hue2freq(hue, scale) for hue in hues]

    track_layer = np.array([])  # This array will contain the track signal
    harmony_layer = np.array([])  # This array will contain the track harmony
    harmony_val = HARMONIES.get(harmonize)  # This will select the ratio for the desired harmony
    octaves = np.array([0.5, 1, 2])  # Go an octave below, same note, or go an octave above
    t = np.linspace(0, t, int(t * SAMPLE_RATE), endpoint=False)

    print(t) # evenly spaced time vector

    # To avoid clicking sounds, apply fade in and fade out
    fade_samples = int(FADE_DURATION * SAMPLE_RATE)

    fade_in = np.linspace(0, 1, fade_samples, endpoint=False)
    fade_out = np.linspace(1, 0, fade_samples, endpoint=False)

    for k in range(n_pixels):
        if randomize_octaves:
            octave = random.choice(octaves)
        else:
            octave = 1

        val = octave * random.choice(frequencies)

        # Make note and harmony note
        note = 0.5 * np.sin(2 * np.pi * val * t)
        h_note = 0.5 * np.sin(2 * np.pi * val * t * harmony_val)

        note[:fade_samples] *= fade_in
        note[-fade_samples:] *= fade_out
        h_note[:fade_samples] *= fade_in
        h_note[-fade_samples:] *= fade_out

        # Place notes into corresponding arrays
        track_layer = np.concatenate([track_layer, note])
        harmony_layer = np.concatenate([harmony_layer, h_note])

    return track_layer, harmony_layer


def apply_pb_effects(
        gain_db, drive_db, cutoff_hz, resonance_lad,
        drive_lad, delay_seconds, damping, room_size, wet_level, dry_level, width, rate_hz_chorus,
        audio, sr
):
    board = Pedalboard([
        Gain(gain_db=gain_db),
        Distortion(drive_db=drive_db),
        LadderFilter(mode=LadderFilter.Mode.HPF12, cutoff_hz=cutoff_hz, resonance=resonance_lad, drive=drive_lad),
        Delay(delay_seconds=delay_seconds),
        Reverb(damping=damping,
               room_size=room_size, wet_level=wet_level, dry_level=dry_level, width=width),
        Chorus(rate_hz=rate_hz_chorus)
    ])

    return board(audio, sr)


def trackmaker(
        img, scale, key, octave, harmony, randomize_octaves, t_value, n_pixels, gain_db, drive_db, cutoff_hz,
        resonance_lad, drive_lad, delay_seconds, room_size, damping, wet_level, dry_level, width, rate_hz_chorus
):
    # Make the scale from parameters above
    scale_to_use = get_scale(octave, key, scale)
    # Make the track!
    track, harmony = get_track_layers(img, scale=scale_to_use, t=t_value, n_pixels=n_pixels,
                                      randomize_octaves=randomize_octaves, harmonize=harmony)

    # Write the track into a file
    track_combined = np.vstack((track, harmony))
    wavfile.write('track.wav', rate=SAMPLE_RATE,
                  data=track_combined.T.astype(np.float32))

    # Read the track
    try:
        with AudioFile('track.wav', 'r') as f:
            audio = f.read(f.frames)

        # Apply the pedalboard effects
        effected = apply_pb_effects(
            gain_db, drive_db, cutoff_hz, resonance_lad,
            drive_lad, delay_seconds, damping, room_size,
            wet_level, dry_level, width, rate_hz_chorus,
            audio, SAMPLE_RATE
        )

        # Write the audio back as a wav file:
        with AudioFile('track.wav', 'w', SAMPLE_RATE, effected.shape[0]) as f:
            f.write(effected)

        # Read the processed track
        with open('track.wav', 'rb') as f:
            audio_bytes = f.read()


        return audio_bytes
    except ValueError:
        return None
