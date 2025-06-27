const crypto = require('crypto');
const fs = require('fs');

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', {
  modulusLength: 4096,
  publicKeyEncoding: {
    type: 'spki',
    format: 'pem'
  },
  privateKeyEncoding: {
    type: 'pkcs8',
    format: 'pem'
  }
});

fs.writeFileSync('private.pem', privateKey);
console.log('Private key saved to private.pem');

fs.writeFileSync('public.pem', publicKey);
console.log('Public key saved to public.pem');