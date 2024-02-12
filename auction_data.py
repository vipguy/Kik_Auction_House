import logging
import sqlite3
import threading



class auction_database:
    def __init__(self, db_path, table_suffix):
        self.db_path = db_path
        self.table_suffix = table_suffix
        self.lock = threading.Lock()
        self.setup_database()
        self.user_data = {}  # Dictionary to store user data
 
    def create_connection(self):
        try:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys=ON")
            return conn
        except sqlite3.Error as e:
            logging.error(f"Error connecting to database: {e}")
            return None

    def setup_database(self):
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    # user_data = f'user_data_{self.table_suffix}'
                    # user_inventory = f'user_inventory_{self.table_suffix}'
                    # user_currency = f'user_currency_{self.table_suffix}'

                    # Create Users table with additional columns if they do not exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS item_registry (
                            item_name TEXT PRIMARY KEY,
                            item_id TEXT,
                            item_description TEXT,
                            item_owner TEXT
                        );
                    """)

                    # Create Inventory table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS user_data (
                            jid TEXT PRIMARY KEY,
                            username TEXT DEFAULT 'hidden-user',
                            groupjids TEXT,
                            currency_balance INTEGER DEFAULT 100000,
                            title TEXT DEFAULT 'Customer'
                        );
                    """)

                    # Create Currency Transactions table if it doesn't exist
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS currency_transactions (
                            transaction_id INTEGER PRIMARY KEY,
                            username TEXT,
                            transaction_type TEXT,
                            amount DECIMAL(10, 2),
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            FOREIGN KEY (username) REFERENCES user(username)
                        );
                    """)
                    conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Error setting up database: {e}")

    def set_user_nickname(self, jid, nickname):
        table_name = "user_data"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET username = ? WHERE jid = ?", (nickname, jid))
                    conn.commit()
                    logging.info(f"Nickname set for {jid}: {nickname}")
                
                    # Update user data in the dictionary
                    if jid in self.user_data:
                        self.user_data[jid]['nickname'] = nickname
            except sqlite3.Error as e:
                logging.error(f"Error setting nickname for {jid}: {e}")
                
    def add_user_if_not_exists(self, from_jid, username=None, groupjids=None):
        initial_coins = 100000
        if not username:
            username = 'hidden-user'
        if not groupjids:
            groupjids = 'none yet'
        table_name = "user_data"
        title = 'Customer'
        jid = from_jid
        
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT OR IGNORE INTO {table_name} (jid, username, groupjids, currency_balance, title) VALUES (?, ?, ?, ?, ?)", (jid, username, groupjids, initial_coins, title,))
                    conn.commit()
                    logging.info(f"User {from_jid} added or already exists in the database.")
            except sqlite3.Error as e:
                logging.error(f"Error in add_user_if_not_exists for {from_jid}: {e}")
                self.setup_database()
                cursor.execute(f"PRAGMA table_info({table_name})")
                table_columns = cursor.fetchall()
                logging.info(f"Current table setup for {table_name}:")
                for column in table_columns:
                    logging.info(f"Column name: {column[1]}, Type: {column[2]}, Nullable: {column[3]}, Default value: {column[4]}")

    def get_user_data(self, jid):
        table_name = 'user_data'
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {table_name} WHERE jid = ?", (jid))
                    user_data = cursor.fetchone()
                    if user_data:
                        return dict(user_data)
                    else:
                        return None
            except sqlite3.Error as e:
                logging.error(f"Error getting user data for {jid}: {e}")
                return None

    def get_registry_data(self, item_name):
        table_name = 'item_registry'
        with self.lock:
            try:
                if item_name == 'all':
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT item_name FROM {table_name}")
                        item_names = cursor.fetchall()
                        return [item[0] for item in item_names]
                elif item_name == 'in_auction':
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT item_id FROM {table_name}")
                        item_names = cursor.fetchall()
                        item_ids = cursor.fetchall()
                        result = [item_id[0] for item_id in item_ids if item_id[0].split('-')[2] == '02']
                        return result
                else:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {table_name} WHERE item_name = ?", (item_name,))
                        item_data = cursor.fetchone()
                        if item_data:
                            return dict(item_data)
                        else:
                            return None     
            except sqlite3.Error as e:
                logging.error(f"Error getting item data for {item_name}: {e}")
                return None
                