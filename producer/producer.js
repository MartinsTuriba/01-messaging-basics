const express = require("express");
const amqp = require("amqplib");
const crypto = require("crypto"); // For generating random message IDs

const app = express();
const PORT = 3000;
const RABBITMQ_URL = "amqp://localhost";  // Change if needed (e.g., Docker IP)
const QUEUE_NAME = "demo_queue";

let channel;

// 1) Parse JSON bodies
app.use(express.json());

// 2) Serve static files from "public" folder
app.use(express.static("public"));

// 3) Connect to RabbitMQ and create a channel
async function connectToRabbitMQ() {
  try {
    const connection = await amqp.connect(RABBITMQ_URL);
    channel = await connection.createChannel();
    await channel.assertQueue(QUEUE_NAME, { durable: false });
    console.log(`Connected to RabbitMQ and asserted queue "${QUEUE_NAME}".`);
  } catch (err) {
    console.error("Error connecting to RabbitMQ:", err);
  }
}

// 4) Endpoint to receive and send messages
app.post("/send", async (req, res) => {
  try {
    const { text } = req.body;
    const messageId = crypto.randomUUID(); // Generate a random ID

    const payload = {
      messageId,
      messageText: text
    };

    // Publish the combined payload (JSON) to the queue
    channel.sendToQueue(QUEUE_NAME, Buffer.from(JSON.stringify(payload)));
    console.log("Sent message:", payload);

    res.send(`Message sent to RabbitMQ with ID: ${messageId}`);
  } catch (error) {
    console.error("Error sending message:", error);
    res.status(500).send("Failed to send message.");
  }
});

// 5) Start server and then connect to RabbitMQ
app.listen(PORT, async () => {
  console.log(`Producer app listening on http://localhost:${PORT}`);
  await connectToRabbitMQ();
});
