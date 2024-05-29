from PIL import Image
import os
import xml.etree.ElementTree as ET
import random

def flip_image_and_xml(input_rgb_file, input_xml_file, output_rgb_file, output_xml_file):
    # 处理图像文件
    img = Image.open(input_rgb_file)
    flipped_img = img.transpose(Image.FLIP_TOP_BOTTOM)
    flipped_img = flipped_img.transpose(Image.FLIP_LEFT_RIGHT)
    flipped_img.save(output_rgb_file)

    # 处理XML文件
    tree = ET.parse(input_xml_file)
    root = tree.getroot()
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)
    for obj in root.findall('object'):
        name = obj.find('name').text
        if name == 'person':
            try:
                point = obj.find('point')
                x = int(obj.find('point/x').text)
                y = int(obj.find('point/y').text)
                point.find('x').text = str(width - x)
                point.find('y').text = str(height - y)
            except:
                bndbox = obj.find('bndbox')
                xmin = int(obj.find('bndbox/xmin').text)
                ymin = int(obj.find('bndbox/ymin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymax = int(obj.find('bndbox/ymax').text)
                bndbox.find('xmin').text = str(width - xmin)
                bndbox.find('ymin').text = str(height - ymin)
                bndbox.find('xmax').text = str(width - xmax)
                bndbox.find('ymax').text = str(height - ymax)
    tree.write(output_xml_file)

# 文件夹路径
rgb_path = "./dataset/train/rgb/"
xml_path = "./dataset/train/labels/"

# 获取文件列表
file_list = list(range(1, 1807))
selected_files = random.sample(file_list, 300)
for index in selected_files:
    input_rgb_file = os.path.join(rgb_path, str(index) + ".jpg")
    input_xml_file = os.path.join(xml_path, str(index) + "R.xml")

    output_rgb_file = os.path.join(rgb_path, str(index) + ".jpg")
    output_xml_file = os.path.join(xml_path, str(index) + "R.xml")
    flip_image_and_xml(input_rgb_file, input_xml_file, output_rgb_file, output_xml_file)
print("successfully create 300 rotated samples")