# Release Policy

The SAP Cloud SDK for AI follows [semantic versioning](https://semver.org/).

## Planned Major Release Schedule[​](#planned-major-release-schedule "Direct link to Planned Major Release Schedule")

| Version | Status     | Release Date   | End of Life   |
| ------- | ---------- | -------------- | ------------- |
| 1.x     | Deprecated | September 2024 | February 2026 |
| 2.x     | Released   | September 2025 | TBD           |

### Upgrading to a New Major Version[​](#upgrading-to-a-new-major-version "Direct link to Upgrading to a New Major Version")

* We provide a step-by-step [upgrade guide](/ai-sdk/docs/js/upgrade-guide.md) for each major version.
* Following the upgrade steps should take less than a day of development effort regardless of the project size.

### Fixes and Maintenance[​](#fixes-and-maintenance "Direct link to Fixes and Maintenance")

* We provide new features and fixes only for the **latest major release** of the SAP Cloud SDK for AI.

## Minor Release Policy[​](#minor-release-policy "Direct link to Minor Release Policy")

We release a new **minor version** every 2 weeks, assuming new functionality or fixes are available.

### Upgrading to a New Minor Version[​](#upgrading-to-a-new-minor-version "Direct link to Upgrading to a New Minor Version")

Upgrading to a new **minor release version** should not involve any effort because we do not introduce breaking changes.

TypeScript version bumps

We regularly upgrade TypeScript to the latest stable version. In rare cases this can lead to compilation errors for projects using TypeScript. The solution is usually upgrading TypeScript to the latest stable version.
