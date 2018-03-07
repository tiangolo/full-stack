# Stage 0, based on Node.js, to build and compile Angular
FROM node:9.7 as building

# Add Chrome dependencies, to run Puppeteer (headless Chrome) for Angular / Karma tests
# Taken from: https://github.com/GoogleChrome/puppeteer/blob/master/docs/troubleshooting.md
# Install latest chrome dev package.
# Note: this installs the necessary libs to make the bundled version of Chromium that Pupppeteer
# installs, work.
RUN apt-get update && apt-get install -y wget --no-install-recommends \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update \
    && apt-get install -y google-chrome-unstable \
      libgconf-2-4 \
      --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get purge --auto-remove -y curl \
    && rm -rf /src/*.deb


WORKDIR /app

COPY package*.json /app/

RUN npm install

COPY ./ /app/

ARG env=prod

RUN npm run test:prod

RUN npm run build -- --prod --environment $env


# Stage 1, based on Nginx, to have only the compiled app, ready for production with Nginx
FROM nginx:1.13

COPY --from=building /app/dist/ /usr/share/nginx/html

COPY ./nginx-custom.conf /etc/nginx/conf.d/default.conf
