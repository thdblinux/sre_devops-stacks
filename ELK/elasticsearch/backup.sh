services:
  elasticsearch:
    image: elasticsearch
    container_name: elasticsearch
    hostname: elasticsearch
    restart: always
    deploy:
      resources:
        limits:
          cpus: '1.0'
          memory: 750M
        reservations:
          cpus: '0.25'
          memory: 512M
    ports:
      - 15672:15672
      - 5672:5672
    volumes:
      - /home/admdesenv/app/elasticsearch/docker/data/:/var/lib/elasticsearch/
      - /home/admdesenv/app/elasticsearch/docker/log/:/var/log/elasticsearch