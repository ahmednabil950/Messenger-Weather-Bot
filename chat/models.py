from django.db import models
from channels import Group
from .settings import MSG_TYPE_MESSAGE
import json

# Create your models here.

class RoomModel(models.Model):
    # room id
    id = models.IntegerField(primary_key=True)

    # room title
    title = models.CharField(max_length=50, blank=False, null=False)

    # staff people only
    staff_only = models.BooleanField(default=False)

    @property
    def websocket_group(self):
        """
        Returns the Channels Group that sockets should subscribe to to get sent
        messages as they are generated.
        """
        return Group("room-%s" % self.id)

    def send_message(self, message, user, msg_type=MSG_TYPE_MESSAGE):
        """
        Called to send a message to the room on behalf of a user.
        """
        final_msg = {
            'room': str(self.id),
            'message': message,
            'username': user.username,
            'msg_type': msg_type
        }
        # Send out the message to everyone in the room
        self.websocket_group.send({
            'text': json.dumps(final_msg)
        })

    def __str__(self):
        return self.title
