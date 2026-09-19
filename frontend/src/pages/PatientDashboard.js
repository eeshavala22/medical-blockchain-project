import { useState, useEffect } from "react";
import { useLocation } from "react-router-dom";
import { getRecords, grantAccess, revokeAccess } from "../utils/api";

function PatientDashboard() {
  const location = useLocation();
  const patientAddress = location.state?.address;

  const [records, setRecords] = useState([]);
  const [hospitalInput, setHospitalInput] = useState("");
  const [status, setStatus] = useState("");

  const loadRecords = async () => {
    if (!patientAddress) return;
    try {
      const res = await getRecords(patientAddress, patientAddress);
      setRecords(res.data.records);
    } catch (err) {
      setStatus("Error loading records: " + err.message);
    }
  };

  useEffect(() => {
    loadRecords();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [patientAddress]);

  const handleGrant = async () => {
    try {
      await grantAccess(patientAddress, hospitalInput);
      setStatus(`Access granted to ${hospitalInput}`);
    } catch (err) {
      setStatus("Error: " + err.message);
    }
  };

  const handleRevoke = async () => {
    try {
      await revokeAccess(patientAddress, hospitalInput);
      setStatus(`Access revoked for ${hospitalInput}`);
    } catch (err) {
      setStatus("Error: " + err.message);
    }
  };

  if (!patientAddress) {
    return <p style={{ textAlign: "center", marginTop: 50 }}>Please connect your wallet from the login page first.</p>;
  }

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Patient Dashboard</h2>
      <p style={{ fontSize: 12, wordBreak: "break-all" }}>Logged in as: {patientAddress}</p>

      <hr />

      <h3>My Records</h3>
      <button onClick={loadRecords}>Refresh</button>
      {records.length === 0 ? (
        <p>No records found.</p>
      ) : (
        <ul>
          {records.map((r, i) => (
            <li key={i}>
              <strong>IPFS Hash:</strong> {r.ipfsHash} <br />
              <strong>Uploaded by:</strong> {r.uploadedBy} <br />
              <strong>Timestamp:</strong> {new Date(Number(r.timestamp) * 1000).toLocaleString()}
            </li>
          ))}
        </ul>
      )}

      <hr />

      <h3>Manage Hospital Access</h3>
      <input
        type="text"
        placeholder="Hospital wallet address"
        value={hospitalInput}
        onChange={(e) => setHospitalInput(e.target.value)}
        style={{ width: "100%", padding: 8, marginBottom: 10 }}
      />
      <button onClick={handleGrant} style={{ marginRight: 10 }}>Grant Access</button>
      <button onClick={handleRevoke}>Revoke Access</button>

      {status && <p style={{ marginTop: 15 }}>{status}</p>}
    </div>
  );
}

export default PatientDashboard;