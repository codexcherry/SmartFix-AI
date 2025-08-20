FROM node:16-alpine

WORKDIR /app

COPY package.json package-lock.json* ./

RUN npm install

COPY . .

RUN npm run build

# Install serve to run the application
RUN npm install -g serve

# Set the command to start the app
CMD ["serve", "-s", "build", "-l", "3000"]
