import { playlist } from "./playlist.js";

const audio = document.getElementById("audio-player");
const albumArtEl = document.querySelector(".album-art");
const trackTitleEl = document.getElementById("track-title");
const trackArtistEl = document.getElementById("track-artist");
const progressBar = document.getElementById("progress-bar");
const progressBarFill = document.getElementById("progress-bar-fill");
const progressBarMarker = document.getElementById("progress-bar-marker");
const timeCurrentEl = document.getElementById("time-current");
const timeDurationEl = document.getElementById("time-duration");
const btnPlayPause = document.getElementById("btn-play-pause");
const btnPrev = document.getElementById("btn-prev");
const btnNext = document.getElementById("btn-next");
const btnMinimize = document.getElementById("btn-minimize");
const btnClose = document.getElementById("btn-close");

let currentTrackIndex = 0;
let isPlaying = false;

function formatTime(seconds) {
  if (!Number.isFinite(seconds)) return "0:00";
  const mins = Math.floor(seconds / 60);
  const secs = Math.floor(seconds % 60)
    .toString()
    .padStart(2, "0");
  return `${mins}:${secs}`;
}

function loadTrack(index) {
  if (playlist.length === 0) {
    trackTitleEl.textContent = "Nenhuma musica adicionada";
    trackArtistEl.textContent = "";
    audio.removeAttribute("src");
    albumArtEl.style.backgroundImage = "";
    return;
  }

  const track = playlist[index];
  trackTitleEl.textContent = track.title;
  trackArtistEl.textContent = track.artist;
  audio.src = track.file;

  // Camada de cima = bloco da faixa (gerado por scripts/generate_block.py).
  // Enquanto esse ficheiro nao existir, cai para o placeholder/gradiente do CSS.
  albumArtEl.style.backgroundImage = track.block
    ? `url("${track.block}"), var(--album-fallback)`
    : "";
}

function updatePlayPauseIcon() {
  btnPlayPause.classList.toggle("control-btn-play", !isPlaying);
  btnPlayPause.classList.toggle("control-btn-pause", isPlaying);
  btnPlayPause.title = isPlaying ? "Pausar" : "Reproduzir";
}

function play() {
  if (playlist.length === 0) return;
  audio.play();
  isPlaying = true;
  updatePlayPauseIcon();
}

function pause() {
  audio.pause();
  isPlaying = false;
  updatePlayPauseIcon();
}

function togglePlayPause() {
  if (playlist.length === 0) return;
  if (isPlaying) {
    pause();
  } else {
    play();
  }
}

function playTrackAt(index) {
  if (playlist.length === 0) return;
  currentTrackIndex = (index + playlist.length) % playlist.length;
  loadTrack(currentTrackIndex);
  play();
}

function playNext() {
  playTrackAt(currentTrackIndex + 1);
}

function playPrev() {
  playTrackAt(currentTrackIndex - 1);
}

function updateProgress() {
  const { currentTime, duration } = audio;
  if (!Number.isFinite(duration) || duration === 0) {
    progressBarFill.style.width = "0%";
    progressBarMarker.style.left = "0%";
    return;
  }

  const percent = (currentTime / duration) * 100;
  progressBarFill.style.width = `${percent}%`;
  progressBarMarker.style.left = `${percent}%`;
  timeCurrentEl.textContent = formatTime(currentTime);
  timeDurationEl.textContent = formatTime(duration);
}

function seekToClick(event) {
  if (playlist.length === 0 || !Number.isFinite(audio.duration)) return;
  const rect = progressBar.getBoundingClientRect();
  const clickRatio = Math.min(Math.max((event.clientX - rect.left) / rect.width, 0), 1);
  audio.currentTime = clickRatio * audio.duration;
  updateProgress();
}

btnPlayPause.addEventListener("click", togglePlayPause);
btnPrev.addEventListener("click", playPrev);
btnNext.addEventListener("click", playNext);
progressBar.addEventListener("click", seekToClick);

audio.addEventListener("timeupdate", updateProgress);
audio.addEventListener("loadedmetadata", updateProgress);
audio.addEventListener("ended", playNext);

btnMinimize.addEventListener("click", () => window.farmPlayer?.minimizeWindow());
btnClose.addEventListener("click", () => window.farmPlayer?.closeWindow());

loadTrack(currentTrackIndex);
updatePlayPauseIcon();
