import numpy as np
from PIL import Image
import cv2


def load_and_preprocess_image(image_path, target_size=30):
    """加载并预处理图像为仿真可用格式"""
    if isinstance(image_path, str):
        image = Image.open(image_path).convert('L')  # 转为灰度
    else:
        image = Image.fromarray(image_path).convert('L')

    # 调整尺寸 - 确保是正方形
    image = image.resize((target_size, target_size), Image.Resampling.LANCZOS)

    # 转为numpy数组并归一化
    image_array = np.array(image).astype(np.float32) / 255.0

    # 确保数据在有效范围内
    image_array = np.clip(image_array, 0, 1)

    return image_array


def ensure_square_image(image_array, target_size=100):
    """确保图像为正方形，用于显示"""
    if len(image_array.shape) == 2:  # 灰度图
        h, w = image_array.shape
    else:  # 彩色图
        h, w, _ = image_array.shape

    # 计算填充量
    pad_h = max(0, target_size - h)
    pad_w = max(0, target_size - w)

    # 计算每边的填充量
    pad_top = pad_h // 2
    pad_bottom = pad_h - pad_top
    pad_left = pad_w // 2
    pad_right = pad_w - pad_left

    # 应用填充
    if len(image_array.shape) == 2:
        padded = np.pad(image_array,
                        ((pad_top, pad_bottom), (pad_left, pad_right)),
                        mode='constant', constant_values=0)
    else:
        padded = np.pad(image_array,
                        ((pad_top, pad_bottom), (pad_left, pad_right), (0, 0)),
                        mode='constant', constant_values=0)

    return padded