import numpy as np
from scipy.fft import fft2, ifft2, fftshift, ifftshift


class LithographySimulator:
    def __init__(self, parameters):
        self.params = parameters

    def transfer_function(self, fx, fy):
        lambda_ = self.params["wavelength"]
        z = self.params["distance"]
        n = self.params["refractive_index"]
        H = np.exp(-1j * np.pi * lambda_ * z * (fx ** 2 + fy ** 2) / n ** 2)
        return H

    def light_source_function(self, fx, fy):
        sigma = self.params["sigma"]
        NA = self.params["numerical_aperture"]
        lambda_ = self.params["wavelength"]

        condition = (fx ** 2 + fy ** 2) <= (sigma * NA / lambda_) ** 2
        J = np.where(condition, (lambda_ ** 2) / (np.pi * (sigma * NA) ** 2), 0)
        return J

    def impulse_response_function(self, fx, fy):
        NA = self.params["numerical_aperture"]
        lambda_ = self.params["wavelength"]

        condition = (fx ** 2 + fy ** 2) <= (NA / lambda_) ** 2
        P = np.where(condition, (lambda_ ** 2) / (np.pi * NA ** 2), 0)
        return P

    def compute_tcc(self, fx, fy):
        J = self.light_source_function(fx, fy)
        P = self.impulse_response_function(fx, fy)
        tcc = np.convolve(J * P, J * P, mode='same')
        return tcc

    def simulate(self, mask):
        Lx = Ly = self.params["image_size"]
        dx = dy = self.params["pixel_size"]

        # 计算空间频率坐标
        fx = np.linspace(-0.5 / dx, 0.5 / dx, Lx)
        fy = np.linspace(-0.5 / dy, 0.5 / dy, Ly)

        # 计算TCC
        tcc = self.compute_tcc(fx, fy)

        # 频域转换和滤波
        M_fft = fftshift(fft2(mask))
        filtered_fft = M_fft * tcc

        # 应用传递函数
        H = self.transfer_function(fx, fy)
        result_fft = filtered_fft * H

        # 逆变换回空间域
        result = ifft2(ifftshift(result_fft))

        # 获取幅度并清理数据
        result_abs = np.abs(result)

        # 清理数据：处理NaN和无穷大
        result_abs = np.nan_to_num(result_abs, nan=0.0, posinf=np.max(result_abs), neginf=0.0)

        # 归一化到0-1范围
        if np.max(result_abs) > 0:
            result_abs = result_abs / np.max(result_abs)

        return result_abs

    def binarize_image(self, image, threshold=None):
        """二值化图像"""
        if threshold is None:
            threshold = 0.5 * np.max(image)
        return (image > threshold).astype(np.uint8)