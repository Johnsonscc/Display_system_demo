import gradio as gr


def create_output_panel(state_manager):
    with gr.Tabs(elem_classes=["output-tabs"]):
        with gr.Tab("📊 仿真结果"):
            # 使用更紧凑的布局和调整比例
            with gr.Row(equal_height=True):
                # 第一行：三个图像
                with gr.Column(min_width=200, scale=1):
                    original_image = gr.Image(
                        label="原始图像",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image"]
                    )

                with gr.Column(min_width=200, scale=1):
                    initial_exposure = gr.Image(
                        label="原始掩膜曝光后图像",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image"]
                    )

                with gr.Column(min_width=200, scale=1):
                    initial_binary = gr.Image(
                        label="原始掩膜曝光后二值图像",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image"]
                    )

            # 第二行：三个图像
            with gr.Row(equal_height=True):
                with gr.Column(min_width=200, scale=1):
                    optimized_mask = gr.Image(
                        label="优化后的掩膜",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image"]
                    )

                with gr.Column(min_width=200, scale=1):
                    optimized_exposure = gr.Image(
                        label="优化掩膜曝光后图像",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image"]
                    )

                with gr.Column(min_width=200, scale=1):
                    optimized_binary = gr.Image(
                        label="优化掩膜曝光后二值图像",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image"]
                    )

            with gr.Row():
                system_status = gr.Textbox(
                    label="系统状态",
                    value="等待初始化...",
                    interactive=False
                )

        with gr.Tab("📈 性能分析"):
            with gr.Row():
                with gr.Column(scale=5):
                    stats_display = gr.DataFrame(
                        headers=["指标", "初始值", "优化值", "改善率"],
                        label="性能统计",
                        interactive=False
                    )

                with gr.Column(scale=5):
                    evolution_plot = gr.Plot(
                        label="优化过程收敛曲线"
                    )

        with gr.Tab("ℹ️ 系统信息"):
            gr.Markdown("""
            ### 数字光刻成像模拟系统

            **系统特性：**
            - 基于Hopkins成像理论
            - 集成遗传算法优化
            - 实时参数调整
            - 性能可视化分析

            **使用说明：**
            1. 上传初始掩膜和目标图像
            2. 调整光学和优化参数
            3. 点击开始仿真优化
            4. 查看优化结果和性能分析
            """)

    # 添加CSS样式确保图像正确显示
    gr.HTML("""
    <style>
    /* 图像样式 */
    .output-image {
        width: 100% !important;
        max-width: 100% !important;
    }
    .output-image img {
        width: 100% !important;
        height: auto !important;
        max-height: 250px !important;
        object-fit: contain !important;
    }

    /* 列布局优化 */
    .gr-row {
        display: flex !important;
        flex-wrap: nowrap !important;
        justify-content: space-between !important;
    }

    .gr-column {
        flex: 1 !important;
        min-width: 30% !important;
        max-width: 30% !important;
        margin: 0 5px !important;
    }

    /* 标签样式 */
    .block-title {
        font-size: 14px !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    </style>
    """)

    return {
        "original_image": original_image,
        "initial_exposure": initial_exposure,
        "initial_binary": initial_binary,
        "optimized_mask": optimized_mask,
        "optimized_exposure": optimized_exposure,
        "optimized_binary": optimized_binary,
        "stats_display": stats_display,
        "evolution_plot": evolution_plot,
        "system_status": system_status
    }