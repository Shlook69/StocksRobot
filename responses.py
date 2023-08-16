import marketApi
import datetime
import dateutil.relativedelta
import data_saves

function_to_call = {} # a dictionary of all the function calls and their "calling" key
WAS_FUNC_DICT_INITIALIZED = False # a global variable to prevent the function_to_call be declared each get_response call


# initialize the function calls dictionary at the start of the program
def init_func_calls_dict():
    global function_to_call 
    global WAS_FUNC_DICT_INITIALIZED

    if not WAS_FUNC_DICT_INITIALIZED:
          function_to_call = {
                         'about' : (about_response, 'Returns a short message about the bot\'s purpose and dev.'),
                         'help': (help_response, 'Lists all the supported commands.'),
                         'priceof': (priceof_response, 'priceof [STOCK_NAME] - Returns the current price of the STOCK_NAME'),
                         'changesof' : (changesof_response, 'changesof [STOCK_NAME] - Returns today\'s and last month\'s change in STOCK_NAME'),
                         'analysis' : (analysis_response, 'analysis [STOCK_NAME] - Shows analysits of analyst (buy/sell, etc..) about STOCK_NAME'),
                         'news' : (news_response, 'news [STOCK_NAME] - send 3 links about STOCK_NAME news'),
                         'follow' : (follow_response, 'follow [STOCK_NAME] - add the STOCK_NAME to user\'s follow list (up to 5 stocks)'),
                         'mystocks' : (mystocks_response, 'mystocks - Shows the stocks the user follows (up to 5 stocks)')
               }
          WAS_FUNC_DICT_INITIALIZED = True


def get_response(message, message_obj):
    p_message = message.lower() # remove case sensitive (parsed message) 
    command_params = p_message.split(' ') # remove the first item as it is the command and not a param
    user_command = command_params.pop(0) # store the command itself

    global function_to_call
    if user_command == 'follow' or user_command == 'mystocks':
        command_params.append(str(message_obj.author.id))
    if user_command in function_to_call:
        if not command_params: # user did not give any params
          print(user_command, command_params)
          return function_to_call[user_command][0]()
        else:                  # user gave params
          return function_to_call[user_command][0](command_params)
    else:
        raise Exception("The command does not exist!") # something is wrong about the command (an error message will appear, see bot.py)


# Returns a short message about the bot's purpose and dev name
def about_response():
     return '''This is a stock market updates bot.
The purpose of this bot is to make stock market information accessible on Discord. Enjoy!

~ Developed by Shlook ~
    '''


# response of priceof command
def priceof_response(command_params):
     stock_name = command_params[0]
     
     if len(command_params) != 1:
          raise Exception("Wrong param amount\n")

     # format string with price
     price_str = command_params[0] + ' current price is: **' + marketApi.get_stock_price_current(stock_name) + '**'
     return price_str    


# response of change in the last month
def changesof_response(command_params):
     if len(command_params) != 1:
          raise Exception("Wrong param amount\n")
     
     stock_name = command_params[0]

     # get the last month date
     now_date = datetime.datetime.now()
     month_ago_date = str(now_date + dateutil.relativedelta.relativedelta(months=-1)) # get the date a month ago
     month_ago_date = month_ago_date[:month_ago_date.find(' ')] # take only date without time (using slicing)

     # get the STOCK CURRENT PRICE, STOCK PRICE A MONTH AGO, CHANGE IN PERCENTAGES
     data = marketApi.get_stock_price_monthly_change(stock_name, month_ago_date)

     # create a parsed string based on our data
     today_price = data[0]
     month_ago_price = data[1]
     change_percentage = data[2]

     # parsed string
     parsed_str = f'''
{stock_name} was worth **{month_ago_price}** a month ago ({month_ago_date}).
Today, {stock_name} is worth **{today_price}**.
Which means a change of **{change_percentage}**%.
''' 
     return parsed_str


# Return if user should buy/sell, etc.. based on analysts (achieved by yfinance api)
def analysis_response(command_params):
     if len(command_params) != 1:
          raise Exception("Wrong param amount\n")
     
     stock_name = command_params[0]

     analysts_opinion = marketApi.get_stock_analysis(stock_name)
     
     parsed_str = f"Now it is best to: **{analysts_opinion}** the **{stock_name}** stock"
     return parsed_str


# Adds a stock to user's followed stocks
def follow_response(command_params):
     if len(command_params) != 2:
         raise Exception("Wrong param amount\n")
     user_id = command_params[1]
     stock_name = command_params[0]
     ret_val = data_saves.add_stock_to_json(user_id, stock_name)
     if 'already' in ret_val:
         return f"**{stock_name} is already on your list!**"
     return f"**Added {stock_name} to your list. 5 STOCKS is the LIMIT!**"


# Returns to the user his list of followed stocks
def mystocks_response(command_params):
     if len(command_params) != 1:
         raise Exception("Wrong param amount\n")
     user_id = command_params[0]
     saved_stocks = data_saves.get_stocks_json(user_id)
     return f"This is your list:\n{str(saved_stocks)}"

# returns 3 news links about the stock
def news_response(command_params):
     stock_name = command_params[0]
     
     news_list_of_tuples = marketApi.get_stock_news(stock_name)
     parsed_str = f"Here are some news about **{stock_name}\n**"

     for tup in news_list_of_tuples:
         parsed_str += (tup[0] + ':\n' + tup[1] + '\n')
     
     return parsed_str


# prints a list of the commands and description of each 
def help_response():
    commands = '**List of supported commands:\n\n**`'
    for key in function_to_call.keys():
        commands += f"?{key} - {function_to_call[key][1]}\n"
    return (commands + '`') # Adding the '`' char to format commands nicely

