import sys
import os
import tempfile
from pathlib import Path
import gradio as gr
import numpy as np
import time
from PIL import Image
import plotly.graph_objects as go  # 确保导入plotly
import pandas as pd

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gradio_app.layouts.header import create_header
from gradio_app.layouts.input_panel import create_input_panel
from gradio_app.layouts.output_panel import create_output_panel
from gradio_app.layouts.footer import create_footer
from gradio_app.components.state_manager import StateManager
from gradio_app.config.theme_config import load_theme
from gradio_app.config.lithography_config import DEFAULT_PARAMETERS

from core.lithography_simulation import LithographySimulator
from core.genetic_algorithm import MaskOptimizer
from utils.image_processing import load_and_preprocess_image


class LithographyApp:
    def __init__(self):
        self.state_manager = StateManager()
        self.simulator = None
        self.current_results = {}

    def initialize_simulation(self, parameters):
        """初始化光刻仿真器"""
        self.simulator = LithographySimulator(parameters)
        return "仿真系统初始化完成"

    def run_simulation(self, mask_image, target_image, wavelength, distance, pixel_size,
                       image_size, refractive_index, sigma, numerical_aperture,
                       population_size, generations, crossover_rate, mutation_rate,
                       progress=gr.Progress()):
        """执行光刻仿真和优化"""
        try:
            # 构建参数字典
            parameters = {
                "wavelength": float(wavelength),
                "distance": float(distance),
                "pixel_size": float(pixel_size),
                "image_size": int(image_size),
                "refractive_index": float(refractive_index),
                "sigma": float(sigma),
                "numerical_aperture": float(numerical_aperture),
                "population_size": int(population_size),
                "generations": int(generations),
                "crossover_rate": float(crossover_rate),
                "mutation_rate": float(mutation_rate)
            }

            # 加载和预处理图像
            mask_array = load_and_preprocess_image(mask_image, parameters["image_size"])
            target_array = load_and_preprocess_image(target_image, parameters["image_size"])

            # 初始化仿真器
            if self.simulator is None:
                self.initialize_simulation(parameters)
            else:
                self.simulator.params = parameters

            progress(0.1, desc="正在执行初始仿真...")

            # 初始掩膜仿真
            initial_simulation = self.simulator.simulate(mask_array)
            initial_binary = self.simulator.binarize_image(initial_simulation)

            # 计算初始PE
            initial_pe = np.sum(np.abs(initial_binary.astype(np.float32) - target_array.astype(np.float32)))

            progress(0.3, desc="正在优化掩膜...")

            # 使用遗传算法优化掩膜
            optimizer = MaskOptimizer(self.simulator, target_array)
            best_mask, log = optimizer.optimize(mask_array)  # 现在返回log而不是stats

            progress(0.8, desc="正在执行优化后仿真...")

            # 优化后仿真
            optimized_simulation = self.simulator.simulate(best_mask)
            optimized_binary = self.simulator.binarize_image(optimized_simulation)
            optimized_pe = np.sum(np.abs(optimized_binary.astype(np.float32) - target_array.astype(np.float32)))

            # 保存结果 - 包含所有六个图像和优化日志
            self.current_results = {
                "original": target_array,  # 原始图像
                "initial": {
                    "mask": mask_array,
                    "simulation": initial_simulation,
                    "binary": initial_binary,
                    "pe": initial_pe
                },
                "optimized": {
                    "mask": best_mask,
                    "simulation": optimized_simulation,
                    "binary": optimized_binary,
                    "pe": optimized_pe
                },
                "target": target_array,
                "log": log  # 保存优化日志而不是stats
            }

            # 更新状态管理器
            self.state_manager.update_results(self.current_results)

            progress(1.0, desc="完成！")

            return self._generate_outputs()

        except Exception as e:
            error_msg = f"仿真过程中出错: {str(e)}"
            print(error_msg)
            # 返回空结果
            return None, None, None, None, None, None, gr.DataFrame(), None

    def _generate_outputs(self):
        """生成输出结果"""
        if not self.current_results:
            # 返回默认的空值 - 使用更小的图像尺寸
            empty_image = np.ones((200, 200)) * 255
            empty_pil = Image.fromarray(empty_image.astype(np.uint8))
            empty_df = pd.DataFrame(columns=["指标", "初始值", "优化值", "改善率"])

            # 创建空的进化图
            fig = go.Figure()
            fig.add_annotation(
                text="暂无数据",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                title="优化过程收敛曲线",
                xaxis_title="迭代次数",
                yaxis_title="适应度值",
                showlegend=True,
                margin=dict(t=40, b=20, l=20, r=20),
                height=400
            )

            return empty_pil, empty_pil, empty_pil, empty_pil, empty_pil, empty_pil, empty_df, fig

        results = self.current_results

        try:
            # 安全地转换图像数据
            def safe_image_convert(data):
                # 处理NaN和无穷大值
                data = np.nan_to_num(data, nan=0.0, posinf=1.0, neginf=0.0)
                # 确保数据在合理范围内
                data = np.clip(data, 0, 1)
                # 转换为0-255范围
                return (data * 255).astype(np.uint8)

            # 获取图像尺寸参数
            image_size = self.simulator.params.get("image_size", 30)
            # 使用更小的显示尺寸以适应三列布局
            display_size = max(200, image_size * 8)

            # 转换为PIL图像并调整显示尺寸
            def prepare_display_image(data):
                img_array = safe_image_convert(data)
                img = Image.fromarray(img_array)
                # 调整到合适的显示尺寸，保持原始比例
                if image_size < 100:  # 如果原始图像太小，放大显示
                    new_size = (display_size, display_size)
                    img = img.resize(new_size, Image.Resampling.NEAREST)
                return img

            # 生成所有六个图像
            original_img = prepare_display_image(results["original"])
            initial_exposure_img = prepare_display_image(results["initial"]["simulation"])
            initial_binary_img = prepare_display_image(results["initial"]["binary"])
            optimized_mask_img = prepare_display_image(results["optimized"]["mask"])
            optimized_exposure_img = prepare_display_image(results["optimized"]["simulation"])
            optimized_binary_img = prepare_display_image(results["optimized"]["binary"])

            # 生成统计信息
            stats_df = self.state_manager.generate_stats()
            evolution_plot = self.state_manager.generate_evolution_plot()

            return (original_img, initial_exposure_img, initial_binary_img,
                    optimized_mask_img, optimized_exposure_img, optimized_binary_img,
                    stats_df, evolution_plot)
        except Exception as e:
            print(f"生成输出时出错: {e}")
            # 返回错误状态的默认值
            error_image = np.ones((200, 200)) * 128
            error_pil = Image.fromarray(error_image.astype(np.uint8))
            error_df = pd.DataFrame([["错误", str(e), "N/A", "N/A"]],
                                    columns=["指标", "初始值", "优化值", "改善率"])

            fig = go.Figure()
            fig.add_annotation(
                text=f"错误: {str(e)}",
                xref="paper", yref="paper",
                x=0.5, y=0.5, xanchor='center', yanchor='middle',
                showarrow=False,
                font=dict(size=16)
            )
            fig.update_layout(
                title="优化过程收敛曲线",
                xaxis_title="迭代次数",
                yaxis_title="适应度值",
                showlegend=True,
                margin=dict(t=40, b=20, l=20, r=20),
                height=400
            )

            return error_pil, error_pil, error_pil, error_pil, error_pil, error_pil, error_df, fig


