const baseUrl = '/ai-sdk/docs';
const YES = ':heavy_check_mark:';
const NO = ':x:';
const PLANNED = ':date:';
const DEPRECATED = ':warning:';
const BETA = ':gear:';
const FEATURE_REQUEST =
  '[Request this feature](https://github.com/SAP/ai-sdk/issues/new?assignees=&labels=feature+request&template=feature_request.md&title=)';
/**
 * Global SDK feature list.
 */
export const features = [
  {
    name: '[SOAP](https://help.sap.com/saphelp_snc700_ehp01/helpdata/en/bb/ddb33d2ae46b3be10000000a114084/content.htm?no_cache=true)',
    java: {
      status: NO,
      docsLink: ``,
      note: 'Out of scope. Deprecated since 4.13.0'
    },
    js: {
      status: NO,
      docsLink: ``,
      note: 'Take a look at the [node-soap](https://github.com/vpulim/node-soap) library'
    }
  }
];
