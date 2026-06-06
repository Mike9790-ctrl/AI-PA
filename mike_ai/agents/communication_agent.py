"""
MIKE AI - Communication Agent
Handles messaging across platforms: Telegram, KakaoTalk, WhatsApp, Email, Discord
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional
from pathlib import Path

class CommunicationAgent:
    """Agent for sending messages across multiple platforms"""
    
    def __init__(self, config_path: str = None):
        self.name = "Communication Agent"
        self.platforms = {
            'telegram': False,
            'kakao': False,
            'whatsapp': False,
            'email': False,
            'discord': False
        }
        self.config_path = config_path or "config/communication_config.json"
        self.message_history = []
        self.load_config()
    
    def load_config(self):
        """Load platform configurations"""
        config_file = Path(self.config_path)
        if config_file.exists():
            with open(config_file, 'r') as f:
                config = json.load(f)
                self.platforms.update(config.get('platforms', {}))
                self.credentials = config.get('credentials', {})
        else:
            self.credentials = {}
            self.save_config()
    
    def save_config(self):
        """Save platform configurations"""
        config_file = Path(self.config_path)
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config = {
            'platforms': self.platforms,
            'credentials': self.credentials,
            'last_updated': datetime.now().isoformat()
        }
        with open(config_file, 'w') as f:
            json.dump(config, f, indent=2)
    
    def setup_platform(self, platform: str, **kwargs):
        """
        Setup a messaging platform
        Supports: telegram, kakao, whatsapp, email, discord
        """
        platform = platform.lower()
        
        if platform == 'telegram':
            return self._setup_telegram(**kwargs)
        elif platform == 'kakao' or platform == 'kakaotalk':
            return self._setup_kakao(**kwargs)
        elif platform == 'whatsapp':
            return self._setup_whatsapp(**kwargs)
        elif platform == 'email':
            return self._setup_email(**kwargs)
        elif platform == 'discord':
            return self._setup_discord(**kwargs)
        else:
            return {'success': False, 'error': f'Unknown platform: {platform}'}
    
    def _setup_telegram(self, bot_token: str = None, api_id: str = None, api_hash: str = None):
        """Setup Telegram bot or client"""
        if bot_token:
            self.credentials['telegram'] = {
                'type': 'bot',
                'token': bot_token,
                'setup_date': datetime.now().isoformat()
            }
            self.platforms['telegram'] = True
            self.save_config()
            return {
                'success': True,
                'message': 'Telegram bot configured successfully',
                'platform': 'telegram',
                'type': 'bot'
            }
        elif api_id and api_hash:
            self.credentials['telegram'] = {
                'type': 'user',
                'api_id': api_id,
                'api_hash': api_hash,
                'setup_date': datetime.now().isoformat()
            }
            self.platforms['telegram'] = True
            self.save_config()
            return {
                'success': True,
                'message': 'Telegram user client configured',
                'platform': 'telegram',
                'type': 'user'
            }
        else:
            return {
                'success': False,
                'error': 'Provide bot_token OR api_id and api_hash for Telegram'
            }
    
    def _setup_kakao(self, app_key: str = None, secret_key: str = None):
        """Setup KakaoTalk messaging"""
        if app_key and secret_key:
            self.credentials['kakao'] = {
                'app_key': app_key,
                'secret_key': secret_key,
                'setup_date': datetime.now().isoformat()
            }
            self.platforms['kakao'] = True
            self.save_config()
            return {
                'success': True,
                'message': 'KakaoTalk configured successfully',
                'platform': 'kakao'
            }
        else:
            return {
                'success': False,
                'error': 'Provide app_key and secret_key for KakaoTalk'
            }
    
    def _setup_whatsapp(self, phone_number: str = None, api_key: str = None):
        """Setup WhatsApp Business API"""
        if phone_number and api_key:
            self.credentials['whatsapp'] = {
                'phone_number': phone_number,
                'api_key': api_key,
                'setup_date': datetime.now().isoformat()
            }
            self.platforms['whatsapp'] = True
            self.save_config()
            return {
                'success': True,
                'message': 'WhatsApp Business configured',
                'platform': 'whatsapp'
            }
        else:
            return {
                'success': False,
                'error': 'Provide phone_number and api_key for WhatsApp'
            }
    
    def _setup_email(self, smtp_server: str = None, email_address: str = None, 
                     password: str = None, port: int = 587):
        """Setup Email (SMTP)"""
        if smtp_server and email_address and password:
            self.credentials['email'] = {
                'smtp_server': smtp_server,
                'email_address': email_address,
                'password': password,  # In production, use encrypted storage
                'port': port,
                'setup_date': datetime.now().isoformat()
            }
            self.platforms['email'] = True
            self.save_config()
            return {
                'success': True,
                'message': f'Email configured for {email_address}',
                'platform': 'email'
            }
        else:
            return {
                'success': False,
                'error': 'Provide smtp_server, email_address, and password'
            }
    
    def _setup_discord(self, bot_token: str = None, guild_id: str = None):
        """Setup Discord bot"""
        if bot_token:
            self.credentials['discord'] = {
                'token': bot_token,
                'guild_id': guild_id,
                'setup_date': datetime.now().isoformat()
            }
            self.platforms['discord'] = True
            self.save_config()
            return {
                'success': True,
                'message': 'Discord bot configured',
                'platform': 'discord'
            }
        else:
            return {
                'success': False,
                'error': 'Provide bot_token for Discord'
            }
    
    def send_message(self, platform: str, recipient: str, message: str, 
                     attachments: List[str] = None) -> Dict:
        """
        Send a message via specified platform
        Returns result dict with success status and details
        """
        platform = platform.lower()
        timestamp = datetime.now().isoformat()
        
        # Check if platform is configured
        if not self.platforms.get(platform, False):
            return {
                'success': False,
                'error': f'{platform} is not configured. Run setup first.',
                'platform': platform
            }
        
        # Log the message attempt
        message_log = {
            'timestamp': timestamp,
            'platform': platform,
            'recipient': recipient,
            'message': message,
            'attachments': attachments or [],
            'status': 'pending'
        }
        
        try:
            if platform == 'telegram':
                result = self._send_telegram(recipient, message, attachments)
            elif platform in ['kakao', 'kakaotalk']:
                result = self._send_kakao(recipient, message, attachments)
            elif platform == 'whatsapp':
                result = self._send_whatsapp(recipient, message, attachments)
            elif platform == 'email':
                result = self._send_email(recipient, message, attachments)
            elif platform == 'discord':
                result = self._send_discord(recipient, message, attachments)
            else:
                result = {'success': False, 'error': f'Unsupported platform: {platform}'}
            
            message_log['status'] = 'sent' if result.get('success') else 'failed'
            message_log['response'] = result
            
        except Exception as e:
            message_log['status'] = 'error'
            message_log['error'] = str(e)
            result = {'success': False, 'error': str(e)}
        
        self.message_history.append(message_log)
        return result
    
    def _send_telegram(self, chat_id: str, message: str, attachments: List[str] = None):
        """Send Telegram message (mock implementation)"""
        # In production: use python-telegram-bot or telethon
        print(f"[TELEGRAM] Sending to {chat_id}: {message[:100]}...")
        if attachments:
            print(f"[TELEGRAM] Attachments: {attachments}")
        return {
            'success': True,
            'message_id': f'tg_{datetime.now().timestamp()}',
            'platform': 'telegram',
            'note': 'Mock mode: Enable with real API credentials for actual sending'
        }
    
    def _send_kakao(self, receiver_uuid: str, message: str, attachments: List[str] = None):
        """Send KakaoTalk message (mock implementation)"""
        # In production: use kakao-talk-api
        print(f"[KAKAO] Sending to {receiver_uuid}: {message[:100]}...")
        return {
            'success': True,
            'message_id': f'kk_{datetime.now().timestamp()}',
            'platform': 'kakao',
            'note': 'Mock mode: Enable with real API credentials for actual sending'
        }
    
    def _send_whatsapp(self, phone_number: str, message: str, attachments: List[str] = None):
        """Send WhatsApp message (mock implementation)"""
        # In production: use twilio or whatsapp-business-api
        print(f"[WHATSAPP] Sending to {phone_number}: {message[:100]}...")
        return {
            'success': True,
            'message_id': f'wa_{datetime.now().timestamp()}',
            'platform': 'whatsapp',
            'note': 'Mock mode: Enable with real API credentials for actual sending'
        }
    
    def _send_email(self, to_address: str, subject_or_message: str, attachments: List[str] = None):
        """Send Email (mock implementation)"""
        # In production: use smtplib or sendgrid
        print(f"[EMAIL] Sending to {to_address}")
        print(f"Subject/Message preview: {subject_or_message[:100]}...")
        return {
            'success': True,
            'message_id': f'em_{datetime.now().timestamp()}',
            'platform': 'email',
            'note': 'Mock mode: Enable with real SMTP credentials for actual sending'
        }
    
    def _send_discord(self, channel_id: str, message: str, attachments: List[str] = None):
        """Send Discord message (mock implementation)"""
        # In production: use discord.py
        print(f"[DISCORD] Sending to channel {channel_id}: {message[:100]}...")
        return {
            'success': True,
            'message_id': f'dc_{datetime.now().timestamp()}',
            'platform': 'discord',
            'note': 'Mock mode: Enable with real bot token for actual sending'
        }
    
    def get_message_history(self, platform: str = None, limit: int = 10) -> List[Dict]:
        """Retrieve message history"""
        history = self.message_history
        if platform:
            history = [m for m in history if m['platform'] == platform]
        return history[-limit:]
    
    def list_contacts(self, platform: str = None) -> Dict:
        """List saved contacts per platform"""
        contacts_file = Path("data/contacts.json")
        if contacts_file.exists():
            with open(contacts_file, 'r') as f:
                all_contacts = json.load(f)
                if platform:
                    return {platform: all_contacts.get(platform, [])}
                return all_contacts
        return {}
    
    def add_contact(self, platform: str, name: str, identifier: str, 
                    extra_info: Dict = None) -> Dict:
        """Add a contact"""
        contacts_file = Path("data/contacts.json")
        contacts_file.parent.mkdir(parents=True, exist_ok=True)
        
        all_contacts = {}
        if contacts_file.exists():
            with open(contacts_file, 'r') as f:
                all_contacts = json.load(f)
        
        if platform not in all_contacts:
            all_contacts[platform] = []
        
        contact = {
            'name': name,
            'identifier': identifier,
            'extra_info': extra_info or {},
            'added_date': datetime.now().isoformat()
        }
        
        # Check for duplicates
        for existing in all_contacts[platform]:
            if existing['identifier'] == identifier:
                return {
                    'success': False,
                    'error': f'Contact {name} already exists on {platform}'
                }
        
        all_contacts[platform].append(contact)
        
        with open(contacts_file, 'w') as f:
            json.dump(all_contacts, f, indent=2)
        
        return {
            'success': True,
            'message': f'Added {name} to {platform} contacts',
            'contact': contact
        }
    
    def execute_capability(self) -> Dict:
        """Return agent capabilities"""
        return {
            'agent_name': self.name,
            'capabilities': [
                'send_messages',
                'setup_platforms',
                'manage_contacts',
                'message_history',
                'multi_platform_support'
            ],
            'supported_platforms': list(self.platforms.keys()),
            'configured_platforms': [p for p, active in self.platforms.items() if active],
            'features': {
                'telegram': 'Bot and User API support',
                'kakao': 'KakaoTalk messaging',
                'whatsapp': 'WhatsApp Business API',
                'email': 'SMTP email sending',
                'discord': 'Discord bot integration'
            }
        }


if __name__ == "__main__":
    # Test the communication agent
    agent = CommunicationAgent()
    print("=== MIKE AI Communication Agent ===\n")
    print(json.dumps(agent.execute_capability(), indent=2))
    
    # Example: Setup platforms (commented out - requires real credentials)
    # agent.setup_platform('telegram', bot_token='YOUR_BOT_TOKEN')
    # agent.setup_platform('email', smtp_server='smtp.gmail.com', 
    #                      email_address='you@gmail.com', password='your_app_password')
    
    # Example: Send message (mock mode)
    # result = agent.send_message('telegram', '@username', 'Hello from MIKE AI!')
    # print(result)
