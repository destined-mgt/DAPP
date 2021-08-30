// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0 <0.7.0;

contract Transer {

    // fileID=>reciver
    mapping(uint256 => address) private reciverMapping;

    // fileID=>sender
    mapping(uint256 => address) private senderMapping;

    // fileID=>exist
    mapping(uint256 => bool) private existMapping;

    //fileId=>swarmId
    mapping(uint256 => bytes32)private swarmIdMapping;

    //event for client to listen
    event ToWhom(address who, uint256 fileID);

    //fileID
    uint256 private fileIncId;


    function ReciveFile(uint256 fileId) public returns (bytes32){
        require(msg.sender == reciverMapping[fileId], "You are not the reciver.");

        require(existMapping[fileId], "File not exist.");

        existMapping[fileId] = false;

        return swarmIdMapping[fileId];
    }

    function SendFile(bytes32 swarmId, address reciver) public {
        //storage file and get a fileId
        uint256 fileId = fileIncId;
        swarmIdMapping[fileId] = swarmId;
        reciverMapping[fileId] = reciver;
        existMapping[fileId] = true;
        senderMapping[fileId] = msg.sender;
        //emit ToWhom
        emit ToWhom(reciver, fileId);
        // inc the fileId
        fileIncId += 1;
    }
}