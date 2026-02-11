# Используем Node.js
FROM node:20-alpine

WORKDIR /app

# Копируем package.json и ставим зависимости
COPY package*.json ./
RUN npm install

# Копируем остальной код и собираем проект
COPY . .
RUN npm run build

# Nuxt слушает порты
ENV NUXT_HOST=0.0.0.0
ENV NUXT_PORT=3000

# Запускаем собранное приложение
CMD ["node", ".output/server/index.mjs"]