const baseUrl = '/ai-sdk/docs';
const YES = ':white_check_mark:';
const NO = ':x:';
const PLANNED = ':date:';
const DEPRECATED = ':warning:';
const WIP = ':wrench:';
const FEATURE_REQUEST =
  '[Request this feature](https://github.com/SAP/ai-sdk/issues/new?assignees=&labels=feature+request&template=feature_request.md&title=)';
/**
 * Global SDK feature list.
 */
export const features = [
  {
    name: 'Orchestration: [Chat Completion](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/chat?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/orchestration/chat-completion)`
    },
    js: {
      status: YES,
      docsLink: ``
    }
  },
  {
    name: 'Orchestration: [Harmonized API](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/harmonized-api?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/orchestration/chat-completion#harmonized-api)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/orchestration/chat-completion#harmonized-api)`
    }
  },
  {
    name: 'Orchestration: [Templating](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/templating?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/orchestration/chat-completion#templating)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/orchestration/chat-completion#templating)`
    }
  },
  {
    name: 'Orchestration: [Input Image Support](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/templating?locale=en-US#input-image-support)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/orchestration/chat-completion#using-images)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/orchestration/chat-completion#image-recognition)`
    }
  },
  {
    name: 'Orchestration: [Streaming](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/streaming?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/orchestration/chat-completion#streaming)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/orchestration/chat-completion#streaming)`
    }
  },
  {
    name: 'Orchestration: [Input Filter](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/input-filtering?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/orchestration/chat-completion#filtering)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/orchestration/chat-completion#content-filtering)`
    }
  },
  {
    name: 'Orchestration: [Output Filter](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/output-filtering?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/orchestration/chat-completion#filtering)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/orchestration/chat-completion#content-filtering)`
    }
  },
  {
    name: 'Orchestration: [Data Masking](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/data-masking?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/orchestration/chat-completion#masking)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/orchestration/chat-completion#data-masking)`
    }
  },
  {
    name: 'Orchestration: [Grounding](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/grounding?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/orchestration/chat-completion#grounding)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/orchestration/chat-completion#grounding)`
    }
  },
  {
    name: 'Orchestration: [Prompt Registry](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/prompt-registry?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/ai-core/prompt-registry)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/orchestration/chat-completion#prompt-registry)`
    }
  },
  {
    name: '[AI Core API](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/about-ai-api?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/ai-core/ai-core-deployment)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/ai-core/ai-api)`
    }
  },
  {
    name: '[Document Grounding API](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/grounding?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/ai-core/document-grounding)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/ai-core/document-grounding)`
    }
  },
  {
    name: '[Prompt Registry API](https://help.sap.com/docs/sap-ai-core/sap-ai-core-service-guide/prompt-registry?locale=en-US)',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/ai-core/prompt-registry)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/ai-core#prompt-registry)`
    }
  },
  {
    name: 'Framework Integration: LangChain/Spring AI for Orchestration',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/spring-ai/orchestration)`
    },
    js: {
      status: YES,
      docsLink: ``
    }
  },
  {
    name: 'Framework Integration: LangChain/Spring AI for Foundation Model',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/spring-ai/openai)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/langchain)`
    }
  },
  {
    name: 'Foundation Model: OpenAI Chat Completion',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/foundation-models/openai/chat-completion)`
    },
    js: {
      status: YES,
      docsLink: ``
    }
  },
  {
    name: 'Foundation Model: OpenAI Streaming',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/foundation-models/openai/chat-completion#stream-chat-completion)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/foundation-models/openai/chat-completion#streaming)`
    }
  },
  {
    name: 'Foundation Model: OpenAI Embedding',
    java: {
      status: YES,
      docsLink: `[docs](${baseUrl}/java/foundation-models/openai/embedding)`
    },
    js: {
      status: YES,
      docsLink: `[docs](${baseUrl}/js/foundation-models/openai/embedding)`
    }
  }
];
