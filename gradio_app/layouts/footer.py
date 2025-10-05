import gradio as gr

def create_footer():
    gr.HTML("""
    <footer style="
        margin-top: 20px;
        padding: 15px;
        text-align: center;
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 8px;
    ">
        <div style="
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 0 20px;
        ">
            <div>© 2025 数字光刻成像模拟系统 | 版本 1.0</div>
            <div>
                <a href="#" style="margin: 0 10px; color: inherit;">使用说明</a> |
                <a href="#" style="margin: 0 10px; color: inherit;">关于我们</a> |
                <a href="#" style="margin: 0 10px; color: inherit;">帮助中心</a>
            </div>
        </div>
    </footer>
    """)
