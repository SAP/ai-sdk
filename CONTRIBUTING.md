# Contributing to the SAP Cloud SDK for AI Documentation Portal

## Prerequisites

- [Node.js](https://nodejs.org/en/download/).
  We recommend the latest LTS version of node.js.
  Check your version with `node -v`.
  You can use [`nvm`](https://github.com/nvm-sh/nvm) for managing multiple Node versions on a single machine.

## Hosting the Documentation Locally

- Run `npm install`
- Run `npm start`
- The SAP Cloud SDK for AI documentation portal should open in a new browser window

### How To Document

The markdown files for the documentation are in the `docs` directory.
Add or change an article and create a pull request.

### Docker Alternative

- Consider the following commands (1) to install node dependencies and (2) to serve the continuously generated site:

  ```bash
  docker run -it --rm -v "${pwd}:/doc" -w "/doc" --entrypoint "/bin/sh" node:alpine3.10 -c "npm ci"
  docker run -it --rm -v "${pwd}:/doc" -w "/doc" --entrypoint "/bin/sh" -p 3000:3000 node:alpine3.10 -c "npm run start -- --port 3000 --host 0.0.0.0"
  ```

<!-- vale off -->
## Dos and Don'ts

- Be concise.
- Put each sentence on its own line to keep the changelogs clean.
- Avoid abbreviations or introduce them unless it's obvious and widely adopted.
- Don't sell your features, explain them.
- Use simple words and short sentences.
- Avoid statements about the complexity (e.g. "simply do this") as it can be discouraging for less-experienced readers.
- Add meaningful examples wherever possible.
- Add links whenever you mention a third party resource.
- Build upon already available content and use it for reference.
- Write incrementally.

<!-- vale on -->

## Linting and Formatting

### Vale

Vale is a command-line tool that brings code-like linting to prose.
This repository has a special configuration to enforce a consistent style.

To use Vale locally, install it via your package manager.

```bash
# macos / linux
$ brew install vale
# windows
$ choco install vale
```

If you use Microsoft Visual Studio Code, you can use the official [Vale plugin](https://marketplace.visualstudio.com/items?itemName=errata-ai.vale-server) to get hints in your editor.
Once installed, add the following lines to your configuration.

```json
{
  "vale.core.useCLI": true,
  "vale.valeCLI.path": "/usr/local/bin/vale"
}
```

### ESLint and Prettier

Please use [ESLint](https://eslint.org) and [Prettier](https://prettier.io/) to keep the markdown files and code examples consistently formatted.

```bash
# Install dependencies including ESLint and Prettier
$ npm install
# Run ESLint and Prettier
$ npm run lint
# Fix ESLint and Prettier issues automatically
$ npm run lint:fix
```

### External Grammar Checker

There is no automated grammar checker, but there are free online grammar checkers available.
Examples are [Grammarly](https://app.grammarly.com/) or [Hemingway](http://www.hemingwayapp.com/).
Since you upload your text to their servers, you may only upload content with `PUBLIC` designation.

Please check your text manually with one of the mentioned tools before creating a pull request.

## Contributing as a Team Member

1. Go to: https://opensource-portal.tools.sap.corp/
2. Search for the `cloud-sdk-team` and ask colleagues to add you.

Once you are part of the team, you can submit `pull requests` without forking the repository.

## Developer Certificate of Origin (DCO)

Due to legal reasons, contributors will be asked to accept a DCO before they submit the first pull request to this project.
This happens in an automated fashion during the submission process.
SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).

## Contributing with AI-generated Code

As artificial intelligence evolves, AI-generated code is becoming valuable for many software projects, including open-source initiatives.
While we recognize the potential benefits of incorporating AI-generated content into our open-source projects there a certain requirements that need to be reflected and adhered to when making contributions.

Please see our [Guideline for AI-generated code contributions to SAP Open Source Software Projects](https://github.com/SAP/.github/blob/main/CONTRIBUTING_USING_GENAI.md) for more details.

## Code of Conduct

All members of the project community must abide by the [SAP Open Source Code of Conduct](https://github.com/SAP/.github/blob/main/CODE_OF_CONDUCT.md).
Only by respecting each other we can develop a productive, collaborative community.
Instances of abusive, harassing, or otherwise unacceptable behavior may be reported by contacting [a project maintainer](.reuse/dep5).

## Engaging in Our Project

We use GitHub to manage reviews of pull requests.

* If you are a new contributor, see: [Steps to Contribute](#steps-to-contribute)

* Before implementing your change, create an issue that describes the problem you would like to solve or the code that should be enhanced. Please note that you are willing to work on that issue.

* The team will review the issue and decide whether it should be implemented as a pull request. In that case, they will assign the issue to you. If the team decides against picking up the issue, the team will post a comment with an explanation.

## Steps to Contribute

Should you wish to work on an issue, please claim it first by commenting on the GitHub issue that you want to work on.
This is to prevent duplicated efforts from other contributors on the same issue.

If you have questions about one of the issues, please comment on them, and one of the maintainers will clarify.

## Contributing Code or Documentation

You are welcome to contribute code in order to fix a bug or to implement a new feature that is logged as an issue.

The following rule governs code contributions:

* Contributions must be licensed under the [Apache 2.0 License](./LICENSE).
* Due to legal reasons, contributors will be asked to accept a Developer Certificate of Origin (DCO) when they create the first pull request to this project. This happens in an automated fashion during the submission process. SAP uses [the standard DCO text of the Linux Foundation](https://developercertificate.org/).
* Contributions must follow our [guidelines on AI-generated code](https://github.com/SAP/.github/blob/main/CONTRIBUTING_USING_GENAI.md) in case you are using such tools.

## Issues and Planning

* We use GitHub issues to track bugs and enhancement requests.

* Please provide as much context as possible when you open an issue. The information you provide must be comprehensive enough to reproduce that issue for the assignee.
