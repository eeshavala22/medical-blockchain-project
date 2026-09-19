const express = require("express");
const router = express.Router();
const { contract } = require("../blockchainConnector");

router.post("/grant", async (req, res) => {
  try {
    const { patientAddress, hospitalAddress } = req.body;
    await contract.methods.grantAccess(hospitalAddress).send({ from: patientAddress, gas: 3000000 });
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.post("/revoke", async (req, res) => {
  try {
    const { patientAddress, hospitalAddress } = req.body;
    await contract.methods.revokeAccess(hospitalAddress).send({ from: patientAddress, gas: 3000000 });
    res.json({ success: true });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;