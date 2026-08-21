from ultralytics import YOLO

model = YOLO(r"yolo11n-cls.pt")

print(model.task)

