pragma solidity ^0.4.23;

import "./DctfToken.sol";
import "./SafeMath.sol";
import "./Ownable.sol";


/**
 * @title DCTF18_Crowdsale
 */
contract DCTF18_Crowdsale is Ownable {
  using SafeMath for uint256;

  /**
   * @dev event for pre-sale investments register logging
   * @param investor who invested in the pre-sale
   * @param amount of tokens purchased
   */
  event RegisteredPreSaleInvestment(address indexed investor, uint256 indexed amount);

  /**
   * @dev event for change wallet address logging
   * @param newWallet address that got set
   * @param oldWallet address that was changed from
   */
  event ChangedWalletAddress(address indexed newWallet, address indexed oldWallet);
  
  /**
   * @dev event for token purchase logging
   * @param investor who purchased tokens
   * @param value weis paid for purchase
   * @param amount of tokens purchased
   */
  event TokenPurchase(address indexed investor, uint256 value, uint256 amount);

  // definition of an Investor
  struct Investor {
    uint256 weiBalance;    // Amount of invested wei (0 for PreInvestors)
    uint256 tokenBalance;  // Amount of owned tokens
    bool whitelisted;      // Flag for marking an investor as whitelisted
    bool purchasing;       // Lock flag
    uint256 cap;           // Investor cap.
    uint256 capTimestamp;  // timestamp of last cap sync
  }

  // start and end timestamps where investments are allowed (both inclusive)
  uint256 public startTime;
  uint256 public endTime;

  // address that can whitelist new investors
  address public registrar;

  // wei to token exchange rate
  uint256 public exchangeRate;

  // address where funds are collected
  address public wallet;

  // token contract
  DctfToken public token;

  // crowdsale sale cap
  uint256 public constant cap = 13337 ether;

  // minimum investment
  uint256 public constant minInvestment = 0 finney;

  // crowdsale investor cap
  uint256 public investorCapBaseline;
  uint256 public capTimestamp;

  // amount of raised money in wei
  uint256 public weiRaised;

  // gas price limit in wei
  uint256 public gasPriceLimit;

  // storage for the investors repository
  uint256 public numInvestors;
  mapping (address => Investor) public investors;

  /**
   * @dev Create a new instance of the contract
   * @param _startTime     uint256
   * @param _registrar     address
   * @param _exchangeRate  uint256
   * @param _wallet        address
   * @param _token         address
   * @param _gasPriceLimit uint256
   */
  constructor(
    uint256 _startTime,
    address _registrar,
    uint256 _exchangeRate,
    address _wallet,
    address _token,
    uint256 _gasPriceLimit
  )
    public
  {
    // validate parameters
    require(_startTime > now);
    require(_registrar != address(0));
    require(_exchangeRate > 0);
    require(_wallet != address(0));
    require(_token != address(0));
    require(_gasPriceLimit > 0);

    // update storage
    startTime = _startTime;
    registrar = _registrar;
    exchangeRate = _exchangeRate;
    wallet = _wallet;
    token = DctfToken(_token);
    gasPriceLimit = _gasPriceLimit;

    // calculate and set the endTime
    endTime = startTime.add(5 days);
  }

  /**
   * @dev Ensure the crowdsale is not started
   */
  modifier notStarted() { 
    require(now < startTime);
    _;
  }
  /**
   * @dev Ensure the crowdsale is not started
   */
  modifier notEnded() { 
    require(now < endTime);
    _;
  }

  /**
   * @dev Fallback function can be used to buy tokens
   */
  function () external payable {
    buyTokens();
  }

  /**
   * @dev Change the wallet address
   * @param _wallet address
   */
  function changeWalletAddress(address _wallet) external notStarted onlyOwner {
    // validate call against the rules
    require(_wallet != address(0));
    require(_wallet != wallet);

    // update storage
    address _oldWallet = wallet;
    wallet = _wallet;

    // trigger event
    emit ChangedWalletAddress(_wallet, _oldWallet);
  }

  /**
   * @dev Register an investment from the pre-sale into the crowdsale and transfer
   *      the tokens to the investor
   * @param _investor address
   * @param _amount   uint256
   */
  function registerPreSaleInvestment(address _investor, uint256 _amount) external onlyOwner {
    // validate call against the rules
    require(_investor != address(0));

    // transfer tokens
    require(transfer(_investor, _amount));

    // update storage
    investors[_investor].tokenBalance = investors[_investor].tokenBalance.add(_amount);

    // trigger event
    emit RegisteredPreSaleInvestment(_investor, _amount);
  }

  /**
   * @dev Whitelist multiple investors at once
   * @param addrs address[]
   */
  function whitelistInvestors(address[] addrs) external {
    require(addrs.length > 0 && addrs.length <= 30);
    for (uint i = 0; i < addrs.length; i++) {
      whitelistInvestor(addrs[i]);
    }
  }

  /**
   * @dev Whitelist a new investor
   * @param addr address
   */
  function whitelistInvestor(address addr) public notEnded {
    require(msg.sender == registrar || msg.sender == owner);
    if (!investors[addr].whitelisted && addr != address(0)) {
      investors[addr].whitelisted = true;
      numInvestors++;
    }
  }

  /**
   * @dev Low level token purchase function
   */
  function buyTokens() public payable {
    address investor = msg.sender;
    
    // update investor cap
    updateInvestorCap(investor);

    // validate purchase    
    validPurchase();

    // lock investor account
    investors[investor].purchasing = true;

    // get the msg wei amount
    uint256 weiAmount = msg.value.sub(refundExcess());

    // value after refunds should be greater or equal to minimum investment
    require(weiAmount > 0);

    // calculate token amount to be sold
    uint256 tokens = weiAmount.mul(1 ether).div(exchangeRate);

    // update storage
    weiRaised = weiRaised.add(weiAmount);
    investors[investor].weiBalance = investors[investor].weiBalance.add(weiAmount);
    investors[investor].tokenBalance = investors[investor].tokenBalance.add(tokens);

    // transfer tokens
    require(transfer(investor, tokens));
    
    // trigger event
    emit TokenPurchase(msg.sender, weiAmount, tokens);
    
    // forward funds
    wallet.transfer(weiAmount);

    // unlock investor account
    investors[investor].purchasing = false; 
  }

  /**
   * @dev Update the investor cap
   * @param investor address
   */
  function updateInvestorCap(address investor) internal {
    require(now >= startTime);

    // Update investor baseline cap
    if (now < startTime.add(1 days) && capTimestamp == 0) {
      capTimestamp = now;
      investorCapBaseline = cap.div(numInvestors);
    } else if (now < startTime.add(2 days) && capTimestamp < startTime.add(1 days)) {
      capTimestamp = now;
      investorCapBaseline = investorCapBaseline.mul(2);
    }

    // InvestorCap.
    if (investors[investor].capTimestamp != capTimestamp) {
      investors[investor].capTimestamp = capTimestamp;
      investors[investor].cap = investorCapBaseline.add(investors[investor].weiBalance);
    }
  }

  /**
   * @dev Wrapper over token's transferFrom function. Ensures the call is valid.
   * @param  to    address
   * @param  value uint256
   * @return bool
   */
  function transfer(address to, uint256 value) internal returns (bool) {
    if (!(
      token.allowance(owner, address(this)) >= value 
      && token.balanceOf(owner) >= value 
      && token.crowdsale() == address(this)
    )) {
      return false;
    }  
    return token.transferFrom(owner, to, value);
  }
  
  /**
   * @dev Refund the excess weiAmount back to the investor so the caps aren't reached
   * @return uint256 the weiAmount after refund
   */
  function refundExcess() internal returns (uint256 excess) {
    uint256 weiAmount = msg.value;
    address investor = msg.sender;

    // calculate excess for investorCap
    if (limited() && !withinInvestorCap(investor, weiAmount)) {
      excess = investors[investor].weiBalance.add(weiAmount).sub(investors[investor].cap);
      weiAmount = msg.value.sub(excess);
    }

    // calculate excess for crowdsale cap
    if (!withinCap(weiAmount)) {
      excess = excess.add(weiRaised.add(weiAmount).sub(cap));
      weiAmount = msg.value.sub(excess);
    }
    
    // refund and update weiAmount
    if (excess > 0) {
      investor.transfer(excess);
    }
  }

  /**
   * @dev Validate the purchase. Reverts if purchase is invalid
   */
  function validPurchase() internal view {
    require (msg.sender != address(0));           // valid investor address
    require (tx.gasprice <= gasPriceLimit);       // tx gas price doesn't exceed limit
    require (!investors[msg.sender].purchasing);  // investor not already purchasing
    require (now >= startTime && now <= endTime); // within crowdsale period
    require (capTimestamp != 0);                  // investor cap initialized
    require (msg.value >= minInvestment);         // value should exceed or be equal to minimum investment
    require (whitelisted(msg.sender));            // check if investor is whitelisted
    require (withinCap(0));                       // check if purchase is within cap
    require (withinInvestorCap(msg.sender, 0));   // check if purchase is within investor cap
  }

  /**
   * @dev Check if by adding the provided _weiAmomunt the cap is not exceeded
   * @param weiAmount uint256
   * @return bool
   */
  function withinCap(uint256 weiAmount) internal view returns (bool) {
    return weiRaised.add(weiAmount) <= cap;
  }

  /**
   * @dev Check if by adding the provided weiAmount to investor's account the investor
   *      cap is not excedeed
   * @param investor  address
   * @param weiAmount uint256
   * @return bool
   */

  function withinInvestorCap(address investor, uint256 weiAmount) internal view returns (bool) {
    return limited() ? investors[investor].weiBalance.add(weiAmount) <= investors[investor].cap : true;
  }
  /**
   * @dev Check if the given address is whitelisted for token purchases
   * @param investor address
   * @return bool
   */
  function whitelisted(address investor) internal view returns (bool) {
    return limited() ? investors[investor].whitelisted : true;
  }

  /**
   * @dev Check if the crowdsale is limited
   * @return bool
   */
  function limited() internal view returns (bool) {
    return now < startTime.add(2 days);
  }
}

