abi = [
    {
        "inputs": [
            {
                "internalType": "contract manager",
                "name": "mag",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "time",
                "type": "uint256"
            }
        ],
        "name": "DecideTime",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract manager",
                "name": "mag",
                "type": "address"
            }
        ],
        "name": "Elect",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address[]",
                "name": "committees",
                "type": "address[]"
            }
        ],
        "name": "endElect",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "finalTime",
                "type": "uint256"
            }
        ],
        "name": "endSetting",
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
        "name": "GetLowerLimit",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract manager",
                "name": "mag",
                "type": "address"
            }
        ],
        "name": "GetUpperLimit",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [],
        "name": "newLoop",
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
        "inputs": [
            {
                "internalType": "contract manager",
                "name": "mag",
                "type": "address"
            }
        ],
        "name": "Refund",
        "outputs": [
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
                "internalType": "uint256",
                "name": "startTime",
                "type": "uint256"
            }
        ],
        "name": "reply",
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
        "name": "Reply",
        "outputs": [],
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
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "startTime",
                "type": "uint256"
            }
        ],
        "name": "startElect",
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
        "name": "startSetting",
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
        "name": "ToGetNumberOfNodes",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [],
        "name": "work",
        "type": "event"
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
