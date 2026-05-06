"""TLS certificate chain probe (TASK-11).

For each SNI hostname seen on the wire, perform a single TLS handshake to
retrieve the leaf certificate and report the issuer. The issuing CA appears in
public Certificate Transparency logs and answers OCSP revocation checks for
every connection — this is a real third-party visibility surface that the
client cannot avoid for HTTPS hosts.

Fail-soft: any per-host error is captured as ``{"hostname": h, "error": str}``.
"""

from __future__ import annotations

import socket
import ssl
from typing import Any


def _parse_der_certificate(der: bytes) -> dict[str, Any]:
    """Parse a DER-encoded leaf certificate using ``cryptography`` if installed,
    else fall back to pyOpenSSL, else return empty fields. Fail-soft.
    """
    out: dict[str, Any] = {
        "issuer_cn": "",
        "issuer_o": "",
        "ocsp_url": None,
        "valid_from": "",
        "valid_until": "",
    }
    try:
        from cryptography import x509
        from cryptography.x509.oid import (
            AuthorityInformationAccessOID,
            ExtensionOID,
            NameOID,
        )
    except ImportError:
        return out
    try:
        cert = x509.load_der_x509_certificate(der)
    except Exception:
        return out

    try:
        for attr in cert.issuer:
            if attr.oid == NameOID.COMMON_NAME and not out["issuer_cn"]:
                out["issuer_cn"] = str(attr.value)
            if attr.oid == NameOID.ORGANIZATION_NAME and not out["issuer_o"]:
                out["issuer_o"] = str(attr.value)
    except Exception:
        pass

    try:
        nb = cert.not_valid_before_utc
        out["valid_from"] = nb.isoformat()
    except (AttributeError, ValueError):
        try:
            out["valid_from"] = cert.not_valid_before.isoformat() + "Z"
        except (AttributeError, ValueError):
            pass
    try:
        na = cert.not_valid_after_utc
        out["valid_until"] = na.isoformat()
    except (AttributeError, ValueError):
        try:
            out["valid_until"] = cert.not_valid_after.isoformat() + "Z"
        except (AttributeError, ValueError):
            pass

    try:
        ext = cert.extensions.get_extension_for_oid(
            ExtensionOID.AUTHORITY_INFORMATION_ACCESS,
        )
        for desc in ext.value:
            if desc.access_method == AuthorityInformationAccessOID.OCSP:
                out["ocsp_url"] = str(desc.access_location.value)
                break
    except Exception:
        pass

    return out


def probe_tls_chain(hostname: str, *, port: int = 443, timeout: float = 5.0) -> dict[str, Any]:
    """Connect to ``hostname:port``, retrieve the leaf certificate metadata.

    Returns ``{hostname, issuer_cn, issuer_o, root_ca, ocsp_url, valid_from,
    valid_until, error}``. The DER bytes are parsed via the ``cryptography``
    library because Python's stdlib ``ssl.getpeercert(binary_form=False)``
    returns ``{}`` when ``verify_mode = CERT_NONE`` (which we must use to
    avoid false-failures on hosts that present non-public CAs or weren't named
    in the harness's trust store).
    """
    result: dict[str, Any] = {
        "hostname": hostname,
        "issuer_cn": "",
        "issuer_o": "",
        "root_ca": "",
        "ocsp_url": None,
        "valid_from": "",
        "valid_until": "",
        "error": None,
    }
    if not hostname or hostname == "—":
        result["error"] = "empty_hostname"
        return result

    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    der: bytes
    try:
        with socket.create_connection((hostname, port), timeout=timeout) as sock:
            with ctx.wrap_socket(sock, server_hostname=hostname) as ssock:
                der = ssock.getpeercert(binary_form=True) or b""
    except (OSError, ssl.SSLError, TimeoutError, ValueError) as e:
        result["error"] = type(e).__name__ + ":" + str(e)[:160]
        return result

    if not der:
        result["error"] = "empty_certificate"
        return result

    parsed = _parse_der_certificate(der)
    result.update(parsed)
    result["root_ca"] = result["issuer_o"] or result["issuer_cn"]
    return result
