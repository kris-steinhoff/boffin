FROM node:lts AS development

EXPOSE 80
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install
COPY . /app
CMD [ "npm", "run", "dev", "--", "--host=0.0.0.0", "--port=80" ]

FROM development AS build

RUN npm run build

FROM nginx:alpine

EXPOSE 80
WORKDIR /usr/share/nginx/html
RUN rm -rf ./*
COPY --from=build /app/build .
ENTRYPOINT ["nginx", "-g", "daemon off;"]
