import{_ as p,r as d,o as s,c as o,a as t,u as c,b as _,F as m,d as h,n as g,t as l,p as f,e as v,f as b}from"./_plugin-vue_export-helper-DBQglHaf.js";import{l as u}from"./common-Bjy0tg9W.js";const y=a=>(f("data-v-0d24e1a0"),a=a(),v(),a),I={class:"holder"},S={class:"header"},k=y(()=>t("a",{href:"/create/"},[t("button",{class:"header-btn"},"Create a poll")],-1)),B={class:"grid"},C=["href"],x={__name:"Home",setup(a){const n=d([]),i=d(document.getElementById("authenticated")!=null);return n.value=JSON.parse(document.getElementById("server-data").innerText),(N,r)=>(s(),o("div",I,[t("div",S,[k,i.value?(s(),o("button",{key:0,onClick:r[0]||(r[0]=(...e)=>c(u)&&c(u)(...e)),class:"header-btn"},"Logout")):_("",!0)]),t("div",B,[(s(!0),o(m,null,h(n.value,e=>(s(),o("a",{href:"/poll/"+e.id},[t("div",{style:g({"background-image":"url("+e.image+")"}),class:"grid-itm"},[t("h3",null,l(e.name)+" "+l(e.open?"(Open)":"(Closed)"),1)],4)],8,C))),256))])]))}},E=p(x,[["__scopeId","data-v-0d24e1a0"]]);b(E).mount("#app");