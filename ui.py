import streamlit as st  # UI
from constants import SCALES, OCTAVE, HARMONIES  # constants
from backend import resize_and_convert, trackmaker  # processing
from backend import rolling_title  # animation
from my_presets import presets as PRESETS
import glob  # find sample images
import json  # export presets
from PIL import Image  # image processing
import tempfile


def init_session_state():
    for k, v in PRESETS['None'].items():
        if k not in st.session_state:
            if k != 'octave':
                st.session_state[k] = v
            else:
                octave_options = ['Low', 'Mid', 'High']
                st.session_state[k] = octave_options[v - 1]


def update_session_state(preset):
    for k, v in preset.items():
        if k != 'octave':
            st.session_state[k] = v
        else:
            octave_options = ['Low', 'Mid', 'High']
            st.session_state[k] = octave_options[v - 1]


def write_intro():
    """ Defines general settings and introduces the app.
    :return: placeholder for the rolling title
    """
    st.set_page_config(
        page_title="Pix2Beats",
        page_icon=":musical_note:",
        layout="centered",
        initial_sidebar_state="expanded",

    )
    st.markdown("""
    <style>
        .stApp {
        background: url("https://images.unsplash.com/photo-1557695126-fa2ce36f6828?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: cover;
        background-opacity: 0;
        }
    </style>""", unsafe_allow_html=True)

    st.title(":blue[Pix]2:red[Beats]")

    plh = st.empty()

    # Display the description
    st.markdown(
        """
        Welcome to :blue[Pix]2:red[Beats]—a  web application at the intersection of visual art and musical expression. 
        Harnessing the power of Artificial Intelligence, :blue[Pix]2:red[Beats] transforms your images into sounds, 
        unlocking a fascinating synergy between the realms of visual and auditory creativity.

        At the heart of :blue[Pix]2:red[Beats] lies the intuition that both images and sound can be effortlessly 
        represented as matrices of numbers. 
        This unique foundation allows us to create a one-of-a-kind mapping between color spaces and musical scales.

        Choose an image, tinker with the parameters, and let :blue[Pix]2:red[Beats] do the rest :musical_note:

        """
    )
    return plh


def handle_presets():
    presetsel, presetupl, _ = st.columns([1, 1, 2])
    with presetsel:
        preset_name = st.selectbox('***Choose a preset***', PRESETS.keys(), key='preset_select',
                                   help='Tip: you can modify an existing preset by selecting it and then selecting '
                                        '*None* from this list.')
        if preset_name is not None:
            if preset_name != 'None':
                update_session_state(PRESETS[preset_name])
            else:
                pass

    with presetupl:
        uploaded_preset = st.file_uploader('***...or upload your own!***', type=["json"])

        css = '''
        <style>
            [data-testid='stFileUploader'] {
                width: max-content;
            }

            [data-testid='stFileUploader'] section {
                padding: 0;
                float: left;
            }
            [data-testid='stFileUploader'] section > input + div {
                display: none;
            }

            [data-testid='stFileUploader'] section + div {
                float: right;
                padding-top: 0;
            }

        </style>
        '''
        st.markdown(css, unsafe_allow_html=True)

        if uploaded_preset is not None:
            preset_name = uploaded_preset.name.split('.')[0]
            preset = json.load(uploaded_preset)
            PRESETS[preset_name] = preset
            uploaded_preset = None
            update_session_state(preset)


def make_sidebar_and_select_file():
    """
    Create the sidebar for the app
    The sidebar lets the user select an image to use
    :return: the image filename
    """
    if st.sidebar.radio("Image to use",
                        ("Use Example Image", "Upload Image"),
                        label_visibility='hidden') == "Use Example Image":
        sample_images = [i for i in glob.glob('*.png') if not i.endswith('_resized.png')]
        filename = st.sidebar.selectbox('Choose a sample image', sample_images)
        img = Image.open(filename)

    else:
        img = st.sidebar.file_uploader("Upload an image", type=["jpg", "png", "jpeg"])
        if img is not None:
            filename = img.name
            img = Image.open(img)
            filename = tmpdir + '/' + filename
            img.save(filename)

    # Display the image
    if img is not None:
        st.sidebar.image(img)

        return img, filename
    else:
        return None, None


