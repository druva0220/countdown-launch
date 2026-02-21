import streamlit as st
import base64

st.set_page_config(layout="wide")

# ---------------- CONFIG ----------------
VIDEO_PATH = "background.mp4"
LAUNCH_DATE = "2026-06-13T00:00:00"

# ---------------- LOAD VIDEO ----------------
with open(VIDEO_PATH, "rb") as f:
    video_bytes = f.read()

video_base64 = base64.b64encode(video_bytes).decode("utf-8")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700&display=swap" rel="stylesheet">
<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;                 /* stop page scroll */
    overscroll-behavior: none;        /* stop bounce scroll on TV browsers */
    font-family: Orbitron, sans-serif;
}

video {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    object-fit: contain;
    background: black;
    z-index: -1;
}

/* MAIN OVERLAY (TV-safe sizing) */
.overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);

    /* prevents taking whole TV */
    width: clamp(720px, 70vw, 1100px);

    /* responsive padding */
    padding: clamp(26px, 3.2vw, 58px) clamp(28px, 3.8vw, 86px);

    background: rgba(0,0,0,0.18);
    border-radius: 28px;
    border: 2px solid rgba(0,255,255,0.9);
    box-shadow: 0 0 55px rgba(0,255,255,0.55);
    color: white;
    text-align: center;
    backdrop-filter: blur(2px);

    /* keep content inside */
    max-height: 82vh;
    box-sizing: border-box;
}

/* very large screens */
@media (min-width: 1700px) {
  .overlay { width: clamp(760px, 58vw, 1100px); }
}

.title {
    font-size: clamp(30px, 3.2vw, 46px);
    color: cyan;
    letter-spacing: 3px;
    font-weight: 800;
    margin-bottom: 10px;
}

/* PRODUCT LAUNCH (like MORE) */
.product.kinetic{
    margin: 10px 0 16px 0;
    position: relative;
    height: 66px;
    display: flex;
    justify-content: center;
    align-items: center;
    overflow: hidden;
}

.kinetic-outline{
    position: relative;
    display: inline-block;
    font-size: clamp(24px, 3.2vw, 54px);
    font-weight: 700;
    letter-spacing: 7px;
    text-transform: uppercase;
    color: transparent;
    opacity: 0;
    transform: translateY(16px) scale(0.985);
    will-change: transform, opacity;
    filter: drop-shadow(0 0 6px rgba(255,255,255,0.18))
            drop-shadow(0 0 10px rgba(0,255,255,0.18));
    animation: outlineInOut 3.8s cubic-bezier(.2,.8,.2,1) infinite;
}

.kinetic-outline::before{
    content: attr(data-text);
    position: absolute;
    inset: 0;
    color: transparent;
    -webkit-text-stroke: 4px rgba(255,255,255,0.92);
    text-stroke: 4px rgba(255,255,255,0.92);
}

.kinetic-outline::after{
    content: attr(data-text);
    position: absolute;
    inset: 0;
    color: transparent;
    -webkit-text-stroke: 1.5px rgba(255,255,255,0.98);
    text-stroke: 1.5px rgba(255,255,255,0.98);
}

.product.kinetic::after{
    content: "";
    position: absolute;
    bottom: 10px;
    width: 0%;
    height: 2px;
    background: rgba(0,255,255,0.75);
    box-shadow: 0 0 10px rgba(0,255,255,0.35);
    opacity: 0;
    animation: underlineSweep 3.8s cubic-bezier(.2,.8,.2,1) infinite;
}

@keyframes outlineInOut {
    0%   { opacity: 0; transform: translateY(18px) scale(0.985); }
    12%  { opacity: 1; transform: translateY(0px)  scale(1.01); }
    24%  { opacity: 1; transform: translateY(0px)  scale(1.00); }
    74%  { opacity: 1; transform: translateY(0px)  scale(1.00); }
    88%  { opacity: 0.35; transform: translateY(-10px) scale(0.995); }
    100% { opacity: 0; transform: translateY(-18px) scale(0.985); }
}

