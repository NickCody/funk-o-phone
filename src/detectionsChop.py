import sexyphone
import numpy as np
import re
from sexyphone import VIDEO_WIDTH
import ChannelManager

channelManager = ChannelManager.ChannelKeySet(20)

def onCook(scriptOp):
    scriptOp.clear()
	
    detections = sexyphone.run_sexyphone_detections()

    vals = [
            (f"{sexyphone.model.model.names[class_id]}", confidence, x)
            for x, confidence, class_id, _
            in detections
    ]

    max_confidences = {}

    for class_id, confidence, x in vals:
        base_class = re.match(r"([a-zA-Z]+)", class_id).group(1)
        
        if base_class not in max_confidences or confidence > max_confidences[base_class][0]:
            max_confidences[base_class] = (confidence,x[0])

    reduced_vals = [(class_id, confidence) for class_id, confidence in max_confidences.items()]

    reduced_vals = [v for v in reduced_vals if v[0] in ["bottle"]]
     
    for v in reduced_vals:
        channelManager.add_key(v[0], v[1][1] / VIDEO_WIDTH)
        print(v[1][1])

    for k,v in channelManager:
        chan = scriptOp.appendChan(k)
        chan[0] = v[1]
    
    scriptOp.numSamples = 1

    channelManager.increment_counter()

    return

def onSetupParameters(scriptOp):
    return

def onPulse(par):
    return
