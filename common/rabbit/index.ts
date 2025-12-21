import Connection, { type Publisher } from "rabbitmq-client";

const rabbit = new Connection(process.env.RABBITMQ_URL!);

let pub_: Publisher | undefined = undefined;

rabbit.on("connection", () => {
  console.log("🐇 RabbitMQ connected");
});

rabbit.on("error", (err) => {
  console.error("🐇 RabbitMQ connection error:", err);
});

const pub = (queues: string[]) => {
  pub_ = rabbit.createPublisher({
    confirm: true,
    maxAttempts: 2,
    queues: queues.map((queue) => ({
      queue,
      durable: true, // Survives broker restart
    })),
  });
  return pub_;
};

// Clean up when you receive a shutdown signal
async function onShutdown() {
  // Waits for pending confirmations and closes the underlying Channel
  if (pub_) await pub_.close();
  // Stop consuming. Wait for any pending message handlers to settle.
  // await sub.close();
  await rabbit.close();
}
// TODO: Uncomment these lines to enable graceful shutdown
//process.on("SIGINT", onShutdown);
//process.on("SIGTERM", onShutdown);

export { pub };
