<script setup>
import { ref } from 'vue'
// Если canvas-confetti вызывает ошибки при сборке, закомментируй импорт и функцию запуска
import confetti from 'canvas-confetti'

const yesSize = ref(1)
const isBookOpen = ref(false)

// Тексты для кнопки НЕТ
const noTexts = [
  "Нет", "Ты уверена?", "Подумай еще!", "Не разбивай мне сердце 💔",
  "Я буду плакать...", "Ну пожалуйста?", "Ладно, я понял...", "Шутка! Жми ДА! ❤️"
]
const noTextIndex = ref(0)
const noBtnText = ref(noTexts[0])

const handleNo = () => {
  yesSize.value *= 1.3
  if (noTextIndex.value < noTexts.length - 1) {
    noTextIndex.value++
  }
  noBtnText.value = noTexts[noTextIndex.value]
}

const handleYes = async () => {
  // 1. Отправляем запрос на бэкенд (тихо)
  try {
    // Используем runtimeConfig если настроен, или относительный путь через Nginx
    await $fetch('/api/response', { method: 'POST', body: { answer: 'yes' } })
  } catch (e) { console.error(e) }

  // 2. Открываем книгу
  isBookOpen.value = true

  // 3. Запускаем конфетти (если пакет установлен)
  if (typeof confetti === 'function') {
    launchConfetti()
  }
}

const launchConfetti = () => {
  const duration = 3000;
  const animationEnd = Date.now() + duration;
  const defaults = { startVelocity: 30, spread: 360, ticks: 60, zIndex: 2000 };

  const randomInRange = (min, max) => Math.random() * (max - min) + min;

  const interval = setInterval(function() {
    const timeLeft = animationEnd - Date.now();

    if (timeLeft <= 0) {
      return clearInterval(interval);
    }

    const particleCount = 50 * (timeLeft / duration);
    confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.1, 0.3), y: Math.random() - 0.2 } });
    confetti({ ...defaults, particleCount, origin: { x: randomInRange(0.7, 0.9), y: Math.random() - 0.2 } });
  }, 250);
}
</script>

<template>
  <div class="scene">
    <div class="book" :class="{ 'open': isBookOpen }">

      <div class="cover">
        <div class="front-content">
          <img src="https://media1.tenor.com/m/hnF3F7fbcowAAAAC/cat-jump.gif" class="cover-gif" />
          <h1 class="title">My Dearest...<br>Will you be my Valentine?</h1>

          <div class="buttons">
            <button
                class="btn yes-btn"
                @click.stop="handleYes"
                :style="{ transform: `scale(${yesSize})` }"
            >
              Да!
            </button>
            <button class="btn no-btn" @click.stop="handleNo">
              {{ noBtnText }}
            </button>
          </div>

          <div class="hint">Open this book to see my heart...</div>
        </div>
      </div>

      <div class="page paper">
        <div class="paper-content rotated-content">
          <h2>Ура! Я знал это! ❤️</h2>
          <p class="letter-text">
            Ты делаешь меня самым счастливым человеком!
            Я обещаю дарить тебе улыбки, обнимашки и вкусняшки.
            Спасибо, что ты есть у меня!
          </p>

          <div class="gallery">
            <div class="photo-frame rotate-left">
              <img src="/photo1.jpg" onError="this.src='https://placekitten.com/200/200'" alt="Us 1" />
              <span>Us ❤️</span>
            </div>
            <div class="photo-frame rotate-right">
              <img src="/photo2.jpg" onError="this.src='https://placekitten.com/201/201'" alt="Us 2" />
              <span>Memories</span>
            </div>
          </div>

          <p class="footer-love">With love,<br>Your Valentine</p>
        </div>
      </div>

    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Crimson+Text:ital,wght@0,400;0,700;1,600&display=swap');

html, body {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  background-color: #2c3e50;
  font-family: 'Crimson Text', serif;
  overflow: hidden;
}

.scene {
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  perspective: 1500px;
}

.book {
  width: 350px;
  height: 500px;
  position: relative;
  transform-style: preserve-3d;
  transition: transform 1.5s cubic-bezier(0.645, 0.045, 0.355, 1);
  box-shadow: 0 20px 50px rgba(0,0,0,0.5);
}

.book.open {
  transform: translateX(50%) rotateY(-180deg);
}

