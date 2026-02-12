<script setup>
import { ref } from 'vue'

const yesSize = ref(1) // Множитель размера
const isSuccess = ref(false)

// Фразы для кнопки "Нет"
const noTexts = [
  "Нет",
  "Ты уверена?",
  "Прям точно?",
  "Подумай хорошенько!",
  "Может передумаешь?",
  "Не разбивай мне сердце 💔",
  "Я буду плакать...",
  "Я буду ОЧЕНЬ плакать...",
  "Ну пожаааалуйста?",
  "Ладно, я понял...",
  "Шутка! Скажи ДА! ❤️"
]
const noTextIndex = ref(0)
const noBtnText = ref(noTexts[0])

const handleNo = () => {
  // Увеличиваем кнопку YES
  yesSize.value *= 1.35

  // Меняем текст на кнопке NO
  if (noTextIndex.value < noTexts.length - 1) {
    noTextIndex.value++
  }
  noBtnText.value = noTexts[noTextIndex.value]
}

const handleYes = async () => {
  isSuccess.value = true

  // Отправляем радость на бэкенд
  try {
    await $fetch('/api/response', {
      method: 'POST',
      body: { answer: 'yes' }
    })
  } catch (e) {
    console.error('Ошибка отправки, но она все равно сказала да!', e)
  }
}
</script>

<template>
  <div class="wrapper">
    <div v-if="!isSuccess" class="container">
      <img
        src="https://media1.tenor.com/m/hnF3F7fbcowAAAAC/cat-jump.gif"
        alt="Cute cat"
        class="gif"
      />

      <h1 class="title">Would you be my Valentine? 💖</h1>

      <div class="buttons">
        <button
          class="btn yes-btn"
          @click="handleYes"
          :style="{ transform: `scale(${yesSize})` }"
        >
          Да!
        </button>

        <button class="btn no-btn" @click="handleNo">
          {{ noBtnText }}
        </button>
      </div>
    </div>

    <div v-else class="container success">
      <img
        src="https://media1.tenor.com/m/lCKwsD2OW1kAAAAC/happy-cat-happy-happy-cat.gif"
        alt="Happy cat"
        class="gif"
      />
      <h1 class="title">Урааа! Я знал это! <br> Люблю тебя! ❤️</h1>
    </div>
  </div>
</template>

<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito:wght@400;700;900&display=swap');

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
  width: 100%;
  overflow: hidden; /* Чтобы кнопка не растягивала страницу со скроллом */
  background-color: #fce4ec; /* Нежно-розовый */
  font-family: 'Nunito', sans-serif;
}

.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  width: 100vw;
}

.container {
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 20px;
  z-index: 10;
}

.gif {
  width: 200px;
  border-radius: 15px;
  mix-blend-mode: multiply; /* Убирает белый фон у гифки, если он есть */
}

.title {
  color: #d81b60;
  font-weight: 900;
  font-size: 2.5rem;
  margin: 0;
  text-shadow: 2px 2px 0px rgba(255, 255, 255, 0.5);
}

.buttons {
  display: flex;
  gap: 20px;
  align-items: center;
  justify-content: center;
  margin-top: 20px;
  position: relative;
}

.btn {
  font-family: 'Nunito', sans-serif;
  font-size: 1.2rem;
  font-weight: bold;
  padding: 12px 24px;
  border: none;
  border-radius: 50px;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap; /* Текст не переносится */
}

.yes-btn {
  background-color: #4caf50;
  color: white;
  box-shadow: 0 4px 0 #388e3c;
  z-index: 2; /* Кнопка ДА всегда сверху */
  transform-origin: center;
}

.yes-btn:active {
  transform: translateY(4px);
  box-shadow: 0 0 0 #388e3c;
}

.no-btn {
  background-color: #ef5350;
  color: white;
  box-shadow: 0 4px 0 #d32f2f;
}

.no-btn:active {
  transform: translateY(4px);
  box-shadow: 0 0 0 #d32f2f;
}

/* Адаптив для телефонов */
@media (max-width: 600px) {
  .title {
    font-size: 1.8rem;
  }
  .gif {
    width: 150px;
  }
  .buttons {
    flex-direction: column; /* Кнопки друг под другом на телефоне */
    gap: 15px;
  }
}
</style>