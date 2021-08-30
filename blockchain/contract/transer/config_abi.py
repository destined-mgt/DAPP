abi = [
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
                "name": "fileID",
                "type": "uint256"
            }
        ],
        "name": "ToWhom",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "fileId",
                "type": "uint256"
            }
        ],
        "name": "ReciveFile",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "swarmId",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "reciver",
                "type": "address"
            }
        ],
        "name": "SendFile",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    }
]
