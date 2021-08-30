abi = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "model",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "score",
                "type": "uint256"
            }
        ],
        "name": "finalscore",
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
        "name": "mergeModel",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "model",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "score",
                "type": "uint256"
            }
        ],
        "name": "modelscore",
        "type": "event"
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
        "name": "submitModel",
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
        "name": "verifyModel",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "int256",
                "name": "num",
                "type": "int256"
            }
        ],
        "name": "Abs",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "pure",
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
        "name": "GetModelToVerify",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
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
        "name": "GetModelsToMerge",
        "outputs": [
            {
                "internalType": "bytes32[]",
                "name": "",
                "type": "bytes32[]"
            }
        ],
        "stateMutability": "nonpayable",
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
        "name": "MQ",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "contract manager",
                "name": "mag",
                "type": "address"
            },
            {
                "internalType": "bytes32",
                "name": "model",
                "type": "bytes32"
            }
        ],
        "name": "Merge",
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
                "internalType": "contract manager",
                "name": "mag",
                "type": "address"
            },
            {
                "internalType": "bytes32",
                "name": "swarmID",
                "type": "bytes32"
            }
        ],
        "name": "SubmitModel",
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
        "inputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "name": "VQ",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
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
                "name": "acc",
                "type": "uint256"
            }
        ],
        "name": "Verify",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "pMQ",
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
        "inputs": [],
        "name": "pVQ",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]
