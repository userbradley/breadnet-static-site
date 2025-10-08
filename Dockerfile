FROM klakegg/hugo:ext-alpine as BUILDER

COPY . /src/

RUN hugo --baseURL http://localhost:8081

FROM nginx:stable-alpine

COPY --from=BUILDER /src/public /var/www/site

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8081