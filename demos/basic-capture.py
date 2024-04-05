import cv2
import argparse


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="YOLOv8 live")
    parser.add_argument(
        "--resolution",
        default=[1920, 1080],
        nargs=2,
        type=int
    )
    args = parser.parse_args()
    return args


def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        print(f"Datatype: {frame.dtype}, Dimensions: {frame.shape}")

        print(frame.shape)
        cv2.imshow("grove", frame)

        if (cv2.waitKey(30) == 27):
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
