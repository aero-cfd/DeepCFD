import torch
import torch.nn as nn
import numpy as np
from matplotlib import pyplot as plt

def shuffle_tensors(*tensors):
    assert len(tensors) > 0
    output = []
    count = len(tensors[0])
    indices = torch.randperm(count)
    for tensor in tensors:
        assert len(tensor) == count
        output.append(tensor[indices])
    return output


def split_tensors(*tensors, ratio):
    assert len(tensors) > 0
    split1, split2 = [], []
    count = len(tensors[0])
    for tensor in tensors:
        assert len(tensor) == count
        split1.append(tensor[:int(len(tensor) * ratio)])
        split2.append(tensor[int(len(tensor) * ratio):])
    if len(tensors) == 1:
        split1, split2 = split1[0], split2[0]
    return split1, split2

def initialize(model, gain=1, std=0.02):
    for module in model.modules():
        if type(module) in [nn.Linear, nn.Conv1d, nn.Conv2d, nn.Conv3d]:
            nn.init.xavier_normal_(module.weight, gain)
            if module.bias is not None:
                nn.init.normal_(module.bias, 0, std)


def visualize(sample_y, out_y, s=0):
    error = np.abs(sample_y - out_y)

    minu = np.min(sample_y[s, 0, :, :])
    maxu = np.max(sample_y[s, 0, :, :])
    
    minv = np.min(sample_y[s, 1, :, :])
    maxv = np.max(sample_y[s, 1, :, :])
    
    minp = np.min(sample_y[s, 2, :, :])
    maxp = np.max(sample_y[s, 2, :, :])
    
    mineu = np.min(error[s, 0, :, :])
    maxeu = np.max(error[s, 0, :, :])
    
    minev = np.min(error[s, 1, :, :])
    maxev = np.max(error[s, 1, :, :])
    
    minep = np.min(error[s, 2, :, :])
    maxep = np.max(error[s, 2, :, :])
    
    f = 0.8
    
    plt.figure()
    fig = plt.gcf()
    fig.set_size_inches(15, 10)
    plt.subplot(3, 3, 1)
    plt.title('CFD', fontsize=18)
    plt.imshow(np.transpose(sample_y[s, 0, :, :]), cmap='jet', vmin = minu, vmax = maxu)
    plt.colorbar(orientation='horizontal')
    plt.ylabel('Ux', fontsize=18)
    plt.subplot(3, 3, 2)
    plt.title('CNN', fontsize=18)
    plt.imshow(np.transpose(out_y[s, 0, :, :]), cmap='jet', vmin = minu, vmax = maxu)
    plt.colorbar(orientation='horizontal')
    plt.subplot(3, 3, 3)
    plt.title('Error', fontsize=18)
    plt.imshow(np.transpose(error[s, 0, :, :]), cmap='jet', vmin = mineu, vmax = f*maxeu)
    plt.colorbar(orientation='horizontal')

    plt.subplot(3, 3, 4)
    plt.imshow(np.transpose(sample_y[s, 1, :, :]), cmap='jet', vmin = minv, vmax = maxv)
    plt.colorbar(orientation='horizontal')
    plt.ylabel('Uy', fontsize=18)
    plt.subplot(3, 3, 5)
    plt.imshow(np.transpose(out_y[s, 1, :, :]), cmap='jet', vmin = minv, vmax = maxv)
    plt.colorbar(orientation='horizontal')
    plt.subplot(3, 3, 6)
    plt.imshow(np.transpose(error[s, 1, :, :]), cmap='jet', vmin = minev, vmax = f*maxev)
    plt.colorbar(orientation='horizontal')

    plt.subplot(3, 3, 7)
    plt.imshow(np.transpose(sample_y[s, 2, :, :]), cmap='jet', vmin = minp, vmax = maxp)
    plt.colorbar(orientation='horizontal')
    plt.ylabel('p', fontsize=18)
    plt.subplot(3, 3, 8)
    plt.imshow(np.transpose(out_y[s, 2, :, :]), cmap='jet', vmin = minp, vmax = maxp)
    plt.colorbar(orientation='horizontal')
    plt.subplot(3, 3, 9)
    plt.imshow(np.transpose(error[s, 2, :, :]), cmap='jet', vmin = minep, vmax = f*maxep)
    plt.colorbar(orientation='horizontal')
    plt.tight_layout()