import os
import json
import urllib.request
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)




class Line():
    def __init__(self):
        self.LINE_CHANNEL_ACCESS_TOKEN   = os.environ['CHANNELACCESSTOKEN']
        self.REQUEST_URL = 'https://api.line.me/v2/bot/message/reply'
        self.REQUEST_METHOD = 'POST'
        self.REQUEST_HEADERS = {
            'Authorization': 'Bearer ' + self.LINE_CHANNEL_ACCESS_TOKEN,
            'Content-Type': 'application/json'
            }

        self.REQUEST_MESSAGE = [
            {
                'type': 'sticker',
                'packageId': 11537,
                'stickerId': 52002742
            }
        ]#リスト型にしてその中に辞書型を入れる


    def CreateREQUESTMESSAGE(self, kind, text):
        self.REQUEST_MESSAGE = [
            {
                'type': kind,
                'text': text
            }
        ]

    def UserSendMessage(self, event):
        user_send_message = json.loads(event['body'])['events'][0]['message']['text']
        return user_send_message

    def GetReplyToken(self, event):
        self.REPLYTOKEN = json.loads(event['body'])['events'][0]['replyToken']

    def GetUserId(self, event):
        user_id = json.loads(event['body'])['events'][0]['source']['userId']
        return user_id

    def BotSendMessage(self):
        try:
            params = {
                    'replyToken': self.REPLYTOKEN,
                    'messages': self.REQUEST_MESSAGE
                }
            request = urllib.request.Request(
                self.REQUEST_URL,
                json.dumps(params).encode('utf-8'),#paramsをjson形式にエンコードする
                method=self.REQUEST_METHOD,
                headers=self.REQUEST_HEADERS
            )
            response = urllib.request.urlopen(request, timeout=10)
        except Exception:
            print('Exception Of BotSendMessage')

    def BotSendMessageError(self):
        try:
            params = {
                'replyToken': self.REPLYTOKEN,
                'messages': 'Error'
            }
            request = urllib.request.Request(
                self.REQUEST_URL,
                json.dumps(params).encode('utf-8'),
                method=self.REQUEST_METHOD,
                headers=self.REQUEST_HEADERS
            )
            response = urllib.request.urlopen(request, timeout=10)
        except Exception:
            print('Exception Of BotSendMessageError')
