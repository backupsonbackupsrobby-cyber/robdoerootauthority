module.exports = {
  apps: [{
    name: "root-multichain-monitor",
    script: "multichain.cjs",
    env: {
      CONTRACT_ADDRESS: "0x84CA4aFC3F395ebc0b519680B546Cd604C9c2018"
    },
    autorestart: true,
    exp_backoff_restart_delay: 2000
  }]
};