@keyframes underlineSweep {
    0%   { width: 0%; opacity: 0; transform: translateX(-20px); }
    12%  { width: 58%; opacity: 1; transform: translateX(0px); }
    24%  { width: 70%; opacity: 1; }
    74%  { width: 70%; opacity: 1; }
    100% { width: 0%;  opacity: 0; transform: translateX(20px); }
}

.date {
    font-size: clamp(16px, 1.7vw, 22px);
    font-weight: 700;
    margin: 8px 0 28px 0;
    color: white;
    text-shadow: 0 0 8px rgba(0,255,255,0.5);
}

/* TIMER GRID — auto-fit so boxes NEVER go out */
.timer {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
    gap: clamp(14px, 2.2vw, 34px);
    justify-content: center;
    align-items: center;
    width: 100%;
}

/* EDGE DISPLAY BORDER (MULTICOLOR) */
.value{
    width: clamp(110px, 10vw, 130px);
    height: clamp(76px, 7.5vw, 88px);
    border-radius: 16px;
    position: relative;
    display: grid;
    place-items: center;
    overflow: hidden;
    border: none;
    box-shadow:
        inset 0 0 18px rgba(0,255,255,0.20),
        0 0 22px rgba(0,255,255,0.35);
}

/* multicolor border ring */
.value::after{
    content:"";
    position:absolute;
    inset:-2px;
    border-radius: 18px;
    background: conic-gradient(
        from 0deg,
        #00fff0,
        #00aaff,
        #7a00ff,
        #ff2bd6,
        #ff7a00,
        #ffe600,
        #00ff66,
        #00fff0
    );
    animation: edgeSpin 2.2s linear infinite;
    filter: blur(0.4px);
}

/* inner black card */
.value::before{
    content:"";
    position:absolute;
    inset: 4px;
    border-radius: 13px;
    background: rgba(0,0,0,0.88);
    box-shadow: inset 0 0 18px rgba(0,255,255,0.22);
    z-index: 1;
}

.value{ animation: edgeBreath 3.5s ease-in-out infinite; }

@keyframes edgeSpin{ to { transform: rotate(360deg); } }
@keyframes edgeBreath{
    0%,100% { box-shadow: inset 0 0 18px rgba(0,255,255,0.18), 0 0 18px rgba(0,255,255,0.28); }
    50%     { box-shadow: inset 0 0 18px rgba(0,255,255,0.26), 0 0 26px rgba(0,255,255,0.38); }
}

/* content above inner card */
.num, .unit, .corner { position: relative; z-index: 2; }

.num{
    font-size: clamp(28px, 2.8vw, 42px);
    font-weight: 800;
    letter-spacing: 2px;
    color: white;
    text-shadow:
        0 0 10px rgba(0,255,255,0.35),
        0 0 22px rgba(0,255,255,0.25);
    line-height: 1;
}

.unit{
    position: absolute;
    bottom: 10px;
    left: 0;
    width: 100%;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 2px;
    color: rgba(0,255,255,0.95);
    text-shadow: 0 0 12px rgba(0,255,255,0.35);
    opacity: 0.95;
}

.corner{
    position:absolute;
    top:10px;
    right:10px;
    width:14px;
    height:14px;
    border-top:2px solid rgba(0,255,255,0.8);
    border-right:2px solid rgba(0,255,255,0.8);
    opacity: 0.55;
}

/* FULLSCREEN BUTTON — bigger for TV remote */
#fullscreen-btn {
    position: fixed;
    bottom: 26px;
    right: 26px;
    width: 56px;
    height: 56px;
    font-size: 22px;
    font-weight: 800;
    color: black;
    background: cyan;
    border: none;
    border-radius: 14px;
    cursor: pointer;
    z-index: 10;
    box-shadow: 0 0 18px rgba(0,255,255,0.75);
}
#fullscreen-btn:hover { background: #00e5e5; }

/* show focus outline for TV navigation */
#fullscreen-btn:focus {
    outline: 3px solid rgba(255,255,255,0.8);
    outline-offset: 4px;
}

/* reduce motion */
@media (prefers-reduced-motion: reduce) {
  .kinetic-outline, .product.kinetic::after { animation: none; opacity: 1; transform: none; }
  .value::after, .value { animation: none; }
}
</style>
</head>

