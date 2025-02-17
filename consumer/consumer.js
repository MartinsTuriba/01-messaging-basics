const express = require("express");
const amqp = require("amqplib");

const app = express();
const PORT = 4000;
const RABBITMQ_URL = "amqp://localhost"; // Adjust if using Docker or a remote broker
const QUEUE_NAME = "demo_queue";

let channel;
let lastMessageId = null;
let lastMessageBody = null;

// Keep all messages in memory (non-persistent)
let messageHistory = [];

// 1) Connect to RabbitMQ and consume messages
async function connectToRabbitMQAndConsume() {
  try {
    const connection = await amqp.connect(RABBITMQ_URL);
    channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME, { durable: false });

    console.log(`Consumer connected, waiting for messages in "${QUEUE_NAME}"...`);

    channel.consume(QUEUE_NAME, (msg) => {
      if (msg !== null) {
        // Attempt to parse the incoming message as JSON
        let parsed;
        try {
          parsed = JSON.parse(msg.content.toString());
        } catch (e) {
          parsed = { messageId: "UNKNOWN", messageText: msg.content.toString() };
        }

        const messageId = parsed.messageId || "UNKNOWN_ID";
        const messageBody = parsed.messageText || "No text property found";

        // Update the "last message" fields
        lastMessageId = messageId;
        lastMessageBody = messageBody;

        // Keep a record of the message with timestamp
        const timeStamp = new Date().toISOString();
        messageHistory.push({
          timeReceived: timeStamp,
          messageId: messageId,
          messageBody: messageBody
        });

        console.log(`[${timeStamp}] Received message: ID=${messageId}, body="${messageBody}"`);

        // Acknowledge the message
        channel.ack(msg);
      }
    });
  } catch (err) {
    console.error("Error connecting to RabbitMQ:", err);
  }
}

// 2) Endpoint: Return the last message as JSON
app.get("/last-message", (req, res) => {
  res.json({
    lastMessageId,
    lastMessageBody
  });
});

// 3) Endpoint: Return the entire message history as JSON
app.get("/messages", (req, res) => {
  res.json(messageHistory);
});

// 4) Serve static files (index.html) from "public" folder
app.use(express.static("public"));

// 5) Start server and connect to RabbitMQ
app.listen(PORT, async () => {
  console.log(`Consumer app listening on http://localhost:${PORT}`);
  await connectToRabbitMQAndConsume();
});
