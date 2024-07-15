#####################
# Local development stage
# dev mode, hot reloading
#####################
FROM node:20-slim AS local
WORKDIR /usr/src/app

# install deps first, improves image build times when only src has changed
COPY package*.json ./
RUN npm ci

# copy src and project files
COPY . .

EXPOSE 4200
# start server in dev mode, host 0.0.0.0 for docker compatability
CMD ["npm", "run", "start", "--", "--host", "0.0.0.0"]

#####################
# Builder stage
# install deps and build project for production
#####################

# use specific image tag for reproducibility
FROM node:20-slim@sha256:8d5c168087c841ac367468f77935aa78eff3195b48bf9eb05cbc761e6b9db507 AS builder
WORKDIR /usr/src/app

# install deps first, improves image build times when only src has changed
COPY package*.json ./
RUN npm ci

# copy src and project files
COPY . .

# build for production
RUN npm run build -- --configuration production

#####################
# Production stage
# copy build output from builder stage
# exposed via nginx in production
#####################

# use specific image tag for reproducibility
FROM nginx:1.25-alpine-slim@sha256:22414422d1ba07234d9b784f6453b4f150c0fa573ad0b62e163da12b68488ae1 AS production

# copy build output from builder stage
COPY --from=builder /usr/src/app/dist/angular-app/browser /usr/share/nginx/html

# use custom nginx conf
COPY nginx.conf /etc/nginx/nginx.conf

# setup ownership and permissions for nginx user
RUN chown -R nginx:nginx /usr/share/nginx/html && \
  chmod -R 755 /usr/share/nginx/html && \
  chown -R nginx:nginx /var/cache/nginx && \
  chown -R nginx:nginx /var/log/nginx && \
  chown -R nginx:nginx /etc/nginx/conf.d
RUN touch /var/run/nginx.pid && \
  chown -R nginx:nginx /var/run/nginx.pid

# non-root user is best practice (least priviledge)
USER nginx

# expose non-priviledged port (matches nginx conf)
EXPOSE 4200

# start nginx server
CMD ["nginx", "-g", "daemon off;"]
