If you run KeyLines from the filesystem, some functionality may not work.
You should serve it from a web server instead.

If you are using Node.js as your web server, you should first install Live Server by running:

> npm install -g live-server

You can then start your web server by running:

> live-server

Live Server will automatically open a new browser tab at http://localhost:8080 to show the KeyLines folder.
Click index.htm to see KeyLines running.

File Name           Description
angular/*           Angular integration code
css/keylines.css    KeyLines style settings
fonts/              Default KeyLines font files
images/             Icon, glyph and flag images for use with KeyLines
index.htm           A 'hello world' sample file
js/keylines.js      The KeyLines JavaScript component
map/*               Map display code
package.json        NPM package file. To install KeyLines as an npm package in your project, run
                      npm install <folder>
                    replacing <folder> with the path to this folder.
                    You can then import or require the 'keylines' package in your project.
react/*             React integration code
ts/keylines.d.ts    TypeScript definition file for KeyLines
vue/*               VueJS integration code
