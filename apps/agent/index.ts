import { sub, Ack } from "@common/rabbit";

const consumer = sub("jobs", async (msg) => {
  return Ack;
});
consumer.start();
