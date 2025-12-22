import { drizzle } from "drizzle-orm/bun-sql";
import * as schema from "./db/schema";
import * as operator from "./db/operator";

const db = drizzle(process.env.DATABASE_PUBLIC_URL!, { schema });

export { db, schema, operator };
