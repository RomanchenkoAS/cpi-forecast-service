FROM nginx:1.22.1-alpine


# Remove sym links from nginx image
RUN rm /var/log/nginx/access.log
RUN rm /var/log/nginx/error.log

# Install logrotate & htpasswrd tool
RUN apk update && apk add logrotate apache2-utils

# Copy nginx config
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# Copy logrotate nginx configuration
COPY logrotate.d/nginx /etc/logrotate.d/

# Define build arguments
ARG NGINX_USER
ARG NGINX_PASSW
# Create a password file with a default user (if provided)
RUN if [ -n "$NGINX_USER" ] && [ -n "$NGINX_PASSW" ]; then \
        htpasswd -cb /etc/nginx/.htpasswd $NGINX_USER $NGINX_PASSW; \
    fi


# Start nginx as a service
CMD nginx -g 'daemon off;'