import os
import torch
import torch.nn as nn
from torch.autograd import Variable
from torchvision import transforms
import time
import random
import numpy as np
from torch.utils.data import Dataset, DataLoader, random_split
from PIL import Image
import h5py
import cv2
import shutil
from model import CSRNet


def save_checkpoint(state, is_best, task_id, filename='checkpoint.pth.tar', save_dir='./model/'):  # 添加保存目录参数
    checkpoint_path = os.path.join(save_dir, task_id + filename)
    torch.save(state, checkpoint_path)
    if is_best:
        best_model_path = os.path.join(
            save_dir, task_id + 'model_best.pth.tar')
        shutil.copyfile(checkpoint_path, best_model_path)


# def load_data(img_path, gt_path, train=True):
#     img = Image.open(img_path).convert('RGB')
#     gt_file = h5py.File(gt_path)
#     target = np.asarray(gt_file['density'])
#     target = cv2.resize(
#         target, (target.shape[1]//8, target.shape[0]//8), interpolation=cv2.INTER_CUBIC)*64
#     return img, target

def load_data(rgb_path, ir_path, gt_path, train=True):
    rgb_img = Image.open(rgb_path).convert('RGB')
    # 假设红外线图片也是三通道，如果是单通道则改为 .convert('L')
    ir_img = Image.open(ir_path).convert('RGB')
    gt_file = h5py.File(gt_path)
    target = np.asarray(gt_file['density'])
    target = cv2.resize(target, (target.shape[1] // 8, target.shape[0] // 8), interpolation=cv2.INTER_CUBIC) * 64
    return rgb_img, ir_img, target


class ImgDataset(Dataset):
    def __init__(self, img_dir, ir_dir, gt_dir, shape=None, shuffle=True, transform=None, train=False, batch_size=1,
                 num_workers=4):
        self.img_dir = img_dir
        self.gt_dir = gt_dir
        self.ir_dir = ir_dir
        self.transform = transform
        self.train = train
        self.shape = shape
        self.batch_size = batch_size
        self.num_workers = num_workers

        self.img_paths = [os.path.join(img_dir, filename) for filename in os.listdir(
            img_dir) if filename.endswith('.jpg')]

        if shuffle:
            random.shuffle(self.img_paths)

        self.nSamples = len(self.img_paths)

    def __len__(self):
        return self.nSamples

    def __getitem__(self, index):
        assert index <= len(self), 'index range error'
        rgb_path = self.img_paths[index]
        img_name = os.path.basename(rgb_path)

        ir_name = os.path.splitext(img_name)[0] + 'R.jpg'
        ir_path = os.path.join(self.ir_dir, ir_name)

        gt_path = os.path.join(
            self.gt_dir, os.path.splitext(img_name)[0] + '.h5')

        rgb_img, ir_img, target = load_data(rgb_path, ir_path, gt_path, self.train)

        if self.transform is not None:
            rgb_img = self.transform(rgb_img)
            ir_img = self.transform(ir_img)

        return rgb_img, ir_img, target


lr = 1e-7
original_lr = lr
batch_size = 1
momentum = 0.95
decay = 5 * 1e-4
epochs = 50
steps = [-1, 1, 100, 150]
scales = [1, 1, 1, 1]
workers = 8
seed = time.time()
print_freq = 30
img_dir = "./dataset/train/rgb/"
gt_dir = "./dataset/train/hdf5s/"
ir_dir = "./dataset/train/tir"
pre = None
task = ""


def main():
    start_epoch = 0
    best_prec1 = 1e6

    torch.cuda.manual_seed(seed)

    model = CSRNet()

    model = model.cuda()

    criterion = nn.MSELoss(size_average=False).cuda()

    optimizer = torch.optim.SGD(model.parameters(), lr,
                                momentum=momentum,
                                weight_decay=decay)

    # 修改归一化参数以适应6通道数据
    transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[
                             0.229, 0.224, 0.225]),
    ])

    dataset = ImgDataset(
        img_dir,
        ir_dir,
        gt_dir, transform=transform, train=True)

    sample_size = min(len(dataset), 600)  # 例如，使用前600个样本进行调试
    dataset = torch.utils.data.Subset(dataset, range(sample_size))
    train_size = int(0.8 * len(dataset))
    val_size = len(dataset) - train_size
    # 将数据集分割为训练集和验证集
    train_dataset, val_dataset = random_split(dataset, [train_size, val_size])
    train_loader = DataLoader(
        train_dataset, batch_size=batch_size, shuffle=True, num_workers=workers)
    val_loader = DataLoader(
        val_dataset, batch_size=batch_size, shuffle=False, num_workers=workers)

    if pre:
        if os.path.isfile(pre):
            print("=> loading checkpoint '{}'".format(pre))
            checkpoint = torch.load(pre)
            start_epoch = checkpoint['epoch']
            best_prec1 = checkpoint['best_prec1']
            model.load_state_dict(checkpoint['state_dict'])
            optimizer.load_state_dict(checkpoint['optimizer'])
            print("=> loaded checkpoint '{}' (epoch {})"
                  .format(pre, checkpoint['epoch']))
        else:
            print("=> no checkpoint found at '{}'".format(pre))

    for epoch in range(start_epoch, epochs):
        adjust_learning_rate(optimizer, epoch)

        train(model, criterion, optimizer, epoch, train_loader)
        prec1 = validate(model, val_loader)

        is_best = prec1 < best_prec1
        best_prec1 = min(prec1, best_prec1)
        print(' * best MAE {mae:.3f} '
              .format(mae=best_prec1))
        save_checkpoint({
            'epoch': epoch + 1,
            'arch': pre,
            'state_dict': model.state_dict(),
            'best_prec1': best_prec1,
            'optimizer': optimizer.state_dict(),
        }, is_best, task)


