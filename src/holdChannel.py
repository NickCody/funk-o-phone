# me - this DAT
# scriptOp - the OP which is cooking

# press 'Setup Parameters' in the OP to call this function to re-create the parameters.
def onSetupParameters(scriptOp):
	return

# called whenever custom pulse parameter is pushed
def onPulse(par):
	return

def onCook(scriptOp):
    scriptOp.clear()
    
    # ACEG
    
    # Access the input CHOP
    inputCHOP = scriptOp.inputs[0]
    persistChannel = op("../ai_midi_groove").par.Channel
    threshold = op("../ai_midi_groove").par.Threshold
    noteon = op("../ai_midi_groove").par.Noteon
    noteoff = op("../ai_midi_groove").par.Noteoff
    midiChannel = op("../ai_midi_groove").par.Midichannel
    
    print(midiChannel)
    # Check if the input CHOP has any channels
    if inputCHOP.numChans > 0:
        if isinstance(inputCHOP[0].vals[0], list):
            current = inputCHOP[0].vals[0][0]
        else:
            current = inputCHOP[0].vals[0]

        if current > threshold:
            add_note_channel(scriptOp, midiChannel, noteon, 127)
            scriptOp.store(persistChannel, current)
        else:
            add_note_channel(scriptOp, midiChannel, noteoff, 127)
            scriptOp.store(persistChannel, 0.0)
    else:
        # No input channels, use values from Hold CHOP
        current = scriptOp.fetch(persistChannel, 0.0, storeDefault=True)
        if current > threshold:
            add_note_channel(scriptOp, midiChannel, noteon, 127)
        else:
            add_note_channel(scriptOp, midiChannel, noteoff, 127)
	
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