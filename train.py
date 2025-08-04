# train.py

from stable_baselines3 import PPO
from stable_baselines3.common.monitor import Monitor
from stable_baselines3.common.env_util import make_vec_env
from env.join_order_env import JoinOrderEnv
from config import NUM_TABLES, TOTAL_TIMESTEPS, MODEL_PATH
import os

def train_ppo():
    # Wrap environment for logging
    env = make_vec_env(lambda: Monitor(JoinOrderEnv(num_tables=NUM_TABLES)), n_envs=1)

    # Create PPO model
    model = PPO(
        policy="MlpPolicy",
        env=env,
        verbose=1,
        learning_rate=0.0005,
    )

    # Train the model
    print(f"Training PPO for {TOTAL_TIMESTEPS} timesteps...")
    model.learn(total_timesteps=TOTAL_TIMESTEPS)

    # Save the model
    model.save(MODEL_PATH)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_ppo()
