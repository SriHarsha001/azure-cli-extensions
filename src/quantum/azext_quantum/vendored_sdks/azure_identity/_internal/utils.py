# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
import os
import logging
from contextvars import ContextVar
from string import ascii_letters, digits
from typing import List, Optional

from urllib.parse import urlparse

from azure.core.exceptions import ClientAuthenticationError
from .._constants import EnvironmentVariables, KnownAuthorities

within_credential_chain = ContextVar("within_credential_chain", default=False)
within_dac = ContextVar("within_dac", default=False)

_LOGGER = logging.getLogger(__name__)

VALID_TENANT_ID_CHARACTERS = frozenset(ascii_letters + digits + "-.")
VALID_SCOPE_CHARACTERS = frozenset(ascii_letters + digits + "_-.:/")
VALID_SUBSCRIPTION_CHARACTERS = frozenset(ascii_letters + digits + "_-. ")


def normalize_authority(authority: str) -> str:
    """Ensure authority uses https, strip trailing spaces and /.

    :param str authority: authority to normalize
    :return: normalized authority
    :rtype: str
    :raises: ValueError if authority is not a valid https URL
    """

    parsed = urlparse(authority)
    if not parsed.scheme:
        return "https://" + authority.rstrip(" /")
    if parsed.scheme != "https":
        raise ValueError(
            "'{}' is an invalid authority. The value must be a TLS protected (https) URL.".format(authority)
        )

    return authority.rstrip(" /")


def get_default_authority() -> str:
    authority = os.environ.get(EnvironmentVariables.AZURE_AUTHORITY_HOST, KnownAuthorities.AZURE_PUBLIC_CLOUD)
    return normalize_authority(authority)


def validate_scope(scope: str) -> None:
    """Raise ValueError if scope is empty or contains a character invalid for a scope

    :param str scope: scope to validate
    :raises: ValueError if scope is empty or contains a character invalid for a scope.
    """
    if not scope or any(c not in VALID_SCOPE_CHARACTERS for c in scope):
        raise ValueError(
            "An invalid scope was provided. Only alphanumeric characters, '.', '-', '_', ':', and '/' are allowed."
        )


def validate_tenant_id(tenant_id: str) -> None:
    """Raise ValueError if tenant_id is empty or contains a character invalid for a tenant ID.

    :param str tenant_id: tenant ID to validate
    :raises: ValueError if tenant_id is empty or contains a character invalid for a tenant ID.
    """
    if not tenant_id or any(c not in VALID_TENANT_ID_CHARACTERS for c in tenant_id):
        raise ValueError(
            "Invalid tenant ID provided. You can locate your tenant ID by following the instructions here: "
            "https://learn.microsoft.com/partner-center/find-ids-and-domain-names"
        )


def validate_subscription(subscription: str) -> None:
    """Raise ValueError if subscription is empty or contains a character invalid for a subscription name/ID.

    :param str subscription: subscription ID to validate
    :raises: ValueError if subscription is empty or contains a character invalid for a subscription ID.
    """
    if not subscription or any(c not in VALID_SUBSCRIPTION_CHARACTERS for c in subscription):
        raise ValueError(
            "Invalid subscription provided. You can locate your subscription by following the "
            "instructions listed here: https://learn.microsoft.com/azure/azure-portal/get-subscription-tenant-id"
        )


def resolve_tenant(
    default_tenant: str,
    tenant_id: Optional[str] = None,
    *,
    additionally_allowed_tenants: Optional[List[str]] = None,
    **_
) -> str:
    """Returns the correct tenant for a token request given a credential's configuration.

    :param str default_tenant: The tenant ID configured on the credential.
    :param str tenant_id: The tenant ID requested by the user.
    :keyword list[str] additionally_allowed_tenants: The list of additionally allowed tenants.
    :return: The tenant ID to use for the token request.
    :rtype: str
    :raises: ~azure.core.exceptions.ClientAuthenticationError
    """
    if tenant_id is None or tenant_id == default_tenant:
        return default_tenant
    if default_tenant == "adfs" or os.environ.get(EnvironmentVariables.AZURE_IDENTITY_DISABLE_MULTITENANTAUTH):
        _LOGGER.info(
            "A token was request for a different tenant than was configured on the credential, "
            "but the configured value was used since multi tenant authentication has been disabled. "
            "Configured tenant ID: %s, Requested tenant ID %s",
            default_tenant,
            tenant_id,
        )
        return default_tenant
    if not default_tenant:
        return tenant_id
    if additionally_allowed_tenants is None:
        additionally_allowed_tenants = []
    if "*" in additionally_allowed_tenants or tenant_id in additionally_allowed_tenants:
        _LOGGER.info(
            "A token was requested for a different tenant than was configured on the credential, "
            "and the requested tenant ID was used to authenticate. Configured tenant ID: %s, "
            "Requested tenant ID %s",
            default_tenant,
            tenant_id,
        )
        return tenant_id
    raise ClientAuthenticationError(
        message="The current credential is not configured to acquire tokens for tenant {}. "
        "To enable acquiring tokens for this tenant add it to the additionally_allowed_tenants "
        'when creating the credential, or add "*" to additionally_allowed_tenants to allow '
        "acquiring tokens for any tenant.".format(tenant_id)
    )
