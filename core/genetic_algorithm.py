import numpy as np
from deap import base, creator, tools, algorithms
from .lithography_simulation import LithographySimulator


class MaskOptimizer:
    def __init__(self, simulator, target_image):
        self.simulator = simulator
        self.target_image = target_image
        self.setup_genetic_algorithm()

    def setup_genetic_algorithm(self):
        # 创建适应度函数和个体类
        creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
        creator.create("Individual", list, fitness=creator.FitnessMin)

        self.toolbox = base.Toolbox()

        # 注册遗传算法操作
        self.toolbox.register("evaluate", self.evaluate_individual)
        self.toolbox.register("mate", tools.cxTwoPoint)
        self.toolbox.register("mutate", tools.mutFlipBit, indpb=0.02)
        self.toolbox.register("select", tools.selTournament, tournsize=3)

    def create_individual_with_noise(self, initial_mask_flat, noise_scale=0.02):
        noise = np.random.normal(0, noise_scale, size=initial_mask_flat.shape)
        individual = initial_mask_flat + noise
        return np.clip(individual, 0, 1)

    def evaluate_individual(self, individual):
        Lx = Ly = self.simulator.params["image_size"]
        mask = np.array(individual, dtype=np.float32).reshape((Lx, Ly))

        # 仿真并计算误差
        simulated_image = self.simulator.simulate(mask)
        binary_image = self.simulator.binarize_image(simulated_image)

        # 计算均方误差
        PE = np.mean((binary_image.astype(np.float32) - self.target_image.astype(np.float32)) ** 2)
        return PE,

    def optimize(self, initial_mask, progress_callback=None):
        Lx = Ly = self.simulator.params["image_size"]

        # 设置初始种群
        self.toolbox.register("individual", tools.initIterate, creator.Individual,
                              lambda: self.create_individual_with_noise(initial_mask.flatten()))
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        # 创建种群
        pop_size = self.simulator.params.get("population_size", 50)
        pop = self.toolbox.population(n=pop_size)

        # 设置统计和精英保留
        hof = tools.HallOfFame(1)
        stats = tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("avg", np.mean)
        stats.register("min", np.min)
        stats.register("max", np.max)

        # 运行遗传算法
        cxpb = self.simulator.params.get("crossover_rate", 0.4)
        mutpb = self.simulator.params.get("mutation_rate", 0.4)
        ngen = self.simulator.params.get("generations", 20)

        # 简化的遗传算法执行（可添加进度回调）
        algorithms.eaSimple(pop, self.toolbox, cxpb=cxpb, mutpb=mutpb,
                            ngen=ngen, stats=stats, halloffame=hof, verbose=True)

        # 返回最优个体
        best_mask = np.array(hof[0], dtype=np.float32).reshape((Lx, Ly))
        return best_mask, stats