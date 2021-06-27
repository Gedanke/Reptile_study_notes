const code = `
(function(){
    if (true) {
        var foo = function () {
            console.log('abc');
            console.log('cde');
            console.log('efg');
            console.log('hij');
        };

        var bar = function () {
            console.log('klm');
            console.log('nop');
            console.log('qrs');
        };

        var baz = function () {
            console.log('tuv');
            console.log('wxy');
            console.log('z');
        };

        foo();
        bar();
        baz();
    }
})();
`
const options = {
    compact: false,
    // deadCodeInjection: true
    deadCodeInjection: false
}

const obfuscator = require('javascript-obfuscator')

function obfuscate(code, options) {
    return obfuscator.obfuscate(code, options).getObfuscatedCode()
}

console.log(obfuscate(code, options))