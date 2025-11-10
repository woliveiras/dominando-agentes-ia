const chromeExecutable = process.env.PUPPETEER_EXECUTABLE_PATH || 
                         process.env.CHROME_BIN ||
                         '/usr/bin/chromium-browser';

module.exports = {
  executablePath: chromeExecutable,
  timeout: 60000,
  args: [
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-gpu',
    '--disable-software-rasterizer',
    '--disable-extensions',
    '--disable-background-networking',
    '--disable-sync',
    '--disable-translate',
    '--disable-default-apps',
    '--mute-audio',
    '--no-first-run',
    '--hide-scrollbars',
    '--disable-infobars',
    '--window-position=0,0',
    '--ignore-certificate-errors',
    '--ignore-certificate-errors-spki-list'
  ]
};
