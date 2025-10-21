#FROM klakegg/hugo:ext-alpine as BUILDER
FROM ghcr.io/gohugoio/hugo:v0.151.2 as BUILDER

USER root:root

WORKDIR /src/
COPY . /src/
COPY .git /src/.git/

RUN hugo build --baseURL http://localhost:8081 --noBuildLock

FROM nginx:stable-alpine

COPY --from=BUILDER /src/public /var/www/site

COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 8081
