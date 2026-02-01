import sqlite3
import json

DB_PATH = "prices.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS price_cache (
                crop TEXT,
                market TEXT,
                result TEXT,
                PRIMARY KEY (crop, market)
            )
        """)
        conn.commit()
        conn.close()
    except Exception as e:
        print(f"Database init error: {e}")
        raise

def get_cached_price(crop, market):
    if not crop or not market:
        return None
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT result FROM price_cache WHERE crop=? AND market=?",
            (crop.lower().strip(), market.lower().strip())
        )
        row = cursor.fetchone()
        conn.close()
        
        if row:
            return json.loads(row[0])
        return None
    except json.JSONDecodeError as e:
        print(f"Cache JSON error: {e}")
        return None
    except Exception as e:
        print(f"Cache retrieval error: {e}")
        return None

def save_price(crop, market, result):
    if not crop or not market or not result:
        return False
    
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT OR REPLACE INTO price_cache VALUES (?, ?, ?)",
            (crop.lower().strip(), market.lower().strip(), json.dumps(result))
        )
        conn.commit()
        conn.close()
        return True
    except json.JSONDecodeError as e:
        print(f"Cache JSON error: {e}")
        return False
    except Exception as e:
        print(f"Cache save error: {e}")
        return False
