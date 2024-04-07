import cv2
import argparse

import supervision as sv
import numpy as np
from ultralytics import YOLO, SAM, checks, hub

model = None
cap = cv2.VideoCapture(0)
# enumerate capture devices
for i in range(0, 10):
    print(f"Device {i}: {cap.get(i)}")
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

try:
    model = YOLO("yolov8l.pt")
except:
    print("Caught error")

# hub.login('caeded7d33870b4fdd4ae54fb86a07468cadba0d40')
# model = YOLO('https://hub.ultralytics.com/models/kzceP1pjvCKqSHMWjs5v')

bounding_box_annotator = sv.BoundingBoxAnnotator()
label_annotator = sv.LabelAnnotator()

def arrayInfo(arr):
   return f"Datatype: {arr.dtype}, Dimensions: {arr.shape}"

def run_sexyphone_detections():
    ret, frame = cap.read()

    if ret:
        result = model(frame, agnostic_nms=True)[0]
        detections = sv.Detections.from_ultralytics(result)

        for det in detections:
            print(det)

        return detections
    else:
        print("Could not read frame")
        return None

def run_sexyphone_frame():
    ret, frame = cap.read()

    result = model(frame, agnostic_nms=True)[0]
    detections = sv.Detections.from_yolov8(result)
    labels = [
        model.model.names[class_id]
        for class_id
        in detections.class_id
    ]

    annotated_image = bounding_box_annotator.annotate(scene=image, detections=detections)
    annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections, labels=labels)

    return annotated_image

def opencv_to_td_frame(frame):
    # Convert BGR to RGB
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Add an alpha channel, filled with 255 (fully opaque)
    h, w, _ = frame.shape
    alpha_channel = np.ones((h, w, 1), dtype=np.uint8) * 255
    frame_with_alpha = np.concatenate((frame, alpha_channel), axis=-1)
    
    # Convert to float32 and normalize to 0.0 - 1.0 range
    frame_with_alpha = frame_with_alpha.astype(np.float32) / 255.0
    
    return frame_with_alpha


if __name__ == "__main__":
    while True:
        frame = run_sexyphone_frame()
        cv2.imshow("Sexyphone", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()