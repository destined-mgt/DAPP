abi = [
    {
        "inputs": [
            {
                "internalType": "contract manager",
                "name": "mag",
                "type": "address"
            }
        ],
        "name": "Buy",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "startTime",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "price",
                "type": "uint256"
            }
        ],
        "name": "buyModel",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "startTime",
                "type": "uint256"
            }
        ],
        "name": "decidePrice",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "contract manager",
                "name": "mag",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "argPrice",
                "type": "uint256"
            }
        ],
        "name": "DecidePrice",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "price",
                "type": "uint256"
            }
        ],
        "name": "finalPrice",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "contract manager",
                "name": "mag",
                "type": "address"
            }
        ],
        "name": "NextStep",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            },
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "who",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "money",
                "type": "uint256"
            }
        ],
        "name": "reward",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "GetPrice",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256[]",
                "name": "arr",
                "type": "uint256[]"
            },
            {
                "internalType": "uint256",
                "name": "left",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "right",
                "type": "uint256"
            }
        ],
        "name": "QSort",
        "outputs": [],
        "stateMutability": "pure",
        "type": "function"
    }
]
