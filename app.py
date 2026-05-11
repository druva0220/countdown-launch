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

/* ── ROBOTIC ARMS — rise from bottom, cover screen ── */
.mc-arm{
  position:absolute;bottom:0;
  width:clamp(200px,22vw,360px);
  height:clamp(420px,62vh,700px);
  overflow:visible;pointer-events:none;z-index:1;
}
.mc-arm-l{left:0; transform-origin:50% 100%;transform:rotate(18deg);}
.mc-arm-r{right:0;transform-origin:50% 100%;transform:scaleX(-1) rotate(18deg);}
.arm-seg{transform-box:fill-box;transform-origin:50% 100%;}
.arm-s1{animation:aS1  9.4s ease-in-out infinite;}
.arm-s2{animation:aS2  7.6s ease-in-out infinite;}
.arm-s3{animation:aS3  5.9s ease-in-out infinite;}
.arm-s4{animation:aS4  4.4s ease-in-out infinite;}
.arm-s5{animation:aS5  3.3s ease-in-out infinite;}
.arm-s6{animation:aS6  2.5s ease-in-out infinite;}
.arm-s7{animation:aS7  1.9s ease-in-out infinite;}
.mc-arm-r .arm-s1{animation-delay:1.9s;}
.mc-arm-r .arm-s2{animation-delay:3.5s;}
.mc-arm-r .arm-s3{animation-delay:0.8s;}
.mc-arm-r .arm-s4{animation-delay:2.3s;}
.mc-arm-r .arm-s5{animation-delay:0.5s;}
.mc-arm-r .arm-s6{animation-delay:1.4s;}
.mc-arm-r .arm-s7{animation-delay:2.8s;}
@keyframes aS1{0%,100%{transform:rotate(-7deg)}  44%{transform:rotate(5deg)}  72%{transform:rotate(1deg)}}
@keyframes aS2{0%,100%{transform:rotate(-5deg)}  36%{transform:rotate(10deg)} 66%{transform:rotate(3deg)}}
@keyframes aS3{0%,100%{transform:rotate(10deg)}  28%{transform:rotate(-12deg)} 58%{transform:rotate(14deg)} 84%{transform:rotate(3deg)}}
@keyframes aS4{0%,100%{transform:rotate(-17deg)} 24%{transform:rotate(20deg)} 54%{transform:rotate(-8deg)}  80%{transform:rotate(18deg)}}
@keyframes aS5{0%,100%{transform:rotate(-25deg)} 19%{transform:rotate(29deg)} 44%{transform:rotate(-10deg)} 69%{transform:rotate(27deg)} 90%{transform:rotate(-20deg)}}
@keyframes aS6{0%,100%{transform:rotate(-36deg)} 14%{transform:rotate(20deg)} 39%{transform:rotate(42deg)} 64%{transform:rotate(-16deg)} 84%{transform:rotate(38deg)}}
@keyframes aS7{0%,100%{transform:rotate(-48deg)} 11%{transform:rotate(56deg)} 34%{transform:rotate(-28deg)} 57%{transform:rotate(52deg)} 79%{transform:rotate(-38deg)} 94%{transform:rotate(50deg)}}

