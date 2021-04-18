import json
import os
import urllib.request
import logging
import boto3

from dish_log_line_bot import Line
from dish_log_dynamodb import Dynamodb




def lambda_handler(event, context):
  line = Line()

  line.GetReplyToken(event)
  user_send_message = line.UserSendMessage(event)
  user_id = line.GetUserId(event)

  dynamodb = Dynamodb()
  delte_mode = dynamodb.DelteMode()

  info_dishes = []
  register_userid1 = os.environ['UserId1']
  register_userid2 = os.environ['UserId2']

  #deltemodeなら下記の条件分岐を行う
  if delte_mode:
    if user_send_message == '削除':
      dynamodb.changeDelteMode(delte_mode)
      line.CreateREQUESTMESSAGE('text', '削除モード解除しました')
      line.BotSendMessage()
      return 0
    else:
      check_delte = dynamodb.DeleteItem(register_userid1, user_send_message)
      if check_delte:
        dynamodb.changeDelteMode(delte_mode)
        line.CreateREQUESTMESSAGE('text', '削除しました。削除モードを終了します。')
        line.BotSendMessage()
        return 0
      else:
        line.CreateREQUESTMESSAGE('text', '削除できませんでした')
        line.BotSendMessage()
        return 0

  #登録されているuserIdかつ送られたメッセージにより条件分岐を行う
  if user_id == register_userid1 or user_id == register_userid2:
    if user_send_message == '表示':
      items = dynamodb.GettingItem(register_userid1)
      for i, item in enumerate(items,1):
        made_date = item['made_date']
        dish_name = item['dish_name']
        dish_info = ('{}:{}').format(i, dish_name)
        info_dishes.append(dish_info)

      if info_dishes:
        line.CreateREQUESTMESSAGE('text', ' '.join(info_dishes))
        line.BotSendMessage()

      else:
        line.CreateREQUESTMESSAGE('text', '登録されていません')
        line.BotSendMessage()

    elif user_send_message == '削除':
        dynamodb.changeDelteMode(delte_mode)
        line.CreateREQUESTMESSAGE('text', 'どの料理を削除しますか？')
        line.BotSendMessage()

    else:
      line.CreateREQUESTMESSAGE('text', '料理ありがとう')
      line.BotSendMessage()
      dynamodb.CreatingNewItem(register_userid1, user_send_message)

  else:
    line.CreateREQUESTMESSAGE('text', '登録されていないユーザですので、利用できません')
    line.BotSendMessage()
