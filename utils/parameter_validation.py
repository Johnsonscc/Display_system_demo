import numpy as np


def validate_parameters(parameters):
    """验证和清理仿真参数"""
    validated = parameters.copy()

    # 确保所有参数都是有效的数值
    for key, value in parameters.items():
        if not np.isfinite(value):
            print(f"警告: 参数 {key} 的值 {value} 无效，使用默认值")
            # 设置合理的默认值
            defaults = {
                "wavelength": 405,
                "distance": 803000000,
                "pixel_size": 7560,
                "image_size": 30,
                "refractive_index": 1.5,
                "sigma": 0.5,
                "numerical_aperture": 0.5,
                "population_size": 50,
                "generations": 20,
                "crossover_rate": 0.4,
                "mutation_rate": 0.4
            }
            validated[key] = defaults.get(key, 1.0)

    # 确保图像尺寸是整数
    validated["image_size"] = int(validated["image_size"])
    validated["population_size"] = int(validated["population_size"])
    validated["generations"] = int(validated["generations"])

    return validated