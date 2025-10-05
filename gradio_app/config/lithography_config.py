# 光刻系统默认参数配置
DEFAULT_PARAMETERS = {
    "wavelength": 405,           # 波长 (nm)
    "distance": 803000000,       # 距离 (nm)
    "pixel_size": 7560,          # 像素尺寸 (nm)
    "image_size": 30,            # 图像尺寸 (pixels)
    "refractive_index": 1.5,     # 折射率
    "sigma": 0.5,                # 部分相干因子
    "numerical_aperture": 0.5,   # 数值孔径
    "population_size": 50,       # 遗传算法种群大小
    "generations": 20,           # 遗传算法迭代次数
    "crossover_rate": 0.4,       # 交叉概率
    "mutation_rate": 0.4         # 变异概率
}