from PIL import Image, ImageDraw
import os
import xml.etree.ElementTree as ET
import random

# 添加黑白两种颜色的大点噪点的函数
def add_noise_to_image(img):
    draw = ImageDraw.Draw(img)
    width, height = img.size
    for _ in range(1000):  # 添加1000个噪点
        x = random.randint(0, width)
        y = random.randint(0, height)
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))  # 随机选择颜色
        draw.ellipse([x, y, x+2, y+2], fill=color)  # 在随机位置添加大小为5x5的椭圆噪点
    return img

# 修改后的函数
def add_noise_to_image_and_xml(input_rgb_file, input_xml_file, output_rgb_file, output_xml_file):
    # 处理图像文件
    img = Image.open(input_rgb_file)
    img_with_noise = add_noise_to_image(img)
    img_with_noise.save(output_rgb_file)

    # 处理XML文件
    tree = ET.parse(input_xml_file)
    # 在这里进行XML文件的处理

    tree.write(output_xml_file)

# 文件夹路径
rgb_path = "./dataset/train/rgb/"
xml_path = "./dataset/train/labels/"

# 获取文件列表
file_list = list(range(1, 1807))
selected_files = random.sample(file_list, 3)
for index in selected_files:
    input_rgb_file = os.path.join(rgb_path, str(index) + ".jpg")
    input_xml_file = os.path.join(xml_path, str(index) + "R.xml")

    output_rgb_file = os.path.join(rgb_path, "_Noise" + str(index) + ".jpg")
    output_xml_file = os.path.join(xml_path, "_Noise" + str(index) + "R.xml")
    add_noise_to_image_and_xml(input_rgb_file, input_xml_file, output_rgb_file, output_xml_file)
print("successfully create 100 samples with random noise")