/* -- ОБЛОЖКА -- */
.cover {
  position: absolute;
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #d81b60 0%, #ad1457 100%);
  border-radius: 5px 15px 15px 5px;
  transform-origin: left;
  z-index: 2;
  /* backface-visibility: hidden; Убрали, чтобы кнопка исчезала через opacity */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  color: white;
  border: 2px solid #880e4f;
}

/* --- ИСПРАВЛЕНИЕ 1: Скрываем контент обложки при открытии --- */
.front-content {
  text-align: center;
  padding: 20px;
  transition: opacity 0.5s ease 0.2s; /* Исчезает с небольшой задержкой */
  /* Важно: чтобы гигантская кнопка не перекрывала все */
  transform-style: preserve-3d;
}

.book.open .front-content {
  opacity: 0;
  pointer-events: none; /* Чтобы нельзя было нажать на невидимую кнопку */
}
/* --------------------------------------------------------- */


.cover-gif {
  width: 150px;
  border-radius: 50%;
  border: 5px solid white;
  margin-bottom: 20px;
}

.title {
  font-size: 2rem;
  text-shadow: 1px 1px 3px rgba(0,0,0,0.3);
  margin-bottom: 30px;
}

.hint {
  margin-top: 40px;
  font-size: 0.9rem;
  opacity: 0.8;
  font-style: italic;
}

/* -- ВНУТРЕННЯЯ СТРАНИЦА -- */
.page {
  position: absolute;
  width: 100%;
  height: 100%;
  background-color: #fdfbf7;
  border-radius: 5px 15px 15px 5px;
  z-index: 1;
  box-shadow: inset 10px 0 20px rgba(0,0,0,0.05);
  display: flex;
  flex-direction: column;
  padding: 20px;
  box-sizing: border-box;
  /* Страница изначально повернута к нам спиной */
  transform: rotateY(180deg);
}

/* Содержимое страницы */
.paper-content {
  border: 3px double #d81b60;
  height: 100%;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  overflow-y: auto;
  background: #fff;
}

/* --- ИСПРАВЛЕНИЕ 2: Разворачиваем текст обратно --- */
.rotated-content {
  /* Так как сама страница повернута на 180,
     контент внутри тоже нужно повернуть на 180, чтобы он стал читаемым */
  transform: rotateY(180deg);
}
/* ------------------------------------------------ */


.page h2 {
  color: #c2185b;
  font-size: 2rem;
  margin-top: 10px;
}

.letter-text {
  font-size: 1.2rem;
  line-height: 1.6;
  color: #4a4a4a;
  margin-bottom: 30px;
}

/* -- ФОТОПОЛАРОИДЫ -- */
.gallery {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

.photo-frame {
  background: white;
  padding: 10px 10px 25px 10px;
  box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
  transform: rotate(-5deg);
  transition: transform 0.3s;
  backface-visibility: hidden; /* Убирает мерцание при анимации */
}

.photo-frame:hover {
  transform: scale(1.1) rotate(0deg) !important;
  z-index: 10;
}

.rotate-right { transform: rotate(5deg); }

.photo-frame img {
  width: 100px;
  height: 100px;
  object-fit: cover;
  border: 1px solid #eee;
}

.photo-frame span {
  display: block;
  margin-top: 5px;
  font-family: 'Crimson Text', cursive;
  color: #333;
  font-size: 1rem;
}

.footer-love {
  margin-top: auto;
  font-style: italic;
  color: #880e4f;
}

/* -- КНОПКИ -- */
.buttons {
  display: flex;
  gap: 15px;
  justify-content: center;
  flex-wrap: wrap;
  /* Важно для 3D трансформации кнопки */
  transform-style: preserve-3d;
}

.btn {
  font-family: 'Crimson Text', serif;
  font-weight: bold;
  padding: 10px 25px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1.1rem;
  box-shadow: 0 4px 6px rgba(0,0,0,0.2);
  transition: all 0.3s ease;
  /* Чтобы кнопка не сплющивалась при повороте */
  backface-visibility: hidden;
}

.yes-btn { background: #fff; color: #d81b60; z-index: 5; }
.no-btn { background: rgba(255,255,255,0.3); color: white; border: 1px solid white; }

/* АДАПТИВНОСТЬ */
@media (max-width: 768px) {
  .book {
    width: 90vw;
    height: 80vh;
  }
  .book.open {
    transform: rotateY(-180deg); /* На мобилке просто переворачиваем */
  }
}
</style>