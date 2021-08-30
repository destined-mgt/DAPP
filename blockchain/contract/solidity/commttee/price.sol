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


contract modelPrice {
    //推动奖励
    event reward(address who, uint256 money);

    event decidePrice(uint startTime);

    event finalPrice(uint price);

    event buyModel(uint startTime,uint price);

    uint private p = 0;

    address [] whosPrice;
    mapping(address => uint) price;
    uint startDecidePriceTime = 0;
    uint decidePriceTime = 5 seconds;

    address [] whosMoney;
    mapping(address => uint) money;
    uint startBuyTime = 0;
    uint buyTime = 5 seconds;

    function StartDecidePrice() private {
        startDecidePriceTime = now;
        emit decidePrice(startDecidePriceTime);
    }

    function DecidePrice(manager mag,uint argPrice) public {
        require(mag.GetStatus()==5,'status!=5');
        if (price[msg.sender] == 0) {
            whosPrice.push(msg.sender);
        }
        price[msg.sender] = argPrice;
    }

    function EndDecidePrice() private returns (bool) {

        //写死，默认测试节点10
        if (whosPrice.length <=0) {
            return false;
        }
        uint [] memory prices = new uint[](whosPrice.length);

        for (uint i = 0; i < whosPrice.length; i++) {
            address sender = whosPrice[i];
            prices[i] = price[sender];
        }

        QSort(prices, 0, prices.length - 1);
        p = prices[prices.length / 2];
        for (uint i = 0; i < whosPrice.length; i++) {
            address sender = whosPrice[i];
            price[sender] = 0;
        }
        delete whosPrice;
        emit finalPrice(p);
        return true;
    }

    function StartBuy() private {
        startBuyTime=now;
        emit buyModel(startBuyTime,p);
    }
    function Buy(manager mag) public payable{
        require(mag.GetStatus()==7,'status!=7');
        require(msg.value >= p,'value<price');
        if (money[msg.sender] == 0) {
            whosMoney.push(msg.sender);
        }
        money[msg.sender] = msg.value;
    }
    function EndBuy()private returns(bool){
        return true;
    }

    function GetPrice() view public returns (uint){
        return p;
    }

    function NextStep(manager mag) public returns(uint,bool){
        bool res=false;
        //判定是否是委员会节点
        if (mag.GetStatus() == 4) {
            emit reward(msg.sender, 1);
            StartDecidePrice();
            mag.SetStatus(5);
            res=true;
        } else if (mag.GetStatus() == 5) {
            if (startDecidePriceTime + decidePriceTime < now) {
                if (EndDecidePrice()) {
                    mag.SetStatus(6);
                    res=true;
                } else {
                    emit decidePrice(startDecidePriceTime);
                }
            } else {
                emit decidePrice(startDecidePriceTime);
            }
        }else if (mag.GetStatus()==6){
            emit reward(msg.sender, 1);
             mag.SetStatus(7);
            res=true;
            StartBuy();
        }else if(mag.GetStatus()==7){
            if(startBuyTime+buyTime<now){
                if(EndBuy()){
                    mag.SetStatus(8);
                    res=true;
                }else{
                    emit buyModel(startBuyTime,p);
                }
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