<body tabindex="0">

<video autoplay muted loop playsinline>
  <source src="__VIDEO_DATA__" type="video/mp4">
</video>

<div class="overlay" id="overlay">
  <div class="title">MIZZO ORION</div>

  <div class="product kinetic">
    <span class="kinetic-outline" data-text="PRODUCT LAUNCH">PRODUCT LAUNCH</span>
  </div>

  <div class="date">Launch Date: June 13, 2026</div>

  <div class="timer">
    <div class="value"><div class="corner"></div><div class="num" id="months">00</div><div class="unit">MONTHS</div></div>
    <div class="value"><div class="corner"></div><div class="num" id="days">00</div><div class="unit">DAYS</div></div>
    <div class="value"><div class="corner"></div><div class="num" id="hours">00</div><div class="unit">HOURS</div></div>
    <div class="value"><div class="corner"></div><div class="num" id="minutes">00</div><div class="unit">MINUTES</div></div>
    <div class="value"><div class="corner"></div><div class="num" id="seconds">00</div><div class="unit">SECONDS</div></div>
  </div>
</div>

<button id="fullscreen-btn" aria-label="Fullscreen" title="Fullscreen">⛶</button>

<script>
/* IMPORTANT: prevent remote scrolling the page */
window.addEventListener('wheel', (e) => e.preventDefault(), { passive: false });
window.addEventListener('touchmove', (e) => e.preventDefault(), { passive: false });

/* FULLSCREEN */
const fsButton = document.getElementById("fullscreen-btn");
const overlay = document.getElementById("overlay");

function enterFullscreen() {
  const el = document.documentElement;
  if (el.requestFullscreen) el.requestFullscreen();
  else if (el.webkitRequestFullscreen) el.webkitRequestFullscreen();
}
function isFullscreen() {
  return document.fullscreenElement || document.webkitFullscreenElement;
}

fsButton.addEventListener("click", enterFullscreen);

/* TV remote support: OK/Enter triggers fullscreen (focus body) */
window.addEventListener("load", () => {
  document.body.focus();
  // also focus the button so remote can click easily
  fsButton.focus();
});

document.addEventListener("keydown", (e) => {
  if (e.key === "Enter" || e.key === " " || e.key === "OK") {
    enterFullscreen();
  }
});

/* also allow clicking overlay area to fullscreen (easy on TV) */
overlay.addEventListener("click", enterFullscreen);

function onFullscreenChange() {
  fsButton.style.display = isFullscreen() ? "none" : "block";
}
document.addEventListener("fullscreenchange", onFullscreenChange);
document.addEventListener("webkitfullscreenchange", onFullscreenChange);

/* COUNTDOWN */
const launchDate = new Date("__LAUNCH_DATE__");
function updateCountdown() {
  const now = new Date();
  let diff = launchDate - now;
  if (diff <= 0) return;

  let totalSeconds = Math.floor(diff / 1000);
  let minutes = Math.floor(totalSeconds / 60);
  let hours = Math.floor(minutes / 60);
  let days = Math.floor(hours / 24);

  let months = Math.floor(days / 30);
  days %= 30;
  hours %= 24;
  minutes %= 60;
  let seconds = totalSeconds % 60;

  document.getElementById("months").innerText = String(months).padStart(2, "0");
  document.getElementById("days").innerText = String(days).padStart(2, "0");
  document.getElementById("hours").innerText = String(hours).padStart(2, "0");
  document.getElementById("minutes").innerText = String(minutes).padStart(2, "0");
  document.getElementById("seconds").innerText = String(seconds).padStart(2, "0");
}
setInterval(updateCountdown, 1000);
updateCountdown();
</script>

</body>
</html>
"""

html_code = html_code.replace("__VIDEO_DATA__", "data:video/mp4;base64," + video_base64)
html_code = html_code.replace("__LAUNCH_DATE__", LAUNCH_DATE)

# IMPORTANT: use a tall iframe on TVs to avoid remote scrolling
st.components.v1.html(html_code, height=2200, scrolling=False)