def train(model, criterion, optimizer, epoch, train_loader):
    losses = AverageMeter()
    batch_time = AverageMeter()
    data_time = AverageMeter()

    print('epoch %d, processed %d samples, lr %.10f' %
          (epoch, epoch * len(train_loader.dataset), lr))

    # 训练模式
    model.train()
    end = time.time()

    # 遍历训练数据加载器
    for i, (rgb_img, ir_img, target) in enumerate(train_loader):
        data_time.update(time.time() - end)

        # 前向传播
        rgb_img = rgb_img.cuda()
        ir_img = ir_img.cuda()
        rgb_img = Variable(rgb_img)
        ir_img = Variable(ir_img)

        output = model(rgb_img, ir_img)
        # output = model(img)

        target = target.type(torch.FloatTensor).unsqueeze(1).cuda()
        target = Variable(target)
        loss = criterion(output, target)

        # 反向传播 & 参数更新
        # losses.update(loss.item(), img.size(0))
        losses.update(loss.item(), rgb_img.size(0))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        batch_time.update(time.time() - end)
        end = time.time()

        if i % print_freq == 0:
            print('Epoch: [{0}][{1}/{2}]\t'
                  'Time {batch_time.val:.3f} ({batch_time.avg:.3f})\t'
                  'Data {data_time.val:.3f} ({data_time.avg:.3f})\t'
                  'Loss {loss.val:.4f} ({loss.avg:.4f})\t'
            .format(
                epoch, i, len(train_loader), batch_time=batch_time,
                data_time=data_time, loss=losses))


# 模型在验证集(val_dataset)上的评估
def validate(model, val_loader):
    print('begin test')

    # 评估模式
    model.eval()
    mae = 0  # 平均绝对误差（MAE）越小越好

    for i, (rgb_img, ir_img, target) in enumerate(val_loader):
        rgb_img = rgb_img.cuda()
        ir_img = ir_img.cuda()
        rgb_img = Variable(rgb_img)
        ir_img = Variable(ir_img)
        output = model(rgb_img, ir_img)

        mae += abs(output.data.sum() -
                   target.sum().type(torch.FloatTensor).cuda())

    mae = mae / len(val_loader)
    print(' * MAE {mae:.3f} '
          .format(mae=mae))

    return mae


# 调整优化器学习率：每当当前轮次 epoch 大于等于 steps 中的某个值时，
# 学习率将乘以 scales 中对应位置的值，即进行学习率衰减。
def adjust_learning_rate(optimizer, epoch):
    """Sets the learning rate to the initial LR decayed by 10 every 30 epochs"""

    lr = original_lr

    for i in range(len(steps)):

        scale = scales[i] if i < len(scales) else 1

        if epoch >= steps[i]:
            lr = lr * scale
            if epoch == steps[i]:
                break
        else:
            break
    for param_group in optimizer.param_groups:
        param_group['lr'] = lr


# 计算和存储平均值和当前值
class AverageMeter(object):
    """Computes and stores the average and current value"""

    def __init__(self):
        self.reset()

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count


if __name__ == '__main__':
    main()
