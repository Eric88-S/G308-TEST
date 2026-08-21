from ultralytics import YOLO

model = YOLO(r"D:\deeplearning\ultralytics-8.3.163\runs\detect\train4\weights\best.pt")
model.predict(
    source=r"D:\deeplearning\make_dataset\vidos",
    show = False,
    save = True,

)