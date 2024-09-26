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
    
    def generate_unique_id(self, num=4):
        unique_id = ''.join(random.choice(letters + symbols) for i in range(num))
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
                            item_description TEXT
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
                    try:
                        print("Created currency_transactions table")
                        cursor.execute(f"""
                            CREATE TABLE item_ownership (
                                item_key TEXT,
                                item_id TEXT,
                                username TEXT,
                                quantity INTEGER,
                                perk_1 TEXT DEFAULT 'not-set',
                                perk_1_value INTEGER DEFAULT 0,
                                perk_2 TEXT DEFAULT 'not-set',
                                perk_2_value INTEGER DEFAULT 0,
                                equiped TEXT DEFAULT FALSE,
                                item_price integer,
                                PRIMARY KEY (item_key, username),
                                FOREIGN KEY (item_key) REFERENCES item_registry (item_key),
                                FOREIGN KEY (username) REFERENCES set_user_data (username)
                            );
                        """)
                    except sqlite3.Error as e:
                        logging.error(f"Error setting up database: {e}") 
                                     
                        cursor.execute(f"""
                            CREATE TABLE new_item_ownership (
                                new_item_key TEXT,
                                item_id TEXT,
                                username TEXT,
                                quantity INTEGER,
                                perk_1 TEXT DEFAULT 'not-set',
                                perk_1_value INTEGER DEFAULT 0,
                                perk_2 TEXT DEFAULT 'not-set',
                                perk_2_value INTEGER DEFAULT 0,
                                equiped TEXT DEFAULT FALSE,
                                item_price integer,
                                PRIMARY KEY (new_item_key, username),
                                FOREIGN KEY (new_item_key) REFERENCES item_registry (item_key),
                                FOREIGN KEY (username) REFERENCES set_user_data (username)
                            );
                        """)
                                    
                    conn.commit()
            except sqlite3.Error as e:
                logging.error(f"Error setting up database: {e}")

    def link_group_to_user(self, jid, unique_id):
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

    def get_user_data(self, jid = None, item_key = None, item_name = None, table='new_user_data', displayname = None, equipped = None):
        table_name = table
        with self.lock:
            if table_name == 'new_user_data':
                try:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {table_name} WHERE username = ?", (jid,))
                        user_data = cursor.fetchone()
                        if user_data:
                            return user_data
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
                            return user_data
                        else:
                            return None
                except sqlite3.Error as e:
                    logging.error(f"Error getting user data for {jid}: {e}")
                    return None
            elif table_name == 'item_ownership':
                if item_key:
                    try:
                        with self.create_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute(f"SELECT * FROM {table_name} WHERE item_key = ? AND username = ?", (item_key, jid))
                            user_data = cursor.fetchall()
                            if user_data:
                                return user_data
                            else:
                                return None
                    except sqlite3.Error as e:
                        logging.error(f"Error getting user data for {jid}: {e}")
                        return None
                elif equipped:
                    print('getting equipped items')
                    try:
                        with self.create_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute(f"SELECT * FROM {table_name} WHERE username = ? AND equiped = ?", (jid, 'TRUE'))
                            user_data = cursor.fetchall()
                            if user_data:
                                for item in user_data:
                                    print(f'equipped items: {item[4]}, {item[5]}, {item[6]}, {item[7]}')
                                return user_data
                            else:
                                return None
                    except sqlite3.Error as e:
                        logging.error(f"Error getting user data for {jid}: {e}")
                        return None
                elif item_name:
                    try:
                        with self.create_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute(f"SELECT * FROM {table_name} WHERE item_name = ?", (item_name,))
                            user_data = cursor.fetchall()
                            if user_data:
                                return user_data
                            else:
                                return None
                    except sqlite3.Error as e:
                        logging.error(f"Error getting user data for {jid}: {e}")
                        return None
                else:
                    print('getting all items')
                    try:
                        with self.create_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute(f"SELECT * FROM {table_name} WHERE username = ?", (jid,))
                            user_data = cursor.fetchall()
                            if user_data:
                                return user_data
                            else:
                                return None
                    except sqlite3.Error as e:
                        logging.error(f"Error getting user data for {jid}: {e}")
                        return None
            elif table_name == 'dashboard_prefrences':
                if displayname:
                    try:
                        with self.create_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute(f"SELECT * FROM {table_name} WHERE display_name LIKE ?", ('%' + displayname + '%',))
                            user_data = cursor.fetchone()
                            if user_data:
                                return user_data
                            else:
                                return None
                    except sqlite3.Error as e:
                        logging.error(f"Error getting user data for {jid}: {e}")
                        return None
                else:
                    try:
                        print(f'getting dashboard prefrences {jid}')
                        with self.create_connection() as conn:
                            cursor = conn.cursor()
                            cursor.execute(f"SELECT * FROM {table_name} WHERE username = ?", (jid,))
                            user_data = cursor.fetchone()
                            return user_data
                    except sqlite3.Error as e:
                        logging.error(f"Error getting user data for {jid}: {e}")
                        return None
    
    def get_registry_data(self, item_id, quality=False, status=False):
        table_name = 'item_registry'
        with self.lock:
            try:
                if Id_config.is_valid_id(item_id):
                    return self.check_item_by_id(table_name, item_id, quality, status)
            except sqlite3.Error as e:
                logging.error(f"Error getting item data for {item_id}: {e}")
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

    def check_item(self, item_key = None, item_name = None, item_id = None, table_name = "item_registry"):
        if item_key:
            with self.lock:
                try:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {table_name} WHERE item_key = ?", (item_key,))
                        item_data = cursor.fetchone()
                        if item_data:
                            return item_data
                        else:
                            return False
                except sqlite3.Error as e:
                    logging.error(f"Error checking item: {e}")
                    return False
        elif item_name:
            with self.lock:
                try:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {table_name} WHERE item_name = ?", (item_name,))
                        item_data = cursor.fetchone()
                        if item_data:
                            return item_data
                        else:
                            return False
                except sqlite3.Error as e:
                    logging.error(f"Error checking item: {e}")
                    return False
        elif item_id:
            with self.lock:
                try:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"SELECT * FROM {table_name} WHERE item_name = ? AND item_id = ?", (item_name, item_id))
                        item_data = cursor.fetchone()
                        if item_data:
                            return item_data
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
                    if transaction_type == 'self':
                        cursor.execute(f"INSERT INTO {table_name} (transaction_id, transaction_type, timestamp , initiator, item_1, amount_1, recipient, item_2, amount_2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (transaction_id, transaction_type, timestamp, initiator, item_1, amount_1, initiator, item_1, amount_1))
                    else:
                        cursor.execute(f"INSERT INTO {table_name} (transaction_id, transaction_type, timestamp , initiator, item_1, amount_1, recipient, item_2, amount_2) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", (transaction_id, transaction_type, timestamp, initiator, item_1, amount_1, recipient, item_2, amount_2))
                    conn.commit()
                    logging.info("Transaction added to currency_transactions successfully.")
            except sqlite3.Error as e:
                logging.error(f"Error adding transaction to currency_transactions: {e}")
        return transaction_id

    def authorize_item_creation(self, transaction_id):
        print(f'authorize_item_creation: {transaction_id}')
        transaction_id = transaction_id
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM temp_registry WHERE transaction_id = ?", (transaction_id,))
                item_data = cursor.fetchone()
                cursor.execute(f"SELECT * FROM Currency_transactions WHERE transaction_id = ?", (transaction_id,))
                Ttransaction_data = cursor.fetchone()
                quantity = Ttransaction_data[5]
                username = Ttransaction_data[6]
                item = self.check_item(item_data[1],item_data[2])
                if item:
                    item_key = item[0]
                    item_id = item[1]
                    item_price = item[4]
                    inventory = self.get_user_data(item_key, table='item_ownership')
                    if inventory:
                        quantity = inventory[3] + quantity
                        cursor.execute(f"UPDATE item_ownership SET quantity = quantity + ? WHERE item_key = ? AND username = ?", (quantity, item_key, username))
                    else:
                        cursor.execute(f"INSERT INTO item_ownership (item_key, item_id, username, quantity, item_price) VALUES (?, ?, ?, ?, ?)", (item_key, item_id, username, quantity, item_price))
                else: 
                    item_key = self.generate_unique_id()
                    cursor.execute(f"INSERT INTO item_registry (item_key, item_id, item_name, item_description, item_price) VALUES (?, ?, ?, ?, ?)", (item_key, item_data[1], item_data[2], item_data[3], item_data[4]))                
                    cursor.execute(f"INSERT INTO item_ownership (item_key, item_id, username, quantity, item_price) VALUES (?, ?, ?, ?, ?)", (item_key, item_data[1], username, quantity, item_data[4]))
                    cursor.execute("DELETE FROM temp_registry WHERE transaction_id = ?", (transaction_id,))
                conn.commit()
            return (f'transaction with the id {transaction_id} authorized successfully.')
        except sqlite3.Error as e:
            logging.error(f"Error authorizing item creation: {e}")
            return None

    def check_item_by_id(self, table_name, item_id, quality=False, status=False, username=None):
        try:
            print(f'id command, quality: {quality}, status: {status}')
            with self.create_connection() as conn:
                cursor = conn.cursor()
                gen_cat, spec_cat, qual, stat = Id_config.split_id(item_id)
                start = f'{gen_cat}-{spec_cat}-'
                if not qual == '01':
                    start += f'{qual}-'
                    if not stat == '01':
                        start += f'{stat}'
                        print(f'start 1: {start}')
                        if username:
                            cursor.execute(f"SELECT * FROM {table_name} WHERE item_id = ? AND username = ?", (start, username))
                        else:
                            cursor.execute(f"SELECT * FROM {table_name} WHERE item_id = ?", (start,))
                        item_data = cursor.fetchall()
                        item_list = {}
                        for row in item_data:
                            key = row[0]
                            print(f'row 0: {key}')
                            item_list[key] = {}
                            for idx, value in enumerate(row):
                                column_name = cursor.description[idx][0]  # Get the column name
                                print(f'column_name: {column_name}, value: {value}')
                                item_list[key][column_name] = value
                        return item_list
                    else:    
                        print(f'start 2: {start}')
                        if username:
                            cursor.execute(f"SELECT * FROM {table_name} WHERE item_id like ? AND username = ?", ('%' + start + '%', username))
                        else:
                            cursor.execute(f"SELECT * FROM {table_name} WHERE item_id like ?", ('%' + start + '%',))
                        item_data = cursor.fetchall()
                        try:
                            print(f'item_data: {item_data[0]}')
                            item_list = {}
                            for row in item_data:
                                key = row[0]
                                print(f'row 0: {key}')
                                item_list[key] = {}
                                for idx, value in enumerate(row):
                                    column_name = cursor.description[idx][0]  # Get the column name
                                    print(f'column_name: {column_name}, value: {value}')
                                    item_list[key][column_name] = value
                            return item_list
                        except Exception as e:
                            print(f"Error occurred while processing item at start 2: {e}")
                            return None
                else:    
                    print(f'start 3: {start}')
                    if username:
                        cursor.execute(f"SELECT * FROM {table_name} WHERE item_id like ? AND username = ?", ('%' + start + '%', username))
                    else:
                        cursor.execute(f"SELECT * FROM {table_name} WHERE item_id like ?", ('%' + start + '%',))
                    item_data = cursor.fetchall()
                    print(f'item_data: {item_data[0][0]}')
                    if stat != '01':
                        try:
                            item_list = {}
                            for row in item_data:
                                if Id_config.split_id(row[1])[3] == stat:
                                    key = row[0]
                                    item_list[key] = {}
                                    for idx, value in enumerate(row):
                                        column_name = cursor.description[idx][0]  # Get the column name
                                        print(f'column_name: {column_name}, value: {value}')
                                        item_list[key][column_name] = value
                        except Exception as e:
                            print(f"Error occurred while processing item data1: {e}")
                            return None
                    else:
                        try:
                            item_list = {}
                            for row in item_data:
                                key = row[0]
                                print(f'row: {row}')
                                print(f'row[0]: {key}')
                                item_list[key] = {}
                                for idx, value in enumerate(row):
                                    column_name = cursor.description[idx][0]  # Get the column name
                                    print(f'column_name: {column_name}, value: {value}')
                                    item_list[key][column_name] = value
                        except Exception as e:
                            print(f"Error occurred while processing item data2: {e}")
                            return None
            return item_list
            
        except Exception as e:
            print(f"Registry id command Error: {e}")
            return 'sorry there was an error during Id_config.is_valid_id(item_id)'
        
    def get_all_items(self, table_name, raw=False):
        with self.create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {table_name}")  # Modify this line to select all columns from the table
            item_data = cursor.fetchall()
            items = ''
            if raw:
                return item_data
            for row in item_data:
                items += f'{str(row[2])}\n'  # Modify this line to select the second column of each row
            return items
        
    def get_auction_registry(self):
        table_name = 'item_ownershiP'
        item_data = self.get_all_items(table_name, raw=True)
        list_of_items = 'list of items in auction:\n'
        if item_data:
            for items in item_data:
                if items[1].split('-')[3] == '02':
                    list_of_items += f'item: {items[2]}, price: {items[4]}\n'
                else:
                    continue
        else:
            return 

    def update_user_data(self, jid, table, column, value , item_key = None):
        print(f'update_user_data: {jid}, {table}, {column}, {value}, {item_key}')
        with self.lock:
            if item_key:
                try:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"UPDATE {table} SET {column} = ? WHERE item_key = ? AND username = ?", (value, item_key, jid))
                        conn.commit()
                        logging.info(f"User data updated successfully for {jid}.")
                except sqlite3.Error as e:
                    logging.error(f"Error updating user data for {jid}: {e}")
            else:
                try:
                    with self.create_connection() as conn:
                        cursor = conn.cursor()
                        cursor.execute(f"UPDATE {table} SET {column} = ? WHERE username = ?", (value, jid))
                        conn.commit()
                        logging.info(f"User data updated successfully for {jid}.")
                except sqlite3.Error as e:
                    logging.error(f"Error updating user data for {jid}: {e}")

    def generate_dashboard_data(self, jid, nickname):
        
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO dashboard_prefrences (username, pfpx, pfpy, pfp_size, box_red, box_green, box_blue, box_alpha, bio, display_name, background_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (jid, 650, 50, 300, 0, 125, 255, 170, 'not-set', nickname, 'not-set'))
                conn.commit()
        except Exception as e:
            logging.error(f"Error inserting dashboard preferences: {e}")
    
    def add_item_to_inventory(self, item_key, item_id, username, quantity, item_price):
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"INSERT INTO item_ownership (item_key, item_id, username, quantity, item_price) VALUES (?, ?, ?, ?, ?)", (item_key, item_id, username, quantity, item_price))
                conn.commit()
        except Exception as e:
            logging.error(f"Error inserting item ownership: {e}")

    def delete_item_from_inventory(self, item_key, user_jid):
        try:
            with self.create_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f"DELETE FROM item_ownership WHERE item_key = ? AND username = ?", (item_key, user_jid))
                conn.commit()
        except Exception as e:
            logging.error(f"Error deleting item from inventory: {e}")
            
    # def enchant_item(item_key):
    #     try:
    #         with self.create_connection() as conn:
    #             cursor = conn.cursor()
    #             cursor.execute(f"SELECT * FROM item_ownership WHERE item_key = ?", (item_key))
    #             item_data = cursor.fetchone()   
                



if __name__ == "__main__":
    db_path = "/C:/Users/holyk/Desktop/code/kikbot-blackjackbot/data_storage/auction.db"  # Provide the correct database path
    auction_db = auction_database(db_path)
    
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

    
