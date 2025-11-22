FROM node:18-alpine

WORKDIR /app

# Copiar dependencias e instalar
COPY package.json .
RUN npm install

# Copiar el resto del código
COPY . .

# Exponer el puerto
EXPOSE 3000

# Iniciar servidor
CMD ["node", "server.js"]