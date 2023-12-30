# pix2beats
[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://pix2beats.streamlit.app/)
[![Python 3.9](https://img.shields.io/badge/python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![License GNU](https://img.shields.io/badge/License-GNU%203--Clause-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)


 A web app to create music from images.

# What is this?
Pix2Beats is a [Streamlit](https://streamlit.io/) web app that allows you to create music from images.

# How does it work?
The idea is that <b>images are made of pixels</b>, and <b>pixels can be represented as numbers</b>.
Therefore, we can use these numeric values to obtain waveforms and, consequently, music.

Then, Pix2Beats applies a series of transformations to this signal (eg, apply effects, add harmonues, etc.) 
to obtain a more pleasant sound. 
This latter step, which is much common in music production, is carried out by
leveraging Spotify's [pedalboard API](https://spotify.github.io/pedalboard/reference/pedalboard.html)

# How do I use it?
You can use the app by <b>clicking on the Streamlit badge above</b>. 
Alternatively, you can run the app locally by cloning this repository and running the following commands:
```bash
pip install -r requirements.txt
streamlit run ui.py
```

