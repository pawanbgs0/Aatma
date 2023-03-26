import os, requests, json
import telebot
import urllib.request as rq
#from newsapi import NewsApiClient



NEWS_API = os.environ['NEWS_API']
#newsapi = NewsApiClient(api_key = NEWS_API)

API_KEY = os.environ['API_KEY']
bot = telebot.TeleBot(API_KEY)



@bot.message_handler(commands = ['start'])
def startup(message):
  print("Started")
  bot.send_message(message.chat.id, "          Hey, Brave enough to contact an Aatma! 🤨 \n\nType the following commands to get help. 👍\n\n/greet - To greet yourself.   🙌\n/motivate - To get an inspirational quote. 🔥\n/horo sunsign - To read your horiscope. 🌟\n/dict word - To search meaning of a word. 👨‍💻\n/news - To keep you updated with world. 🗞\n\nI hope you won't be afraid of all these. 😌\n\nWatching you closely! 🧐")

@bot.message_handler(commands = ['greet'])
def greet(message):
  print("Greeted")
  user_name = message.from_user.first_name
  bot.reply_to(message, "Bravo " + user_name + "! 🙌 You just gave a command to an 'Aatma'. \nI am delighted to welcome you to the Induction of GDSC SNU 🥳. Looks like you are enjoying the event. 🎊")

@bot.message_handler(commands = ['motivate'])
def get_quote(message):
  print("Motivated")
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " 🔥\n  - " + json_data[0]['a'] + ' 👊'
  bot.send_message(message.chat.id, quote)


@bot.message_handler(commands = ['gift'])
def gift(message):
  print("Gifted")
  user_name = message.from_user.first_name
  data = 'Thank You ' + user_name + ' for staying with us till now! 🤗 \n\nAs an honor, we are delighted to gift you a badge that can actually be showcased at your Google Developers account. ☺️' + '\n\nClick https://example.com to redeem it now 🎊'
  bot.send_message(message.chat.id, data)

def dict_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "/dict":
    return False
  else:
    return True



@bot.message_handler(func = dict_request)
def dict_word(message):
  print("Dicted")
  word = message.text.split()[1]
  url = "https://api.dictionaryapi.dev/api/v2/entries/en/%s" % (word)

  def url_check(url):
    try:
      rq.urlopen(url)
    except:
      bot.send_message(message.chat.id, 'There is a spelling mistake or word not found. 👀\nTry searching a different word 💁‍♂️')
      return False
    return True
  
  if (url_check(url)):
    response = requests.get(url)
  
    json_data = json.loads(response.text)

    definition = json_data[0].get('meanings', 'Not Found')[0].get('definitions', 'Not Found')[0].get('definition', 'Not Found')

    example = json_data[0].get('meanings', 'Not Found')[0].get('definitions', 'Not Found')[0].get('example', 'Not Found')

    data = 'Word: ' + word + ' 📖\n\n' + 'Definition: ' + definition + ' 💯\n\n' + 'Example: ' + example + ' 📚'

    bot.send_message(message.chat.id, data)


@bot.message_handler(commands = ['news'])
def news(message):
  print("Newsed")
  url = 'https://newsapi.org/v2/top-headlines?country=in&apiKey=%s' % (NEWS_API)
  response = requests.get(url)
  json_data = json.loads(response.text)
  data = '🌐🌐🌐 Aaj ki Taza Khabar 🌐🌐🌐\n\n' + '➡️ ' + json_data.get('articles')[0].get('title') + '\nRead more: ' + json_data.get('articles')[0].get('url') + '\n\n'

  i = 1
  while (i < 10):
    data = data + '➡️ ' + json_data.get('articles')[i].get('title') + '\nRead more: ' + json_data.get('articles')[i].get('url') + '\n\n'
    i = i + 1
  #print(data)
  bot.send_message(message.chat.id, data)


def horo_request(message):
  print("Horoed")
  request = message.text.split()
  if len(request) < 2 or request[0].lower() not in "/horo" or request[1].lower() not in "libra" and request[1].lower() not in "taurus" and request[1].lower() not in "gemini" and request[1].lower() not in "cancer" and request[1].lower() not in "leo" and request[1].lower() not in "virgo" and request[1].lower() not in "scorpio" and request[1].lower() not in "sagittarius" and request[1].lower() not in "capricorn" and request[1].lower() not in "aquarius" and request[1].lower() not in "pisces" and request[1].lower() not in "aries":
    user_name = message.from_user.first_name
    data = "Hey " + user_name + "!" + " Looks like there is a mistake, 😕 check your command again 🔄, try /horo leo"
    print("Wrong Command")
    bot.send_message(message.chat.id, data)
    return False
  else:
    return True

@bot.message_handler(func = horo_request)
def get_horo(message):
  sign = message.text.split()[1]
  url = "http://horoscope-api.herokuapp.com/horoscope/today/%s" % (sign)
  response = requests.get(url)
  json_data = json.loads(response.text)

  data = 'Date: ' + json_data['date'] + ' ✨\n\n' + 'Sunsign: ' + json_data['sunsign'] + ' 🌝\n\n' + 'Horoscope: ' + json_data['horoscope'] + ' 🌟'

  bot.send_message(message.chat.id, data)


print("We are ready")
bot.polling()