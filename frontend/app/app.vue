<script setup>
import { ref, watch } from 'vue'
import confetti from 'canvas-confetti'

const accepted = ref(false)
const currentPage = ref(0) // 0 = Cover, 1 = Intro, 2 = Gallery, 3 = Game
const totalPages = 3

// --- YES/NO BUTTON LOGIC ---
const noTexts = [
  "Нет", "Ты уверена?", "Подумай еще!", "Не разбивай мне сердце 💔",
  "Я буду плакать...", "Ну пожалуйста?", "Ладно, я понял...", "Шутка! Жми ДА! ❤️"
]
const noTextIndex = ref(0)
const noBtnText = ref(noTexts[0])
const yesScale = ref(1)
const noPos = ref({ x: 0, y: 0 })

coconst clamp = (value, min, max) => Math.min(Math.max(value, min), max)

const handleNo = () => {
  yesScale.value *= 1.2

  // Approximate button size and margin in pixels
  const buttonWidth = 150
  const buttonHeight = 50
  const margin = 16

  // Compute maximum safe translation so the button stays within the viewport
  const viewportWidth = typeof window !== 'undefined' ? window.innerWidth : 0
  const viewportHeight = typeof window !== 'undefined' ? window.innerHeight : 0
  const maxX = Math.max(0, (viewportWidth - buttonWidth) / 2 - margin)
  const maxY = Math.max(0, (viewportHeight - buttonHeight) / 2 - margin)

  // Move No button randomly within the clamped range
  const randomX = Math.random() * 200 - 100
  const randomY = Math.random() * 200 - 100

  noPos.value = {
    x: clamp(randomX, -maxX, maxX),
    y: clamp(randomY, -maxY, maxY)
  }
  if (noTextIndex.value < noTexts.length - 1) {
    noTextIndex.value++
  } else {
    noTextIndex.value = 0
  }
  noBtnText.value = noTexts[noTextIndex.value]
}

const handleYes = async () => {
  // Simulate backend call
  try {
    // await $fetch('/api/response', { method: 'POST', body: { answer: 'yes' } })
  } catch (e) {
    console.error('Failed to send response to backend:', e)
  }

  accepted.value = true
  launchConfetti()
  setTimeout(() => {
    currentPage.value = 1 // Open book after slight delay
  }, 500)
}

// --- CONFETTI ---
const launchConfetti = () => {
  const duration = 3000;
  const animationEnd = Date.now() + duration;
  const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 2000 };
  const randomInRange = (min, max) => Math.random() * (max - min) + min;

  const interval = setInterval(function() {
    const timeLeft = animationEnd - Date.now();
    if (timeLeft <= 0) return clearInterval(interval);
    const particleCount = 50 * (timeLeft / duration);
    confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } });
    confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } });
  }, 250);
}

// --- BOOK NAVIGATION ---
const nextPage = () => {
  if (currentPage.value < totalPages) currentPage.value++
}
const prevPage = () => {
  if (currentPage.value > 0) currentPage.value--
}

// --- MINI GAME: MATCH PAIRS ---
const gameStarted = ref(false)
const cards = ref([])
const flippedCards = ref([])
const matchedPairs = ref(0)
const gameWon = ref(false)

const emojis = ['💝', '🌹', '🧸', '🍫', '✨', '🎀']

const initGame = () => {
  gameStarted.value = true
  matchedPairs.value = 0
  gameWon.value = false
  flippedCards.value = []

  // Create pairs
  cards.value = [...emojis, ...emojis]
      .sort(() => Math.random() - 0.5)
      .map((emoji, index) => ({
        id: index,
        emoji,
        isFlipped: false,
        isMatched: false
      }))
}

