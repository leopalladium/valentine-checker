<script setup>
import { ref } from 'vue'
import confetti from 'canvas-confetti'

const accepted = ref(false)
const currentPage = ref(0) // 0 = Cover, 1 = Intro, 2 = Gallery, 3 = Quiz, 4 = Letter
const totalPages = 4

// --- TIMELINE DATA ---
const timelineEvents = [
  { date: 'First Hello', title: 'Start of Us', desc: 'The day our worlds collided.' },
  { date: '14 Feb', title: 'First Valentine', desc: 'Simple, sweet, and unforgettable.' },
  { date: 'Summer', title: 'Adventures', desc: 'Sunsets, road trips, and laughter.' },
  { date: 'Today', title: 'Forever', desc: 'Writing our next chapter...' }
]
const activeEventIndex = ref(0)
const selectEvent = (index) => {
  activeEventIndex.value = index
}

// --- LETTER OVERLAY ---
const showLetter = ref(false)
const closeLetter = () => {
  showLetter.value = false
}
const openLetter = () => {
  showLetter.value = true
  launchConfetti()
}

// --- YES/NO BUTTON LOGIC ---
const noTexts = [
  "Нет", "Ты уверена?", "Подумай еще!", "Не разбивай мне сердце 💔",
  "Я буду плакать...", "Ну пожалуйста?", "Ладно, я понял...", "Шутка! Жми ДА! ❤️"
]
const noTextIndex = ref(0)
const noBtnText = ref(noTexts[0])
const yesScale = ref(1)
const noPos = ref({ x: 0, y: 0 })

const clamp = (value, min, max) => Math.min(Math.max(value, min), max)

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

// --- QUIZ LOGIC ---
const quizStarted = ref(false)
const currentQuestion = ref(0)
const quizScore = ref(0)
const quizCompleted = ref(false)

const questions = [
  {
    q: "Where was our first date?",
    options: ["Cinema", "Park", "Cafe", "Moon"],
    correct: 1 // Index of correct answer
  },
  {
    q: "What is my favorite food?",
    options: ["Pizza", "Sushi", "Burgers", "You"],
    correct: 1
  },
  {
    q: "Who said 'I love you' first?",
    options: ["Me", "You", "Both at once", "My cat"],
    correct: 0
  }
]

const handleAnswer = (index) => {
  if (index === questions[currentQuestion.value].correct) {
    quizScore.value++
  }

  if (currentQuestion.value < questions.length - 1) {
    currentQuestion.value++
  } else {
    quizCompleted.value = true
    launchConfetti()
  }
}

const restartQuiz = () => {
  quizStarted.value = true
  currentQuestion.value = 0
  quizScore.value = 0
  quizCompleted.value = false
}

// --- Z-INDEX LOGIC ---
const getZIndex = (pageIndex) => {
  // If page is flipped (current page > page index), it goes to the left stack.
  // Left stack: higher index = higher z-index (on top).
  // Right stack: lower index = higher z-index (on top).
  return currentPage.value > pageIndex ? pageIndex : (10 - pageIndex)
}
</script>

