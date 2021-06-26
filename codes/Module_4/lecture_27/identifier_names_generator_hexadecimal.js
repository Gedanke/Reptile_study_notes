const code = `
let hello = '1' + 1
console.log('hello', hello)
`

const options = {
    compact: true,
    identifierNamesGenerator: 'hexadecimal'
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))