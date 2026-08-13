#!/usr/bin/env bash
# ============================================================================
# FieldCommand IMS — TLS certificate generator
# ============================================================================
# Creates the certificate nginx uses to serve the dashboard over HTTPS on the
# closed EMCOMM-NET LAN (no public domain, so no public CA is possible).
#
# Two modes:
#   local-CA (default)  — creates a private root CA, then a server certificate
#                         signed by it. Install the root (fieldcommand-ca.crt)
#                         on devices ONCE and they show a clean padlock, no
#                         warning. Best for the imaged Pi 500 workstations.
#   --self-signed       — a single self-signed server certificate. No root to
#                         distribute, but every device shows a one-time
#                         "not secure" warning to accept.
#
# The certificate's Subject Alternative Name (SAN) includes the server IP, so
# modern browsers accept it for https://192.168.50.1.
#
# Usage:
#   sudo bash fc-gen-cert.sh                 # local-CA, default IP/host
#   sudo bash fc-gen-cert.sh --self-signed
#   sudo bash fc-gen-cert.sh --ip 192.168.50.1 --host fieldcommand.local
#   sudo bash fc-gen-cert.sh --force         # regenerate (invalidates trust)
# ============================================================================
set -euo pipefail

TLS_DIR="${FC_TLS_DIR:-/etc/fieldcommand/tls}"
PUB_DIR="${FC_PUB_DIR:-/opt/fieldcommand/html}"   # where the CA root is published for download
IP="192.168.50.1"
HOST="fieldcommand.local"
MODE="local-ca"
FORCE=0
DAYS=3650   # ~10 years, so field units never silently expire

while [[ $# -gt 0 ]]; do
    case "$1" in
        --self-signed) MODE="self-signed"; shift ;;
        --ip)          IP="$2"; shift 2 ;;
        --host)        HOST="$2"; shift 2 ;;
        --dir)         TLS_DIR="$2"; shift 2 ;;
        --pubdir)      PUB_DIR="$2"; shift 2 ;;
        --days)        DAYS="$2"; shift 2 ;;
        --force)       FORCE=1; shift ;;
        -h|--help)     grep -E '^#( |$)' "$0" | sed -E 's/^# ?//'; exit 0 ;;
        *) echo "Unknown option: $1" >&2; exit 2 ;;
    esac
done

command -v openssl >/dev/null 2>&1 || { echo "openssl not found — install it first (apt-get install openssl)"; exit 1; }

mkdir -p "$TLS_DIR"; chmod 700 "$TLS_DIR"
SRV_CRT="$TLS_DIR/server.crt"
SRV_KEY="$TLS_DIR/server.key"
CA_CRT="$TLS_DIR/fieldcommand-ca.crt"
CA_KEY="$TLS_DIR/fieldcommand-ca.key"

if [[ -f "$SRV_CRT" && -f "$SRV_KEY" && "$FORCE" != "1" ]]; then
    echo "Certificate already present at $SRV_CRT — leaving it in place."
    echo "(Use --force to regenerate; this invalidates any already-installed trust.)"
    exit 0
fi

SAN="subjectAltName=IP:${IP},IP:127.0.0.1,DNS:${HOST},DNS:localhost"

if [[ "$MODE" == "self-signed" ]]; then
    echo "==> Generating a self-signed certificate for ${IP} (${HOST})…"
    openssl req -x509 -newkey rsa:2048 -nodes \
        -keyout "$SRV_KEY" -out "$SRV_CRT" -days "$DAYS" \
        -subj "/O=FieldCommand IMS/CN=${HOST}" \
        -addext "$SAN" \
        -addext "keyUsage=digitalSignature,keyEncipherment" \
        -addext "extendedKeyUsage=serverAuth"
else
    echo "==> Generating a private local Certificate Authority (root)…"
    if [[ ! -f "$CA_CRT" || ! -f "$CA_KEY" || "$FORCE" == "1" ]]; then
        openssl req -x509 -newkey rsa:4096 -nodes \
            -keyout "$CA_KEY" -out "$CA_CRT" -days "$DAYS" \
            -subj "/O=FieldCommand IMS/CN=FieldCommand IMS Local Root CA" \
            -addext "basicConstraints=critical,CA:TRUE" \
            -addext "keyUsage=critical,keyCertSign,cRLSign"
    else
        echo "    (reusing existing root CA — devices that already trust it stay valid)"
    fi

    echo "==> Generating the server certificate signed by the local CA…"
    openssl req -newkey rsa:2048 -nodes \
        -keyout "$SRV_KEY" -out "$TLS_DIR/server.csr" \
        -subj "/O=FieldCommand IMS/CN=${HOST}"
    EXT="$TLS_DIR/server.ext"
    {
        echo "$SAN"
        echo "basicConstraints=CA:FALSE"
        echo "keyUsage=digitalSignature,keyEncipherment"
        echo "extendedKeyUsage=serverAuth"
    } > "$EXT"
    openssl x509 -req -in "$TLS_DIR/server.csr" \
        -CA "$CA_CRT" -CAkey "$CA_KEY" -CAcreateserial \
        -out "$TLS_DIR/server.leaf.crt" -days "$DAYS" -extfile "$EXT"
    # nginx wants leaf + issuer chain in one file
    cat "$TLS_DIR/server.leaf.crt" "$CA_CRT" > "$SRV_CRT"
    rm -f "$TLS_DIR/server.csr" "$EXT" "$TLS_DIR/server.leaf.crt"

    # Publish the CA root so operators can download and install it on their devices.
    if [[ -d "$PUB_DIR" ]]; then
        cp "$CA_CRT" "$PUB_DIR/fieldcommand-ca.crt" 2>/dev/null || true
        echo "    Root CA published for device install: ${PUB_DIR}/fieldcommand-ca.crt"
        echo "    (also reachable at https://${IP}/fieldcommand-ca.crt once HTTPS is up)"
    fi
fi

chmod 600 "$SRV_KEY"; [[ -f "$CA_KEY" ]] && chmod 600 "$CA_KEY"
chmod 644 "$SRV_CRT"; [[ -f "$CA_CRT" ]] && chmod 644 "$CA_CRT"

echo "==> Done."
echo "    Certificate: $SRV_CRT"
echo "    Private key: $SRV_KEY"
[[ "$MODE" == "local-ca" ]] && echo "    Root CA:     $CA_CRT  (install on devices for a warning-free padlock)"
echo "    Point nginx at these (ssl_certificate / ssl_certificate_key) and reload."