def make_widgets_and_get_parameters():
    """
    UI to get the parameters required to generate the track
    :return: list of parameters
    """
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        scale_options = list(SCALES.keys())

        scale = st.selectbox('***Choose the scale***', scale_options, key='scale')
        key = st.selectbox('***Choose the key***', OCTAVE, key='key')

    with col2:
        octave_options = ['Low', 'Mid', 'High']
        octave = st.selectbox('***Choose the octave***', octave_options, key='octave')
        octave = octave_options.index(octave)

        harmony_options = list(HARMONIES.keys())
        harmony = st.selectbox('*Choose how to harmonize*', harmony_options, key='harmony')

    with col3:
        t_value = st.slider('***Note duration (seconds)***',
                            min_value=0.10, max_value=1.0, step=0.01, key='t_value')
        n_pixels = st.slider('***Pixels to sample***', min_value=64, max_value=320, step=1, key='n_pixels')

    randomize_octaves = st.checkbox('***Randomize octaves***', key='randomize_octaves',
                                    help='If checked, the octaves of the notes will be randomized. '
                                         'Otherwise, the notes will be played in the same octave.')
    resize_to_n_pixels = st.checkbox('***Resize image to N pixels***', key='resize_to_n_pixels',
                                     help='If checked, the image will be resized to N pixels. '
                                          'Otherwise, the image will be used as is. '
                                          'N is the number of pixels selected above.')

    # ***Start Pedalboard Definitions***
    st.markdown("## Pedalboard")
    with st.expander("###### Click here to see the pedalboard"):
        col4, col5, col6, col7 = st.columns(4)
        # Chorus Parameters
        with col4:
            st.markdown("### Chorus")
            rate_hz_chorus = st.slider('rate_hz', min_value=0.0, max_value=100.0, step=0.1, key='rate_hz_chorus',
                                       help='The rate_hz parameter controls the rate of the chorus effect. ')

        # Delay Parameters
        with col5:
            st.markdown("### Delay")
            delay_seconds = st.slider('delay_seconds',
                                      key='delay_seconds',
                                      min_value=0.0, max_value=2.0, step=0.1,
                                      help='The delay_seconds parameter controls the delay of the effect. ')

        # Distortion Parameters
        with col6:
            st.markdown("### Distortion")
            drive_db = st.slider('drive_db', min_value=0.0, max_value=100.0, step=1.0,
                                 key='drive_db',
                                 help='The drive_db parameter controls the amount of distortion. ')

        # Gain Parameters
        with col7:
            st.markdown("### Gain")
            gain_db = st.slider('gain_db', min_value=0.0, max_value=100.0, step=1.0,
                                key='gain_db',
                                help='The gain_db parameter controls the gain of the effect. ')

        st.markdown("### Reverb")
        rev1, rev2, rev3, rev4, rev5 = st.columns(5)
        # Reverb Parameters
        with rev1:
            room_size = st.slider('room_size', min_value=0.0, max_value=1.0, step=0.1,
                                  key='room_size',
                                  help='The room_size parameter controls the size of the reverbing room. ')
        with rev2:
            damping = st.slider('damping', min_value=0.0, max_value=1.0, step=0.1,
                                key='damping')
        with rev3:
            wet_level = st.slider('wet_level', min_value=0.0, max_value=1.0, step=0.1,
                                  key='wet_level',
                                  help='The wet_level parameter controls the amount of wet signal. ')
        with rev4:
            dry_level = st.slider('dry_level', min_value=0.1, max_value=1.0, step=0.1, key='dry_level',
                                  help='The dry_level parameter controls the amount of dry signal. ')
        with rev5:
            width = st.slider('width', min_value=0.0, max_value=1.0, step=0.1, key='width',
                              help='The width parameter controls the width of the stereo image. ')

        st.markdown("### Ladder Filter")

        lf1, lf2, lf3 = st.columns(3)
        # Ladder Filter Parameters
        with lf1:
            cutoff_hz = st.slider('cutoff_hz', min_value=0.0, max_value=1000.0, step=1.0,
                                  key='cutoff_hz',
                                  help='The cutoff_hz parameter controls the cutoff frequency of the filter. ')
        with lf2:
            resonance_lad = st.slider('resonance', min_value=0.0, max_value=1.0, step=0.1,
                                      key='resonance_lad',
                                      help='The resonance parameter controls the resonance of the filter. ')
        with lf3:
            drive_lad = st.slider('drive', min_value=1.0, max_value=100.0, step=0.1,
                                  key='drive_lad',
                                  help='The drive parameter controls the drive of the filter. ')

    return {
        'scale': scale,
        'key': key,
        'octave': octave,
        'harmony': harmony,
        'randomize_octaves': randomize_octaves,
        'resize_to_n_pixels': resize_to_n_pixels,
        't_value': t_value,
        'n_pixels': n_pixels,
        'gain_db': gain_db,
        'drive_db': drive_db,
        'cutoff_hz': cutoff_hz,
        'resonance_lad': resonance_lad,
        'drive_lad': drive_lad,
        'delay_seconds': delay_seconds,
        'room_size': room_size,
        'damping': damping,
        'wet_level': wet_level,
        'dry_level': dry_level,
        'width': width,
        'rate_hz_chorus': rate_hz_chorus
    }


