import sexyphone
import numpy as np
import re
from sexyphone import VIDEO_WIDTH, VIDEO_HEIGHT

def onCook(scriptOp):
    scriptOp.clear()

    half_precision = op("../AI_Detector").par.Halfprecision
    min_confidence = op("../AI_Detector").par.Minconfidence
    history_len = op("../AI_Detector").par.Historylength
    detectio_csv = op("../AI_Detector").par.Detectioncsv
    max_detection = op("../AI_Detector").par.Maxdetection
    detection_filter = [item.strip() for item in detectio_csv.eval().split(',')]

    detections = [
        (det[5]['class_name'], det[2], det[0])
        for det in sexyphone.run_sexyphone_detections(detection_filter, int(max_detection), float(min_confidence), 
                                                      bool(half_precision))
    ]
    
    vals = []
    if detections is not None:
        for det in detections:
            print(det)
            class_name, confidence, coords = det
            x1, y1, x2, y2= coords
            percent_x = ((x1+x2)/2)/VIDEO_WIDTH
            percent_y = ((y1+y2)/2)/VIDEO_HEIGHT
            vals.append((class_name, confidence, (percent_x, percent_y)))

    max_confidences = {}

    for class_name, confidence, coord in vals:
        base_class = re.match(r"([a-zA-Z]+)", class_name).group(1)
        if base_class not in max_confidences or confidence > max_confidences[base_class][0]:
            max_confidences[base_class] = (confidence, (coord[0], coord[1]))

    for k,v in max_confidences.items():
        chan = scriptOp.appendChan(f"{k}x")
        chan[0] = v[1][0]
        chan = scriptOp.appendChan(f"{k}y")
        chan[0] = v[1][1]
    
    scriptOp.numSamples = 1

    return

def onSetupParameters(scriptOp):
    return

def onPulse(par):
    return
