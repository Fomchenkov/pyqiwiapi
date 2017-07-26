import requests

"""
Simple Qiwi Api Wrapper.
See Qiwi Api Documentation: 
https://developer.qiwi.com/qiwiwallet/qiwicom_en.html
"""


class QiwiApi(object):
	"""
	Qiwi Api Class.
	Methods:
		get_tgt_ticket
		get_st_ticket
		get_payments_history
		get_payments_stat
		get_wallet_balance
	"""
	login = ''
	password = ''
	tgt_ticket = ''
	st_ticket = ''

	def __init__(self, login, password):
		self.login = login
		self.password = password

	def get_tgt_ticket(self):
		"""
		Get tgt ticket.
		:return: tgt ticket.
		"""
		s = requests.Session()
		url = 'https://auth.qiwi.com/cas/tgts'
		s.headers = {
			'content-type': 'application/json',
			'accept': 'application/vnd.qiwi.sso-v1+json'
		}
		params = {
			'login': self.login,
			'password': self.password
		}
		try:
			self.tgt_ticket = s.post(url, json=params).json()['entity']['ticket']
			return self.tgt_ticket
		except KeyError as e:
			print(r.text)
			raise e

	def get_st_ticket(self, need_payments=False):
		"""
		Get st ticket.
		:param need_payments: If True - allow payments.
		:return: st ticket.
		"""
		if not self.tgt_ticket:
			raise Exception('You need call get_tgt_ticket() method.')
		if need_payments:
			service = 'https://qiwi.com/j_spring_cas_security_check'
		else:
			service = 'http://t.qiwi.com/j_spring_cas_security_check'
		url = 'https://auth.qiwi.com/cas/sts'
		s = requests.Session()
		s.headers = {
			'content-type': 'application/json',
			'accept': 'application/vnd.qiwi.sso-v1+json'
		}
		params = {
			'service': service,	
			'ticket': self.tgt_ticket
		}
		try:
			self.st_ticket = s.post(url, json=params).json()['entity']['ticket']
			return self.st_ticket
		except KeyError as e:
			print(r.text)
			raise e

	def get_payments_history(self, rows, operation=None, 
							sources=None, startDate=None, endDate=None, 
							nextTxnDate=None, nextTxnId=None):
		"""
		Get payments history.
		:param rows:
		:param operation:
		:param sources:
		:param startDate:
		:param endDate:
		:param nextTxnDate:
		:param nextTxnId:
		:return: API repsponse JSON.
		"""
		if not self.st_ticket:
			raise Exception('You need call get_st_ticket() method.')
		params = {}
		if rows: params['rows'] = rows
		if operation: params['operation'] = operation
		if sources: params['sources'] = sources
		if startDate: params['startDate'] = startDate
		if endDate: params['endDate'] = endDate
		if nextTxnDate: params['nextTxnDate'] = nextTxnDate
		if nextTxnId: params['nextTxnId'] = nextTxnId
		url = 'https://edge.qiwi.com/payment-history/'
		url += 'v1/persons/{!s}/payments'.format(self.login)
		s = requests.Session()
		s.headers = {
			'content-type': 'application/json',
			'accept': 'application/json',
			'Authorization': 'Token {!s}'.format(self.st_ticket),
		}
		return s.get(url, params=params).json()

	def get_payments_stat(self, startDate=None, endDate=None, operation=None):
		"""
		Get payments statistic.
		:param startDate:
		:param endDate:
		:param operation:
		:param sources:
		:return: API reponse JSON.
		"""
		if not self.st_ticket:
			raise Exception('You need call get_st_ticket() method.')
		params = {}
		if startDate: params['startDate'] = startDate
		if endDate: params['endDate'] = endDate
		if operation: params['operation'] = operation
		s = requests.Session()
		url = 'https://edge.qiwi.com/payment-history/v1/'
		url += 'persons/{!s}/payments/total'.format(self.login)
		s.headers = {
			'content-type': 'application/json',
			'accept': 'application/json',
			'Authorization': 'Token {!s}'.format(self.st_ticket)
		}
		return s.get(url, params=params).json()

	def get_wallet_balance(self):
		"""
		Get wallet balance.
		:return: API response JSON.
		"""
		if not self.st_ticket:
			raise Exception('You need call get_st_ticket() method.')
		s = requests.Session()
		url = 'https://edge.qiwi.com/funding-sources/'
		url += 'v1/accounts/{!s}'.format(self.login)
		s.headers = {
			'content-type': 'application/json',
			'accept': 'application/json',
			'Authorization': 'Token {!s}'.format(self.st_ticket)
		}
		return s.get(url, params={}).json()
