FROM nginx:alpine

COPY default.conf /etc/nginx/conf.d/default.conf
COPY proxy_common.conf /etc/nginx/proxy_common.conf

COPY --from=academic-express/backend /app/static /app/static
COPY --from=academic-express/frontend /app/dist /usr/share/nginx/html

EXPOSE 80
