from PIL import Image, ImageDraw,ImageEnhance,ImageStat,ImageFilter
import os
import xml.etree.ElementTree as ET
import random
 

# 修改后的函数
def clear_to_image(input_rgb_file, output_rgb_file):
    # 处理图像文件
    img = Image.open(input_rgb_file)
    stat = ImageStat.Stat(img)
    luminance = stat.mean[0]  # 获取图像的亮度值
    print(luminance)
    if luminance < 80:
        brightness_factor = 80 / luminance  # 根据亮度值计算增加的亮度倍数
        img = ImageEnhance.Brightness(img).enhance(brightness_factor)

    contrast = stat.stddev[0]  # 获取图像的对比度值
    print(contrast)
    if contrast < 50:
        contrast_factor = 50 / contrast
        img = ImageEnhance.Contrast(img).enhance(contrast_factor)  # 根据对比度值增加对比度
    
    sharpness_factor = 2.0
    img = ImageEnhance.Sharpness(img).enhance(sharpness_factor)

    img.save(output_rgb_file)

# 文件夹路径
rgb_path = "./dataset/train/rgb/"
tir_path = "./dataset/train/tir/"

test_rgb_path = "./dataset/test/rgb/"
tests_tir_path = "./dataset/test/tir/"
# 获取文件列表
for index in range(1, 1807):
    input_rgb_file = os.path.join(rgb_path, str(index) + ".jpg")
    output_rgb_file = os.path.join(rgb_path, str(index) + ".jpg")
    clear_to_image(input_rgb_file, output_rgb_file) 
    input_tir_file = os.path.join(tir_path, str(index) + "R.jpg")
    output_tir_file = os.path.join(tir_path, str(index) + "R.jpg")
    clear_to_image(input_tir_file, output_tir_file) 

for index in range(1, 1000):
    input_rgb_file = os.path.join(test_rgb_path, str(index) + ".jpg")
    output_rgb_file = os.path.join(test_rgb_path, str(index) + ".jpg")
    clear_to_image(input_rgb_file, output_rgb_file) 
    input_tir_file = os.path.join(tests_tir_path, str(index) + "R.jpg")
    output_tir_file = os.path.join(tests_tir_path, str(index) + "R.jpg")
    clear_to_image(input_tir_file, output_tir_file) 
print("successfully create all samples with clear")