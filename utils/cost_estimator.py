import psycopg2
from config import RAILWAY_DB_URL
import json

# Table list used to generate real SQL queries
TABLES = [f"t{i}" for i in range(20)]

def mock_cost(plan):
    """
    Simple simulated cost:
    - Penalize if join jumps far (e.g., t1 → t8)
    - Reward for smooth plans (adjacent tables)
    """
    cost = 0
    for i in range(1, len(plan)):
        if abs(plan[i] - plan[i - 1]) > 1:
            cost += 5
        else:
            cost += 1
    return cost


def join_condition(t1, t2):
    return f"{t2}.fk = {t1}.id"


def build_join_query(plan):
    """
    Build a SQL JOIN query based on table plan.
    e.g. t0 JOIN t1 ON t1.fk = t0.id JOIN t2 ON t2.fk = t1.id ...
    """
    base = TABLES[plan[0]]
    query = base
    for i in range(1, len(plan)):
        t1 = TABLES[plan[i - 1]]
        t2 = TABLES[plan[i]]
        condition = join_condition(t1, t2)
        query += f" JOIN {t2} ON {condition}"
    return f"EXPLAIN (FORMAT JSON) SELECT * FROM {query};"


def estimate_postgres_cost(plan):
    """
    Sends EXPLAIN (FORMAT JSON) to Railway PostgreSQL
    and returns the estimated total cost.
    """
    sql = build_join_query(plan)

    try:
        conn = psycopg2.connect(RAILWAY_DB_URL)
        cur = conn.cursor()
        cur.execute(sql)

        result = cur.fetchone()[0]  # first row, already a Python list
        plan_json = result[0]["Plan"]  # extract plan from JSON
        total_cost = plan_json["Total Cost"]

        cur.close()
        conn.close()
        return total_cost

    except Exception as e:
        print("PostgreSQL EXPLAIN failed:", e)
        return 1e9  # Large penalty if EXPLAIN fails
