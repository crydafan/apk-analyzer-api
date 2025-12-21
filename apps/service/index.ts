import { Elysia } from "elysia";
import { db, schema } from "@common/db";

const app = new Elysia()
  .get("/", () => {})
  .post("/", async () => {
    const [job] = await db.insert(schema.jobsTable).values({}).returning();
    return job;
  })
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);
