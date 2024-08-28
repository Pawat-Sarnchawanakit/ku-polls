import{_ as P,r as u,f as S,o as v,c as h,a as n,n as m,u as y,g as F,t as B,p as N,d as z,e as O}from"./_plugin-vue_export-helper-DUaCvcyY.js";import{v as Y,A as b,d as j,g as A}from"./poll_loader-glaRrpo0.js";import{h as E,e as V}from"./edit-B0qfXUHy.js";const J="data:image/svg+xml,%3csvg%20xmlns='http://www.w3.org/2000/svg'%20width='1em'%20height='1em'%20viewBox='0%200%2024%2024'%3e%3cpath%20fill='white'%20d='M2%2021v-2h20v2zm1-3v-7h3v7zm5%200V6h3v12zm5%200V9h3v9zm5%200V3h3v15z'/%3e%3c/svg%3e",T=d=>(N("data-v-ba8afcb5"),d=d(),z(),d),L={style:{"background-color":"transparent",height:"100%",overflow:"auto"}},$={style:{display:"flex","flex-direction":"row"}},q={href:"/"},D=T(()=>n("br",null,null,-1)),H=T(()=>n("p",{style:{color:"#FFF",margin:"auto","text-align":"center"}},"Press ESC to close.",-1)),U={key:0,style:{display:"flex","justify-content":"center","margin-bottom":"10px"}},G={__name:"Poll",setup(d){var k=!1;const w=u(!1),_=u(!1),l=u("#FFF"),a=u("Please answer all questions."),s=u(!1),g=u(!1),f=u(null);let t=!1;const r=document.location.pathname.split("/").filter(o=>o.length!=0)[1];let i;function C(){document.location.href=window.location.protocol+"//"+window.location.host+"/res/"+r}function M(){document.location.href=window.location.protocol+"//"+window.location.host+"/create/"+r}async function x(o){if(o.yaml!=null){const e=Y(o.yaml);if(!e.ok){t=!0,l.value="#F00",a.value=e.message,s.value.showModal();return}e.res==0&&(w.value=!0),i=e.yaml,t=!0,i.allow==0?t=!1:(i.allow&b.CLIENT&&(localStorage.getItem("answered_"+r)=="y"?(l.value="#FFF",a.value="You already answered this poll.",s.value.showModal(),t=!0):t=!1),t&&i.allow&b.AUTH&&(t=!0,await(await fetch(window.location.protocol+"//"+window.location.host+"/gyatt",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({f:"aa",n:r})})).text()!="y"?t=!1:(l.value="#FFF",a.value="You already answered this poll.",s.value.showModal()))),j(f.value,i)}else{const e=document.createElement("h1");e.innerText="You don't have permission to view this poll.",e.style.color="#FFF",e.style.margin="auto",e.style.textAlign="center",f.value.appendChild(e)}o.closed?(t=!0,l.value="#F00",a.value="This poll is already closed.",s.value.showModal()):o.can_vote||(t=!0,l.value="#F00",a.value="You do not have permission to vote in this poll.",s.value.showModal()),t||(g.value=!0)}S(()=>k=!0),fetch(window.location.protocol+"//"+window.location.host+"/gyatt",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({f:"get",n:r})}).then(o=>o.json().then(e=>(e.is_creator&&(_.value=!0),e.can_res&&(w.value=!0),k?x(e):S(()=>x(e.yaml)))));function I(){if(t)return;t=!0;const o=A(f.value,i);if(!o.ok){l.value="#F00",a.value=o.message,s.value.showModal(),t=!1;return}l.value="#FFF",a.value="Please wait, submitting...",s.value.showModal(),fetch(window.location.protocol+"//"+window.location.host+"/gyatt",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({f:"submit",n:r,r:o.answers})}).then(e=>e.text().then(c=>{!e.ok&&c==""&&(c=e.statusText);const p=c=="ok";if(l.value=p?"#FFF":"#F00",a.value=p?"Your response has been recorded.":c,s.value.showModal(),!p){t=!1;return}t&&(g.value=!1),i.allow!=0&&i.allow&b.CLIENT&&localStorage.setItem("answered_"+r,"y")})).catch(()=>{l.value="#F00",a.value="Failed to submit response.",s.value.showModal(),t=!1})}return(o,e)=>(v(),h("div",L,[n("div",$,[n("a",q,[n("input",{class:"left-btn",style:m({"background-image":`url("${y(E)}")`}),type:"button"},null,4)]),w.value||_.value?(v(),h("input",{key:0,onClick:C,class:"left-btn",style:m({"background-image":`url("${y(J)}")`}),type:"button"},null,4)):F("",!0),_.value?(v(),h("input",{key:1,onClick:M,class:"left-btn",style:m({"background-image":`url("${y(V)}")`}),type:"button"},null,4)):F("",!0)]),n("dialog",{ref_key:"dlg",ref:s,style:{"background-color":"#2B2B2B",border:"none","border-radius":"10px"}},[n("h1",{style:m({color:l.value})},B(a.value),5),D,H],512),n("div",{ref_key:"poll",ref:f},null,512),g.value?(v(),h("div",U,[n("button",{onClick:I},"Submit")])):F("",!0)]))}},K=P(G,[["__scopeId","data-v-ba8afcb5"]]);O(K).mount("#app");