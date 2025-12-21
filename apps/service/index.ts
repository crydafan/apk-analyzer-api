import { Elysia, status, t } from "elysia";
import { db, schema, operator } from "@common/db";

const app = new Elysia()
  .get(
    "/:id",
    async ({ params }) => {
      const [job] = await db
        .select()
        .from(schema.jobsTable)
        .where(operator.eq(schema.jobsTable.id, params.id));
      if (!job) {
        return status(404, { success: false, message: "Job not found" });
      }
      return {
        success: true,
        message: "Job retrieved successfully",
        data: job,
      };
    },
    {
      params: t.Object({
        id: t.String(),
      }),
    }
  )
  .post("/", async () => {
    const [job] = await db.insert(schema.jobsTable).values({}).returning();
    return status(201, {
      success: true,
      message: "Job created",
      data: job,
    });
  })
  .listen(3000);

console.log(
  `🦊 Elysia is running at ${app.server?.hostname}:${app.server?.port}`
);
