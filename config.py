# config.py

RAILWAY_DB_URL = "postgresql://username:password@host:port/database"

# Number of tables in the join environment
NUM_TABLES = 20

# PPO training settings
TOTAL_TIMESTEPS = 50000
LEARNING_RATE = 0.0005

# Output model file name
MODEL_PATH = "ppo_20table_join_order.zip"
