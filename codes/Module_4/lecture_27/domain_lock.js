const code = `
console.log('hello world')
`

const options = {
    domainLock: ['github.com']
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))
