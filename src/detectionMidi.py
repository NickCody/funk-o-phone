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
    frequency = int(op('frequency').par.value0) 
    channel = int(op('channel').par.value0)
    velocity = int(op('velocity').par.value0)
    y_coord = scriptOp.inputs[0][0]
    midiNote = scriptOp.inputs[1][0]

    if midiNote == None or y_coord == None:
        return

    midiNote = int(midiNote)

    current_milliseconds = int(time.time() * 1000)
    last_note_milliseconds = scriptOp.fetch('last_note_milliseconds', current_milliseconds, storeDefault=True)
    last_note_played = scriptOp.fetch('last_note_played', int(op('lownote').par.value0), storeDefault=True)

    if current_milliseconds - last_note_milliseconds > frequency * y_coord:
        # print(f"Playing {midiNote} on channel {channel} with velocity {velocity}")
        # chan = scriptOp.appendChan(f"ch{channel}n")
        # chan[0] = midiNote
        # send_note(channel, midiNote, velocity, target_midi)
        scriptOp.store('last_note_milliseconds', current_milliseconds)
        scriptOp.store('last_note_played', midiNote)
    
    scriptOp.numSamples = 1

    return

def send_note(channel, note, velocity, midi_out_str):
    # Get reference to the MIDI Out CHOP
    midi_out = op(midi_out_str)

    # Define Note On message components
    status_byte = 0x90 + (channel-1)
    note_number = note  # MIDI note number
    velocity = velocity  # Velocity value

    # Construct Note On message as a list
    note_on_message = [status_byte, note_number, velocity]

    # Convert the message list to bytes
    note_on_bytes = bytes(note_on_message)

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