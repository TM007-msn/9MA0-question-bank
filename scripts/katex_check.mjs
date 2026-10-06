// Render-check LaTeX strings exactly the way the review sheet does.
//
// The review sheet (build_review.py) loads KaTeX 0.16.11 auto-render with the
// delimiters $$...$$ (display) and $...$ (inline). This script uses the same
// KaTeX version (package.json) and the same splitter, so a string passes here
// only if it renders there without a red error.
//
// Input (stdin): JSON object {label: text}. Output (stdout): JSON list of
// [label, message] for every failure. Called by scripts/validate.py.

import katex from "katex";
import splitAtDelimiters from "katex/contrib/auto-render/splitAtDelimiters.js";

const DELIMITERS = [
  { left: "$$", right: "$$", display: true },
  { left: "$", right: "$", display: false },
];

function check(text) {
  const errors = [];
  for (const part of splitAtDelimiters(text, DELIMITERS)) {
    if (part.type === "text") {
      // auto-render leaves an unclosed delimiter as plain text, so the maths
      // after it would show as raw LaTeX.
      if (part.data.includes("$")) {
        errors.push(`unclosed $ delimiter near: ${part.data.slice(part.data.indexOf("$"), part.data.indexOf("$") + 40)}`);
      }
      continue;
    }
    try {
      katex.renderToString(part.data, { displayMode: part.display, throwOnError: true, strict: "ignore" });
    } catch (err) {
      errors.push(`${err.message} in: ${part.rawData.slice(0, 80)}`);
    }
  }
  return errors;
}

let input = "";
process.stdin.setEncoding("utf8");
process.stdin.on("data", (chunk) => (input += chunk));
process.stdin.on("end", () => {
  const failures = [];
  for (const [label, text] of Object.entries(JSON.parse(input))) {
    for (const message of check(text)) failures.push([label, message]);
  }
  process.stdout.write(JSON.stringify(failures));
});
