from __future__ import annotations

from typing import Any, Dict, Final, List, Optional, Callable, Tuple
import json
import os
import pathlib

from dataclasses import dataclass

from gen_ai_hub.evaluations.constants import (
    AI_CORE_PREFIX,
    AUTH_ENDPOINT_SUFFIX,
    CONFIG_FILE_ENV_VAR,
    PROFILE_ENV_VAR,
    VCAP_AICORE_SERVICE_NAME,
    VCAP_SERVICES_ENV_VAR,
    HOME_PATH_ENV_VAR,
    DEFAULT_HOME_PATH,
)
from gen_ai_hub.evaluations.helpers.logging import get_logger

logger = get_logger()


def get_home() -> str:
    return os.environ.get(HOME_PATH_ENV_VAR, DEFAULT_HOME_PATH)


def get_nested_value(data_dict, keys: List[str]):
    """
    Retrieve a nested value from a dictionary using a list of strings.

    :param data_dict: The dictionary to search.
    :param keys: A list of strings representing nested keys.
    :return: The value associated with the nested keys, or None if not found.
    """
    current_value = data_dict
    for key in keys:
        current_value = current_value[key]
    return current_value


@dataclass
class VCAPEnvironment:
    services: List[Service]

    @classmethod
    def from_env(cls, env_var: Optional[str] = None):
        env_var = env_var or VCAP_SERVICES_ENV_VAR
        env = json.loads(os.environ.get(env_var, '{}'))
        return cls.from_dict(env)

    @classmethod
    def from_dict(cls, env: Dict[str, Any]):
        services = [Service(service) for services in env.values() for service in services]
        return cls(services=services)

    def __getitem__(self, name) -> Service:
        return self.get_service(name, exactly_one=True)

    def get_service(self, label, exactly_one: bool = True) -> Service:
        services = [s for s in self.services if s.label == label]
        if exactly_one:
            if len(services) == 0:
                raise KeyError(f"No service found with label '{label}'.")
            return services[0]
        else:
            return services

    def get_service_by_name(self, name, exactly_one: bool = True) -> Service:
        services = [s for s in self.services if s.name == name]
        if exactly_one:
            if len(services) == 0:
                raise KeyError(f"No service found with name '{name}'.")
            return services[0]
        else:
            return services


NoDefault = object()


class Service:

    def __init__(self, env: Dict[str, Any]):
        self._env = env

    @property
    def label(self) -> Optional[str]:
        return self._env.get('label')

    @property
    def name(self) -> Optional[str]:
        return self._env.get('name')

    def __getitem__(self, key):
        return self.get(key)

    def get(self, key, default=NoDefault):
        if isinstance(key, str):
            key_splitted = key.split('.')
        else:
            key_splitted = key
        try:
            return get_nested_value(self._env, key_splitted) or default
        except KeyError:
            if default is NoDefault:
                raise KeyError(f"Key '{key}' not found in service '{self.name}'.")
            return default


@dataclass
class CredentialsValue:
    name: str
    vcap_key: Optional[Tuple[str, ...]] = None
    transform_fn: Optional[Callable] = None


@dataclass
class Source:
    name: str
    get: Callable[[CredentialsValue], Optional[str]]


CREDENTIAL_VALUES: Final[List[CredentialsValue]] = [
    CredentialsValue(name='client_id', vcap_key=('credentials', 'clientid')),
    CredentialsValue(name='client_secret', vcap_key=('credentials', 'clientsecret')),
    CredentialsValue(name='auth_url',
                     vcap_key=('credentials', 'url'),
                     transform_fn=lambda url: url.rstrip('/') +
                                              ('' if url.endswith(AUTH_ENDPOINT_SUFFIX) else AUTH_ENDPOINT_SUFFIX)),
    CredentialsValue(name='base_url',
                     vcap_key=('credentials', 'serviceurls', 'AI_API_URL'),
                     transform_fn=lambda url: url.rstrip('/') + ('' if url.endswith('/v2') else '/v2')),
    CredentialsValue(name='resource_group'),
    CredentialsValue(name='cert_url', vcap_key=('credentials', 'certurl'),
                     transform_fn=lambda url: url.rstrip('/') +
                                              ('' if url.endswith(AUTH_ENDPOINT_SUFFIX) else AUTH_ENDPOINT_SUFFIX)),
    # Even though the certificate and key in VCAP_SERVICES are not file paths, the names are defined this way in order
    # to keep it compatible with the config names. It'll be handled in fetch_credentials function.
    CredentialsValue(name='cert_file_path'),
    CredentialsValue(name='key_file_path'),
    CredentialsValue(name='cert_str', vcap_key=('credentials', 'certificate'),
                     transform_fn=lambda cert_str: cert_str.replace('\\n', '\n')),
    CredentialsValue(name='key_str', vcap_key=('credentials', 'key'),
                     transform_fn=lambda key_str: key_str.replace('\\n', '\n')),
    # Currently supporting only the AWS creds, would need to extend to other hyperscalers in future.
    CredentialsValue(name='aws_access_key_id'),
    CredentialsValue(name='aws_secret_access_key'),
    CredentialsValue(name='orchestration_url'),
    CredentialsValue(name='input_object_store_secret_name'),
]


