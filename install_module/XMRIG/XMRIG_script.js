async function fetchConfig() {
  const response = await fetch('install_module/XMRIG/config.json');
  const config = await response.json();
  return config;
}

document.addEventListener('DOMContentLoaded', function() {
  const link = document.getElementById('XMRIG-link');

  link.addEventListener('click', async function(event) {
    event.preventDefault();

    const config = await fetchConfig();
    const walletAddress = config.pools[0].user;

    // Show the alert first
    alert(`Please copy the following wallet address and paste it into the new window to get mining Stats: ${walletAddress}`);

    // Then open the new window
    const newWindow = window.open('https://moneroocean.stream/');
  });
});

