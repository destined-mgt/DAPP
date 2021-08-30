// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.6.0 <0.7.0;

abstract contract manager {
    //获取节点数量
    function GetNumberOfNodes() virtual public returns (uint256);
    //判断是否为委员会成员
    function IsCommiteeMember(address) virtual public returns (bool);
    //报告选举出的新委员会
    function NewCommittee(address[] memory) virtual public returns (bool);
    function GetStatus() virtual public view returns(uint);
    function SetStatus(uint) virtual public;
}


//用于选定工作参数c以及其他

contract workArg {

    //推动奖励
    event reward(address who, uint256 money);

    event decideC(uint startTime);

    event finalC(uint c);

    uint private c = 0;

    address [] public whosAcc;

    mapping(address => uint) acc;

    uint startDecideCTime = 0;
    uint decideCTime = 5 seconds;

    function StartDecideC() private {
        startDecideCTime = now;
        emit decideC(startDecideCTime);
    }

    function DecideC(manager mag,uint argacc) public {
        require(mag.GetStatus()==9,"status!=1");
        if (acc[msg.sender] == 0) {
            whosAcc.push(msg.sender);
        }
        acc[msg.sender] = argacc;
    }

    function EndDecideC() private returns (bool) {
        //写死，默认测试节点10
        if (whosAcc.length <=0) {
            return false;
        }
        uint [] memory accs = new uint[](whosAcc.length);

        for (uint i = 0; i < whosAcc.length; i++) {
            address sender = whosAcc[i];
            accs[i] = acc[sender];
        }

        QSort(accs, 0, accs.length - 1);
        c = accs[accs.length / 2];
        for (uint i = 0; i < whosAcc.length; i++) {
            address sender = whosAcc[i];
            acc[sender] = 0;
        }
        delete whosAcc;
        emit finalC(c);
        return true;
    }
    function GetC() view public returns (uint){
        return c;
    }
    function NextStep(manager mag) public returns(uint,bool){
        bool res=false;
        //判定是否是委员会节点
        if (mag.GetStatus() == 8) {
            emit reward(msg.sender, 1);
            StartDecideC();
            mag.SetStatus(9);
            res=true;
        } else if (mag.GetStatus() == 9) {
            if (startDecideCTime + decideCTime < now) {
                if (EndDecideC()) {
                    mag.SetStatus(10);
                    res=true;
                } else {
                    emit decideC(startDecideCTime);
                }
            } else {
                emit decideC(startDecideCTime);
            }
        }
        return(mag.GetStatus(),res);
    }
    function QSort(uint256[] memory arr, uint left, uint right) public pure {
        uint i = left;
        uint j = right;
        if (i == j) return;
        uint pivot = arr[uint(left + (right - left) / 2)];
        while (i <= j) {
            while (arr[uint(i)] < pivot) i++;
            while (pivot < arr[uint(j)]) j--;
            if (i <= j) {
                (arr[uint(i)], arr[uint(j)]) = (arr[uint(j)], arr[uint(i)]);
                i++;
                j--;
            }
        }
        if (left < j)
            QSort(arr, left, j);
        if (i < right)
            QSort(arr, i, right);
    }
}
