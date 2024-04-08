import sexyphone
import numpy as np
import re
from sexyphone import VIDEO_WIDTH, VIDEO_HEIGHT
import ChannelManager

channelManager = ChannelManager.ChannelKeySet(20)

def onCook(scriptOp):
    scriptOp.clear()
	
    detections = sexyphone.run_sexyphone_detections()
    if detections is None:
        return
    
    vals = []
    for det in detections:
        coords, _, confidence, _, _, info = det
        x1, y1, _, _ = coords
        class_name = info['class_name']
        vals.append((class_name, confidence, (x1, y1)))

    max_confidences = {}

    for class_id, confidence, coord in vals:
        base_class = re.match(r"([a-zA-Z]+)", class_id).group(1)
        
        if base_class not in max_confidences or confidence > max_confidences[base_class][0]:
            max_confidences[base_class] = (confidence,(coord[0],coord[1]))

    reduced_vals = [(class_id, confidence) for class_id, confidence in max_confidences.items()]

    reduced_vals = [v for v in reduced_vals if v[0] in ["bottle"]]
     
    for v in reduced_vals:
        channelManager.add_key(v[0], (v[1][1][0] / VIDEO_WIDTH, v[1][1][1] / VIDEO_HEIGHT))

    for k,v1 in channelManager:
        print(f"{k}: {v1}")
        chan = scriptOp.appendChan(f"{k}x")
        chan[0] = v1[1][0]
        chan = scriptOp.appendChan(f"{k}y")
        chan[0] = v1[1][1]
    
    scriptOp.numSamples = 1

    channelManager.increment_counter()

    return

def onSetupParameters(scriptOp):
    return

def onPulse(par):
    return
