import math
import random

from django.http import HttpResponse
from django.template import loader

from .forms import GameForm

def encryption(key, num):
		return "/".join([str(ord(x)) for x in str(key + num)])

def description(key, string):
		return int("".join([str(chr(int(x))) for x in string.split("/")])) - key

def index(request):
		min = 1
		max = 100
		key = 10
		sumKey = 4

		if request.method == 'GET':
				mystery = random.randint(1, 100)
				attempt =  math.floor (math.log(max) / math.log(2) + 1)
				checksum = encryption(sumKey, mystery) + encryption(sumKey, attempt)

				template = loader.get_template('game/index.html')
				context = {
					"min": min,
					"max": max,

					"attemptEn": encryption(key, attempt),
					"mysteryEn":  encryption(key, mystery),
					"checksumEn": checksum,

					"answerText": '',
					"attempt": attempt,

					"endGame": False,
					"burglary": False
				}
				return HttpResponse(template.render(context, request))
		
		if request.method == 'POST':
				form = GameForm(request.POST)
				template = loader.get_template('game/index.html')
				if form.is_valid():
						mystery = +description(key, request.POST['mystery'])
						attempt = +description(key, request.POST['attempt'])
						checksum = request.POST['checksum']
						answerNum = int(request.POST['answer'])
						endGame = False
						burglary = False

						if checksum != encryption(sumKey, mystery) + encryption(sumKey, attempt):
								burglary = True

						attempt -= 1
						if answerNum < min or answerNum > max:
								attempt = attempt + 1
								answerText = "Число не входит в диапазон."
						elif answerNum == mystery:
								endGame = True
								answerText = "Вы выиграли! Загаданное число: " + str(mystery)
						elif attempt == 0:
								endGame = True
								answerText = "Вы проиграли! Загаданное число: " + str(mystery)
						else:
								answerText = "Загаданное число "
								if (answerNum > mystery):
										answerText += "меньше "
								else:
										answerText += "больше "
								answerText += str(answerNum) + "."

						context = {
								"min": min,
								"max": max,

								"attemptEn": encryption(key, attempt),
								"mysteryEn":  encryption(key, mystery),
								"checksumEn": encryption(sumKey, mystery) + encryption(sumKey, attempt),

								"answerText": answerText,
								"attempt": attempt,

								"endGame": endGame,
								"burglary": burglary
						}
						return HttpResponse(template.render(context, request))

