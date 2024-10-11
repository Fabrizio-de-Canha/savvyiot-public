# Step 1: Use an official Node.js image as the base image
FROM node:18-alpine

WORKDIR /app

# Copy everything from the build context (iot_frontend directory)
COPY . .  
# This will copy everything from the iot_frontend directory

RUN npm ci --legacy-peer-deps

RUN npm run build
RUN npm install -g serve

EXPOSE 3000

CMD ["serve", "-s", "dist"]
