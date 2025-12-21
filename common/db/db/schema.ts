import { pgTable, pgEnum, timestamp, uuid } from "drizzle-orm/pg-core";

export const jobStatusEnum = pgEnum("job_status", [
  "pending",
  "in_progress",
  "completed",
  "failed",
]);

export const jobsTable = pgTable("jobs", {
  id: uuid("id").primaryKey().defaultRandom(),
  status: jobStatusEnum("status").notNull().default("pending"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().notNull(),
});
