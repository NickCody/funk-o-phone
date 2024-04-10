import sexyphone
import numpy as np
import re
from sexyphone import VIDEO_WIDTH, VIDEO_HEIGHT
import ChannelManager

channelManager = ChannelManager.ChannelKeySet(60)

def onCook(scriptOp):
    scriptOp.clear()

    history_len = op("../AI_Detector").par.Historylength
    detectio_csv = op("../AI_Detector").par.Detectioncsv
    max_detection = op("../AI_Detector").par.Maxdetection
    detection_vector = [item.strip() for item in detectio_csv.eval().split(',')]
    detections = sexyphone.run_sexyphone_detections(detection_vector, int(max_detection))
    
    channelManager.set_hist(history_len)

    # if len(detections) == 0:
    #     return
    
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
            x_c = (coord[0] + coord[2])/2
            y_c = (coord[1] + coord[3])/2
            max_confidences[base_class] = (confidence,(x_c,y_c))

    reduced_vals = [(class_id, confidence) for class_id, confidence in max_confidences.items()]
    reduced_vals = [v for v in reduced_vals]
     
    for v in reduced_vals:
        channelManager.add_key(v[0], (v[1][1][0] / VIDEO_WIDTH, v[1][1][1] / VIDEO_HEIGHT))

    for k,v1 in channelManager:
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
