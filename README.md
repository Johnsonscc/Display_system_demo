# 数字光刻成像模拟系统

## 系统介绍

数字光刻成像模拟系统是一个基于Hopkins成像理论和遗传算法优化的先进光刻仿真平台。
### 技术架构

```
gradio_app/
├── components/               # 可复用组件
│   ├── performance_monitor.py # 性能监控
│   └── state_manager.py      # 状态管理
├── config/
│   ├── theme_config.py       # 主题配置
│   └── lithography_config.py # 光刻参数配置
├── layouts/                  # 界面布局
│   ├── header.py             # 页头
│   ├── input_panel.py        # 输入面板
│   ├── output_panel.py       # 输出面板
│   └── footer.py             # 页脚
├── assets/                   # 静态资源
│   └── styles.css            # 页面样式
├── app.py                    # 主程序
core/                     # 核心业务逻辑
├── lithography_simulation.py  # 光刻仿真核心
├── genetic_algorithm.py       # 遗传算法优化
utils/                    # 工具函数
└── image_processing.py
```

## 安装指南

### 系统要求

- Python 3.8+
- Web浏览器（Chrome、Firefox、Safari等）

### 安装步骤

1. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

2. **运行系统**
   ```bash
   cd gradio_app
   python app.py
   ```

3. **访问系统**
   系统启动后，在浏览器中打开 `http://127.0.0.1:7860`


## 参数说明

### 默认参数值

| 参数    | name | 默认值    | 说明       |
|-------|------|--------|----------|
| 波长    |   wavelength   | 405 nm | 紫外光波长 |
| 距离  |    distance  | 803000000 nm | 光刻距离   |
| 像素尺寸  |   pixel_size   | 7560 nm   | DMD微镜尺寸 |
| 图像尺寸 |    image_size  | 30 pixels | 仿真图像尺寸 |
| 折射率   |   refractive_index   | 1.5  | 光学系统折射率 |
| 部分相干因子 |   sigma   | 0.5  | 光源相干性  |
| 数值孔径 |    numerical_aperture  | 0.5  | 光学系统数值孔径 |
| 种群大小 |    population_size  | 50   | 遗传算法种群规模 |
| 迭代次数 |   generations   | 20   | 遗传算法迭代次数 |
| 交叉概率 |    crossover_rate  | 0.4  | 遗传算法交叉概率 |
| 变异概率 |  mutation_rate    | 0.4  | 遗传算法变异概率 |


## 版本信息

- **当前版本**：1.0
- **更新日期**：2025年10月
- **开发团队**：课题组


---

*注意：本系统为研究用途，实际光刻工艺参数请参考设备制造商的技术规范。*