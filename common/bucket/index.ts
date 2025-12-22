import { s3 } from "bun";

const bucket = {
  upload_file: async (key: string, buffer: Uint8Array) => {
    const metadata = s3.file(key);
    const bytes = await metadata.write(buffer);
    console.log(`🪣 Uploaded ${bytes} bytes to ${key}`);
  },
  presign: (key: string) => {
    const url = s3.presign(key, { expiresIn: 3600 });
    console.log(
      `🪣 Generated presigned URL for ${key}: ${url.slice(0, 100)}...`
    );
    return url;
  },
};

export { bucket };
