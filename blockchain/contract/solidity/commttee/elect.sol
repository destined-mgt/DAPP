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

contract election {

    //开始设置
    event startSetting(uint256 startTime);
    //结束设置
    event endSetting(uint256 finalTime);
    //开始选举
    event startElect(uint256 startTime);
    //结束选举
    event endElect(address [] committees);
    //是否开始选举
    event reply(uint256 startTime);
    //新一轮选举
    event newLoop();
    //推动奖励
    event reward(address who, uint256 money);
    //工作阶段时间
    event work();

    //各个委员会节点在选举设置阶段决定的时间
    mapping(address => uint256)public times;
    //投入的时间
    uint256 [] public decidedTime;
    //参与投票的节点
    address []  public timeNodes;
    //设置阶段的时间间隔
    uint256 public settingTime = 5 seconds;
    //设置阶段的开始时间
    uint256 public settingStartTime;
    //设置阶段的结果
    uint256 public finalTime;
    //选举阶段的开始时间
    uint256 public electStartTime;
    //各个节点在选举阶段决定的时间资金投入
    mapping(address => uint256) public elect;
    //参与选举的节点
    address [] public electNodes;
    //选举的最终数值
    uint256 [] public decidedElect;
    //回应阶段时间间隔
    uint256 replyTime =  5 seconds;
    //回应阶段的启动者
    address replyStarter;
    //回应阶段的开始时间
    uint256 replyStartTime;
    //各个节点在回应阶段决定的是否回应
    mapping(address => bool) public rep;
    //参与回应的节点
    address [] public replyNodes;

    //外部用户无法调用，无需阶段限制
    function StartDecideTime(manager mag) private {
        for (uint i = 0; i < timeNodes.length; i++) {
            times[timeNodes[i]] = 0;
        }
        delete timeNodes;
        delete decidedTime;
        settingStartTime = now;
        //可以设置时间的信号
        emit startSetting(settingStartTime);
        mag.SetStatus(1);
    }

    //设置选举的最少消耗时间,调用者必须是委员会成员
    function DecideTime(manager mag, uint time) public {
        //因为外部用户可以调用，因此需要阶段限制
        require(mag.GetStatus() == 1);
        bool isCmt = false;
        isCmt = mag.IsCommiteeMember(msg.sender);
        require(isCmt);
        if (times[msg.sender] == 0 && time > 0) {
            times[msg.sender] = time;
            timeNodes.push(msg.sender);
        }
    }
    //外部用户无法调用，无需阶段限制
    function EndDecideTime(manager mag) private returns (bool){
        if (timeNodes.length<=0){
            return false;
        }
        uint256 totalPeople = mag.GetNumberOfNodes();
        //如果投票用户少于总用户数量的50%本轮设置无效，跳转回阶段1
        if (timeNodes.length * 2 < totalPeople) {
            //emit
            settingStartTime = now;
            //可以设置时间的信号
            emit startSetting(settingStartTime);
            return false;
        }
        for (uint i = 0; i < timeNodes.length; i++) {
            uint256 tempTime = times[timeNodes[i]];
            decidedTime.push(tempTime);
        }
        QSort(decidedTime, 0, decidedTime.length - 1);
        finalTime = decidedTime[uint((decidedTime.length - 1) / 2)];
        //结束设置的信号
        emit endSetting(finalTime);
        return true;
    }

    function StartElect(manager mag) private {
        //如果不取走钱，钱会被清除
        for (uint i = 0; i < electNodes.length; i++) {
            address node = electNodes[i];
            elect[node] = 0;
        }
        delete electNodes;
        delete decidedElect;
        electStartTime = now;
        emit startElect(electStartTime);
        mag.SetStatus(3);
    }

    function Elect(manager mag) public payable {
        require(mag.GetStatus() == 3);
        if (elect[msg.sender] == 0 && msg.value > 0) {
            elect[msg.sender] = msg.value;
            electNodes.push(msg.sender);
        }
    }

    function EndElect(manager mag) private returns (bool){
        for (uint i = 0; i < electNodes.length; i++) {
            uint256 tempElect = elect[electNodes[i]];
            //需要向管理器获取竞选节点的平均准确率acc
            decidedElect.push(tempElect);
        }
        if (decidedElect.length <= 0) {
            //状态回退
            settingStartTime = now;
            //可以设置时间的信号
            emit startSetting(settingStartTime);
            return false;
        }

        QSort(decidedElect, 0, decidedElect.length - 1);
        uint256 upperLimit = GetUpperLimit(mag);
        uint256 lowerLimit = GetLowerLimit(mag);
        //为了测试
        lowerLimit = 0;
        upperLimit = 10000;
        if (decidedElect.length < lowerLimit) {
            //状态回退
            settingStartTime = now;
            //可以设置时间的信号
            emit startSetting(settingStartTime);
            return false;
        } else {
            if (decidedElect.length > upperLimit) {
                address[] memory committee = new address[](upperLimit);
                for (uint i = 0; i < upperLimit; i++) {
                    committee[i] = electNodes[i];
                }
                //向节点公布竞选结果但还没有向节点管理器做最终提交
                emit endElect(committee);
            } else {
                address[] memory committee = new address[](decidedElect.length);
                for (uint i = 0; i < electNodes.length; i++) {
                    committee[i] = electNodes[i];
                }
                emit endElect(committee);
            }
        }
        return true;
    }

    function StartReply(manager mag) private {
        for (uint i = 0; i < replyNodes.length; i++) {
            rep[replyNodes[i]] = false;
        }
        delete replyNodes;
        replyStartTime = now;
        //启动者
        replyStarter = msg.sender;
        //可以设置时间的信号
        emit reply(replyStartTime);
        mag.SetStatus(17);
    }

    function Reply(manager mag) public {
        //选举结束阶段才能启动回应阶段
        require(mag.GetStatus() == 17);
        //必须是委员会节点
        bool isCmt = false;
        isCmt = mag.IsCommiteeMember(msg.sender);
        require(isCmt);
        //
        if (!rep[msg.sender]) {
            rep[msg.sender] = true;
            replyNodes.push(msg.sender);
        }
    }

    function EndReply(manager mag) private returns (bool){
        //获取结果
        bool result = replyNodes.length * 2 >= ToGetNumberOfNodes(mag);
        if (result) {
            emit newLoop();
            return true;
        } else {
            //返回状态
            emit work();
            return false;
        }
    }
    //
    function ToGetNumberOfNodes(manager mag) public returns (uint256){
        return mag.GetNumberOfNodes();
    }
    //
    function GetUpperLimit(manager mag) public returns (uint256){
        return uint256(ToGetNumberOfNodes(mag));
    }

    function GetLowerLimit(manager mag) public returns (uint256){
        return uint256(ToGetNumberOfNodes(mag));
    }

    //
    function NextStep(manager mag) public returns (uint, bool){
        require(mag.IsCommiteeMember(msg.sender));
        bool isSuc=false;
        if (mag.GetStatus() == 0) {
            emit reward(msg.sender, 1);
            StartDecideTime(mag);
            isSuc=true;
        }
        else if (mag.GetStatus() == 1) {
            if (settingStartTime + settingTime < now) {
                //是否顺利推动
                if (EndDecideTime(mag)) {
                    //顺利推动，进入2阶段
                    emit reward(msg.sender, 1);
                    mag.SetStatus(2);
                    isSuc=true;
                } else {
                    //不顺利推动,返回1阶段
                    mag.SetStatus(1);
                    emit startSetting(settingStartTime);
                }
            } else {
                emit startSetting(settingStartTime);
            }
        } else if (mag.GetStatus() == 2) {
            emit reward(msg.sender, 1);
            StartElect(mag);
            isSuc=true;
        } else if (mag.GetStatus() == 3) {
            if (electStartTime + finalTime < now) {
                if (EndElect(mag)) {
                    emit reward(msg.sender, 1);
                    mag.SetStatus(4);
                    isSuc=true;
                } else {
                    mag.SetStatus(1);
                    emit startElect(electStartTime);
                }
            } else {
                emit startElect(electStartTime);
            }

        } else if (mag.GetStatus() == 16) {
            emit reward(msg.sender, 1);
            StartReply(mag);
            isSuc=true;
        }
        else if (mag.GetStatus() == 17) {
            if (replyStartTime + replyTime < now) {
                if (EndReply(mag)) {
                    //只有成功状态，发起者才有奖励
                    emit reward(replyStarter, 1);
                    //状态转移
                    mag.SetStatus(0);
                    isSuc=true;
                } else {
                    //状态转移
                    mag.SetStatus(16);
                    emit reply(replyStartTime);
                }
            } else {
                emit reply(replyStartTime);
            }

        }
        return (mag.GetStatus(), isSuc);
    }
    //只有在012状态是可以退钱的
    function Refund(manager mag) public returns (bool) {
        require(mag.GetStatus() == 0 || mag.GetStatus() == 1 || mag.GetStatus() == 2);
        uint256 amount = elect[msg.sender];
        if (amount > 0) {
            //首先要设置0，不要打乱逻辑顺序
            elect[msg.sender] = 0;
            if (!msg.sender.send(amount)) {
                elect[msg.sender] = amount;
                return false;
            }
        }
        return true;
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
