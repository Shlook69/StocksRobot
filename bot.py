import discord
import responses

ERROR_IN_COMMAND = '**Invalid command/usage. Try `?help`**'

async def send_message(message, user_message):
    try:
        response = responses.get_response(user_message, message)
        await message.channel.send(response)
    except Exception as e: # and error occured (most likely in responses.py) for instance, a user sent 2 params instead of 1
        await message.channel.send(ERROR_IN_COMMAND) # show user an error messsage
        print(e) # print exception for debug


def run_discord_bot():
    TOKEN = 'I am sorry, the token must be kept secret...' # token to run bot
    intents = discord.Intents.default()
    intents.message_content = True # setup this intent (event) because there is a need to get user message content
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready(): # bot is running
        print(f'{client.user} is now running!')
    responses.init_func_calls_dict()

    
    @client.event
    async def on_message(message): # a message has been written
        if message.author == client.user: # check if there was a bug and prevent infinite loop
            return

        # extract the following (and make sure are string):
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)
        
        print(f'{username} said: {user_message} ({channel})') # just for debug purposes

        if user_message[0] == '?': # check if the message if for our bot
            user_message = user_message[1:] # remove the bot sign from the user message
            await send_message(message, user_message)


    client.run(token=TOKEN) # run the bot

