FROM redis:4.0.11

# Set default values for REDIS_PASSWORD, and REDIS_PORT in case they're not provided in the .env file
ARG REDIS_PASSWORD=default_password
ARG REDIS_PORT=6379

# Set the values from the environment variables
ENV REDIS_PASSWORD=$REDIS_PASSWORD
ENV REDIS_PORT=$REDIS_PORT

CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\" --port \"$REDIS_PORT\""]
