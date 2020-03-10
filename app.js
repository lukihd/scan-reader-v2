const {app, BrowserWindow} = require('electron')

/**
 * @function createWindow - Create a chromium window on call / Set window params
 */
function createWindow() {
  window = new BrowserWindow({width: 800, height: 600})
  // window.loadFile('index.html')
}

/**
 * Open window on app click
 */
app.on('ready', createWindow)

/**
 * Close on cross button click
 */
app.on('window-all-closed', () => {
  // On macOS it is common for applications and their menu bar
  // to stay active until the user quits explicitly with Cmd + Q
  if (process.platform !== 'darwin') {
    app.quit()
  }
})