def run_app():
    app = LithographyApp()

    with gr.Blocks(
            title="数字光刻成像模拟系统",
            theme=load_theme(),
            css="assets/styles.css",
            # 添加全屏布局属性
            fill_width=True,
            fill_height=True
    ) as demo:
        create_header()

        # 使用全宽布局容器
        with gr.Row(elem_classes=["main-content"]):
            # 左侧输入面板
            with gr.Column(scale=3, min_width=300):
                input_components = create_input_panel(DEFAULT_PARAMETERS)

            # 右侧输出面板
            with gr.Column(scale=9, min_width=600):
                output_components = create_output_panel(app.state_manager)

        create_footer()

        # 绑定仿真按钮事件
        input_components["simulate_button"].click(
            fn=app.run_simulation,
            inputs=[
                input_components["mask_input"],
                input_components["target_input"],
                input_components["wavelength"],
                input_components["distance"],
                input_components["pixel_size"],
                input_components["image_size"],
                input_components["refractive_index"],
                input_components["sigma"],
                input_components["numerical_aperture"],
                input_components["population_size"],
                input_components["generations"],
                input_components["crossover_rate"],
                input_components["mutation_rate"]
            ],
            outputs=[
                output_components["original_image"],
                output_components["initial_exposure"],
                output_components["initial_binary"],
                output_components["optimized_mask"],
                output_components["optimized_exposure"],
                output_components["optimized_binary"],
                output_components["stats_display"],
                output_components["evolution_plot"]
            ]
        )

        # 初始化仿真系统
        demo.load(
            fn=lambda: app.initialize_simulation(DEFAULT_PARAMETERS),
            outputs=[output_components["system_status"]]
        )

    # 启动时设置全屏参数
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=True,
        inbrowser=False,
        show_error=True,
        max_threads=50,
        prevent_thread_lock=False
    )

if __name__ == "__main__":
    run_app()