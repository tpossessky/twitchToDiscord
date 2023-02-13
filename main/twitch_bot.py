import aiofiles
import twitchAPI
from twitchAPI import Twitch
from twitchAPI.chat import Chat, EventData, ChatMessage
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope
from twitchAPI.types import ChatEvent
import random

APP_ID = ''
APP_SECRET = ''
USER_SCOPE = [AuthScope.CHAT_READ]
TARGET_CHANNEL = 'littlefrei'


async def on_ready(ready_event: EventData):
    print('TwitchBot is ready, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)


async def on_message(msg: ChatMessage):
    if msg.user.name == 'solacestream':
        async with aiofiles.open('msg.txt', 'w') as f:
            num = random.randint(100000, 999999)
            await f.write('{:03d}\n'.format(num))


# this is where we set up the bot
async def run():
    # set up twitch api instance and add user authentication with some scopes
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, USER_SCOPE, force_verify=False)

    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

    # create chat instance
    chat = await Chat(twitch)

    # register the handlers for the events you want

    # listen to when the bot is done starting up and ready to join channels
    chat.register_event(ChatEvent.READY, on_ready)
    # listen to chat messages
    chat.register_event(ChatEvent.MESSAGE, on_message)

    # we are done with our setup, lets start this bot up!
    chat.start()

# lets run our setup
