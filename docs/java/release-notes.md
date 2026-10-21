# Release Notes

[![Maven Central Version](https://img.shields.io/maven-central/v/com.sap.ai.sdk/core?color=dark-green)](https://central.sonatype.com/search?smo=true\&namespace=com.sap.ai.sdk)

## Should I update?[​](#should-i-update "Direct link to Should I update?")

We highly recommend regularly updating to the latest SAP Cloud SDK for AI version. It will help you:

* Ensure access to the latest SAP Cloud SDK for AI features
* Keep up with the latest changes in SAP ecosystem
* Protect yourself from bugs and breaking changes in the future

## 2.0.0 - October 20, 2026[​](#200---october-20-2026 "Direct link to 2.0.0 - October 20, 2026")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F2.0.0)

### 🔧 Compatibility Notes[​](#-compatibility-notes "Direct link to 🔧 Compatibility Notes")

See the [migration guide](/ai-sdk/docs/java/migration-guide.md).

### ✨ New Functionality[​](#-new-functionality "Direct link to ✨ New Functionality")

* \[Orchestration] Added new models `GPT_51`, `GPT_6_ASTRA`, `GPT_6_LUNA`, `GPT_61_SOL`, and `QWEN_3_8_MAX` to `OrchestrationModel`.
* \[OpenAI] Added new models `GPT_51`, `GPT_6_ASTRA`, `GPT_6_LUNA`, `GPT_61_SOL` to `OpenAiModel`.

## 2.0.0-M1 - September 25, 2026[​](#200-m1---september-25-2026 "Direct link to 2.0.0-M1 - September 25, 2026")

[All Release Changes](https://github.com/SAP/ai-sdk-java/releases/tag/rel%2F2.0.0-M1)

### 🔧 Compatibility Notes[​](#-compatibility-notes-1 "Direct link to 🔧 Compatibility Notes")

See the [migration guide](/ai-sdk/docs/java/migration-guide.md).

### ✨ New Functionality[​](#-new-functionality-1 "Direct link to ✨ New Functionality")

* \[Orchestration] Added `GEMINI_3_8_FLASH` and `GPT_51` to model list in `OrchestrationAiModel`.
* \[OpenAI] Added `GPT_51` to model list in `OpenAiModel`.
* \[Spring AI] Chat completion calls via the Spring AI integration now can have multiple module configs to support fallback modules as well.
