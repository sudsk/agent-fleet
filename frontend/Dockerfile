FROM node:18-alpine

WORKDIR /app

# Copy package files and install dependencies
COPY package.json package-lock.json ./
RUN npm ci

# Copy application files
COPY . .

# Set environment variables
ENV NODE_ENV=development
ENV PORT=3000

# Start development server
CMD ["npm", "start"]
