import streamlit as st
import base64
import os

st.set_page_config(layout="wide")

# ── CONFIG ────────────────────────────────────────────────────────────────────
IMG_PATH    = "launch_place.jpg"
FINAL_PATH  = "final.mp4"
LAUNCH_DATE = "2026-06-13T00:00:00"

# ── LOAD ASSETS ───────────────────────────────────────────────────────────────
with open(IMG_PATH, "rb") as f:
    img_b64 = base64.b64encode(f.read()).decode()
with open(FINAL_PATH, "rb") as f:
    final_b64 = base64.b64encode(f.read()).decode()


HTML = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{margin:0;padding:0;box-sizing:border-box;}
html,body{width:100%;height:100%;overflow:hidden;background:#000;font-family:Orbitron,sans-serif;}

.layer{position:fixed;inset:0;transition:opacity 0.9s ease;}
.layer.hidden{opacity:0;pointer-events:none;}

/* ── PHASE 0 · TIMER (MISSION CONTROL) ── */
#l-timer{
  background:#00030e;z-index:10;
  display:flex;flex-direction:column;
  align-items:center;justify-content:center;
  overflow:hidden;
}
/* Scrolling grid */
#l-timer::before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background-image:
    linear-gradient(rgba(0,205,255,0.042) 1px,transparent 1px),
    linear-gradient(90deg,rgba(0,205,255,0.042) 1px,transparent 1px);
  background-size:54px 54px;
  animation:gridScroll 20s linear infinite;
}
/* Horizontal sweep scanline */
#l-timer::after{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(180deg,transparent 0%,rgba(0,215,255,0.026) 50%,transparent 100%);
  background-size:100% 280px;
  animation:scanSweep 8s linear infinite;
}
@keyframes gridScroll{to{background-position:54px 54px;}}
@keyframes scanSweep{from{background-position:0 -280px;}to{background-position:0 110vh;}}

/* Top status bar */
.mc-topbar{
  position:absolute;top:0;left:0;right:0;z-index:3;
  display:flex;justify-content:space-between;align-items:center;
  padding:10px 32px;
  border-bottom:1px solid rgba(0,205,255,0.13);
  font-size:11px;letter-spacing:3.5px;color:rgba(0,175,255,0.68);
}
.mc-topbar-item{display:flex;align-items:center;gap:8px;}
.mc-dot{
  width:6px;height:6px;border-radius:50%;
  background:#00c8ff;box-shadow:0 0 7px #00c8ff;
  animation:dotBlink 1.7s ease-in-out infinite;
}
.mc-dot.slow{animation-duration:3.4s;}
@keyframes dotBlink{0%,100%{opacity:1;}50%{opacity:0.18;}}

/* Bottom status bar */
.mc-botbar{
  position:absolute;bottom:0;left:0;right:0;z-index:3;
  display:flex;justify-content:center;align-items:center;gap:20px;
  padding:10px 32px;
  border-top:1px solid rgba(0,205,255,0.13);
  font-size:11px;letter-spacing:3.5px;color:rgba(0,148,250,0.58);
}
.mc-bsep{color:rgba(0,205,255,0.25);}

/* Main content */
.mc-body{
  position:relative;z-index:2;
  display:flex;flex-direction:column;align-items:center;
  gap:clamp(14px,2vh,32px);
  width:100%;max-width:1280px;padding:0 40px;
}

/* Brand header */
.mc-header{display:flex;align-items:center;gap:24px;}
.mc-bracket{
  font-size:clamp(40px,5.5vw,78px);font-weight:100;line-height:1;
  color:rgba(0,205,255,0.50);
  text-shadow:0 0 20px rgba(0,195,255,0.35);
}
.mc-title{text-align:center;}
.mc-product{
  font-size:clamp(30px,4.8vw,68px);
  font-weight:900;letter-spacing:10px;color:#fff;
  text-shadow:0 0 16px rgba(0,215,255,0.55),0 0 45px rgba(0,160,255,0.28);
}
.mc-subtitle{
  margin-top:7px;
  font-size:clamp(9px,1.05vw,13px);letter-spacing:7px;
  color:rgba(0,205,255,0.62);
}

