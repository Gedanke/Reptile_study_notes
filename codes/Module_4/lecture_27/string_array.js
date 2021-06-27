const code = `
var a = 'hello world'   
`
const options = {
    // stringArray: true,
    stringArray: false,
    rotateStringArray: true,
    stringArrayEncoding: ['base64'], //  ['none'],['base64'],['rc4']
    stringArrayThreshold: 1,
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))