const handleCardClick = (card) => {
  if (card.isFlipped || card.isMatched || flippedCards.value.length >= 2) return

  card.isFlipped = true
  flippedCards.value.push(card)

  if (flippedCards.value.length === 2) {
    const [c1, c2] = flippedCards.value
    if (c1.emoji === c2.emoji) {
      // Match!
      c1.isMatched = true
      c2.isMatched = true
      matchedPairs.value++
      flippedCards.value = []
      if (matchedPairs.value === emojis.length) {
        setTimeout(() => {
            gameWon.value = true
            launchConfetti()
        }, 500)
      }
    } else {
      // No match
      setTimeout(() => {
        c1.isFlipped = false
        c2.isFlipped = false
        flippedCards.value = []
      }, 1000)
    }
  }
}

// Init game when page 3 is opened
watch(currentPage, (val) => {
  if (val === 3 && !gameStarted.value) {
    initGame()
  }
})

const getZIndex = (pageIndex) => {
  // If page is flipped (current page > page index), it goes to the left stack.
  // Left stack: higher index = higher z-index (on top).
  // Right stack: lower index = higher z-index (on top).
  return currentPage.value > pageIndex ? pageIndex : (10 - pageIndex)
}
</script>

<template>
  <div class="scene">
    <!-- Floating Decisions Layer -->
    <div class="decision-overlay" :class="{ 'fade-out': accepted }">
      <h1 class="main-title" v-if="!accepted">Will you be my Valentine?</h1>
      <div class="buttons-container" v-if="!accepted">
        <button
          class="btn yes-btn"
          @click="handleYes"
          :style="{ transform: `scale(${yesScale})` }"
        >
          Да! ❤️
        </button>
        <button
          class="btn no-btn"
          @click="handleNo"
          :style="{ transform: `translate(${noPos.x}px, ${noPos.y}px)` }"
        >
          {{ noBtnText }}
        </button>
      </div>
    </div>

    <!-- The 3D Book -->
    <div class="book-container">
      <div class="book" :class="{ 'book-open': currentPage > 0 }">

        <!-- COVER -->
        <div
          class="page cover"
          :class="{ 'flipped': currentPage > 0 }"
          :style="{ zIndex: getZIndex(0) }"
          @click="currentPage === 0 ? nextPage() : null"
        >
          <div class="front">
            <div class="cover-design">
              <span class="cover-text">Our Story</span>
              <div class="heart-shape">❤️</div>
              <span class="tap-hint">Нажми, чтобы открыть</span>
            </div>
          </div>
          <div class="back">
             <!-- Inside Front Cover -->
             <div class="paper-texture"></div>
          </div>
        </div>

        <!-- PAGE 1: INTRO -->
        <div
          class="page page-1"
          :class="{ 'flipped': currentPage > 1 }"
          :style="{ zIndex: getZIndex(1) }"
        >
          <div class="front">
            <div class="content text-page">
              <h2>My Dearest,</h2>
              <p>
                Я так долго ждал момента, чтобы сказать тебе это.
                Ты наполнила мою жизнь светом и теплом.
                Каждый момент с тобой — это магия.
              </p>
              <p>
                Я обещаю быть твоей поддержкой, твоей радостью
                и тем, кто всегда приносит шоколадки. 🍫
              </p>
              <div class="nav-hint" @click="nextPage">Далее ➡️</div>
            </div>
          </div>
          <div class="back">
            <!-- Back of Page 1 (Left side of spread 2) -->
             <div class="content photo-page">
               <h3>Memories ✨</h3>
               <div class="polaroids">
                 <div class="polaroid p1">
                   <div class="img-box">
                      <!-- Placeholders -->
                      <img src="https://placehold.co/150x150/ffced9/d81b60?text=Photo+1" alt="Us">
                   </div>
                   <span>First Date</span>
                 </div>
                 <div class="polaroid p2">
                    <div class="img-box">
                      <img src="https://placehold.co/150x150/ffced9/d81b60?text=Photo+2" alt="Us">
                    </div>
                   <span>Silly Fits</span>
                 </div>
               </div>
             </div>
          </div>
        </div>

        <!-- PAGE 2: GALLERY/MORE TEXT -->
        <div
          class="page page-2"
          :class="{ 'flipped': currentPage > 2 }"
          :style="{ zIndex: getZIndex(2) }"
        >
          <div class="front">
            <!-- Front of Page 2 (Right side of spread 2) -->
             <div class="content photo-page-2">
                <div class="big-photo">
                   <img src="https://placehold.co/250x200/ffced9/d81b60?text=Couple+Goal" alt="Big Photo">
                   <span>Best Travel 🌍</span>
                </div>
                <p class="love-note">
                  "В тебе я нашел всё, что искал."
                </p>
                <div class="nav-actions">
                  <button class="small-btn" @click="prevPage">⬅️ Back</button>
                  <button class="small-btn" @click="nextPage">Game ➡️</button>
                </div>
             </div>
          </div>
          <div class="back">
            <!-- Back of Page 2 (Left side of spread 3) -->
            <div class="content game-intro">
               <h3>Love Match!</h3>
               <p>Найди все пары, чтобы выиграть мое сердце ❤️</p>
               <div class="score">Pairs found: {{ matchedPairs }} / 6</div>
               <button class="small-btn" v-if="gameWon" @click="initGame">Play Again 🔄</button>
            </div>
          </div>
        </div>

        <!-- PAGE 3: GAME -->
        <div
          class="page page-3"
          style="z-index: 7;"
        >
          <div class="front">
             <div class="content game-board">
                <div class="grid" :class="{ 'winner': gameWon }">
                  <div
                    v-for="card in cards"
                    :key="card.id"
                    class="card-container"
                    @click="handleCardClick(card)"
                  >
                    <div class="card" :class="{ 'is-flipped': card.isFlipped || card.isMatched }">
                      <div class="card-front">❓</div>
                      <div class="card-back">{{ card.emoji }}</div>
                    </div>
                  </div>
                </div>
                <div class="nav-actions bottom">
                  <button class="small-btn" @click="prevPage">⬅️ Back</button>
                </div>
             </div>
          </div>
          <div class="back"></div> <!-- Last page back is empty/cover back -->
        </div>

      </div>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Dancing+Script:wght@700&family=Nunito:wght@400;600;800&display=swap');

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background: #201e21; /* Dark elegant background */
  font-family: 'Nunito', sans-serif;
  overflow: hidden;
}

