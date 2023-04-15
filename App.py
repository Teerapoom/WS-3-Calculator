from flask import render_template, jsonify, request
import re

from web3 import Web3
from flask import Flask

from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app)

ABI = [{
			"inputs": [
				{
					"internalType": "int256",
					"name": "num1",
					"type": "int256"
				},
				{
					"internalType": "int256",
					"name": "num2",
					"type": "int256"
				}
			],
			"name": "add",
			"outputs": [
				{
					"internalType": "int256",
					"name": "",
					"type": "int256"
				}
			],
			"stateMutability": "pure",
			"type": "function"
		},
		{
			"inputs": [
				{
					"internalType": "int256",
					"name": "num1",
					"type": "int256"
				},
				{
					"internalType": "int256",
					"name": "num2",
					"type": "int256"
				}
			],
			"name": "div",
			"outputs": [
				{
					"internalType": "int256",
					"name": "",
					"type": "int256"
				}
			],
			"stateMutability": "pure",
			"type": "function"
		},
		{
			"inputs": [
				{
					"internalType": "int256",
					"name": "num1",
					"type": "int256"
				},
				{
					"internalType": "int256",
					"name": "num2",
					"type": "int256"
				}
			],
			"name": "mul",
			"outputs": [
				{
					"internalType": "int256",
					"name": "",
					"type": "int256"
				}
			],
			"stateMutability": "pure",
			"type": "function"
		},
		{
			"inputs": [
				{
					"internalType": "int256",
					"name": "num1",
					"type": "int256"
				},
				{
					"internalType": "int256",
					"name": "num2",
					"type": "int256"
				}
			],
			"name": "sub",
			"outputs": [
				{
					"internalType": "int256",
					"name": "",
					"type": "int256"
				}
			],
			"stateMutability": "pure",
			"type": "function"
		}]

ABI_ADDRESS = "0x77844B76a65e33B843bc2e0Cd3315Fa1BB51d727"


web3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))

class contractMethod:
    def __init__(self):
        self.contract = web3.eth.contract(address=ABI_ADDRESS, abi=ABI)

    def add(self, a, b):
        return self.contract.functions.add(a, b).call()

    def sub(self, a, b):
        return self.contract.functions.sub(a, b).call()

    def mul(self, a, b):
        return self.contract.functions.mul(a, b).call()

    def div(self, a, b):
        return self.contract.functions.div(a, b).call()

contract = contractMethod()

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/calculate', methods=['POST'])
def result():
    data = request.get_json()
    equation = data['equation']
    if re.match(r'^\d+[\+\-\*\/]\d+$', equation):
        a, operator, b = re.split(r'([\+\-\*\/])', equation)
        a = int(a)
        b = int(b)
        switcher = {
            '+': contract.add(a, b),
            '-': contract.sub(a, b),
            '*': contract.mul(a, b),
            '/': contract.div(a, b)
        }
        result = switcher.get(operator, 'Invalid Equation')

    else:
        result = 'Invalid Equation'

    return jsonify({'result': result})


if __name__ == '__main__':
	app.run(debug=True)