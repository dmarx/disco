(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-51bd8868"],{"23c1":function(t,e,n){"use strict";n.d(e,"b",(function(){return c})),n.d(e,"d",(function(){return a})),n.d(e,"a",(function(){return f})),n.d(e,"c",(function(){return l}));var r=n("7a23"),o=n("0613"),u=n("b311"),i=n.n(u),c=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("themeName")})),a=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("themeVersion")})),f=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("demo")})),l=function(){var t=function(t){var e=t;if("undefined"===typeof e&&(e=document.querySelectorAll(".highlight")),e&&e.length>0)for(var n=0;n<e.length;++n){var r=e[n],o=r.querySelector(".highlight-copy");if(o){var u=new i.a(o,{target:function(t){var e=t.closest(".highlight");if(e){var n=e.querySelector(".tab-pane.active");return null==n&&(n=e.querySelector(".highlight-code")),n}return e}});u.on("success",(function(t){var e=t.trigger.innerHTML;t.trigger.innerHTML="copied",t.clearSelection(),setTimeout((function(){t.trigger.innerHTML=e}),2e3)}))}}};return{init:function(e){t(e)}}}},6170:function(t,e,n){"use strict";n.d(e,"e",(function(){return u})),n.d(e,"g",(function(){return i})),n.d(e,"j",(function(){return c})),n.d(e,"h",(function(){return a})),n.d(e,"a",(function(){return f})),n.d(e,"r",(function(){return l})),n.d(e,"q",(function(){return s})),n.d(e,"l",(function(){return d})),n.d(e,"f",(function(){return p})),n.d(e,"m",(function(){return y})),n.d(e,"b",(function(){return g})),n.d(e,"d",(function(){return h})),n.d(e,"n",(function(){return m})),n.d(e,"c",(function(){return b})),n.d(e,"p",(function(){return v})),n.d(e,"o",(function(){return w})),n.d(e,"i",(function(){return O})),n.d(e,"k",(function(){return S}));var r=n("7a23"),o=n("0613"),u=Object(r["computed"])((function(){return o["a"].getters.layoutConfig()})),i=(Object(r["computed"])((function(){return o["a"].getters.layoutConfig("sidebar.display")})),Object(r["computed"])((function(){return"fluid"===o["a"].getters.layoutConfig("footer.width")}))),c=Object(r["computed"])((function(){return"fluid"===o["a"].getters.layoutConfig("header.width")})),a=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("header.left")})),f=Object(r["computed"])((function(){return!0===o["a"].getters.layoutConfig("aside.display")})),l=Object(r["computed"])((function(){return"fluid"===o["a"].getters.layoutConfig("toolbar.width")})),s=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("toolbar.display")})),d=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("loader.display")})),p=Object(r["computed"])((function(){return"fluid"===o["a"].getters.layoutConfig("content.width")})),y=Object(r["computed"])((function(){return"/"+o["a"].getters.layoutConfig("loader.logo")})),g=Object(r["computed"])((function(){return!!o["a"].getters.layoutConfig("aside.display")})),h=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("aside.theme")})),m=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("toolbar.display")})),b=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("aside.menuIcon")})),v=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("main.logo.light")})),w=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("main.logo.dark")})),O=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("header.menuIcon")})),S=Object(r["computed"])((function(){return o["a"].getters.layoutConfig("illustrations.set")}))},b311:function(t,e,n){
/*!
 * clipboard.js v2.0.10
 * https://clipboardjs.com/
 *
 * Licensed MIT © Zeno Rocha
 */
(function(e,n){t.exports=n()})(0,(function(){return function(){var t={686:function(t,e,n){"use strict";n.d(e,{default:function(){return M}});var r=n(279),o=n.n(r),u=n(370),i=n.n(u),c=n(817),a=n.n(c);function f(t){try{return document.execCommand(t)}catch(e){return!1}}var l=function(t){var e=a()(t);return f("cut"),e},s=l;function d(t){var e="rtl"===document.documentElement.getAttribute("dir"),n=document.createElement("textarea");n.style.fontSize="12pt",n.style.border="0",n.style.padding="0",n.style.margin="0",n.style.position="absolute",n.style[e?"right":"left"]="-9999px";var r=window.pageYOffset||document.documentElement.scrollTop;return n.style.top="".concat(r,"px"),n.setAttribute("readonly",""),n.value=t,n}var p=function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{container:document.body},n="";if("string"===typeof t){var r=d(t);e.container.appendChild(r),n=a()(r),f("copy"),r.remove()}else n=a()(t),f("copy");return n},y=p;function g(t){return g="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"===typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},g(t)}var h=function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{},e=t.action,n=void 0===e?"copy":e,r=t.container,o=t.target,u=t.text;if("copy"!==n&&"cut"!==n)throw new Error('Invalid "action" value, use either "copy" or "cut"');if(void 0!==o){if(!o||"object"!==g(o)||1!==o.nodeType)throw new Error('Invalid "target" value, use a valid Element');if("copy"===n&&o.hasAttribute("disabled"))throw new Error('Invalid "target" attribute. Please use "readonly" instead of "disabled" attribute');if("cut"===n&&(o.hasAttribute("readonly")||o.hasAttribute("disabled")))throw new Error('Invalid "target" attribute. You can\'t cut text from elements with "readonly" or "disabled" attributes')}return u?y(u,{container:r}):o?"cut"===n?s(o):y(o,{container:r}):void 0},m=h;function b(t){return b="function"===typeof Symbol&&"symbol"===typeof Symbol.iterator?function(t){return typeof t}:function(t){return t&&"function"===typeof Symbol&&t.constructor===Symbol&&t!==Symbol.prototype?"symbol":typeof t},b(t)}function v(t,e){if(!(t instanceof e))throw new TypeError("Cannot call a class as a function")}function w(t,e){for(var n=0;n<e.length;n++){var r=e[n];r.enumerable=r.enumerable||!1,r.configurable=!0,"value"in r&&(r.writable=!0),Object.defineProperty(t,r.key,r)}}function O(t,e,n){return e&&w(t.prototype,e),n&&w(t,n),t}function S(t,e){if("function"!==typeof e&&null!==e)throw new TypeError("Super expression must either be null or a function");t.prototype=Object.create(e&&e.prototype,{constructor:{value:t,writable:!0,configurable:!0}}),e&&j(t,e)}function j(t,e){return j=Object.setPrototypeOf||function(t,e){return t.__proto__=e,t},j(t,e)}function E(t){var e=x();return function(){var n,r=k(t);if(e){var o=k(this).constructor;n=Reflect.construct(r,arguments,o)}else n=r.apply(this,arguments);return C(this,n)}}function C(t,e){return!e||"object"!==b(e)&&"function"!==typeof e?T(t):e}function T(t){if(void 0===t)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return t}function x(){if("undefined"===typeof Reflect||!Reflect.construct)return!1;if(Reflect.construct.sham)return!1;if("function"===typeof Proxy)return!0;try{return Date.prototype.toString.call(Reflect.construct(Date,[],(function(){}))),!0}catch(t){return!1}}function k(t){return k=Object.setPrototypeOf?Object.getPrototypeOf:function(t){return t.__proto__||Object.getPrototypeOf(t)},k(t)}function A(t,e){var n="data-clipboard-".concat(t);if(e.hasAttribute(n))return e.getAttribute(n)}var L=function(t){S(n,t);var e=E(n);function n(t,r){var o;return v(this,n),o=e.call(this),o.resolveOptions(r),o.listenClick(t),o}return O(n,[{key:"resolveOptions",value:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:{};this.action="function"===typeof t.action?t.action:this.defaultAction,this.target="function"===typeof t.target?t.target:this.defaultTarget,this.text="function"===typeof t.text?t.text:this.defaultText,this.container="object"===b(t.container)?t.container:document.body}},{key:"listenClick",value:function(t){var e=this;this.listener=i()(t,"click",(function(t){return e.onClick(t)}))}},{key:"onClick",value:function(t){var e=t.delegateTarget||t.currentTarget,n=this.action(e)||"copy",r=m({action:n,container:this.container,target:this.target(e),text:this.text(e)});this.emit(r?"success":"error",{action:n,text:r,trigger:e,clearSelection:function(){e&&e.focus(),document.activeElement.blur(),window.getSelection().removeAllRanges()}})}},{key:"defaultAction",value:function(t){return A("action",t)}},{key:"defaultTarget",value:function(t){var e=A("target",t);if(e)return document.querySelector(e)}},{key:"defaultText",value:function(t){return A("text",t)}},{key:"destroy",value:function(){this.listener.destroy()}}],[{key:"copy",value:function(t){var e=arguments.length>1&&void 0!==arguments[1]?arguments[1]:{container:document.body};return y(t,e)}},{key:"cut",value:function(t){return s(t)}},{key:"isSupported",value:function(){var t=arguments.length>0&&void 0!==arguments[0]?arguments[0]:["copy","cut"],e="string"===typeof t?[t]:t,n=!!document.queryCommandSupported;return e.forEach((function(t){n=n&&!!document.queryCommandSupported(t)})),n}}]),n}(o()),M=L},828:function(t){var e=9;if("undefined"!==typeof Element&&!Element.prototype.matches){var n=Element.prototype;n.matches=n.matchesSelector||n.mozMatchesSelector||n.msMatchesSelector||n.oMatchesSelector||n.webkitMatchesSelector}function r(t,n){while(t&&t.nodeType!==e){if("function"===typeof t.matches&&t.matches(n))return t;t=t.parentNode}}t.exports=r},438:function(t,e,n){var r=n(828);function o(t,e,n,r,o){var u=i.apply(this,arguments);return t.addEventListener(n,u,o),{destroy:function(){t.removeEventListener(n,u,o)}}}function u(t,e,n,r,u){return"function"===typeof t.addEventListener?o.apply(null,arguments):"function"===typeof n?o.bind(null,document).apply(null,arguments):("string"===typeof t&&(t=document.querySelectorAll(t)),Array.prototype.map.call(t,(function(t){return o(t,e,n,r,u)})))}function i(t,e,n,o){return function(n){n.delegateTarget=r(n.target,e),n.delegateTarget&&o.call(t,n)}}t.exports=u},879:function(t,e){e.node=function(t){return void 0!==t&&t instanceof HTMLElement&&1===t.nodeType},e.nodeList=function(t){var n=Object.prototype.toString.call(t);return void 0!==t&&("[object NodeList]"===n||"[object HTMLCollection]"===n)&&"length"in t&&(0===t.length||e.node(t[0]))},e.string=function(t){return"string"===typeof t||t instanceof String},e.fn=function(t){var e=Object.prototype.toString.call(t);return"[object Function]"===e}},370:function(t,e,n){var r=n(879),o=n(438);function u(t,e,n){if(!t&&!e&&!n)throw new Error("Missing required arguments");if(!r.string(e))throw new TypeError("Second argument must be a String");if(!r.fn(n))throw new TypeError("Third argument must be a Function");if(r.node(t))return i(t,e,n);if(r.nodeList(t))return c(t,e,n);if(r.string(t))return a(t,e,n);throw new TypeError("First argument must be a String, HTMLElement, HTMLCollection, or NodeList")}function i(t,e,n){return t.addEventListener(e,n),{destroy:function(){t.removeEventListener(e,n)}}}function c(t,e,n){return Array.prototype.forEach.call(t,(function(t){t.addEventListener(e,n)})),{destroy:function(){Array.prototype.forEach.call(t,(function(t){t.removeEventListener(e,n)}))}}}function a(t,e,n){return o(document.body,t,e,n)}t.exports=u},817:function(t){function e(t){var e;if("SELECT"===t.nodeName)t.focus(),e=t.value;else if("INPUT"===t.nodeName||"TEXTAREA"===t.nodeName){var n=t.hasAttribute("readonly");n||t.setAttribute("readonly",""),t.select(),t.setSelectionRange(0,t.value.length),n||t.removeAttribute("readonly"),e=t.value}else{t.hasAttribute("contenteditable")&&t.focus();var r=window.getSelection(),o=document.createRange();o.selectNodeContents(t),r.removeAllRanges(),r.addRange(o),e=r.toString()}return e}t.exports=e},279:function(t){function e(){}e.prototype={on:function(t,e,n){var r=this.e||(this.e={});return(r[t]||(r[t]=[])).push({fn:e,ctx:n}),this},once:function(t,e,n){var r=this;function o(){r.off(t,o),e.apply(n,arguments)}return o._=e,this.on(t,o,n)},emit:function(t){var e=[].slice.call(arguments,1),n=((this.e||(this.e={}))[t]||[]).slice(),r=0,o=n.length;for(r;r<o;r++)n[r].fn.apply(n[r].ctx,e);return this},off:function(t,e){var n=this.e||(this.e={}),r=n[t],o=[];if(r&&e)for(var u=0,i=r.length;u<i;u++)r[u].fn!==e&&r[u].fn._!==e&&o.push(r[u]);return o.length?n[t]=o:delete n[t],this}},t.exports=e,t.exports.TinyEmitter=e}},e={};function n(r){if(e[r])return e[r].exports;var o=e[r]={exports:{}};return t[r](o,o.exports,n),o.exports}return function(){n.n=function(t){var e=t&&t.__esModule?function(){return t["default"]}:function(){return t};return n.d(e,{a:e}),e}}(),function(){n.d=function(t,e){for(var r in e)n.o(e,r)&&!n.o(t,r)&&Object.defineProperty(t,r,{enumerable:!0,get:e[r]})}}(),function(){n.o=function(t,e){return Object.prototype.hasOwnProperty.call(t,e)}}(),n(686)}().default}))}}]);
//# sourceMappingURL=chunk-51bd8868.c37b1612.js.map