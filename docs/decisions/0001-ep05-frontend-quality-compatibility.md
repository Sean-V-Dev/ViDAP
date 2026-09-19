# Decision Record: EP05 Frontend Quality Compatibility Amendment

| Field | Value |
|---|---|
| ID | 0001 |
| Status | Accepted |
| Date | 2026-09-18 |
| Owners | Central |
| Governing requirements | `ViDAP_Overview.txt`; `ViDAP_Phase_0_Plan.md`; D0.4 in `ViDAP_P0_EP02_Validation_and_Reconciliation.md`; `ViDAP_P0_EP05.md`; `ViDAP_P0_EP05_Implementation_Report.md` |

## Context

P0-EP05 version 0.1 stopped before implementation after primary npm metadata showed no maintained, peer-compatible intersection for the required current ESLint 10, `eslint-plugin-jsx-a11y`, and TypeScript-ESLint set. The accepted scaffold also pins TypeScript 7.0.2, while the examined TypeScript-ESLint release declares support only below TypeScript 6.1.0.

The blocker does not affect the approved roles of compiler checking, React Hooks checks, formatting, testing, or the Python quality layers. At EP05's intentionally no-UI boundary, JSX accessibility rules would have no meaningful authored interface to inspect. A forced peer graph or an unsupported ESLint 9 line would not meet the project's compatibility and maintenance constraints.

## Decision

For P0-EP05, use an exact, currently maintained TypeScript 6.x release that is declared compatible with the selected current TypeScript-ESLint integration. The worker must intentionally replace the scaffold's TypeScript 7.x dependency and update only the authoritative `package-lock.json` as part of the approved EP05 implementation.

Defer `eslint-plugin-jsx-a11y` and JSX accessibility lint rules. EP05 retains ESLint flat configuration, TypeScript-aware linting, and React Hooks checks, but must not install JSX-a11y, force unsupported peers, or substitute a second linter. The deferral applies only to this compatibility-limited lint layer; it does not remove ViDAP's later accessibility obligations.

## Alternatives considered

- **Force current ESLint 10 with JSX-a11y:** Rejected because the plugin's declared peer range excludes ESLint 10.
- **Use the ESLint 9 line:** Rejected because the reported current line is explicitly unsupported and would still leave the TypeScript 7 peer mismatch.
- **Keep TypeScript 7 and force TypeScript-ESLint:** Rejected because it would bypass declared compatibility rather than establish a supported quality harness.
- **Pause all of EP05:** Rejected because the remaining quality layers remain compatible and valuable.

## Consequences and tradeoffs

EP05 gains a maintained, peer-compatible TypeScript-aware ESLint path and retains compiler checking, formatting, tests, and Python quality checks. It does not gain automated JSX accessibility warnings in this packet. Because EP05 creates no visible React UI, this is a bounded, transparent deferral rather than a claim that accessibility has been completed.

The TypeScript 6.x selection must be rechecked from primary metadata immediately before installation. If no actively maintained compatible 6.x release is available, the revised packet must stop and return that evidence to Central.

## Validation evidence

`ViDAP_P0_EP05_Implementation_Report.md` preserves the dependency metadata and lock-restoration evidence for blocker B-EP05-001. The prior independent validator returned `Blocked` and did not modify or accept the work. A fresh worker and fresh validator must validate the revised packet; this decision does not approve implementation.

## Follow-up owners

- **Central:** revise P0-EP05 to version 0.2 and obtain explicit user approval before execution.
- **EP05 worker:** select and document the exact compatible TypeScript 6.x and current TypeScript-ESLint versions; do not install JSX-a11y.
- **Future Central packet:** reconsider JSX-a11y when a maintained release declares compatibility with the selected ESLint line and meaningful JSX UI exists to check.

## Supersession and revisit triggers

Revisit this decision when `eslint-plugin-jsx-a11y` declares maintained compatibility with the selected ESLint major, when a real React UI becomes authorized, or if the selected TypeScript 6.x/TypeScript-ESLint compatibility intersection ceases to be maintained.