/* Separator rule */
.mc-rule{width:100%;display:flex;align-items:center;gap:16px;}
.mc-rule-line{
  flex:1;height:1px;
  background:linear-gradient(90deg,transparent,rgba(0,205,255,0.52),transparent);
}
.mc-rule-icon{
  color:rgba(0,205,255,0.72);font-size:15px;
  text-shadow:0 0 14px rgba(0,190,255,0.65);
}

/* Timer row */
.mc-timer{
  display:flex;align-items:center;justify-content:center;
  gap:clamp(6px,1.6vw,24px);
}
.mc-unit{display:flex;flex-direction:column;align-items:center;gap:11px;}

/* Number panel */
.mc-panel{
  position:relative;
  width:clamp(108px,12.5vw,172px);height:clamp(78px,9.5vh,118px);
  background:rgba(0,10,26,0.88);
  border:1px solid rgba(0,195,255,0.20);
  display:grid;place-items:center;
  box-shadow:inset 0 0 28px rgba(0,30,70,0.40),0 0 16px rgba(0,185,255,0.06);
}
/* Top-left corner bracket */
.mc-panel::before{
  content:"";position:absolute;top:-1px;left:-1px;
  width:13px;height:13px;
  border-top:2px solid rgba(0,205,255,0.72);
  border-left:2px solid rgba(0,205,255,0.72);
}
/* Bottom-right corner bracket */
.mc-panel::after{
  content:"";position:absolute;bottom:-1px;right:-1px;
  width:13px;height:13px;
  border-bottom:2px solid rgba(0,205,255,0.72);
  border-right:2px solid rgba(0,205,255,0.72);
}
/* Bottom glow bar */
.mc-pbar{
  position:absolute;bottom:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,transparent,rgba(0,205,255,0.70),transparent);
  box-shadow:0 0 8px rgba(0,195,255,0.55);
}
.mc-num{
  font-size:clamp(44px,6.8vw,92px);font-weight:800;letter-spacing:4px;
  color:#fff;line-height:1;font-variant-numeric:tabular-nums;
  text-shadow:0 0 10px rgba(0,215,255,0.70),0 0 28px rgba(0,160,255,0.42);
}
.mc-num.tick{animation:numTick 0.18s ease;}
@keyframes numTick{
  0%  {transform:scaleY(1);opacity:1;}
  40% {transform:scaleY(0.05);opacity:0.3;}
  100%{transform:scaleY(1);opacity:1;}
}
.mc-label{
  font-size:clamp(9px,0.95vw,12px);letter-spacing:4.5px;
  color:rgba(0,170,255,0.72);font-weight:600;
}

/* Colon separator */
.mc-sep{
  font-size:clamp(30px,4.2vw,58px);font-weight:900;
  color:rgba(0,200,255,0.42);margin-bottom:22px;
  text-shadow:0 0 12px rgba(0,185,255,0.45);
  animation:colonBlink 1s step-end infinite;
}
@keyframes colonBlink{0%,49%{opacity:1;}50%,100%{opacity:0.15;}}

/* Date / footer line */
.mc-date{
  font-size:clamp(10px,1.2vw,15px);letter-spacing:5px;
  color:rgba(0,148,250,0.62);
  display:flex;align-items:center;gap:20px;
}
.mc-dsep{color:rgba(0,205,255,0.22);}
.mc-date em{font-style:normal;color:rgba(0,215,255,0.88);}


/* ── FINAL.MP4 background inside timer ── */
#final-bg{
  position:absolute;inset:0;width:100%;height:100%;
  object-fit:cover;z-index:0;opacity:0.55;pointer-events:none;
}

