import torch
import os
import argparse
from datasets.crowd import Crowd
from nets.RGBTCCNet import ThermalRGBNet
from utils.raw_evaluation import eval_game
import numpy as np
import math

parser = argparse.ArgumentParser(description='Test')
parser.add_argument('--data-dir', default='F:/DataSets/RGBT_CC',
                        help='training data directory')
parser.add_argument('--model', default='./model/best_model.pth'
                    , help='model name')
parser.add_argument('--img_size', default=224, type=int, help='network input size')
parser.add_argument('--device', default='0', help='gpu device')
args = parser.parse_args()

if __name__ == '__main__':
    test_path = os.path.join(args.data_dir, "new_test_224")
    gt_exist = os.path.exists(test_path)
    datasets = Crowd(test_path, method='test')
    dataloader = torch.utils.data.DataLoader(datasets, 1, shuffle=False,
                                             num_workers=0, pin_memory=False)

    os.environ['CUDA_VISIBLE_DEVICES'] = args.device  # set vis gpu
    device = torch.device('cuda')

    model = ThermalRGBNet()
    model.to(device)
    model_path = args.model
    checkpoint = torch.load(model_path, device)
    model.load_state_dict(checkpoint, strict=False)
    model.eval()

    print('testing...')
    # Iterate over data.
    game = [0, 0, 0, 0]
    mse = [0, 0, 0, 0]
    total_relative_error = 0
    epoch_res = []
    print(len(dataloader))
    for idx, (inputs, target, name) in enumerate(dataloader):
        print(idx)
        
        if type(inputs) == list:
            inputs[0] = inputs[0].to(device)
            inputs[1] = inputs[1].to(device)
        else:
            inputs = inputs.to(device)
        if len(inputs[0].shape) == 5:
            inputs[0] = inputs[0].squeeze(0)
            inputs[1] = inputs[1].squeeze(0)
        if len(inputs[0].shape) == 3:
            inputs[0] = inputs[0].unsqueeze(0)
            inputs[1] = inputs[1].unsqueeze(0)
        with torch.set_grad_enabled(False):
            count, outputs, _ = model(inputs)  # outputs batch_size为4
            outputs1 = torch.cat((outputs[0], outputs[1]), dim=1)
            outputs2 = torch.cat((outputs[2], outputs[3]), dim=1)
            outputs3 = torch.cat((outputs[4], outputs[5]), dim=1)
            outputs = torch.cat((outputs1, outputs2, outputs3), dim=2)
            
            ans = torch.sum(outputs)
            formatted_ans = "{:.2f}".format(ans.item())
            name = int(name[0])
            epoch_res.append([name, f"{name},{formatted_ans}\n"])

    epoch_res.sort()
    with open('./ans.txt', 'w') as file:
        for result in epoch_res:
            file.writelines(result[1])