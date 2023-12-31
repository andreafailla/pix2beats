SAMPLE_IMAGES = ["mona_lisa.png", "pixel_art_landscape.png", "sunflower.png"]

SAMPLE_RATE = 22050  # standard audio sample rate

FADE_DURATION = 0.015  # duration of fade in and fade out

NOTES = ["A", "A#", "B", "C", "C#", "D", "D#", "E", "F", "F#", "G", "G#"]

PIANO_NOTES = {
    "A0": 27.5,
    "A#0": 29.13523509488062,
    "B0": 30.86770632850775,
    "C0": 32.70319566257483,
    "C#0": 34.64782887210901,
    "D0": 36.70809598967594,
    "D#0": 38.890872965260115,
    "E0": 41.20344461410875,
    "F0": 43.653528929125486,
    "F#0": 46.2493028389543,
    "G0": 48.999429497718666,
    "G#0": 51.91308719749314,
    "A1": 55.0,
    "A#1": 58.27047018976124,
    "B1": 61.7354126570155,
    "C1": 65.40639132514966,
    "C#1": 69.29565774421802,
    "D1": 73.41619197935188,
    "D#1": 77.78174593052023,
    "E1": 82.4068892282175,
    "F1": 87.30705785825097,
    "F#1": 92.4986056779086,
    "G1": 97.99885899543733,
    "G#1": 103.82617439498628,
    "A2": 110.0,
    "A#2": 116.54094037952248,
    "B2": 123.47082531403103,
    "C2": 130.8127826502993,
    "C#2": 138.59131548843604,
    "D2": 146.8323839587038,
    "D#2": 155.56349186104046,
    "E2": 164.81377845643496,
    "F2": 174.61411571650194,
    "F#2": 184.9972113558172,
    "G2": 195.99771799087463,
    "G#2": 207.65234878997256,
    "A3": 220.0,
    "A#3": 233.08188075904496,
    "B3": 246.94165062806206,
    "C3": 261.6255653005986,
    "C#3": 277.1826309768721,
    "D3": 293.6647679174076,
    "D#3": 311.1269837220809,
    "E3": 329.6275569128699,
    "F3": 349.2282314330039,
    "F#3": 369.9944227116344,
    "G3": 391.99543598174927,
    "G#3": 415.3046975799451,
    "A4": 440.0,
    "A#4": 466.1637615180899,
    "B4": 493.8833012561241,
    "C4": 523.2511306011972,
    "C#4": 554.3652619537442,
    "D4": 587.3295358348151,
    "D#4": 622.2539674441618,
    "E4": 659.2551138257398,
    "F4": 698.4564628660078,
    "F#4": 739.9888454232688,
    "G4": 783.9908719634985,
    "G#4": 830.6093951598903,
    "A5": 880.0,
    "A#5": 932.3275230361799,
    "B5": 987.7666025122483,
    "C5": 1046.5022612023945,
    "C#5": 1108.7305239074883,
    "D5": 1174.6590716696303,
    "D#5": 1244.5079348883237,
    "E5": 1318.5102276514797,
    "F5": 1396.9129257320155,
    "F#5": 1479.9776908465376,
    "G5": 1567.981743926997,
    "G#5": 1661.2187903197805,
    "A6": 1760.0,
    "A#6": 1864.6550460723597,
    "B6": 1975.533205024496,
    "C6": 2093.004522404789,
    "C#6": 2217.4610478149766,
    "D6": 2349.31814333926,
    "D#6": 2489.0158697766474,
    "E6": 2637.02045530296,
    "F6": 2793.825851464031,
    "F#6": 2959.955381693075,
    "G6": 3135.9634878539946,
    "G#6": 3322.437580639561,
    "A7": 3520.0,
    "A#7": 3729.3100921447194,
    "B7": 3951.066410048992,
    "C7": 4186.009044809578,
    "C#7": 4434.922095629953,
    "D7": 4698.63628667852,
    "D#7": 4978.031739553295,
    "E7": 5274.04091060592,
    "F7": 5587.651702928062,
    "F#7": 5919.91076338615,
    "G7": 6271.926975707989,
    "G#7": 6644.875161279122,
    "A8": 7040.0,
    "A#8": 7458.620184289437,
    "B8": 7902.132820097988,
    "C8": 8372.018089619156,
    "": 0.0,
}

SCALES = {
    "Major": [0, 2, 4, 5, 7, 9, 11],
    "Natural Minor": [0, 2, 3, 5, 7, 8, 10],
    "Dorian": [0, 2, 3, 5, 7, 9, 10],
    "Mixolydian": [0, 2, 4, 5, 7, 9, 10],
    "Aeolian": [0, 2, 3, 5, 7, 8, 10],
    "Phrygian": [0, 1, 3, 5, 7, 8, 10],
    "Lydian": [0, 2, 4, 6, 7, 9, 11],
    "Harmonic Minor": [0, 2, 3, 5, 7, 8, 11],
    "Melodic Minor": [0, 2, 3, 5, 7, 8, 9, 10, 11],
    "Locrian": [0, 1, 3, 5, 6, 8, 10],
    "Blues": [0, 2, 3, 4, 5, 7, 9, 10, 11],
    "Chromatic": [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
}

HARMONIES = {
    "None": 1,
    "Major second": 9 / 8,
    "Minor third": 6 / 5,
    "Major third": 5 / 4,
    "Perfect fourth": 4 / 3,
    "Diatonic tritone": 45 / 32,
    "Perfect fifth": 3 / 2,
    "Minor sixth": 8 / 5,
    "Major sixth": 5 / 3,
    "Minor seventh": 9 / 5,
    "Major seventh": 15 / 8,
}

HSV_THRESHOLDS = [26, 52, 78, 104, 128, 154, 180]
