from ultralytics import YOLO

if __name__ == "__main__":
    # 加载模型，可选yolov8n/s/m
    model = YOLO("yolov8s.pt")

    # 训练，epoch≥50
    results = model.train(
        data="data.yaml",
        epochs=80,
        imgsz=640,
        project="train_output",
        name="run3",
        dropout=0.15,
        erasing=0.1,
        deterministic=False
    )

    # 评估模型（val集）
    metrics = model.val()
    print("评估mAP指标：", metrics.box.map)

    # 推理，批量保存结果图
    infer_result = model.predict(
        source="./dataset/images/valid",
        save=True,
        save_txt=False,
        conf=0.15
    )