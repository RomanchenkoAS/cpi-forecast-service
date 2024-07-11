FROM nginx:1.22.1-alpine


# Remove sym links from nginx image
RUN rm /var/log/nginx/access.log
RUN rm /var/log/nginx/error.log

# Install logrotate
RUN apk update && apk add logrotate

# Copy nginx config
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

# Copy logrotate nginx configuration
COPY logrotate.d/nginx /etc/logrotate.d/

# Start nginx as a service
CMD nginx -g 'daemon off;'