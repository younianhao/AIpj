from PIL import Image
import os
import xml.etree.ElementTree as ET
import random

def crop_and_resize_image_and_xml(input_rgb_file, input_xml_file, output_rgb_file, output_xml_file,crop_scale):
    # 处理图像文件
    img = Image.open(input_rgb_file)
    width, height = img.size
    right = width*0.5 + width*crop_scale*0.5
    bottom = height*0.5 + height*crop_scale*0.5
    left = width*0.5 - width*crop_scale*0.5
    top = height*0.5 - height*crop_scale*0.5
    cropped_img = img.crop((left, top, right, bottom))
    cropped_img = cropped_img.resize((width, height))  # 将裁剪后的图像缩放回原始尺寸
    cropped_img.save(output_rgb_file)

    #处理XML文件
    tree = ET.parse(input_xml_file)
    root = tree.getroot()
    width = int(root.find('size/width').text)
    height = int(root.find('size/height').text)
    for obj in root.findall('object'):
        name = obj.find('name').text
        if name == 'person':
            x = 0
            try:
                point = obj.find('point')
                x = int(obj.find('point/x').text)
                y = int(obj.find('point/y').text)
                if x >=left and x < right and y >=top and y < bottom: 
                    point.find('x').text = str(round((x-left)/(right-left)*width))
                    point.find('y').text = str(round((y-top)/(bottom-top)*height))
                else:
                    root.remove(obj)
            except:
                bndbox = obj.find('bndbox')
                xmin = int(obj.find('bndbox/xmin').text)
                ymin = int(obj.find('bndbox/ymin').text)
                xmax = int(obj.find('bndbox/xmax').text)
                ymax = int(obj.find('bndbox/ymax').text)
                x = (xmin + xmax) // 2
                if x >=left and x < right and y >=top and y < bottom: 
                    bndbox.find('xmin').text = str(round((xmin-left)/(right-left)*width))
                    bndbox.find('ymin').text = str(round((ymin-top)/(bottom-top)*height))
                    bndbox.find('xmax').text = str(round((xmax-left)/(right-left)*width))
                    bndbox.find('ymax').text = str(round((ymax-top)/(bottom-top)*height))
                else:
                    root.remove(obj)
    tree.write(output_xml_file)

# 文件夹路径
rgb_path = "./dataset/train/rgb/"
xml_path = "./dataset/train/labels/"
crop_scale= 0.4

# 获取文件列表
file_list = list(range(1, 1807))
selected_files = random.sample(file_list, 300)
for index in selected_files:
    input_rgb_file = os.path.join(rgb_path, str(index) + ".jpg")
    input_xml_file = os.path.join(xml_path, str(index) + "R.xml")

    output_rgb_file = os.path.join(rgb_path, "_Crop" + str(index) + ".jpg")
    output_xml_file = os.path.join(xml_path, "_Crop" + str(index) + "R.xml")
    crop_and_resize_image_and_xml(input_rgb_file, input_xml_file, output_rgb_file, output_xml_file, crop_scale)
print("successfully create 300 cropped and resized samples")