def init_conf(profile: str = None):
    # Read configuration from ${AICORE_HOME}/config_<profile>.json.
    home = pathlib.Path(get_home())
    profile = profile or os.environ.get(PROFILE_ENV_VAR)
    profile_config_file = f'config_{profile}.json'
    direct_config_file = pathlib.Path(os.getenv(CONFIG_FILE_ENV_VAR)) if os.getenv(CONFIG_FILE_ENV_VAR) else None
    path_to_config = (direct_config_file or
                      (home / ('config.json' if profile in ('default', '', None) else profile_config_file)))
    config = {}
    if path_to_config.exists():
        logger.debug('Config file path %s', path_to_config)
        try:
            with path_to_config.open(encoding='utf-8') as f:
                return json.load(f)
        except json.decoder.JSONDecodeError:
            raise KeyError(f'{path_to_config} is not a valid json file. Please fix or remove it!')
        except PermissionError as e:
            logger.warning("Permission denied when trying to read config file '%s'. File ignored.", path_to_config)
            return config
    elif profile:
        raise FileNotFoundError(f"Unable to locate profile config file '{profile_config_file}' "
                                f"in AICORE_HOME '{home}')")
    return config


def extract_credentials(source: Source, exclude: List[str] = None) -> Dict[str, str]:
    """Extract all credentials from a source."""
    exclude = exclude or []
    credentials = {}
    for cv in CREDENTIAL_VALUES:
        if cv.name in exclude:
            continue
        if value := source.get(cv):
            credentials[cv.name] = cv.transform_fn(value) if cv.transform_fn else value
    return credentials


def resolve_credentials(sources: List[Source]) -> Dict[str, str]:
    """Extract credentials from the first source that has any defined."""
    for source in sources:
        if credentials := extract_credentials(source, exclude=['resource_group']):
            logger.debug(f"Using credentials from: {source.name}")
            return credentials
    raise ValueError("No credentials found in any source")


def resolve_resource_group(sources: List[Source]) -> Optional[str]:
    """Find resource_group from the first source that defines it."""
    rg_cred = CredentialsValue(name='resource_group')
    for source in sources:
        if value := source.get(rg_cred):
            logger.debug("Using resource_group '%s' from: %s", value, source.name)
            return value
    logger.debug("No resource_group found in any source")
    return None


def validate_credentials(credentials: Dict[str, str]) -> None:
    """Validate that we have a complete authentication method."""
    required_base = {'client_id', 'auth_url', 'base_url'}

    # Check which auth method we have
    has_client_secret = 'client_secret' in credentials
    has_cert_files = 'cert_file_path' in credentials and 'key_file_path' in credentials
    has_cert_strings = 'cert_str' in credentials and 'key_str' in credentials

    # Must have exactly one auth method
    auth_methods = sum([has_client_secret, has_cert_files, has_cert_strings])

    if auth_methods == 0:
        raise ValueError(
            "No authentication method found. Must provide one of:\n"
            "1. client_secret\n"
            "2. cert_file_path AND key_file_path\n"
            "3. cert_str AND key_str"
        )

    if auth_methods > 1:
        raise ValueError(
            "Multiple authentication methods found. Please provide only one of:\n"
            "1. client_secret\n"
            "2. cert_file_path AND key_file_path\n"
            "3. cert_str AND key_str"
        )

    # Check required base fields
    missing = required_base - set(credentials.keys())
    if missing:
        raise ValueError(f"Missing required credentials: {missing}")


def _str_or_none(value) -> Optional[str]:
    return str(value) if value else None


def fetch_credentials(profile: str = None, **kwargs) -> Dict[str, str]:
    """
    Fetch credentials from a single source based on precedence.

    Precedence order: kwargs > environment variables > config file > VCAP service

    Once a source is selected (first one with any credential), all credentials
    come from that source only. Resource group is an exception and follows
    precedence independently.
    """
    config = init_conf(profile=profile)

    try:
        vcap_service = VCAPEnvironment.from_env()[VCAP_AICORE_SERVICE_NAME]
    except KeyError:
        vcap_service = None

    sources = [
        Source("kwargs",
               lambda cv: _str_or_none(kwargs.get(cv.name))),
        Source("environment variables",
               lambda cv: _str_or_none(os.environ.get(f'{AI_CORE_PREFIX}_{cv.name.upper()}'))),
        Source("config file",
               lambda cv: _str_or_none(config.get(f'{AI_CORE_PREFIX}_{cv.name.upper()}'))),
        Source("VCAP service",
               lambda cv: _str_or_none(vcap_service.get(cv.vcap_key, None) if vcap_service and cv.vcap_key else None)),
    ]

    credentials = resolve_credentials(sources)

    # Use cert_url as auth_url if present (VCAP provides cert_url for certificate auth)
    if 'cert_url' in credentials:
        credentials['auth_url'] = credentials.pop('cert_url')

    validate_credentials(credentials)

    resource_group = resolve_resource_group(sources)
    if resource_group:
        credentials['resource_group'] = resource_group

    return credentials
