import logging
import sqlite3
import threading
import random
import Id_config

letters = 'abcdefghijklmnopqrstuvwxyz'
symbols = '!@#$%^&*()_+'


class auction_database:
    def __init__(self, db_path):
        self.db_path = db_path
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
                            item_key TEXT PRIMARY KEY,
                            item_id TEXT,
                            item_name TEXT,
                            item_description TEXT,
                            item_price integer
                        );
                    """)
                    
                    cursor.execute("""
                        CREATE TABLE IF NOT EXISTS temp_registry (
                            transaction_id TEXT PRIMARY KEY,
                            item_id TEXT,
                            item_name TEXT,
                            item_description TEXT,
                            item_price integer
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
                            title TEXT DEFAULT 'Customer',
                            nickname TEXT DEFAULT 'not-set'
                        );
                    """)
                    print("Created set_user_data table")
                    # Create Currency Transactions table if it doesn't exist
                    cursor.execute(f"""
                        CREATE TABLE IF NOT EXISTS currency_transactions (
                            transaction_id INTEGER PRIMARY KEY,
                            transaction_type TEXT,
                            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                            initiator TEXT,
                            item_1 TEXT,
                            amount_1 INTEGER,
                            recipient TEXT,
                            item_2 TEXT,
                            amount_2 INTEGER
                        );
                    """)
                    print("Created currency_transactions table")
                    cursor.execute(f"""
                        CREATE TABLE item_ownership (
                            item_key INTEGER,
                            username INTEGER,
                            quantity INTEGER,
                            PRIMARY KEY (item_key, username),
                            FOREIGN KEY (item_key) REFERENCES item_registry (item_key),
                            FOREIGN KEY (username) REFERENCES set_user_data (username)
                        );
                    """)
                                   
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
                                new_id = self.generate_unique_id()
                                cursor.execute(f"UPDATE {table_name} SET {ajid_slot} = ?, unique_id = ? WHERE unique_id = ?", (jid, new_id, unique_id))
                                conn.commit()
                                return f"you are now linked to the chat."
                        else:
                            logging.info(f"No empty ajid slots available for {jid}")
                            return f"No empty ajid slots available for {jid}"
                    else:
                        logging.info(f"No user found with u_id: {unique_id}")
                        return f"No user found with u_id: {unique_id}"
            except sqlite3.Error as e:   
                return f"Error linking chat, speak to the auction house owner for assistance {jid}: {e}"
                
    def add_user_if_not_exists(self, from_jid, groupjids=None, table=None):
        initial_coins = 1000
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
            print('generated id')
            unique_id = self.generate_unique_id()
            with self.lock:
                try:
                    print('trying to add user')
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        print('cursor created')
                        cursor.execute(f"INSERT OR IGNORE INTO {table_name} (username, ajid_1, ajid_2, ajid_3, ajid_4, unique_id, currency_balance, title) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (from_jid, ajid_1, ajid_2, ajid_3, ajid_4, unique_id, initial_coins, title))
                        print('inserted')
                        conn.commit()
                        logging.info(f"User {from_jid} updated the set user database.")
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
            if table_name == 'new_user_data':
                try:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {table_name} WHERE username = ?", (jid))
                        user_data = cursor.fetchone()
                        if user_data:
                            return dict(user_data)
                        else:
                            return None
                except sqlite3.Error as e:
                    logging.error(f"Error getting user data for {jid}: {e}")
                    return None
            elif table_name == 'set_user_data':
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
            elif table_name == 'item_ownership':
                try:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {table_name} WHERE username = ?", (jid,))
                        user_data = cursor.fetchall()
                        if user_data:
                            return [dict(row) for row in user_data]
                        else:
                            return None
                except sqlite3.Error as e:
                    logging.error(f"Error getting user data for {jid}: {e}")
                    return None

    def get_registry_data(self, item_name, quality=False, status=False):
        table_name = 'item_registry'
        print (f'item_name: {item_name[1], {item_name}}')
        with self.lock:
            try:

                if item_name == 'in_auction':
                    print('command in_auction')
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT item_id FROM {table_name}")
                        item_names = cursor.fetchall()
                        item_ids = cursor.fetchall()
                        result = [item_id[1] for item_id in item_ids if item_id[1].split('-')[2] == '02']
                        return result
                elif Id_config.is_valid_id(item_name):
                    return self.check_item_by_id(table_name, item_name, quality, status)
                else:
                    print('item name command')
                    item_name.pop(0)
                    item = ''
                    for i in range(len(item_names)):
                        item += str(item_names[i-1]) + ' '
                    item = item.strip()
                    print(f'item: {item}')
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {table_name} WHERE item_name LIKE ?", ('%' + item + '%',))
                        item_data = cursor.fetchall()
                        if item_data:
                            return [dict(row) for row in item_data]
                        else:
                            return None     
            except sqlite3.Error as e:
                logging.error(f"Error getting item data for {item_name}: {e}")
                return None
            
    def update_item_id(self,old_id, new_item_id = None):
        table_name = "item_registry"
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"UPDATE {table_name} SET item_id = ? WHERE item_id = ?", (new_item_id, old_id))
                    conn.commit()
                    logging.info("Item IDs updated successfully.")
            except sqlite3.Error as e:
                logging.error(f"Error updating item IDs: old_id: {old_id}, new_id: {new_item_id}, {e}")


    def check_item(self, item_name, table_name = "item_registry"):
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"SELECT * FROM {table_name} WHERE item_name = ?", (item_name,))
                    item_data = cursor.fetchone()
                    if item_data:
                        return True
                    else:
                        return False
            except sqlite3.Error as e:
                logging.error(f"Error checking item: {e}")
                return False
            
    def add_item_temp(self, transaction_id, item_id, item_name, item_description, item_price):
        table_name = "temp_registry"
         
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT INTO {table_name} (transaction_id, item_id, item_name, item_description, item_price) VALUES (?, ?, ?, ?, ?)", (transaction_id, item_id, item_name, item_description, item_price))
                    conn.commit()
                    logging.info("Item added to temp_registry successfully.")
            except sqlite3.Error as e:
                logging.error(f"Error adding item to temp_registry: {e}")

    def generate_transaction(self, transaction_type, initiator, item_1, amount_1 = 1, recipient = 'not-set', item_2 = 'not-set', amount_2 = 0):
        table_name = "currency_transactions"
        transaction_id = self.generate_unique_id()
        timestamp = sqlite3.datetime.datetime.now()
        print(f'transaction_id: {transaction_id}, transaction_type: {transaction_type}, timestamp: {timestamp}, initiator: {initiator}, item_1: {item_1}, amount_1: {amount_1}, recipient: {recipient}, item_2: {item_2}, amount_2: {amount_2}')
        with self.lock:
            try:
                with self.create_connection() as conn:
                    cursor = conn.cursor()
                    cursor.execute(f"INSERT INTO {table_name} (transaction_id, transaction_type, timestamp , initiator, item_1, amount_1, recipient, item_2, amount_2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (transaction_id, transaction_type, timestamp, initiator, item_1, amount_1, recipient, item_2, amount_2))
                    conn.commit()
                    logging.info("Transaction added to currency_transactions successfully.")
            except sqlite3.Error as e:
                logging.error(f"Error adding transaction to currency_transactions: {e}")
        return transaction_id

    def check_item_by_id(self, table_name, item_name, quality=False, status=False):
        try:
            print(f'id command, quality: {quality}, status: {status}')
            with self.create_connection() as conn:
                cursor = conn.cursor()
                gen_cat, spec_cat, qual, stat = Id_config.split_id(item_name)
                start = f'{gen_cat}-{spec_cat}-'
                if not qual == '07':
                    start += f'{qual}-'
                    if not stat == '04':
                        start += f'{stat}-'
                        print(f'start: {start}')
                        cursor.execute(f"SELECT * FROM {table_name} WHERE item_id = ?", (start,))
                        item_data = cursor.fetchall()
                    else:    
                        print(f'start: {start}')
                        cursor.execute(f"SELECT * FROM {table_name} WHERE item_id like ?", ('%' + start + '%',))
                        item_data = cursor.fetchall()
                else:    
                    print(f'start: {start}')
                    cursor.execute(f"SELECT * FROM {table_name} WHERE item_id like ?", ('%' + start + '%',))
                    item_data = cursor.fetchall()
                    if not status:
                        item_list = 'item list:\n'
                        for row in item_data:
                            print(f'Id command Row itteration: {row[1]}')
                            if Id_config.split_id(row[1])[3] == stat:
                                item_list += f'{str(row[2])}, price: {str(row[4])}\n'
            return item_list
        except Exception as e:
            print(f"Registry id command Error: {e}")
            return 'sorry there was an error during Id_config.is_valid_id(item_name)'
        
    def get_all_items(self, table_name, raw=False):

        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT item_name FROM {table_name}")
            item_names = cursor.fetchall()
            print (f'item_names: {type(item_names)}')
            items = ''
            if raw:
                return item_names
            for name in item_names:
                print(f'name: {name[0]}, type: {type(name[0])}')
                items += f' {str(name[0])}\n'  # Modify this line to select the second column of each row
            return items
        
    def get_auction_registry(self):
        table_name = 'item_registry'
        item_data = self.get_all_items(table_name, raw=True)
        list_of_items = 'list of items in auction:\n'
        for items in item_data:
            if items[1].split('-')[3] == '02':
                list_of_items += f'item: {items[2]}, price: {items[4]}\n'
            else:
                continue
        return list_of_items
        
if __name__ == "__main__":
    db_path = "/C:/Users/holyk/Desktop/code/kikbot-blackjackbot/data_storage/auction.db"  # Provide the correct database path
    table_suffix = "suffix"  # Provide the desired table suffix
    auction_db = auction_database(db_path, table_suffix)
    
    # with auction_db.create_connection() as conn:
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM item_registry")
    #     rows = cursor.fetchall()
    #     for row in rows:
    #         gen_cat= random.randint(1,9)
    #         spec_cat = random.randint(1,9)
    #         quality = random.randint(1,9)
    #         status = random.randint(1,9)
    #         new_item_id = f"#0{gen_cat}-0{spec_cat}-0{quality}-0{status}"
    #         # new_item_id = Id_config.generate_id()

    #         try:
    #             auction_db.update_item_id(row[0], new_item_id)
    #         except Exception as e:
    #             logging.error(f"Error updating item ID: {e}")
    #             continue
    # Update all item_id in the item_registry table

# Example usage:
# auction_db.update_item_id("new_item_id")
    # auction_db.add_user_if_not_exists("abc123sdjnsdkjndscjn",table='set_user_data')

    
