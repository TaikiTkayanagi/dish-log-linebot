import boto3
import datetime
from boto3.dynamodb.conditions import Key

class Dynamodb():

  def __init__(self):
    self.dynamodb = boto3.resource('dynamodb')
    self.table = self.dynamodb.Table('cooking_name')
    self.dt_today = datetime.date.today()

  def CreatingNewItem(self, user_id, dish_name):
    if not self.dynamodb:
      self.dynamodb = boto3.resource('dynamodb')
      self.table = self.dynamodb.Table('cooking_name')

    self.table.put_item(
      Item={
        'user_id': user_id,
        'dish_name': dish_name,
        'made_date': str(self.dt_today),
      }
    )

  def GettingItem(self, user_id):
    if not self.dynamodb:
      self.dynamodb = boto3.resource('dynamodb')
      self.table = self.dynamodb.Table('cooking_name')

    try:
        response = self.table.query(
          KeyConditionExpression=Key('user_id').eq(user_id)
        )
        items = response['Items']
        return items
    except Exception:
        print(Exception)
        return 'Error'

  #mode_delteの値を取得
  def DelteMode(self):
    if not self.dynamodb:
      self.dynamodb = boto3.resource('dynamodb')
      self.table = self.dynamodb.Table('cooking_name')

    try:
      response = self.table.get_item(Key={'user_id': 'root', 'dish_name': 'root'})
    except ClientError as e:
      print(e.response['Error']['Message'])
    else:
      print(response['Item']['mode_delte'])
      return response['Item']['mode_delte']

  #mode_delteを変更する
  def changeDelteMode(self, delte_mode):
    if delte_mode:
      response = self.table.update_item(
        Key={
            'user_id': 'root',
            'dish_name': 'root'
        },
        UpdateExpression="set mode_delte=:val",
        ExpressionAttributeValues={
            ':val': False
        },
        ReturnValues="UPDATED_NEW"
      )
      return response
    else:
      response = self.table.update_item(
        Key={
            'user_id': 'root',
            'dish_name': 'root'
        },
        UpdateExpression="set mode_delte=:val",
        ExpressionAttributeValues={
            ':val': True
        },
        ReturnValues="UPDATED_NEW"
      )
      return response

  #指定されたitemを削除する
  def DeleteItem(self, user_id, dish_name):
    if not self.dynamodb:
      self.dynamodb = boto3.resource('dynamodb')
      self.table = self.dynamodb.Table('cooking_name')
    try:
      response = self.table.delete_item(
        Key={
          'user_id': user_id,
          'dish_name': dish_name
        }
      )
      return True
    except Exception:
      return False
