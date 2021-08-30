abi = [
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
        "name": "decideC",
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
                "name": "argacc",
                "type": "uint256"
            }
        ],
        "name": "DecideC",
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
                "name": "c",
                "type": "uint256"
            }
        ],
        "name": "finalC",
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
        "name": "GetC",
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
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "whosAcc",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
