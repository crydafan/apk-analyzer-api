import { drizzle } from "drizzle-orm/bun-sql";
import * as schema from "./db/schema";

const db = drizzle(process.env.DATABASE_PUBLIC_URL!, { schema });

export { db, schema };
