import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { connectWallet } from "../utils/web3";

function Login() {
  const [address, setAddress] = useState(null);
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleConnect = async () => {
    setError("");
    const wallet = await connectWallet();
    if (wallet) {
      setAddress(wallet.address);
    } else {
      setError("Could not connect wallet. Is MetaMask installed and unlocked?");
    }
  };

  const goToPatient = () => {
    navigate("/patient", { state: { address } });
  };

  const goToHospital = () => {
    navigate("/hospital", { state: { address } });
  };

  return (
    <div style={{ maxWidth: 500, margin: "80px auto", textAlign: "center", fontFamily: "sans-serif" }}>
      <h1>Medical Data Exchange</h1>
      <p>Connect your wallet to continue</p>

      {!address ? (
        <button onClick={handleConnect} style={{ padding: "10px 20px", fontSize: 16 }}>
          Connect MetaMask
        </button>
      ) : (
        <div>
          <p><strong>Connected as:</strong></p>
          <p style={{ fontSize: 12, wordBreak: "break-all" }}>{address}</p>
          <div style={{ marginTop: 20 }}>
            <button onClick={goToPatient} style={{ padding: "10px 20px", marginRight: 10 }}>
              Continue as Patient
            </button>
            <button onClick={goToHospital} style={{ padding: "10px 20px" }}>
              Continue as Hospital
            </button>
          </div>
        </div>
      )}

      {error && <p style={{ color: "red" }}>{error}</p>}
    </div>
  );
}

export default Login;