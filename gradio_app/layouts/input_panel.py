import gradio as gr


def create_input_panel(default_parameters):
    with gr.Tab("⚙️ 仿真参数配置", elem_classes=["parameter-tab"]):
        # 图像上传区域 - 使用 Group 替代 Box
        with gr.Group():
            gr.Markdown("### 📁 图像输入")
            with gr.Row():
                with gr.Column():
                    mask_input = gr.Image(
                        label="初始掩膜图像",
                        type="filepath",
                        height=180,
                        elem_classes=["input-image"]
                    )
                with gr.Column():
                    target_input = gr.Image(
                        label="目标图像",
                        type="filepath",
                        height=180,
                        elem_classes=["input-image"]
                    )

        gr.HTML("<div style='margin: 20px 0;'></div>")  # 添加间距

        # 光学参数
        with gr.Accordion("🔬 光学参数配置", open=True, elem_classes=["accordion"]):
            with gr.Row():
                with gr.Column():
                    wavelength = gr.Number(
                        value=default_parameters["wavelength"],
                        label="波长 (nm)",
                        precision=0,
                        elem_classes=["parameter-input"]
                    )
                    distance = gr.Number(
                        value=default_parameters["distance"],
                        label="传播距离 (nm)",
                        precision=0,
                        elem_classes=["parameter-input"]
                    )

                with gr.Column():
                    pixel_size = gr.Number(
                        value=default_parameters["pixel_size"],
                        label="像素尺寸 (nm)",
                        precision=0,
                        elem_classes=["parameter-input"]
                    )
                    image_size = gr.Number(
                        value=default_parameters["image_size"],
                        label="图像尺寸 (像素)",
                        precision=0,
                        elem_classes=["parameter-input"]
                    )

        gr.HTML("<div style='margin: 15px 0;'></div>")  # 添加间距

        # 系统参数
        with gr.Accordion("⚡ 系统参数配置", open=False, elem_classes=["accordion"]):
            with gr.Row():
                refractive_index = gr.Number(
                    value=default_parameters["refractive_index"],
                    label="折射率",
                    precision=2,
                    elem_classes=["parameter-input"]
                )
                sigma = gr.Number(
                    value=default_parameters["sigma"],
                    label="部分相干因子",
                    precision=2,
                    elem_classes=["parameter-input"]
                )
                numerical_aperture = gr.Number(
                    value=default_parameters["numerical_aperture"],
                    label="数值孔径",
                    precision=2,
                    elem_classes=["parameter-input"]
                )

        gr.HTML("<div style='margin: 15px 0;'></div>")  # 添加间距

        # 优化参数
        with gr.Accordion("🧬 遗传算法参数", open=False, elem_classes=["accordion"]):
            with gr.Row():
                with gr.Column():
                    population_size = gr.Number(
                        value=default_parameters["population_size"],
                        label="种群大小",
                        precision=0,
                        elem_classes=["parameter-input"]
                    )
                    generations = gr.Number(
                        value=default_parameters["generations"],
                        label="迭代次数",
                        precision=0,
                        elem_classes=["parameter-input"]
                    )

                with gr.Column():
                    crossover_rate = gr.Slider(
                        0, 1,
                        value=default_parameters["crossover_rate"],
                        label="交叉概率",
                        elem_classes=["parameter-slider"]
                    )
                    mutation_rate = gr.Slider(
                        0, 1,
                        value=default_parameters["mutation_rate"],
                        label="变异概率",
                        elem_classes=["parameter-slider"]
                    )

        gr.HTML("<div style='margin: 20px 0;'></div>")  # 添加间距

        # 操作按钮
        with gr.Row():
            simulate_button = gr.Button(
                "🚀 开始仿真优化",
                variant="primary",
                size="lg",
                elem_classes=["analyze-btn", "primary-button"]
            )

    # 输入面板样式
    gr.HTML("""
    <style>
    /* 组容器样式 */
    .gr-group {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
    }

    .parameter-input {
        background: white !important;
        border: 2px solid #e1e5e9 !important;
        border-radius: 8px !important;
        padding: 10px !important;
    }

    .parameter-slider {
        margin: 15px 0 !important;
    }

    .primary-button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
        font-size: 16px !important;
        padding: 15px 30px !important;
        transition: all 0.3s ease !important;
    }

    .primary-button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4) !important;
    }

    /* 图像输入样式 */
    .input-image {
        border: 2px dashed #4a90e2 !important;
        border-radius: 10px !important;
        padding: 15px !important;
        background: #f8f9fa !important;
        transition: all 0.3s ease !important;
    }

    .input-image:hover {
        border-color: #667eea !important;
        background: #e3f2fd !important;
    }
    </style>
    """)

    return {
        "mask_input": mask_input,
        "target_input": target_input,
        "wavelength": wavelength,
        "distance": distance,
        "pixel_size": pixel_size,
        "image_size": image_size,
        "refractive_index": refractive_index,
        "sigma": sigma,
        "numerical_aperture": numerical_aperture,
        "population_size": population_size,
        "generations": generations,
        "crossover_rate": crossover_rate,
        "mutation_rate": mutation_rate,
        "simulate_button": simulate_button
    }