// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract AccessControl {
    struct Record {
        string ipfsHash;
        address uploadedBy;
        uint256 timestamp;
    }

    mapping(address => Record[]) private patientRecords;
    mapping(address => mapping(address => bool)) private accessGranted;

    event RecordAdded(address indexed patient, string ipfsHash, address hospital);
    event AccessChanged(address indexed patient, address hospital, bool granted);

    function addRecord(address patient, string memory ipfsHash) public {
        patientRecords[patient].push(Record(ipfsHash, msg.sender, block.timestamp));
        emit RecordAdded(patient, ipfsHash, msg.sender);
    }

    function grantAccess(address hospital) public {
        accessGranted[msg.sender][hospital] = true;
        emit AccessChanged(msg.sender, hospital, true);
    }

    function revokeAccess(address hospital) public {
        accessGranted[msg.sender][hospital] = false;
        emit AccessChanged(msg.sender, hospital, false);
    }

    function hasAccess(address patient, address hospital) public view returns (bool) {
        return accessGranted[patient][hospital];
    }

    function getRecords(address patient) public view returns (Record[] memory) {
        require(
            msg.sender == patient || accessGranted[patient][msg.sender],
            "Access denied"
        );
        return patientRecords[patient];
    }
}