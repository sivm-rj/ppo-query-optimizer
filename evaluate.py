# evaluate.py

from stable_baselines3 import PPO
from env.join_order_env import JoinOrderEnv
from utils.cost_estimator import estimate_postgres_cost
from config import NUM_TABLES, MODEL_PATH

import matplotlib.pyplot as plt

def evaluate(model, episodes=10):
    rl_costs = []
    greedy_costs = []
    plans = []

    for ep in range(episodes):
        env = JoinOrderEnv(num_tables=NUM_TABLES)
        obs, _ = env.reset()
        done = False
        plan = []

        while not done:
            action, _ = model.predict(obs, deterministic=True)
            plan.append(int(action))
            obs, reward, done, _, _ = env.step(action)

        rl_cost = estimate_postgres_cost(plan)
        greedy_plan = sorted(env.tables)
        greedy_cost = estimate_postgres_cost(greedy_plan)

        plans.append(plan)
        rl_costs.append(rl_cost)
        greedy_costs.append(greedy_cost)

        print(f"\nEpisode {ep + 1}")
        print(f"PPO Join Order: {plan} | Cost: {rl_cost}")
        print(f"Greedy Order : {greedy_plan} | Cost: {greedy_cost}")

    return rl_costs, greedy_costs

def plot_costs(rl_costs, greedy_costs):
    plt.plot(rl_costs, label="RL Plan Cost")
    plt.plot(greedy_costs, label="Greedy Plan Cost")
    plt.xlabel("Episode")
    plt.ylabel("PostgreSQL Estimated Cost")
    plt.title("RL vs Greedy Join Order Cost")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    print("Loading PPO model...")
    model = PPO.load(MODEL_PATH)

    print("Evaluating model...")
    rl_costs, greedy_costs = evaluate(model, episodes=10)

    plot_costs(rl_costs, greedy_costs)

    rl_avg = sum(rl_costs) / len(rl_costs)
    greedy_avg = sum(greedy_costs) / len(greedy_costs)
    print(f"\nAvg RL Cost:     {rl_avg}")
    print(f"Avg Greedy Cost: {greedy_avg}")

    if rl_avg < greedy_avg:
        print("PPO Agent found better plans than Greedy!")
    else:
        print("Greedy was still better (try more training or tuning).")
