import streamlit as st
import base64

st.set_page_config(layout="wide")

# ---------------- CONFIG ----------------
VIDEO_PATH = "/home/dhruvin/countdown-project/assets/background.mp4"
LAUNCH_DATE = "2026-06-13T00:00:00"

# ---------------- LOAD VIDEO ----------------
with open(VIDEO_PATH, "rb") as f:
    video_bytes = f.read()

video_base64 = base64.b64encode(video_bytes).decode("utf-8")

# ---------------- HTML ----------------
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
    overflow: hidden;
    font-family: Orbitron, sans-serif;
}

/* VIDEO FULLSCREEN (NO CROPPING) */
video {
    position: fixed;
    inset: 0;
    width: 100vw;
    height: 100vh;
    object-fit: contain;
    background: black;
    z-index: -1;
}

/* MAIN OVERLAY */
.overlay {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: rgba(0,0,0,0.2);
    padding: 70px 90px;
    border-radius: 25px;
    border: 2px solid cyan;
    box-shadow: 0 0 45px cyan;
    color: white;
    text-align: center;
    max-width: 90vw;
    max-height: 85vh;
}

/* HEADINGS */
.title {
    font-size: 46px;
    color: cyan;
    letter-spacing: 3px;
    font-weight: 800;
}

.product {
    font-size: 30px;
    margin: 12px 0 8px 0;
}

.date {
    font-size: 24px;
    font-weight: 700;
    margin-bottom: 40px;
    color: white;
    text-shadow: 0 0 8px rgba(0,255,255,0.6);
}

/* TIMER */
.timer {
    display: flex;
    gap: 35px;
    justify-content: center;
}

.box {
    text-align: center;
}

.value {
    font-size: 36px;
    font-weight: bold;
    background: black;
    padding: 20px 26px;
    border-radius: 10px;
    border: 2px solid cyan;
    min-width: 70px;
    box-shadow: inset 0 0 12px rgba(0,255,255,0.7),
                0 0 15px rgba(0,255,255,0.6);
}

.label {
    margin-top: 10px;
    font-size: 13px;
    color: cyan;
    letter-spacing: 1.5px;
}

/* FULLSCREEN BUTTON */
#fullscreen-btn {
    position: fixed;
    bottom: 30px;
    right: 30px;
    padding: 12px 18px;
    font-size: 14px;
    font-weight: 600;
    color: black;
    background: cyan;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    z-index: 10;
    box-shadow: 0 0 15px rgba(0,255,255,0.8);
}

#fullscreen-btn:hover {
    background: #00e5e5;
}
</style>
</head>

<body>

<video autoplay muted loop playsinline>
    <source src="__VIDEO_DATA__" type="video/mp4">
</video>

<div class="overlay">
    <div class="title">MIZZO ORION</div>
    <div class="product">PRODUCT LAUNCH</div>
    <div class="date">Launch Date: June 13, 2026</div>

    <div class="timer">
        <div class="box"><div class="value" id="months">00</div><div class="label">MONTHS</div></div>
        <div class="box"><div class="value" id="days">00</div><div class="label">DAYS</div></div>
        <div class="box"><div class="value" id="hours">00</div><div class="label">HOURS</div></div>
        <div class="box"><div class="value" id="minutes">00</div><div class="label">MINUTES</div></div>
        <div class="box"><div class="value" id="seconds">00</div><div class="label">SECONDS</div></div>
    </div>
</div>

<button id="fullscreen-btn">⛶ </button>

<script>
/* ---------- FULLSCREEN LOGIC ---------- */
const fsButton = document.getElementById("fullscreen-btn");

function enterFullscreen() {
    const el = document.documentElement;
    if (el.requestFullscreen) {
        el.requestFullscreen();
    } else if (el.webkitRequestFullscreen) {
        el.webkitRequestFullscreen();
    }
}

function isFullscreen() {
    return document.fullscreenElement || document.webkitFullscreenElement;
}

fsButton.addEventListener("click", enterFullscreen);

function onFullscreenChange() {
    if (isFullscreen()) {
        fsButton.style.display = "none";
    } else {
        fsButton.style.display = "block";
    }
}

document.addEventListener("fullscreenchange", onFullscreenChange);
document.addEventListener("webkitfullscreenchange", onFullscreenChange);

/* ---------- COUNTDOWN ---------- */
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

# ---------------- INJECT DATA ----------------
html_code = html_code.replace(
    "__VIDEO_DATA__", "data:video/mp4;base64," + video_base64
)
html_code = html_code.replace("__LAUNCH_DATE__", LAUNCH_DATE)

# ---------------- RENDER ----------------
st.components.v1.html(html_code, height=1000, scrolling=False)
