import sexyphone
import numpy as np
import re

def onCook2(scriptOp):
	scriptOp.clear()
	
	# get input value
	chop1 = scriptOp.inputs[0]
	channel0 = chop1[0]
	value0 = channel0.eval()
	
	# create new out channels
	a = scriptOp.appendChan('out1')
	b = scriptOp.appendChan('out2')
	c = scriptOp.appendChan('out3')
	
	# assign out channels
	# with below values
	a[0] = value0*0.5
	b[0] = value0
	c[0] = ((value0+value0)/100)*value0
	return

def onCook(scriptOp):
    scriptOp.clear()
	
    detections = sexyphone.run_sexyphone_detections()
    if detections is None:
        return
    
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

    for v in reduced_vals:
        chan = scriptOp.appendChan(v[0])
        chan[0] = v[1][1]
    
    scriptOp.numSamples = 1

    return

def onSetupParameters(scriptOp):
    return

def onPulse(par):
    return
