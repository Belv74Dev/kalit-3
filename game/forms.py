from django import forms

class GameForm(forms.Form):
	attempt = forms.CharField(label='attemptEn')
	mystery = forms.CharField(label='mysteryEn')
	checksum = forms.CharField(label='checksumEn')
	answer = forms.CharField(label='answerEn')