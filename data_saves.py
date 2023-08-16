import json

DATA_FILE_NAME = "savedata.json"


# loads json data from file
def get_json_load():
    with open (DATA_FILE_NAME, 'r') as f:
        return json.load(f)


# returns the user's followed stocks
def get_stocks_json(user_id):
    data = get_json_load()
    if user_id not in data.keys():
        return []
    return data[user_id]


# add stock to the user's list in json
def add_stock_to_json(user_id, stock_name):
    current_user_stocks = get_stocks_json(user_id)
    if (len(current_user_stocks) == 5):
        current_user_stocks.pop(0) # limit of 5 saved stocks
    if (stock_name in current_user_stocks): # stock is already in list
        return "**Stock is already on your list!**"
    current_user_stocks.append(stock_name) # now list is updated with the new added stock
    data = get_json_load()
    with open (DATA_FILE_NAME, 'w') as f: # adding to JSON file the updated list
        data[user_id] = current_user_stocks
        json.dump(data, f, indent=4)
    return "**Added stock to your list.**"