.scene {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1500px;
  background-image: radial-gradient(circle at center, #3a2e3a 0%, #1a151a 100%);
}

/* --- DECISION LAYER --- */
.decision-overlay {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: Center;
  transition: opacity 1s ease, pointer-events 1s step-end;
}

.decision-overlay.fade-out {
  opacity: 0;
  pointer-events: none;
}

.main-title {
  color: #fff;
  font-family: 'Dancing Script', cursive;
  font-size: 4rem;
  margin-bottom: 2rem;
  text-shadow: 0 4px 10px rgba(216, 27, 96, 0.5);
  text-align: center;
}

.buttons-container {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.btn {
  padding: 15px 40px;
  font-size: 1.5rem;
  border-radius: 50px;
  border: none;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  font-weight: 800;
}

.yes-btn {
  background: #d81b60;
  color: white;
  box-shadow: 0 10px 20px rgba(216, 27, 96, 0.4);
}

.yes-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 15px 30px rgba(216, 27, 96, 0.6);
}

.no-btn {
  background: #fff;
  color: #333;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
}

/* --- BOOK 3D --- */
.book-container {
  width: 400px; /* Single page width */
  height: 550px;
  position: relative;
  /* Shift whole container left when open to center the spread */
  transition: transform 1s ease-in-out;
}
/* When book is open (page > 0), we can shift container if we want,
   but simplistic approach: Keep it centered, it opens to right. */

.book {
  width: 100%;
  height: 100%;
  position: relative;
  transform-style: preserve-3d;
}

.page {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  transform-origin: left; /* Hinge on left */
  transform-style: preserve-3d;
  transition: transform 1.2s cubic-bezier(0.645, 0.045, 0.355, 1);
}

.page.flipped {
  transform: rotateY(-180deg);
}

.front, .back {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  backface-visibility: hidden;
  border-radius: 5px 15px 15px 5px;
  background-color: #fff9f0; /* Paper color */
  box-shadow: inset 5px 0 10px rgba(0,0,0,0.05);
  overflow: hidden;
}

.back {
  transform: rotateY(180deg);
  border-radius: 15px 5px 5px 15px; /* Mirrored */
  box-shadow: inset -5px 0 10px rgba(0,0,0,0.05);
}

/* --- PAGE CONTENTS --- */
.cover .front {
  background: linear-gradient(45deg, #7b1fa2, #e91e63);
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #4a148c;
}
.cover-design {
  text-align: center;
  color: white;
}
.cover-text {
  display: block;
  font-family: 'Dancing Script', cursive;
  font-size: 3rem;
}
.heart-shape {
  font-size: 5rem;
  margin: 20px 0;
  animation: pulse 2s infinite;
}
.tap-hint {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-top: 20px;
  display: block;
}

.content {
  padding: 30px;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: #4e342e;
}

.text-page h2 {
  font-family: 'Dancing Script', cursive;
  color: #d81b60;
  font-size: 2.5rem;
}

.text-page p {
  font-size: 1.1rem;
  line-height: 1.6;
  margin-bottom: 20px;
  text-align: justify;
}

.polaroids {
  margin-top: 20px;
  display: flex;
  flex-direction: column;
  gap: 30px;
}
.polaroid {
  background: white;
  padding: 10px 10px 30px 10px;
  box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
  transform: rotate(-5deg);
  transition: transform 0.3s;
}
.polaroid:hover { transform: scale(1.05) rotate(0deg); z-index: 10; }
.polaroid.p2 { transform: rotate(3deg); }
.img-box img {
    width: 100%;
    height: auto;
    display: block;
}
.polaroid span {
  font-family: 'Dancing Script', cursive;
  font-size: 1.2rem;
  margin-top: 5px;
  display: block;
}

.small-btn {
  background: none;
  border: 1px solid #d81b60;
  color: #d81b60;
  padding: 5px 15px;
  border-radius: 20px;
  cursor: pointer;
  margin-top: 20px;
  font-family: 'Nunito', sans-serif;
  transition: all 0.2s;
}
.small-btn:hover {
  background: #d81b60;
  color: white;
}
.nav-actions {
  margin-top: auto;
  display: flex;
  gap: 10px;
}

/* --- GAME --- */
.game-board {
  padding: 15px;
  justify-content: flex-start;
}
.grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  width: 100%;
  margin-top: 20px;
}
.card-container {
  aspect-ratio: 3/4;
  perspective: 100px;
}
.card {
  width: 100%;
  height: 100%;
  position: relative;
  transition: transform 0.6s;
  transform-style: preserve-3d;
  cursor: pointer;
  box-shadow: 0 4px 6px rgba(0,0,0,0.1);
  border-radius: 8px;
}
.card.is-flipped {
  transform: rotateY(180deg);
}
.card-front, .card-back {
  position: absolute;
  width: 100%;
  height: 100%;
  backface-visibility: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  border-radius: 8px;
}
.card-front {
  background: #ffecb3;
  color: #ff6f00;
}
.card-back {
  background: white;
  transform: rotateY(180deg);
  border: 2px solid #ffecb3;
}
.winner .card-back {
  background: #d4edda;
  border-color: #c3e6cb;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

/* Mobile adjustments */
@media (max-width: 600px) {
  .book-container {
    width: 90vw;
    height: 70vh;
  }
  .main-title { font-size: 2.5rem; }
  .btn { padding: 10px 20px; font-size: 1.2rem; }
}
</style>