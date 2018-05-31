import requests
import json


class messenger:

    def __init__(self):
        self.ACCESS_TOKEN = ""
        self.URL_BASE = "https://graph.facebook.com/v2.6/me/"
        self.VERIFY_TOKEN = "typicallywillreplyatinstant"
        self.post_url = "messages?access_token="
        self.assest_url = "message_attachments?access_token="

    def URL_TO_POST(self, url):
        return self.URL_BASE + url + self.ACCESS_TOKEN

    def Verify_Token(self, token):
        if (token == self.VERIFY_TOKEN):
            return True
        else:
            return False

    def check_json_sent(self, Received_Json_From_Facebook):

        if Received_Json_From_Facebook["entry"][0]["messaging"][0].get("message").get("attachments"):
            return Received_Json_From_Facebook["entry"][0]["messaging"][0].get("message").get("attachments")[0].get("type")
        elif Received_Json_From_Facebook["entry"][0]["messaging"][0].get("message").get("quick_reply"):
            return "quick_reply"
        elif Received_Json_From_Facebook["entry"][0]["messaging"][0].get("message").get("text"):
            return "text"

    def get_payload(self, Received_Json_From_Facebook):
        return Received_Json_From_Facebook["entry"][0]["messaging"][0].get("message").get("quick_reply").get("payload")

    def get_attachement_link(self, Received_Json_From_Facebook):
        return Received_Json_From_Facebook["entry"][0]["messaging"][0].get("message").get("attachments")[0].get("payload").get("url")

    def get_receptient_ID(self, Received_Json_From_Facebook):
        return Received_Json_From_Facebook["entry"][0]["messaging"][0]["sender"]["id"]

    def get_received_text(self, Received_Json_From_Facebook):
        text = Received_Json_From_Facebook["entry"][0]["messaging"][0].get(
            "message")
        if text:
            return text["text"]

    def get_typing_status(self, rec_ID, status):

        params = {"access_token": self.ACCESS_TOKEN}
        headers = {"Content-Type": "application/json"}

        post_message_url = self.URL_TO_POST(self.post_url)
        type_req = dict()
        type_req["recipient"] = {"id": rec_ID}

        if status == "on":
            type_req["sender_action"] = "typing_on"
        elif status == "off":
            type_req["sender_action"] = "typing_off"
        elif status == "seen":
            type_req["sender_action"] = "mark_seen"

        type_req = json.dumps(type_req)
        req = requests.post(post_message_url,  headers=headers, data=type_req)

        return req.json(), req.status_code

    def send_text_msgs(self, array_of_msgs, msg_type, rec_ID):

        params = {"access_token": self.ACCESS_TOKEN}
        headers = {"Content-Type": "application/json"}

        post_message_url = self.URL_TO_POST(self.post_url)
        Json_Body = dict()

        Json_Body["messaging_type"] = msg_type
        Json_Body["recipient"] = {"id": rec_ID}

        req = None

        for msg in array_of_msgs:

            Json_Body["message"] = {"text": msg}
            Json_Body = json.dumps(Json_Body)
            req = requests.post(
                post_message_url,  headers=headers, data=Json_Body, timeout=3)
            Json_Body = json.loads(Json_Body)

        return req.json(), req.status_code

    def send_media_msgs(self, array_of_msgs, rec_ID, media_type, Assest=False):

        params = {"access_token": self.ACCESS_TOKEN}
        headers = {"Content-Type": "application/json"}

        post_message_url = self.URL_TO_POST(self.post_url)
        Json_Body = dict()

        Json_Body["recipient"] = {"id": rec_ID}

        req = None

        for msg in array_of_msgs:

            Json_Body["message"] = {"attachment": {"type": media_type,  "payload": {
                "url": msg,  "is_reusable": str(Assest).lower()}}}
            Json_Body = json.dumps(Json_Body)
            req = requests.post(
                post_message_url,  headers=headers, data=Json_Body, timeout=3)
            Json_Body = json.loads(Json_Body)

        return req.json(), req.json().get("attachment_id")

    def get_media_content(self, directory, extention, Received_Json_From_Facebook):

        print('Beginning file download with requests')

        url = self.get_attachement_link(Received_Json_From_Facebook)

        r = requests.get(url)

        with open(directory + extention,  'wb') as f:
            f.write(r.content)

        print(r.status_code)
        print(r.headers['content-type'])
        print(r.encoding)

        print("Done....")

        return (r.status_code, r.headers['content-type'])

    def saving_assests(self, type_of_content, url):

        params = {"access_token": self.ACCESS_TOKEN}
        headers = {"Content-Type": "application/json"}

        post_message_url = self.URL_TO_POST(self.assest_url)
        Json_Body = dict()

        Json_Body = {"message": {"attachment": {
            "type": type_of_content, "payload": {"is_reusable": "true", "url": url}}}}
        Json_Body = json.dumps(Json_Body)
        req = requests.post(post_message_url,  headers=headers,
                            data=Json_Body, timeout=3)

        return req.json()["attachment_id"]

    def quick_reply(self, text, array_of_quiks, rec_ID):

        params = {"access_token": self.ACCESS_TOKEN}
        headers = {"Content-Type": "application/json"}

        post_message_url = self.URL_TO_POST(self.post_url)
        Json_Body = dict()

        Json_Body = {"recipient": {"id": rec_ID}, "message": {
            "text": text, "quick_replies": array_of_quiks}}
        Json_Body = json.dumps(Json_Body)
        req = requests.post(post_message_url,  headers=headers,
                            data=Json_Body, timeout=3)

        return req.json()


    def get_started_msg(self, greeting_msg):
        headers = {"Content-Type": "application/json"}
        profile_api = "https://graph.facebook.com/v2.6/me/messenger_profile?access_token="+self.ACCESS_TOKEN
        json_format = dict()
        json_format = {
            "get_started": {
                "payload": "GET_STARTED_PAYLOAD"
            }
        }
        req = requests.post(profile_api, headers=headers, data=json.dumps(json_format), timeout=3)
        return req.json()