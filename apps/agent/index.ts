import { sub, Ack, Drop } from "@common/rabbit";
import { db, schema, operator } from "@common/db";

type MessageBody = {
  jobId: string; // Job id
  fileName: string; // Storage key
};

const consumer = sub("jobs", async (msg) => {
  const body: MessageBody = msg.body;

  const [job] = await db
    .select()
    .from(schema.jobsTable)
    .where(operator.eq(schema.jobsTable.id, body.jobId))
    .limit(1);

  if (!job) {
    // No job with such id found, to whom are we supposed to process this?
    console.log(`⚙️ Job with id ${body.jobId} not found, dropping message.`);
    return Drop;
  }

  console.log(`⚙️ Processing job with id ${body.jobId}`);
  job.status = "in_progress";
  job.updatedAt = new Date();

  await db
    .update(schema.jobsTable)
    .set({
      status: job.status,
      updatedAt: job.updatedAt,
    })
    .where(operator.eq(schema.jobsTable.id, body.jobId));

  // Simulate a 3 second task
  await new Promise((resolve) => setTimeout(resolve, 3000));

  job.status = "completed";
  job.updatedAt = new Date();

  await db
    .update(schema.jobsTable)
    .set({
      status: job.status,
      updatedAt: job.updatedAt,
    })
    .where(operator.eq(schema.jobsTable.id, body.jobId));

  console.log(`⚙️ Completed job with id ${body.jobId}`);

  return Ack;
});
consumer.start();
