"""
    modules here :
"""

import json
import re
from typing import Optional
from urllib.parse import urlparse, parse_qs, quote
from base64 import b64encode

from bs4 import BeautifulSoup
from utils.client import Client
from utils.models import Stel_tsession, Confirm_, Link_, Con_Log, G_hash, C_code


class Telegram(Client): 
    """
        This class represents a Telegram client.

        It provides methods to interact with the Telegram API for user authentication and session management.

        Methods:
        - __init__: Initialize the Telegram client with the given phone number.
        - send_num: Send the phone number to initiate the session.
        - confirm: Confirm the login with the given session token.
        - confirm_link: Confirms the link by extracting the hash from the response.
        - confirm_login: Confirms the login by extracting the auth_code from the response.
        - get_hash: Retrieve the main hash.
        - try_code: Attempts to log in with the provided hash and auth code.
    """
    
    def __init__(self, phone_number: str):
        """
            Initialize the Telegram client with the given phone number.
        """
        Client.__init__(self)
        self.number = phone_number
        print(self.number)
        self.stel_ssid: Optional[str] = self.auth_get('',{},{}).cookies.get('stel_ssid')
        print(self.stel_ssid)

    def send_num(self) -> Stel_tsession:
        """
            Send the phone number to initiate the session.

            :return: Stel_tsession object with the response data.
        """
        res = self.auth_post('/request',cookies={"stel_ssid": self.stel_ssid},headers={},data={"phone": self.number})
        print(res.content)
        return Stel_tsession(res)
    
    def confirm(self, stel_tsession: str) -> Confirm_:
        """
            Confirm the login with the given session token.

            :param stel_tsession: The session token to confirm.
            :return: Confirm_ object with the response data.
        """
        res = self.auth_post('/login',headers={"Cookie": f"stel_ssid={self.stel_ssid}; stel_tsession_{self.number}={stel_tsession}; stel_tsession={stel_tsession}"},data={},cookies={})
        return Confirm_(res)

    def confirm_link(self, stel_token: str) -> Link_:
        """
        Confirms the link by extracting the hash from the response.

        :param stel_token: The stel_token cookie value.
        :return: An instance of Link_ with the extracted hash or False if extraction fails.
        """
        try:
            res = self.auth_get('',headers={"Referer": "https://oauth.telegram.org/auth?bot_id=5444323279&origin=https%3A%2F%2Ffragment.com&request_access=write&return_to=https%3A%2F%2Ffragment.com%2F",},cookies={'stel_ssid':self.stel_ssid, 'stel_token':stel_token})
            print(res.content)
            script_tag = BeautifulSoup(res.text, "html.parser").findAll("script")[1]
            confirm_url = script_tag.string[script_tag.string.find("var confirm_url = ") + len("var confirm_url = ")+ 1: script_tag.string.find("',")]
            if confirm_url:
                hash_ = parse_qs(urlparse(confirm_url).query).get("hash")[0]
                return Link_(hash_,confirm_url)
            return Link_(False,False)
        except (IndexError, AttributeError, TypeError) as e:
            # Catch specific exceptions for better error handling
            print(f"Error occurred: {e}")
            return Link_(False,False)
    
    def confirm_login(self, link: str, stel_token: str) -> Con_Log:
        """
            Confirms the login by extracting the auth_code from the response.

            :param link: The URL to send the GET request to.
            :param stel_token: The stel_token cookie value.
            :return: An instance of Con_Log with the extracted auth_code or False if extraction fails.
        """
        res = self.session.get(link, cookies={"stel_ssid": self.stel_ssid, "stel_token": stel_token}, headers={**self.headers})
        try:
            soup = BeautifulSoup(res.text, 'html.parser')
            scr_ = soup.find('script').string
            j_ = scr_[int(scr_.find('result: ') + len('result: ')):int(scr_.find('}, origin:') + 1  )]
            en_ = quote(json.dumps(json.loads(j_)))
            auth_code = b64encode(en_.encode('utf-8')).decode('utf-8')

            return Con_Log(auth_code)
        except (AttributeError, IndexError):
            return Con_Log(False)
    
    def get_hash(self) -> G_hash:
        """
            Retrieve the main hash.

            :return: G_hash object with the retrieved hash or False if not found.
        """
        res = self.fr_get('',cookies={"stel_ssid": self.stel_ssid},headers={})
        try:
            main_h = re.search(r"hash=([A-Za-z0-9]{15,32})", res.text).group(1)
            return G_hash(main_h)
        except (AttributeError, IndexError):
            return G_hash(False)    

    def try_code(self,m_hash,auth_code: str) -> C_code:
        """
            Attempts to log in with the provided hash and auth code.

            :param m_hash: The hash to use for the login attempt.
            :param tgauthcode: The authentication code to use for the login attempt.
            :return: An instance of C_code containing the result of the login attempt.
        """
        print(auth_code)
        print(f'{self._api("")}/api')
        res = self.session.post(f'{self._api("")}/api',headers={"Referer": self._api("")},params={"hash": m_hash},cookies={"stel_ssid": self.stel_ssid, "stel_dt": "-180"},data={"auth": auth_code, "method": "logIn"})
        print(res.content)
        return C_code(res)
    
    
phone_number_string = '' #ex: +964xxxxxx

c = Telegram(phone_number_string)

send_num = c.send_num().stel_tsession
input('m ') # when you click on Accept Button.  write any thing ( this input just for wait clicking )
confirm = c.confirm(send_num).stel_token

confirm_link = c.confirm_link(confirm).link
print(confirm_link)

confirm_login = c.confirm_login(confirm_link,confirm).auth_code

get_hash = c.get_hash().hash
print(get_hash)

try_code = c.try_code(get_hash,confirm_login).stel_token

print(try_code)
