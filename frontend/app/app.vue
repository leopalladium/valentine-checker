<script setup>
import { ref, watch } from 'vue'
import confetti from 'canvas-confetti'

const showDisclaimer = ref(true) // Disclaimer state
const accepted = ref(false)
const currentPage = ref(0) // 0 = Cover, 1 = Intro, 2 = Gallery, 3 = Quiz, 4 = Letter
const totalPages = 4

// --- TIMELINE DATA ---
const timelineEvents = [
  { date: 'Первый привет', title: '27 июня 2025', desc: 'День, когда мы встретились с тобой.' },
  { date: 'Наше лето', title: 'Мы ещё не знали', desc: 'Помнишь как мы говорили, что не хотим отношений? Я тоже помню, до сих пор смешно.' },
  { date: '13 октября ', title: 'Теперь мы встречаемся', desc: 'Мы прошли через многое и решили стать парой.' },
  { date: 'Сегодня', title: 'Вместе и навсегда', desc: 'Представь, четыре месяца и один день как пара. Давай мы вместе напишем следующую главу...' }
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

const acceptDisclaimer = () => {
  showDisclaimer.value = false
}

// --- YES/NO BUTTON LOGIC ---
const noTexts = [
  "No", "Ты уверена?", "Подумай еще!", "Не разбивай мне сердце 💔",
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
    q: "Когда мы познакомились?",
    options: ["27 июня", "12 июля", "27 июля", "23 мая"],
    correct: 0 // Index of correct answer
  },
  {
    q: "Какое моё любимое блюдо?",
    options: ["Пицца", "Šťouchané brambory", "Лапша", "Ты"],
    correct: 3
  },
  {
    q: "Кто первый признался в своих чувствах?",
    options: ["Я", "Ты", "Одновременно", "Никто не признавался"],
    correct: [0, 2, 3]
  }
]

