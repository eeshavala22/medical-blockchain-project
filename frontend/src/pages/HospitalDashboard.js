import { useState } from "react";
import { useLocation } from "react-router-dom";
import { getRecords, uploadRecord } from "../utils/api";

function HospitalDashboard() {
  const location = useLocation();
  const hospitalAddress = location.state?.address;

  const [patientInput, setPatientInput] = useState("");
  const [records, setRecords] = useState([]);
  const [file, setFile] = useState(null);
  const [status, setStatus] = useState("");

  const handleViewRecords = async () => {
    try {
      const res = await getRecords(patientInput, hospitalAddress);
      setRecords(res.data.records);
      setStatus("");
    } catch (err) {
      setStatus("Error: " + (err.response?.data?.error || err.message));
      setRecords([]);
    }
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file || !patientInput) {
      setStatus("Please select a file and enter a patient address first.");
      return;
    }
    try {
      const arrayBuffer = await file.arrayBuffer();
      const byteArray = Array.from(new Uint8Array(arrayBuffer));

      const res = await uploadRecord(byteArray, patientInput, hospitalAddress);
      setStatus(`Uploaded successfully. IPFS hash: ${res.data.ipfsHash}`);
    } catch (err) {
      setStatus("Upload error: " + (err.response?.data?.error || err.message));
    }
  };

  if (!hospitalAddress) {
    return <p style={{ textAlign: "center", marginTop: 50 }}>Please connect your wallet from the login page first.</p>;
  }

  return (
    <div style={{ maxWidth: 700, margin: "40px auto", fontFamily: "sans-serif" }}>
      <h2>Hospital Dashboard</h2>
      <p style={{ fontSize: 12, wordBreak: "break-all" }}>Logged in as: {hospitalAddress}</p>

      <hr />

      <h3>Patient Address</h3>
      <input
        type="text"
        placeholder="Patient wallet address"
        value={patientInput}
        onChange={(e) => setPatientInput(e.target.value)}
        style={{ width: "100%", padding: 8, marginBottom: 10 }}
      />

      <h3>Upload a Record</h3>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleUpload} style={{ marginLeft: 10 }}>Upload</button>

      <hr />

      <h3>View Patient Records</h3>
      <button onClick={handleViewRecords}>Fetch Records</button>
      {records.length > 0 && (
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

      {status && <p style={{ marginTop: 15 }}>{status}</p>}
    </div>
  );
}

export default HospitalDashboard;