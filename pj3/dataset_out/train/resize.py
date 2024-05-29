from PIL import Image
import os

# 输入和输出文件夹路径
input_folder = 'images'
output_folder = 'resized_images'

# 输出文件夹不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 遍历输入文件夹中的图像文件
for filename in os.listdir(input_folder):
    if filename.endswith(".jpg") or filename.endswith(".png"):
        # 读取图像
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # 调整图像大小为640*512
        resized_img = img.resize((640, 512))

        # 保存调整大小后的图像
        output_path = os.path.join(output_folder, filename)
        resized_img.save(output_path)

print("图像调整大小完成")
