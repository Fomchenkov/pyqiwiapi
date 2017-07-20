import json
import requests


class Qiwi(object):
	"""
	Python Qiwi API wrapper
	"""
	def __init__(self, login, password):
		self.login = login
		self.password = password

	def get_tgt_ticket(self):
		"""
		Get tgt qiwi ticket
		"""
		s = requests.Session()
		user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
		user_agent += ' (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		header = {
			'content-type': 'application/json',
			'X-Requested-With':'XMLHttpRequest',
			'User-Agent': user_agent
		}
		s.headers = header
		json_data = {
			'login': self.login,
			'password': self.password
		}
		r = s.post('https://auth.qiwi.com/cas/tgts', json=json_data)
		try:
			self.tgt_ticket = json.loads(r.text)['entity']['ticket']
		except KeyError as e:
			print(r.text)
			raise e
		return self.tgt_ticket

	def get_st_ticket(self, service='http://t.qiwi.com/j_spring_cas_security_check'):
		"""
		Get st qiwi ticket
		"""
		s = requests.Session()
		user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
		user_agent += ' (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		header = {
			'content-type': 'application/json',
			'X-Requested-With':'XMLHttpRequest',
			'User-Agent': user_agent
		}
		s.headers = header
		json_data = {
			'service': service,
			'ticket': self.tgt_ticket
		}
		r = s.post('https://auth.qiwi.com/cas/sts', json=json_data)
		try:
			self.st_ticket = json.loads(r.text)['entity']['ticket']
		except KeyError as e:
			print(r.text)
			raise e
		return self.st_ticket

	def get_payment_history(self, params):
		"""
		Get payment history
		"""
		s = requests.Session()
		url = 'https://edge.qiwi.com/payment-history/v1/persons/{!s}/payments'.format(self.login)
		user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
		user_agent += ' (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
		header = {
			'content-type': 'application/json',
			'X-Requested-With':'XMLHttpRequest',
			'User-Agent': user_agent,
			'Authorization': 'Token {!s}'.format(self.st_ticket)
		}
		s.headers = header
		r = s.get(url, params=params)
		return json.loads(r.text)
