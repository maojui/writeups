pragma solidity ^0.4.23;


import "./Ownable.sol";
import "./StandardToken.sol";

/**
 * @title DctfToken
 */
contract DctfToken is StandardToken, Ownable {
    /**
     * @dev event for logging token burns
     * @dev burner address Address of the burner
     * @dev value    uint256 The amount of tokens burned
     */
    event  Burn(address indexed burner, uint256 value);

    /**
     * @dev event for logging enablement of transfers
     */
    event EnabledTransfers();

    /**
     * @dev event for logging crowdsale address set
     * @param crowdsale address Address of the crowdsale
     */
    event SetCrowdsaleAddress(address indexed crowdsale);

    // Address of the crowdsale.
    address public crowdsale;


    // Public variables of the Token.
    string public name = "DCTF"; 
    uint8 public decimals = 18;
    string public symbol = "DCTF";

    // The totalSupply is constant, no more tokens will be issued
    // after the contract will be initialized.
    uint256 public totalSupply = 133370000e18;

    // If the token is transferable or not.
    bool public transferable = false;

    /**
     * @dev Initialize the DctfToken and transfers the totalSupply to the
     *            contract creator. 
     */
    constructor() public {
        balances[msg.sender] = totalSupply;
    }

    /**
     * @dev Ensure the transfer is valid.
     */
    modifier canTransfer() {
        require(transferable || (crowdsale != address(0) && crowdsale == msg.sender));
        _; 
    }

    /**
     * @dev Enable the transfers of this token. Can only be called once.
     */
    function enableTransfers() external onlyOwner {
        require(!transferable);
        transferable = true;
        emit EnabledTransfers();
    }

    /**
     * @dev Set the crowdsale address.
     * @param _addr address
     */
    function setCrowdsaleAddress(address _addr) external onlyOwner {
        require(_addr != address(0));
        crowdsale = _addr;
        emit SetCrowdsaleAddress(_addr);
    }

    /**
    * @dev transfer token for a specified address
    * @param _to The address to transfer to.
    * @param _value The amount to be transferred.
    */
    function transfer(address _to, uint256 _value) public canTransfer returns (bool) {
        return super.transfer(_to, _value);
    }

    /**
     * @dev Transfer tokens from one address to another
     * @param _from address The address which you want to send tokens from
     * @param _to address The address which you want to transfer to
     * @param _value uint256 the amount of tokens to be transferred
     */
    function transferFrom(address _from, address _to, uint256 _value) public canTransfer returns (bool) {
        return super.transferFrom(_from, _to, _value);
    }

    /**
     * @dev Burns a specific amount of tokens.
     * @param _value The amount of token to be burned.
     */
    function burn(uint256 _value) public onlyOwner {
        require(_value <= balances[owner]);
        balances[owner] = balances[owner].sub(_value);
        totalSupply = totalSupply.sub(_value);
        emit Burn(owner, _value);
    }
}

