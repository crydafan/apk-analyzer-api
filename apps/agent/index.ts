import { sub } from "@common/rabbit";

const consumer = sub("jobs", async (msg) => {});
consumer.start();
