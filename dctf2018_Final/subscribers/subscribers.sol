pragma solidity ^0.4.19; 

contract DCTF18_Subscribers{
    
    event EnabledRegistration(address _from);
    event DisabledRegistration(address _from);
    event newSubscription(address _subscriber, uint _subscription);
    event subscriptionDeleted(uint _id, address _subscriber, uint _subscription);

    struct Subscriber{
        uint subscription; //0 - default Subscriber, 1 - VIP Subscriber
        address subscriber; // address of the new subscriber
    }

    uint private registration_open = 0;
    address private owner; //address of the owner
   
    Subscriber[] private subscribers; //list of subscribers

    constructor() public {
        owner = msg.sender; //owner of the smart contract
        registration_open = 1; //registrations are open by default
        emit EnabledRegistration(owner);
    }

    function subscribe(address subscriber, uint subscription) public {
        require(registration_open > 0);
        //only owner can subscribe VIPs
        if(subscription == 1) {
            require(msg.sender == owner);
        }

        //save new subscribers
        Subscriber s; 
        s.subscription = subscription;
        s.subscriber = subscriber;

        subscribers.push(s);

        emit newSubscription(subscriber, subscription);
    }  

    function enableRegistration() public {
        require(msg.sender == owner && registration_open != 1);
        registration_open = 1;
        emit EnabledRegistration(owner);
    }

    function disableRegistration() public {
        require(msg.sender == owner && registration_open != 0);
        registration_open = 0;
        emit DisabledRegistration(owner);
    }

    function deleteRegistration(uint id) public {
        require(msg.sender == owner);
        
        address subscriber = subscribers[id].subscriber;
        uint subscription = subscribers[id].subscription;

        delete subscribers[id];
        emit subscriptionDeleted(id, subscriber, subscription);
    }

    function getSubscriber(uint id) public constant returns (address subscriber,uint subscription){
        subscriber = subscribers[id].subscriber;
        subscription = subscribers[id].subscription;
    }

    function isVIP(uint id) public constant returns (address subscriber, bool vip) {
        subscriber = subscribers[id].subscriber;
        vip = (subscribers[id].subscription == 1);
    }
}
