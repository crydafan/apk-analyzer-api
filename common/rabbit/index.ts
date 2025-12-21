import Connection, {
  type Consumer,
  type ConsumerHandler,
  ConsumerStatus,
  type Publisher,
} from "rabbitmq-client";

const rabbit = new Connection(process.env.RABBITMQ_URL!);

let pub_: Publisher | undefined = undefined;
let sub_: Consumer | undefined = undefined;

rabbit.on("connection", () => {
  console.log("🐇 RabbitMQ connected");
});

rabbit.on("error", (err) => {
  console.error("🐇 RabbitMQ connection error:", err);
});

const sub = (queue: string, callback: ConsumerHandler) => {
  sub_ = rabbit.createConsumer(
    {
      queue,
      queueOptions: { durable: true },
    },
    async (msg, reply) => {
      console.log(`🐇 Received message (${queue}):`, msg);
      return await callback(msg, reply);
    }
  );

  sub_.on("ready", () => {
    console.log(`🐇 Consumer ready (${queue})`);
  });

  sub_.on("error", (err) => {
    // Maybe the consumer was cancelled, or the connection was reset before a
    // message could be acknowledged.
    console.log(`🐇 Consumer error (${queue})`, err);
  });

  return sub_;
};

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
  if (sub_) await sub_.close();
  await rabbit.close();
}
// TODO: Uncomment these lines to enable graceful shutdown
//process.on("SIGINT", onShutdown);
//process.on("SIGTERM", onShutdown);

export { pub, sub, ConsumerStatus };
