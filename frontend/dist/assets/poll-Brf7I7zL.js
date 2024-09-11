import{_ as Y,r as i,g as $,o as d,c as v,a as r,n as p,u,b as f,t as T,p as L,e as O,f as A}from"./_plugin-vue_export-helper-DBQglHaf.js";import{a as C,l as S}from"./common-Bjy0tg9W.js";import{v as j,A as z,d as q,r as H,g as J}from"./poll_loader-DlehWYRP.js";import{h as D,e as G,l as K,a as Q}from"./logout-C7V15774.js";const R="data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20width='1em'%20height='1em'%20viewBox='0%200%2024%2024'%3e%3cpath%20fill='white'%20d='M2%2021v-2h20v2zm1-3v-7h3v7zm5%200V6h3v12zm5%200V9h3v9zm5%200V3h3v15z'/%3e%3c/svg%3e",U="data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20width='1em'%20height='1em'%20viewBox='0%200%2024%2024'%3e%3cpath%20fill='white'%20d='M7%2021q-.825%200-1.412-.587T5%2019V6H4V4h5V3h6v1h5v2h-1v13q0%20.825-.587%201.413T17%2021zM17%206H7v13h10zM9%2017h2V8H9zm4%200h2V8h-2zM7%206v13z'/%3e%3c/svg%3e",V=g=>(L("data-v-73a3df6a"),g=g(),O(),g),W={style:{"background-color":"transparent",height:"100%",overflow:"auto"}},X={style:{display:"flex","flex-direction":"row"}},Z={href:"/"},ee=V(()=>r("br",null,null,-1)),te=V(()=>r("p",{style:{color:"#FFF",margin:"auto","text-align":"center"}},"Press ESC to close.",-1)),le={key:0,style:{display:"flex","justify-content":"center","margin-bottom":"10px"}},oe={__name:"Poll",setup(g){const b=i("Submit"),y=i(!1),F=i(!1),x=i(!1),o=i("#FFF"),a=i("Please answer all questions."),s=i(!1),w=i(!1),m=i(null),h=JSON.parse(document.getElementById("server-data").innerText),M=i(h.auth);let t=!1;const _=document.location.pathname.split("/").filter(l=>l.length!=0)[1];let c;h.is_creator&&(F.value=!0),h.can_res&&(y.value=!0),$(()=>E(h));function B(){document.location.href=window.location.protocol+"//"+window.location.host+"/res/"+h.id}function I(){document.location.href=window.location.protocol+"//"+window.location.host+"/create/"+h.id}function E(l){if(l.yaml!=null){const e=j(l.yaml);if(!e.ok){t=!0,o.value="#F00",a.value=e.message,s.value.showModal();return}e.res==0&&(y.value=!0),c=e.yaml,t=!0,c.allow==0?t=!1:c.allow&z.CLIENT&&localStorage.getItem("answered_"+_)=="y"?(o.value="#FFF",a.value="You already answered this poll.",s.value.showModal(),t=!0):t=!1,q(m.value,c),!t&&l.prev_ans.length>0&&(x.value=!0,H(m.value,e.yaml,l.prev_ans),o.value="#FFF",a.value="You already answered this poll.",s.value.showModal(),b.value="Change answers")}else{const e=document.createElement("h1");e.innerText="You don't have permission to view this poll.",e.style.color="#FFF",e.style.margin="auto",e.style.textAlign="center",m.value.appendChild(e)}l.closed?(t=!0,o.value="#F00",a.value="This poll is already closed.",s.value.showModal()):l.can_vote||(t=!0,o.value="#F00",a.value="You do not have permission to vote in this poll.",s.value.showModal()),t||(w.value=!0)}function N(){fetch(window.location.protocol+"//"+window.location.host+"/gyatt",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({f:"submit",n:_,r:[]})}).then(l=>l.text().then(e=>{!l.ok&&e==""&&(e=l.statusText);const n=e=="ok";if(o.value=n?"#FFF":"#F00",a.value=n?"Your response has been deleted.":e,s.value.showModal(),!n){t=!1;return}t&&(w.value=!1),setTimeout(()=>window.location.reload(!0),500)})).catch(()=>{o.value="#F00",a.value="Failed to delete response.",s.value.showModal(),t=!1})}function P(){if(t)return;t=!0;const l=J(m.value,c);if(!l.ok){o.value="#F00",a.value=l.message,s.value.showModal(),t=!1;return}o.value="#FFF",a.value="Please wait, submitting...",s.value.showModal(),fetch(window.location.protocol+"//"+window.location.host+"/gyatt",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({f:"submit",n:_,r:l.answers})}).then(e=>e.text().then(n=>{!e.ok&&n==""&&(n=e.statusText);const k=n=="ok";if(o.value=k?"#FFF":"#F00",a.value=k?"Your response has been recorded.":n,s.value.showModal(),!k){t=!1;return}t&&(w.value=!1),c.allow!=0&&c.allow&z.CLIENT&&localStorage.setItem("answered_"+_,"y"),setTimeout(()=>window.location.reload(!0),500)})).catch(()=>{o.value="#F00",a.value="Failed to submit response.",s.value.showModal(),t=!1})}return(l,e)=>(d(),v("div",W,[r("div",X,[r("a",Z,[r("input",{class:"left-btn",style:p({"background-image":`url("${u(D)}")`}),type:"button"},null,4)]),y.value||F.value?(d(),v("input",{key:0,title:"View responses",onClick:B,class:"left-btn",style:p({"background-image":`url("${u(R)}")`}),type:"button"},null,4)):f("",!0),F.value?(d(),v("input",{key:1,title:"Edit poll",onClick:I,class:"left-btn",style:p({"background-image":`url("${u(G)}")`}),type:"button"},null,4)):f("",!0),x.value?(d(),v("input",{key:2,title:"Delete responses",onClick:N,class:"left-btn",style:p({"background-image":`url("${u(U)}")`}),type:"button"},null,4)):f("",!0),M.value?f("",!0):(d(),v("input",{key:3,title:"Login",onClick:e[0]||(e[0]=(...n)=>u(C)&&u(C)(...n)),class:"left-btn",style:p({"background-image":`url("${u(K)}")`}),type:"button"},null,4)),M.value?(d(),v("input",{key:4,title:"Logout",onClick:e[1]||(e[1]=(...n)=>u(S)&&u(S)(...n)),class:"left-btn",style:p({"background-image":`url("${u(Q)}")`}),type:"button"},null,4)):f("",!0)]),r("dialog",{ref_key:"dlg",ref:s,style:{"background-color":"#2B2B2B",border:"none","border-radius":"10px"}},[r("h1",{style:p({color:o.value})},T(a.value),5),ee,te],512),r("div",{ref_key:"poll",ref:m},null,512),w.value?(d(),v("div",le,[r("button",{onClick:P},T(b.value),1)])):f("",!0)]))}},ae=Y(oe,[["__scopeId","data-v-73a3df6a"]]);A(ae).mount("#app");
