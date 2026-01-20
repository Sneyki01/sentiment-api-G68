FROM nginx:alpine

# Limpia default html
RUN rm -rf /usr/share/nginx/html/*

# Copia el sitio estático
COPY public/ /usr/share/nginx/html/

EXPOSE 80