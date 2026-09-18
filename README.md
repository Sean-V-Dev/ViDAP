# ViDAP

ViDAP is an open-source, local-first visual data-science playground. Its goal
is to let people work with real data through an inspectable graph: explore and
transform data, train and evaluate established machine-learning libraries,
compare experiments, understand results in practical language, and export
conventional Python or Jupyter artifacts.

> **Foundation planning is active. No runnable application exists yet.** Setup,
> build, test, and launch commands arrive only in later approved packets.

## Intended architecture and prerequisites

The accepted direction is a TypeScript/React local web UI and a separate local
CPython/FastAPI host. The browser remains a visual editing and presentation
layer; future workflow and execution semantics are outside browser-only state.
This describes intended architecture, not implementation.

The accepted future setup contract is Windows, Git, Node.js 24 LTS with its
bundled npm, CPython 3.14.x subject to P0-EP04 compatibility verification, and
uv. These are planned prerequisites, not usable setup instructions today.

## Scope today

Phase 0 is establishing project policy and reproducible foundations. It does
not implement a node graph, workflow schema, dataset loading, profiling,
training, experiments, exports, hosted services, authentication, deployment,
or cross-platform support. Windows is the only planned platform claim until
other environments are validated.

## Authority and navigation

- [Product specification](ViDAP_Overview.txt)
- [Phased Plan Spine](ViDAP_Phased_Plan_Spine.md)
- [Roadmap](ViDAP_Roadmap.md)
- [Phase 0 plan](ViDAP_Phase_0_Plan.md)
- [P0-EP01 reconciliation](ViDAP_P0_EP01_Validation_and_Reconciliation.md)
- [P0-EP02 reconciliation](ViDAP_P0_EP02_Validation_and_Reconciliation.md)
- [Contribution guide](CONTRIBUTING.md)
- [Security policy](SECURITY.md)
- [Decision-record guide](docs/decisions/README.md)
- [MIT License](LICENSE)

## Contributing and reporting

Start with the [contribution guide](CONTRIBUTING.md). Report ordinary,
non-sensitive bugs and proposals through
[GitHub Issues](https://github.com/Sean-V-Dev/ViDAP/issues). Report suspected
vulnerabilities only through the private route in [SECURITY.md](SECURITY.md).

## Local and generated state

`.vidap-local/` is reserved for untracked developer or runtime state only when
a later packet names a legitimate use. Build, test, coverage, environment,
package-cache, and downloaded-data paths are untracked under `.gitignore`.
Approved tracked fixture content is permitted only under accepted D0.7 policy;
generated and local fixture subareas remain ignored. New mutable or generated
paths must be named and documented with their ignore rules in the same later
packet. Ignored state is not an approved location for secrets.

## License

ViDAP is licensed under the [MIT License](LICENSE).
