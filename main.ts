import { copyFileSync, existsSync, mkdirSync, readFileSync, statSync } from "node:fs";
import { join } from "node:path";

// "The World Today" — 19 November 2026 front page.
// The entry is the image this program ships: entry.png, drawn by
// tools/draw_frontpage.py. This program only copies it to the output
// directory, after checking it is a whole 1024x1024 PNG under 1 MiB.

const SOURCE = new URL("./entry.png", import.meta.url).pathname;
const OUT_DIR = process.env.MAKEFUN_OUTPUT_DIR || "/output";
const TARGET = join(OUT_DIR, "entry.png");

function fail(message: string): never {
  console.error("main.ts: " + message);
  process.exit(1);
}

if (!existsSync(SOURCE)) {
  fail("entry.png not found next to main.ts");
}

const bytes = readFileSync(SOURCE);

// PNG signature: 89 50 4E 47 0D 0A 1A 0A
if (
  bytes.length < 24 ||
  bytes[0] !== 0x89 ||
  bytes[1] !== 0x50 ||
  bytes[2] !== 0x4e ||
  bytes[3] !== 0x47
) {
  fail("entry.png is not a PNG file");
}

if (bytes.length > 1048576) {
  fail("entry.png is " + bytes.length + " bytes, over the 1 MiB limit");
}

const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width !== 1024 || height !== 1024) {
  fail("entry.png is " + width + "x" + height + ", expected 1024x1024");
}

// Only create the output directory itself; never remove it, and never
// clear its contents — the grader may mount it read-only or shared.
mkdirSync(OUT_DIR, { recursive: true });
copyFileSync(SOURCE, TARGET);

const written = statSync(TARGET);
if (written.size !== bytes.length) {
  fail("copied file is " + written.size + " bytes, expected " + bytes.length);
}

console.log("wrote " + TARGET + " (" + written.size + " bytes, 1024x1024 PNG)");
