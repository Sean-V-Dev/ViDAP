export const requiredNodeMajor = 24;

export function nodeMajor(version) {
  return Number.parseInt(version.split(".", 1)[0], 10);
}

export function unsupportedNodeMessage(version) {
  return (
    `ViDAP requires Node.js ${requiredNodeMajor}.x; found ${version}. ` +
    "Use the Node 24 LTS runtime pinned in .nvmrc, then run npm.cmd again."
  );
}

export function validateNodeVersion(version) {
  if (nodeMajor(version) === requiredNodeMajor) {
    return null;
  }

  return unsupportedNodeMessage(version);
}

const validationMessage = validateNodeVersion(process.versions.node);

if (validationMessage !== null) {
  console.error(validationMessage);
  process.exitCode = 1;
}
