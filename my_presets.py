import json

presets = {
    'None':
        {'scale': 'Major', 'key': 'A', 'octave': 2, 'harmony': 'None',
         'randomize_octaves': True, 'resize_to_n_pixels': False,
         't_value': 0.2, 'n_pixels': 64,
         'gain_db': 0.0, 'drive_db': 0.0,
         'cutoff_hz': 0.0, 'resonance_lad': 0.0, 'drive_lad': 1.0, 'delay_seconds': 0.0,
         'room_size': 0.0, 'damping': 0.0, 'wet_level': 0.0, 'dry_level': 0.1, 'width': 0.0,
         'rate_hz_chorus': 0.0},
    'Bitcrusher': {'scale': 'Natural Minor', 'key': 'G', 'octave': 3, 'harmony': 'Perfect fifth',
                   'randomize_octaves': True, 'resize_to_n_pixels': False, 't_value': 0.1, 'n_pixels': 100,
                   'gain_db': 9.0, 'drive_db': 14.0, 'cutoff_hz': 81.0, 'resonance_lad': 0.4, 'drive_lad': 5.8,
                   'delay_seconds': 0.0, 'room_size': 0.1, 'damping': 0.0, 'wet_level': 0.0, 'dry_level': 0.3,
                   'width': 0.0, 'rate_hz_chorus': 0.0}

   }