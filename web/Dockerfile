FROM node:22-alpine AS base
WORKDIR /app
ENV NODE_ENV=production
COPY package.json package-lock.json* ./
RUN if [ -f package-lock.json ]; then npm ci; else npm install; fi
FROM base AS dev
ENV NODE_ENV=development
RUN npm install -D typescript @types/node @types/react @types/react-dom
COPY tsconfig.json ./tsconfig.json
COPY next.config.mjs ./next.config.mjs
COPY app ./app
EXPOSE 3000
CMD ["npm","run","dev"]
