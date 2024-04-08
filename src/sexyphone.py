import cv2
import argparse

import supervision as sv
import numpy as np
from ultralytics import YOLO, SAM, checks, hub
import platform

model = None

global VIDEO_WIDTH

VIDEO_WIDTH=640
VIDEO_HEIGHT=480
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, VIDEO_WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, VIDEO_HEIGHT)
cap.set(cv2.CAP_PROP_FPS, 30)


try:
    # See for values => https://docs.ultralytics.com/models/yolov8/#overview
    model = YOLO("yolov8n.pt")
except:
    print("Caught error")

def arrayInfo(arr):
   return f"Datatype: {arr.dtype}, Dimensions: {arr.shape}"

def run_sexyphone_detections():
    ret, frame = cap.read()
 
    if ret:
        # write if to detect os is windows
        if platform.system() == 'Windows':
            dv="cpu"
        elif platform.system() == 'Darwin':
            dv="mps"


        result = model.predict(frame, device=dv, verbose=False, max_det=4, stream_buffer=True, imgsz=(480,640), classes=[39])[0]
        detections = sv.Detections.from_ultralytics(result)

        # for det in detections:
        #     print(det)

        return detections
    else:
        print(f"Could not read frame:{ret}")
        return None

def run_sexyphone_frame():
    ret, frame = cap.read()

    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    result = model(frame, agnostic_nms=True)[0]
    detections = sv.Detections.from_ultralytics(result)
    labels = [
        model.model.names[class_id]
        for class_id
        in detections.class_id
    ]

    annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)
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