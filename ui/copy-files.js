const fs = require('fs');
const path = require('path');

const sourceDir = path.resolve(__dirname, '../api/app/store/metadata');
const destDir = path.resolve(__dirname, 'src/assets/metadata');

// Ensure the destination directory exists
if (!fs.existsSync(destDir)) {
  fs.mkdirSync(destDir, { recursive: true });
}

// Function to recursively copy files
function copyFiles(source, destination) {
  fs.readdirSync(source).forEach(file => {
    const sourceFile = path.join(source, file);
    const destFile = path.join(destination, file);

    if (fs.lstatSync(sourceFile).isDirectory()) {
      fs.mkdirSync(destFile, { recursive: true });
      copyFiles(sourceFile, destFile);
    } else {
      fs.copyFileSync(sourceFile, destFile);
    }
  });
}

// Start copying files
copyFiles(sourceDir, destDir);

console.log('Files copied successfully.');
