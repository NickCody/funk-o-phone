from ultralytics import YOLO


def main():
    model = YOLO('yolov8l.pt')  # yolov3-v7

    # iterate over model.names dict and custom format each row
    for k, v in model.names.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
