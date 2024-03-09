import cv2


def main():
    # enumerate all the cameras

    print("Enumerating camera devices")

    for i in range(10):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Camera {i} is available")
            cap.release()
        else:
            print(f"Camera {i} is not available")

if __name__ == "__main__":
    main()