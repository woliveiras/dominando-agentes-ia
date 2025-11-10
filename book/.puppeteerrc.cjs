const chromeExecutable = process.env.PUPPETEER_EXECUTABLE_PATH || 
                         process.env.CHROME_BIN ||
                         '/usr/bin/chromium-browser';

const { join } = require('path');

module.exports = {
  // Lê o caminho do Chrome de variáveis de ambiente (CI) ou usa o padrão do sistema
  executablePath: process.env.PUPPETEER_EXECUTABLE_PATH || 
                  process.env.CHROME_PATH ||
                  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  
  // Timeout de 60 segundos
  timeout: 60000,
  
  // Argumentos do Chrome otimizados para CI
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-extensions',
    '--disable-background-networking',
    '--disable-default-apps',
    '--disable-sync',
    '--disable-translate',
    '--hide-scrollbars',
    '--metrics-recording-only',
    '--mute-audio',
    '--no-first-run',
    '--safebrowsing-disable-auto-update',
    '--disable-features=site-per-process',
    '--disable-background-timer-throttling',
    '--disable-backgrounding-occluded-windows',
    '--disable-renderer-backgrounding'
  ]
};
