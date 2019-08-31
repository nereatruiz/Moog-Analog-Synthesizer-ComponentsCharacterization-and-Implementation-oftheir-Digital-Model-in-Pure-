# Python requirements
# Runs on python 3
# pip install wave pyaudio python-rtmidi mido music21 

import pyaudio
import wave
import mido
import os
import time
import music21
import math
import csv

# Audio and midi config
CHUNK = 1024  # Audio buffer size
FORMAT = pyaudio.paInt16  # Audio format (16bit)
CHANNELS = 1  # Number of channels to record
RATE = 44100  # Sampling rate of the recorded files
MIDI_DEVICE_NAME = 'Slim Phatty'  # Device name of the MIDI output port
AUDIO_DEVICE_INDEX = 0  # Will use default audio device

# Sampling config
PRESETS_TO_SAMPLE = []  # Will be selected on the synth using MIDI Program Change messages
NOTE_SECONDS = 2  # Note sustain (time between note on and note off messages)
TAIL_SECONDS = 2  # Time recording after note off message
NOTE_MIN = 0  # Lowest MIDI note to sample
NOTE_MAX = 127  # Highest MIDI note to sample
VELOCITIES = [127]  # MIDI velocities to sample for each note
RECORDING_FOLDER = '.'  # Where the audio will be stored ('.' means current directory)

# Other config stuff
WRITE_CSV = True
RECORD_AUDIO = True

# Set MIDI and audio stuff
print('Available MIDI device names:')
for name in mido.get_output_names():
    print('\t{0}'.format(name))
try:
    outport = mido.open_output(MIDI_DEVICE_NAME)
    print('Will use MIDI output port "{0}" (change that by setting \'MIDI_DEVICE_NAME\' in sampler.py)'.format(MIDI_DEVICE_NAME))
except IOError:
    print('Could not connect to MIDI output port, skipping audio recording')
    RECORD_AUDIO = False
p = pyaudio.PyAudio()
print('Available audio device indexes:')
for i in range(0, p.get_device_count()):
    print('\t{0} - {1}'.format(i, p.get_device_info_by_index(i)['name']))
print('Will use audio device "{0}" (change that by setting \'AUDIO_DEVICE_INDEX\' in Moog Slim phatty parameters sampler.py)'.format(p.get_device_info_by_index(AUDIO_DEVICE_INDEX)['name']))


def seconds_to_time_label(seconds):
    hours_remaining = math.floor(seconds / 3600)
    extra_seconds = seconds % 3600
    minutes_remaining = math.floor(extra_seconds / 60)
    seconds_remaining = extra_seconds % 60
    return '%.2i:%.2i:%.2i remaining' % (hours_remaining, minutes_remaining, seconds_remaining)

def start_audio_stream():
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)
    return stream

def stop_audio_stream(stream):
    stream.stop_stream()
    stream.close()

def note_off_all():
    for midi_note in range(0, 127):
        outport.send(mido.Message('note_off', note=midi_note))

def get_note_list():
    notes = []
    for midi_note in range(NOTE_MIN, NOTE_MAX):
        for midi_vel in VELOCITIES:
            notes.append((midi_note, midi_vel))
    return notes

