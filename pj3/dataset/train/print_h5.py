import h5py

def print_h5_file_contents(file_path):
    with h5py.File(file_path, 'r') as f:
        # 打印H5文件中的内容
        print("H5文件内容：")
        print("------------------------")
        for key in f.keys():
            print(f"Dataset: {key}")
            dataset = f[key]
            print(f"Shape: {dataset.shape}")
            print(f"Data Type: {dataset.dtype}")
            print("Data:")
            print(dataset[()])
            print("------------------------")

# 调用函数并传入标准H5文件路径
print_h5_file_contents('hdf5s/1.h5')
