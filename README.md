# for direct access :
  # using this method you can directly run the bot and place different types of order and also view order history
  git clone https://github.com/akhil-sreenivasan-25/akhil_sreenivasan-binance-bot.git
  akhil_sreenivasan-binance-bot\env1\src>baseapp.py
# need to acces and modification on code :
  # this method allow you to acess code and modify, and you run the program through terminal by activating the virtual enviornment
  py -m venv env1 
  cd env1\scripts 
  activate 
  git clone https://github.com/akhil-sreenivasan-25/akhil_sreenivasan-binance-bot.git
  cd akhil_sreenivasan-binance-bot/env1
  pip install -r requirement.txt
  cd src
  py baseapp.py 

# Tkinder view
  run test_tk.py

# other details
  in this bot there are mainly 4 operations
    1. market order - place order on market price
    2. limit order  - place order on a spesific price, when market reach the price, the order trigerred
    3. stop limit order - place a stop price, and market reach the price, then triger a limit order
    4. order history - show our orders, we need to enter the pair which we need
