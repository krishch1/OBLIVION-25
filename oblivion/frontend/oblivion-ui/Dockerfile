# oblivion/frontend/oblivion-ui/Dockerfile

# ---- Stage 1: Build the React application ----
FROM node:20-alpine AS build

WORKDIR /app

# Copy package.json and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the application files
COPY . .

# Build the application for production
RUN npm run build

# ---- Stage 2: Serve the built application with Nginx ----
FROM nginx:stable-alpine

# Copy the built static files from the build stage to the Nginx server directory
COPY --from=build /app/dist /usr/share/nginx/html

# Expose port 80
EXPOSE 80

# When the container starts, run Nginx in the foreground
CMD ["nginx", "-g", "daemon off;"]