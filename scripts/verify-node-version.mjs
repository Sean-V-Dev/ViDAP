const requiredMajor = 24;
const actualVersion = process.versions.node;
const actualMajor = Number.parseInt(actualVersion.split(".", 1)[0], 10);

if (actualMajor !== requiredMajor) {
  console.error(
    `ViDAP requires Node.js ${requiredMajor}.x; found ${actualVersion}. ` +
      "Use the Node 24 LTS runtime pinned in .nvmrc, then run npm.cmd again.",
  );
  process.exitCode = 1;
}
