from _token import token
import sys
from package.bots.calculator_bot import CalculatorBot

try:
    n = int(sys.argv[1])
except:
    n = -1

if n == -1:
    n = None

bot = CalculatorBot(token)
bot.loop(n)