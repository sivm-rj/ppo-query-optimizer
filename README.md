# PPO-Based SQL Join Order Optimizer

This project uses **Reinforcement Learning (PPO)** to optimize **SQL join orders** across multiple tables and compares the performance with PostgreSQL's default planner using **real cost estimates** (`EXPLAIN (FORMAT JSON)`).

The environment is built using **Gym**, and the RL agent is trained with **Stable-Baselines3 (PPO)**.

---

## 📌 Features

- ✅ Custom Gym environment for join order optimization
- ✅ Supports N-table joins (default: 20)
- ✅ Uses mock cost for training and PostgreSQL `EXPLAIN` for evaluation
- ✅ Visualizations: cost comparison, training rewards
- ✅ Easy deployment on [Railway PostgreSQL](https://railway.app/)

---

## 📁 Project Structure

```
ppo-query-optimizer/
├── config.py                  # PostgreSQL URL and training settings
├── requirements.txt
├── .gitignore
├── train.py                  # PPO training script
├── evaluate.py               # RL vs Greedy cost comparison
├── visualize.py              # Training reward visualization (optional)
├── env/
│   └── join_order_env.py     # Custom Gym environment
├── utils/
│   ├── cost_estimator.py     # mock_cost + PostgreSQL EXPLAIN cost
│   └── db_setup.py           # Create tables and insert test rows
└── notebooks/
    └── demo.ipynb            # Optional: interactive Colab version
```

---

## 🔧 Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/your-username/ppo-query-optimizer.git
cd ppo-query-optimizer
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure PostgreSQL Connection

Edit `config.py`:

```python
RAILWAY_DB_URL = "postgresql://<user>:<pass>@<host>:<port>/<db>"
NUM_TABLES = 20
TOTAL_TIMESTEPS = 50000
MODEL_PATH = "ppo_20table_join_order.zip"
```

You can use [Railway](https://railway.app/) to host your free PostgreSQL instance.

---

## 🏁 Running the Project

### ✅ Step 1: Set Up the Database

```bash
python utils/db_setup.py
```

Creates tables `t0` to `t19` and inserts test rows.

---

### 🎓 Step 2: Train the PPO Agent

```bash
python train.py
```

Trains on mock cost. The model is saved to disk.

---

### 🔍 Step 3: Evaluate Join Order Plans

```bash
python evaluate.py
```

Runs the PPO agent to generate join plans and compares **real PostgreSQL costs** with a **greedy baseline**.

---

## 📊 Visualizations

- **Training rewards** over time (`visualize.py`)
- **Cost comparison**: RL vs Greedy

---

## 🧠 Example Output

```
PPO Join Order: [12, 7, 16, 10, 6, ...]
PostgreSQL Cost (RL): 1320.3

Greedy Join Order: [0, 1, 2, ..., 19]
PostgreSQL Cost (Greedy): 2422.9

✅ PPO Agent found better plans than Greedy!
```

---

## 🙌 Credits

Developed by [Shivam Raj](https://github.com/your-username)  
Inspired by research on **learned query optimizers** and **AI for databases**.

---


