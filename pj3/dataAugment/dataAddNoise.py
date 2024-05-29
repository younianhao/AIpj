from PIL import Image, ImageDraw
import os
import xml.etree.ElementTree as ET
import random

# 添加黑白两种颜色的大点噪点的函数
def add_noise_to_image(img):
    draw = ImageDraw.Draw(img)
    width, height = img.size
    for _ in range(500):  # 添加1000个噪点
        x = random.randint(0, width)
        y = random.randint(0, height)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # 随机选择颜色
        draw.ellipse([x, y, x+2, y+2], fill=color)  # 在随机位置添加大小为2x2的椭圆噪点
    return img

# 修改后的函数
def add_noise_to_image_and_xml(input_rgb_file, output_rgb_file):
    # 处理图像文件
    img = Image.open(input_rgb_file)
    img_with_noise = add_noise_to_image(img)
    img_with_noise.save(output_rgb_file)


# 文件夹路径
rgb_path = "./dataset/train/rgb/"

# 获取文件列表
file_list = list(range(1, 1807))
selected_files = random.sample(file_list, 300)
for index in selected_files:
    input_rgb_file = os.path.join(rgb_path, str(index) + ".jpg")

    output_rgb_file = os.path.join(rgb_path, str(index) + ".jpg")
    add_noise_to_image_and_xml(input_rgb_file, output_rgb_file)
print("successfully create 300 samples with random noise")