if __name__ == '__main__':
    # all newly created files will be deleted when the context manager exits
    with tempfile.TemporaryDirectory() as tmpdir:

        init_session_state()  # tells to use the default parameters

        plh = write_intro()  # returns placeholder for the rolling title

        handle_presets() # load/upload presets

        img, filename = make_sidebar_and_select_file()

        param_dict = make_widgets_and_get_parameters()

        if filename is not None:
            # convert the image to RGB and resize it if necessary
            img = resize_and_convert(filename, tmpdir=tmpdir,
                                     n_pixels=param_dict['n_pixels'] if param_dict['resize_to_n_pixels'] else None)
            del param_dict['resize_to_n_pixels']

            # Generate the track
            track = trackmaker(img, **param_dict)

            # Display the track
            st.audio(track, format='audio/wav')

            # buttons
            b0, b1, _ = st.columns([1, 1, 2], gap='small')
            with b0:
                st.download_button('Download Track', data=track, file_name=f'{filename}.wav', mime='audio/wav')

            with b1:
                exp_preset_name = filename.split('/')[-1] if filename.startswith(tmpdir) else filename

                st.download_button('Export Preset',
                                   data=json.dumps(param_dict),
                                   file_name=f'{exp_preset_name}.json',
                                   mime='application/json')

    # footer at the bottom of the sidebar
    st.sidebar.markdown("""
        <style>
            .sidebar .sidebar-content {
            background: url("https://images.unsplash.com/photo-1557695126-fa2ce36f6828?q=80&w=2670&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
            background-size: cover;
            background-opacity: 0;
            }
            a:link , a:visited{
            color: white;
            background-color: transparent;
            text-decoration: underline;
            }
            
            a:hover,  a:active {
            color: red;
            background-color: transparent;
            text-decoration: underline;
            }
        </style>
        Developed by <a href=https://linktr.ee/andreafailla>Andrea Failla</a><br>
        Powered by <img src="https://user-images.githubusercontent.com/7164864/217935870-c0bc60a3-6fc0-4047-b011-7b4c59488c91.png" style="width:20px;height:10px;"><br>
        Leave a :star: on <a href=https://github.com/andreafailla/pix2beats>GitHub</a>!
        """,
                        unsafe_allow_html=True)

    towrite = 'Where each image tells a unique musical story'
    rolling_title(plh, towrite, 0.05)
