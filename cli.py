# Testing script
# append the root project path to the pythonpath so that blockchain.py can be accessed by every adapter

import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))
from PyInquirer import prompt, print_json, style_from_dict, Token, Separator
from blockchain import Blockchain
import api

def askForMethod():
	questions = [
		{
			'type': 'list',
			'message': 'Select action',
			'name': 'action',
			'choices': [
				{
					'name': 'Store'
				},
				{
					'name': 'Retrieve'
				},
				{
					'name': 'Migrate'
				},
			],
			# 'validate': lambda output: True if (output == "Store") else False
		},

	]
	try:
		answer = prompt(questions)['action']
		if(answer == 'Store'):
			caseStore()
		elif(answer == 'Retrieve'):
			caseRetrieve()
		elif(answer == 'Migrate'):
			caseMigrate()
	except (KeyboardInterrupt, SystemExit):
		raise
	except (KeyError):
		print('Exiting...')


def caseStore():
	questions = [
		{
			'type': 'list',
			'message': 'Select action',
			'name': 'blockchain',
			'choices': [
				{
					'name': 'Bitcoin',
					'value': Blockchain.BITCOIN,
				},
				{
					'name': 'Ethereum',
					'value': Blockchain.ETHEREUM,
				},
				{
					'name': 'Stellar',
					'value': Blockchain.STELLAR,
				},
				{
					'name': 'EOS',
					'value': Blockchain.EOS,
				},
				{
					'name': 'IOTA',
					'value': Blockchain.IOTA,
				},
				{
					'name': 'Hyperledger',
					'value': Blockchain.HYPERLEDGER,
				},
				{
					'name': 'Multichain',
					'value': Blockchain.MULTICHAIN,
				},
				{
					'name': 'Postgres',
					'value': Blockchain.POSTGRES,
				},
				{
					'name': 'Monero',
					'value': Blockchain.MONERO,
				},
				{
					'name': 'Litecoin',
					'value': Blockchain.LITECOIN,
				},				
				{
					'name': 'Ripple',
					'value': Blockchain.RIPPLE,
				},
			],
		},
		{
			'type': 'input',
			'name': 'data',
			'message': 'Please input the data to store',
		}
	]
	answer = prompt(questions)
	api.store(answer['data'], answer['blockchain'])



def caseRetrieve():	
	questions = [
		{
			'type': 'input',
			'name': 'hash',
			'message': 'Please input the transaction hash',
		}
	]
	answer = prompt(questions)
	api.retrieve(answer['hash'])

def caseMigrate():
	questions = [
		{
			'type': 'input',
			'name': 'hash',
			'message': 'Please input the hash of the transaction connected to the data',
		},
		{
			'type': 'list',
			'name': 'blockchain',
			'message': 'Please select which Blockchain to migrate to',
			'choices': [
				{
					'name': 'Bitcoin',
					'value': Blockchain.BITCOIN,
				},
				{
					'name': 'Ethereum',
					'value': Blockchain.ETHEREUM,
				},
				{
					'name': 'Stellar',
					'value': Blockchain.STELLAR,
				},
				{
					'name': 'EOS',
					'value': Blockchain.EOS,
				},
				{
					'name': 'IOTA',
					'value': Blockchain.IOTA,
				},
				{
					'name': 'Hyperledger',
					'value': Blockchain.HYPERLEDGER,
				},
				{
					'name': 'Multichain',
					'value': Blockchain.MULTICHAIN,
				},
				{
					'name': 'Postgres',
					'value': Blockchain.POSTGRES,
				},
				{
					'name': 'Monero',
					'value': Blockchain.MONERO,
				},
				{
					'name': 'Litecoin',
					'value': Blockchain.LITECOIN,
				},
				{
					'name': 'Ripple',
					'value': Blockchain.RIPPLE,
				},
			],
		},
	]
	answer = prompt(questions)
	api.migrate(answer['hash'], answer['blockchain'])

askForMethod()
