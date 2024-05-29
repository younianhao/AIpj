import os

def rename_images(directory):
    # 获取文件夹中所有文件的列表
    files = os.listdir(directory)
    
    # 遍历文件列表
    for file in files:
        # 检查文件是否为图片文件
        if file.endswith(".jpg"):
            # 分割文件名，获取数字部分
            number = file.split("_")[1].split(".")[0]
            # 构建新的文件名
            new_name = f"{number}.jpg"
            # 重命名文件
            os.rename(os.path.join(directory, file), os.path.join(directory, new_name))
            print(f"Renamed {file} to {new_name}")

# 调用函数并传入文件夹路径
rename_images('images')
