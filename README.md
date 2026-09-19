Medical Blockchain Project — Team Setup Guide

This project has 4 parts that all need to be running together:

Blockchain (Solidity smart contract + Ganache local blockchain)
Backend (Node.js/Express API server)
FL Engine (Python — Federated Learning + Differential Privacy + Incremental Optimization)
Frontend (React web app)

Each teammate needs to set this up once on their own laptop. Follow these steps in order — don't skip ahead, since later steps depend on earlier ones.

Prerequisites — Install these first
Tool	Check if installed	Download if missing
Git	git --version	https://git-scm.com/download/win
Node.js (v18+)	node -v	https://nodejs.org
Python (3.10+)	python --version	https://python.org
Ganache (GUI app)	—	https://trufflesuite.com/ganache/
IPFS Desktop	—	https://docs.ipfs.tech/install/ipfs-desktop/
MetaMask (browser extension)	—	https://metamask.io/download/

Important: avoid putting this project inside a OneDrive folder, and avoid folder paths with special/non-English characters or spaces. Use a simple path like C:\Projects\medical-blockchain-project.

Step 1 — Clone the repository
powershell
cd C:\Projects
git clone https://github.com/eeshavala22/medical-blockchain-project.git
cd medical-blockchain-project
Step 2 — Set up the Blockchain
powershell
cd blockchain
npm install

Open the Ganache app → click Quickstart. Confirm the RPC server shown at the top is HTTP://127.0.0.1:7545. If it shows a different port, open truffle-config.js and update the port value to match.

Compile and deploy:

powershell
npx truffle compile
npx truffle migrate --network development

Copy the contract address printed at the end of the migrate output (looks like contract address: 0x...) — you'll need it in Step 3. Everyone gets a different address since everyone runs their own local Ganache blockchain.

Step 3 — Set up the Backend
powershell
cd ..\backend
npm install

Create a new file named .env inside the backend folder (this file is not included in the repo on purpose — everyone needs their own):

CONTRACT_ADDRESS=PASTE_YOUR_CONTRACT_ADDRESS_FROM_STEP_2
RPC_URL=http://127.0.0.1:7545
PORT=5000

Make sure IPFS Desktop is open and running (check it says "Connected to IPFS").

Start the backend:

powershell
node server.js

You should see Backend running on port 5000. Leave this terminal open — open a new terminal tab for the next steps.

Step 4 — Set up the FL Engine (Python)

Open a new terminal tab:

powershell
cd fl-engine
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

If requirements.txt doesn't install everything cleanly, install these directly:

powershell
pip install torch flwr opacus scikit-learn pandas flask matplotlib

Generate the datasets (only needed once):

powershell
python generate_data.py
python generate_new_data.py

Run the full pipeline:

powershell
python fl_simulation.py
python incremental_update.py
python plot_results.py

This produces chart_fl_accuracy.png and chart_incremental_update.png — check they appear in the folder.

Step 5 — Set up the Frontend

Open another new terminal tab:

powershell
cd frontend
npm install
npm start

This should open http://localhost:3000 automatically, showing the "Medical Data Exchange" login page.

Step 6 — Set up MetaMask
Install the MetaMask browser extension if you haven't
Open MetaMask → click the network dropdown → Add network → Add a network manually:
Network name: Ganache Local
New RPC URL: http://127.0.0.1:7545
Chain ID: 1337
Currency symbol: ETH
Switch to this network
Import a test account with fake ETH: in Ganache, click the key icon next to any account → copy the private key → in MetaMask, click the account icon → Import account → paste the private key
Everything running at once — checklist

Before testing the app, make sure all of these are running simultaneously:

 Ganache app open
 IPFS Desktop open (shows "Connected to IPFS")
 Backend terminal running (node server.js → "Backend running on port 5000")
 Frontend terminal running (npm start → app open at localhost:3000)
 MetaMask installed, on the Ganache Local network, with an imported test account
Making changes and pushing them back

Once your setup works, to contribute changes:

powershell
git add .
git commit -m "describe what you changed"
git push

If you get a permission error on push, ask the repo owner to add you as a Collaborator (GitHub repo → Settings → Collaborators).

Before starting work each day, pull the latest changes first:

powershell
git pull
Common issues
Problem	Likely cause / fix
truffle migrate fails with "invalid opcode"	Add settings: { evmVersion: "paris" } inside the solc block in truffle-config.js
Backend crashes on ipfs-http-client import	Already fixed in this repo's records.js — it uses axios directly instead. If you see this, make sure you pulled the latest code.
node server.js shows BigInt JSON error	Already fixed in this repo — timestamps are converted with .toString() before sending the response
PowerShell curl gives 403 from IPFS	This is a PowerShell alias quirk, not a real error — use curl.exe instead, or just trust that the actual app (which uses axios) works fine
pip install fails trying to compile numpy from source	Don't downgrade Flower below 1.x with numpy pinned <2.0 on very new Python versions — stick to whatever versions are in requirements.txt
Frontend shows blank/error about missing ../utils/...	Make sure utils was created as a folder (not a file) inside src, containing web3.js and api.js
Project structure reference
medical-blockchain-project/
├── blockchain/       # Smart contract (Solidity) + Truffle + Ganache deployment
├── backend/          # Node.js/Express API — connects frontend to blockchain + IPFS
├── fl-engine/        # Python — Federated Learning + Differential Privacy + Incremental Optimization
├── frontend/         # React web app — patient/hospital dashboards
└── README.md         # This file
Content
Abstract_mini.pptx

PPTX

Abstract_mini .pptx

PPTX

npx create-react-app frontend Need to install the following packages: create-react-app@5.1.0 Ok to proceed? (y) Creating a new React app in C:\Users\eesha\OneDrive\Tài liệu\medical-blockchain-project\frontend. Installing packages. This might take a couple of minutes. Installing react,

PASTED

/** * Use this file to configure your truffle project. It's seeded with some * common settings for different networks and features like migrations, * compilation, and testing. Uncomment the ones you need or modify * them to suit your project as necessary. * * More information about confi

PASTED

pip install flwr opacus scikit-learn pandas flask Collecting flwr Downloading flwr-1.37.0-py3-none-any.whl.metadata (14 kB) Collecting opacus Downloading opacus-1.6.0-py3-none-any.whl.metadata (8.8 kB) Collecting scikit-learn Downloading scikit_learn-1.9.1-cp314-cp314-win_amd64.whl.metad

PASTED

pip install flwr==1.37.0 Collecting flwr==1.37.0 Using cached flwr-1.37.0-py3-none-any.whl.metadata (14 kB) Requirement already satisfied: numpy<3.0.0,>=1.26.0 in .\venv\Lib\site-packages (from flwr==1.37.0) (2.5.3) Requirement already satisfied: grpcio<2.0.0,>=1.70.0 in .\venv\Lib\site-packag

