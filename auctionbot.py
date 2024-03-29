import os
import io
import re
import sys
import json
import math
import time
import glob
import logging
import argparse
import random
import requests
import threading
from PIL import Image
from termcolor import colored
from PIL import ImageFilter
from PIL import Image, ImageDraw, ImageFont
import Id_config

from kik_unofficial.datatypes.xmpp.chatting import IncomingChatMessage, IncomingGroupChatMessage, IncomingImageMessage
from kik_unofficial.datatypes.xmpp.sign_up import RegisterResponse
from kik_unofficial.datatypes.xmpp.login import LoginResponse
from kik_unofficial.datatypes.xmpp.roster import FetchRosterResponse, PeersInfoResponse
from kik_unofficial.datatypes.xmpp.base_elements import XMPPElement

from auction_data import auction_database
from kik_unofficial.client import KikClient
from kik_unofficial.callbacks import KikClientCallback
import kik_unofficial.datatypes.xmpp.chatting as chatting
from kik_unofficial.datatypes.xmpp.errors import LoginError
import textwrap
import os

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
        self.background_requests = {}
        self.player_status = {}  # Dictionary to store each player's current position in the mine
        self.player_loot = {}  # Dictionary to store each player's loot
        self.user_inventory = {}
        self.user_gems = {}
        self.bets = 0
        self.minute_time = time.time()
        self.instance_drops = {}
        self.total_loot = {
            'ores': {
                "Adamantite Ore": 4**2, "Arcane Ore": 5**2, "Celestial Ore": 6**2, "Dark Ore": 7**2, "Dragon Ore": 8**2, "Eldritch Ore": 10*2,
                "Dream Ore": 12**2, "Ebon Ore": 14**2, "Glimmer Ore": 16**2, "Meteorite Ore": 18**2, "Mithril Ore": 20**2, "Phantasmal Ore": 22**2,
                "Star Ore": 24**2, "Sylvan Ore": 26**2, "Titanium Ore": 28**2, "Gold ore": 30**2, "Silver Ore": 32**2, "Tin ore": 34**2, "Copper ore": 36**2,
                "Iron ore": 38**2, "Coal": 40**2,
            },
            'gems': {
                "Iolite": 4**2, "Fire Opal": 5**2, "Lapis Lazuli": 6**2, "Malachite": 7**2, "Moonstone": 8**2, "Morganite": 10**2, "Tanzanite": 12**2,
                "Spinel": 14**2, "Jade": 16**2, "Tourmaline": 18**2, "Citrine": 20**2, "Peridot": 22**2, "Garnet": 24**2,
                "Aquamarine": 26**2, "Opal": 28**2, "Topaz": 30**2, "Amethyst": 32**2, "Emerald": 34**2, "Sapphire": 36**2,
                "Ruby": 38**2, "Diamond": 40**2,
            }
        }
        self.total_rates = {
                "Iolite": 6**2, "Fire Opal": 7**2, "Lapis Lazuli": 8**2, "Malachite": 9**2, "Moonstone": 10**2, "Morganite": 11**2, "Tanzanite": 12**2,
                "Spinel": 14**2, "Jade": 16**2, "Tourmaline": 18**2, "Citrine": 20**2, "Peridot": 22**2, "Garnet": 24**2,
                "Aquamarine": 26**2, "Opal": 28**2, "Topaz": 30**2, "Amethyst": 32**2, "Emerald": 34**2, "Sapphire": 36**2,
                "Ruby": 38**2, "Diamond": 40**2,
        }

        # Initialize dictionaries to hold commands and image triggers for each group


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
        self.client.wait_for_messages()

        #HEARTBEAT KEEP ALIVE PRIMAL WAY
        self.start_heartbeat()

    def start_heartbeat(self):
        print('start_heartbeat')
        heartbeat_thread = threading.Thread(target=self.send_heartbeat)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()    

    def send_heartbeat(self, group_jid='your_main_jid_here'): #ADD A group_jid OR user_jid
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
        self.client.request_roster()
        self.start_heartbeat  # request list of chat partners

    def on_login_ended(self, response: LoginResponse):
        print("Logged in as " + response.username)
        print("Full name: {} {}".format(response.first_name, response.last_name))

    # This method is called if a captcha is required to login
    def on_roster_received(self, response: FetchRosterResponse):
        print("Roster received!")
        groups = []
        users = []
        user_text = ''

        try:
            print(colored(f"Roster components: roster: {type(response)}, .peers: {type(response.peers)}, more: {type(response.more)}, raw: {type(response.raw_element)}", "yellow"))
            for us in users:
                user_data = database.get_user_data(jid=[us][0], table='set_user_data')[0]
                if user_data:
                    print(f"adding user: {[us][0]}")
                    user_text += (f'\n{[us][0]}')
                # else:
                #     print(f"removing user: {[us][0]}")
                #     self.client.remove_friend([us][0])
                #     time.sleep(1)

            group_text = '\n'.join([f"Group: {gr}" for gr in groups])
            partner_count = len(response.peers)

            roster_info = (
                f"Roster Received\n"
                f"Total Peers: {partner_count}\n"
                f"Groups ({len(groups)}):\n{group_text}\n"
                f"Users ({len(users)}):\n{user_text}"
            )
        except Exception as e:
            print(f"Error occurred: {str(e)}")

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
    
    def start_mining(self, player_id, luck=0, energy=50, hp=100, defense=0, attack=10, speed=5):
        # Initialize the player's position in the mine (e.g., start at the entrance)
        self.player_status[player_id] = {
            'depth': 0,
            'status': 'mining',
            'energy': energy,
            'luck': luck,
            'hp': hp,
            'defense': defense,
            'attack': attack,
            'speed': speed
        }
        self.player_loot[player_id] = {}

        self.instance_drops[player_id] = {
            'left': {
                "nothing": 420.00,
                "combat": 420.00,
            },
            'right': {
                "nothing": 420.00,
                "combat": 420.00,
            },
            'center': {
                "nothing": 420.00,
                "combat": 420.00,
            }

        }
        return "You enter the mine. Which direction will you choose? (left/right/center)"

    def mine(self, player_id, direction):
        if self.player_status[player_id]['energy'] <= 2:
            self.player_status[player_id]['status'] = 'no_energy'
            return self.player_loot[player_id] #self.instance_drops[player_id]
        self.player_status[player_id]['depth'] += 1  # Increment the player's position in the mine
        self.player_status[player_id]['energy'] -= 3  # Deduct energy for mining


        # print(f'ore1: {list(self.instance_drops[player_id]['ores'].keys())[-1]}\n ore2: {list(self.instance_drops[player_id]['ores'].keys())[-2]}\n gem1: {list(self.instance_drops[player_id]['gems'].keys())[-1]}\n gem2: {list(self.instance_drops[player_id]['gems'].keys())[-2]}')
        

        if self.player_status[player_id]['depth'] % 6 == 0 or self.player_status[player_id]['depth'] == 1:
            try:
                if self.player_status[player_id]['depth'] == 1:
                    num = 1
                else:
                    num = int((self.player_status[player_id]['depth']) / 6)
                self.instance_drops[player_id]['left'].setdefault(list(self.total_loot['ores'].keys())[-num], list(self.total_loot['ores'].values())[-num])
                self.instance_drops[player_id]['right'].setdefault(list(self.total_loot['gems'].keys())[-num], list(self.total_loot['gems'].values())[-num])
                self.instance_drops[player_id]['center'].setdefault(list(self.total_loot['ores'].keys())[-num], list(self.total_loot['ores'].values())[-num])
                self.instance_drops[player_id]['center'].setdefault(list(self.total_loot['gems'].keys())[-num], list(self.total_loot['gems'].values())[-num])
                self.instance_drops[player_id]['left']['nothing'] = ((sum(list(self.instance_drops[player_id]['left'].values())) / 100) * 75 ) - (self.instance_drops[player_id]['left']['nothing'] + self.instance_drops[player_id]['left']['combat'])
                self.instance_drops[player_id]['right']['nothing'] = ((sum(list(self.instance_drops[player_id]['right'].values())) / 100) * 75 ) - (self.instance_drops[player_id]['right']['nothing'] + self.instance_drops[player_id]['right']['combat'])
                self.instance_drops[player_id]['center']['nothing'] = ((sum(list(self.instance_drops[player_id]['center'].values())) / 100) * 55 ) - (self.instance_drops[player_id]['center']['nothing'] + self.instance_drops[player_id]['center']['combat'])
                self.instance_drops[player_id]['left']['combat'] = ((sum(list(self.instance_drops[player_id]['left'].values())) / 100) * 75 ) - (self.instance_drops[player_id]['left']['nothing'] + self.instance_drops[player_id]['left']['combat'])
                self.instance_drops[player_id]['right']['combat'] = ((sum(list(self.instance_drops[player_id]['right'].values())) / 100) * 75 ) - (self.instance_drops[player_id]['right']['nothing'] + self.instance_drops[player_id]['right']['combat'])
                self.instance_drops[player_id]['center']['combat'] = ((sum(list(self.instance_drops[player_id]['center'].values())) / 100) * 55 ) - (self.instance_drops[player_id]['center']['nothing'] + self.instance_drops[player_id]['center']['combat'])
            except:
                pass
            if self.player_status[player_id]['depth'] >6 and self.player_status[player_id]['luck'] >= 1 and num < len(self.total_loot['ores'] ):
                print(num)
                # try:
                last_ore = list(self.total_loot['ores'].keys())[-num+1]
                last_ore_value = self.total_loot['ores'][last_ore]
                last_gem = list(self.total_loot['gems'].keys())[-num+1]
                last_gem_value = self.total_loot['gems'][last_gem]

                try:
                    nothing_value_lnr = self.instance_drops[player_id]['left']['nothing']
                    pre_not = nothing_value_lnr
                    nothing_value_center = self.instance_drops[player_id]['center']['nothing']
                    combat_value_lnr = self.instance_drops[player_id]['left']['combat']
                    pre_com = combat_value_lnr
                    combat_value_center = self.instance_drops[player_id]['center']['combat']
                except:
                    pre_not = 0
                    pre_com = 0
                    nothing_value_lnr = 0
                    combat_value_lnr = 0                 

                luck_multiplier = 1 + 0.1 * self.player_status[player_id]['luck']  
                last_ore_value = int(last_ore_value * math.pow(luck_multiplier, -1))
                last_gem_value = int(last_gem_value * math.pow(luck_multiplier, -1))

                try:
                    nothing_value_lnr = int(nothing_value_lnr * math.pow(luck_multiplier, -2.4))
                    nothing_value_center = int(nothing_value_center * math.pow(luck_multiplier, -2.4))
                    combat_value_lnr = int(combat_value_lnr * math.pow(luck_multiplier, -2.2))
                    combat_value_center = int(combat_value_center * math.pow(luck_multiplier, -2.2))
                except:
                    pass
                
                self.instance_drops[player_id]['left'][last_ore] = last_ore_value if last_ore_value > 0 else 1
                self.instance_drops[player_id]['right'][last_gem] = last_gem_value if last_gem_value > 0 else 1
                self.instance_drops[player_id]['center'][last_ore] = last_ore_value if last_ore_value > 0 else 1
                self.instance_drops[player_id]['center'][last_gem] = last_gem_value if last_gem_value > 0 else 1

                try:
                    self.instance_drops[player_id]['left']['nothing'] = nothing_value_lnr if nothing_value_lnr > 0 else 0
                    self.instance_drops[player_id]['right']['nothing'] = nothing_value_lnr if nothing_value_lnr > 0 else 0
                    self.instance_drops[player_id]['center']['nothing'] = nothing_value_center if nothing_value_center > 0 else 0
                    self.instance_drops[player_id]['left']['combat'] = combat_value_lnr if combat_value_lnr > 0 else 0
                    self.instance_drops[player_id]['right']['combat'] = combat_value_lnr if combat_value_lnr > 0 else 0
                    self.instance_drops[player_id]['center']['combat'] = combat_value_center if combat_value_center > 0 else 0
                except:
                    pass
                try:
                    print(f'{last_ore}: {self.total_loot['ores'][last_ore]} -> {last_ore_value}, {last_gem}: {self.total_loot['gems'][last_gem]} -> {last_gem_value}, nothing: {pre_not} -> {self.instance_drops[player_id]['left']['nothing']}, combat: {pre_com} -> {self.instance_drops[player_id]['left']['combat']}')
                except Exception as e:
                    print(f'Error: {e}')
                    
        # Simulate the outcome of mining based on the chosen direction
        try:
            if self.instance_drops[player_id]['left']['nothing'] <= 0:
                self.instance_drops[player_id]['left'].pop('nothing')
                self.instance_drops[player_id]['right'].pop('nothing')
                self.instance_drops[player_id]['center'].pop('nothing')
        except KeyError:
            pass

        try:
            if self.instance_drops[player_id]['left']['combat'] <= 0:
                self.instance_drops[player_id]['left'].pop('combat')
                self.instance_drops[player_id]['right'].pop('combat')
                self.instance_drops[player_id]['center'].pop('combat')
        except KeyError:
            pass
        outcome = random.choices(list(self.instance_drops[player_id][direction].keys()), weights=list(self.instance_drops[player_id][direction].values()))
        outcome = str(outcome[0])
        if outcome == "nothing":
            return f"energy: {self.player_status[player_id]['energy']}.\nmine depth: {self.player_status[player_id]['depth']}.\nYou mine {direction} and find {outcome}.\n say 'left', 'right', or 'center' to continue mining."
        if outcome == "combat":
            return f"energy: {self.player_status[player_id]['energy']}.\nmine depth: {self.player_status[player_id]['depth']}\nYou mine {direction} and become locked in comabt however... combat isnt set yet so keep mining.\n say 'left', 'right', or 'center' to continue mining."
        if outcome in self.player_loot[player_id]:
            self.player_loot[player_id][outcome] += 1
        else:
            self.player_loot[player_id][outcome] = 1
        return f"energy: {self.player_status[player_id]['energy']}.\nmine depth: {self.player_status[player_id]['depth']}.\nYou mine {direction} and find {outcome}.\n say 'left', 'right', or 'center' to continue mining."
    
    def start_cutting_gems(self, user_jid):
        self.instance_drops[user_jid] = {}
        self.instance_drops[user_jid]['gem broke'] = int(40**2)
        components = self.get_player_stats(user_jid)
        if components:
            luck = components['luck']
        else:
            luck = 0
        self.player_status[user_jid] = {
            'depth': 0,
            'status': 'cutting gems',
            'energy': 1,
            'luck': luck,
            'hp': 0,
            'defense': 0,
            'attack': 0,
            'speed': 0
        }

        components = self.get_player_stats(user_jid)
        if components:
            luck = components['luck']
        else:
            luck = 0
        item_id = "#09-06-01-01"
        columns = database.check_item_by_id('item_ownership', item_id, username=user_jid)
        self.user_gems[user_jid] = {}
        if columns:
            print(f"Columns: {columns}")
            msg = 'here is a list of gems you can cut: \n'
            for key in columns:
                print(f"Row: {columns[key]['username']}, username: {user_jid}")
                if columns[key]['username'] == user_jid:
                    item_name = database.check_item(key)[2]
                    msg += f"{key} : {item_name}, {columns[key]['quantity']} \n"
                    self.user_gems[user_jid][key] = {
                        'name': item_name,
                        'Id': columns[key]['item_id'],
                        'quantity': columns[key]['quantity']
                    }

            print(f'gems: {self.user_gems[user_jid]}')
        
        return msg + '\n say "!cut <gem_key>" to cut a gem.\n or just say cut to automatically cut the first gem in your inventory.'

    def cut_gem(self, user_jid):
        # self.player_status[user_jid]['depth'] += 1
        # if self.player_status[user_jid]['depth'] >= 5:
        #     return 'cut success'
        luck_multiplier = 1 + 0.1 * self.player_status[user_jid]['luck'] 
        self.instance_drops[user_jid]['gem broke'] = int((40**2) * math.pow(luck_multiplier, -1))
        outcome = random.choices(list(self.instance_drops[user_jid].keys()), weights=list(self.instance_drops[user_jid].values()))
        outcome = str(outcome[0])
        # print(f'{outcome}, {self.player_status[user_jid]['depth']}, {self.instance_drops[user_jid]}')
        if outcome == 'gem broke':
            return 'gem broke'
        else:
            return 'cut success'

    def item_registry(self, user_jid, command_parts):

        print(f'item_registry command: {command_parts}')
        user_title = database.get_user_data(jid=user_jid, table='set_user_data')['title']

        if len(command_parts) < 2:
            with open("data_storage/id_sys1.txt","r") as f:
                example = f.read()
            return example
        

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
                message = f"registry results: Key\\Name\\Price\n"
                for item in items:
                    message += f"{item} ,{items[item]['item_name']}, {items[item]['item_price']}\n"
                    print(f"item: {items[item]}")
                return message                 
            
        elif 'all' in command_parts:
            if user_title == 'owner':
                items = database.get_all_items(table_name='item_registry')
                if items:
                    return f"Items:\n {items}"
                else:
                    return "No items in the registry."
            else:
                return "You do not have permission to use this command."
                    
        elif 'add' == command_parts[1] and user_title == 'owner':
                return "the add command should be as follows: !registry add <#02-01-01-01> <item name> <item descreiption> <item price>"     
                
        elif 'add' == command_parts[1] and user_title == 'owner':
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
                self.client.send_chat_message('your_main_jid_here', f'transaction with the id: {segments[4]} has been added to the temp registry.')
                return f"Item with id tag {id_tag} added to the registry."
        
    def items_in_auction(self, user_jid, command_parts):
        print(f'items_in_auction command: {command_parts}')
        # user_title = database.get_user_data(user_jid, 'set_user_data')['title']
        items = database.get_auction_registry()
        if items:
            return f"Items in auction: {items}"
        else:
            return "No items in auction."
        
    def bid_on_item(self, user_jid, command_parts):
        pass

    def show_Inventory(self, user_jid, command_args=None):
        user = database.get_user_data(user_jid, table='dashboard_prefrences')
        username = user[0]
        display_name = user[9]
        items = database.get_user_data(username, table='item_ownership')
        try:
            self.user_inventory[user_jid].clear()
        except:
            pass
        for name in user:
            print(f'all data {name}:')
        if items:
            for row in items:
                item_key = row[0]
                try:
                    key, id, name, description, price = database.check_item(item_key, 'item_registry', 'item_name')
                except TypeError:
                    print(f'item key: {item_key}')
                if user_jid not in self.user_inventory:
                    self.user_inventory[user_jid] = {}
                self.user_inventory[user_jid][item_key] = {
                    'item_id': id,
                    'item_name': name,
                    'item_description': description,
                    'item_quantity': row[3],
                    'item_price': price,
                    'item_perk': row[4],
                    'item_perk_value': row[5]+row[7],
                    'equipped': row[8]
                }
            if not command_args:
                return f"i have changed up the inventory command a bit. you can now say '!inventory keys' to get a list of keys for your items, or you can say '!inventory <item_key>' to get the details of a specific item. i amd also working on a way to display the items in a more user friendly way. please be patient." 
            
            if command_args == 'keys' or command_args == 'key':
                keys = 'keys: \n'
                for key in self.user_inventory[user_jid].keys():
                    keys += f"{key} , {self.user_inventory[user_jid][key]['item_name']}, {self.user_inventory[user_jid][key]['item_quantity']} \n"
                return keys
            elif command_args:
                message = f'{display_name}\'s Inventory:\n'
                item = self.user_inventory[user_jid][command_args]
                for key in item:
                    message += f"{key}: {item[key]}\n"
                return message
            else:
                return f"you do not have any items in your inventory."

    def show_dashboard(self, user_jid=None, group_jid=None):
        separator = colored("--------------------------------------------------------", "cyan")
        set_user_data = database.get_user_data(user_jid, table='set_user_data')
        username = set_user_data['username']
        user = database.get_user_data(username, table='dashboard_prefrences')
        dict = self.get_data_from_raw(user_jid)
        components = self.get_player_stats(user_jid)
        print(colored(f"updated username: {username}", 'green'))
        if user:
            try:
                display_name = user[9]
                picture_link = dict[2]
                display_name = self.remove_unwanted_chars(display_name)
            except Exception as e:
                print(colored(f"Error: {e}, user type: {type(user)}", 'green'))

            print(colored({f'this is the user data: {type(user)}, {user[0]}'}, 'green'))
            color = (user['box_red'], user['box_green'], user['box_blue'], user['box_alpha'])
            print(colored(f"username: {username}, display_name: {display_name}, user existing user is true", 'green'))
            self.create_and_paste_image(username, picture_link, box_color=color, pfpx=user['pfpx'], pfpy=user['pfpy'], pfp_size=user['pfp_size'])
            # self.client.send_chat_image(group_jid, "images/final_products/final_image_with_box.png")
            image_base = Image.open("images/final_products/final_image_with_box.png")
            draw = ImageDraw.Draw(image_base)
            font = ImageFont.truetype("arial.ttf", 70)
            wrapped_name = textwrap.wrap(display_name, width=17)
            name_y = 40
            for line in wrapped_name:
                draw.text((50, name_y), line, (255, 255, 255), font=font)
                name_y += 55
            font = ImageFont.truetype("arial.ttf", 50)
            barx, bary = 60, 230
            for item in components:
                draw.text((barx, bary), f"{item}: {components[item]}", (0, 0, 0), font=font)
                bary += 100
            # ...

            # Calculate the width and height of the text box
            box_width = 400
            box_height = 400

            # Wrap the bio text to fit within the box width
            font = ImageFont.truetype("arial.ttf", 40)

            wrapped_bio = textwrap.wrap(user['bio'], width=20)

            # Draw the text box
            barx, bary = 560, 400
            # draw.rectangle([(barx, bary), (barx + box_width, bary + box_height)], outline=(0, 0, 0))

            # Draw the wrapped bio text
            text_y = bary + 10
            for line in wrapped_bio:
                draw.text((barx, text_y), line, (0, 0, 0), font=font)
                text_y += 45
            image_base.save("images/final_products/temp_dashboard.png")
            if group_jid:
                self.client.send_chat_image(group_jid, "images/final_products/temp_dashboard.png")
            else:
                self.client.send_chat_image(user_jid, "images/final_products/temp_dashboard.png")

        else:
            try:
                display_name = str(dict[1])
                picture_link = dict[2]
                display_name = self.remove_unwanted_chars(display_name)
            except Exception as e:
                print(colored(f"Error: {e}, user type: {type(user)}", 'green'))
            print(colored(f"username: {username}, display_name: {display_name}, user existing user is false", 'green'))
            # database.update_user_data(user_jid, '', 'nickname', display_name)
            # self.client.send_chat_message(group_jid, "seems like you do not have a dashboard set up. sit tight while we get that sorted out for you.")
            database.generate_dashboard_data(username, display_name)
            time.sleep(1)
            self.show_dashboard(user_jid, group_jid)
        print(f'dashboard command end: {separator}')

    def link_to_user(self, user_jid, group_jid, tag='check_id'):
        if not database.get_user_data(user_jid, table='set_user_data'):
            self.client.send_chat_message(group_jid, 'click: >>> @mc_twin\nthen say: \'link\'\nthen come back here and say: \'!connect blahblah\'')
            return False
        elif tag == 'return_username':
            print(f'user_jid: {user_jid}')
            return database.get_user_data(user_jid, table='set_user_data')['username']
        else:
            return True
            
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

    def remove_unwanted_chars(self, text):
        # The regular expression pattern to match
        pattern = r'\\x[0-9a-fA-F]+'
        
        # Use re.sub() to replace the matched patterns with an empty string
        cleaned_text = re.sub(pattern, '', text)
        
        return cleaned_text    
    
    def get_user_profile(self, image_url, folder_path='c:/Users/holyk/Desktop/code/kikbot-blackjackbot/images/temp'):
        # Create the folder if it doesn't exist
        os.makedirs(folder_path, exist_ok=True)

        # Send a GET request to download the image
        response = requests.get(image_url)

        # Extract the filename from the URL
        filename = os.path.basename(image_url)

        # Save the image to the specified folder
        image_path = os.path.join(folder_path, filename)
        with open(image_path, "wb") as file:
            file.write(response.content)
        return Image.open(image_path)

    def get_player_stats(self, user_jid):
        set_user_data = database.get_user_data(user_jid, table='set_user_data')
        print(set_user_data)
        username = set_user_data['username']
        title = set_user_data['title']
        currency = set_user_data['currency_balance']
        stats = database.get_user_data(username, table='item_ownership', equipped=True)
        luck = 0
        stamina = 50
        health = 100
        defense = 0
        attack = 10
        agility = 10
        if stats:
            for item in stats:
                if item[4] == 'Luck':
                    luck += item[5]
                if item[6] == 'Luck':
                    luck += item[7]
                if item[4] == 'Stamina':
                    stamina += item[5]
                if item[6] == 'Stamina':
                    stamina += item[7]
                if item[4] == 'Health':
                    health += item[5]
                if item[6] == 'Health':
                    health += item[7]
                if item[4] == 'Defense':
                    defense += item[5]
                if item[6] == 'Defense':
                    defense += item[7]
                if item[4] == 'Attack':
                    attack += item[5]
                if item[6] == 'Attack':
                    attack += item[7]
                if item[4] == 'Agility':
                    agility += item[5]
                if item[6] == 'Agility':
                    agility += item[7]
        components = {
            'Title': title,
            'coins': currency,
            'luck': luck,
            'stamina': stamina,
            'Hp\\Def': f'{health}/{defense}',
            'attack': attack,
            'agility': agility,
        }
        return components
        
    def create_and_paste_image(self, user, image_url, box_color='white', pfpx=650, pfpy=50, pfp_size=300):
        
        path = database.get_user_data(user, table='dashboard_prefrences')['background_path']
        
        if path != 'not-set' and os.path.exists(path):
            random_image = Image.open(path)
            random_image = random_image.filter(ImageFilter.BLUR())
        else:
            image_files = glob.glob("images/backgrounds/*.jpg")
            random_image_file = random.choice(image_files)
            random_image = Image.open(random_image_file)
            random_image = random_image.filter(ImageFilter.BLUR())

        hex_guide = Image.open("images/guides/Untitled96_20240218160236.png")
        hex_guide = hex_guide.resize((pfp_size, pfp_size))

        box_guide = Image.open("images/guides/Untitled98_20240219153934.png").convert("RGBA")

        if not box_color == 'white':
            # box_guide = box_guide.convert("RGBA")
            box_guide_data = box_guide.getdata()
            new_box_guide_data = []
            for item in box_guide_data:
                # Set the color of white pixels to the specified box_color
                if item[:3] == (255, 255, 255):
                    new_box_guide_data.append((box_color[0], box_color[1], box_color[2], box_color[3]))
                elif item[:3] == (0, 0, 0):
                    new_box_guide_data.append((item[0], item[1], item[2], 0))
                else:
                    new_box_guide_data.append(item)
            box_guide.putdata(new_box_guide_data)
            
        else:
            box_guide = box_guide.convert("L")

        profile_picture = self.get_user_profile(image_url)
        profile_picture = profile_picture.resize((pfp_size, pfp_size)).convert("RGBA")

        # Crop the image to a 1:1 ratio
        width, height = random_image.size
        if width > height:
            left = (width - height) // 2
            right = left + height
            top = 0
            bottom = height
        else:
            top = (height - width) // 2
            bottom = top + width
            left = 0
            right = width

        cropped_image = random_image.crop((left, top, right, bottom))

        # Resize the cropped image to 1000x1000
        random_background = cropped_image.resize((1000, 1000)).convert("RGBA")
        random_background.save("images/final_products/random_background.png")

        # Open the original image
        # mask = Image.new('RGBA', (300, 300), )
        

        profile_picture.paste(hex_guide, (0, 0), mask=hex_guide)
        # Convert all white pixels to transparent
        profile_picture = profile_picture.convert("RGBA")
        data = profile_picture.getdata()
        new_data = []
        for item in data:
            # Set the alpha value to 0 for white pixels
            if item[:3] == (255, 255, 255):
                new_data.append((255, 255, 255, 0))
            else:
                new_data.append(item)
        profile_picture.putdata(new_data)
        profile_picture.save("images/final_products/profile_picture.png")

        random_background.paste(box_guide, (0, 0), mask=box_guide)

        random_background.paste(profile_picture, (pfpx, pfpy), mask=profile_picture)
        # profile_picture.paste(random_background, (x, y))

        random_background.save("images/final_products/final_image_with_box.png")
        
    def get_data_from_raw(self, jid):
            separator = colored("--------------------------------------------------------", "cyan")

            try:
                print('catching stdout')

                buffer = io.StringIO()
                data = ''
                original_stdout = sys.stdout

                sys.stdout = buffer
                self.client.request_info_of_users(jid)

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
                        break

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
                    return username, display_name, picture_link
                except Exception as e:
                    self.client.send_chat_message(jid, f"Failed to extract user information: {e}")
                # self.client.send_chat_message(jid, f'raw3: {data}')
                # Redirect stdout back to the terminal
                print(separator)
                    
            except Exception as e:
                self.client.send_chat_message(jid, f'Failed to get user data.: {e}')

    def generate_beta_items(self,user_jid):
        print('generate_beta_items')
        items = [
            {
                'id_tag': '#02-01-07-03',
                'item_name': 'beta helmet',
                'item_description': 'this is a beta helmet',
                'item_price': '69420'
            },
            {
                'id_tag': '#02-02-07-03',
                'item_name': 'beta chestplate',
                'item_description': 'this is a beta chestplate',
                'item_price': '69420'
            },
            {
                'id_tag': '#02-03-07-03',
                'item_name': 'beta leggings',
                'item_description': 'these are beta leggings',
                'item_price': '69420'
            },
            {
                'id_tag': '#02-04-07-03',
                'item_name': 'beta boots',
                'item_description': 'these are beta boots',
                'item_price': '69420'
            },
            {
                'id_tag': '#02-05-07-03',
                'item_name': 'beta gloves',
                'item_description': 'these are beta gloves',
                'item_price': '69420'
            },
            {
                'id_tag': '#02-06-07-03',
                'item_name': 'beta bracers',
                'item_description': 'these are beta bracers',
                'item_price': '69420'
            },
            {
                'id_tag': '#02-07-07-03',
                'item_name': 'beta mask',
                'item_description': 'this is a beta mask',
                'item_price': '69420'
            },
            {
                'id_tag': '#02-08-07-03',
                'item_name': 'beta shoulderwear',
                'item_description': 'this is beta shoulderwear',
                'item_price': '69420'
            },
            {
                'id_tag': '#02-09-07-03',
                'item_name': 'beta cloak',
                'item_description': 'this is a beta cloak',
                'item_price': '69420'
            }
        ]
        for item in items:
            transaction =  database.generate_transaction('self',user_jid, item['item_name'], 1)
            database.add_item_temp(transaction, item['id_tag'], item['item_name'], item['item_description'], item['item_price'])
            time.sleep(.1)
            msg = database.authorize_item_creation(transaction)
        self.client.send_chat_message(user_jid, msg)
        print('generate_beta_items end')
    
    def give(self, user_jid, recipient, item, amount ):
        database.generate_transaction('gift', user_jid, item, amount, recipient)
        if item == 'coins':
            initiator_coin_balance = database.get_user_data(user_jid, table='set_user_data')['currency_balance']
            recipient_coin_balance = database.get_user_data(recipient, 'set_user_data')['currency_balance']
            database.update_user_data(user_jid, 'set_user_data', 'currency_balance', initiator_coin_balance - amount, recipient)
            database.update_user_data(recipient, 'set_user_data', 'currency_balance', recipient_coin_balance + amount, recipient)
            return
        item_key, item_id, item_name, item_description, item_price = database.check_item(item_name=item)
        user_owned = database.get_user_data(user_jid, item_key, table='item_ownership')
        owned = database.get_user_data(recipient, item_key, table='item_ownership')
        if user_owned:
            if int(user_owned[0][3]) - amount == 0:
                database.delete_item_from_inventory(item_key, user_jid)
                database.update_user_data(user_jid, 'item_ownership', 'quantity', owned[0][3] - amount, item_key)
                database.update_user_data(recipient, 'item_ownership', 'quantity', owned[0][3] - amount, item_key)
                return
            if owned[0][3] - amount < 0:
                return f'You do not have enough of this item to give {amount} to {recipient}.'
        else:
            database.add_item_to_inventory(item_key, item_id, user_jid, amount, item_price)

    def sell(self, user_jid, item_key, amount):    
        item_key, item_id, item_name, item_description, item_price = database.check_item(item_key, 'item_registry')
        user_owned = database.get_user_data(user_jid, item_key, table='item_ownership')
        user_data = database.get_user_data(user_jid, table='set_user_data')
        total_price = int((float(item_price * amount) * 0.7))
        auction_owned = database.get_user_data('your_main_jid_here', item_key, 'item_ownership')
        auction_data = database.get_user_data('your_main_jid_here', table = 'set_user_data')
        for item in auction_owned[0]:
            print(f'auction_owned: {item}')
        for item in auction_data:
            print(f'auction_data: {item}')  
        if user_owned:
            if int(user_owned[0][3]) - amount == 0:
                database.generate_transaction('sell', user_jid, item_name, amount, 'your_main_jid_here', 'coins', total_price)
                database.delete_item_from_inventory(item_key, user_jid)
                database.update_user_data(user_jid, 'set_user_data', 'currency_balance', user_data[6] + total_price)
                if auction_owned:
                    database.update_user_data('your_main_jid_here', 'item_ownership', 'quantity', auction_owned[0][3] + amount, item_key)
                    database.update_user_data('your_main_jid_here', 'set_user_data', 'currency_balance', auction_data[6] - total_price)
                else:
                    database.add_item_to_inventory(item_key, item_id, 'your_main_jid_here', amount, item_price)
                    database.update_user_data('your_main_jid_here', 'set_user_data', 'currency_balance', auction_data[6] - total_price)
                return f'e1 you have sold {amount} {item_name} for {total_price} coins.'
            elif int(user_owned[0][3]) - amount > 0:
                database.generate_transaction('sell', user_jid, item_name, amount, 'your_main_jid_here', 'coins', total_price)
                database.update_user_data(user_jid, 'item_ownership', 'quantity', int(user_owned[0][3]) - amount, item_key)
                database.update_user_data(user_jid, 'set_user_data', 'currency_balance', user_data[6] + total_price)
                if auction_owned:
                    database.update_user_data('your_main_jid_here', 'item_ownership', 'quantity', auction_owned[0][3] + amount, item_key)
                    database.update_user_data('your_main_jid_here', 'set_user_data', 'currency_balance', auction_data[6] - total_price)
                else:
                    database.add_item_to_inventory(item_key, item_id, 'your_main_jid_here', amount, item_price)
                    database.update_user_data('your_main_jid_here', 'set_user_data', 'currency_balance', auction_data[6] - total_price)
                return f'e2 you have sold {amount} {item_name} for {total_price} coins.'
            elif int(user_owned[0][3]) - amount < 0:
                return f'e3 You do not have enough of this item to sell {amount}.'
            
        else:
            # database.add_item_to_inventory(item_key, item_id, user_jid, amount, item_price)
            print('wut... how did you get here?')
        print(f'item_key: {item_key}, item_id: {item_id}, item_name: {item_name}, item_description: {item_description}, item_price: {item_price}, user_jid: {user_jid}, amount: {amount}, total_price: {total_price}')
        return f'e4 um.....what? try these.\n !sell <item_key> <amount>'

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

        try:
            if self.player_status[user_jid]:
                print('user status exists')
        except:
            self.player_status[user_jid] = {
                'depth': 0,
                'status': 'idle',
                'energy': 50,
                'luck': 0,
                'hp': 100,
                'defense': 0,
                'attack': 10,
                'speed': 5
            }
            
        if self.player_status[user_jid]['status'] == 'mining':
            if command in ['left', 'right', 'center']:
                msg = self.mine(user_jid, command)
                if self.player_status[user_jid]['status'] == 'no_energy':
                    self.client.send_chat_message(user_jid, "You have run out of energy and have exited the mine.")
                    self.player_status[user_jid]['status'] = 'idle'
                    print(f'player loot: {self.player_loot[user_jid]}')
                    for item in self.player_loot[user_jid]:
                        database.generate_transaction('mining game', user_jid, item, self.player_loot[user_jid][item])
                        item_key, item_id, item_name, item_description, item_price = database.check_item(item_name=item)
                        owned = database.get_user_data(user_jid, item_key=item_key, table='item_ownership')
                        if owned:
                            database.update_user_data(user_jid, 'item_ownership', 'quantity', owned[0][3] + self.player_loot[user_jid][item], item_key)
                        else:
                            database.add_item_to_inventory(item_key, item_id, user_jid, self.player_loot[user_jid][item], item_price)
                else:
                    self.client.send_chat_message(user_jid, msg)
            elif command in ['exit', '!exit' 'leave']:
                self.player_status[user_jid]['status'] = 'idle'
                print(f'player loot: {self.player_loot[user_jid]}')
                for item in self.player_loot[user_jid]:
                    database.generate_transaction('mining game', user_jid, item, self.player_loot[user_jid][item])
                    item_key, item_id, item_name, item_description, item_price = database.check_item(item_name=item)
                    owned = database.get_user_data(user_jid, item_key=item_key, table='item_ownership')
                    print(f'owned: {owned}')
                    if owned:
                        for i in owned[0]:
                            print(f'owned: {i}')
                        database.update_user_data(user_jid, 'item_ownership', 'quantity', owned[0][3] + self.player_loot[user_jid][item], item_key)
                    else:
                        database.add_item_to_inventory(item_key, item_id, user_jid, self.player_loot[user_jid][item], item_price)
                self.client.send_chat_message(user_jid, "you have exit the mine.")
            else:
                self.client.send_chat_message(user_jid, "You are currently mining. Please finish mining or say \'exit\' before using other commands.")
            return
        
        if self.player_status[user_jid]['status'] == 'in_combat':
            pass

        if self.player_status[user_jid]['status'] == 'cutting gems':
            if command == "!inventory":
                if len(command_parts) > 1:
                    self.client.send_chat_message(user_jid, self.show_Inventory(user_jid, command_parts[1]))
                else:
                    self.client.send_chat_message(user_jid, self.show_Inventory(user_jid))
                return
            if command in ['exit', 'leave', 'stop']:
                self.player_status[user_jid]['status'] = 'idle'
                self.client.send_chat_message(user_jid, "you have stopped cutting gems.")
                return
            # try:
            if len(command_parts) > 1:
                if command_parts[1].lower() in [gem.lower() for gem in list(self.total_rates.keys())]:
                    print('gem change detected')
                    for key in self.user_gems[user_jid].keys():
                        if self.user_gems[user_jid][key]['name'].lower() == command_parts[1].lower():
                            try:
                                self.instance_drops[user_jid].pop(list(self.instance_drops[user_jid].keys())[1])
                            except:
                                pass
                            self.instance_drops[user_jid][key] = self.total_rates[self.user_gems[user_jid][key]['name']] 
                            self.client.send_chat_message(user_jid, f'you have selected {self.user_gems[user_jid][key]["name"]} to cut.')
                    print(f'user gems: {self.user_gems[user_jid]}')
                    print(f'instance drops: {self.instance_drops[user_jid]}')        
                    return
            # except:
            #     print('error in gem change detected')

            if command == 'cut':
                print(f'instance drops: {self.instance_drops[user_jid]}')
                # if self.user_gems[user_jid]:
                if len(self.instance_drops[user_jid]) <= 1:
                    gem = list(self.user_gems[user_jid].keys())[0]
                    if self.user_gems[user_jid][gem]['quantity'] <= 0:
                        self.user_gems[user_jid][gem]['quantity'].pop(0)
                        gem = list(self.user_gems[user_jid].keys())[0]
                    self.instance_drops[user_jid][gem] = self.total_rates[self.user_gems[user_jid][gem]['name']] 
                else:
                    gem = list(self.instance_drops[user_jid].keys())[1]   
                    if self.user_gems[user_jid][gem]['quantity'] <= 0:
                        self.user_gems[user_jid][gem]['quantity'].pop(0)
                        gem = list(self.user_gems[user_jid].keys())[0]
                    gem = list(self.instance_drops[user_jid].keys())[1]   
                print(f'gem: {gem}')
                num_of_cuts = (int(self.user_gems[user_jid][gem]['Id'][8])-1) * 4
                msg = 'cutting gem...\n'
                for i in range(num_of_cuts):
                    status = self.cut_gem(user_jid)
                    if status == 'gem broke':
                        msg += f'the {self.user_gems[user_jid][gem]['name']} shatters...'
                        self.client.send_chat_message(user_jid, msg)
                        database.generate_transaction('cutting gems', user_jid, gem, -1)
                        print(colored(f'gem: {gem}', 'yellow'))
                        database.update_user_data(user_jid, 'item_ownership', 'quantity', self.user_gems[user_jid][gem]['quantity'] - 1, gem)
                        time.sleep(.2)
                        self.user_gems[user_jid][gem]['quantity'] -= 1

                        return
                    else:
                        msg += f'the {self.user_gems[user_jid][gem]['name']} shimmers, you press on.\n'
                else:
                    msg += f'you have finished cutting the {self.user_gems[user_jid][gem]['name']}.'
                    new_gem = database.check_item(item_name=('Cut ' + self.user_gems[user_jid][gem]['name']))
                    database.generate_transaction('cutting gems', user_jid, gem, -1, user_jid, new_gem[2], 1)
                    old_gem_quantity = database.get_user_data(user_jid, item_key=gem, table='item_ownership')
                    if old_gem_quantity[0][3] - 1 == 0:
                        database.delete_item_from_inventory(gem, user_jid)
                    else:
                        database.update_user_data(user_jid, 'item_ownership', 'quantity', old_gem_quantity[0][3] - 1, gem)
                    print(colored(f'key: {new_gem[0]}, id: {new_gem[1]}, name: {new_gem[2]}', 'green'))
                    new_gem_quantity = database.get_user_data(user_jid, item_key=new_gem[0], table='item_ownership')
                    if new_gem_quantity:
                        database.update_user_data(user_jid, 'item_ownership', 'quantity', new_gem_quantity[0][3] + 1, new_gem[0])
                    else:
                        database.add_item_to_inventory(new_gem[0], new_gem[1], user_jid, 1, new_gem[3])
                    self.user_gems[user_jid][gem]['quantity'] -= 1                    
                    self.client.send_chat_message(user_jid, msg)
                    return
            else:
                self.client.send_chat_message(user_jid, "You are currently cutting gems. Please finish cutting or say \'stop\' before using other commands.")
                return

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
                self.client.send_chat_message(chat_message.from_jid, f'your unique_id links you to your inventory in the group chat of your choice.\n in order for this to work, copy your unique_id then go to an unlinked chat has the auction house and say !connect [unique_id]\n for example: !connect 98wgf98ey4g9e.')
                self.client.send_chat_message(chat_message.from_jid, f'!connect {unique_id}')
            else:
                self.client.send_chat_message(chat_message.from_jid, "sorry, you do not have a unique_id. please contact the auction house owner for assistance.")

        if command == '!transaction':
            msg = database.generate_transaction(user_jid, command_parts)
            self.client.send_chat_message(chat_message.from_jid, msg)

        if command == 'pfp3':
            username, display_name, picture_link = self.get_data_from_raw(chat_message.from_jid)
            self.client.send_chat_message(chat_message.from_jid, f"Username: {username}\nDisplay Name: {display_name}\nPicture Link: {picture_link}")

        if command == "!dashboard":
            if len(command_parts) == 1:
                file_path = "data_storage/dashboard.txt"

                with open(file_path, "r") as file:
                    file_contents = file.read()

                # Now you can send the file contents as needed
                # For example, you can print it to the console
                self.client.send_chat_message(chat_message.from_jid, file_contents)
            if len(command_parts) > 1:
                if command_parts[1] == 'box_color':
                    colors = {
                        'box_red': command_parts[2],
                        'box_green': command_parts[3], 
                        'box_blue': command_parts[4], 
                        'box_alpha': command_parts[5]
                    }
                    for column in colors:
                        database.update_user_data(user_jid, 'dashboard_prefrences', column, colors[column])
                    self.client.send_chat_message(chat_message.from_jid, "box color updated to: " + str(colors))
                if command_parts[1] == 'pfp':
                    pfp = {
                        'pfpx': command_parts[2],
                        'pfpy': command_parts[3],
                        'pfp_size': command_parts[4]
                    }
                    for column in pfp:
                        database.update_user_data(user_jid, 'dashboard_prefrences', column, pfp[column])
                    self.client.send_chat_message(chat_message.from_jid, "pfp updated to: " + str(pfp))
                if command_parts[1] == 'nickname' or command_parts[1] == 'display_name':    
                    nickname = ''
                    for i in range(2, len(command_parts)):
                        nickname += f'{command_parts[i]} '
                    print(nickname)
                    nickname = self.remove_unwanted_chars(nickname)
                    database.update_user_data(user_jid, 'dashboard_prefrences', 'display_name', nickname)
                    self.client.send_chat_message(chat_message.from_jid, "nickname updated to: " + nickname)
                if command_parts[1] == 'bio':

                    bio = ''
                    for i in range(2, len(command_parts)):
                        bio += f'{command_parts[i]} '
                    database.update_user_data(user_jid, 'dashboard_prefrences', 'bio', bio)
                    self.client.send_chat_message(chat_message.from_jid, "bio updated to: " + bio)

                if command_parts[1] == 'background':
                    # if len(command_parts) == 2:
                    self.background_requests[user_jid] = True
                    self.client.send_chat_message(chat_message.from_jid, "cool i\'ll create a background request for you...\n\n\n\n\n now just send me the pic you want as your background and i\'ll take care of the rest.")
 
        if command == '!fill':
            self.generate_beta_items(user_jid)
        
        if command == '!mine':
            if self.player_status[user_jid]['status'] != 'mining' and self.player_status[user_jid]['status'] != 'in_combat':
                components = self.get_player_stats(user_jid)
                stamina = components['stamina']
                self.client.send_chat_message(user_jid, self.start_mining(user_jid, energy=stamina))
            return
                
        if command == '!cutgems' or command == '!cut':
            user_title = database.get_user_data(jid=user_jid, table='set_user_data')['title']
            print(f'user_title: {user_title}')
            # if not user_title in ['Jewler', 'Alchemist']:
            #     self.client.send_chat_message(user_jid, "You must be a jewler or alchemist to cut gems.")
            #     return
            if self.player_status[user_jid]['status'] != 'cutting gems':
                self.client.send_chat_message(user_jid, self.start_cutting_gems(user_jid))
                return
                
        if command == "!inventory":
                if len(command_parts) > 1:
                    self.client.send_chat_message(user_jid, self.show_Inventory(user_jid, command_parts[1]))
                else:
                    self.client.send_chat_message(user_jid, self.show_Inventory(user_jid))

        if command == "!bet":
            if len(command_parts) == 1:
                with open("data_storage/bet.txt","r") as f:
                    self.client.send_chat_message(user_jid, f.read())
                    return
            
            if len(command_parts) == 2 and command_parts[1].isdigit():
                balance = database.get_user_data(user_jid, table= 'set_user_data')['currency_balance']
                if balance == 0:
                    self.client.send_chat_message(user_jid, "You do not have any coins to bet.")
                    return
                if balance - int(command_parts[1]) < 0:
                    self.client.send_chat_message(user_jid, f"You do not have enough coins to make a bet of {command_parts[1]}")
                    return
                else:
                    result = random.choices(['lose', 'win'], weights=[0.6, 0.4], k=1)
                    if result[0] == 'win':
                        database.update_user_data(user_jid, 'set_user_data', 'currency_balance', balance + int(int(command_parts[1])*1.2))
                        self.client.send_chat_message(user_jid, f"You have won {command_parts[1]} coins. your new balance is {balance + int(int(command_parts[1])*1.2)}")
                    else:
                        database.update_user_data(user_jid, 'set_user_data', 'currency_balance', balance - int(command_parts[1]))
                        self.client.send_chat_message(user_jid, f"You have lost {command_parts[1]} coins. your new balance is {balance - int(command_parts[1])}")
                return
            else:
                self.client.send_chat_message(user_jid, "You must provide a number to bet, item bets come later.")
                return

        if command == '!message':
            target = command_parts[1]
            message = ''
            for i in range(2, len(command_parts)):
                message += f'{command_parts[i]} '
            self.client.send_chat_message(target, message)
        
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
                user_jid = database.get_user_data(user_jid, table='set_user_data')['username']
                if len(command_parts) > 1:
                    Inventory_message = self.show_Inventory(user_jid, command_parts[1])
                    self.client.send_chat_message(group_jid, Inventory_message)
                else:
                    Inventory_message = self.show_Inventory(user_jid)
                    self.client.send_chat_message(group_jid, Inventory_message)

        if command == "!dashboard":
            if self.link_to_user(user_jid, group_jid):
                if len(command_parts) == 1:
                    self.show_dashboard(user_jid, group_jid)
                else:
                    self.client.send_chat_message(group_jid, "whoops. edit your dashboard settings in dm.")
        
        if command == "!trade":
            if len(command_parts) == 1:
                with open("data_storage/trade.txt","r") as f:
                    self.client.send_chat_message(group_jid, f.read())
            elif self.link_to_user(user_jid, group_jid):
                trade_message = self.trade(user_jid, command_parts)
                self.client.send_chat_message(group_jid, trade_message)

        if command == "!give":
            if len(command_parts) == 1:
                with open("data_storage/give.txt","r") as f:
                    self.client.send_chat_message(group_jid, f.read())
                    return
            initiator = self.link_to_user(user_jid, group_jid)
            recipient = database.get_user_data(command_parts[1], table='set_user_data')['useername']
            item =  command_parts[2]
            amount = command_parts[3]

            if recipient and item and amount:
                give_message = self.give(initiator, recipient, item, amount)
                self.client.send_chat_message(group_jid, give_message)
            elif not recipient:
                all_users  = database.get_all_items('new_user_data', raw=True)
                unmatched_users = []
                list_of_users = ''
                for group in all_users:
                    if group[1] == group_jid:
                        unmatched_users.append(group[0])
                for user in unmatched_users:
                    person = database.get_user_data(user, table='set_user_data')['useername']
                    if person:
                        list_of_users += f'{person}\n'
    
                self.client.send_chat_message(group_jid, "You must provide a recipient.")
            elif not item:
                self.client.send_chat_message(group_jid, "You must provide an item.")
            elif not amount:
                self.client.send_chat_message(group_jid, "You must provide an amount.")

        if command == "!sell":  
            username = self.link_to_user(user_jid, group_jid, tag = 'return_username')
            if len(command_parts) == 1:
                with open("data_storage/sell.txt","r") as f:
                    self.client.send_chat_message(group_jid, f.read())
                    return
            item_key = command_parts[1]
            amount = int(command_parts[2])
            sell_message = self.sell(username, item_key, amount)
            self.client.send_chat_message(group_jid, sell_message)

        if command == "!bet":
            if len(command_parts) == 1:
                with open("data_storage/bet.txt","r") as f:
                    self.client.send_chat_message(group_jid, f.read())
                    return
                
            username = self.link_to_user(user_jid, group_jid, tag = 'return_username')
            if not username:
                return
            
            self.bets += 1
            print(f'bets: {self.bets}')
            current_time = time.time()
            minutes_since_last_bet = int((current_time - self.minute_time)/60)

            if self.bets < 0:
                self.bets = 0
            if  minutes_since_last_bet > 1:
                if minutes_since_last_bet > self.bets:
                    self.bets -= minutes_since_last_bet
                    self.minute_time = time.time()
                else:
                    self.bets = 0
                    self.minute_time = time.time()
            if self.bets >= 5:
                self.client.send_chat_message(group_jid, "woah... you guys.. don't spam chat plz. if you wanna bet, just say !bet [amount] in dms with me. YESSS, I'm talking to you, you know who you are.")
                return
            
            if len(command_parts) == 2 and command_parts[1].isdigit():
                balance = database.get_user_data(username, table= 'set_user_data')['currency_balance']
                if balance == 0:
                    self.client.send_chat_message(user_jid, "You do not have any coins to bet.")
                    return
                print(f'bets: {self.bets}')
                if balance - int(command_parts[1]) < 0:
                    self.client.send_chat_message(group_jid, f"You do not have enough coins to make a bet of {command_parts[1]}")
                    return
                else:
                    result = random.choices(['lose', 'win'], weights=[0.5, 0.5], k=1)
                    if result[0] == 'win':
                        database.update_user_data(username, 'set_user_data', 'currency_balance', balance + int(int(command_parts[1])*1.2))
                        self.client.send_chat_message(group_jid, f"You have won {command_parts[1]} coins. your new balance is {balance + int(int(command_parts[1])*1.2)}")
                    else:
                        database.update_user_data(username, 'set_user_data', 'currency_balance', balance - int(command_parts[1]))
                        self.client.send_chat_message(group_jid, f"You have lost {command_parts[1]} coins. your new balance is {balance - int(command_parts[1])}")
                return  
                     
            
            if len(command_parts) == 2 and command_parts[1].lower() == 'all':
                balance = database.get_user_data(username, table= 'set_user_data')['currency_balance']
                print(f'balance: {balance}')
                if balance <= 0:
                    # self.client.send_chat_message(group_jid, "you got 1000.")
                    # database.update_user_data(username, 'set_user_data', 'currency_balance', 1000)
                    balance = 1000
                else:
                    result = random.choices(['lose', 'win'], weights=[0.5, 0.5], k=1)
                    if result[0] == 'win':
                        database.update_user_data(username, 'set_user_data', 'currency_balance', balance + int(balance*1.2))
                        self.client.send_chat_message(group_jid, f"You have won {int(balance*1.2)} coins. your new balance is {balance + int(balance*1.2)}")
                    else:
                        database.update_user_data(username, 'set_user_data', 'currency_balance', balance - balance)
                        self.client.send_chat_message(group_jid, "You have lost all of your coins. whomp whomp.")
                return
            else:
                self.client.send_chat_message(group_jid, "You must provide a number to bet, item bets come later.")
                return

        if command == "!sparechange":
            username = self.link_to_user(user_jid, group_jid, tag = 'return_username')
            if not username:
                return
            # if len(command_parts) == 1:
            #     with open("data_storage/sparechange.txt","r") as f:
            #         self.client.send_chat_message(group_jid, f.read())
            #         return
            balance = database.get_user_data(username, table= 'set_user_data')['currency_balance']
            if balance < 1000:
                self.client.send_chat_message(group_jid, "you got 1000.")
                database.update_user_data(username, 'set_user_data', 'currency_balance', 1000)
            else:
                self.client.send_chat_message(group_jid, "BREH. You asked for it.")
                database.update_user_data(username, 'set_user_data', 'currency_balance', 1000)
       
        if command == "help" or command == "commands" or command == "!help":
            if len(command_parts) == 1:
                with open("data_storage/help.txt","r") as f:
                    self.client.send_chat_message(chat_message.group_jid, f.read())
                return
            elif command_parts[1] == '1' or command_parts[1] == 'bid':
                with open("data_storage/bid.txt","r") as f:
                    self.client.send_chat_message(chat_message.group_jid, f.read())
                return
            elif command_parts[1] == '2' or command_parts[1] == 'dashboard':
                with open("data_storage/dashboard.txt","r") as f:
                    self.client.send_chat_message(chat_message.group_jid, f.read())
                return
            elif command_parts[1] == '3' or command_parts[1] == 'in_auction':
                with open("data_storage/in_auction.txt","r") as f:
                    self.client.send_chat_message(chat_message.group_jid, f.read())
                return
            elif command_parts[1] == '4' or command_parts[1] == 'inventory':
                with open("data_storage/inventory.txt","r") as f:
                    self.client.send_chat_message(chat_message.group_jid, f.read())
                return
            elif command_parts[1] == '5' or command_parts[1] == 'mine':
                with open("data_storage/mine.txt","r") as f:
                    self.client.send_chat_message(chat_message.group_jid, f.read())
                return
            elif command_parts[1] == '6' or command_parts[1] == 'registry':
                with open("data_storage/registry.txt","r") as f:
                    self.client.send_chat_message(chat_message.group_jid, f.read())
                return
            # elif command_parts[1] == '6' or command_parts[1] == '!transaction':
            #     with open("data_storage/transaction.txt","r") as f:
            #         self.client.send_chat_message(chat_message.group_jid, f.read())
            #     return
            # elif command_parts[1] == '7' or command_parts[1] == '!fill':
            #     with open("data_storage/fill.txt","r") as f:
            #         self.client.send_chat_message(chat_message.group_jid, f.read())
            #     return
            # elif command_parts[1] == '9' or command_parts[1] == '!connect':
            #     with open("data_storage/connect.txt","r") as f:
            #         self.client.send_chat_message(chat_message.group_jid, f.read())
            #     return
            elif command_parts[1] == '7' or command_parts[1] == 'extra':
                with open("data_storage/extra.txt","r") as f:
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
        
    def on_image_received(self, response: IncomingImageMessage):
        print("Image received!")
        separator = colored("--------------------------------------------------------", "cyan")
        group_message_header = colored("[+ IMAGE RECEIVED +]", "cyan")

        try:
            group_jid = response.group_jid
            user_jid = response.from_jid
        except:
            user_jid = response.from_jid
        url = response.image_url

        print(separator)
        print(group_message_header)
        print(colored(f"From AJID: {user_jid}", "yellow"))
        if group_jid:
            print(colored(f"From group: {group_jid}", "yellow"))
        else:
            print(colored(f"From group: was in dms silly.", "yellow"))
        print(colored(f"Image URL: {url}", "yellow"))
        print(separator)

        if user_jid in self.background_requests:
            # Get the filename from the from_jid
            filename = response.from_jid[:-13]

            # Create the directory if it doesn't exist
            directory = 'images/personal_backgrounds'
            os.makedirs(directory, exist_ok=True)

            # Download and save the image
            image_path = os.path.join(directory, f"{filename}.png")
            response = requests.get(url)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            database.update_user_data(user_jid, 'dashboard_prefrences', 'background_path', image_path)

            # Send a chat message in the group
            self.client.send_chat_message(user_jid, f"Image saved as {filename}.png")


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