<template>
  <div class="scene">
    <!-- Letter Overlay -->
    <div v-if="showLetter" class="letter-overlay" @click.self="closeLetter">
      <div class="letter-paper">
        <button class="close-btn" @click="closeLetter">✖</button>
        <h2>My Promise to You</h2>
        <p>
          More than anything, I want you to know how much you mean to me.
          Wait, I have more to say...
        </p>
        <p>
          Every day with you is a new adventure. I love your smile, your laugh,
          and even the way you steal my hoodies. You are my person.
        </p>
        <p class="sign">With all my love,<br>Your Valentine ❤️</p>
      </div>
    </div>

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
    <div class="book-container" :class="{ 'shifted': currentPage > 0 }">
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
              <h2>Дорогая Аня,</h2>
              <p>
                Я так долго ждал момента, чтобы сказать тебе это.
                Ты наполнила мою жизнь светом и теплом.
                Каждый момент с тобой — это настоящее чудо.
              </p>
              <p>
                Я обещаю быть твоей поддержкой, твоей радостью
                и тем, кто будет рядом и всегда приносит шоколадки. 🍫
              </p>
              <div class="nav-actions">
                <button class="small-btn" @click="nextPage">Далее ➡️</button>
              </div>
            </div>
          </div>
          <div class="back">
            <!-- Back of Page 1 (Left side of spread 2) - TIMELINE -->
             <div class="content timeline-page">
               <h3>Our Timeline ⏳</h3>
               <div class="timeline">
                 <div
                   v-for="(event, index) in timelineEvents"
                   :key="index"
                   class="timeline-item"
                   :class="{ 'active': activeEventIndex === index }"
                   @click="selectEvent(index)"
                 >
                   <div class="point"></div>
                   <div class="date-label">{{ event.date }}</div>
                 </div>
               </div>
               <div class="event-details">
                 <h4>{{ timelineEvents[activeEventIndex].title }}</h4>
                 <p>{{ timelineEvents[activeEventIndex].desc }}</p>
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
            <!-- Front of Page 2 (Right side of spread 2) - GALLERY -->
             <div class="content photo-page-2">
                <div class="photo-grid">
                  <div class="polaroid small-p">
                    <div class="img-box">
                      <img src="https://placehold.co/100x100/ffced9/d81b60?text=Us" alt="Pic">
                    </div>
                  </div>
                  <div class="polaroid small-p">
                    <div class="img-box">
                      <img src="https://placehold.co/100x100/ffced9/d81b60?text=Cute" alt="Pic">
                    </div>
                  </div>
                   <div class="big-photo">
                      <img src="https://placehold.co/200x150/ffced9/d81b60?text=Travel" alt="Big Photo">
                   </div>
                </div>
                <p class="love-note">
                  "Collection of our happiest moments."
                </p>
                <div class="nav-actions">
                  <button class="small-btn" @click="prevPage">⬅️ Back</button>
                  <button class="small-btn" @click="nextPage">Quiz ➡️</button>
                </div>
             </div>
          </div>
          <div class="back">
            <!-- Back of Page 2 (Left side of spread 3) -->
            <div class="content quiz-intro">
               <h3>Couple Quiz! 🧠</h3>
               <p>How well do you know us?</p>
               <p v-if="!quizStarted">Answer correct to match our vibe!</p>

               <div v-if="!quizStarted" class="start-quiz-box">
                 <button class="small-btn" @click="restartQuiz">Start Quiz ▶️</button>
               </div>

               <button class="small-btn" v-if="quizCompleted" @click="nextPage">See Prize ➡️</button>
            </div>
          </div>
        </div>

        <!-- PAGE 3: QUIZ -->
        <div
          class="page page-3"
          :class="{ 'flipped': currentPage > 3 }"
          :style="{ zIndex: getZIndex(3) }"
        >
          <div class="front">
             <div class="content quiz-board">
                <div v-if="quizStarted && !quizCompleted" class="question-container">
                  <h4>Question {{ currentQuestion + 1 }}/{{ questions.length }}</h4>
                  <p class="q-text">{{ questions[currentQuestion].q }}</p>
                  <div class="options">
                    <button
                      v-for="(opt, idx) in questions[currentQuestion].options"
                      :key="idx"
                      class="option-btn"
                      @click="handleAnswer(idx)"
                    >
                      {{ opt }}
                    </button>
                  </div>
                </div>

                <div v-else-if="quizCompleted" class="quiz-result">
                  <h3>Quiz Done! 🎉</h3>
                  <p>You scored {{ quizScore }} / {{ questions.length }}</p>
                  <p v-if="quizScore === questions.length">Perfect Match! ❤️</p>
                  <p v-else>Good enough for me! 😘</p>
                  <div class="nav-actions">
                     <button class="small-btn" @click="restartQuiz">Retry 🔄</button>
                     <button class="small-btn" @click="nextPage">My Note ➡️</button>
                  </div>
                </div>

                <div v-else class="waiting-state">
                   <p>Click "Start Quiz" on the left page!</p>
                </div>

                <div class="nav-actions bottom" v-if="!quizCompleted">
                    <button class="small-btn" @click="prevPage">⬅️ Back</button>
                </div>
             </div>
          </div>
          <div class="back">
             <!-- Back of Page 3 (Left side of spread 4) - Final decor -->
             <div class="content final-decor">
               <h3>Just for you...</h3>
               <div class="decor-heart">💌</div>
             </div>
          </div>
        </div>

        <!-- PAGE 4: LETTER -->
        <div
          class="page page-4"
          style="z-index: 6;"
        >
          <div class="front">
             <div class="content letter-page">
                <h3>Read Me</h3>
                <div class="envelope-container" @click="openLetter">
                   <div class="envelope">
                     <div class="envelope-flap"></div>
                     <div class="envelope-pocket"></div>
                     <div class="envelope-letter"></div>
                   </div>
                   <span class="click-hint">Click to open 👆</span>
                </div>
                <div class="nav-actions bottom">
                  <button class="small-btn" @click="prevPage">⬅️ Back</button>
                </div>
             </div>
          </div>
          <div class="back"></div>
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
  font-size: 2.5rem; /* Reduced from 4rem */
  margin-bottom: 35vh;
  text-shadow: 0 4px 10px rgba(216, 27, 96, 0.5);
  text-align: center;
  pointer-events: none; /* Let clicks pass through if overlapping (though margin keeps it away) */
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
  z-index: 10;
  position: relative;
}

