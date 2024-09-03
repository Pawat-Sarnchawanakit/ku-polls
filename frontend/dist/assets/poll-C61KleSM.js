import{_ as z,r as i,f as E,o as p,c as f,a as n,n as m,u as F,g as b,t as x,p as N,d as P,e as Y}from"./_plugin-vue_export-helper-DUaCvcyY.js";import{v as V,A as S,d as A,r as L,g as O}from"./poll_loader-DlehWYRP.js";import{h as $,e as j}from"./edit-B0qfXUHy.js";const J="data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20width='1em'%20height='1em'%20viewBox='0%200%2024%2024'%3e%3cpath%20fill='white'%20d='M2%2021v-2h20v2zm1-3v-7h3v7zm5%200V6h3v12zm5%200V9h3v9zm5%200V3h3v15z'/%3e%3c/svg%3e",M=d=>(N("data-v-df1cdc5b"),d=d(),P(),d),q={style:{"background-color":"transparent",height:"100%",overflow:"auto"}},D={style:{display:"flex","flex-direction":"row"}},G={href:"/"},H=M(()=>n("br",null,null,-1)),K=M(()=>n("p",{style:{color:"#FFF",margin:"auto","text-align":"center"}},"Press ESC to close.",-1)),Q={key:0,style:{display:"flex","justify-content":"center","margin-bottom":"10px"}},R={__name:"Poll",setup(d){const k=i("Submit"),h=i(!1),_=i(!1),o=i("#FFF"),a=i("Please answer all questions."),s=i(!1),w=i(!1),u=i(null),c=JSON.parse(document.getElementById("server-data").innerText);let e=!1;const g=document.location.pathname.split("/").filter(t=>t.length!=0)[1];let r;c.is_creator&&(_.value=!0),c.can_res&&(h.value=!0),E(()=>I(c));function C(){document.location.href=window.location.protocol+"//"+window.location.host+"/res/"+c.id}function T(){document.location.href=window.location.protocol+"//"+window.location.host+"/create/"+c.id}function I(t){if(t.yaml!=null){const l=V(t.yaml);if(!l.ok){e=!0,o.value="#F00",a.value=l.message,s.value.showModal();return}l.res==0&&(h.value=!0),r=l.yaml,e=!0,r.allow==0?e=!1:r.allow&S.CLIENT&&localStorage.getItem("answered_"+g)=="y"?(o.value="#FFF",a.value="You already answered this poll.",s.value.showModal(),e=!0):e=!1,A(u.value,r),!e&&t.prev_ans.length>0&&(L(u.value,l.yaml,t.prev_ans),o.value="#FFF",a.value="You already answered this poll.",s.value.showModal(),k.value="Change answers")}else{const l=document.createElement("h1");l.innerText="You don't have permission to view this poll.",l.style.color="#FFF",l.style.margin="auto",l.style.textAlign="center",u.value.appendChild(l)}t.closed?(e=!0,o.value="#F00",a.value="This poll is already closed.",s.value.showModal()):t.can_vote||(e=!0,o.value="#F00",a.value="You do not have permission to vote in this poll.",s.value.showModal()),e||(w.value=!0)}function B(){if(e)return;e=!0;const t=O(u.value,r);if(!t.ok){o.value="#F00",a.value=t.message,s.value.showModal(),e=!1;return}o.value="#FFF",a.value="Please wait, submitting...",s.value.showModal(),fetch(window.location.protocol+"//"+window.location.host+"/gyatt",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({f:"submit",n:g,r:t.answers})}).then(l=>l.text().then(v=>{!l.ok&&v==""&&(v=l.statusText);const y=v=="ok";if(o.value=y?"#FFF":"#F00",a.value=y?"Your response has been recorded.":v,s.value.showModal(),!y){e=!1;return}e&&(w.value=!1),r.allow!=0&&r.allow&S.CLIENT&&localStorage.setItem("answered_"+g,"y"),setTimeout(()=>window.location.reload(!0),500)})).catch(()=>{o.value="#F00",a.value="Failed to submit response.",s.value.showModal(),e=!1})}return(t,l)=>(p(),f("div",q,[n("div",D,[n("a",G,[n("input",{class:"left-btn",style:m({"background-image":`url("${F($)}")`}),type:"button"},null,4)]),h.value||_.value?(p(),f("input",{key:0,onClick:C,class:"left-btn",style:m({"background-image":`url("${F(J)}")`}),type:"button"},null,4)):b("",!0),_.value?(p(),f("input",{key:1,onClick:T,class:"left-btn",style:m({"background-image":`url("${F(j)}")`}),type:"button"},null,4)):b("",!0)]),n("dialog",{ref_key:"dlg",ref:s,style:{"background-color":"#2B2B2B",border:"none","border-radius":"10px"}},[n("h1",{style:m({color:o.value})},x(a.value),5),H,K],512),n("div",{ref_key:"poll",ref:u},null,512),w.value?(p(),f("div",Q,[n("button",{onClick:B},x(k.value),1)])):b("",!0)]))}},U=z(R,[["__scopeId","data-v-df1cdc5b"]]);Y(U).mount("#app");
