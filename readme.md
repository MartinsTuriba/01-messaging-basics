# Testing the Entire Flow

## Prerequisites
- Docker and Docker Compose installed
- Node.js and npm installed

## Steps

### 1. Start RabbitMQ using Docker
Navigate to the project root directory and run:

```bash
docker-compose up -d
```

This will start RabbitMQ in a Docker container in detached mode. You can verify it's running with:
```bash
docker ps
```

RabbitMQ Management UI will be available at [http://localhost:15672](http://localhost:15672) (default credentials: guest/guest)

### 2. Start the Producer

```bash
cd producer
npm install
npm start
```

Once started, open [http://localhost:3000](http://localhost:3000) in your browser.

### 3. Start the Consumer

```bash
cd consumer
npm install
npm start
```

Once started, open [http://localhost:4000](http://localhost:4000) in a separate browser tab.

### 4. Send Test Messages

1. Navigate to the producer page in your browser
2. Click the "Send Message" button
3. You should receive an alert: "Message sent to RabbitMQ!"
4. Verify the message reception:
   - Check the consumer's terminal where you ran `npm start`
   - Or view the consumer's webpage at [http://localhost:4000](http://localhost:4000)
   - The message should appear within a few seconds

## Troubleshooting

If you don't see the messages appearing:
- Verify that RabbitMQ container is running: `docker ps`
- Check RabbitMQ logs: `docker logs <container-id>`
- Check both producer and consumer console logs for any errors
- Ensure all npm dependencies are properly installed

### Stopping RabbitMQ
To stop the RabbitMQ container:
```bash
docker-compose down
```