.yes-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 15px 30px rgba(216, 27, 96, 0.6);
}

.no-btn {
  background: #fff;
  color: #333;
  box-shadow: 0 5px 15px rgba(0,0,0,0.2);
  z-index: 1;
  position: relative;
}

/* --- BOOK 3D --- */
.book-container {
  width: 400px; /* Single page width */
  height: 550px;
  position: relative;
  /* Shift whole container right when open to center the spread */
  transition: transform 1s ease-in-out, width 0.5s, height 0.5s;
}

.book-container.shifted {
  /* Shift right by 50% of width so the spine is at center */
  transform: translateX(50%);
}

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
  padding: 10px; /* Added padding to prevent overflow */
}
.cover-design {
  text-align: center;
  color: white;
  width: 100%;
}

.heart-shape {
  font-size: 3rem; /* Reduced from 4rem */
  margin: 15px 0;
  animation: pulse 2s infinite;
}
.tap-hint {
  font-size: 0.9rem;
  opacity: 0.8;
  margin-top: 20px;
  display: block;
}

.content {
  padding: 20px;
  height: 100%;
  box-sizing: border-box;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  color: #4e342e;
  overflow-y: auto;
  scrollbar-width: none;
}
.content::-webkit-scrollbar {
  display: none;
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

/* Timeline Styles */
.timeline-page {
  display: flex;
  flex-direction: column;
}
.timeline {
  display: flex;
  justify-content: space-between;
  margin: 20px 0;
  width: 100%;
  position: relative;
}
.timeline::before {
  content: '';
  position: absolute;
  top: 10px; /* Align with dots */
  left: 0;
  width: 100%;
  height: 2px;
  background: #ff80ab;
  z-index: 0;
}
.timeline-item {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  flex: 1;
}
.point {
  width: 20px;
  height: 20px;
  background: #fff;
  border: 3px solid #d81b60;
  border-radius: 50%;
  transition: all 0.3s;
}
.date-label {
  font-size: 0.8rem;
  margin-top: 5px;
  font-weight: bold;
  opacity: 0.7;
}
.timeline-item.active .point {
  background: #d81b60;
  transform: scale(1.3);
}
.timeline-item.active .date-label {
  color: #d81b60;
  opacity: 1;
}
.event-details {
  background: #fff0f6;
  padding: 15px;
  border-radius: 10px;
  margin-top: 10px;
  border: 1px dashed #d81b60;
  min-height: 100px;
  transition: all 0.3s ease;
}
.event-details h4 {
  margin: 0 0 10px 0;
  color: #c2185b;
  font-family: 'Dancing Script', cursive;
  font-size: 1.5rem;
}

.photo-grid {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
  margin-bottom: 15px;
}
.small-p {
  width: 80px;
  padding: 5px 5px 20px 5px;
  transform: rotate(-5deg);
}
.small-p:nth-child(2) { transform: rotate(5deg); }

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

/* --- QUIZ STYLES */
.quiz-board {
  justify-content: center;
}
.question-container {
  width: 100%;
}
.q-text {
  font-size: 1.2rem;
  font-weight: bold;
  margin: 15px 0;
}
.options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.option-btn {
  background: white;
  border: 1px solid #d81b60;
  padding: 10px;
  border-radius: 8px;
  color: #c2185b;
  cursor: pointer;
  font-family: 'Nunito', sans-serif;
  transition: all 0.2s;
}
.option-btn:hover {
  background: #fce4ec;
  transform: translateX(5px);
}

/* ENVELOPE STYLES */
.envelope-container {
  cursor: pointer;
  margin-top: 30px;
  transition: transform 0.3s;
}
.envelope-container:hover {
  transform: scale(1.1);
}
.envelope {
  width: 120px;
  height: 80px;
  background: #ef5350;
  position: relative;
  display: inline-block;
  border-bottom-left-radius: 5px;
  border-bottom-right-radius: 5px;
}
.envelope-flap {
  position: absolute;
  top: 0;
  left: 0;
  width: 0;
  height: 0;
  border-left: 60px solid transparent;
  border-right: 60px solid transparent;
  border-top: 40px solid #e53935;
  transform-origin: top;
  z-index: 2;
}
.envelope-pocket {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 0;
  height: 0;
  border-left: 60px solid #e57373;
  border-right: 60px solid #ef9a9a;
  border-bottom: 40px solid #ef5350;
  border-top: 40px solid transparent;
  z-index: 1;
}
.click-hint {
  display: block;
  margin-top: 15px;
  font-size: 0.9rem;
  color: #880e4f;
  animation: bounce 1s infinite;
}

/* LETTER OVERLAY */
.letter-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0,0,0,0.8);
  z-index: 5000;
  display: flex;
  justify-content: center;
  align-items: center;
  backdrop-filter: blur(5px);
  padding: 20px;
}
.letter-paper {
  background: #fffbf0;
  width: 100%;
  max-width: 500px;
  padding: 40px;
  border-radius: 5px;
  box-shadow: 0 0 20px rgba(255, 255, 255, 0.2);
  position: relative;
  text-align: left;
  font-family: 'Dancing Script', cursive;
  font-size: 1.5rem;
  line-height: 1.6;
  color: #4e342e;
  transform: rotate(-1deg);
}
.letter-paper h2 {
  text-align: center;
  margin-top: 0;
  color: #d81b60;
}
.close-btn {
  position: absolute;
  top: 10px;
  right: 15px;
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: #aaa;
}
.sign {
  margin-top: 30px;
  text-align: right;
  font-weight: bold;
}

@keyframes pulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.2); }
  100% { transform: scale(1); }
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

/* Mobile adjustments */
@media (max-width: 768px) {
  .book-container {
    width: 45vw; /* Spread will be 90vw */
    height: 60vh;
  }

  .book-container.shifted {
    transform: translateX(50%);
  }

  .main-title { font-size: 1.8rem; }
  .btn { padding: 10px 20px; font-size: 1.2rem; }

  /* Responsive Content */
  .cover-text { font-size: 1.5rem; } /* Reduced from 1.8rem */
  .heart-shape { font-size: 2.5rem; }

  .letter-paper { padding: 20px; font-size: 1.2rem; }
}

@media (max-width: 480px) {
  .book-container { height: 55vh; }
  .main-title { font-size: 1.5rem; }
}
</style>