/* ── DAYS PHASE ── */
#l-days{background:#00020c;z-index:10;overflow:hidden;}
#launch-img{
  position:absolute;inset:0;width:100%;height:100%;
  object-fit:cover;opacity:0.62;
}
.days-vignette{
  position:absolute;inset:0;
  background:radial-gradient(ellipse at center,transparent 30%,rgba(0,0,10,0.72) 100%);
  z-index:1;pointer-events:none;
}
.days-gradient{
  position:absolute;inset:0;
  background:linear-gradient(180deg,rgba(0,2,14,0.55) 0%,transparent 40%,transparent 60%,rgba(0,2,14,0.70) 100%);
  z-index:1;pointer-events:none;
}
#days-overlay{
  position:absolute;inset:0;z-index:2;
  display:flex;flex-direction:column;align-items:center;justify-content:center;
  gap:clamp(8px,1.8vh,22px);
}
.days-topbar{
  position:absolute;top:0;left:0;right:0;
  display:flex;justify-content:space-between;align-items:center;
  padding:10px 32px;
  border-bottom:1px solid rgba(0,205,255,0.13);
  font-size:11px;letter-spacing:3.5px;color:rgba(0,175,255,0.68);
}
.days-botbar{
  position:absolute;bottom:0;left:0;right:0;
  display:flex;justify-content:center;align-items:center;gap:20px;
  padding:10px 32px;
  border-top:1px solid rgba(0,205,255,0.13);
  font-size:11px;letter-spacing:3.5px;color:rgba(0,148,250,0.58);
}
.days-mission-label{
  font-size:clamp(9px,1.0vw,13px);letter-spacing:7px;
  color:rgba(0,195,255,0.55);margin-bottom:4px;
}
.days-bracket-row{display:flex;align-items:center;gap:18px;}
.days-bracket{
  font-size:clamp(28px,3.8vw,54px);font-weight:100;
  color:rgba(0,205,255,0.45);text-shadow:0 0 18px rgba(0,195,255,0.30);
}
#days-num-panel{
  position:relative;
  display:flex;flex-direction:column;align-items:center;gap:10px;
  padding:20px 48px;
  border:1px solid rgba(0,195,255,0.18);
  background:rgba(0,8,22,0.60);
  box-shadow:inset 0 0 40px rgba(0,30,70,0.50),0 0 30px rgba(0,185,255,0.08);
}
#days-num-panel::before{
  content:"";position:absolute;top:-1px;left:-1px;width:16px;height:16px;
  border-top:2px solid rgba(0,205,255,0.75);border-left:2px solid rgba(0,205,255,0.75);
}
#days-num-panel::after{
  content:"";position:absolute;bottom:-1px;right:-1px;width:16px;height:16px;
  border-bottom:2px solid rgba(0,205,255,0.75);border-right:2px solid rgba(0,205,255,0.75);
}
#ddays{
  font-size:clamp(100px,16vw,210px);font-weight:900;
  line-height:1;letter-spacing:-4px;
  color:#fff;font-variant-numeric:tabular-nums;
  text-shadow:0 0 20px rgba(0,215,255,0.80),0 0 60px rgba(0,160,255,0.38);
}
.days-unit-label{
  font-size:clamp(14px,2.2vw,32px);letter-spacing:10px;font-weight:700;
  color:rgba(0,215,255,0.85);
  text-shadow:0 0 14px rgba(0,195,255,0.55);
}
.days-pbar{
  width:100%;height:2px;
  background:linear-gradient(90deg,transparent,rgba(0,205,255,0.70),transparent);
  box-shadow:0 0 8px rgba(0,195,255,0.55);
}
.days-date-line{
  font-size:clamp(9px,1.1vw,14px);letter-spacing:5px;
  color:rgba(0,148,250,0.65);margin-top:4px;
}
.days-date-line em{font-style:normal;color:rgba(0,215,255,0.90);}


#fs-btn{position:fixed;bottom:24px;right:24px;z-index:200;padding:11px 18px;font-size:14px;font-weight:700;color:#000;background:cyan;border:none;border-radius:10px;cursor:pointer;box-shadow:0 0 18px rgba(0,255,255,0.75);font-family:Orbitron,sans-serif;}
#fs-btn:hover{background:#00e5e5;}

