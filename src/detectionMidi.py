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

    
    midiNote = op('math_detect_to_midi')['ch4']

    # if midiNote != None:
    #     intNote = int(midiNote)
    #     midiNote = f"ch{intNote}"
    #     chan = scriptOp.appendChan(midiNote)
    #     chan[0] = 100
    #     scriptOp.numSamples = 1

    if midiNote != None:
        current_milliseconds = time.time() * 1000
        last_note_milliseconds = scriptOp.fetch('last_note_milliseconds', current_milliseconds, storeDefault=True)

        if current_milliseconds - last_note_milliseconds > 128:
            op('midiout2').sendNoteOn(1, midiNote, 60)
            scriptOp.store('last_note_milliseconds', current_milliseconds);

    return