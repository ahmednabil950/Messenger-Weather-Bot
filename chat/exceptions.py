import json


# User logged into the chat
# if an unauthorized user tries to do it? 
# and what if the requested room does not exist? or 
# if the user has no rights to enter this room at all? 
# That's right, an error will occur! And in the first two cases, 
# it will clearly be thrown at the system level, 
# and in the third case the user will likely get to the secret room. 
# To prevent such a trouble from happening, you need to add error handling.

class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super(ClientError, self).__init__(code)
        self.code = code

    def send_to(self, channel):
        channel.send({
            "text": json.dumps({
                "error": self.code,
            }),
        })