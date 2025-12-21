import { s3 } from "bun";

const bucket = {
  upload_file: async (key: string, buffer: Uint8Array) => {
    const metadata = s3.file(key);
    const bytes = await metadata.write(buffer);
    console.log(`🪣 Uploaded ${bytes} bytes to ${key}`);
  },
};

export { bucket };
