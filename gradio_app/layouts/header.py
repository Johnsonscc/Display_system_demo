import gradio as gr
from ..config.theme_config import load_theme

theme = load_theme()


def create_header():
    with gr.Row(variant="compact", elem_classes=["header-row"]):
        with gr.Column(scale=1):
            gr.Image("assets/icons/logo.png", width=40, show_label=False,
                     show_download_button=False, container=False)
        with gr.Column(scale=9):
            gr.Markdown("""
            # <center> ⚒️数字光刻成像模拟系统</center>
            ### <center>基于Hopkins成像算法的DMD数字光刻模拟系统</center>
            """)

    # 添加全局样式确保铺满屏幕
    gr.HTML("""
    <style>
        /* 确保整个应用铺满视口 */
        .gradio-container {
            max-width: 100% !important;
            width: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
        }

        /* 主内容区域 */
        .main-content {
            width: 100% !important;
            max-width: 100% !important;
            margin: 0 auto;
        }

        /* 头部行 */
        .header-row {
            width: 100% !important;
            margin: 0 !important;
            padding: 20px !important;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        /* 确保所有容器都铺满 */
        .gr-box {
            width: 100% !important;
        }

        /* 标签页容器 */
        .output-tabs {
            width: 100% !important;
        }

        /* 移除可能限制宽度的样式 */
        .container {
            max-width: 100% !important;
        }
    </style>
    """)