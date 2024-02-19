import threading
import argparse
import os
import json
import time
import logging
from termcolor import colored
import Id_config
import io
import sys
import re

from kik_unofficial.datatypes.xmpp.chatting import IncomingChatMessage, IncomingGroupChatMessage
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse
from kik_unofficial.datatypes.xmpp.base_elements import XMPPElement

from chatbot_db import ChatbotDatabase
from auction_data import auction_database
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.datatypes.xmpp.errors import LoginError

username = {}
response = {}
users = {}
db_path = 'data_storage/auction.db'

database = auction_database(db_path)

# Configure the logging as usual
logging.basicConfig(
    level=logging.INFO,  # Set your desired log level
    format="%(asctime)s [%(levelname)s]: %(message)s",
)



# This bot class handles all the callbacks from the kik client
class EchoBot(KikClientCallback):
    def __init__(self, creds: dict, database):
        print('innit')
        self.bot_display_name = None
        self.pong_list = []
        self.database = database        
        self.captcha_answers = {}

        # Initialize dictionaries to hold commands and image triggers for each group
        self.db = ChatbotDatabase()

        #creds
        username = creds['username']
        password = creds.get('password') or input("Enter your password:")
        device_id = creds['device_id']
        android_id = creds['android_id']
        node = creds.get('node')
        print(f'creds: {creds}')

        self.client = KikClient(self, username, str(password), node, device_id=device_id, android_id=android_id)
        
        self.custom_commands = {}
        # Initialize dictionaries 

        #Captcha
        self.pending_math_problems = {}  # Dictionary to store pending math problems
        self.captcha_status = {}  # Initialize a dictionary to store captcha status for each group
        self.timeout_duration = 20  # Set the timeout duration in seconds
        self.timers = {}  # Dictionary to store timers for each user
        self.db_lock = threading.Lock()
        self.user_data = {}
        self.db = auction_database(db_path)  # Ensure this is the correct class with the transfer_chips method
        self.database = ChatbotDatabase()
        self.client.wait_for_messages()

        #HEARTBEAT KEEP ALIVE PRIMAL WAY
        self.start_heartbeat()

    def start_heartbeat(self):
        print('start_heartbeat')
        heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()    

    def send_heartbeat(self, group_jid='1100228878084_g@groups.kik.com'): #ADD A group_jid OR user_jid
        print('send_heartbeat')
        while True:
            try:
                if group_jid:
                    self.client.send_chat_message(group_jid, "hello Mistress")#EDIT YOUR MESSAGE
                time.sleep(300)  
            except Exception as e:
                logging.error(f"Heartbeat error: {e}")

    # This method is called when the bot is fully logged in and setup
    def on_authenticated(self):
        self.client.request_roster()  # request list of chat partners

    def on_login_ended(self, response: LoginResponse):
        print("Logged in as " + response.username)
        print("Full name: {} {}".format(response.first_name, response.last_name))

    # This method is called if a captcha is required to login
    def on_roster_received(self, response: FetchRosterResponse):
        print("Roster received!")
        groups = []
        users = []
        print(colored(f"Roster components: roster: {type(response)}, .peers: {type(response.peers)}, more: {type(response.more)}, raw: {type(response.raw_element)}", "yellow"))
        for peer in response.peers:
            if "groups.kik.com" in peer.jid:
                groups.append(peer.jid)
            else:
                users.append(peer.jid)
           

        user_text = '\n'.join([f"User: {us}, pfp: {us}" for us in users])
        group_text = '\n'.join([f"Group: {gr}" for gr in groups])
        partner_count = len(response.peers)

        roster_info = (
            f"Roster Received\n"
            f"Total Peers: {partner_count}\n"
            f"Groups ({len(groups)}):\n{group_text}\n"
            f"Users ({len(users)}):\n{user_text}"
        )

        print(roster_info)
    
    def on_sign_up_ended(self, response: RegisterResponse):
        print("Sign up ended!")
        print("[+] Registered as " + response.kik_node)

    def on_login_error(self, login_error: LoginError):
        print("Login error: " + login_error.message)
        if login_error.is_captcha():
            login_error.solve_captcha_wizard(self.client)

    def _send_xmpp_element(self, message: XMPPElement):
        """
        Serializes and sends the given XMPP element to kik servers
        :param xmpp_element: The XMPP element to send
        :return: The UUID of the element that was sent
        """
        while not self.client.connected:
            print("[!] Waiting for connection.")
            time.sleep(0.1)
        if type(message.serialize()) is list:
            print("[!] Sending multi packet data.")
            packets = message.serialize()
            for p in packets:
                self.client.loop.call_soon_threadsafe(self.client.connection.send_raw_data, p)
            return message.message_id
        else:
            self.client.loop.call_soon_threadsafe(self.client.connection.send_raw_data, message.serialize())
            return message.message_id
        
    def item_registry(self, user_jid, command_parts):
        print(f'item_registry command: {command_parts}')
        try:
            user_title = database.get_user_data(jid=user_jid, table='set_user_data')['title']
        except Exception as e:
            print(f"Error: {e}")
            user_title = 'customer'
        if len(command_parts) < 2:
            with open("data_storage/id_sys1.txt","r") as f:
                example = f.read()
            return example
        
        elif len(command_parts) == 2:
            if command_parts[1].startswith('#'):
                print('id tag')
                id_tag = command_parts[1]
                split_result = Id_config.split_id(id_tag)
                gen_cat, spec_cat, quality, status = split_result if split_result else ( False, False, False, False)
                if gen_cat == False:
                    return "Invalid id tag. Please use the correct format."
                
                else:
                    qualit = False
                    statu = False
                    msg = Id_config.define_id(gen_cat, spec_cat, quality, status)
                    print(colored(f"context: {msg}", "yellow"))
                    if not ' end' in msg:
                        print('not end in msg')
                        return msg
                    if 'quality_All' in msg:
                        print('quality_All in msg')
                        quality = True
                    if 'status_All' in msg:
                        print('status_All in msg')
                        status = True
                    items = database.get_registry_data(id_tag, qualit, statu)
                    return items                 
                
            elif 'all' in command_parts:
                if user_title == 'owner':
                    items = database.get_all_items(table_name='item_registry')
                    if items:
                        return f"Items:\n {items}"
                    else:
                        return "No items in the registry."
                else:
                    return "You do not have permission to use this command."
                
            elif 'remove' in command_parts:
                if user_title == 'owner':
                    if database.check_item(id_tag):
                        database.remove_item_from_registry(id_tag)
                        return f"Item with id tag {id_tag} removed from the registry."
                    else:
                        return f"Item with id tag {id_tag} does not exist in the registry."
                else:
                    return "You do not have permission to use this command."
                
            elif 'check' in command_parts:
                if database.check_item(id_tag):
                    return f"Item with id tag {id_tag} exists in the registry."
                else:
                    return f"Item with id tag {id_tag} does not exist in the registry."
            else:
                print('callback, no command_parts match')
                database.get_registry_data(item_name=command_parts)
                
        elif 'add' == command_parts[1] and user_title == 'owner':
            if len(command_parts) == 2:
                return "the add command should be as follows: !registry add <#0x-0x-0x-0x> <item name> <item descreiption> <item price>"
            else:
                print(colored(f"context: {command_parts}", "yellow"))
                segments = self.recombine_items(command_parts, user_jid)
                print(segments)
                if len(segments) != 5:
                    return "Invalid number of segments. Please provide item name, description, and price."
                else:
                    id_tag = command_parts[2]
                    transaction_id = segments[4].replace('<', '').replace('>', '')
                    item_name = segments[1].replace('<', '').replace('>', '')
                    item_description = segments[2].replace('<', '').replace('>', '')
                    item_price = segments[3].replace('<', '').replace('>', '')
                    database.add_item_temp(transaction_id, id_tag, item_name, item_description, item_price)
                    self.client.send_chat_message('silverknightdelta_7e8@talk.kik.com', f'transaction with the id: {segments[4]} has been added to the temp registry.')
                    return f"Item with id tag {id_tag} added to the registry."
        
    def items_in_auction(self, user_jid, command_parts):
        print(f'items_in_auction command: {command_parts}')
        user_title = database.get_user_data(user_jid)['title']
        if user_title == 'owner':
            items = database.get_registry_data('in_auction')
            if items:
                return f"Items in auction: {items}"
            else:
                return "No items in auction."
        else:
            return "You do not have permission to view items in auction."
        
    def bid_on_item(self, user_jid, command_parts):
        pass

    def show_Inventory(self, user_jid):
        user = database.get_user_data(user_jid, table='set_user_data')['username']
        items = database.get_user_data(user, table='item_ownership')
        if items:
            return f"Items in {user}'s inventory: {items}"
        else:
            return f"you do not have any items in your inventory."

    def show_dashboard(self, user_jid):
        pass

    def link_to_user(self, user_jid, group_jid, tag='check_id'):
        if tag == 'check_id':
            if not database.get_user_data(user_jid, table='set_user_data'):
                self.client.send_chat_message(group_jid, 'You must link this chat to your inventory in order use this fuction. message me in dm and say \'link\'.')
                return False
            else:
                return True
        elif tag == 'return_username':
            return database.get_user_data(user_jid)['username']
        
    def recombine_items(self, items_list, user_jid):
        items_list = items_list[2:]  # Remove the first two items '!registry' and 'add'
        item_id = items_list[0]  # Third item is the item id
        item_name = ""
        item_description = ""
        item_price = ""
        transaction_id = ""
        des = False

        for i in range(1, len(items_list)):
            if items_list[i].startswith('<') and '>' in items_list[i] and not item_name:  # Start of item name
                item_name += items_list[i]  # Remove the '<' character
                
            elif not des:
                item_description += f'{items_list[i]} '  # Add a space to separate the words
                if items_list[i].endswith('>'):
                    des = True
                    continue  # End of item name, description, or price
            elif not item_price and items_list[i].startswith('<') and '>' in items_list[i]: 
                 # Item name is not set yet
                item_price += items_list[i]  # Remove the '>' character
            
        transaction_id = database.generate_transaction('craft', user_jid, item_name,)
        return [item_id,item_name,item_description,item_price,transaction_id]  # Exit the loop since we have found the item price

        
    # This method is called when the bot receives a direct message (chat message)
    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print("Chat message received!")
        separator = colored("--------------------------------------------------------", "cyan")
        group_message_header = colored("[+ DIRECT MESSAGE +]", "cyan")

        print(separator)
        print(group_message_header)
        print(colored(f"From AJID: {chat_message.from_jid}", "yellow"))
        print(colored(f"Says: {chat_message.body}", "yellow"))
        print(separator)

        user_jid = chat_message.from_jid
        command_parts = chat_message.body.strip().split()
        command = command_parts[0].lower() if command_parts else ""


        database.add_user_if_not_exists(chat_message.from_jid, table='set_user_data')
        self.client.send_chat_message(chat_message.from_jid, f'You said "{chat_message.body}"!')

        if chat_message.body.lower() == "friend":
            self.client.add_friend(chat_message.from_jid)
            self.client.send_chat_message(chat_message.from_jid, "You are now my friend! <3")

        if chat_message.body.lower() == "link":
            self.client.add_friend(chat_message.from_jid)
            database.add_user_if_not_exists(user_jid, table='set_user_data')
            user_data = database.get_user_data(chat_message.from_jid, table='set_user_data')
            print(colored(f"User data: {user_data}", "yellow"))
            unique_id = user_data['unique_id'] if user_data else None
            if unique_id:
                self.client.send_chat_message(chat_message.from_jid, f'your unique_id links you to your inventory in the group chat of your choice.\n in order for this to work, copy your unique_id then go to an unlinked chat has the auction house and say !connect [unique_id]\n for example: !connect 98wgf98ey4g9e .')
                self.client.send_chat_message(chat_message.from_jid, f'!connect {unique_id}')
            else:
                self.client.send_chat_message(chat_message.from_jid, "sorry, you do not have a unique_id. please contact the auction house owner for assistance.")

        if command == '!transaction':
            msg = database.generate_transaction(user_jid, command_parts)
            self.client.send_chat_message(chat_message.from_jid, msg)

        if command == 'pfp3':
            try:
                print(separator)
                print('catching stdout')
                # Create a string buffer
                buffer = io.StringIO()
                data = ''

                # Save a reference to the original stdout
                original_stdout = sys.stdout

                # Redirect stdout to the buffer
                sys.stdout = buffer

                self.client.request_info_of_users(chat_message.from_jid)
                while True:
                    if not 'pic' in data:
                        data = buffer.getvalue() 
                    else:    
                        sys.stdout = original_stdout
                        username_match = re.search(r"<username>(.*?)</username>", data)
                        print(f"username_match: {username_match}")
                        display_name_match = re.search(r"<display-name>(.*?)</display-name>", data)
                        print(f"display_name_match: {display_name_match}")
                        picture_link_match = re.search(r"<pic ts=\"\d+\">(.*?)</pic>", data)
                        print(f"picture_link_match: {picture_link_match}")

                        try:
                            if username_match and display_name_match and picture_link_match:
                                username = username_match.group(1)
                                display_name = display_name_match.group(1)
                                picture_link = picture_link_match.group(1)
                                picture_link = picture_link + '/orig.jpg'
                            
                                # Use the extracted information
                                print(f"Username: {username}")
                                print(f"Display Name: {display_name}")
                                print(f"Picture Link: {picture_link}")
                            self.client.send_chat_message(chat_message.from_jid, f"Username: {username}\nDisplay Name: {display_name}\nPicture Link: {picture_link}")
                        except Exception as e:
                            self.client.send_chat_message(chat_message.from_jid, f"Failed to extract user information: {e}")
                        break
                # self.client.send_chat_message(chat_message.from_jid, f'raw3: {data}')
                # Redirect stdout back to the terminal
                print(separator)
                    
            except Exception as e:
                self.client.send_chat_message(chat_message.from_jid, f'Failed to get user data.: {e}')

    # This method is called when the bot receives a chat message in a group
    def on_group_message_received(self, chat_message: chatting.IncomingGroupChatMessage):
        print("Group message received!")
        separator = colored("--------------------------------------------------------", "cyan")
        group_message_header = colored("[+ GROUP MESSAGE +]", "cyan")

        print(separator)
        print(group_message_header)
        print(colored(f"From AJID: {chat_message.from_jid}", "yellow"))
        print(colored(f"From group: {chat_message.group_jid}", "yellow"))
        print(colored(f"Says: {chat_message.body}", "yellow"))
        print(separator)

        body = chat_message.body.split()
        command = body[0].lower() if body else ""
        group_jid = chat_message.group_jid
        user_jid = chat_message.from_jid
        message_body = chat_message.body
        command_parts = chat_message.body.strip().split()
        command = command_parts[0].lower() if command_parts else ""
        # Convert message to lowercase for case-insensitive comparisons
        message = str(chat_message.body.lower())
        database.add_user_if_not_exists(user_jid, table='new_user_data', groupjids=group_jid)
 

        if command == "!registry":
            print('registry command triggered.')
            try:
            # if self.link_to_user(user_jid, group_jid):
                registry_message = self.item_registry(user_jid, command_parts)
                self.client.send_chat_message(group_jid, registry_message)
            except Exception as e:
                print(f"Error: {e}. Positional arguments provided-- group id: {group_jid}, user_id: {user_jid}, command parts: {command_parts}")

        if command == "!in_auction":
            bid_message = self.items_in_auction(user_jid, command_parts)
            self.client.send_chat_message(group_jid, bid_message)

        if command == "!bid":
            bid_message = self.bid_on_item(user_jid, command_parts)
            if bid_message and self.link_to_user(user_jid, group_jid):
                self.client.send_chat_message(group_jid, bid_message)

        if command == "!inventory":
            if self.link_to_user(user_jid, group_jid):
                Inventory_message = self.show_Inventory(user_jid)
                self.client.send_chat_message(group_jid, Inventory_message)
            else:
                self.client.send_chat_message(group_jid, "You must link this chat to your inventory in order use this fuction. message me in dm and say 'link'.")

        if command == "!dashboard":
            try:
                data = self.client.request_info_of_users(user_jid)
                print(separator)
                print(colored(f"Data: {data}, data type = {type(data)}", "yellow"))
                print(separator)
                dashboard_message = self.show_dashboard(user_jid)
                if dashboard_message and self.link_to_user(user_jid, group_jid):
                    self.client.send_chat_message(group_jid, dashboard_message)
            except Exception as e:
                print(f"Error: {e}")

        if chat_message.body.lower() == "help" or chat_message.body.lower() == "commands" or chat_message.body.lower() == "cmds" or chat_message.body.lower() == "command" or chat_message.body.lower() == "cmd" or chat_message.body.lower() == "help me" or chat_message.body.lower() == "helpme" or chat_message.body.lower() == "help me!":
            with open("data_storage/help.txt","r") as f:
                self.client.send_chat_message(chat_message.group_jid, f.read())
            return
        
        if chat_message.body.lower() == "ping":
                self.client.send_chat_message(chat_message.group_jid, "pong")
        
        if chat_message.body.lower() == "intro":
            with open("data_storage/intro.txt","r") as f:
                self.client.send_chat_message(chat_message.group_jid, f.read())
            return    
        
        if command == "!connect":
            unique_id = command_parts[1]
            if unique_id:
                msg = database.link_group_to_user(user_jid, unique_id)
                self.client.send_chat_message(chat_message.group_jid, msg)
            else:
                self.client.send_chat_message(chat_message.group_jid, "You must provide a unique_id to link your chat to your inventory. head to dms and say link to get your unique_id.")
        


    
def main():
    print('main')
    # The credentials file where you store the bot's login information
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--creds', default='creds.json', help='Path to credentials file')
    args = parser.parse_args()

    # Changes the current working directory to /examples
    if not os.path.isfile(args.creds):
        print("Can't find credentials file.")
        return
    else:
        print(f"Using credentials file: {args.creds}")

    # load the bot's credentials from creds.json
    with open(args.creds, "r") as f:
        creds = json.load(f)

    bot = EchoBot(creds, database)

    # let the bot start
    bot.client.wait_for_messages()


if __name__ == '__main__':
    main()

    creds_file = "creds.json"

    # Check if the credentials file is in the current working directory, otherwise change directory
    if not os.path.isfile(creds_file):
        os.chdir("credit file path")

    # Load the bot's credentials from creds.json
    with open(creds_file) as f:
        creds = json.load(f)
    callback = EchoBot(creds, database)
