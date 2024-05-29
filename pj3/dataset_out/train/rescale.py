import os
import xml.etree.ElementTree as ET

# 输入和输出文件夹路径
input_folder = 'labels'
output_folder = 'resized_labels'

# 输出文件夹不存在则创建
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# 缩放比例
scale_x = 640 / 1024
scale_y = 512 / 768

# 遍历输入文件夹中的XML文件
for filename in os.listdir(input_folder):
    if filename.endswith(".xml"):
        # 解析XML文件
        xml_path = os.path.join(input_folder, filename)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 调整XML文件中的位置值
        for obj in root.findall('object'):
            try:
                x = float(obj.find('point/x').text)
                y = float(obj.find('point/y').text)
            except (ValueError, AttributeError):
                try:
                    xmin = float(obj.find('bndbox/xmin').text)
                    ymin = float(obj.find('bndbox/ymin').text)
                    xmax = float(obj.find('bndbox/xmax').text)
                    ymax = float(obj.find('bndbox/ymax').text)
                    x = (xmin + xmax) // 2
                    y = (ymin + ymax) // 2
                except (ValueError, AttributeError):
                    continue

            x = int(x * scale_x)
            y = int(y * scale_y)
        
            obj.find('point/x').text = str(x)
            obj.find('point/y').text = str(y)

        # 保存调整后的XML文件
        output_path = os.path.join(output_folder, filename)
        tree.write(output_path)

print("XML文件调整完成")