/* ── SIDE ARMS — wall-mounted, extend inward ── */
.mc-arm-side{
  position:absolute;
  width:clamp(180px,22vw,290px);
  height:clamp(70px,13vh,120px);
  overflow:visible;pointer-events:none;z-index:1;
}
.mc-arm-side-l{ left:0; top:26%; }
.mc-arm-side-r{ right:0; top:60%; transform:scaleX(-1); }
.side-seg{ transform-box:fill-box; transform-origin:0% 50%; }
.ss1{animation:ssA1  8.6s ease-in-out infinite;}
.ss2{animation:ssA2  6.3s ease-in-out infinite;}
.ss3{animation:ssA3  4.5s ease-in-out infinite;}
.ss4{animation:ssA4  3.0s ease-in-out infinite;}
.mc-arm-side-r .ss1{animation-delay:2.2s;}
.mc-arm-side-r .ss2{animation-delay:1.4s;}
.mc-arm-side-r .ss3{animation-delay:3.6s;}
.mc-arm-side-r .ss4{animation-delay:0.9s;}
@keyframes ssA1{0%,100%{transform:rotate(-14deg)} 42%{transform:rotate(12deg)} 72%{transform:rotate(3deg)}}
@keyframes ssA2{0%,100%{transform:rotate(-20deg)} 34%{transform:rotate(24deg)} 64%{transform:rotate(-8deg)}}
@keyframes ssA3{0%,100%{transform:rotate(-32deg)} 26%{transform:rotate(36deg)} 54%{transform:rotate(-16deg)} 80%{transform:rotate(28deg)}}
@keyframes ssA4{0%,100%{transform:rotate(-46deg)} 20%{transform:rotate(52deg)} 44%{transform:rotate(-26deg)} 70%{transform:rotate(46deg)} 90%{transform:rotate(-36deg)}}

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

  <!-- LEFT ARM — needle driver, base at bottom -->
  <svg class="mc-arm mc-arm-l" viewBox="0 0 240 880" overflow="visible" xmlns="http://www.w3.org/2000/svg">
    <!-- Floor mount bracket -->
    <rect x="74" y="838" width="92" height="40" rx="6" fill="#000c20" stroke="rgba(0,195,255,0.75)" stroke-width="2.2"/>
    <rect x="81" y="845" width="78" height="26" rx="4" fill="rgba(0,4,16,0.90)" stroke="rgba(0,195,255,0.30)" stroke-width="1"/>
    <circle cx="100" cy="858" r="4"   fill="rgba(0,195,255,0.58)"/>
    <circle cx="120" cy="858" r="4"   fill="rgba(0,195,255,0.58)"/>
    <circle cx="140" cy="858" r="4"   fill="rgba(0,195,255,0.58)"/>
    <g transform="translate(120,860)">
      <!-- S1: w=92 h=162 -->
      <g class="arm-seg arm-s1">
        <rect x="-46" y="-162" width="92" height="162" rx="7" fill="#000c20" stroke="rgba(0,195,255,0.48)" stroke-width="2.2"/>
        <rect x="-46" y="-162" width="12" height="162" rx="6" fill="rgba(0,185,255,0.11)"/>
        <rect x="34"  y="-162" width="12" height="162" rx="6" fill="rgba(0,0,20,0.32)"/>
        <rect x="-34" y="-152" width="68" height="142" rx="4" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.23)" stroke-width="1.1"/>
        <rect x="-22" y="-148" width="44" height="134" rx="2" fill="rgba(0,195,255,0.04)"/>
        <line x1="-32" y1="-122" x2="32" y2="-122" stroke="rgba(0,195,255,0.26)" stroke-width="1.4"/>
        <line x1="-32" y1="-81"  x2="32" y2="-81"  stroke="rgba(0,195,255,0.26)" stroke-width="1.4"/>
        <line x1="-32" y1="-41"  x2="32" y2="-41"  stroke="rgba(0,195,255,0.26)" stroke-width="1.4"/>
        <circle cx="-29" cy="-122" r="3" fill="rgba(0,195,255,0.45)"/>
        <circle cx="29"  cy="-122" r="3" fill="rgba(0,195,255,0.45)"/>
        <circle cx="-29" cy="-81"  r="3" fill="rgba(0,195,255,0.45)"/>
        <circle cx="29"  cy="-81"  r="3" fill="rgba(0,195,255,0.45)"/>
        <circle cx="-29" cy="-41"  r="3" fill="rgba(0,195,255,0.45)"/>
        <circle cx="29"  cy="-41"  r="3" fill="rgba(0,195,255,0.45)"/>
        <rect x="-51" y="-167" width="102" height="11" rx="3.5" fill="#000d22" stroke="rgba(0,195,255,0.60)" stroke-width="1.8"/>
        <g transform="translate(0,-162)">
          <!-- S2: w=48 h=134 -->
          <g class="arm-seg arm-s2">
            <rect x="-38" y="-134" width="76" height="134" rx="5.5" fill="#000c20" stroke="rgba(0,195,255,0.43)" stroke-width="1.8"/>
            <rect x="-38" y="-134" width="13" height="134" rx="4.5" fill="rgba(0,185,255,0.09)"/>
            <rect x="25"  y="-134" width="13" height="134" rx="4.5" fill="rgba(0,0,20,0.28)"/>
            <rect x="-24" y="-125" width="48" height="116" rx="3" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.20)" stroke-width="0.9"/>
            <rect x="-14" y="-121" width="28" height="108" rx="2" fill="rgba(0,195,255,0.04)"/>
            <line x1="-22" y1="-100" x2="22" y2="-100" stroke="rgba(0,195,255,0.22)" stroke-width="1.1"/>
            <line x1="-22" y1="-67"  x2="22" y2="-67"  stroke="rgba(0,195,255,0.22)" stroke-width="1.1"/>
            <line x1="-22" y1="-34"  x2="22" y2="-34"  stroke="rgba(0,195,255,0.22)" stroke-width="1.1"/>
            <circle cx="-19" cy="-100" r="2.2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="19"  cy="-100" r="2.2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="-19" cy="-67"  r="2.2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="19"  cy="-67"  r="2.2" fill="rgba(0,195,255,0.38)"/>
            <rect x="-41" y="-139" width="82" height="9" rx="2.5" fill="#000d22" stroke="rgba(0,195,255,0.55)" stroke-width="1.5"/>
            <g transform="translate(0,-134)">
              <!-- S3: w=40 h=112 -->
              <g class="arm-seg arm-s3">
                <rect x="-32" y="-112" width="64" height="112" rx="5" fill="#000c20" stroke="rgba(0,195,255,0.40)" stroke-width="1.7"/>
                <rect x="-32" y="-112" width="11" height="112" rx="4" fill="rgba(0,185,255,0.09)"/>
                <rect x="21"  y="-112" width="11" height="112" rx="4" fill="rgba(0,0,20,0.27)"/>
                <rect x="-21" y="-104" width="42" height="96" rx="2.5" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.18)" stroke-width="0.9"/>
                <rect x="-11" y="-100" width="22" height="88" rx="2" fill="rgba(0,195,255,0.04)"/>
                <line x1="-19" y1="-84" x2="19" y2="-84" stroke="rgba(0,195,255,0.21)" stroke-width="1"/>
                <line x1="-19" y1="-56" x2="19" y2="-56" stroke="rgba(0,195,255,0.21)" stroke-width="1"/>
                <line x1="-19" y1="-28" x2="19" y2="-28" stroke="rgba(0,195,255,0.21)" stroke-width="1"/>
                <circle cx="-16" cy="-84" r="2" fill="rgba(0,195,255,0.35)"/>
                <circle cx="16"  cy="-84" r="2" fill="rgba(0,195,255,0.35)"/>
                <circle cx="-16" cy="-56" r="2" fill="rgba(0,195,255,0.35)"/>
                <circle cx="16"  cy="-56" r="2" fill="rgba(0,195,255,0.35)"/>
                <rect x="-37" y="-117" width="74" height="9" rx="2.5" fill="#000d22" stroke="rgba(0,195,255,0.52)" stroke-width="1.4"/>
                <g transform="translate(0,-112)">
                  <!-- S4: w=32 h=92 -->
                  <g class="arm-seg arm-s4">
                    <rect x="-26" y="-92" width="52" height="92" rx="4.5" fill="#000c20" stroke="rgba(0,195,255,0.38)" stroke-width="1.6"/>
                    <rect x="-26" y="-92" width="10" height="92" rx="3.5" fill="rgba(0,185,255,0.08)"/>
                    <rect x="16"  y="-92" width="10" height="92" rx="3.5" fill="rgba(0,0,20,0.26)"/>
                    <rect x="-16" y="-85" width="32" height="77" rx="2.5" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.17)" stroke-width="0.8"/>
                    <line x1="-15" y1="-69" x2="15" y2="-69" stroke="rgba(0,195,255,0.20)" stroke-width="1"/>
                    <line x1="-15" y1="-46" x2="15" y2="-46" stroke="rgba(0,195,255,0.20)" stroke-width="1"/>
                    <line x1="-15" y1="-23" x2="15" y2="-23" stroke="rgba(0,195,255,0.20)" stroke-width="1"/>
                    <circle cx="-11" cy="-69" r="1.8" fill="rgba(0,195,255,0.32)"/>
                    <circle cx="11"  cy="-69" r="1.8" fill="rgba(0,195,255,0.32)"/>
                    <circle cx="-11" cy="-46" r="1.8" fill="rgba(0,195,255,0.32)"/>
                    <circle cx="11"  cy="-46" r="1.8" fill="rgba(0,195,255,0.32)"/>
                    <rect x="-29" y="-97" width="58" height="8" rx="2" fill="#000d22" stroke="rgba(0,195,255,0.50)" stroke-width="1.4"/>
                    <g transform="translate(0,-92)">
                      <!-- S5: w=26 h=74 -->
                      <g class="arm-seg arm-s5">
                        <rect x="-21" y="-74" width="42" height="74" rx="4" fill="#000c20" stroke="rgba(0,195,255,0.36)" stroke-width="1.5"/>
                        <rect x="-21" y="-74" width="8"  height="74" rx="3" fill="rgba(0,185,255,0.08)"/>
                        <rect x="13"  y="-74" width="8"  height="74" rx="3" fill="rgba(0,0,20,0.25)"/>
                        <rect x="-13" y="-68" width="26" height="60" rx="2" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.16)" stroke-width="0.8"/>
                        <line x1="-11" y1="-55" x2="11" y2="-55" stroke="rgba(0,195,255,0.19)" stroke-width="0.9"/>
                        <line x1="-11" y1="-37" x2="11" y2="-37" stroke="rgba(0,195,255,0.19)" stroke-width="0.9"/>
                        <line x1="-11" y1="-19" x2="11" y2="-19" stroke="rgba(0,195,255,0.19)" stroke-width="0.9"/>
                        <circle cx="-9"  cy="-55" r="1.5" fill="rgba(0,195,255,0.30)"/>
                        <circle cx="9"   cy="-55" r="1.5" fill="rgba(0,195,255,0.30)"/>
                        <rect x="-24" y="-79" width="48" height="8" rx="2" fill="#000d22" stroke="rgba(0,195,255,0.48)" stroke-width="1.3"/>
                        <g transform="translate(0,-74)">
                          <!-- S6: w=21 h=57 -->
                          <g class="arm-seg arm-s6">
                            <rect x="-17" y="-57" width="34" height="57" rx="3.5" fill="#000c20" stroke="rgba(0,195,255,0.34)" stroke-width="1.4"/>
                            <rect x="-17" y="-57" width="7"  height="57" rx="3"   fill="rgba(0,185,255,0.08)"/>
                            <rect x="10"  y="-57" width="7"  height="57" rx="3"   fill="rgba(0,0,20,0.24)"/>
                            <rect x="-10" y="-51" width="20" height="43" rx="2"   fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.15)" stroke-width="0.8"/>
                            <line x1="-8" y1="-42" x2="8" y2="-42" stroke="rgba(0,195,255,0.18)" stroke-width="0.9"/>
                            <line x1="-8" y1="-21" x2="8" y2="-21" stroke="rgba(0,195,255,0.18)" stroke-width="0.9"/>
                            <rect x="-20" y="-62" width="40" height="8" rx="2" fill="#000d22" stroke="rgba(0,195,255,0.46)" stroke-width="1.2"/>
                            <g transform="translate(0,-57)">
                              <!-- S7 — needle driver -->
                              <g class="arm-seg arm-s7">
                                <rect x="-18" y="-36" width="36" height="36" rx="4" fill="#000c20" stroke="rgba(0,195,255,0.60)" stroke-width="1.6"/>
                                <rect x="-18" y="-36" width="6"  height="36" rx="3" fill="rgba(0,185,255,0.12)"/>
                                <rect x="12"  y="-36" width="6"  height="36" rx="3" fill="rgba(0,0,20,0.28)"/>
                                <line x1="-12" y1="-28" x2="12" y2="-28" stroke="rgba(0,195,255,0.38)" stroke-width="1"/>
                                <line x1="-12" y1="-20" x2="12" y2="-20" stroke="rgba(0,195,255,0.38)" stroke-width="1"/>
                                <line x1="-12" y1="-12" x2="12" y2="-12" stroke="rgba(0,195,255,0.38)" stroke-width="1"/>
                                <path d="M0,-36 C-28,-60 -26,-90 -7,-100" fill="none" stroke="rgba(190,245,255,0.97)" stroke-width="2.8" stroke-linecap="round"/>
                                <circle cx="-7" cy="-100" r="4" fill="rgba(190,245,255,0.97)"/>
                                <circle cx="-7" cy="-100" r="7" fill="none" stroke="rgba(190,245,255,0.35)" stroke-width="1"/>
                                <path d="M0,-36 C17,-28 19,-14 14,-4 C10,6 17,13 14,22" fill="none" stroke="rgba(0,215,255,0.60)" stroke-width="1.3" stroke-dasharray="5,3"/>
                              </g>
                              <circle r="13"  fill="#000c1e" stroke="rgba(0,195,255,0.68)" stroke-width="1.6"/>
                              <circle r="8"   fill="none"   stroke="rgba(0,195,255,0.35)" stroke-width="1.2"/>
                              <circle r="4"   fill="rgba(0,195,255,0.42)"/>
                            </g>
                          </g>
                          <circle r="17"  fill="#000c1e" stroke="rgba(0,195,255,0.72)" stroke-width="1.8"/>
                          <circle r="11"  fill="none"   stroke="rgba(0,195,255,0.32)" stroke-width="1.3"/>
                          <circle r="5"   fill="rgba(0,195,255,0.38)"/>
                          <line x1="-5" y1="0" x2="5" y2="0" stroke="rgba(0,215,255,0.55)" stroke-width="1"/>
                          <line x1="0" y1="-5" x2="0" y2="5" stroke="rgba(0,215,255,0.55)" stroke-width="1"/>
                        </g>
                      </g>
                      <circle r="22"  fill="#000c1e" stroke="rgba(0,195,255,0.74)" stroke-width="2"/>
                      <circle r="14"  fill="none"   stroke="rgba(0,195,255,0.30)" stroke-width="1.4"/>
                      <circle r="7"   fill="rgba(0,195,255,0.36)"/>
                      <line x1="-7" y1="0" x2="7" y2="0" stroke="rgba(0,215,255,0.55)" stroke-width="1.1"/>
                      <line x1="0" y1="-7" x2="0" y2="7" stroke="rgba(0,215,255,0.55)" stroke-width="1.1"/>
                    </g>
                  </g>
                  <circle r="28"  fill="#000c1e" stroke="rgba(0,195,255,0.76)" stroke-width="2.1"/>
                  <circle r="18"  fill="none"   stroke="rgba(0,195,255,0.29)" stroke-width="1.5"/>
                  <circle r="8"   fill="rgba(0,195,255,0.34)"/>
                  <line x1="-8" y1="0" x2="8" y2="0" stroke="rgba(0,215,255,0.54)" stroke-width="1.2"/>
                  <line x1="0" y1="-8" x2="0" y2="8" stroke="rgba(0,215,255,0.54)" stroke-width="1.2"/>
                </g>
              </g>
              <circle r="34"  fill="#000c1e" stroke="rgba(0,195,255,0.78)" stroke-width="2.2"/>
              <circle r="21"  fill="none"   stroke="rgba(0,195,255,0.28)" stroke-width="1.5"/>
              <circle r="10"  fill="rgba(0,195,255,0.32)"/>
              <line x1="-10" y1="0" x2="10" y2="0" stroke="rgba(0,215,255,0.53)" stroke-width="1.3"/>
              <line x1="0" y1="-10" x2="0" y2="10" stroke="rgba(0,215,255,0.53)" stroke-width="1.3"/>
            </g>
          </g>
          <circle r="40"  fill="#000c1e" stroke="rgba(0,195,255,0.80)" stroke-width="2.4"/>
          <circle r="25"  fill="none"   stroke="rgba(0,195,255,0.27)" stroke-width="1.6"/>
          <circle r="12"  fill="rgba(0,195,255,0.30)"/>
          <line x1="-12" y1="0" x2="12" y2="0" stroke="rgba(0,215,255,0.52)" stroke-width="1.4"/>
          <line x1="0" y1="-12" x2="0" y2="12" stroke="rgba(0,215,255,0.52)" stroke-width="1.4"/>
        </g>
      </g>
      <circle r="48"  fill="#000c1e" stroke="rgba(0,195,255,0.84)" stroke-width="2.6"/>
      <circle r="38"  fill="none"   stroke="rgba(0,195,255,0.26)" stroke-width="1.8"/>
      <circle r="28"  fill="#000814" stroke="rgba(0,195,255,0.42)" stroke-width="1.4"/>
      <circle r="8"   fill="rgba(0,195,255,0.36)"/>
      <line x1="-8" y1="0" x2="8" y2="0" stroke="rgba(0,215,255,0.60)" stroke-width="1.5"/>
      <line x1="0" y1="-8" x2="0" y2="8" stroke="rgba(0,215,255,0.60)" stroke-width="1.5"/>
      <circle cx="38"  cy="0"   r="3" fill="rgba(0,195,255,0.38)"/>
      <circle cx="-38" cy="0"   r="3" fill="rgba(0,195,255,0.38)"/>
      <circle cx="0"   cy="-38" r="3" fill="rgba(0,195,255,0.38)"/>
      <circle cx="0"   cy="38"  r="3" fill="rgba(0,195,255,0.38)"/>
    </g>
  </svg>

  <!-- RIGHT ARM — tissue forceps, base at bottom (mirrored) -->
  <svg class="mc-arm mc-arm-r" viewBox="0 0 240 880" overflow="visible" xmlns="http://www.w3.org/2000/svg">
    <rect x="74" y="838" width="92" height="40" rx="6" fill="#000c20" stroke="rgba(0,195,255,0.72)" stroke-width="2"/>
    <rect x="81" y="845" width="78" height="26" rx="4" fill="rgba(0,4,16,0.90)" stroke="rgba(0,195,255,0.28)" stroke-width="1"/>
    <circle cx="100" cy="858" r="4"   fill="rgba(0,195,255,0.55)"/>
    <circle cx="120" cy="858" r="4"   fill="rgba(0,195,255,0.55)"/>
    <circle cx="140" cy="858" r="4"   fill="rgba(0,195,255,0.55)"/>
    <g transform="translate(120,860)">
      <g class="arm-seg arm-s1">
        <rect x="-46" y="-162" width="92" height="162" rx="6" fill="#000c20" stroke="rgba(0,195,255,0.46)" stroke-width="2"/>
        <rect x="-46" y="-162" width="12" height="162" rx="5" fill="rgba(0,185,255,0.10)"/>
        <rect x="34"  y="-162" width="12" height="162" rx="5" fill="rgba(0,0,20,0.30)"/>
        <rect x="-34" y="-152" width="68" height="142" rx="3" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.22)" stroke-width="1"/>
        <rect x="-22" y="-148" width="44" height="134" rx="2" fill="rgba(0,195,255,0.04)"/>
        <line x1="-32" y1="-122" x2="32" y2="-122" stroke="rgba(0,195,255,0.24)" stroke-width="1.2"/>
        <line x1="-32" y1="-81"  x2="32" y2="-81"  stroke="rgba(0,195,255,0.24)" stroke-width="1.2"/>
        <line x1="-32" y1="-41"  x2="32" y2="-41"  stroke="rgba(0,195,255,0.24)" stroke-width="1.2"/>
        <circle cx="-29" cy="-122" r="2.5" fill="rgba(0,195,255,0.42)"/>
        <circle cx="29"  cy="-122" r="2.5" fill="rgba(0,195,255,0.42)"/>
        <circle cx="-29" cy="-81"  r="2.5" fill="rgba(0,195,255,0.42)"/>
        <circle cx="29"  cy="-81"  r="2.5" fill="rgba(0,195,255,0.42)"/>
        <rect x="-51" y="-167" width="102" height="10" rx="3" fill="#000d22" stroke="rgba(0,195,255,0.58)" stroke-width="1.6"/>
        <g transform="translate(0,-162)">
          <g class="arm-seg arm-s2">
            <rect x="-38" y="-134" width="76" height="134" rx="5.5" fill="#000c20" stroke="rgba(0,195,255,0.43)" stroke-width="1.8"/>
            <rect x="-38" y="-134" width="13" height="134" rx="4.5" fill="rgba(0,185,255,0.09)"/>
            <rect x="25"  y="-134" width="13" height="134" rx="4.5" fill="rgba(0,0,20,0.28)"/>
            <rect x="-24" y="-125" width="48" height="116" rx="3" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.20)" stroke-width="0.9"/>
            <rect x="-14" y="-121" width="28" height="108" rx="2" fill="rgba(0,195,255,0.04)"/>
            <line x1="-22" y1="-100" x2="22" y2="-100" stroke="rgba(0,195,255,0.22)" stroke-width="1.1"/>
            <line x1="-22" y1="-67"  x2="22" y2="-67"  stroke="rgba(0,195,255,0.22)" stroke-width="1.1"/>
            <line x1="-22" y1="-34"  x2="22" y2="-34"  stroke="rgba(0,195,255,0.22)" stroke-width="1.1"/>
            <circle cx="-19" cy="-100" r="2.2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="19"  cy="-100" r="2.2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="-19" cy="-67"  r="2.2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="19"  cy="-67"  r="2.2" fill="rgba(0,195,255,0.38)"/>
            <rect x="-41" y="-139" width="82" height="9" rx="2.5" fill="#000d22" stroke="rgba(0,195,255,0.55)" stroke-width="1.5"/>
            <g transform="translate(0,-134)">
              <g class="arm-seg arm-s3">
                <rect x="-32" y="-112" width="64" height="112" rx="5" fill="#000c20" stroke="rgba(0,195,255,0.40)" stroke-width="1.7"/>
                <rect x="-32" y="-112" width="11" height="112" rx="4" fill="rgba(0,185,255,0.09)"/>
                <rect x="21"  y="-112" width="11" height="112" rx="4" fill="rgba(0,0,20,0.27)"/>
                <rect x="-21" y="-104" width="42" height="96" rx="2.5" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.18)" stroke-width="0.9"/>
                <rect x="-11" y="-100" width="22" height="88" rx="2" fill="rgba(0,195,255,0.04)"/>
                <line x1="-19" y1="-84" x2="19" y2="-84" stroke="rgba(0,195,255,0.21)" stroke-width="1"/>
                <line x1="-19" y1="-56" x2="19" y2="-56" stroke="rgba(0,195,255,0.21)" stroke-width="1"/>
                <line x1="-19" y1="-28" x2="19" y2="-28" stroke="rgba(0,195,255,0.21)" stroke-width="1"/>
                <circle cx="-16" cy="-84" r="2" fill="rgba(0,195,255,0.35)"/>
                <circle cx="16"  cy="-84" r="2" fill="rgba(0,195,255,0.35)"/>
                <circle cx="-16" cy="-56" r="2" fill="rgba(0,195,255,0.35)"/>
                <circle cx="16"  cy="-56" r="2" fill="rgba(0,195,255,0.35)"/>
                <rect x="-37" y="-117" width="74" height="9" rx="2.5" fill="#000d22" stroke="rgba(0,195,255,0.52)" stroke-width="1.4"/>
                <g transform="translate(0,-112)">
                  <g class="arm-seg arm-s4">
                    <rect x="-26" y="-92" width="52" height="92" rx="4.5" fill="#000c20" stroke="rgba(0,195,255,0.38)" stroke-width="1.6"/>
                    <rect x="-26" y="-92" width="10" height="92" rx="3.5" fill="rgba(0,185,255,0.08)"/>
                    <rect x="16"  y="-92" width="10" height="92" rx="3.5" fill="rgba(0,0,20,0.26)"/>
                    <rect x="-16" y="-85" width="32" height="77" rx="2.5" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.17)" stroke-width="0.8"/>
                    <line x1="-15" y1="-69" x2="15" y2="-69" stroke="rgba(0,195,255,0.20)" stroke-width="1"/>
                    <line x1="-15" y1="-46" x2="15" y2="-46" stroke="rgba(0,195,255,0.20)" stroke-width="1"/>
                    <line x1="-15" y1="-23" x2="15" y2="-23" stroke="rgba(0,195,255,0.20)" stroke-width="1"/>
                    <circle cx="-11" cy="-69" r="1.8" fill="rgba(0,195,255,0.32)"/>
                    <circle cx="11"  cy="-69" r="1.8" fill="rgba(0,195,255,0.32)"/>
                    <circle cx="-11" cy="-46" r="1.8" fill="rgba(0,195,255,0.32)"/>
                    <circle cx="11"  cy="-46" r="1.8" fill="rgba(0,195,255,0.32)"/>
                    <rect x="-29" y="-97" width="58" height="8" rx="2" fill="#000d22" stroke="rgba(0,195,255,0.50)" stroke-width="1.4"/>
                    <g transform="translate(0,-92)">
                      <g class="arm-seg arm-s5">
                        <rect x="-21" y="-74" width="42" height="74" rx="4" fill="#000c20" stroke="rgba(0,195,255,0.36)" stroke-width="1.5"/>
                        <rect x="-21" y="-74" width="8"  height="74" rx="3" fill="rgba(0,185,255,0.08)"/>
                        <rect x="13"  y="-74" width="8"  height="74" rx="3" fill="rgba(0,0,20,0.25)"/>
                        <rect x="-13" y="-68" width="26" height="60" rx="2" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.16)" stroke-width="0.8"/>
                        <line x1="-11" y1="-55" x2="11" y2="-55" stroke="rgba(0,195,255,0.19)" stroke-width="0.9"/>
                        <line x1="-11" y1="-37" x2="11" y2="-37" stroke="rgba(0,195,255,0.19)" stroke-width="0.9"/>
                        <line x1="-11" y1="-19" x2="11" y2="-19" stroke="rgba(0,195,255,0.19)" stroke-width="0.9"/>
                        <circle cx="-9"  cy="-55" r="1.5" fill="rgba(0,195,255,0.30)"/>
                        <circle cx="9"   cy="-55" r="1.5" fill="rgba(0,195,255,0.30)"/>
                        <rect x="-24" y="-79" width="48" height="8" rx="2" fill="#000d22" stroke="rgba(0,195,255,0.48)" stroke-width="1.3"/>
                        <g transform="translate(0,-74)">
                          <g class="arm-seg arm-s6">
                            <rect x="-17" y="-57" width="34" height="57" rx="3.5" fill="#000c20" stroke="rgba(0,195,255,0.34)" stroke-width="1.4"/>
                            <rect x="-17" y="-57" width="7"  height="57" rx="3"   fill="rgba(0,185,255,0.08)"/>
                            <rect x="10"  y="-57" width="7"  height="57" rx="3"   fill="rgba(0,0,20,0.24)"/>
                            <rect x="-10" y="-51" width="20" height="43" rx="2"   fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.15)" stroke-width="0.8"/>
                            <line x1="-8" y1="-42" x2="8" y2="-42" stroke="rgba(0,195,255,0.18)" stroke-width="0.9"/>
                            <line x1="-8" y1="-21" x2="8" y2="-21" stroke="rgba(0,195,255,0.18)" stroke-width="0.9"/>
                            <rect x="-20" y="-62" width="40" height="8" rx="2" fill="#000d22" stroke="rgba(0,195,255,0.46)" stroke-width="1.2"/>
                            <g transform="translate(0,-57)">
                              <!-- S7 — tissue forceps -->
                              <g class="arm-seg arm-s7">
                                <rect x="-18" y="-36" width="36" height="36" rx="4" fill="#000c20" stroke="rgba(0,195,255,0.60)" stroke-width="1.6"/>
                                <rect x="-18" y="-36" width="6"  height="36" rx="3" fill="rgba(0,185,255,0.12)"/>
                                <rect x="12"  y="-36" width="6"  height="36" rx="3" fill="rgba(0,0,20,0.28)"/>
                                <line x1="-12" y1="-28" x2="12" y2="-28" stroke="rgba(0,195,255,0.38)" stroke-width="1"/>
                                <line x1="-12" y1="-20" x2="12" y2="-20" stroke="rgba(0,195,255,0.38)" stroke-width="1"/>
                                <line x1="-12" y1="-12" x2="12" y2="-12" stroke="rgba(0,195,255,0.38)" stroke-width="1"/>
                                <path d="M-11,-36 L-31,-92" stroke="rgba(170,235,255,0.94)" stroke-width="3.2" stroke-linecap="round"/>
                                <path d="M11,-36 L31,-92" stroke="rgba(170,235,255,0.94)" stroke-width="3.2" stroke-linecap="round"/>
                                <line x1="-27" y1="-74" x2="-18" y2="-68" stroke="rgba(0,215,255,0.65)" stroke-width="1.2"/>
                                <line x1="-25" y1="-60" x2="-16" y2="-54" stroke="rgba(0,215,255,0.65)" stroke-width="1.2"/>
                                <line x1="-23" y1="-46" x2="-14" y2="-40" stroke="rgba(0,215,255,0.65)" stroke-width="1.2"/>
                                <line x1="27"  y1="-74" x2="18"  y2="-68" stroke="rgba(0,215,255,0.65)" stroke-width="1.2"/>
                                <line x1="25"  y1="-60" x2="16"  y2="-54" stroke="rgba(0,215,255,0.65)" stroke-width="1.2"/>
                                <line x1="23"  y1="-46" x2="14"  y2="-40" stroke="rgba(0,215,255,0.65)" stroke-width="1.2"/>
                                <circle cx="-31" cy="-92" r="4"  fill="rgba(150,230,255,0.94)"/>
                                <circle cx="-31" cy="-92" r="7"  fill="none" stroke="rgba(150,230,255,0.35)" stroke-width="1"/>
                                <circle cx="31"  cy="-92" r="4"  fill="rgba(150,230,255,0.94)"/>
                                <circle cx="31"  cy="-92" r="7"  fill="none" stroke="rgba(150,230,255,0.35)" stroke-width="1"/>
                              </g>
                              <circle r="13"  fill="#000c1e" stroke="rgba(0,195,255,0.68)" stroke-width="1.6"/>
                              <circle r="8"   fill="none"   stroke="rgba(0,195,255,0.35)" stroke-width="1.2"/>
                              <circle r="4"   fill="rgba(0,195,255,0.42)"/>
                            </g>
                          </g>
                          <circle r="17"  fill="#000c1e" stroke="rgba(0,195,255,0.72)" stroke-width="1.8"/>
                          <circle r="11"  fill="none"   stroke="rgba(0,195,255,0.32)" stroke-width="1.3"/>
                          <circle r="5"   fill="rgba(0,195,255,0.38)"/>
                          <line x1="-5" y1="0" x2="5" y2="0" stroke="rgba(0,215,255,0.55)" stroke-width="1"/>
                          <line x1="0" y1="-5" x2="0" y2="5" stroke="rgba(0,215,255,0.55)" stroke-width="1"/>
                        </g>
                      </g>
                      <circle r="22"  fill="#000c1e" stroke="rgba(0,195,255,0.74)" stroke-width="2"/>
                      <circle r="14"  fill="none"   stroke="rgba(0,195,255,0.30)" stroke-width="1.4"/>
                      <circle r="7"   fill="rgba(0,195,255,0.36)"/>
                      <line x1="-7" y1="0" x2="7" y2="0" stroke="rgba(0,215,255,0.55)" stroke-width="1.1"/>
                      <line x1="0" y1="-7" x2="0" y2="7" stroke="rgba(0,215,255,0.55)" stroke-width="1.1"/>
                    </g>
                  </g>
                  <circle r="28"  fill="#000c1e" stroke="rgba(0,195,255,0.76)" stroke-width="2.1"/>
                  <circle r="18"  fill="none"   stroke="rgba(0,195,255,0.29)" stroke-width="1.5"/>
                  <circle r="8"   fill="rgba(0,195,255,0.34)"/>
                  <line x1="-8" y1="0" x2="8" y2="0" stroke="rgba(0,215,255,0.54)" stroke-width="1.2"/>
                  <line x1="0" y1="-8" x2="0" y2="8" stroke="rgba(0,215,255,0.54)" stroke-width="1.2"/>
                </g>
              </g>
              <circle r="34"  fill="#000c1e" stroke="rgba(0,195,255,0.78)" stroke-width="2.2"/>
              <circle r="21"  fill="none"   stroke="rgba(0,195,255,0.28)" stroke-width="1.5"/>
              <circle r="10"  fill="rgba(0,195,255,0.32)"/>
              <line x1="-10" y1="0" x2="10" y2="0" stroke="rgba(0,215,255,0.53)" stroke-width="1.3"/>
              <line x1="0" y1="-10" x2="0" y2="10" stroke="rgba(0,215,255,0.53)" stroke-width="1.3"/>
            </g>
          </g>
          <circle r="40"  fill="#000c1e" stroke="rgba(0,195,255,0.80)" stroke-width="2.4"/>
          <circle r="25"  fill="none"   stroke="rgba(0,195,255,0.27)" stroke-width="1.6"/>
          <circle r="12"  fill="rgba(0,195,255,0.30)"/>
          <line x1="-12" y1="0" x2="12" y2="0" stroke="rgba(0,215,255,0.52)" stroke-width="1.4"/>
          <line x1="0" y1="-12" x2="0" y2="12" stroke="rgba(0,215,255,0.52)" stroke-width="1.4"/>
        </g>
      </g>
      <circle r="48"  fill="#000c1e" stroke="rgba(0,195,255,0.84)" stroke-width="2.6"/>
      <circle r="38"  fill="none"   stroke="rgba(0,195,255,0.26)" stroke-width="1.8"/>
      <circle r="28"  fill="#000814" stroke="rgba(0,195,255,0.42)" stroke-width="1.4"/>
      <circle r="8"   fill="rgba(0,195,255,0.36)"/>
      <line x1="-8" y1="0" x2="8" y2="0" stroke="rgba(0,215,255,0.60)" stroke-width="1.5"/>
      <line x1="0" y1="-8" x2="0" y2="8" stroke="rgba(0,215,255,0.60)" stroke-width="1.5"/>
      <circle cx="38"  cy="0"   r="3" fill="rgba(0,195,255,0.38)"/>
      <circle cx="-38" cy="0"   r="3" fill="rgba(0,195,255,0.38)"/>
      <circle cx="0"   cy="-38" r="3" fill="rgba(0,195,255,0.38)"/>
      <circle cx="0"   cy="38"  r="3" fill="rgba(0,195,255,0.38)"/>
    </g>
  </svg>

  <!-- LEFT SIDE ARM — wall-mounted at ~26% height -->
  <svg class="mc-arm-side mc-arm-side-l" viewBox="0 0 290 130" overflow="visible" xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="49" width="22" height="32" rx="4" fill="#000c20" stroke="rgba(0,195,255,0.75)" stroke-width="2"/>
    <rect x="3" y="53" width="16" height="24" rx="3" fill="rgba(0,4,16,0.90)" stroke="rgba(0,195,255,0.30)" stroke-width="1"/>
    <circle cx="11" cy="61" r="3" fill="rgba(0,195,255,0.55)"/>
    <circle cx="11" cy="69" r="3" fill="rgba(0,195,255,0.55)"/>
    <g transform="translate(20,65)">
      <g class="side-seg ss1">
        <rect x="0" y="-18" width="76" height="36" rx="5" fill="#000c20" stroke="rgba(0,195,255,0.48)" stroke-width="2"/>
        <rect x="0" y="-18" width="76" height="7"  rx="5" fill="rgba(0,185,255,0.11)"/>
        <rect x="0" y="11"  width="76" height="7"  rx="5" fill="rgba(0,0,20,0.32)"/>
        <rect x="7" y="-12" width="62" height="24" rx="3" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.23)" stroke-width="1"/>
        <rect x="16" y="-8" width="44" height="16" rx="2" fill="rgba(0,195,255,0.04)"/>
        <line x1="26" y1="-11" x2="26" y2="11" stroke="rgba(0,195,255,0.26)" stroke-width="1.3"/>
        <line x1="50" y1="-11" x2="50" y2="11" stroke="rgba(0,195,255,0.26)" stroke-width="1.3"/>
        <circle cx="26" cy="-9" r="2.5" fill="rgba(0,195,255,0.42)"/>
        <circle cx="26" cy="9"  r="2.5" fill="rgba(0,195,255,0.42)"/>
        <circle cx="50" cy="-9" r="2.5" fill="rgba(0,195,255,0.42)"/>
        <circle cx="50" cy="9"  r="2.5" fill="rgba(0,195,255,0.42)"/>
        <rect x="70" y="-22" width="10" height="44" rx="3" fill="#000d22" stroke="rgba(0,195,255,0.58)" stroke-width="1.6"/>
        <g transform="translate(76,0)">
          <g class="side-seg ss2">
            <rect x="0" y="-13" width="58" height="26" rx="4" fill="#000c20" stroke="rgba(0,195,255,0.43)" stroke-width="1.7"/>
            <rect x="0" y="-13" width="58" height="5"  rx="4" fill="rgba(0,185,255,0.09)"/>
            <rect x="0" y="8"   width="58" height="5"  rx="4" fill="rgba(0,0,20,0.28)"/>
            <rect x="6" y="-8"  width="46" height="16" rx="2.5" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.20)" stroke-width="0.9"/>
            <line x1="20" y1="-7" x2="20" y2="7" stroke="rgba(0,195,255,0.22)" stroke-width="1.1"/>
            <line x1="40" y1="-7" x2="40" y2="7" stroke="rgba(0,195,255,0.22)" stroke-width="1.1"/>
            <circle cx="20" cy="-5" r="2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="20" cy="5"  r="2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="40" cy="-5" r="2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="40" cy="5"  r="2" fill="rgba(0,195,255,0.38)"/>
            <rect x="52" y="-17" width="9" height="34" rx="2.5" fill="#000d22" stroke="rgba(0,195,255,0.52)" stroke-width="1.4"/>
            <g transform="translate(58,0)">
              <g class="side-seg ss3">
                <rect x="0" y="-9" width="44" height="18" rx="3.5" fill="#000c20" stroke="rgba(0,195,255,0.40)" stroke-width="1.6"/>
                <rect x="0" y="-9" width="44" height="4"  rx="3.5" fill="rgba(0,185,255,0.09)"/>
                <rect x="0" y="5"  width="44" height="4"  rx="3.5" fill="rgba(0,0,20,0.27)"/>
                <rect x="5" y="-5" width="34" height="10" rx="2" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.18)" stroke-width="0.9"/>
                <line x1="15" y1="-4" x2="15" y2="4" stroke="rgba(0,195,255,0.21)" stroke-width="1"/>
                <line x1="30" y1="-4" x2="30" y2="4" stroke="rgba(0,195,255,0.21)" stroke-width="1"/>
                <rect x="38" y="-13" width="8" height="26" rx="2" fill="#000d22" stroke="rgba(0,195,255,0.48)" stroke-width="1.2"/>
                <g transform="translate(44,0)">
                  <g class="side-seg ss4">
                    <rect x="0" y="-7" width="28" height="14" rx="3" fill="#000c20" stroke="rgba(0,195,255,0.60)" stroke-width="1.5"/>
                    <rect x="0" y="-7" width="28" height="3"  rx="3" fill="rgba(0,185,255,0.12)"/>
                    <rect x="0" y="4"  width="28" height="3"  rx="3" fill="rgba(0,0,20,0.28)"/>
                    <line x1="10" y1="-5" x2="10" y2="5" stroke="rgba(0,195,255,0.38)" stroke-width="1"/>
                    <line x1="20" y1="-5" x2="20" y2="5" stroke="rgba(0,195,255,0.38)" stroke-width="1"/>
                    <path d="M28,0 C42,-12 44,-26 34,-34" fill="none" stroke="rgba(190,245,255,0.96)" stroke-width="2.4" stroke-linecap="round"/>
                    <circle cx="34" cy="-34" r="3.5" fill="rgba(190,245,255,0.96)"/>
                    <circle cx="34" cy="-34" r="6"   fill="none" stroke="rgba(190,245,255,0.32)" stroke-width="1"/>
                    <path d="M28,0 C36,6 38,13 32,17" fill="none" stroke="rgba(0,215,255,0.55)" stroke-width="1.1" stroke-dasharray="4,3"/>
                  </g>
                  <circle r="7"   fill="#000c1e" stroke="rgba(0,195,255,0.68)" stroke-width="1.4"/>
                  <circle r="4"   fill="none"   stroke="rgba(0,195,255,0.35)" stroke-width="1"/>
                  <circle r="2"   fill="rgba(0,195,255,0.42)"/>
                </g>
              </g>
              <circle r="10"  fill="#000c1e" stroke="rgba(0,195,255,0.72)" stroke-width="1.6"/>
              <circle r="6"   fill="none"   stroke="rgba(0,195,255,0.32)" stroke-width="1.2"/>
              <circle r="3"   fill="rgba(0,195,255,0.38)"/>
              <line x1="-3" y1="0" x2="3" y2="0" stroke="rgba(0,215,255,0.55)" stroke-width="0.9"/>
              <line x1="0" y1="-3" x2="0" y2="3" stroke="rgba(0,215,255,0.55)" stroke-width="0.9"/>
            </g>
          </g>
          <circle r="14"  fill="#000c1e" stroke="rgba(0,195,255,0.76)" stroke-width="1.9"/>
          <circle r="9"   fill="none"   stroke="rgba(0,195,255,0.30)" stroke-width="1.3"/>
          <circle r="4.5" fill="rgba(0,195,255,0.34)"/>
          <line x1="-4.5" y1="0" x2="4.5" y2="0" stroke="rgba(0,215,255,0.54)" stroke-width="1"/>
          <line x1="0" y1="-4.5" x2="0" y2="4.5" stroke="rgba(0,215,255,0.54)" stroke-width="1"/>
        </g>
      </g>
      <circle r="22"  fill="#000c1e" stroke="rgba(0,195,255,0.84)" stroke-width="2.2"/>
      <circle r="15"  fill="none"   stroke="rgba(0,195,255,0.28)" stroke-width="1.6"/>
      <circle r="10"  fill="#000814" stroke="rgba(0,195,255,0.40)" stroke-width="1.2"/>
      <circle r="4"   fill="rgba(0,195,255,0.34)"/>
      <line x1="-4" y1="0" x2="4" y2="0" stroke="rgba(0,215,255,0.58)" stroke-width="1.3"/>
      <line x1="0" y1="-4" x2="0" y2="4" stroke="rgba(0,215,255,0.58)" stroke-width="1.3"/>
      <circle cx="15"  cy="0"   r="2.5" fill="rgba(0,195,255,0.38)"/>
      <circle cx="-15" cy="0"   r="2.5" fill="rgba(0,195,255,0.38)"/>
      <circle cx="0"   cy="-15" r="2.5" fill="rgba(0,195,255,0.38)"/>
      <circle cx="0"   cy="15"  r="2.5" fill="rgba(0,195,255,0.38)"/>
    </g>
  </svg>

  <!-- RIGHT SIDE ARM — mirrored via scaleX(-1), at ~60% height -->
  <svg class="mc-arm-side mc-arm-side-r" viewBox="0 0 290 130" overflow="visible" xmlns="http://www.w3.org/2000/svg">
    <rect x="0" y="49" width="22" height="32" rx="4" fill="#000c20" stroke="rgba(0,195,255,0.75)" stroke-width="2"/>
    <rect x="3" y="53" width="16" height="24" rx="3" fill="rgba(0,4,16,0.90)" stroke="rgba(0,195,255,0.30)" stroke-width="1"/>
    <circle cx="11" cy="61" r="3" fill="rgba(0,195,255,0.55)"/>
    <circle cx="11" cy="69" r="3" fill="rgba(0,195,255,0.55)"/>
    <g transform="translate(20,65)">
      <g class="side-seg ss1">
        <rect x="0" y="-18" width="76" height="36" rx="5" fill="#000c20" stroke="rgba(0,195,255,0.48)" stroke-width="2"/>
        <rect x="0" y="-18" width="76" height="7"  rx="5" fill="rgba(0,185,255,0.11)"/>
        <rect x="0" y="11"  width="76" height="7"  rx="5" fill="rgba(0,0,20,0.32)"/>
        <rect x="7" y="-12" width="62" height="24" rx="3" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.23)" stroke-width="1"/>
        <rect x="16" y="-8" width="44" height="16" rx="2" fill="rgba(0,195,255,0.04)"/>
        <line x1="26" y1="-11" x2="26" y2="11" stroke="rgba(0,195,255,0.26)" stroke-width="1.3"/>
        <line x1="50" y1="-11" x2="50" y2="11" stroke="rgba(0,195,255,0.26)" stroke-width="1.3"/>
        <circle cx="26" cy="-9" r="2.5" fill="rgba(0,195,255,0.42)"/>
        <circle cx="26" cy="9"  r="2.5" fill="rgba(0,195,255,0.42)"/>
        <circle cx="50" cy="-9" r="2.5" fill="rgba(0,195,255,0.42)"/>
        <circle cx="50" cy="9"  r="2.5" fill="rgba(0,195,255,0.42)"/>
        <rect x="70" y="-22" width="10" height="44" rx="3" fill="#000d22" stroke="rgba(0,195,255,0.58)" stroke-width="1.6"/>
        <g transform="translate(76,0)">
          <g class="side-seg ss2">
            <rect x="0" y="-13" width="58" height="26" rx="4" fill="#000c20" stroke="rgba(0,195,255,0.43)" stroke-width="1.7"/>
            <rect x="0" y="-13" width="58" height="5"  rx="4" fill="rgba(0,185,255,0.09)"/>
            <rect x="0" y="8"   width="58" height="5"  rx="4" fill="rgba(0,0,20,0.28)"/>
            <rect x="6" y="-8"  width="46" height="16" rx="2.5" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.20)" stroke-width="0.9"/>
            <line x1="20" y1="-7" x2="20" y2="7" stroke="rgba(0,195,255,0.22)" stroke-width="1.1"/>
            <line x1="40" y1="-7" x2="40" y2="7" stroke="rgba(0,195,255,0.22)" stroke-width="1.1"/>
            <circle cx="20" cy="-5" r="2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="20" cy="5"  r="2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="40" cy="-5" r="2" fill="rgba(0,195,255,0.38)"/>
            <circle cx="40" cy="5"  r="2" fill="rgba(0,195,255,0.38)"/>
            <rect x="52" y="-17" width="9" height="34" rx="2.5" fill="#000d22" stroke="rgba(0,195,255,0.52)" stroke-width="1.4"/>
            <g transform="translate(58,0)">
              <g class="side-seg ss3">
                <rect x="0" y="-9" width="44" height="18" rx="3.5" fill="#000c20" stroke="rgba(0,195,255,0.40)" stroke-width="1.6"/>
                <rect x="0" y="-9" width="44" height="4"  rx="3.5" fill="rgba(0,185,255,0.09)"/>
                <rect x="0" y="5"  width="44" height="4"  rx="3.5" fill="rgba(0,0,20,0.27)"/>
                <rect x="5" y="-5" width="34" height="10" rx="2" fill="rgba(0,4,16,0.88)" stroke="rgba(0,195,255,0.18)" stroke-width="0.9"/>
                <line x1="15" y1="-4" x2="15" y2="4" stroke="rgba(0,195,255,0.21)" stroke-width="1"/>
                <line x1="30" y1="-4" x2="30" y2="4" stroke="rgba(0,195,255,0.21)" stroke-width="1"/>
                <rect x="38" y="-13" width="8" height="26" rx="2" fill="#000d22" stroke="rgba(0,195,255,0.48)" stroke-width="1.2"/>
                <g transform="translate(44,0)">
                  <g class="side-seg ss4">
                    <rect x="0" y="-7" width="28" height="14" rx="3" fill="#000c20" stroke="rgba(0,195,255,0.60)" stroke-width="1.5"/>
                    <rect x="0" y="-7" width="28" height="3"  rx="3" fill="rgba(0,185,255,0.12)"/>
                    <rect x="0" y="4"  width="28" height="3"  rx="3" fill="rgba(0,0,20,0.28)"/>
                    <line x1="10" y1="-5" x2="10" y2="5" stroke="rgba(0,195,255,0.38)" stroke-width="1"/>
                    <line x1="20" y1="-5" x2="20" y2="5" stroke="rgba(0,195,255,0.38)" stroke-width="1"/>
                    <path d="M28,0 C42,-12 44,-26 34,-34" fill="none" stroke="rgba(190,245,255,0.96)" stroke-width="2.4" stroke-linecap="round"/>
                    <circle cx="34" cy="-34" r="3.5" fill="rgba(190,245,255,0.96)"/>
                    <circle cx="34" cy="-34" r="6"   fill="none" stroke="rgba(190,245,255,0.32)" stroke-width="1"/>
                    <path d="M28,0 C36,6 38,13 32,17" fill="none" stroke="rgba(0,215,255,0.55)" stroke-width="1.1" stroke-dasharray="4,3"/>
                  </g>
                  <circle r="7"   fill="#000c1e" stroke="rgba(0,195,255,0.68)" stroke-width="1.4"/>
                  <circle r="4"   fill="none"   stroke="rgba(0,195,255,0.35)" stroke-width="1"/>
                  <circle r="2"   fill="rgba(0,195,255,0.42)"/>
                </g>
              </g>
              <circle r="10"  fill="#000c1e" stroke="rgba(0,195,255,0.72)" stroke-width="1.6"/>
              <circle r="6"   fill="none"   stroke="rgba(0,195,255,0.32)" stroke-width="1.2"/>
              <circle r="3"   fill="rgba(0,195,255,0.38)"/>
              <line x1="-3" y1="0" x2="3" y2="0" stroke="rgba(0,215,255,0.55)" stroke-width="0.9"/>
              <line x1="0" y1="-3" x2="0" y2="3" stroke="rgba(0,215,255,0.55)" stroke-width="0.9"/>
            </g>
          </g>
          <circle r="14"  fill="#000c1e" stroke="rgba(0,195,255,0.76)" stroke-width="1.9"/>
          <circle r="9"   fill="none"   stroke="rgba(0,195,255,0.30)" stroke-width="1.3"/>
          <circle r="4.5" fill="rgba(0,195,255,0.34)"/>
          <line x1="-4.5" y1="0" x2="4.5" y2="0" stroke="rgba(0,215,255,0.54)" stroke-width="1"/>
          <line x1="0" y1="-4.5" x2="0" y2="4.5" stroke="rgba(0,215,255,0.54)" stroke-width="1"/>
        </g>
      </g>
      <circle r="22"  fill="#000c1e" stroke="rgba(0,195,255,0.84)" stroke-width="2.2"/>
      <circle r="15"  fill="none"   stroke="rgba(0,195,255,0.28)" stroke-width="1.6"/>
      <circle r="10"  fill="#000814" stroke="rgba(0,195,255,0.40)" stroke-width="1.2"/>
      <circle r="4"   fill="rgba(0,195,255,0.34)"/>
      <line x1="-4" y1="0" x2="4" y2="0" stroke="rgba(0,215,255,0.58)" stroke-width="1.3"/>
      <line x1="0" y1="-4" x2="0" y2="4" stroke="rgba(0,215,255,0.58)" stroke-width="1.3"/>
      <circle cx="15"  cy="0"   r="2.5" fill="rgba(0,195,255,0.38)"/>
      <circle cx="-15" cy="0"   r="2.5" fill="rgba(0,195,255,0.38)"/>
      <circle cx="0"   cy="-15" r="2.5" fill="rgba(0,195,255,0.38)"/>
      <circle cx="0"   cy="15"  r="2.5" fill="rgba(0,195,255,0.38)"/>
    </g>
  </svg>

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
const PHASE_DURATION = 15000;

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
