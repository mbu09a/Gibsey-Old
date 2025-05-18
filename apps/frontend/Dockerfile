FROM node:18.19.1-alpine AS builder
WORKDIR /usr/src/app

# Install dependencies first to leverage Docker cache
COPY package*.json ./
RUN npm ci --legacy-peer-deps

# Copy the rest of the application
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:18.19.1-alpine
WORKDIR /usr/src/app

# Copy built assets from builder
COPY --from=builder /usr/src/app/.next ./.next
COPY --from=builder /usr/src/app/public ./public
COPY --from=builder /usr/src/app/package*.json ./

# Install only production dependencies
RUN npm ci --only=production --legacy-peer-deps

# Expose the port the app runs on
EXPOSE 3000

# Start the application
CMD ["npm", "start"]