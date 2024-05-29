import os

folder_path = 'labels'
for filename in os.listdir(folder_path):
    if filename.startswith('GT_IMG_') and filename.endswith('.xml'):
        new_filename = filename.replace('GT_IMG_', '').replace('.xml', 'R.xml')
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
