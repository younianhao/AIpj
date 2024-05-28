def read_file(file_path):
    """Reads a file and returns a dictionary with line number as key and value as float."""
    data = {}
    with open(file_path, 'r') as file:
        for line in file:
            line_number, value = line.strip().split(',')
            data[int(line_number)] = float(value)
    return data


def write_result(file_path, data):
    """Writes the result to a file."""
    with open(file_path, 'w') as file:
        for line_number, value in sorted(data.items()):
            file.write(f"{line_number},{value:.2f}\n")


def merge_files(file1, file2, weight1, weight2, output_file):
    """Merges two files with given weights and writes the result to the output file."""
    data1 = read_file(file1)
    data2 = read_file(file2)

    result = {}
    for line_number in data1:
        if line_number in data2:
            result[line_number] = data1[line_number] * weight1 + data2[line_number] * weight2
        else:
            result[line_number] = data1[line_number] * weight1

    for line_number in data2:
        if line_number not in result:
            result[line_number] = data2[line_number] * weight2

    write_result(output_file, result)


# Define file paths and weights
file1 = 'ans_5.24_16.70.txt'
file2 = 'ans_5.25_12.70.txt'
weight1 = 0.15
weight2 = 0.85
output_file = '2.txt'

# Merge files and write the result
merge_files(file1, file2, weight1, weight2, output_file)