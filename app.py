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

<style>
html, body {
    margin: 0;
    padding: 0;
    width: 100%;
    height: 100%;
    overflow: hidden;
    font-family: Arial, sans-serif;
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
    background: rgba(0,0,0,0.7);
    padding: 70px 90px;
    border-radius: 25px;
    border: 2px solid cyan;
    box-shadow: 0 0 45px cyan;
    color: white;
    text-align: center;
}

/* HEADINGS */
.title {
    font-size: 46px;
    color: cyan;
    letter-spacing: 3px;
}

.product {
    font-size: 30px;
    margin: 12px 0 8px 0;
}

.date {
    color: #ffffff;
    margin-bottom: 40px;
    font-size: 24px;
    font-weight: 700;
    letter-spacing: 1px;
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

    <p style="margin-top:30px; opacity:0.6; font-size:14px;">
        Click anywhere to enter full screen
    </p>
</div>

<script>
/* FULLSCREEN ON FIRST CLICK */
function goFullScreen() {
    const el = document.documentElement;
    if (el.requestFullscreen) {
        el.requestFullscreen();
    } else if (el.webkitRequestFullscreen) {
        el.webkitRequestFullscreen();
    }
}
document.addEventListener("click", goFullScreen, { once: true });

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

# ---------------- INJECT DATA ----------------
html_code = html_code.replace(
    "__VIDEO_DATA__", "data:video/mp4;base64," + video_base64
)
html_code = html_code.replace("__LAUNCH_DATE__", LAUNCH_DATE)

# ---------------- RENDER ----------------
st.components.v1.html(html_code, height=1000, scrolling=False)
