from PIL import Image, ImageEnhance
import os
import xml.etree.ElementTree as ET
import random

def random_color_transform(image, hue_factor, saturation_factor, brightness_factor):
    enhancer = ImageEnhance.Color(image)
    image = enhancer.enhance(hue_factor)  # 色调

    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(saturation_factor)  # 饱和度

    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(brightness_factor)  # 亮度

    return image

def random_image_color(input_rgb_file, input_xml_file, output_rgb_file, output_xml_file):
    # 处理图像文件
    img = Image.open(input_rgb_file)
    hue_factor, saturation_factor, brightness_factor = 1, 1, 1
    if random.random() > 0.5:
        hue_factor = random.uniform(0.25, 0.75)
    else:
        hue_factor = random.uniform(1.25, 1.75)
    if random.random() > 0.5:
        saturation_factor = random.uniform(0.25, 0.75)
    else:
        saturation_factor = random.uniform(1.25, 1.75)
    if random.random() > 0.5:
        brightness_factor = random.uniform(0.25, 0.75)
    else:
        brightness_factor = random.uniform(1.25, 1.75)
    img = random_color_transform(img, hue_factor, saturation_factor, brightness_factor)
    img.save(output_rgb_file)

    # 处理XML文件
    tree = ET.parse(input_xml_file)
    tree.write(output_xml_file)

# 文件夹路径
rgb_path = "./dataset/train/rgb/"
xml_path = "./dataset/train/labels/"

# 获取文件列表
file_list = list(range(1, 1807))
selected_files = random.sample(file_list, 600)
for index in selected_files:
    input_rgb_file = os.path.join(rgb_path, str(index) + ".jpg")
    input_xml_file = os.path.join(xml_path, str(index) + "R.xml")

    output_rgb_file = os.path.join(rgb_path, "_Color" + str(index) + ".jpg")
    output_xml_file = os.path.join(xml_path, "_Color" + str(index) + "R.xml")
    random_image_color(input_rgb_file, input_xml_file, output_rgb_file, output_xml_file)
print("successfully create 300 colored samples with random color transformation")