
// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0 <0.7.0;


contract manager {
    //每个节点的活跃度
    mapping(address => bool) private nodes;
    //活跃节点，指的是本轮购买模型的节点
    address [] private activeNodes;
    //活跃节点数量
    uint256 private sumOfNodes;
    //委员会节点
    address[] private committees;
    //委员会节点判定
    mapping(address => bool) private isCommittees;
    //选举合约的地址，仅仅接收固定合约传递的选举结果
    address private elect;
    //是不是第一次设置
    bool private isFstSetForElect;
    //购买合约的地址,仅仅接收固定合约传递的选举结果
    address private buy;
    //是不是第一次设置
    bool private isFstSetForBuy;
    uint status=0;

    function GetStatus() public view returns(uint){
        return status;
    }
    function SetStatus(uint st) public {
        status=st;
    }

    //节点注册，可以任意注册
    function Register() public returns (bool){
        if (nodes[msg.sender] == false) {
            nodes[msg.sender] = true;
            sumOfNodes++;
            return true;
        }
        return false;
    }
    //获取活跃节点数量
    function GetNumberOfNodes() view public returns (uint256) {
        return sumOfNodes;
    }
    //获取委员会节点的数量
    function GetNumberOfCommittee() view public returns (uint256){
        return committees.length;
    }
    //委员会节点判断
    function IsCommiteeMember(address addr) view public returns (bool) {
        return true;
        return isCommittees[addr];
    }
    //接收到的委员会名单会进行进一步验证
    function NewCommittee(address[] memory newCommittee) public returns (bool) {
        //固定地址
        if (msg.sender != elect) {
            return false;
        }
        committees = newCommittee;
        return true;

    }

    function SetElect(address addr) public returns (bool){
        if (isFstSetForElect == false) {
            isFstSetForElect = true;
            elect = addr;
            return true;
        }
        return false;
    }

    function SetBuy(address addr) public returns (bool){
        if (isFstSetForBuy == false) {
            isFstSetForBuy = true;
            buy = addr;
            return true;
        }
        return false;
    }

    //推动
    //每隔一分钟，系统征集心跳包
    function NextStep() public {

    }

}