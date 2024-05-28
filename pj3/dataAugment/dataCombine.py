from PIL import Image
import os
import xml.etree.ElementTree as ET
import random

def split_and_combine_images(cd, input_xml_files, output_rgb_file, output_xml_file):
    # 处理rgb图像文件
    img1 = Image.open(input_rgb_files[0])
    img2 = Image.open(input_rgb_files[1])
    img3 = Image.open(input_rgb_files[2])
    img4 = Image.open(input_rgb_files[3])
    width, height = img1.size
    half_width = width // 2
    half_height = height // 2

    part1 = img1.crop((0, 0, half_width, half_height))
    part2 = img2.crop((half_width, 0, width, half_height))
    part3 = img3.crop((0, half_height, half_width, height))
    part4 = img4.crop((half_width, half_height, width, height))
    combined_img = Image.new('RGB', (width, height))
    combined_img.paste(part1, (0, 0))
    combined_img.paste(part2, (half_width, 0))
    combined_img.paste(part3, (0, half_height))
    combined_img.paste(part4, (half_width, half_height))
    combined_img.save(output_rgb_file)

    # 处理XML文件
    tree1 = ET.parse(input_xml_files[0])
    tree2 = ET.parse(input_xml_files[1])
    tree3 = ET.parse(input_xml_files[2])
    tree4 = ET.parse(input_xml_files[3])
    root1 = tree1.getroot()
    root2 = tree2.getroot()
    root3 = tree3.getroot()
    root4 = tree4.getroot()

    combined_tree = ET.ElementTree(ET.Element("annotation"))
    combined_root = combined_tree.getroot()

    for element in root1.findall('size') + root1.findall('segmented'):
        combined_root.append(element)

    for obj in root1.findall('object'):
        name = obj.find('name').text
        if name == 'person':
            x = 0
            y = 0
            try:
                x = int(obj.find('point/x').text)
                y = int(obj.find('point/y').text)
            except:
                xmin = int(obj.find('bndbox/xmin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymin = int(obj.find('bndbox/ymin').text)
                ymax = int(obj.find('bndbox/ymax').text)
                x = (xmin + xmax) // 2
                y = (ymin + ymax) // 2
            if x >=0 and x < half_width and y>=0 and y < half_height:
                combined_root.append(obj)

    for obj in root2.findall('object'):
        name = obj.find('name').text
        if name == 'person':
            x = 0
            y = 0
            try:
                x = int(obj.find('point/x').text)
                y = int(obj.find('point/y').text)
            except:
                xmin = int(obj.find('bndbox/xmin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymin = int(obj.find('bndbox/ymin').text)
                ymax = int(obj.find('bndbox/ymax').text)
                x = (xmin + xmax) // 2
                y = (ymin + ymax) // 2
            if x >=half_width and x < width and y>=0 and y < half_height:
                combined_root.append(obj)

    for obj in root3.findall('object'):
        name = obj.find('name').text
        if name == 'person':
            x = 0
            y = 0
            try:
                x = int(obj.find('point/x').text)
                y = int(obj.find('point/y').text)
            except:
                xmin = int(obj.find('bndbox/xmin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymin = int(obj.find('bndbox/ymin').text)
                ymax = int(obj.find('bndbox/ymax').text)
                x = (xmin + xmax) // 2
                y = (ymin + ymax) // 2
            if x >=0 and x < half_width and y>=half_height and y < height:
                combined_root.append(obj)

    for obj in root4.findall('object'):
        name = obj.find('name').text
        if name == 'person':
            x = 0
            y = 0
            try:
                x = int(obj.find('point/x').text)
                y = int(obj.find('point/y').text)
            except:
                xmin = int(obj.find('bndbox/xmin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymin = int(obj.find('bndbox/ymin').text)
                ymax = int(obj.find('bndbox/ymax').text)
                x = (xmin + xmax) // 2
                y = (ymin + ymax) // 2
            if x >=half_width and x < width and y>=half_height and y < height:
                combined_root.append(obj)

    combined_tree.write(output_xml_file)

# 文件夹路径
rgb_path = "./dataset/train/rgb/"
xml_path = "./dataset/train/labels/"

# 获取文件列表
file_list = list(range(1, 20))
selected_files1 = random.sample(file_list, 300)
selected_files2 = random.sample(file_list, 300)
selected_files3 = random.sample(file_list, 300)
selected_files4 = random.sample(file_list, 300)

# 遍历文件并处理
for index1, index2, index3, index4 in zip(selected_files1, selected_files2, selected_files3, selected_files4):
    input_rgb_files = [os.path.join(rgb_path, str(index1) + ".jpg"), os.path.join(rgb_path, str(index2) + ".jpg"), os.path.join(rgb_path, str(index3) + ".jpg"), os.path.join(rgb_path, str(index4) + ".jpg")]
    input_xml_files = [os.path.join(xml_path, str(index1) + "R.xml"), os.path.join(xml_path, str(index2) + "R.xml"), os.path.join(xml_path, str(index3) + "R.xml"), os.path.join(xml_path, str(index4) + "R.xml")]

    output_rgb_file = os.path.join(rgb_path, "_combined" + str(index1) + "_" + str(index2) + "_" + str(index3) + "_" + str(index4) + ".jpg")
    output_xml_file = os.path.join(xml_path, "_combined" + str(index1) + "_" + str(index2) + "_" + str(index3) + "_" + str(index4) + "R.xml")

    split_and_combine_images(input_rgb_files, input_xml_files, output_rgb_file, output_xml_file)
print("successfully create 300 combined samples")