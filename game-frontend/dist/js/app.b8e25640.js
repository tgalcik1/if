(function(){"use strict";var e={2500:function(e,t,n){var s=n(3751),a=n(641);const o={id:"app"};function r(e,t,n,s,r,i){const d=(0,a.g2)("router-view");return(0,a.uX)(),(0,a.CE)("div",o,[(0,a.bF)(d)])}var i={name:"App"},d=n(6262);const u=(0,d.A)(i,[["render",r]]);var c=u,l=n(5220);n(4114);const p=e=>((0,a.Qi)("data-v-3611ff15"),e=e(),(0,a.jt)(),e),v={class:"title"},m=p((()=>(0,a.Lk)("h1",{style:{"background-color":"black",color:"white",padding:"16px"}},"Heir of the Profane",-1))),g=p((()=>(0,a.Lk)("h3",null,"An LLM-Based Text Adventure Game",-1))),f=p((()=>(0,a.Lk)("button",null,"Exit Game",-1)));function h(e,t){return(0,a.uX)(),(0,a.CE)("div",v,[m,g,(0,a.Lk)("button",{onClick:t[0]||(t[0]=e=>this.$router.push("/game"))},"Start Game"),f])}const y={},b=(0,d.A)(y,[["render",h],["__scopeId","data-v-3611ff15"]]);var w=b;const k={class:"game-container"};function L(e,t,n,s,o,r){const i=(0,a.g2)("Navbar"),d=(0,a.g2)("Sidebar"),u=(0,a.g2)("DialogueWindow"),c=(0,a.g2)("InputBar");return(0,a.uX)(),(0,a.CE)("div",k,[(0,a.bF)(i),(0,a.bF)(d),(0,a.bF)(u,{ref:"dialogueWindow"},null,512),(0,a.bF)(c,{onPlayerMessage:r.handlePlayerMessage},null,8,["onPlayerMessage"])])}const _=e=>((0,a.Qi)("data-v-06d35684"),e=e(),(0,a.jt)(),e),C={class:"navbar"},M=_((()=>(0,a.Lk)("p",{style:{"margin-left":"16px"}},"Heir of the Profane",-1))),E=_((()=>(0,a.Lk)("button",{style:{height:"40px"},disabled:""},"Settings",-1)));function I(e,t){return(0,a.uX)(),(0,a.CE)("div",C,[M,(0,a.Lk)("div",null,[E,(0,a.Lk)("button",{style:{height:"40px"},onClick:t[0]||(t[0]=e=>this.$router.push("/"))},"Return to Title")])])}const x={},X=(0,d.A)(x,[["render",I],["__scopeId","data-v-06d35684"]]);var A=X;const j={class:"sidebar"};function F(e,t,n,s,o,r){const i=(0,a.g2)("Map"),d=(0,a.g2)("Inventory"),u=(0,a.g2)("Quests");return(0,a.uX)(),(0,a.CE)("div",j,[(0,a.bF)(i),(0,a.bF)(d),(0,a.bF)(u)])}const O=e=>((0,a.Qi)("data-v-04f5c1d6"),e=e(),(0,a.jt)(),e),P={class:"map"},Q=O((()=>(0,a.Lk)("p",null,"Map",-1))),T=O((()=>(0,a.Lk)("div",{class:"window"},null,-1))),B=[Q,T];function S(e,t){return(0,a.uX)(),(0,a.CE)("div",P,B)}const W={},$=(0,d.A)(W,[["render",S],["__scopeId","data-v-04f5c1d6"]]);var G=$;const D=e=>((0,a.Qi)("data-v-33ac0bdb"),e=e(),(0,a.jt)(),e),H={class:"inventory"},K=D((()=>(0,a.Lk)("p",null,"Inventory",-1))),q={class:"grid"},N=D((()=>(0,a.Lk)("img",{src:"",alt:".",style:{width:"100%"}},null,-1))),R=[N];function U(e,t,n,s,o,r){return(0,a.uX)(),(0,a.CE)("div",H,[K,(0,a.Lk)("div",q,[((0,a.uX)(!0),(0,a.CE)(a.FK,null,(0,a.pI)(o.maxItems,(e=>((0,a.uX)(),(0,a.CE)("div",{class:"item-slot",key:e},R)))),128))])])}var V={name:"Inventory",data(){return{maxItems:56}}};const J=(0,d.A)(V,[["render",U],["__scopeId","data-v-33ac0bdb"]]);var z=J;const Y=e=>((0,a.Qi)("data-v-0916de65"),e=e(),(0,a.jt)(),e),Z={class:"quests"},ee=Y((()=>(0,a.Lk)("p",null,"Quests",-1))),te=Y((()=>(0,a.Lk)("div",{class:"quest-list"},null,-1))),ne=[ee,te];function se(e,t){return(0,a.uX)(),(0,a.CE)("div",Z,ne)}const ae={},oe=(0,d.A)(ae,[["render",se],["__scopeId","data-v-0916de65"]]);var re=oe,ie={name:"Sidebar",components:{Map:G,Inventory:z,Quests:re}};const de=(0,d.A)(ie,[["render",F],["__scopeId","data-v-579d572d"]]);var ue=de,ce=n(33);const le={class:"dialogue-window",ref:"dialogueWindow"},pe={key:0,class:"system-message"},ve={key:1,class:"player-message"};function me(e,t,n,s,o,r){return(0,a.uX)(),(0,a.CE)("div",le,[((0,a.uX)(!0),(0,a.CE)(a.FK,null,(0,a.pI)(o.messages,((e,t)=>((0,a.uX)(),(0,a.CE)("div",{class:"messages",key:t},["system"==e.type?((0,a.uX)(),(0,a.CE)("div",pe,[(0,a.Lk)("p",null,(0,ce.v_)(e.text),1)])):(0,a.Q3)("",!0),"player"==e.type?((0,a.uX)(),(0,a.CE)("div",ve,[(0,a.Lk)("p",null,(0,ce.v_)(e.text),1)])):(0,a.Q3)("",!0)])))),128))],512)}var ge={name:"DialogueWindow",data(){return{messages:[]}},methods:{addPlayerMessage(e){this.messages.push({type:"player",text:e}),this.scrollToBottom()},addSystemMessage(e){this.messages.push({type:"system",text:e}),this.scrollToBottom()},scrollToBottom(){this.$nextTick((()=>{const e=this.$refs.dialogueWindow;e&&e.scrollTo({top:e.scrollHeight,behavior:"smooth"})}))}},mounted(){this.scrollToBottom(),window.api&&window.api.receive&&window.api.receive("fromMain",(e=>{"message"==e.type&&this.addSystemMessage(e.message)}))}};const fe=(0,d.A)(ge,[["render",me],["__scopeId","data-v-50d357a2"]]);var he=fe;const ye={class:"input-bar"};function be(e,t,n,o,r,i){return(0,a.uX)(),(0,a.CE)("div",ye,[(0,a.bo)((0,a.Lk)("input",{"onUpdate:modelValue":t[0]||(t[0]=e=>r.message=e),onKeyup:t[1]||(t[1]=(0,s.jR)(((...e)=>i.sendMessage&&i.sendMessage(...e)),["enter"])),style:{width:"100%"}},null,544),[[s.Jo,r.message]]),(0,a.Lk)("button",{onClick:t[2]||(t[2]=(...e)=>i.sendMessage&&i.sendMessage(...e))},"Send")])}var we={name:"InputBar",data(){return{message:""}},methods:{sendMessage(){this.message&&(this.$emit("player-message",this.message),window.api.send("toMain",{command:"send-message",message:this.message}),this.message="")}}};const ke=(0,d.A)(we,[["render",be],["__scopeId","data-v-427620f6"]]);var Le=ke,_e={name:"GameView",components:{Navbar:A,Sidebar:ue,DialogueWindow:he,InputBar:Le},methods:{handlePlayerMessage(e){this.$refs.dialogueWindow.addPlayerMessage(e)}},mounted(){window.api.send("toMain",{command:"start-game"})},beforeUnmount(){window.api.send("toMain",{command:"end-game"})}};const Ce=(0,d.A)(_e,[["render",L]]);var Me=Ce;const Ee=[{path:"/",name:"title",component:w},{path:"/game",name:"game",component:Me}],Ie=(0,l.aE)({history:(0,l.LA)(),routes:Ee});var xe=Ie;const Xe=(0,s.Ef)(c);Xe.use(xe),Xe.mount("#app")}},t={};function n(s){var a=t[s];if(void 0!==a)return a.exports;var o=t[s]={exports:{}};return e[s].call(o.exports,o,o.exports,n),o.exports}n.m=e,function(){var e=[];n.O=function(t,s,a,o){if(!s){var r=1/0;for(c=0;c<e.length;c++){s=e[c][0],a=e[c][1],o=e[c][2];for(var i=!0,d=0;d<s.length;d++)(!1&o||r>=o)&&Object.keys(n.O).every((function(e){return n.O[e](s[d])}))?s.splice(d--,1):(i=!1,o<r&&(r=o));if(i){e.splice(c--,1);var u=a();void 0!==u&&(t=u)}}return t}o=o||0;for(var c=e.length;c>0&&e[c-1][2]>o;c--)e[c]=e[c-1];e[c]=[s,a,o]}}(),function(){n.d=function(e,t){for(var s in t)n.o(t,s)&&!n.o(e,s)&&Object.defineProperty(e,s,{enumerable:!0,get:t[s]})}}(),function(){n.g=function(){if("object"===typeof globalThis)return globalThis;try{return this||new Function("return this")()}catch(e){if("object"===typeof window)return window}}()}(),function(){n.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)}}(),function(){var e={524:0};n.O.j=function(t){return 0===e[t]};var t=function(t,s){var a,o,r=s[0],i=s[1],d=s[2],u=0;if(r.some((function(t){return 0!==e[t]}))){for(a in i)n.o(i,a)&&(n.m[a]=i[a]);if(d)var c=d(n)}for(t&&t(s);u<r.length;u++)o=r[u],n.o(e,o)&&e[o]&&e[o][0](),e[o]=0;return n.O(c)},s=self["webpackChunkcognitive_battery_app"]=self["webpackChunkcognitive_battery_app"]||[];s.forEach(t.bind(null,0)),s.push=t.bind(null,s.push.bind(s))}();var s=n.O(void 0,[504],(function(){return n(2500)}));s=n.O(s)})();
//# sourceMappingURL=app.b8e25640.js.map