@media(prefers-reduced-motion:reduce){
  #l-timer::before,#l-timer::after,
  .mc-dot,.mc-sep,.mc-num.tick{animation:none !important;opacity:1;}
}
</style>
</head>
<body>

<!-- TIMER (MISSION CONTROL) -->
<div class="layer" id="l-timer">

  <video id="final-bg" muted loop playsinline>
    <source src="data:video/mp4;base64,__FINAL_B64__" type="video/mp4">
  </video>

  <div class="mc-topbar">
    <div class="mc-topbar-item"><div class="mc-dot"></div>SYSTEM NOMINAL</div>
    <div class="mc-topbar-item">LAUNCH SEQUENCE: ACTIVE</div>
    <div class="mc-topbar-item"><div class="mc-dot slow"></div>TELEMETRY LIVE</div>
  </div>

  <div class="mc-body">

    <div class="mc-header">
      <span class="mc-bracket">⟦</span>
      <div class="mc-title">
        <div class="mc-product">MIZZO ORION</div>
        <div class="mc-subtitle">PRODUCT LAUNCH COUNTDOWN</div>
      </div>
      <span class="mc-bracket">⟧</span>
    </div>

    <div class="mc-rule">
      <div class="mc-rule-line"></div>
      <span class="mc-rule-icon">◈</span>
      <div class="mc-rule-line"></div>
    </div>

    <div class="mc-timer">
      <div class="mc-unit">
        <div class="mc-panel"><div class="mc-pbar"></div>
          <div class="mc-num" id="months">00</div></div>
        <div class="mc-label">MONTHS</div>
      </div>
      <div class="mc-sep">:</div>
      <div class="mc-unit">
        <div class="mc-panel"><div class="mc-pbar"></div>
          <div class="mc-num" id="days">00</div></div>
        <div class="mc-label">DAYS</div>
      </div>
      <div class="mc-sep">:</div>
      <div class="mc-unit">
        <div class="mc-panel"><div class="mc-pbar"></div>
          <div class="mc-num" id="hours">00</div></div>
        <div class="mc-label">HOURS</div>
      </div>
      <div class="mc-sep">:</div>
      <div class="mc-unit">
        <div class="mc-panel"><div class="mc-pbar"></div>
          <div class="mc-num" id="minutes">00</div></div>
        <div class="mc-label">MINUTES</div>
      </div>
      <div class="mc-sep">:</div>
      <div class="mc-unit">
        <div class="mc-panel"><div class="mc-pbar"></div>
          <div class="mc-num" id="seconds">00</div></div>
        <div class="mc-label">SECONDS</div>
      </div>
    </div>

    <div class="mc-rule">
      <div class="mc-rule-line"></div>
      <span class="mc-rule-icon">◈</span>
      <div class="mc-rule-line"></div>
    </div>

    <div class="mc-date">
      <span>T—MINUS</span>
      <span class="mc-dsep">│</span>
      <span>LAUNCH: <em>JUNE 13, 2026</em></span>
      <span class="mc-dsep">│</span>
      <span>MISSION MO—001</span>
    </div>

  </div>

  <div class="mc-botbar">
    <span>◈</span>
    <span>ALL SYSTEMS GO</span>
    <span class="mc-bsep">│</span>
    <span>COUNTDOWN NOMINAL</span>
    <span class="mc-bsep">│</span>
    <span>◈</span>
  </div>


</div>

<!-- DAYS COUNTDOWN PHASE -->
<div class="layer hidden" id="l-days">
  <img id="launch-img" src="data:image/jpeg;base64,__IMG_B64__" alt=""/>
  <div class="days-vignette"></div>
  <div class="days-gradient"></div>
  <div id="days-overlay">
    <div class="days-topbar">
      <span>◈ MISSION MO-001</span>
      <span>LAUNCH SEQUENCE: ACTIVE</span>
      <span>RANGE: NOMINAL ◈</span>
    </div>
    <div class="days-mission-label">MIZZO ORION — PRODUCT LAUNCH</div>
    <div class="days-bracket-row">
      <span class="days-bracket">⟦</span>
      <div id="days-num-panel">
        <div class="days-pbar"></div>
        <div id="ddays">00</div>
        <div class="days-unit-label">DAYS TO LAUNCH</div>
        <div class="days-date-line">TARGET: <em>JUNE 13, 2026</em></div>
      </div>
      <span class="days-bracket">⟧</span>
    </div>
    <div class="days-botbar">
      <span>◈</span>
      <span>COUNTDOWN IN PROGRESS</span>
      <span>│</span>
      <span>ALL SYSTEMS GO</span>
      <span>◈</span>
    </div>
  </div>
