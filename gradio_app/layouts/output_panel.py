import gradio as gr


def create_output_panel(state_manager):
    with gr.Tabs(elem_classes=["output-tabs"]):
        with gr.Tab("📊 仿真结果", elem_id="simulation-results"):
            # 标题
            gr.Markdown("### 🎯 光刻仿真结果展示")

            # 第一行：三个图像
            with gr.Row(equal_height=True, variant="panel"):
                with gr.Column(min_width=300, scale=1, variant="compact"):
                    gr.Markdown("#### 原始图像与仿真")
                    original_image = gr.Image(
                        label="原始目标图像",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image", "image-card"]
                    )

                with gr.Column(min_width=300, scale=1, variant="compact"):
                    gr.Markdown("#### 初始掩膜效果")
                    initial_exposure = gr.Image(
                        label="原始掩膜曝光图像",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image", "image-card"]
                    )

                with gr.Column(min_width=300, scale=1, variant="compact"):
                    gr.Markdown("#### 二值化结果")
                    initial_binary = gr.Image(
                        label="原始掩膜二值图像",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image", "image-card"]
                    )

            # 第二行：三个图像
            with gr.Row(equal_height=True, variant="panel"):
                with gr.Column(min_width=300, scale=1, variant="compact"):
                    gr.Markdown("#### 优化后掩膜")
                    optimized_mask = gr.Image(
                        label="遗传算法优化掩膜",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image", "image-card"]
                    )

                with gr.Column(min_width=300, scale=1, variant="compact"):
                    gr.Markdown("#### 优化后效果")
                    optimized_exposure = gr.Image(
                        label="优化掩膜曝光图像",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image", "image-card"]
                    )

                with gr.Column(min_width=300, scale=1, variant="compact"):
                    gr.Markdown("#### 优化二值化")
                    optimized_binary = gr.Image(
                        label="优化掩膜二值图像",
                        show_label=True,
                        container=True,
                        height="auto",
                        elem_classes=["output-image", "image-card"]
                    )

            # 系统状态
            with gr.Row():
                with gr.Column():
                    system_status = gr.Textbox(
                        label="🛠️ 系统运行状态",
                        value="等待初始化...",
                        interactive=False,
                        elem_classes=["status-box"]
                    )

        with gr.Tab("📈 性能分析", elem_id="performance-analysis"):
            gr.Markdown("### 📊 系统性能分析")

            with gr.Row():
                with gr.Column(scale=6):
                    # 使用 Group 替代 Box
                    with gr.Group():
                        gr.Markdown("#### 关键指标对比")
                        stats_display = gr.DataFrame(
                            headers=["性能指标", "初始值", "优化值", "改善率"],
                            label="仿真性能统计",
                            interactive=False,
                            elem_classes=["stats-table"]
                        )

                with gr.Column(scale=4):
                    # 使用 Group 替代 Box
                    with gr.Group():
                        gr.Markdown("#### 优化过程")
                        evolution_plot = gr.Plot(
                            label="遗传算法收敛曲线",
                            elem_classes=["evolution-plot"]
                        )

        with gr.Tab("ℹ️ 系统信息", elem_id="system-info"):
            with gr.Row():
                with gr.Column(scale=7):
                    gr.Markdown("""
                    ### 🌟 数字光刻成像模拟系统

                    **系统特性：**
                    - 🎯 基于Hopkins成像理论的光刻仿真
                    - 🧬 集成遗传算法掩膜优化
                    - ⚡ 实时参数调整与可视化
                    - 📊 全面的性能分析
                    - 🎨 直观的结果展示

                    **使用流程：**
                    1. 📁 上传初始掩膜和目标图像
                    2. ⚙️ 调整光学参数和优化参数
                    3. 🚀 开始仿真优化过程
                    4. 📈 查看优化结果和性能分析

                    **技术优势：**
                    - 高精度光学仿真模型
                    - 智能掩膜优化算法
                    - 实时进度监控
                    - 专业级可视化分析
                    """)

                with gr.Column(scale=3):
                    gr.Markdown("""
                    ### 🔧 系统参数

                    **版本信息：**
                    - 版本号：v1.0.0
                    - 更新日期：2025年10月

                    **支持格式：**
                    - 图像格式：PNG, JPG, BMP
                    - 最大尺寸：1024x1024
                    - 色彩模式：灰度/RGB

                    **系统要求：**
                    - Python 3.8+
                    - 内存：8GB+
                    - 存储：1GB+
                    """)

    # 增强的CSS样式
    gr.HTML("""
    <style>
    /* 卡片式设计 */
    .image-card {
        background: white;
        border-radius: 12px;
        padding: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
        border: 1px solid #e9ecef;
    }

    .image-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.12);
    }

    /* 组容器样式 */
    .gr-group {
        background: white;
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border: 1px solid #e9ecef;
    }

    /* 标签页样式 */
    #simulation-results, #performance-analysis, #system-info {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        border-radius: 12px;
        padding: 20px;
    }

    /* 状态框样式 */
    .status-box {
        background: linear-gradient(135deg, #e3f2fd 0%, #bbdefb 100%);
        border: 2px solid #4a90e2;
        border-radius: 10px;
        font-weight: 600;
        color: #2c3e50;
    }

    /* 进化图样式 */
    .evolution-plot {
        background: white;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }

    /* 响应式图像布局 */
    @media (min-width: 1200px) {
        .gr-row {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
        }

        .gr-column {
            min-width: auto !important;
        }
    }

    /* 标题样式 */
    h3, h4 {
        color: #2c3e50 !important;
        margin-bottom: 15px !important;
    }

    /* 图标样式 */
    .tab-nav .tab-item {
        font-weight: 600 !important;
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