class Stel_tsession:
    """
        Represents a session with the Stel system.

        This class manages the session status and the Stel session token.
    """
    def __init__(self, res):
        """
        Initializes Stel_tsession instance.
        
        :param res: The response object from the request.
        """
        self.status = 'true' in res.text
        self.stel_tsession = res.cookies.get('stel_tsession') if self.status else None
        

class Confirm_:
    """
        Represents a confirmation response.

        This class manages the confirmation status and the Stel token.
    """
    
    def __init__(self, res):
        """
        Initializes Confirm_ instance.
        
        :param res: The response object from the request.
        """
        self.status = 'true' in res.text
        self.stel_token = res.cookies.get('stel_token') if self.status else None

class Link_:
    """
        Represents a link extracted from the response.

        This class manages the status of the link and the link URL.
    """
    def __init__(self, hash,confirm_url):
        """
        Initializes Link_ instance.
        
        :param hash: The hash value extracted from the response.
        """
        self.status = hash is not False
        self.hash = hash
        self.link = f"https://oauth.telegram.org{confirm_url}&allow_write=1" if self.status else None


class Con_Log:
    """
        Represents a Telegram authorization code.

        This class manages the status of the authorization code and the code itself.
    """

    def __init__(self, auth_code):
        """
        Initializes Con_Log instance.
        
        :param auth_code: The Telegram authorization code extracted from the response.
        """
        self.status = auth_code is not False
        self.auth_code = auth_code if self.status else None



class G_hash:
    """
        Represents a main hash value extracted from the response.

        This class manages the status of the hash value and the hash itself.
    """
    def __init__(self, main_h):
        """
        Initializes G_hash instance.
        
        :param main_h: The main hash value extracted from the response.
        """
        self.status = main_h is not False
        self.hash = main_h if self.status else None


class C_code:
    """
        Represents a response code.

        This class manages the status of the response code and the code itself.
    """
    def __init__(self, res):
        """
        Initializes C_code instance.
        
        :param res: The response object from the request.
        """
        try:
            self.status = True
            self.stel_token = res.cookies.get('stel_token')
        except AttributeError:
            self.status = False
