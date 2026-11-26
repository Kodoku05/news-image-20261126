import { copyFile, mkdir } from 'node:fs/promises';
import { resolve, join } from 'node:path';
import { fileURLToPath } from 'node:url';

// The committed artwork is the complete offline rendering input.
const artwork = fileURLToPath(new URL('./entry.png', import.meta.url));
const destination = resolve(process.env.MAKEFUN_OUTPUT_DIR || '/output');

try {
  await mkdir(destination, { recursive: true });
  await copyFile(artwork, join(destination, 'entry.png'));
} catch (failure) {
  const reason = failure instanceof Error ? failure.message : String(failure);
  console.error(`Newspaper export failed for ${destination}: ${reason}`);
  process.exitCode = 1;
}
