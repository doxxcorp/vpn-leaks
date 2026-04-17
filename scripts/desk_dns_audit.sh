#!/usr/bin/env bash
# Phase-8-style DNS/email audit for one or more apex domains (systematic desk, S tier).
# Paste stdout into research/desk-<date>-<apex>.txt or a report appendix.
# Does not replace vpn-leaks run; do not treat as O (observed during tunnel).
# See docs/website-exposure-methodology.md Appendix D.
set -euo pipefail

if [ "$#" -eq 0 ]; then
  echo "Usage: $0 <domain> [domain ...]" >&2
  exit 1
fi

for DOMAIN in "$@"; do
  echo "########################################"
  echo "# DOMAIN: ${DOMAIN}"
  echo "# UTC: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  echo "########################################"
  echo ""

  for rtype in NS A AAAA MX TXT CAA SOA; do
    echo "=== ${rtype} ${DOMAIN} ==="
    dig +short "${DOMAIN}" "${rtype}" || true
    echo ""
  done

  echo "=== SPF (TXT grep) ==="
  dig +short TXT "${DOMAIN}" | grep -i spf || true
  echo ""

  echo "=== DMARC ==="
  dig +short TXT "_dmarc.${DOMAIN}" || true
  echo ""

  echo "=== DKIM (common selectors) ==="
  for sel in google zendesk1 zendesk2 default s1 s2 k1 selector1 selector2; do
    r=$(dig +short TXT "${sel}._domainkey.${DOMAIN}" 2>/dev/null || true)
    if [ -n "${r}" ]; then
      echo "DKIM [${sel}]: ${r}"
    fi
  done
  echo ""

  echo "=== Subdomain CNAME (common names) ==="
  for sub in mail support help status blog docs api autodiscover; do
    c=$(dig +short CNAME "${sub}.${DOMAIN}" || true)
    if [ -n "${c}" ]; then
      echo "${sub}.${DOMAIN} -> ${c}"
    fi
  done
  echo ""
done
