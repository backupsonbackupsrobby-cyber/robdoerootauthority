const { ethers } = require("ethers");
const { SerialPort } = require("serialport");

const SERIAL_PATH = process.env.SERIAL_PATH || "/dev/ttyUSB0";
const BAUD_RATE = 115200;
const RECONNECT_INTERVAL = 3000;

let port = null;
let isConnecting = false;

function connectSerial() {
    if (isConnecting) return;
    isConnecting = true;

    port = new SerialPort({ path: SERIAL_PATH, baudRate: BAUD_RATE, autoOpen: false });

    port.open((err) => {
        isConnecting = false;
        if (err) {
            setTimeout(connectSerial, RECONNECT_INTERVAL);
            return;
        }
        console.log(`[+] Hardware Link Active: ${SERIAL_PATH}`);
    });

    port.on("error", () => reconnect());
    port.on("close", () => reconnect());
}

function reconnect() {
    if (port && port.isOpen) {
        try { port.close(); } catch (e) {}
    }
    port = null;
    setTimeout(connectSerial, RECONNECT_INTERVAL);
}

connectSerial();

const CHAINS = [
    { name: "Ethereum Mainnet", rpc: "https://ethereum-rpc.publicnode.com", id: 1 },
    { name: "Arbitrum One",     rpc: "https://arbitrum-one-rpc.publicnode.com", id: 42161 },
    { name: "Optimism",         rpc: "https://optimism-rpc.publicnode.com", id: 10 },
    { name: "Polygon Mainnet",  rpc: "https://polygon-bor-rpc.publicnode.com", id: 137 },
    { name: "Base",             rpc: "https://base-rpc.publicnode.com", id: 8453 },
    { name: "BNB Smart Chain",  rpc: "https://bsc-rpc.publicnode.com", id: 56 },
    { name: "Avalanche C-Chain", rpc: "https://avalanche-c-chain-rpc.publicnode.com", id: 43114 }
];

const TARGET_CONTRACT = process.env.CONTRACT_ADDRESS || "0x84CA4aFC3F395ebc0b519680B546Cd604C9c2018";
const TRANSFER_TOPIC = ethers.id("Transfer(address,address,uint256)");

async function attachChain(chain) {
    try {
        const provider = new ethers.JsonRpcProvider(chain.rpc);
        const filter = { address: TARGET_CONTRACT, topics: [TRANSFER_TOPIC] };

        provider.on(filter, (log) => {
            const tokenId = BigInt(log.topics[3]).toString();
            const payload = `SF_TRIGGER:${chain.id}:${tokenId}\n`;

            console.log(`[EVENT] ${chain.name} | Token #${tokenId}`);

            if (port && port.isOpen) {
                port.write(payload, (err) => {});
            }
        });
    } catch (err) {}
}

async function run() {
    console.log("========================================");
    console.log(" HARDWARE RELAY DAEMON ACTIVE          ");
    console.log(" Target:", TARGET_CONTRACT);
    console.log("========================================");
    for (const chain of CHAINS) {
        await attachChain(chain);
    }
}

run();
