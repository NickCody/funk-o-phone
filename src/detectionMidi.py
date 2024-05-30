# me - this DAT
# scriptOp - the OP which is cooking
import time


# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
    return

# called whenever custom pulse parameter is pushed
def onPulse(par):
    return


def onCook(scriptOp):
    scriptOp.clear()

    target_midi = scriptOp.parent().par.Targetmidiout
    low_frequency = int(op('lowfrequency').par.value0) 
    high_frequency = int(op('highfrequency').par.value0) 
    channel = int(op('channel').par.value0)
    velocity = int(op('velocity').par.value0)
    tempo_coefficient = scriptOp.inputs[0][0]
    midiNote = scriptOp.inputs[1][0]

    
    if midiNote == None or tempo_coefficient == None:
        send_all_off(channel, target_midi)
        return

    VALID_NOTES = [1,3,4,6,8,9,11,13,15,16,18,20,21,23,25,27,28,30,32,33,35,37,39,42,44,45,47,51,52,54,56,57,59,61,63,64,66,68,69,71,73,75,76,78,80,81,83,85,87,88,90,92,93,95,97,99,100,102,104,105,107,109,111,112,114,116,117,119,121,123,124,126]

    idx = int(midiNote/128.0 * len(VALID_NOTES))
    #constrain idx to the length of the VALID_NOTES list
    idx = min(idx, len(VALID_NOTES)-1)
    midiNote = VALID_NOTES[idx]
    
    current_milliseconds = int(time.time() * 1000.0)
    last_note_milliseconds = scriptOp.fetch('last_note_milliseconds', current_milliseconds, storeDefault=True)
    # last_note_played = scriptOp.fetch('last_note_played', midiNote, storeDefault=True)
    duration = current_milliseconds - last_note_milliseconds

    midiNote = int(midiNote)
    
    # freq = low_frequency + abs(high_frequency - low_frequency) * tempo_coefficient
    # if duration > freq:
    #     if midiNote == last_note_played:
    #         scriptOp.store('last_note_played', 0)
    #         return
    #     else:
    #         add_note_channel(scriptOp, channel, midiNote, velocity)
    #         scriptOp.store('last_note_played', midiNote)
    #         scriptOp.store('last_note_milliseconds', current_milliseconds)
    # else:
    #     if last_note_played != 0:
    #         add_note_channel(scriptOp, channel, last_note_played, velocity)

    # send_all_off(channel, target_midi)
    # add_note_channel(scriptOp, channel, midiNote, velocity)
    

    if duration < high_frequency and duration > low_frequency:
        send_all_off(channel, target_midi)
    else:
        add_note_channel(scriptOp, channel, midiNote, velocity)

    # if duration > high_frequency:
    #     send_note(channel, midiNote, velocity, target_midi)
        
    scriptOp.store('last_note_milliseconds', current_milliseconds)
    # scriptOp.numSamples = 1

    return

def add_note_channel(scriptOp, channel, note, velocity):
    # print(f"Playing {note} on channel {channel} with velocity {velocity}")
    chan = scriptOp.appendChan(f"ch{channel}n{note}")
    # chan = scriptOp.appendChan(f"ch{channel}n")
    chan[0] = velocity

def send_note(channel, note, velocity, midi_out_str):
    # Get reference to the MIDI Out CHOP
    midi_out = op(midi_out_str)

    # Define Note On message components
    status_byte = 0x90 + (channel-1)
    note_number = note  # MIDI note number
    velocity = velocity  # Velocity value

    # Construct Note On message as a list
    note_on_message = [status_byte.to_bytes(1, 'little'), note_number.to_bytes(1, 'little'), velocity.to_bytes(1, 'little')]

    # Convert the message list to bytes
    note_on_bytes = b''.join(note_on_message)

    # Send Note On message through MIDI Out CHOP
    midi_out.send(note_on_bytes)    


def send_all_off(channel, midi_out_str):
    # Get reference to the MIDI Out CHOP
    midi_out = op(midi_out_str)

    # Define All Notes Off message components
    status_byte = 0xB0 + (channel-1)  # Control Change message on MIDI channel 1
    controller_number = 0x7B  # All Notes Off controller number
    value = 0x00  # Value for turning off all notes

    # Construct All Notes Off message as a list
    all_notes_off_message = [status_byte, controller_number, value]

    # Convert the message list to bytes
    all_notes_off_bytes = bytes(all_notes_off_message)

    # Send All Notes Off message through MIDI Out CHOP
    midi_out.send(all_notes_off_bytes)

def send_note_off(channel, note, midi_out_str):
    # Get reference to the MIDI Out CHOP
    midi_out = op(midi_out_str)

    # Define Note Off message components
    status_byte = 0x80 + (channel-1)  # Note Off message on MIDI channel 1
    note_number = note  # MIDI note number
    velocity = 0  # Velocity value

    # Construct Note Off message as a list
    note_off_message = [status_byte, note_number, velocity]

    # Convert the message list to bytes
    note_off_bytes = bytes(note_off_message)

    # Send Note Off message through MIDI Out CHOP
    midi_out.send(note_off_bytes)