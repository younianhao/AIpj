def write_result(file_path, data):
    """Writes the result to a file."""
    with open(file_path, 'w') as file:
        for line_number, value in sorted(data.items()):
            file.write(f"{line_number},{value:.2f}\n")


def process_files(file_paths, output_file):
    data = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            for line in file:
                values = line.strip().split(',')
                data.append([float(value) for value in values[:-1]])
    
    updated_results = []
    for i in range(len(data[0])):
        column_values = [row[i] for row in data]
        column_values.sort()
        updated_results.append(sum(column_values[1:-1]) / 3)
    
    result = {i+1: value for i, value in enumerate(updated_results)}
    write_result(output_file, result)


file_paths = ['1.txt', '2.txt', '3.txt', '4.txt', '5.txt']
output_file = 'output.txt'

process_files(file_paths, output_file)