from ultralytics import YOLO

if __name__ == "__main__":
    model = YOLO(r"yolo11n-pose.pt")
    model.train(
        data=r"julong.yaml",
        epochs=10,
        imgsz=640,
        batch=2,
        cache="ram",
        workers=1,

    )




