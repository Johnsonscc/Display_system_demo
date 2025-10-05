import pandas as pd
import plotly.graph_objects as go
import numpy as np


class StateManager:
    def __init__(self):
        self.current_results = {}
        self.optimization_history = []

    def update_results(self, results):
        self.current_results = results
        # 安全地访问stats对象
        if "stats" in results and hasattr(results["stats"], 'select'):
            try:
                min_fitness, avg_fitness = results["stats"].select("min", "avg")
                self.optimization_history = {
                    "min_fitness": min_fitness,
                    "avg_fitness": avg_fitness
                }
            except Exception as e:
                print(f"更新优化历史时出错: {e}")
                self.optimization_history = {
                    "min_fitness": [],
                    "avg_fitness": []
                }

    def generate_stats(self):
        if not self.current_results:
            return pd.DataFrame(columns=["指标", "初始值", "优化值", "改善率"])

        try:
            initial_pe = self.current_results["initial"]["pe"]
            optimized_pe = self.current_results["optimized"]["pe"]
            improvement = (initial_pe - optimized_pe) / initial_pe * 100 if initial_pe > 0 else 0

            stats_data = {
                "指标": ["图形偏差(PE)", "最大强度", "对比度"],
                "初始值": [
                    f"{initial_pe:.4f}",
                    f"{np.max(self.current_results['initial']['simulation']):.4f}",
                    f"{self._calculate_contrast(self.current_results['initial']['binary']):.4f}"
                ],
                "优化值": [
                    f"{optimized_pe:.4f}",
                    f"{np.max(self.current_results['optimized']['simulation']):.4f}",
                    f"{self._calculate_contrast(self.current_results['optimized']['binary']):.4f}"
                ],
                "改善率": [
                    f"{improvement:.2f}%" if improvement > 0 else "N/A",
                    "N/A", "N/A"
                ]
            }

            return pd.DataFrame(stats_data)
        except Exception as e:
            print(f"生成统计信息时出错: {e}")
            return pd.DataFrame([["错误", str(e), "N/A", "N/A"]],
                                columns=["指标", "初始值", "优化值", "改善率"])

    def generate_evolution_plot(self):
        if not self.optimization_history or not self.optimization_history["min_fitness"]:
            fig = go.Figure()
            fig.add_annotation(text="暂无优化历史数据", x=0.5, y=0.5, showarrow=False)
            fig.update_layout(
                xaxis_title="迭代次数",
                yaxis_title="适应度值",
                showlegend=True,
                margin=dict(t=40, b=20, l=20, r=20)
            )
            return fig

        try:
            generations = list(range(len(self.optimization_history["min_fitness"])))

            fig = go.Figure()

            fig.add_trace(go.Scatter(
                x=generations,
                y=self.optimization_history["min_fitness"],
                mode='lines+markers',
                name='最小适应度',
                line=dict(color='red', width=2)
            ))

            fig.add_trace(go.Scatter(
                x=generations,
                y=self.optimization_history["avg_fitness"],
                mode='lines+markers',
                name='平均适应度',
                line=dict(color='green', width=2)
            ))

            fig.update_layout(
                title="遗传算法优化过程",
                xaxis_title="迭代次数",
                yaxis_title="适应度值",
                showlegend=True,
                margin=dict(t=40, b=20, l=20, r=20)
            )

            return fig
        except Exception as e:
            print(f"生成进化图时出错: {e}")
            fig = go.Figure()
            fig.add_annotation(text=f"错误: {str(e)}", x=0.5, y=0.5, showarrow=False)
            return fig

    def _calculate_contrast(self, image):
        try:
            if np.std(image) == 0:
                return 0
            return (np.max(image) - np.min(image)) / (np.max(image) + np.min(image))
        except:
            return 0