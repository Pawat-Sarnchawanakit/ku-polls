/*! js-yaml 4.1.0 https://github.com/nodeca/js-yaml @license MIT */function ne(e){return typeof e>"u"||e===null}function he(e){return typeof e=="object"&&e!==null}function de(e){return Array.isArray(e)?e:ne(e)?[]:[e]}function me(e,n){var i,o,r,u;if(n)for(u=Object.keys(n),i=0,o=u.length;i<o;i+=1)r=u[i],e[r]=n[r];return e}function ge(e,n){var i="",o;for(o=0;o<n;o+=1)i+=e;return i}function xe(e){return e===0&&Number.NEGATIVE_INFINITY===1/e}var be=ne,Ae=he,ve=de,ye=ge,ke=xe,we=me,y={isNothing:be,isObject:Ae,toArray:ve,repeat:ye,isNegativeZero:ke,extend:we};function ie(e,n){var i="",o=e.reason||"(unknown reason)";return e.mark?(e.mark.name&&(i+='in "'+e.mark.name+'" '),i+="("+(e.mark.line+1)+":"+(e.mark.column+1)+")",!n&&e.mark.snippet&&(i+=`

`+e.mark.snippet),o+" "+i):o}function L(e,n){Error.call(this),this.name="YAMLException",this.reason=e,this.mark=n,this.message=ie(this,!1),Error.captureStackTrace?Error.captureStackTrace(this,this.constructor):this.stack=new Error().stack||""}L.prototype=Object.create(Error.prototype);L.prototype.constructor=L;L.prototype.toString=function(n){return this.name+": "+ie(this,n)};var _=L;function Y(e,n,i,o,r){var u="",l="",c=Math.floor(r/2)-1;return o-n>c&&(u=" ... ",n=o-c+u.length),i-o>c&&(l=" ...",i=o+c-l.length),{str:u+e.slice(n,i).replace(/\t/g,"→")+l,pos:o-n+u.length}}function P(e,n){return y.repeat(" ",n-e.length)+e}function Ce(e,n){if(n=Object.create(n||null),!e.buffer)return null;n.maxLength||(n.maxLength=79),typeof n.indent!="number"&&(n.indent=1),typeof n.linesBefore!="number"&&(n.linesBefore=3),typeof n.linesAfter!="number"&&(n.linesAfter=2);for(var i=/\r?\n|\r|\0/g,o=[0],r=[],u,l=-1;u=i.exec(e.buffer);)r.push(u.index),o.push(u.index+u[0].length),e.position<=u.index&&l<0&&(l=o.length-2);l<0&&(l=o.length-1);var c="",t,s,h=Math.min(e.line+n.linesAfter,r.length).toString().length,f=n.maxLength-(n.indent+h+3);for(t=1;t<=n.linesBefore&&!(l-t<0);t++)s=Y(e.buffer,o[l-t],r[l-t],e.position-(o[l]-o[l-t]),f),c=y.repeat(" ",n.indent)+P((e.line-t+1).toString(),h)+" | "+s.str+`
`+c;for(s=Y(e.buffer,o[l],r[l],e.position,f),c+=y.repeat(" ",n.indent)+P((e.line+1).toString(),h)+" | "+s.str+`
`,c+=y.repeat("-",n.indent+h+3+s.pos)+`^
`,t=1;t<=n.linesAfter&&!(l+t>=r.length);t++)s=Y(e.buffer,o[l+t],r[l+t],e.position-(o[l]-o[l+t]),f),c+=y.repeat(" ",n.indent)+P((e.line+t+1).toString(),h)+" | "+s.str+`
`;return c.replace(/\n$/,"")}var _e=Ce,Te=["kind","multi","resolve","construct","instanceOf","predicate","represent","representName","defaultStyle","styleAliases"],Se=["scalar","sequence","mapping"];function Fe(e){var n={};return e!==null&&Object.keys(e).forEach(function(i){e[i].forEach(function(o){n[String(o)]=i})}),n}function Ee(e,n){if(n=n||{},Object.keys(n).forEach(function(i){if(Te.indexOf(i)===-1)throw new _('Unknown option "'+i+'" is met in definition of "'+e+'" YAML type.')}),this.options=n,this.tag=e,this.kind=n.kind||null,this.resolve=n.resolve||function(){return!0},this.construct=n.construct||function(i){return i},this.instanceOf=n.instanceOf||null,this.predicate=n.predicate||null,this.represent=n.represent||null,this.representName=n.representName||null,this.defaultStyle=n.defaultStyle||null,this.multi=n.multi||!1,this.styleAliases=Fe(n.styleAliases||null),Se.indexOf(this.kind)===-1)throw new _('Unknown kind "'+this.kind+'" is specified for "'+e+'" YAML type.')}var v=Ee;function K(e,n){var i=[];return e[n].forEach(function(o){var r=i.length;i.forEach(function(u,l){u.tag===o.tag&&u.kind===o.kind&&u.multi===o.multi&&(r=l)}),i[r]=o}),i}function Oe(){var e={scalar:{},sequence:{},mapping:{},fallback:{},multi:{scalar:[],sequence:[],mapping:[],fallback:[]}},n,i;function o(r){r.multi?(e.multi[r.kind].push(r),e.multi.fallback.push(r)):e[r.kind][r.tag]=e.fallback[r.tag]=r}for(n=0,i=arguments.length;n<i;n+=1)arguments[n].forEach(o);return e}function U(e){return this.extend(e)}U.prototype.extend=function(n){var i=[],o=[];if(n instanceof v)o.push(n);else if(Array.isArray(n))o=o.concat(n);else if(n&&(Array.isArray(n.implicit)||Array.isArray(n.explicit)))n.implicit&&(i=i.concat(n.implicit)),n.explicit&&(o=o.concat(n.explicit));else throw new _("Schema.extend argument should be a Type, [ Type ], or a schema definition ({ implicit: [...], explicit: [...] })");i.forEach(function(u){if(!(u instanceof v))throw new _("Specified list of YAML types (or a single Type object) contains a non-Type object.");if(u.loadKind&&u.loadKind!=="scalar")throw new _("There is a non-scalar type in the implicit list of a schema. Implicit resolving of such types is not supported.");if(u.multi)throw new _("There is a multi type in the implicit list of a schema. Multi tags can only be listed as explicit.")}),o.forEach(function(u){if(!(u instanceof v))throw new _("Specified list of YAML types (or a single Type object) contains a non-Type object.")});var r=Object.create(U.prototype);return r.implicit=(this.implicit||[]).concat(i),r.explicit=(this.explicit||[]).concat(o),r.compiledImplicit=K(r,"implicit"),r.compiledExplicit=K(r,"explicit"),r.compiledTypeMap=Oe(r.compiledImplicit,r.compiledExplicit),r};var Ie=U,Ne=new v("tag:yaml.org,2002:str",{kind:"scalar",construct:function(e){return e!==null?e:""}}),Le=new v("tag:yaml.org,2002:seq",{kind:"sequence",construct:function(e){return e!==null?e:[]}}),je=new v("tag:yaml.org,2002:map",{kind:"mapping",construct:function(e){return e!==null?e:{}}}),Me=new Ie({explicit:[Ne,Le,je]});function De(e){if(e===null)return!0;var n=e.length;return n===1&&e==="~"||n===4&&(e==="null"||e==="Null"||e==="NULL")}function qe(){return null}function Be(e){return e===null}var Ye=new v("tag:yaml.org,2002:null",{kind:"scalar",resolve:De,construct:qe,predicate:Be,represent:{canonical:function(){return"~"},lowercase:function(){return"null"},uppercase:function(){return"NULL"},camelcase:function(){return"Null"},empty:function(){return""}},defaultStyle:"lowercase"});function Pe(e){if(e===null)return!1;var n=e.length;return n===4&&(e==="true"||e==="True"||e==="TRUE")||n===5&&(e==="false"||e==="False"||e==="FALSE")}function Re(e){return e==="true"||e==="True"||e==="TRUE"}function Ue(e){return Object.prototype.toString.call(e)==="[object Boolean]"}var He=new v("tag:yaml.org,2002:bool",{kind:"scalar",resolve:Pe,construct:Re,predicate:Ue,represent:{lowercase:function(e){return e?"true":"false"},uppercase:function(e){return e?"TRUE":"FALSE"},camelcase:function(e){return e?"True":"False"}},defaultStyle:"lowercase"});function $e(e){return 48<=e&&e<=57||65<=e&&e<=70||97<=e&&e<=102}function Ge(e){return 48<=e&&e<=55}function Ke(e){return 48<=e&&e<=57}function We(e){if(e===null)return!1;var n=e.length,i=0,o=!1,r;if(!n)return!1;if(r=e[i],(r==="-"||r==="+")&&(r=e[++i]),r==="0"){if(i+1===n)return!0;if(r=e[++i],r==="b"){for(i++;i<n;i++)if(r=e[i],r!=="_"){if(r!=="0"&&r!=="1")return!1;o=!0}return o&&r!=="_"}if(r==="x"){for(i++;i<n;i++)if(r=e[i],r!=="_"){if(!$e(e.charCodeAt(i)))return!1;o=!0}return o&&r!=="_"}if(r==="o"){for(i++;i<n;i++)if(r=e[i],r!=="_"){if(!Ge(e.charCodeAt(i)))return!1;o=!0}return o&&r!=="_"}}if(r==="_")return!1;for(;i<n;i++)if(r=e[i],r!=="_"){if(!Ke(e.charCodeAt(i)))return!1;o=!0}return!(!o||r==="_")}function Qe(e){var n=e,i=1,o;if(n.indexOf("_")!==-1&&(n=n.replace(/_/g,"")),o=n[0],(o==="-"||o==="+")&&(o==="-"&&(i=-1),n=n.slice(1),o=n[0]),n==="0")return 0;if(o==="0"){if(n[1]==="b")return i*parseInt(n.slice(2),2);if(n[1]==="x")return i*parseInt(n.slice(2),16);if(n[1]==="o")return i*parseInt(n.slice(2),8)}return i*parseInt(n,10)}function ze(e){return Object.prototype.toString.call(e)==="[object Number]"&&e%1===0&&!y.isNegativeZero(e)}var Ze=new v("tag:yaml.org,2002:int",{kind:"scalar",resolve:We,construct:Qe,predicate:ze,represent:{binary:function(e){return e>=0?"0b"+e.toString(2):"-0b"+e.toString(2).slice(1)},octal:function(e){return e>=0?"0o"+e.toString(8):"-0o"+e.toString(8).slice(1)},decimal:function(e){return e.toString(10)},hexadecimal:function(e){return e>=0?"0x"+e.toString(16).toUpperCase():"-0x"+e.toString(16).toUpperCase().slice(1)}},defaultStyle:"decimal",styleAliases:{binary:[2,"bin"],octal:[8,"oct"],decimal:[10,"dec"],hexadecimal:[16,"hex"]}}),Ve=new RegExp("^(?:[-+]?(?:[0-9][0-9_]*)(?:\\.[0-9_]*)?(?:[eE][-+]?[0-9]+)?|\\.[0-9_]+(?:[eE][-+]?[0-9]+)?|[-+]?\\.(?:inf|Inf|INF)|\\.(?:nan|NaN|NAN))$");function Xe(e){return!(e===null||!Ve.test(e)||e[e.length-1]==="_")}function Je(e){var n,i;return n=e.replace(/_/g,"").toLowerCase(),i=n[0]==="-"?-1:1,"+-".indexOf(n[0])>=0&&(n=n.slice(1)),n===".inf"?i===1?Number.POSITIVE_INFINITY:Number.NEGATIVE_INFINITY:n===".nan"?NaN:i*parseFloat(n,10)}var en=/^[-+]?[0-9]+e/;function nn(e,n){var i;if(isNaN(e))switch(n){case"lowercase":return".nan";case"uppercase":return".NAN";case"camelcase":return".NaN"}else if(Number.POSITIVE_INFINITY===e)switch(n){case"lowercase":return".inf";case"uppercase":return".INF";case"camelcase":return".Inf"}else if(Number.NEGATIVE_INFINITY===e)switch(n){case"lowercase":return"-.inf";case"uppercase":return"-.INF";case"camelcase":return"-.Inf"}else if(y.isNegativeZero(e))return"-0.0";return i=e.toString(10),en.test(i)?i.replace("e",".e"):i}function rn(e){return Object.prototype.toString.call(e)==="[object Number]"&&(e%1!==0||y.isNegativeZero(e))}var on=new v("tag:yaml.org,2002:float",{kind:"scalar",resolve:Xe,construct:Je,predicate:rn,represent:nn,defaultStyle:"lowercase"}),ln=Me.extend({implicit:[Ye,He,Ze,on]}),un=ln,re=new RegExp("^([0-9][0-9][0-9][0-9])-([0-9][0-9])-([0-9][0-9])$"),oe=new RegExp("^([0-9][0-9][0-9][0-9])-([0-9][0-9]?)-([0-9][0-9]?)(?:[Tt]|[ \\t]+)([0-9][0-9]?):([0-9][0-9]):([0-9][0-9])(?:\\.([0-9]*))?(?:[ \\t]*(Z|([-+])([0-9][0-9]?)(?::([0-9][0-9]))?))?$");function cn(e){return e===null?!1:re.exec(e)!==null||oe.exec(e)!==null}function tn(e){var n,i,o,r,u,l,c,t=0,s=null,h,f,m;if(n=re.exec(e),n===null&&(n=oe.exec(e)),n===null)throw new Error("Date resolve error");if(i=+n[1],o=+n[2]-1,r=+n[3],!n[4])return new Date(Date.UTC(i,o,r));if(u=+n[4],l=+n[5],c=+n[6],n[7]){for(t=n[7].slice(0,3);t.length<3;)t+="0";t=+t}return n[9]&&(h=+n[10],f=+(n[11]||0),s=(h*60+f)*6e4,n[9]==="-"&&(s=-s)),m=new Date(Date.UTC(i,o,r,u,l,c,t)),s&&m.setTime(m.getTime()-s),m}function fn(e){return e.toISOString()}var an=new v("tag:yaml.org,2002:timestamp",{kind:"scalar",resolve:cn,construct:tn,instanceOf:Date,represent:fn});function pn(e){return e==="<<"||e===null}var sn=new v("tag:yaml.org,2002:merge",{kind:"scalar",resolve:pn}),H=`ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=
\r`;function hn(e){if(e===null)return!1;var n,i,o=0,r=e.length,u=H;for(i=0;i<r;i++)if(n=u.indexOf(e.charAt(i)),!(n>64)){if(n<0)return!1;o+=6}return o%8===0}function dn(e){var n,i,o=e.replace(/[\r\n=]/g,""),r=o.length,u=H,l=0,c=[];for(n=0;n<r;n++)n%4===0&&n&&(c.push(l>>16&255),c.push(l>>8&255),c.push(l&255)),l=l<<6|u.indexOf(o.charAt(n));return i=r%4*6,i===0?(c.push(l>>16&255),c.push(l>>8&255),c.push(l&255)):i===18?(c.push(l>>10&255),c.push(l>>2&255)):i===12&&c.push(l>>4&255),new Uint8Array(c)}function mn(e){var n="",i=0,o,r,u=e.length,l=H;for(o=0;o<u;o++)o%3===0&&o&&(n+=l[i>>18&63],n+=l[i>>12&63],n+=l[i>>6&63],n+=l[i&63]),i=(i<<8)+e[o];return r=u%3,r===0?(n+=l[i>>18&63],n+=l[i>>12&63],n+=l[i>>6&63],n+=l[i&63]):r===2?(n+=l[i>>10&63],n+=l[i>>4&63],n+=l[i<<2&63],n+=l[64]):r===1&&(n+=l[i>>2&63],n+=l[i<<4&63],n+=l[64],n+=l[64]),n}function gn(e){return Object.prototype.toString.call(e)==="[object Uint8Array]"}var xn=new v("tag:yaml.org,2002:binary",{kind:"scalar",resolve:hn,construct:dn,predicate:gn,represent:mn}),bn=Object.prototype.hasOwnProperty,An=Object.prototype.toString;function vn(e){if(e===null)return!0;var n=[],i,o,r,u,l,c=e;for(i=0,o=c.length;i<o;i+=1){if(r=c[i],l=!1,An.call(r)!=="[object Object]")return!1;for(u in r)if(bn.call(r,u))if(!l)l=!0;else return!1;if(!l)return!1;if(n.indexOf(u)===-1)n.push(u);else return!1}return!0}function yn(e){return e!==null?e:[]}var kn=new v("tag:yaml.org,2002:omap",{kind:"sequence",resolve:vn,construct:yn}),wn=Object.prototype.toString;function Cn(e){if(e===null)return!0;var n,i,o,r,u,l=e;for(u=new Array(l.length),n=0,i=l.length;n<i;n+=1){if(o=l[n],wn.call(o)!=="[object Object]"||(r=Object.keys(o),r.length!==1))return!1;u[n]=[r[0],o[r[0]]]}return!0}function _n(e){if(e===null)return[];var n,i,o,r,u,l=e;for(u=new Array(l.length),n=0,i=l.length;n<i;n+=1)o=l[n],r=Object.keys(o),u[n]=[r[0],o[r[0]]];return u}var Tn=new v("tag:yaml.org,2002:pairs",{kind:"sequence",resolve:Cn,construct:_n}),Sn=Object.prototype.hasOwnProperty;function Fn(e){if(e===null)return!0;var n,i=e;for(n in i)if(Sn.call(i,n)&&i[n]!==null)return!1;return!0}function En(e){return e!==null?e:{}}var On=new v("tag:yaml.org,2002:set",{kind:"mapping",resolve:Fn,construct:En}),In=un.extend({implicit:[an,sn],explicit:[xn,kn,Tn,On]}),S=Object.prototype.hasOwnProperty,j=1,le=2,ue=3,M=4,R=1,Nn=2,W=3,Ln=/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F-\x84\x86-\x9F\uFFFE\uFFFF]|[\uD800-\uDBFF](?![\uDC00-\uDFFF])|(?:[^\uD800-\uDBFF]|^)[\uDC00-\uDFFF]/,jn=/[\x85\u2028\u2029]/,Mn=/[,\[\]\{\}]/,ce=/^(?:!|!!|![a-z\-]+!)$/i,te=/^(?:!|[^,\[\]\{\}])(?:%[0-9a-f]{2}|[0-9a-z\-#;\/\?:@&=\+\$,_\.!~\*'\(\)\[\]])*$/i;function Q(e){return Object.prototype.toString.call(e)}function C(e){return e===10||e===13}function F(e){return e===9||e===32}function k(e){return e===9||e===32||e===10||e===13}function O(e){return e===44||e===91||e===93||e===123||e===125}function Dn(e){var n;return 48<=e&&e<=57?e-48:(n=e|32,97<=n&&n<=102?n-97+10:-1)}function qn(e){return e===120?2:e===117?4:e===85?8:0}function Bn(e){return 48<=e&&e<=57?e-48:-1}function z(e){return e===48?"\0":e===97?"\x07":e===98?"\b":e===116||e===9?"	":e===110?`
`:e===118?"\v":e===102?"\f":e===114?"\r":e===101?"\x1B":e===32?" ":e===34?'"':e===47?"/":e===92?"\\":e===78?"":e===95?" ":e===76?"\u2028":e===80?"\u2029":""}function Yn(e){return e<=65535?String.fromCharCode(e):String.fromCharCode((e-65536>>10)+55296,(e-65536&1023)+56320)}var fe=new Array(256),ae=new Array(256);for(var E=0;E<256;E++)fe[E]=z(E)?1:0,ae[E]=z(E);function Pn(e,n){this.input=e,this.filename=n.filename||null,this.schema=n.schema||In,this.onWarning=n.onWarning||null,this.legacy=n.legacy||!1,this.json=n.json||!1,this.listener=n.listener||null,this.implicitTypes=this.schema.compiledImplicit,this.typeMap=this.schema.compiledTypeMap,this.length=e.length,this.position=0,this.line=0,this.lineStart=0,this.lineIndent=0,this.firstTabInLine=-1,this.documents=[]}function pe(e,n){var i={name:e.filename,buffer:e.input.slice(0,-1),position:e.position,line:e.line,column:e.position-e.lineStart};return i.snippet=_e(i),new _(n,i)}function a(e,n){throw pe(e,n)}function D(e,n){e.onWarning&&e.onWarning.call(null,pe(e,n))}var Z={YAML:function(n,i,o){var r,u,l;n.version!==null&&a(n,"duplication of %YAML directive"),o.length!==1&&a(n,"YAML directive accepts exactly one argument"),r=/^([0-9]+)\.([0-9]+)$/.exec(o[0]),r===null&&a(n,"ill-formed argument of the YAML directive"),u=parseInt(r[1],10),l=parseInt(r[2],10),u!==1&&a(n,"unacceptable YAML version of the document"),n.version=o[0],n.checkLineBreaks=l<2,l!==1&&l!==2&&D(n,"unsupported YAML version of the document")},TAG:function(n,i,o){var r,u;o.length!==2&&a(n,"TAG directive accepts exactly two arguments"),r=o[0],u=o[1],ce.test(r)||a(n,"ill-formed tag handle (first argument) of the TAG directive"),S.call(n.tagMap,r)&&a(n,'there is a previously declared suffix for "'+r+'" tag handle'),te.test(u)||a(n,"ill-formed tag prefix (second argument) of the TAG directive");try{u=decodeURIComponent(u)}catch{a(n,"tag prefix is malformed: "+u)}n.tagMap[r]=u}};function T(e,n,i,o){var r,u,l,c;if(n<i){if(c=e.input.slice(n,i),o)for(r=0,u=c.length;r<u;r+=1)l=c.charCodeAt(r),l===9||32<=l&&l<=1114111||a(e,"expected valid JSON character");else Ln.test(c)&&a(e,"the stream contains non-printable characters");e.result+=c}}function V(e,n,i,o){var r,u,l,c;for(y.isObject(i)||a(e,"cannot merge mappings; the provided source object is unacceptable"),r=Object.keys(i),l=0,c=r.length;l<c;l+=1)u=r[l],S.call(n,u)||(n[u]=i[u],o[u]=!0)}function I(e,n,i,o,r,u,l,c,t){var s,h;if(Array.isArray(r))for(r=Array.prototype.slice.call(r),s=0,h=r.length;s<h;s+=1)Array.isArray(r[s])&&a(e,"nested arrays are not supported inside keys"),typeof r=="object"&&Q(r[s])==="[object Object]"&&(r[s]="[object Object]");if(typeof r=="object"&&Q(r)==="[object Object]"&&(r="[object Object]"),r=String(r),n===null&&(n={}),o==="tag:yaml.org,2002:merge")if(Array.isArray(u))for(s=0,h=u.length;s<h;s+=1)V(e,n,u[s],i);else V(e,n,u,i);else!e.json&&!S.call(i,r)&&S.call(n,r)&&(e.line=l||e.line,e.lineStart=c||e.lineStart,e.position=t||e.position,a(e,"duplicated mapping key")),r==="__proto__"?Object.defineProperty(n,r,{configurable:!0,enumerable:!0,writable:!0,value:u}):n[r]=u,delete i[r];return n}function $(e){var n;n=e.input.charCodeAt(e.position),n===10?e.position++:n===13?(e.position++,e.input.charCodeAt(e.position)===10&&e.position++):a(e,"a line break is expected"),e.line+=1,e.lineStart=e.position,e.firstTabInLine=-1}function A(e,n,i){for(var o=0,r=e.input.charCodeAt(e.position);r!==0;){for(;F(r);)r===9&&e.firstTabInLine===-1&&(e.firstTabInLine=e.position),r=e.input.charCodeAt(++e.position);if(n&&r===35)do r=e.input.charCodeAt(++e.position);while(r!==10&&r!==13&&r!==0);if(C(r))for($(e),r=e.input.charCodeAt(e.position),o++,e.lineIndent=0;r===32;)e.lineIndent++,r=e.input.charCodeAt(++e.position);else break}return i!==-1&&o!==0&&e.lineIndent<i&&D(e,"deficient indentation"),o}function B(e){var n=e.position,i;return i=e.input.charCodeAt(n),!!((i===45||i===46)&&i===e.input.charCodeAt(n+1)&&i===e.input.charCodeAt(n+2)&&(n+=3,i=e.input.charCodeAt(n),i===0||k(i)))}function G(e,n){n===1?e.result+=" ":n>1&&(e.result+=y.repeat(`
`,n-1))}function Rn(e,n,i){var o,r,u,l,c,t,s,h,f=e.kind,m=e.result,p;if(p=e.input.charCodeAt(e.position),k(p)||O(p)||p===35||p===38||p===42||p===33||p===124||p===62||p===39||p===34||p===37||p===64||p===96||(p===63||p===45)&&(r=e.input.charCodeAt(e.position+1),k(r)||i&&O(r)))return!1;for(e.kind="scalar",e.result="",u=l=e.position,c=!1;p!==0;){if(p===58){if(r=e.input.charCodeAt(e.position+1),k(r)||i&&O(r))break}else if(p===35){if(o=e.input.charCodeAt(e.position-1),k(o))break}else{if(e.position===e.lineStart&&B(e)||i&&O(p))break;if(C(p))if(t=e.line,s=e.lineStart,h=e.lineIndent,A(e,!1,-1),e.lineIndent>=n){c=!0,p=e.input.charCodeAt(e.position);continue}else{e.position=l,e.line=t,e.lineStart=s,e.lineIndent=h;break}}c&&(T(e,u,l,!1),G(e,e.line-t),u=l=e.position,c=!1),F(p)||(l=e.position+1),p=e.input.charCodeAt(++e.position)}return T(e,u,l,!1),e.result?!0:(e.kind=f,e.result=m,!1)}function Un(e,n){var i,o,r;if(i=e.input.charCodeAt(e.position),i!==39)return!1;for(e.kind="scalar",e.result="",e.position++,o=r=e.position;(i=e.input.charCodeAt(e.position))!==0;)if(i===39)if(T(e,o,e.position,!0),i=e.input.charCodeAt(++e.position),i===39)o=e.position,e.position++,r=e.position;else return!0;else C(i)?(T(e,o,r,!0),G(e,A(e,!1,n)),o=r=e.position):e.position===e.lineStart&&B(e)?a(e,"unexpected end of the document within a single quoted scalar"):(e.position++,r=e.position);a(e,"unexpected end of the stream within a single quoted scalar")}function Hn(e,n){var i,o,r,u,l,c;if(c=e.input.charCodeAt(e.position),c!==34)return!1;for(e.kind="scalar",e.result="",e.position++,i=o=e.position;(c=e.input.charCodeAt(e.position))!==0;){if(c===34)return T(e,i,e.position,!0),e.position++,!0;if(c===92){if(T(e,i,e.position,!0),c=e.input.charCodeAt(++e.position),C(c))A(e,!1,n);else if(c<256&&fe[c])e.result+=ae[c],e.position++;else if((l=qn(c))>0){for(r=l,u=0;r>0;r--)c=e.input.charCodeAt(++e.position),(l=Dn(c))>=0?u=(u<<4)+l:a(e,"expected hexadecimal character");e.result+=Yn(u),e.position++}else a(e,"unknown escape sequence");i=o=e.position}else C(c)?(T(e,i,o,!0),G(e,A(e,!1,n)),i=o=e.position):e.position===e.lineStart&&B(e)?a(e,"unexpected end of the document within a double quoted scalar"):(e.position++,o=e.position)}a(e,"unexpected end of the stream within a double quoted scalar")}function $n(e,n){var i=!0,o,r,u,l=e.tag,c,t=e.anchor,s,h,f,m,p,g=Object.create(null),b,x,w,d;if(d=e.input.charCodeAt(e.position),d===91)h=93,p=!1,c=[];else if(d===123)h=125,p=!0,c={};else return!1;for(e.anchor!==null&&(e.anchorMap[e.anchor]=c),d=e.input.charCodeAt(++e.position);d!==0;){if(A(e,!0,n),d=e.input.charCodeAt(e.position),d===h)return e.position++,e.tag=l,e.anchor=t,e.kind=p?"mapping":"sequence",e.result=c,!0;i?d===44&&a(e,"expected the node content, but found ','"):a(e,"missed comma between flow collection entries"),x=b=w=null,f=m=!1,d===63&&(s=e.input.charCodeAt(e.position+1),k(s)&&(f=m=!0,e.position++,A(e,!0,n))),o=e.line,r=e.lineStart,u=e.position,N(e,n,j,!1,!0),x=e.tag,b=e.result,A(e,!0,n),d=e.input.charCodeAt(e.position),(m||e.line===o)&&d===58&&(f=!0,d=e.input.charCodeAt(++e.position),A(e,!0,n),N(e,n,j,!1,!0),w=e.result),p?I(e,c,g,x,b,w,o,r,u):f?c.push(I(e,null,g,x,b,w,o,r,u)):c.push(b),A(e,!0,n),d=e.input.charCodeAt(e.position),d===44?(i=!0,d=e.input.charCodeAt(++e.position)):i=!1}a(e,"unexpected end of the stream within a flow collection")}function Gn(e,n){var i,o,r=R,u=!1,l=!1,c=n,t=0,s=!1,h,f;if(f=e.input.charCodeAt(e.position),f===124)o=!1;else if(f===62)o=!0;else return!1;for(e.kind="scalar",e.result="";f!==0;)if(f=e.input.charCodeAt(++e.position),f===43||f===45)R===r?r=f===43?W:Nn:a(e,"repeat of a chomping mode identifier");else if((h=Bn(f))>=0)h===0?a(e,"bad explicit indentation width of a block scalar; it cannot be less than one"):l?a(e,"repeat of an indentation width identifier"):(c=n+h-1,l=!0);else break;if(F(f)){do f=e.input.charCodeAt(++e.position);while(F(f));if(f===35)do f=e.input.charCodeAt(++e.position);while(!C(f)&&f!==0)}for(;f!==0;){for($(e),e.lineIndent=0,f=e.input.charCodeAt(e.position);(!l||e.lineIndent<c)&&f===32;)e.lineIndent++,f=e.input.charCodeAt(++e.position);if(!l&&e.lineIndent>c&&(c=e.lineIndent),C(f)){t++;continue}if(e.lineIndent<c){r===W?e.result+=y.repeat(`
`,u?1+t:t):r===R&&u&&(e.result+=`
`);break}for(o?F(f)?(s=!0,e.result+=y.repeat(`
`,u?1+t:t)):s?(s=!1,e.result+=y.repeat(`
`,t+1)):t===0?u&&(e.result+=" "):e.result+=y.repeat(`
`,t):e.result+=y.repeat(`
`,u?1+t:t),u=!0,l=!0,t=0,i=e.position;!C(f)&&f!==0;)f=e.input.charCodeAt(++e.position);T(e,i,e.position,!1)}return!0}function X(e,n){var i,o=e.tag,r=e.anchor,u=[],l,c=!1,t;if(e.firstTabInLine!==-1)return!1;for(e.anchor!==null&&(e.anchorMap[e.anchor]=u),t=e.input.charCodeAt(e.position);t!==0&&(e.firstTabInLine!==-1&&(e.position=e.firstTabInLine,a(e,"tab characters must not be used in indentation")),!(t!==45||(l=e.input.charCodeAt(e.position+1),!k(l))));){if(c=!0,e.position++,A(e,!0,-1)&&e.lineIndent<=n){u.push(null),t=e.input.charCodeAt(e.position);continue}if(i=e.line,N(e,n,ue,!1,!0),u.push(e.result),A(e,!0,-1),t=e.input.charCodeAt(e.position),(e.line===i||e.lineIndent>n)&&t!==0)a(e,"bad indentation of a sequence entry");else if(e.lineIndent<n)break}return c?(e.tag=o,e.anchor=r,e.kind="sequence",e.result=u,!0):!1}function Kn(e,n,i){var o,r,u,l,c,t,s=e.tag,h=e.anchor,f={},m=Object.create(null),p=null,g=null,b=null,x=!1,w=!1,d;if(e.firstTabInLine!==-1)return!1;for(e.anchor!==null&&(e.anchorMap[e.anchor]=f),d=e.input.charCodeAt(e.position);d!==0;){if(!x&&e.firstTabInLine!==-1&&(e.position=e.firstTabInLine,a(e,"tab characters must not be used in indentation")),o=e.input.charCodeAt(e.position+1),u=e.line,(d===63||d===58)&&k(o))d===63?(x&&(I(e,f,m,p,g,null,l,c,t),p=g=b=null),w=!0,x=!0,r=!0):x?(x=!1,r=!0):a(e,"incomplete explicit mapping pair; a key node is missed; or followed by a non-tabulated empty line"),e.position+=1,d=o;else{if(l=e.line,c=e.lineStart,t=e.position,!N(e,i,le,!1,!0))break;if(e.line===u){for(d=e.input.charCodeAt(e.position);F(d);)d=e.input.charCodeAt(++e.position);if(d===58)d=e.input.charCodeAt(++e.position),k(d)||a(e,"a whitespace character is expected after the key-value separator within a block mapping"),x&&(I(e,f,m,p,g,null,l,c,t),p=g=b=null),w=!0,x=!1,r=!1,p=e.tag,g=e.result;else if(w)a(e,"can not read an implicit mapping pair; a colon is missed");else return e.tag=s,e.anchor=h,!0}else if(w)a(e,"can not read a block mapping entry; a multiline key may not be an implicit key");else return e.tag=s,e.anchor=h,!0}if((e.line===u||e.lineIndent>n)&&(x&&(l=e.line,c=e.lineStart,t=e.position),N(e,n,M,!0,r)&&(x?g=e.result:b=e.result),x||(I(e,f,m,p,g,b,l,c,t),p=g=b=null),A(e,!0,-1),d=e.input.charCodeAt(e.position)),(e.line===u||e.lineIndent>n)&&d!==0)a(e,"bad indentation of a mapping entry");else if(e.lineIndent<n)break}return x&&I(e,f,m,p,g,null,l,c,t),w&&(e.tag=s,e.anchor=h,e.kind="mapping",e.result=f),w}function Wn(e){var n,i=!1,o=!1,r,u,l;if(l=e.input.charCodeAt(e.position),l!==33)return!1;if(e.tag!==null&&a(e,"duplication of a tag property"),l=e.input.charCodeAt(++e.position),l===60?(i=!0,l=e.input.charCodeAt(++e.position)):l===33?(o=!0,r="!!",l=e.input.charCodeAt(++e.position)):r="!",n=e.position,i){do l=e.input.charCodeAt(++e.position);while(l!==0&&l!==62);e.position<e.length?(u=e.input.slice(n,e.position),l=e.input.charCodeAt(++e.position)):a(e,"unexpected end of the stream within a verbatim tag")}else{for(;l!==0&&!k(l);)l===33&&(o?a(e,"tag suffix cannot contain exclamation marks"):(r=e.input.slice(n-1,e.position+1),ce.test(r)||a(e,"named tag handle cannot contain such characters"),o=!0,n=e.position+1)),l=e.input.charCodeAt(++e.position);u=e.input.slice(n,e.position),Mn.test(u)&&a(e,"tag suffix cannot contain flow indicator characters")}u&&!te.test(u)&&a(e,"tag name cannot contain such characters: "+u);try{u=decodeURIComponent(u)}catch{a(e,"tag name is malformed: "+u)}return i?e.tag=u:S.call(e.tagMap,r)?e.tag=e.tagMap[r]+u:r==="!"?e.tag="!"+u:r==="!!"?e.tag="tag:yaml.org,2002:"+u:a(e,'undeclared tag handle "'+r+'"'),!0}function Qn(e){var n,i;if(i=e.input.charCodeAt(e.position),i!==38)return!1;for(e.anchor!==null&&a(e,"duplication of an anchor property"),i=e.input.charCodeAt(++e.position),n=e.position;i!==0&&!k(i)&&!O(i);)i=e.input.charCodeAt(++e.position);return e.position===n&&a(e,"name of an anchor node must contain at least one character"),e.anchor=e.input.slice(n,e.position),!0}function zn(e){var n,i,o;if(o=e.input.charCodeAt(e.position),o!==42)return!1;for(o=e.input.charCodeAt(++e.position),n=e.position;o!==0&&!k(o)&&!O(o);)o=e.input.charCodeAt(++e.position);return e.position===n&&a(e,"name of an alias node must contain at least one character"),i=e.input.slice(n,e.position),S.call(e.anchorMap,i)||a(e,'unidentified alias "'+i+'"'),e.result=e.anchorMap[i],A(e,!0,-1),!0}function N(e,n,i,o,r){var u,l,c,t=1,s=!1,h=!1,f,m,p,g,b,x;if(e.listener!==null&&e.listener("open",e),e.tag=null,e.anchor=null,e.kind=null,e.result=null,u=l=c=M===i||ue===i,o&&A(e,!0,-1)&&(s=!0,e.lineIndent>n?t=1:e.lineIndent===n?t=0:e.lineIndent<n&&(t=-1)),t===1)for(;Wn(e)||Qn(e);)A(e,!0,-1)?(s=!0,c=u,e.lineIndent>n?t=1:e.lineIndent===n?t=0:e.lineIndent<n&&(t=-1)):c=!1;if(c&&(c=s||r),(t===1||M===i)&&(j===i||le===i?b=n:b=n+1,x=e.position-e.lineStart,t===1?c&&(X(e,x)||Kn(e,x,b))||$n(e,b)?h=!0:(l&&Gn(e,b)||Un(e,b)||Hn(e,b)?h=!0:zn(e)?(h=!0,(e.tag!==null||e.anchor!==null)&&a(e,"alias node should not have any properties")):Rn(e,b,j===i)&&(h=!0,e.tag===null&&(e.tag="?")),e.anchor!==null&&(e.anchorMap[e.anchor]=e.result)):t===0&&(h=c&&X(e,x))),e.tag===null)e.anchor!==null&&(e.anchorMap[e.anchor]=e.result);else if(e.tag==="?"){for(e.result!==null&&e.kind!=="scalar"&&a(e,'unacceptable node kind for !<?> tag; it should be "scalar", not "'+e.kind+'"'),f=0,m=e.implicitTypes.length;f<m;f+=1)if(g=e.implicitTypes[f],g.resolve(e.result)){e.result=g.construct(e.result),e.tag=g.tag,e.anchor!==null&&(e.anchorMap[e.anchor]=e.result);break}}else if(e.tag!=="!"){if(S.call(e.typeMap[e.kind||"fallback"],e.tag))g=e.typeMap[e.kind||"fallback"][e.tag];else for(g=null,p=e.typeMap.multi[e.kind||"fallback"],f=0,m=p.length;f<m;f+=1)if(e.tag.slice(0,p[f].tag.length)===p[f].tag){g=p[f];break}g||a(e,"unknown tag !<"+e.tag+">"),e.result!==null&&g.kind!==e.kind&&a(e,"unacceptable node kind for !<"+e.tag+'> tag; it should be "'+g.kind+'", not "'+e.kind+'"'),g.resolve(e.result,e.tag)?(e.result=g.construct(e.result,e.tag),e.anchor!==null&&(e.anchorMap[e.anchor]=e.result)):a(e,"cannot resolve a node with !<"+e.tag+"> explicit tag")}return e.listener!==null&&e.listener("close",e),e.tag!==null||e.anchor!==null||h}function Zn(e){var n=e.position,i,o,r,u=!1,l;for(e.version=null,e.checkLineBreaks=e.legacy,e.tagMap=Object.create(null),e.anchorMap=Object.create(null);(l=e.input.charCodeAt(e.position))!==0&&(A(e,!0,-1),l=e.input.charCodeAt(e.position),!(e.lineIndent>0||l!==37));){for(u=!0,l=e.input.charCodeAt(++e.position),i=e.position;l!==0&&!k(l);)l=e.input.charCodeAt(++e.position);for(o=e.input.slice(i,e.position),r=[],o.length<1&&a(e,"directive name must not be less than one character in length");l!==0;){for(;F(l);)l=e.input.charCodeAt(++e.position);if(l===35){do l=e.input.charCodeAt(++e.position);while(l!==0&&!C(l));break}if(C(l))break;for(i=e.position;l!==0&&!k(l);)l=e.input.charCodeAt(++e.position);r.push(e.input.slice(i,e.position))}l!==0&&$(e),S.call(Z,o)?Z[o](e,o,r):D(e,'unknown document directive "'+o+'"')}if(A(e,!0,-1),e.lineIndent===0&&e.input.charCodeAt(e.position)===45&&e.input.charCodeAt(e.position+1)===45&&e.input.charCodeAt(e.position+2)===45?(e.position+=3,A(e,!0,-1)):u&&a(e,"directives end mark is expected"),N(e,e.lineIndent-1,M,!1,!0),A(e,!0,-1),e.checkLineBreaks&&jn.test(e.input.slice(n,e.position))&&D(e,"non-ASCII line breaks are interpreted as content"),e.documents.push(e.result),e.position===e.lineStart&&B(e)){e.input.charCodeAt(e.position)===46&&(e.position+=3,A(e,!0,-1));return}if(e.position<e.length-1)a(e,"end of the stream or a document separator is expected");else return}function se(e,n){e=String(e),n=n||{},e.length!==0&&(e.charCodeAt(e.length-1)!==10&&e.charCodeAt(e.length-1)!==13&&(e+=`
`),e.charCodeAt(0)===65279&&(e=e.slice(1)));var i=new Pn(e,n),o=e.indexOf("\0");for(o!==-1&&(i.position=o,a(i,"null byte is not allowed in input")),i.input+="\0";i.input.charCodeAt(i.position)===32;)i.lineIndent+=1,i.position+=1;for(;i.position<i.length-1;)Zn(i);return i.documents}function Vn(e,n,i){n!==null&&typeof n=="object"&&typeof i>"u"&&(i=n,n=null);var o=se(e,i);if(typeof n!="function")return o;for(var r=0,u=o.length;r<u;r+=1)n(o[r])}function Xn(e,n){var i=se(e,n);if(i.length!==0){if(i.length===1)return i[0];throw new _("expected a single document in the stream, but found more")}}var Jn=Vn,ei=Xn,ni={loadAll:Jn,load:ei},ii=ni.load;const J={CLIENT:1,AUTH:2},ee={CREATOR:1,AUTH:2};function oi(e){let n;try{n=ii(e)}catch(o){return{ok:!1,message:o.message}}if(n==null||n.poll==null)return{ok:!1,message:"Poll missing."};n.name=n.name||"Unnamed poll",n.image=n.image||"",n.begin=n.begin||new Date/1e3|0,n.end=n.end||null;{if(n.allow=n.allow||"CLIENT",typeof n.allow=="string"&&(n.allow=[n.allow]),!(n.allow instanceof Array))return{ok:!1,message:"allow must be string or a list of string."};let o=0,r=!1;for(const u of n.allow)switch(u){case"*":r=!0;break;case"CLIENT":o|=J.CLIENT;break;case"AUTH":o|=J.AUTH;break}r&&(o=0),n.allow=o}{if(n.res=n.res||"*",typeof n.res=="string"&&(n.res=[n.res]),!(n.res instanceof Array))return{ok:!1,message:"res must be string or a list of string."};let o=0,r=!1;for(const u of n.res)switch(u){case"*":r=!0;break;case"CREATOR":o|=ee.CREATOR;break;case"AUTH":o|=ee.AUTH;break}r&&(o=0),n.res=o}const i=new Set;for(const o of n.poll){if(typeof o!="object")return{ok:!1,message:"Questions must be an object."};const r=Object.keys(o)[0];if(i.has(r))return{ok:!1,message:"Duplicated question: `"+r+"`"};i.add(r);const u=o[r];if(u.type==null)return{ok:!1,message:"Question `"+r+"` must have a type."};switch(u.text=u.text||"",u.type){case"LABEL":u.label=u.label||"";break;case"CHOICE":{if(u.required=u.required||!1,u.choices==null)return{ok:!1,message:"Question `"+r+"` must have choices."};if(u.choices.length<1)return{ok:!1,message:"Question `"+r+"` must have at least 1 choice."};const l=new Set;for(const c of u.choices){if(typeof c!="object")return{ok:!1,message:"A choice in question `"+r+"` must be an object."};const t=Object.keys(c)[0];if(l.has(t))return{ok:!1,message:"Duplicated choice in question `"+r+"` named `"+t+"`"};l.add(t)}break}case"SHORT":break;default:return{ok:!1,message:"Unknown question type in question `"+r+"`"}}}return{ok:!0,yaml:n}}function li(e,n,i=!0){for(const o of n.poll){const r=Object.keys(o)[0],u=o[r],l=document.createElement("div");l.setAttribute("style","background-color: #3B3B3B;padding: 10px;margin: 15px;"+(i?"margin-left: auto;margin-right:auto;":"")+"border-radius: 5px;width: 600px"),l.setAttribute("id","pi_"+r);const c=document.createElement("h2");switch(c.setAttribute("style","color: #FFF; margin: 0;margin-bottom: 5px;"),c.innerText=u.text,l.appendChild(c),u.type){case"LABEL":{const t=document.createElement("p");t.setAttribute("style","color: #FFF;font-size: 12pt"),t.innerText=u.label,l.appendChild(t);break}case"CHOICE":{const t=document.createElement("div");t.setAttribute("style","display: flex;flex-direction: column");for(const s of u.choices){const h=Object.keys(s)[0],f=document.createElement("div");f.setAttribute("style","display: flex;flex-direction: row");const m=document.createElement("input");m.setAttribute("type","radio"),m.setAttribute("name",r),m.setAttribute("choice",h),f.appendChild(m);const p=document.createElement("p");p.setAttribute("style","color: #FFF;font-size: 12pt;margin-left: 7px"),p.innerText=s[h],f.appendChild(p),t.appendChild(f)}l.append(t);break}case"SHORT":{const t=document.createElement("input");t.setAttribute("style","color: #FFF; background-color: #2B2B2B;border: none; border-radius: 5px;width: 80%;font-size: 12pt"),l.appendChild(t);break}}e.appendChild(l)}}function q(e,n){for(const i of e.children)if(i.getAttribute("id")=="pi_"+n)return i;return null}function ui(e,n){let i={};for(const o of n.poll){const r=Object.keys(o)[0],u=o[r];switch(u.type){case"CHOICE":{const l=q(e,r);if(!l)return{ok:!1,message:"Failed to question block for `"+r+"`"};const c=l.querySelector("div > input:checked");if(!c){if(u.required)return{ok:!1,message:"You need to answer the question `"+(u.text||r)+"`"};continue}i[r]=c.getAttribute("choice");break}case"SHORT":{const l=q(e,r);if(!l)return{ok:!1,message:"Failed to question block for `"+r+"`"};const c=l.querySelector("input");if(!c)return{ok:!1,message:"Failed to input block for `"+r+"`"};i[r]=c.value;break}}}return{ok:!0,answers:i}}function ri(e,n){for(const i of e)if(i.key==n)return i.value;return null}function ci(e,n,i){for(const o of n.poll){const r=Object.keys(o)[0],u=ri(i,r);if(console.log(u),u==null)continue;switch(o[r].type){case"CHOICE":{const c=q(e,r);if(!c)continue;const t=c.querySelector('div > input[choice="'+u+'"]');if(!t)continue;t.checked=!0;break}case"SHORT":{const c=q(e,r);if(!c)continue;const t=c.querySelector("input");if(!t)continue;t.value=u;break}}}}export{J as A,li as d,ui as g,ci as r,oi as v};
