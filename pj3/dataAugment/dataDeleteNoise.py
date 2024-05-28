from PIL import Image, ImageFilter
import os
import xml.etree.ElementTree as ET
import random

# 修改后的函数
def denoise_to_image_and_xml(input_rgb_file, input_xml_file, output_rgb_file, output_xml_file):
    # 处理图像文件
    img = Image.open(input_rgb_file)
    img_with_denoise = img.filter(ImageFilter.SHARPEN)
    img_with_denoise.save(output_rgb_file)

    # 处理XML文件
    tree = ET.parse(input_xml_file)
    # 在这里进行XML文件的处理

    tree.write(output_xml_file)

# 文件夹路径
rgb_path = "./dataset/train/rgb/"
xml_path = "./dataset/train/labels/"

# 获取文件列表
file_list = list(range(1652, 1655))
selected_files = random.sample(file_list, 3)
for index in selected_files:
    input_rgb_file = os.path.join(rgb_path, str(index) + ".jpg")
    input_xml_file = os.path.join(xml_path, str(index) + "R.xml")

    output_rgb_file = os.path.join(rgb_path, "_DeNoise" + str(index) + ".jpg")
    output_xml_file = os.path.join(xml_path, "_DeNoise" + str(index) + "R.xml")
    denoise_to_image_and_xml(input_rgb_file, input_xml_file, output_rgb_file, output_xml_file)
print("successfully create 100 samples with denoise")