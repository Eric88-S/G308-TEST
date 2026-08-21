import os
import shutil

def data_preprocess():
    # 原始根目录（当前Second文件夹）
    origin_root = "./"
    # 输出标准YOLO文件夹
    out_root = "./dataset"

    split_list = ["train", "valid", "test"]
    # 创建目标标准目录：dataset/images/train ...  dataset/labels/train ...
    for split_name in split_list:
        os.makedirs(os.path.join(out_root, "images", split_name), exist_ok=True)
        os.makedirs(os.path.join(out_root, "labels", split_name), exist_ok=True)

    # 循环迁移 train / valid / test 的图片和标签
    for split_name in split_list:
        # 原始图片路径 Second/train/images
        src_img_dir = os.path.join(origin_root, split_name, "images")
        # 原始标签路径 Second/train/labels
        src_label_dir = os.path.join(origin_root, split_name, "labels")

        # 目标路径 dataset/images/train
        dst_img_dir = os.path.join(out_root, "images", split_name)
        dst_label_dir = os.path.join(out_root, "labels", split_name)

        # 复制全部图片
        for filename in os.listdir(src_img_dir):
            if filename.endswith((".jpg", ".png", ".jpeg","JPG")):
                src_file = os.path.join(src_img_dir, filename)
                dst_file = os.path.join(dst_img_dir, filename)
                shutil.copy(src_file, dst_file)

        # 复制全部标签txt
        for filename in os.listdir(src_label_dir):
            if filename.endswith(".txt"):
                src_file = os.path.join(src_label_dir, filename)
                dst_file = os.path.join(dst_label_dir, filename)
                shutil.copy(src_file, dst_file)

    print(" 文件迁移完成！结构已经转为标准YOLO格式")

# 启动入口，不要忘记！
if __name__ == '__main__':
    data_preprocess()