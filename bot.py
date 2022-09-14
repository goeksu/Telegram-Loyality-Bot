import os
import telebot
from telebot import types
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

bot = telebot.TeleBot('CRED-HERE')
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
  'projectId': 'CRED-HERE',
})
db = firestore.client()


@bot.message_handler(commands=['start'])
def send_welcome(message):

  
  

  dbsearch = db.collection('users').document(str(message.from_user.id))
  global doc
  doc = dbsearch.get()
  if doc.exists:
    #user exists
    print(f'user id found {message.from_user.id}')
    bot.send_message(message.chat.id, f'Welcome {doc.to_dict()}')
    welcomescreen(message, doc)
  else:
    #need to registration
    print(u'no user')
    registerstart = bot.send_message(message.chat.id, 'hello, we need to meet first. What is your name?')
    bot.register_next_step_handler(registerstart, registername)

def registername(message):
    global name
    name = message.text
    registerphone = bot.send_message(message.chat.id, f'nice to meet you {name}, we need your phone too, what was your phone number?')
    bot.register_next_step_handler(registerphone, registerdone)
    
def registerdone(message):
    phone = message.text
    data = {
        u'name': name,
        u'phone': phone}
    db.collection(u'users').document(str(message.from_user.id)).set(data)
    bot.send_message(message.chat.id, f'{name}, you have registered successfully. welcome to the club')
    dbsearch = db.collection('users').document(str(message.from_user.id))
    doc = dbsearch.get()
    welcomescreen(message, doc)
   #registration complete


#welcome
def welcomescreen(message, doc):
  
  markup = types.ReplyKeyboardMarkup(row_width=1)
  
  itemkuku = types.KeyboardButton('Kuku Nuts')
  itemkoka = types.KeyboardButton('Koka Pastry')
  itemvito = types.KeyboardButton('Don Vito')
  itemreturn = types.KeyboardButton('Return')
  markup.row(itemkuku, itemkoka, itemvito)
  markup.row(itemreturn)
  bot.send_message(message.chat.id, "Choose the store:", reply_markup=markup)

bot.polling()
print('done')
