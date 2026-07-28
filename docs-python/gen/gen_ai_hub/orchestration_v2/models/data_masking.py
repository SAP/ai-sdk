# pylint: disable=duplicate-code
"""
Data Masking Module Configuration Models
"""

from enum import Enum
from typing import Optional, Union, List

from pydantic import Field, model_validator

from gen_ai_hub.orchestration_v2.models.base import ABCBaseModel as BaseModel


class DataMaskingProviderName(str, Enum):
    """
    Enumerates the available data masking providers.

    This enum defines the supported providers for masking sensitive data in the LLM module.

    Values: SAP_DATA_PRIVACY_INTEGRATION: Refers to the SAP Data Privacy Integration service, which offers
    anonymization and pseudonymization capabilities for sensitive data.
    """
    SAP_DATA_PRIVACY_INTEGRATION = "sap_data_privacy_integration"


class MaskingMethod(str, Enum):
    """
    Enumerates the supported masking methods.

    This enum defines the two main methods for masking sensitive information: anonymization and pseudonymization.
    Anonymization irreversibly removes sensitive data, while pseudonymization allows the original data to be recovered.

    Values:
        ANONYMIZATION: Irreversibly replaces sensitive data with placeholders (e.g., MASKED_ENTITY).

        PSEUDONYMIZATION: Replaces sensitive data with reversible placeholders (e.g., MASKED_ENTITY_ID).
    """
    ANONYMIZATION = "anonymization"
    PSEUDONYMIZATION = "pseudonymization"


class ProfileEntity(str, Enum):
    """
    Enumerates the entity categories that can be masked by the SAP Data Privacy Integration service.

    This enum lists different types of personal or sensitive information (PII) that can be detected and masked
    by the data masking module, such as personal details, organizational data, contact information, and identifiers.

    Values:
        PERSON: Represents personal names.

        ORG: Represents organizational names.

        UNIVERSITY: Represents educational institutions.

        LOCATION: Represents geographical locations.

        EMAIL: Represents email addresses.

        PHONE: Represents phone numbers.

        ADDRESS: Represents physical addresses.

        SAP_IDS_INTERNAL: Represents internal SAP identifiers.

        SAP_IDS_PUBLIC: Represents public SAP identifiers.

        URL: Represents URLs.

        USERNAME_PASSWORD: Represents usernames and passwords.

        NATIONAL_ID: Represents national identification numbers.

        IBAN: Represents International Bank Account Numbers.

        SSN: Represents Social Security Numbers.

        CREDIT_CARD_NUMBER: Represents credit card numbers.

        PASSPORT: Represents passport numbers.

        DRIVING_LICENSE: Represents driving license numbers.

        NATIONALITY: Represents nationality information.

        RELIGIOUS_GROUP: Represents religious group affiliation.

        POLITICAL_GROUP: Represents political group affiliation.

        PRONOUNS_GENDER: Represents pronouns and gender identity.

        GENDER: Represents gender information.

        SEXUAL_ORIENTATION: Represents sexual orientation.

        TRADE_UNION: Represents trade union membership.

        SENSITIVE_DATA: Represents any other sensitive information.
    """

    PERSON = "profile-person"
    ORG = "profile-org"
    UNIVERSITY = "profile-university"
    LOCATION = "profile-location"
    EMAIL = "profile-email"
    PHONE = "profile-phone"
    ADDRESS = "profile-address"
    SAP_IDS_INTERNAL = "profile-sapids-internal"
    SAP_IDS_PUBLIC = "profile-sapids-public"
    URL = "profile-url"
    USERNAME_PASSWORD = "profile-username-password"
    NATIONAL_ID = "profile-nationalid"
    IBAN = "profile-iban"
    SSN = "profile-ssn"
    CREDIT_CARD_NUMBER = "profile-credit-card-number"
    PASSPORT = "profile-passport"
    DRIVING_LICENSE = "profile-driverlicense"
    NATIONALITY = "profile-nationality"
    RELIGIOUS_GROUP = "profile-religious-group"
    POLITICAL_GROUP = "profile-political-group"
    PRONOUNS_GENDER = "profile-pronouns-gender"
    GENDER = "profile-gender"
    SEXUAL_ORIENTATION = "profile-sexual-orientation"
    TRADE_UNION = "profile-trade-union"
    SENSITIVE_DATA = "profile-sensitive-data"
    ETHNICITY = "profile-ethnicity"


class DPIMethodConstant(BaseModel):
    """
    Replaces the entity with the specified value followed by an incrementing number
    """
    method: str = "constant"
    value: str


class DPIMethodFabricatedData(BaseModel):
    """
    Replaces the entity with a randomly generated value appropriate to its type.
    """
    method: str = "fabricated_data"


class DPICustomEntity(BaseModel):
    """
    regex: Regular expression to match the entity
    replacement_strategy: Replacement strategy to be used for the entity
    """
    regex: str
    replacement_strategy: DPIMethodConstant


class DPIStandardEntity(BaseModel):
    """
    type: Standard entity type to be masked
    replacement_strategy: Replacement strategy to be used for the entity
    """
    type_: ProfileEntity = Field(..., alias="type")
    replacement_strategy: Optional[Union[DPIMethodConstant, DPIMethodFabricatedData]] = None


class MaskGroundingInput(BaseModel):
    """
    Controls whether the input to the grounding module will be masked with the configuration
    supplied in the masking module
    """
    enabled: bool = False


class MaskingProviderConfig(BaseModel):
    """
    SAP Data Privacy Integration provider for data masking.

    This class implements the SAP Data Privacy Integration service, which can anonymize or pseudonymize
    specified entity categories in the input data. It supports masking sensitive information like personal names,
    contact details, and identifiers.

    Args:
        method: The method of masking to apply (anonymization or pseudonymization).

        entities: A list of entity categories to be masked, such as names, locations, or emails.

        allowlist: A list of strings that should not be masked.

        mask_grounding_input: A flag indicating whether to mask input to the grounding module.
    """
    type_: DataMaskingProviderName = Field(default=DataMaskingProviderName.SAP_DATA_PRIVACY_INTEGRATION, alias="type")
    method: MaskingMethod
    entities: List[Union[DPIStandardEntity, DPICustomEntity]]
    allowlist: Optional[List[str]] = None
    mask_grounding_input: Optional[MaskGroundingInput] = None

class MaskingModuleConfig(BaseModel):
    """
    Configuration for the data masking module.

    Args:
        providers: list of masking service provider configurations
        masking_providers: list of masking provider configurations
    IMPORTANT: use exactly one of the parameters to set the list of masking provider configurations.
    DEPRECATED: parameter 'masking_providers' will be removed Sept 15, 2026. Use 'providers' instead.
    """
    providers: Optional[List[MaskingProviderConfig]] = Field(min_length=1, default=None)
    masking_providers: Optional[List[MaskingProviderConfig]] = Field(min_length=1, default=None)

    @model_validator(mode="after")
    def enforce_exactly_one_provider_list(self):

        has_providers = self.providers is not None
        has_masking_providers = self.masking_providers is not None

        if has_providers == has_masking_providers:
            raise ValueError(
                "MaskingModuleConfigProviders must set exactly one of: 'providers' or 'masking_providers' "
                "DEPRECATED: parameter 'masking_providers' will be removed Sept 15, 2026. Use 'providers' instead."
            )

        return self

__all__ = ["DataMaskingProviderName", "MaskingMethod", "ProfileEntity", "DPIMethodConstant", "DPIMethodFabricatedData",
           "DPICustomEntity", "DPIStandardEntity", "MaskGroundingInput", "MaskingProviderConfig", "MaskingModuleConfig"]