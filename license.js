const crypto = require('crypto');
const fs = require('fs');

const licenseData = {
  startTime: new Date().toISOString(),
  expiredTime: new Date(Date.now() + 1000 * 60 * 60 * 24 * 365).toISOString(), // 一年后过期
  company: "IIAIM",
  description: "IIAIM",
  maxUsers: undefined,
  maxApps: undefined,
  maxDatasets: undefined,
  functions: {
    sso: true,
    pay: true,
    customTemplates: true,
    datasetEnhance: true,
    batchEval: true
  }
};

function generateLicense(licenseData) {
  const licenseContent = Buffer.from(JSON.stringify(licenseData)).toString('base64');
  const privateKey = fs.readFileSync('keys/private.pem');
  const sign = crypto.createSign('RSA-SHA256');
  sign.update(licenseContent);
  const signature = sign.sign(privateKey, 'base64');
  return signature + licenseContent;
}

function verifyLicense(license) {
  const signature = license.substring(0, 684);
  const content = license.substring(684);
  
  const verify = crypto.createVerify('RSA-SHA256');
  verify.update(content);
  
  const publicKey = fs.readFileSync('keys/public.pem');
  const isValid = verify.verify(publicKey, signature, 'base64');
  
  if (isValid) {
    const licenseData = JSON.parse(Buffer.from(content, 'base64').toString());
    console.log('License Verify OK:', licenseData);
    return licenseData;
  } else {
    console.log('License Verify Failed.');
    return null;
  }
}

try {
  const license = generateLicense(licenseData);
  console.log('Generated License:', license);
  console.log('\nVerifying license...');
  verifyLicense(license);
} catch (error) {
  console.error('Error:', error.message);
}

module.exports = {
  generateLicense,
  verifyLicense
}; 