import logging
import sqlite3
import threading
import random
import Id_config

letters = 'abcdefghijklmnopqrstuvwxyz'
symbols = '!@#$%^&*()_+'


class auction_database:
    def __init__(self, db_path, table_suffix):
        self.db_path = db_path
        self.table_suffix = table_suffix
        self.lock = threading.Lock()
        self.setup_database()
        self.user_data = {}  # Dictionary to store user data
    
    def generate_unique_id(self):
        unique_id = ''.join(random.choice(letters + symbols) for i in range(15))
        return unique_id
 
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
                    print("Creating tables if they do not exist")
                    # Create Users table with additional columns if they do not exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS item_registry (
                            item_name TEXT PRIMARY KEY,
                            item_id TEXT,
                            item_description TEXT,
                            item_owner TEXT
                        );
                    """)
                    print("Created item_registry table")
                    # Create Inventory table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS new_user_data (
                            jid TEXT PRIMARY KEY,
                            groupjids TEXT
                        );
                    """)
                    print("Created new_user_data table")
                    # Create Inventory table if it doesn't exist
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS set_user_data (
                            username PRIMARY KEY,
                            ajid_1 TEXT DEFAULT 'not-set',
                            ajid_2 TEXT DEFAULT 'not-set',
                            ajid_3 TEXT DEFAULT 'not-set',
                            ajid_4 TEXT DEFAULT 'not-set',
                            unique_id TEXT,
                            currency_balance INTEGER DEFAULT 100000,
                            title TEXT DEFAULT 'Customer'
                        );
                    """)
                    print("Created set_user_data table")
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
                    print("Created currency_transactions table")
                    conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Error setting up database: {e}")

    def link_group_to_user(self, jid, unique_id, ):
        table_name = "set_user_data"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {table_name} WHERE unique_id = ?", (unique_id,))
                    user_data = cursor.fetchone()
                    if user_data:
                        ajid_slots = ['ajid_1', 'ajid_2', 'ajid_3', 'ajid_4']
                        for ajid_slot in ajid_slots:
                            if user_data[ajid_slot] == 'not-set':
                                cursor.execute(f"UPDATE {table_name} SET {ajid_slot} = ? WHERE unique_id = ?", (jid, unique_id))
                                conn.commit()
                        else:
                            logging.info(f"No empty ajid slots available for {jid}")
                            return f"No empty ajid slots available for {jid}"
                    else:
                        logging.info(f"No user found with u_id: {unique_id}")
                        return f"No user found with u_id: {unique_id}"
            except sqlite3.Error as e:   
                return f"Error linking chat, speak to the auction house owner for assistance {jid}: {e}"
                
    def add_user_if_not_exists(self, from_jid, groupjids=None, table=None):
        initial_coins = 100000
        table_name = table
        title = 'Customer'
        ajid_1, ajid_2, ajid_3, ajid_4 = 'not-set', 'not-set', 'not-set', 'not-set'

        if table_name == 'new_user_data':
            with self.lock:
                try:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"INSERT OR IGNORE INTO {table_name} (jid, groupjids) VALUES (?, ?)", (from_jid, groupjids))
                        conn.commit()
                        logging.info(f"User {from_jid} added or already exists in the database.")
                except sqlite3.Error as e:
                    logging.error(f"Error in add_user_if_not_exists for {from_jid}: {e}")
        else:
            username = from_jid[:-13]
            unique_id = self.generate_unique_id()
            with self.lock:
                try:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"INSERT OR IGNORE INTO {table_name} (username, ajid_1, ajid_2, ajid_3, ajid_4, unique_id, currency_balance, title) VALUES (?, ?, ?, ?, ?, ?, ?, ?,)", (username,ajid_1, ajid_2, ajid_3, ajid_4, unique_id, initial_coins, title,))
                        conn.commit()
                        logging.info(f"User {from_jid} added or already exists in the database.")
                except sqlite3.Error as e:
                    logging.error(f"Error in add_user_if_not_exists for {from_jid}: {e}")
                    cursor.execute(f"PRAGMA table_info({table_name})")
                    table_columns = cursor.fetchall()
                    logging.info(f"Current table setup for {table_name}:")
                    for column in table_columns:
                        logging.info(f"Column name: {column[1]}, Type: {column[2]}, Nullable: {column[3]}, Default value: {column[4]}")

    def get_user_data(self, jid, table='new_user_data'):
        table_name = table
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {table_name} WHERE username = ? OR ajid_1 = ? OR ajid_2 = ? OR ajid_3 = ? OR ajid_4 = ?", (jid, jid, jid, jid, jid))
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
                elif Id_config.is_valid_id(item_name):
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {table_name} WHERE item_id = ?", (item_name,))
                        item_data = cursor.fetchone()
                        if item_data:
                            return dict(item_data)
                        else:
                            return None    
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
    
    def check_user_id(self, user_id):
        table_name = "set_user_data"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {table_name} WHERE ajid_1 = ? OR ajid_2 = ? OR ajid_3 = ? OR ajid_4 = ?", (user_id, user_id, user_id, user_id))
                    user_data = cursor.fetchone()
                    if user_data:
                        return True
                    else:
                        return False
            except sqlite3.Error as e:
                logging.error(f"Error checking user id: {e}")
                return False
            
# if __name__ == "__main__":
#     db_path = "/C:/Users/holyk/Desktop/code/kikbot-blackjackbot/data_storage/auction.db"  # Provide the correct database path
#     table_suffix = "suffix"  # Provide the desired table suffix
#     auction_db = auction_database(db_path, table_suffix)
#     auction_db.setup_database()