def sample_note(midi_note, midi_vel, output_filename, stream, parameter_settings=None):
    frames = []

    # Set parameter settings
    if parameter_settings is not None:
        for cc_number, value in parameter_settings:
            outport.send(mido.Message('control_change', control=cc_number, value=value))
    
    # Send note on and start recording for NOTE_SECONDS
    outport.send(mido.Message('note_on', note=midi_note, velocity=midi_vel))
    for i in range(0, int(RATE / CHUNK * NOTE_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # Send note off and continue recording during TAIL_SECONDS
    outport.send(mido.Message('note_off', note=midi_note))
    for i in range(0, int(RATE / CHUNK * TAIL_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    wf = wave.open(output_filename, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()


textual_description_template = """Single note sampled from a Moog Slim Phatty analogue synthesizer. <a href="https://www.moogmusic.com/products/slim-phatty/">Slim Phatty</a> is an 2-voice analogue synthesizer designed by Moog Music.
Synthesizer: Moog Slim Phatty
Factory preset #: %i
Note: %s
Midi note: %i
Midi velocity: %i
"""

def sample_preset(preset_number):
    print('\nSTARTING TO SAMPLE PRESET {0}!'.format(preset_number))

    # Send program change message to synth so preset it set
    if RECORD_AUDIO:
        outport.send(mido.Message('program_change', program=preset_number - 1))

    # Stop all notes (just in case)
    if RECORD_AUDIO:
        note_off_all()

    # Start audio stream and sampling process
    if RECORD_AUDIO:
        stream = start_audio_stream()
    failed = []
    existing = []
    recorded = []
    notes = get_note_list()
    csv_rows = []
    for count, (midi_note, midi_vel) in enumerate(notes):

        # Generate filename
        mp = music21.pitch.Pitch()
        mp.midi = midi_note
        note_name = mp.name.replace('-', 'b') + str(mp.octave)
        output_filename = '%s/Slim Phatty preset %.3i - %.3i (%s) - %.3i.wav' % (RECORDING_FOLDER, preset_number, midi_note, note_name, midi_vel)
        csv_rows.append([  # Prepare CSV information for Freesound bulk description
            output_filename[6:],  # Audio filename
            'Slim Phatty preset #%i - %s (%i) - vel %i' % (preset_number, note_name, midi_note, midi_vel), # Sound name
            ' '.join(['multisample single-note synthesizer analogue Moog Slim Phatty %s midi-note-%i midi-velocity-%i' % (note_name.replace('#', 'Sharp'), midi_note, midi_vel)]),  # Tags
            '',  # Geotag
            textual_description_template % (preset_number, note_name, midi_note, midi_vel),  # Textual description
            'Creative Commons 0',  # License
            'Slim Phatty preset #%i' % preset_number,  # Pack name
            '0',  # Is explicit
            ])

        if not os.path.exists(output_filename) and RECORD_AUDIO:
            seconds_remaining = (len(notes) - count) * (NOTE_SECONDS + TAIL_SECONDS)
            time_remaining_label = seconds_to_time_label(seconds_remaining)
            print("* recording {0} - {1} [{2}/{3}] - {4}".format(midi_note, midi_vel, count + 1, len(notes), time_remaining_label))
            try:
                sample_note(midi_note, midi_vel, output_filename, stream)
                recorded.append(output_filename)
            except IOError:
                # If something fails, send note off and do the next note
                # At a later re-run failed notes can be fixed
                print('ERROR with {0}, skipping'.format(output_filename))
                outport.send(mido.Message('note_off', note=midi_note))
                failed.append(output_filename)
                stream = start_audio_stream()  # restart audio stream
        else:
            existing.append(output_filename)

    if RECORD_AUDIO:
        stop_audio_stream(stream)
        note_off_all()

    print('DONE SAMPLING PRESET {0}!'.format(preset_number))
    if RECORD_AUDIO:
        print('{0} notes recorded successfully'.format(len(recorded)))
        print('{0} notes already existing'.format(len(existing)))
        print('{0} notes failed recording'.format(len(failed)))
    else:
        print('No new notes were recorded (audio recording disabled)')
    return failed, csv_rows

if RECORD_AUDIO:
    note_off_all()

expected_total_time = len(PRESETS_TO_SAMPLE) * len(VELOCITIES) * len(range(NOTE_MIN, NOTE_MAX)) * (NOTE_SECONDS + TAIL_SECONDS)
time_remaining_label = seconds_to_time_label(expected_total_time)
if RECORD_AUDIO:
    input('\n\nWill start sampling {0} presets, you want to continue? (will take approx {1})'.format(len(PRESETS_TO_SAMPLE), time_remaining_label))

for preset_number in PRESETS_TO_SAMPLE:
    while True:
        failed, csv_rows = sample_preset(preset_number)
        if not failed:
            if WRITE_CSV:
                csv_filename = 'Slim Phatty preset #%i descriptions.csv' % preset_number
                csv_header = ['audio_filename', 'name', 'tags', 'geotag', 'description', 'license', 'pack_name', 'is_explicit']
                csvfile = csv.writer(open(csv_filename, 'w'))
                csvfile.writerow(csv_header)
                csvfile.writerows(csv_rows)
                print('CSV output saved in %s' % csv_filename)
            break  # Break while loop if no sounds failed, otherwise run it again


PARAMETERS_CSV = [

# ADSR FILTER ATTACK
    
[3, [ (23,0), (24,0), (25,0), (26,0), (27,int(round(127*0.5))), (28,0), (29,0), (30, int(round(127*1.0))), (31,0), (19, int(round(127*1.0))),  (21,0),  (9, 0)]],
[4, [ (23,0), (24,0), (25,0), (26,0), (27,int(round(127*0.5))), (28,0), (29,0), (30, int(round(127*1.0))), (31,0), (19, int(round(127*1.0))),  (21,0),  (9, 6)]],
[5, [ (23,0), (24,0), (25,0), (26,0), (27,int(round(127*0.5))), (28,0), (29,0), (30, int(round(127*1.0))), (31,0), (19, int(round(127*1.0))),  (21,0),  (9, 43)]],
[6, [ (23,0), (24,0), (25,0), (26,0), (27,int(round(127*0.5))), (28,0), (29,0), (30, int(round(127*1.0))), (31,0), (19, int(round(127*1.0))),  (21,0),  (9, 89)]],
]



def sample_csv():

    print('\nSTARTING CSV!')

    # Send program change message to synth so preset it set
    if RECORD_AUDIO:
        outport.send(mido.Message('program_change', program=0))

    # Stop all notes (just in case)
    if RECORD_AUDIO:
        note_off_all()

    # Start audio stream and sampling process
    if RECORD_AUDIO:
        stream = start_audio_stream()
    failed = []
    recorded = []
    notes = get_note_list()


    for count, (row_number, params) in enumerate(PARAMETERS_CSV):

        output_filename = 'row %i.wav' % (row_number)
        midi_note = 54
        midi_vel = 127
        
        if RECORD_AUDIO:
            seconds_remaining = (len(PARAMETERS_CSV) - count) * (NOTE_SECONDS + TAIL_SECONDS)
            time_remaining_label = seconds_to_time_label(seconds_remaining)
            print("* recording [{0}/{1}] - {2}".format(count + 1, len(notes), time_remaining_label))
            try:
                sample_note(midi_note, midi_vel, output_filename, stream, parameter_settings=params)
                recorded.append(output_filename)
            except IOError:
                # If something fails, send note off and do the next note
                # At a later re-run failed notes can be fixed
                print('ERROR with {0}, skipping'.format(output_filename))
                outport.send(mido.Message('note_off', note=midi_note))
                failed.append(output_filename)
                stream = start_audio_stream()  # restart audio stream
       

    if RECORD_AUDIO:
        stop_audio_stream(stream)
        note_off_all()

    print('DONE SAMPLING CSV {0}!')
    if RECORD_AUDIO:
        print('{0} notes recorded successfully'.format(len(recorded)))
        print('{0} notes failed recording'.format(len(failed)))
    else:
        print('No new notes were recorded (audio recording disabled)')



sample_csv()  


    





p.terminate()