const handleAnswer = (index) => {
  const question = questions[currentQuestion.value]
  const isCorrect = Array.isArray(question.correct)
      ? question.correct.includes(index)
      : index === question.correct

  if (isCorrect) {
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

// --- SWIPE SUPPORT ---
const touchStartX = ref(0)
const touchEndX = ref(0)

const handleTouchStart = (e) => {
  touchStartX.value = e.changedTouches[0].screenX
}

const handleTouchEnd = (e) => {
  touchEndX.value = e.changedTouches[0].screenX
  handleSwipe()
}

const handleSwipe = () => {
  if (!accepted.value) return // Don't swipe if not accepted yet
  const threshold = 50
  if (touchEndX.value < touchStartX.value - threshold) {
    nextPage()
  }
  if (touchEndX.value > touchStartX.value + threshold) {
    prevPage()
  }
}

// Reactivate animations when page changes
const pageAnimStates = ref([true, false, false, false, false]) // Cover + 4 pages
watch(currentPage, (val) => {
   // Reset others
   pageAnimStates.value = pageAnimStates.value.map(() => false)
   // trigger animation for new page after flip duration
   setTimeout(() => {
     pageAnimStates.value[val] = true
   }, 600) // Halfway through flip
})

// --- Z-INDEX LOGIC ---
const getZIndex = (pageIndex) => {
  // If page is flipped (current page > page index), it goes to the left stack.
  // Left stack: higher index = higher z-index (on top).
  // Right stack: lower index = higher z-index (on top).
  return currentPage.value > pageIndex ? pageIndex : (10 - pageIndex)
}
</script>

<template>
  <div class="scene" @touchstart="handleTouchStart" @touchend="handleTouchEnd">
    <!-- Background Particles (CSS only simple decorative elements) -->
    <div class="bg-hearts">
      <div class="bg-heart" v-for="n in 10" :key="n" :style="{ left: Math.random()*100 + '%', animationDelay: Math.random()*5 + 's' }">❤️</div>
    </div>

    <!-- Letter Overlay -->
    <div v-if="showLetter" class="letter-overlay" @click.self="closeLetter">
      <div class="letter-paper">
        <button class="close-btn" @click="closeLetter">✖</button>
        <h2>Самой лучшей девушке в этом мире</h2>
        <p>
          Больше всего хочется сказать тебе, что ты не представляешь сколько ты значишь для меня. Ты — это свет в моих днях, улыбка на моем лице и тепло в моем сердце. Я благодарен судьбе за каждый момент, который мы провели вместе.
          Хотя, мне хочется сказать ещё кое-что...
        </p>
        <p>
          Каждый день с тобой — это приключение, и я не могу дождаться, чтобы продолжать
          исследовать этот мир вместе.
          Ты - моё вдохновение, моя поддержка и моя любовь.
          Я обещаю всегда быть рядом, поддерживать тебя и любить всем сердцем.
        </p>
        <p>P.S. Помнишь, я тебе говорил, где лежит что-то маленькое, что я для тебя приготовил? Сейчас тот момент, когда стоит это взять</p>
        <p class="sign">С любовью,<br>Навеки твой <br>Клим ❤️</p>
      </div>
    </div>

    <!-- Disclaimer Overlay -->
    <div v-if="showDisclaimer" class="disclaimer-overlay">
      <div class="disclaimer-content">
        <p>Кажется ты начала что-то подозревать, я добавляю это сообщение в час ночи 14 февраля, надеюсь тебе понравится.</p>
        <button class="accept-btn" @click="acceptDisclaimer">Okay let's go</button>
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
          Yes! ❤️
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
            <div class="content text-page" :class="{ 'animate-in': pageAnimStates[1] }">
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
              <!-- Internal Nav Removed for Cleaner Look on Desktop, Swipe/Click works -->
              <div class="mobile-hint">Swipe to turn ➡️</div>
            </div>
          </div>
          <div class="back">
            <!-- Back of Page 1 (Left side of spread 2) - TIMELINE -->
             <div class="content timeline-page" :class="{ 'animate-in': pageAnimStates[2] }">
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
             <div class="content photo-page-2" :class="{ 'animate-in': pageAnimStates[2] }">
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
             </div>
          </div>
          <div class="back">
            <!-- Back of Page 2 (Left side of spread 3) -->
            <div class="content quiz-intro" :class="{ 'animate-in': pageAnimStates[3] }">
               <h3>Парный квиз! 🧠</h3>
               <p>Как хорошо ты знаешь нас?</p>
               <p v-if="!quizStarted">Отвечай и не подглядывай!</p>

               <div v-if="!quizStarted" class="start-quiz-box">
                 <button class="small-btn" @click="restartQuiz">Начать квиз ▶️</button>
               </div>

               <div class="score" v-if="quizCompleted">Умничка! 🏆</div>
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
             <div class="content quiz-board" :class="{ 'animate-in': pageAnimStates[3] }">
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
                  <p>Результат {{ quizScore }} / {{ questions.length }}</p>
                  <p v-if="quizScore === questions.length">Идеально! ❤️</p>
                  <p v-else>Ты хорошо справилась! 😘</p>
                  <div class="nav-actions">
                     <button class="small-btn" @click="restartQuiz">Ещё раз 🔄</button>
                     <button class="small-btn" @click="nextPage">Дальше ➡️</button>
                  </div>
                </div>

                <div v-else class="waiting-state">
                   <p>Тыкни "Начать квиз" на странице слева!</p>
                </div>
             </div>
          </div>
          <div class="back">
             <!-- Back of Page 3 (Left side of spread 4) - Final decor -->
             <div class="content final-decor" :class="{ 'animate-in': pageAnimStates[4] }">
               <h3>Только для тебя...</h3>
               <div class="decor-heart">💌</div>
               <p>Открой письмо, оно справа...</p>
             </div>
          </div>
        </div>

        <!-- PAGE 4: LETTER (Redesigned as Moleskine Pocket) -->
        <div
          class="page page-4"
          style="z-index: 6;"
        >
          <div class="front">
             <div class="content pocket-container" @click="openLetter" :class="{ 'animate-in': pageAnimStates[4] }">
                <div class="letter-peek">
                   <div class="letter-text">Самой лучшей девушке...</div>
                </div>
                <div class="moleskine-pocket">
                   <span class="pocket-decor">Важные штуки 📂</span>
                </div>
                <span class="click-hint">Нажми, чтобы открыть</span>
             </div>
          </div>
          <div class="back"></div>
        </div>

      </div>
    </div>

    <!-- PC Navigation Controls (Under the book) -->
    <div class="pc-controls" v-if="accepted">
      <button class="nav-btn" @click="prevPage" :disabled="currentPage === 0">❮ Prev</button>
      <span class="page-indicator">{{ currentPage }} / {{ totalPages }}</span>
      <button class="nav-btn" @click="nextPage" :disabled="currentPage === totalPages">Next ❯</button>
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
  background: #201e21;
  font-family: 'Nunito', sans-serif;
  overflow: hidden;
}

.scene {
  width: 100vw;
  height: 100vh;
  display: flex;
  flex-direction: column; /* Stack controls below book on PC */
  justify-content: center;
  align-items: center;
  perspective: 1500px;
  /* Better Background */
  background: linear-gradient(135deg, #2b1022 0%, #4a192c 50%, #1a0b18 100%);
  position: relative;
  overflow: hidden;
}

/* Floating BG Hearts */
.bg-hearts {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  pointer-events: none;
  z-index: 0;
  overflow: hidden;
}
.bg-heart {
  position: absolute;
  bottom: -50px;
  font-size: 2rem;
  opacity: 0.1;
  animation: floatUp 10s infinite linear;
  color: #d81b60;
}

@keyframes floatUp {
  0% { transform: translateY(0) rotate(0deg); opacity: 0; }
  10% { opacity: 0.2; }
  90% { opacity: 0.2; }
  100% { transform: translateY(-110vh) rotate(360deg); opacity: 0; }
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

.polaroid {
  background: white;
  padding: 10px 10px 30px 10px;
  box-shadow: 2px 2px 8px rgba(0,0,0,0.2);
  transform: rotate(-5deg);
  transition: transform 0.3s;
}
.polaroid:hover { transform: scale(1.05) rotate(0deg); z-index: 10; }

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
  background: transparent;
  border: 2px solid #d81b60; /* Thicker border */
  color: #d81b60;
  padding: 8px 18px;
  border-radius: 25px; /* Match nav-btn radius */
  cursor: pointer;
  margin-top: 15px;
  font-family: 'Nunito', sans-serif;
  font-weight: 700; /* Bold text */
  transition: all 0.2s;
  box-shadow: 0 2px 5px rgba(216, 27, 96, 0.1);
}
.small-btn:hover {
  background: #d81b60;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(216, 27, 96, 0.3);
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

/* --- ANIMATIONS (Standardized) --- */
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
  max-height: 80vh; /* Limit height to 80% of viewport */
  overflow-y: auto; /* Enable vertical scrolling */
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
/* Custom scrollbar for letter */
.letter-paper::-webkit-scrollbar {
  width: 8px;
}
.letter-paper::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}
.letter-paper::-webkit-scrollbar-thumb {
  background: #d81b60;
  border-radius: 4px;
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

/* DISCLAIMER STYLES */
.disclaimer-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.9);
  z-index: 6000;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 20px;
  backdrop-filter: blur(8px);
}
.disclaimer-content {
  background: #fff;
  padding: 30px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
.accept-btn {
  margin-top: 20px;
  padding: 10px 20px;
  background: #d81b60;
  color: white;
  border: none;
  border-radius: 25px;
  cursor: pointer;
  font-size: 1.2rem;
  transition: background 0.3s;
}
.accept-btn:hover {
  background: #c2185b;
}

/* --- ANIMATIONS (Standardized) --- */
/* Default hidden state for content elements */
.content h2,
.content h3,
.content p,
.content .timeline,
.content .photo-grid,
.content .quiz-board > div,
.content .pocket-container > * {
  opacity: 0;
  transform: translateY(20px);
  transition: all 0.6s cubic-bezier(0.25, 0.46, 0.45, 0.94);
}

/* Active state when page is turned */
.animate-in h2,
.animate-in h3 { opacity: 1; transform: translateY(0); transition-delay: 0.1s; }
.animate-in p { opacity: 1; transform: translateY(0); transition-delay: 0.2s; }
.animate-in .timeline,
.animate-in .photo-grid { opacity: 1; transform: translateY(0); transition-delay: 0.3s; }
.animate-in .quiz-board > div { opacity: 1; transform: translateY(0); transition-delay: 0.2s; }
.animate-in .pocket-container > * { opacity: 1; transform: translateY(0); transition-delay: 0.3s; }

/* Timeline Item Interaction */
.timeline-item {
  transition: transform 0.2s;
}
.timeline-item:hover {
  transform: scale(1.1);
}

/* Button Standardization */
.small-btn {
  background: transparent;
  border: 2px solid #d81b60; /* Thicker border */
  color: #d81b60;
  padding: 8px 18px;
  border-radius: 25px; /* Match nav-btn radius */
  cursor: pointer;
  margin-top: 15px;
  font-family: 'Nunito', sans-serif;
  font-weight: 700; /* Bold text */
  transition: all 0.2s;
  box-shadow: 0 2px 5px rgba(216, 27, 96, 0.1);
}
.small-btn:hover {
  background: #d81b60;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(216, 27, 96, 0.3);
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

/* PC Controls */
.pc-controls {
  margin-top: 40px;
  display: flex;
  gap: 20px;
  align-items: center;
  z-index: 100;
  background: rgba(0,0,0,0.3);
  padding: 10px 20px;
  border-radius: 30px;
  backdrop-filter: blur(5px);
}
.nav-btn {
  background: transparent;
  border: 2px solid #ff80ab;
  color: #ff80ab;
  padding: 8px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-family: 'Nunito', sans-serif;
  font-weight: bold;
  transition: all 0.2s;
}
.nav-btn:hover:not(:disabled) {
  background: #ff80ab;
  color: white;
}
.nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
  border-color: #555;
  color: #555;
}
.page-indicator {
  color: rgba(255,255,255,0.7);
  font-family: 'Nunito', sans-serif;
}

/* Page Pocket Design (Moleskine Style) */
.pocket-container {
  width: 100%;
  height: 100%;
  position: relative;
  /* Page background is already inherited, but we make sure content aligns bottom */
  display: flex;
  justify-content: center;
  align-items: flex-end;
  overflow: hidden; /* IMPORTANT: Clip letter inside page */
  padding-bottom: 0 !important; /* Override generic padding */
}

.moleskine-pocket {
  width: 90%;
  height: 40%;
  background: #d7ccc8; /* Beige/Cardboard color */
  border-top: 1px solid #a1887f;
  border-radius: 5px 5px 0 0;
  position: absolute;
  bottom: 0;
  z-index: 20;
  box-shadow: 0 -3px 10px rgba(0,0,0,0.1);
  display: flex;
  justify-content: center;
  align-items: center;
}
.pocket-decor {
  font-family: 'Dancing Script', cursive;
  color: #5d4037;
  font-size: 1.2rem;
  opacity: 0.8;
}

.letter-peek {
  width: 85%;
  height: 50%; /* Taller than pocket so it peeks out */
  background: #fff;
  border: 1px solid #efebe9;
  position: absolute;
  bottom: 10px; /* Start inside pocket */
  z-index: 10;
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  box-shadow: 0 -2px 5px rgba(0,0,0,0.1);
  display: flex;
  justify-content: center;
  padding-top: 15px;
}
.letter-text {
  font-family: 'Dancing Script', cursive;
  font-size: 1.5rem;
  color: #d81b60;
}

/* Hover Effect for Desktop */
.pocket-container:hover .letter-peek {
  transform: translateY(-40px);
}

/* Mobile Hints */
.mobile-hint {
  display: none;
  font-size: 0.8rem;
  opacity: 0.6;
  margin-top: 10px;
  color: #d81b60;
}

/* --- MOBILE RESPONSIVENESS (АДАПТИВНОСТЬ) --- */
@media (max-width: 768px) {
  .pc-controls {
    display: none; /* Hide PC controls on mobile */
  }

  .mobile-hint {
    display: block; /* Show hint to swipe */
  }

  /* Adjust book size to fit mobile screen width using vmin for consistent ratio */
  .book-container {
    width: 43vmin; /* Keeps spread at 86vmin, safe for both portrait/landscape */
    height: 62vmin; /* Aspect ratio ~1.44 */
    /* Override pixel sizes */
  }

  /* Center the spine when book opens */
  .book-container.shifted {
    transform: translateX(50%);
  }

  /* Adjust title size and spacing for mobile */
  .main-title {
    font-size: 1.8rem;
    margin-bottom: 30vh; /* Slightly reduced gap on mobile to ensure buttons stay visible */
  }

  /* Larger buttons for touch targets */
  .btn {
    padding: 10px 20px;
    font-size: 1.2rem;
  }

  /* Resize heart on cover */
  .heart-shape { font-size: 2.5rem; }

  /* Adjust letter overlay padding */
  .letter-paper { padding: 20px; font-size: 1.2rem; }

  /* Stack buttons nicely if space is tight */
  .buttons-container {
    gap: 1.5rem;
  }

  /* --- FIXES FOR MOBILE CONTENT --- */

  /* Ensure scrolling works smoothly on touch devices */
  .content {
    -webkit-overflow-scrolling: touch;
    padding: 10px; /* More space for content */
  }

  /* Prevent buttons from being squashed or pushed out */
  .nav-actions {
     /* Hide internal nav actions on mobile if we have swipe,
        but maybe keep for Quiz/Game specifics */
     display: none;
  }

  /* Quiz/etc buttons that we WANT to keep */
  .quiz-intro .start-quiz-box, .quiz-result .nav-actions, .quiz-intro button {
     display: block;
  }

  .quiz-board .nav-actions {
    display: none; /* Hide "Back" on quiz page, use swipe */
  }

  .letter-page .nav-actions {
    display: none;
  }

  /* Adjust Photo Grid to be more flexible */
  .photo-grid {
    gap: 5px;
    margin-bottom: 10px;
  }

  .big-photo img {
    max-height: 100px; /* Limit height to save space */
  }

  .polaroid {
    padding: 5px;
  }

  .img-box img {
    max-width: 100%;
  }

  /* Allow text to scroll if needed */
  .text-page p {
    font-size: 0.85rem;
    line-height: 1.3;
  }
}

@media (max-width: 480px) {
  /* Smaller mobile devices layout tweaks */
  .book-container {
      /* Even safer on super small screens */
      width: 42vmin;
      height: 60vmin;
  }
  .main-title { font-size: 1.5rem; }
}
</style>

