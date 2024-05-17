from PIL import Image
import os
import xml.etree.ElementTree as ET
import random

def split_and_combine_images(input_rgb_file1, input_rgb_file2, input_xml_file1, input_xml_file2, output_rgb_file, output_xml_file):
    # 处理图像文件
    img1 = Image.open(input_rgb_file1)
    img2 = Image.open(input_rgb_file2)
    width, height = img1.size
    half_width = width // 2

    left_half1 = img1.crop((0, 0, half_width, height))
    right_half2 = img2.crop((half_width, 0, width, height))
    combined_img = Image.new('RGB', (width, height))
    combined_img.paste(left_half1, (0, 0))
    combined_img.paste(right_half2, (half_width, 0))
    combined_img.save(output_rgb_file)

    # 处理XML文件
    tree1 = ET.parse(input_xml_file1)
    tree2 = ET.parse(input_xml_file2)
    root1 = tree1.getroot()
    root2 = tree2.getroot()

    combined_tree = ET.ElementTree(ET.Element("annotation"))
    combined_root = combined_tree.getroot()

    for element in root1.findall('size') + root1.findall('segmented'):
        combined_root.append(element)

    for obj in root1.findall('object'):
        name = obj.find('name').text
        if name == 'person':
            x = 0
            try:
                x = int(obj.find('point/x').text)
            except:
                xmin = int(obj.find('bndbox/xmin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                x = (xmin + xmax) // 2
            if x >=0 and x < half_width:
                combined_root.append(obj)

    for obj in root2.findall('object'):
        name = obj.find('name').text
        if name == 'person':
            x = 0
            try:
                x = int(obj.find('point/x').text)
            except:
                xmin = int(obj.find('bndbox/xmin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                x = (xmin + xmax) // 2
            if x >=half_width and x <= width:
                combined_root.append(obj)

    combined_tree.write(output_xml_file)

# 文件夹路径
rgb_path = "./dataset/train/rgb/"
xml_path = "./dataset/train/labels/"

# 获取文件列表
file_list = list(range(1, 1807))
selected_files1 = random.sample(file_list, 300)
selected_files2 = random.sample(file_list, 300)

# 遍历文件并处理
for index1, index2 in zip(selected_files1, selected_files2):
    input_rgb_file1 = os.path.join(rgb_path, str(index1) + ".jpg")
    input_rgb_file2 = os.path.join(rgb_path, str(index2) + ".jpg")
    input_xml_file1 = os.path.join(xml_path, str(index1) + "R.xml")
    input_xml_file2 = os.path.join(xml_path, str(index2) + "R.xml")

    output_rgb_file = os.path.join(rgb_path, "_combined" + str(index1) + "and" + str(index2) + ".jpg")
    output_xml_file = os.path.join(xml_path, "_combined" + str(index1) + "and" + str(index2) + "R.xml")

    split_and_combine_images(input_rgb_file1, input_rgb_file2, input_xml_file1, input_xml_file2, output_rgb_file, output_xml_file)