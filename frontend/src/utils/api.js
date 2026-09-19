import axios from "axios";

const API_BASE = "http://localhost:5000/api";

export const getRecords = (patientAddress, requesterAddress) =>
  axios.get(`${API_BASE}/records/${patientAddress}?requester=${requesterAddress}`);

export const uploadRecord = (fileBuffer, patientAddress, hospitalAddress) =>
  axios.post(`${API_BASE}/records/upload`, {
    fileBuffer,
    patientAddress,
    hospitalAddress,
  });

export const grantAccess = (patientAddress, hospitalAddress) =>
  axios.post(`${API_BASE}/access/grant`, { patientAddress, hospitalAddress });

export const revokeAccess = (patientAddress, hospitalAddress) =>
  axios.post(`${API_BASE}/access/revoke`, { patientAddress, hospitalAddress });