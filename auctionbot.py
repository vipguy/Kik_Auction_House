import threading
import argparse
import os
import json
import time
import logging
from termcolor import colored

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

table_suffix = 'users'  
database = auction_database(db_path, table_suffix)

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
        self.db = auction_database(db_path, table_suffix)  # Ensure this is the correct class with the transfer_chips method
        self.database = ChatbotDatabase()
        self.client.wait_for_messages()

        #HEARTBEAT KEEP ALIVE PRIMAL WAY
        self.start_heartbeat()

    def query_user(self, jid):
        print('query_user')
        if jid in self.users:
            return self.users[jid]
        else:
            self.client.request_info_of_users(jid)
            while jid not in self.users:
                pass  # You might want to add a timeout or a better waiting mechanism here
            return self.users[jid]

    def get_group_jid_number(jid):
        print('get_group_jid_number')
        return jid.split('@')[0][0:-2]

    def start_heartbeat(self):
        print('start_heartbeat')
        heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()    

    def send_heartbeat(self, group_jid='1100261147932_g@groups.kik.com'): #ADD A group_jid OR user_jid
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
        for peer in response.peers:
            if "groups.kik.com" in peer.jid:
                groups.append(peer.jid)
            else:
                users.append(peer.jid)

        user_text = '\n'.join([f"User: {us}" for us in users])
        group_text = '\n'.join([f"Group: {gr}" for gr in groups])
        partner_count = len(response.peers)

        roster_info = (
            f"Roster Received\n"
            f"Total Peers: {partner_count}\n"
            f"Groups ({len(groups)}):\n{group_text}\n"
            f"Users ({len(users)}):\n{user_text}"
        )

        print(roster_info)
    
    def item_registry(self, user_jid, command_parts):
        print(f'item_registry command: {command_parts}')
        user_title = database.get_user_data(user_jid)['title']
        if len(command_parts) < 2:
            with open("data_storage/id_sys1.txt","r") as f:
                example = f.read()
            return example
        if 'all' in command_parts and user_title == 'owner':
            items = database.get_registry_data('all')
            if items:
                return f"Items: {items}"
            else:
                return "No items in the registry."
            
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
        pass

    def show_dashboard(self, user_jid):
        pass

    def extract_username(jid):
        username = jid.split('@')[0][:-4]
        return username
        
    # This method is called when the bot receives a direct message (chat message)
    def on_chat_message_received(self, chat_message: chatting.IncomingChatMessage):
        print("Chat message received!")
        database.add_user_if_not_exists(chat_message.from_jid)
        self.client.send_chat_message(chat_message.from_jid, f'You said "{chat_message.body}"!')
        if chat_message.body.lower() == "friend":
            self.client.add_friend(chat_message.from_jid)
            self.client.send_chat_message(chat_message.from_jid, "You can now add me to groups! <3")


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
        database.add_user_if_not_exists(user_jid)
 

        if command == "!registry":
            try:
                registry_message = self.item_registry(user_jid, command_parts)
                self.client.send_chat_message(group_jid, registry_message)
            except Exception as e:
                print(f"Error: {e}. Positional arguments provided-- group id: {group_jid}, user_id: {user_jid}, command parts: {command_parts}")

        if command == "!in_auction":
            bid_message = self.items_in_auction(user_jid, command_parts)
            self.client.send_chat_message(group_jid, bid_message)

        if command == "!bid":
            bid_message = self.bid_on_item(user_jid, command_parts)
            if bid_message:
                self.client.send_chat_message(group_jid, bid_message)
            else:
                self.client.send_chat_message(group_jid, "not ready yet!")

        if command == "!inventory":
            Inventory_message = self.show_Inventory(user_jid)
            if Inventory_message:
                self.client.send_chat_message(group_jid, Inventory_message)
            else:    
                self.client.send_chat_message(group_jid, "not ready yet!")

        if command == "!dashboard":
            try:
                data = self.client.request_info_of_users(user_jid)
                print(separator)
                print(colored(f"Data: {data}, data type = {type(data)}", "yellow"))
                print(separator)
                dashboard_message = self.show_dashboard(user_jid)
                if dashboard_message:
                    self.client.send_chat_message(group_jid, dashboard_message)
                else:
                    self.client.send_chat_message(group_jid, "not ready yet!")

            except Exception as e:
                print(f"Error: {e}")

        if chat_message.body.lower() == "help" or chat_message.body.lower() == "commands" or chat_message.body.lower() == "cmds" or chat_message.body.lower() == "command" or chat_message.body.lower() == "cmd" or chat_message.body.lower() == "help me" or chat_message.body.lower() == "helpme" or chat_message.body.lower() == "help me!" or chat_message.body.lower() == "intro":
            with open("data_storage/help.txt","r") as f:
                self.client.send_chat_message(chat_message.group_jid, f.read())
            return
        
        if chat_message.body.lower() == "ping":
                self.client.send_chat_message(chat_message.group_jid, "pong")
        
        if chat_message.body.lower() == "intro":
            with open("data_storage/intro.txt","r") as f:
                self.client.send_chat_message(chat_message.group_jid, f.read())
            return    
        
        if command == "!talk":
            self.client.send_chat_message(chat_message.group_jid, f'You said "{chat_message.body}"!')
        
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

# Configure the logging as usual
logging.basicConfig(
    level=logging.INFO,  # Set your desired log level
    format="%(asctime)s [%(levelname)s]: %(message)s",
)


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