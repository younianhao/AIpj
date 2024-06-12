def write_result(file_path, data):
    """Writes the result to a file."""
    with open(file_path, 'w') as file:
        for line_number, value in sorted(data.items()):
            file.write(f"{line_number},{value:.2f}\n")


def optimize_decision(ans_files, mae_values, output_file):
    ans_data = []
    for ans_file in ans_files:
        with open(ans_file, 'r') as file:
            ans_values = file.readline().strip().split('——ANS：')[1].split(', ')
            ans_data.append([float(value) for value in ans_values])
    
    num_images = len(ans_data[0])
    final_result = []
    for i in range(num_images):
        image_votes = {}
        for ans_values in ans_data:
            ans_value = ans_values[i]
            interval = int(ans_value)
            if interval not in image_votes:
                image_votes[interval] = 0
            image_votes[interval] += 1
        
        max_votes = max(image_votes.values())
        max_intervals = [interval for interval, votes in image_votes.items() if votes == max_votes]
        min_mae = float('inf')
        selected_ans = None
        for ans_values in ans_data:
            ans_value = ans_values[i]
            interval = int(ans_value)
            if interval in max_intervals:
                mae = abs(ans_value - interval)
                if mae < min_mae:
                    min_mae = mae
                    selected_ans = ans_value
                elif mae == min_mae and mae_values[interval-1] < mae_values[int(selected_ans)-1]:
                    selected_ans = ans_value
        final_result.append(selected_ans)
    result = {i+1: value for i, value in enumerate(final_result)}
    write_result(output_file, result)
    


ans_files = ['ans1.txt', 'ans2.txt', 'ans3.txt', 'ans4.txt', 'ans5.txt']
mae_values = [12.71, 12.74, 12.80, 12.89, 12.93]
output_file = 'output.txt'

optimize_decision(ans_files,mae_values,output_file)