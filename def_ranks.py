import requests as req

response = req.get('https://www.numberfire.com/nba/daily-fantasy/games/top-dvp-matchups')
print(response)