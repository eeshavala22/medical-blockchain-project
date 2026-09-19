const express = require("express");
const router = express.Router();
const axios = require("axios");
const FormData = require("form-data");
const { contract } = require("../blockchainConnector");

const IPFS_API = "http://127.0.0.1:5001/api/v0";

router.post("/upload", async (req, res) => {
  try {
    const { fileBuffer, patientAddress, hospitalAddress } = req.body;

    const form = new FormData();
    form.append("file", Buffer.from(fileBuffer), "record.dat");

    const ipfsRes = await axios.post(`${IPFS_API}/add`, form, {
      headers: form.getHeaders(),
    });

    const ipfsHash = ipfsRes.data.Hash;

    await contract.methods
      .addRecord(patientAddress, ipfsHash)
      .send({ from: hospitalAddress, gas: 3000000 });

    res.json({ success: true, ipfsHash });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

router.get("/:patientAddress", async (req, res) => {
  try {
    const { patientAddress } = req.params;
    const requester = req.query.requester;
    const records = await contract.methods
      .getRecords(patientAddress)
      .call({ from: requester });

    // Convert BigInt fields (like timestamp) into strings so JSON.stringify works
    const formattedRecords = records.map((r) => ({
      ipfsHash: r.ipfsHash,
      uploadedBy: r.uploadedBy,
      timestamp: r.timestamp.toString(),
    }));

    res.json({ records: formattedRecords });
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

module.exports = router;