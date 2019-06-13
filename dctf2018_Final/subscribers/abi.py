abi = [
	{
		"constant": True,
		"inputs": [
			{
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "getSubscriber",
		"outputs": [
			{
				"name": "subscriber",
				"type": "address"
			},
			{
				"name": "subscription",
				"type": "uint256"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [],
		"name": "disableRegistration",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "subscriber",
				"type": "address"
			},
			{
				"name": "subscription",
				"type": "uint256"
			}
		],
		"name": "subscribe",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "deleteRegistration",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"name": "id",
				"type": "uint256"
			}
		],
		"name": "isVIP",
		"outputs": [
			{
				"name": "subscriber",
				"type": "address"
			},
			{
				"name": "vip",
				"type": "bool"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [],
		"name": "enableRegistration",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"name": "_from",
				"type": "address"
			}
		],
		"name": "EnabledRegistration",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"name": "_from",
				"type": "address"
			}
		],
		"name": "DisabledRegistration",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"name": "_subscriber",
				"type": "address"
			},
			{
				"indexed": False,
				"name": "_subscription",
				"type": "uint256"
			}
		],
		"name": "newSubscription",
		"type": "event"
	},
	{
		"anonymous": False,
		"inputs": [
			{
				"indexed": False,
				"name": "_id",
				"type": "uint256"
			},
			{
				"indexed": False,
				"name": "_subscriber",
				"type": "address"
			},
			{
				"indexed": False,
				"name": "_subscription",
				"type": "uint256"
			}
		]
    }]