</div>


<button id="fs-btn">&#x26F6; Fullscreen</button>

<script>
(function(){

const LAUNCH = new Date("__LAUNCH_DATE__");


// ── COUNTDOWN ────────────────────────────────────────────────────────────────
function getTimeLeft(){
  const d=LAUNCH-new Date(); if(d<=0) return null;
  let s=Math.floor(d/1000),m=Math.floor(s/60),h=Math.floor(m/60),dy=Math.floor(h/24);
  return{months:Math.floor(dy/30),days:dy%30,hours:h%24,minutes:m%60,seconds:s%60};
}
function updateTimerDisplay(){
  const t=getTimeLeft(); if(!t) return;
  ['months','days','hours','minutes','seconds'].forEach(k=>{
    const el=document.getElementById(k); if(!el) return;
    const v=String(t[k]).padStart(2,'0');
    if(el.innerText!==v){
      el.classList.remove('tick');
      void el.offsetWidth;
      el.classList.add('tick');
      el.innerText=v;
    }
  });
}

// ── PHASE MACHINE ─────────────────────────────────────────────────────────────
const lTimer  = document.getElementById('l-timer');
const lDays   = document.getElementById('l-days');
const finalBg = document.getElementById('final-bg');

const PH = {DAYS:0, TIMER:1};
let phase = PH.DAYS;
let phaseStart = 0;
const PHASE_DURATION = 30000;

function updateDaysDisplay(){
  const d = LAUNCH - new Date();
  const days = d > 0 ? Math.ceil(d / (1000*60*60*24)) : 0;
  const el = document.getElementById('ddays');
  if(el) el.innerText = String(days);
}

function go(p){
  phase = p;
  lTimer.classList.toggle('hidden', p !== PH.TIMER);
  lDays.classList.toggle('hidden',  p !== PH.DAYS);
  phaseStart = performance.now();
  if(p === PH.TIMER){
    finalBg.currentTime = 0;
    finalBg.play().catch(()=>{});
  } else {
    finalBg.pause();
    updateDaysDisplay();
  }
}

// ── MAIN LOOP ─────────────────────────────────────────────────────────────────
function loop(){
  requestAnimationFrame(loop);
  if(phase === PH.TIMER) updateTimerDisplay();
  if(performance.now() - phaseStart >= PHASE_DURATION)
    go(phase === PH.TIMER ? PH.DAYS : PH.TIMER);
}
requestAnimationFrame(loop);

go(PH.DAYS);

// ── FULLSCREEN ────────────────────────────────────────────────────────────────
const fsBtn=document.getElementById('fs-btn');
fsBtn.addEventListener('click',()=>{
  const el=document.documentElement;
  if(el.requestFullscreen) el.requestFullscreen();
  else if(el.webkitRequestFullscreen) el.webkitRequestFullscreen();
});
function onFsChange(){
  fsBtn.style.display=(document.fullscreenElement||document.webkitFullscreenElement)?'none':'block';
}
document.addEventListener('fullscreenchange',onFsChange);
document.addEventListener('webkitfullscreenchange',onFsChange);

})();
</script>
</body>
</html>
"""

HTML = (HTML
    .replace("__IMG_B64__",     img_b64)
    .replace("__FINAL_B64__",   final_b64)
    .replace("__LAUNCH_DATE__", LAUNCH_DATE))

st.components.v1.html(HTML, height=900, scrolling=False)
