import numpy as np
import os
import xml.etree.ElementTree as ET
import h5py
from scipy.ndimage import gaussian_filter


def parse_xml(xml_file, image_shape):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    density_map = np.zeros(image_shape, dtype=np.float32)
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
                x = (xmin + xmax) / 2
                y = (ymin + ymax) / 2
            except (ValueError, AttributeError):
                continue
        x, y = int(x), int(y)
        if 0 <= y < image_shape[0] and 0 <= x < image_shape[1]:
            density_map[y, x] = 1
    density_map = gaussian_filter(density_map, sigma=15)
    return density_map


xml_path = "./dataset_out/train/resized_labels/"
mat_path = "./dataset_out/train/hdf5s/"
image_shape = (512, 640)  # Assuming the image shape is fixed

sum = 0
for xml_file in os.listdir(xml_path):
    if xml_file.endswith(".xml"):
        sum = sum + 1
        density_map = parse_xml(os.path.join(xml_path, xml_file), image_shape)
        with h5py.File(os.path.join(mat_path, xml_file.replace("R.xml", ".h5")), 'w') as hf:
            hf.create_dataset('density', data=density_map)

print("Successfully parsed " + str(sum) + " labels")
