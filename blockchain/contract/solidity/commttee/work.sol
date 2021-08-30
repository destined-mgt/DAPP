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

contract work {
    //推动奖励
    event reward(address who, uint256 money);
    //模型可以提交啦
    event submitModel(uint256 startTime);
    //有模型验证！
    event verifyModel(uint256 startTime);
    //有模型合并!
    event mergeModel(uint256 startTime);
    //模型打分情况
    event modelscore(bytes32 model, uint score);
    //最终模型
    event finalscore(bytes32 model, uint score);

    // 模型属于谁
    mapping(bytes32 => address) whosModel;
    // 模型的父模型是谁
    mapping(bytes32 => bytes32) modelFather;

    // 待合并队列
    bytes32[]  public MQ;
    // 合并之后的验证队列
    bytes32[]  public VQ;

    //初始提交模型时间
    uint256 sbumitModelTime = 10 seconds;
    uint256 startSubmitModelTime = 0;

    uint256 verifyModelTime = 1 seconds;
    uint256 startVerifyModelTime = 0;
    uint256 mergeModelTime = 5 seconds;
    uint256 startMergeModelTime = 0;

    //VQ的队列指针
    uint public  pVQ = 0;
    //MQ的队列指针
    uint public pMQ = 0;

    //最终模型准率率
    uint finalAcc = 0;

    //模型合并数
    uint k = 0;

    //模型准确率统计
    //某人说，某个模型多少分
    //统计所有说话的人
    mapping(address => uint) modelAcc;
    address [] people;


    //触发开关
    function StartSubmitModel() private {
        //做一些阶段初始化工作
        delete VQ;
        pVQ = 0;
        //准备发布事件
        startSubmitModelTime = now;
        emit submitModel(startSubmitModelTime);
    }

    // 普通节点调用
    // 参与节点提交模型
    // 模型严格按照上传顺序进行打分
    // 当上一个模型没有完成打分，当前模型旧不能上传新模型
    function SubmitModel(manager mag,bytes32 swarmID) public returns (bool) {
        require(mag.GetStatus() == 11);
        if (whosModel[swarmID] == (address)(0)) {
            VQ.push(swarmID);
        }
        //记录
        whosModel[swarmID] = msg.sender;
        return true;
    }
    //结束开关
    function EndSubmitModel() private returns (bool){
        if (VQ.length <= 0) {
            return false;
        }
        for (uint i = 0; i < VQ.length; i++) {
            bytes32 model = VQ[i];
            whosModel[model] = (address)(0);
        }
        return true;
    }

    function GetModelToVerify(manager mag) public view returns (bytes32){
        require(mag.GetStatus() == 13);
        //验证身份
        if (pVQ >= VQ.length) {
            require(false, "VQ,Empty");
        }
        //指针前移
        bytes32 model = VQ[pVQ];
        //返回模型
        return model;
    }

    function StartVerifyModel() private {
        pMQ = 0;
        delete MQ;
        delete people;
        startVerifyModelTime = now;
        emit verifyModel(startVerifyModelTime);
    }

    //验证函数,接收结果
    function Verify(manager mag,uint acc) public {
        require(mag.GetStatus() == 13);
        if (modelAcc[msg.sender] == 0) {
            people.push(msg.sender);
        }
        modelAcc[msg.sender] = acc;
    }
    //结束某个模型的验证
    function EndVerify() private returns (bool){
        if (people.length == 0) {
            return false;
        }

        uint [] memory totalAcc = new uint[](people.length);

        for (uint i = 0; i < people.length; i++) {
            totalAcc[i] = modelAcc[people[i]];
        }
        //准确率排序
        QSort(totalAcc, 0, totalAcc.length - 1);
        //确定中位数准确率
        uint mid = totalAcc[totalAcc.length / 2];

        for (uint i = 0; i < people.length; i++) {
            uint acc = modelAcc[people[i]];
            //清空数据
            modelAcc[people[i]] = 0;
            //变式写法
            if (Abs((int)(acc - mid)) * 10 <= mid) {
                //得一分
            }
            if (Abs((int)(acc - mid)) * 10 > 2 * mid) {
                //作恶一次
            }
            //模型记录
        }
        //经过验证的模型与之前投票确定的模型准确率基本线c比较
        //满足基线即可进入队列,兑现奖励，不满足需要看是不是合并模型，如果是那么需要还原
        //如果不是，那么就需要对提交该模型的节点做出惩罚
        //NOTICE！暂时不比较c
        emit modelscore(VQ[pVQ], mid);
        finalAcc = mid;
        MQ.push(VQ[pVQ]);
        //队列指针自增
        pVQ += 1;
        return true;
    }

    function StartMergeModel() private {
        pVQ = 0;
        delete VQ;
        mergeModelTime = now;
        emit mergeModel(mergeModelTime);
    }

    function GetModelsToMerge(manager mag) public returns (bytes32[] memory){
        //验证
        require(mag.GetStatus() == 15);

        k = GenK();
        //验证身份
        bytes32[] memory models = new bytes32[](k);

        if (pMQ >= MQ.length) {
            require(false, "MQ,Empty");
        }
        for (uint i = 0; i < k; i++) {
            models[i] = MQ[pMQ + i];
        }
        return models;
    }

    function Merge(manager mag,bytes32 model) public {
        require(mag.GetStatus() == 15);
        whosModel[model] = msg.sender;
        for (uint i = 0; i < k; i++) {
            //父亲模型
            modelFather[MQ[i]] = model;
        }
        pMQ += k;
        //进入队列
        VQ.push(model);
    }

    function EndMerge() private view returns (bool) {
        if (pMQ >= MQ.length) {
            return true;
        }
        return false;
    }

    //推进函数
    function NextStep(manager mag) public returns (uint, bool){
        bool isSuc = false;
        //委员会节点身份判定
        if (mag.GetStatus() == 10) {
            //进入下一个状态，模型提交
            //公布奖励信息
            emit reward(msg.sender, 1);
            //调用阶段初始化函数
            StartSubmitModel();
            //状态变更
            mag.SetStatus(11);
            isSuc = true;
        } else if (mag.GetStatus() == 11) {
            if (startSubmitModelTime + sbumitModelTime < now) {
                if (EndSubmitModel()) {
                    mag.SetStatus(12);
                    isSuc = true;
                } else {
                    emit submitModel(startSubmitModelTime);
                }
            } else {
                emit submitModel(startSubmitModelTime);
            }

        } else if (mag.GetStatus() == 12) {
            //进入下一状态，模型的打分
            //公布奖励信息
            emit reward(msg.sender, 1);
            //调用阶段初始化函数
            StartVerifyModel();
            mag.SetStatus(13);
            isSuc = true;
        } else if (mag.GetStatus() == 13) {
            //结束某一个模型的验证
            if (startVerifyModelTime + verifyModelTime < now) {
                if (EndVerify()) {
                    //是否彻底结束了验证，需要看验证队列中是否还存在数值
                    if (pVQ >= VQ.length) {
                        //如果此时，合并队列中仅有一个模型，意味着阶段结束
                        if (MQ.length == 1) {
                            mag.SetStatus(16);
                            emit finalscore(MQ[0], finalAcc);
                        } else {
                            //进入合并模式
                            mag.SetStatus(14);
                        }
                        isSuc = true;
                    } else {
                        //继续进行验证
                        emit verifyModel(startVerifyModelTime);
                    }
                } else {
                    //验证人数不足，继续发送消息
                    emit verifyModel(startVerifyModelTime);
                }
            } else {
                emit verifyModel(startVerifyModelTime);
            }
        } else if (mag.GetStatus() == 14) {
            //进入下一状态，模型的合并
            //公布奖励信息
            emit reward(msg.sender, 1);
            //调用阶段初始化函数
            StartMergeModel();
            mag.SetStatus(15);
            isSuc = true;
        } else if (mag.GetStatus() == 15) {
            //结束某一批次模型的合并
            if (startMergeModelTime + mergeModelTime < now) {
                if (EndMerge()) {
                    //进入验证状态
                    mag.SetStatus(12);
                    isSuc = true;
                } else {
                    emit mergeModel(startMergeModelTime);
                }
            } else {
                emit mergeModel(startMergeModelTime);
            }

        }
        return (mag.GetStatus(), isSuc);
    }

    function GenK() private view returns (uint){
        // uint cal = 2;
        // if (cal > MQ.length - pMQ) {
        //     cal = MQ.length - pMQ;
        // }
        uint256 cal = MQ.length - pMQ;
        return cal;
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

    function Abs(int num) public pure returns (uint) {
        if (num > 0) {
            return uint(num);
        } else {
            return uint(- num);
        }
    }


}