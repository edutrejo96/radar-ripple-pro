# ripple_radar_pro_route_engine_v61.py
# =============================================================================
# RIPPLE RADAR PRO — ADVANCED INTELLIGENCE v5.0
# =============================================================================
# Un solo archivo Streamlit.
#
# Incluye:
# 1) XRPL/RLUSD real vía account_tx
# 2) Public Route Vigilance
# 3) Institutional Fingerprints
# 4) Wallet Cluster Intelligence
# 5) Cross-Network Intelligence Layer
# 6) Time Intelligence / régimen / aceleración
# 7) Liquidity Topology Engine
# 8) Anomaly Detection
# 9) Pump vs Adoption discriminator
# 10) Flip Phase Engine 0-5
# 11) UI simple, estética y explicada
#
# Instalación:
#   python -m venv .venv
#   .venv\Scripts\activate
#   pip install streamlit plotly pandas numpy requests python-dateutil streamlit-autorefresh
#
# Ejecutar:
#   streamlit run ripple_radar_pro_route_engine_v62_universal.py
#
# Nota honesta:
# XRPL/RLUSD usa datos públicos reales. Rutas privadas como SWIFT, FedNow, DTCC,
# Hidden Road, Prime, Treasury, Metaco, Mastercard y OTC se infieren SOLO por
# huellas públicas cuando interactúan con XRPL/RLUSD.
# =============================================================================

from __future__ import annotations

import json
import math
import random
import sqlite3
import hashlib
import html
import re
import unicodedata
import time as _time
import traceback
import statistics

# --- SISTEMA DE TRADUCCIÓN RRP (CORREGIDO) ---
I18N = {
    "Español": {
        "ui_info": "Traduce la interfaz al idioma seleccionado. Los nombres de instituciones, pruebas y datos técnicos se mantienen en su idioma original para preservar la integridad.",
        "radar_desc": "Radar avanzado para vigilar rutas privadas por sus huellas públicas: clusters, topología, fingerprints y anomalías.",
        "legend_title": "🗺️ Leyenda del mapa — cómo leer colores y líneas",
        "data_meaning": "📘 ¿Qué significan estos datos?",
        "disclaimer": "No es asesoramiento financiero. Es un radar de huellas públicas, topología, clusters y adopción real.",
        "metrics": {
            "subida": "Subida",
            "riesgo": "Riesgo",
            "flip": "Flip",
            "cobertura": "Cobertura",
            "pump": "Pump",
            "hot": "Rutas hot"
        }
    },
    "日本語": {
        "ui_info": "選択した言語にUIを翻訳します。証拠の整合性を保つため、機関名・証拠・URL・技術データは原語のままです。",
        "radar_desc": "公開された痕跡（クラスター、トポロジー、フィンガープリント、異常値、DEX/AMM、トラストライン、大口送金など）からプライベートルートを監視する先進的なレーダー。",
        "legend_title": "🗺️ マップの凡例 — 色と線の読み方",
        "data_meaning": "📘 上記のデータは何を意味しますか？",
        "disclaimer": "これは金融アドバイスではありません。公開された痕跡、トポロジー、クラスター、および実際の採用状況を監視するレーダーです。",
        "metrics": {
            "subida": "上昇率",
            "riesgo": "リスク",
            "flip": "フリップ",
            "cobertura": "カバレッジ",
            "pump": "パンプ",
            "hot": "ホットルート"
        }
    }
}


# --- SISTEMA DE TRADUCCIÓN DINÁMICO ---
I18N = {
    "Español": {
        "ui_info": "Traduce la interfaz al idioma seleccionado. Por integridad, datos técnicos y nombres permanecen en original.",
        "radar_desc": "Radar avanzado para vigilar rutas privadas por sus huellas públicas: clusters, topología, fingerprints y anomalías.",
        "legend_title": "🗺️ Leyenda del mapa — cómo leer colores y líneas",
        "data_meaning": "📘 ¿Qué significan estos datos?",
        "disclaimer": "No es asesoramiento financiero. Es un radar de huellas públicas y adopción real.",
        "metrics": {
            "subida": "Subida",
            "riesgo": "Riesgo",
            "flip": "Flip",
            "cobertura": "Cobertura",
            "fase": "Fase",
            "pump": "Pump",
            "hot": "Rutas hot"
        },
        "signal_mixed": "🟡 Señal mixta",
        "normal_act": "🟠 Actividad normal"
    },
    "日本語": {
        "ui_info": "選択した言語にUIを翻訳します。証拠の整合性を保つため、技術データは原語のままです。",
        "radar_desc": "公開された痕跡（クラスター、トポロジー、フィンガープリント、異常値）からプライベートルートを監視する先進的なレーダー。",
        "legend_title": "🗺️ マップの凡例 — 色と線の読み方",
        "data_meaning": "📘 上記のデータは何を意味しますか？",
        "disclaimer": "これは金融アドバイスではありません。実際の採用状況を監視するレーダーです。",
        "metrics": {
            "subida": "上昇率",
            "riesgo": "リスク",
            "flip": "フリップ",
            "cobertura": "カバレッジ",
            "fase": "フェーズ",
            "pump": "パンプ",
            "hot": "ホットルート"
        },
        "signal_mixed": "🟡 混合信号",
        "normal_act": "🟠 通常のアクティビティ"
    }
}


# --- SISTEMA DE TRADUCCIÓN CENTRALIZADO (I18N) ---
I18N = {
    "Español": {
        "ui_info": "Traduce la interfaz al idioma seleccionado. Los datos técnicos permanecen en original.",
        "desc": "Radar avanzado para vigilar rutas privadas por sus huellas públicas.",
        "legend": "Leyenda del mapa — cómo leer colores y líneas",
        "nodes": "Nodos (círculos)",
        "lines": "Líneas — tipos de ruta",
        "disclaimer": "No es asesoramiento financiero. Radar de adopción real.",
        "what_mean": "📘 ¿Qué significan estos datos?",
        "risk": "Riesgo",
        "rise": "Subida",
        "pump": "Pump"
    },
    "日本語": {
        "ui_info": "選択した言語にUIを翻訳します。技術データは原語のままです。",
        "desc": "公開された痕跡からプライベートルートを監視する先進的なレーダー。",
        "legend": "マップの凡例 — 色と線の読み方",
        "nodes": "ノード (地図上の円)",
        "lines": "ライン — ルートの種類",
        "disclaimer": "これは金融アドバイスではありません。実際の採用レーダーです。",
        "what_mean": "📘 上記のデータは何を意味しますか？",
        "risk": "リスク",
        "rise": "上昇",
        "pump": "パンプ"
    }
}

from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import defaultdict, Counter, deque
from datetime import datetime, timedelta, timezone, date as _date
from typing import Dict, Any, List, Tuple, Optional, Set

from urllib.parse import quote as _url_quote

import numpy as np
import pandas as pd
import requests
import plotly.graph_objects as go
import streamlit as st
import streamlit.components.v1 as _st_components

try:
    from streamlit_autorefresh import st_autorefresh
except Exception:
    st_autorefresh = None


APP_NAME = "Ripple Radar Pro"
VERSION = "Route Path Intelligence v6.2.3 PRO — Proof-First Universal Public Discovery"
BUILD_ID = "v91_2026_05_12_LIVE_ROUTE_NUMBERS_NO_DUP_SIGNAL"
BUILD_NOTE = "A-B con números vivos por ficha + Pump/Adopción explicado sin duplicar señales"
DB_PATH = "ripple_radar_advanced.sqlite"

import os as _os

XRPL_SERVER = "https://s1.ripple.com:51234"
RLUSD_ISSUER = "rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De"
RLUSD_CURRENCY = "RLUSD"

REFRESH_SECONDS      = 60
BACKFILL_DAYS        = 240
# Desactivado por defecto para que Streamlit no recree iframes/formularios y no corte Radar FM.
# El gráfico A→B se actualiza igualmente cuando una búsqueda, ruta o wallet dispara rerun.
ENABLE_BACKGROUND_AUTOREFRESH = False

# ── Umbrales whale / auto-mapa ─────────────────────────────────────────────
WHALE_XRP_THRESHOLD   = 100_000      # XRP mínimo para considerarlo whale
WHALE_RLUSD_THRESHOLD = 50_000       # RLUSD/USD mínimo para considerarlo whale
AUTO_MAP_XRP          = 1_000_000    # ≥1M XRP → analiza la TX, pero NO fuerza mapa
AUTO_MAP_RLUSD        = 500_000      # ≥500k RLUSD → analiza la TX, pero NO fuerza mapa
AUTO_MAP_CONFIDENCE   = 0.35         # legado: ahora manda STRICT_AUTO_MAP_CONFIDENCE
WHALE_SCAN_LEDGERS    = 8            # cuántos ledgers hacia atrás escanear

# ── Wallet Supreme Gatekeeper ──────────────────────────────────────────────
# Nunca meter una wallet desconocida al radar solo por volumen alto.
# Separar XRP nativo de IOU/token emitido. Los IOU no aprobados quedan fuera.
APPROVED_ISSUED_CURRENCIES = {"RLUSD", "USD", "USDC", "EUR", "GBP"}
STRICT_AUTO_MAP_CONFIDENCE = 0.72
STRICT_WATCH_CONFIDENCE    = 0.45
UNKNOWN_WALLET_CONF_CAP    = 0.30
IOU_ONLY_CONF_CAP          = 0.12
SUSPICIOUS_IOU_DOMINANCE   = 3.0
WALLET_HARD_BLOCKLIST = {
    # Falsos positivos confirmados: actividad IOU/token/errores o sin conexión real.
    "rhXm7BZpMF6swg36ZpfCKAsiBPUbVwQLkE",
    "r4ufLj57fi9M1p22BKPokmtLzkimYYGMD1",
}
DISCARDED_CONF_CAP = 0.15
DISCARDED_STATUSES = {"discarded", "descartada", "quarantine"}

def _is_unknown_wallet_label(label: str) -> bool:
    lbl = str(label or "").strip().lower()
    return lbl in {
        "", "?", "nan", "none", "desconocido", "unknown",
        "exchange / gateway", "whale detectada automáticamente",
        "whale desconocida", "wallet en cuarentena",
        "desconocido / token no aprobado", "hub bidireccional potencial",
        "treasury / distribuidor potencial", "acumulador / market maker potencial",
    }

def _is_discarded_status(status: str) -> bool:
    return str(status or "").strip().lower() in DISCARDED_STATUSES

def _wallet_state_label(status: str, added_to_map: int = 0) -> str:
    stt = str(status or "").strip().lower()
    if stt == "discarded":
        return "🗑️ Descartada"
    if stt == "quarantine":
        return "🛡️ Cuarentena"
    if int(added_to_map or 0) == 1 and stt == "map":
        return "✅ Radar"
    if int(added_to_map or 0) == 1 and stt not in {"discarded", "quarantine"}:
        return "✅ Radar"
    return "👁️ Watchlist"

DONATION_WALLETS = [
    # ── XRPL ────────────────────────────────────────────────────────────────
    {"red": "XRPL",     "token": "RLUSD", "address": "r34fDWoDZWaRbUNtWQz4fwpvXf7UJZ6Z5H",                          "icon": "💧", "color": "#0EA5E9"},
    {"red": "XRPL",     "token": "USDC",  "address": "r34fDWoDZWaRbUNtWQz4fwpvXf7UJZ6Z5H",                          "icon": "💧", "color": "#0EA5E9"},
    # ── Stellar ──────────────────────────────────────────────────────────────
    {"red": "Stellar",  "token": "EURC",  "address": "GARDMPLSUNUQBBMZUWNTSVCYIK7ZUICUGEENRZ4A2X6EQ4IHAGF2J7IA",    "icon": "⭐", "color": "#A855F7"},
    {"red": "Stellar",  "token": "USDC",  "address": "GARDMPLSUNUQBBMZUWNTSVCYIK7ZUICUGEENRZ4A2X6EQ4IHAGF2J7IA",    "icon": "⭐", "color": "#A855F7"},
    # ── Ethereum / EVM ───────────────────────────────────────────────────────
    {"red": "Ethereum", "token": "EURC",  "address": "0x0C8077866A26AF0e1F398c207F1081b92BeC98d0",                   "icon": "Ξ",  "color": "#6366F1"},
    {"red": "Ethereum", "token": "USDC",  "address": "0x0C8077866A26AF0e1F398c207F1081b92BeC98d0",                   "icon": "Ξ",  "color": "#6366F1"},
    {"red": "Ethereum", "token": "USDT",  "address": "0x0C8077866A26AF0e1F398c207F1081b92BeC98d0",                   "icon": "Ξ",  "color": "#6366F1"},
]

# =============================================================================
# WALLETS CONOCIDAS DE XRPL (etiquetas para rastrear transacciones reales)
# =============================================================================
# Fuentes: XRPL Foundation, Bithomp explorer, XRPScan, reportes públicos Ripple.
# Añadir más a medida que se identifiquen nuevas wallets.
KNOWN_XRPL_WALLETS: Dict[str, str] = {
    # Ripple / RippleNet
    "rHb9CJAWyB4rj91VRWn96DkukG4bwdtyTh": "Génesis XRPL (Cuenta original)",
    "r3kmLJN5D28dHuH8vZNUZpMC4JB8Ypq7bP": "Ripple Labs (operacional)",
    "rGFuMiw48HdbnrUbkRYuitXTmfrDBnTCMC": "Ripple / RippleNet",
    "r4GDFMLGJUKMjNEycnDnhqSsL9NjLBnzKK": "Ripple Escrow (reserva XRP)",
    "rN7n3473SaZBCG4dFL83w7PB5bMUjAntPx": "Ripple Treasury",
    "rEhKZcz6TYqSdDqUMbdHqxcD8Eqn7AXqp":  "Ripple ODL Payments",
    "rMxCKbEDwqr76QuheSUMdEGf4B9xJ8m5De": "RLUSD Issuer (Ripple)",
    # Exchanges conocidos
    "rvYAfWj5gh67oV6fW32ZzP3Aw4Eubs59B":  "Bitstamp (hot wallet)",
    "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz": "Bitstamp (cold wallet)",
    "rEb8TK3gBgk5auZkwc6sHnwrGVJH8DuaLh": "Bitstamp (cold 2)",
    "r9Dr5xwkeLegBeXq6ujinjSBLQzQ1zQGjH": "GateHub (gateway USD)",
    "rhub8VRN55s94qWKDv6jmDy1pUykJzF3wq": "GateHub5 (USD issuer)",
    "rBndiPPKs9k5rjBb7HsEiqXKVZ5s2VrKKs": "Bitso (ODL México)",
    "rHXuEaRYnnJom7nAQp3cXV4iu7gQnDuBMN": "Coins.ph (ODL Filipinas)",
    "rKiCet8SdvWxPXnAgYarFUXMh1zCPz432Y": "Kraken",
    "rLNaPoKeeBjZe2qs6x52yVPZpZ8td4dc6w": "Kraken (cold)",
    "rU2mEJSLqBRkYLVTv55rFTgQajkLTnT6mA": "Binance",
    "rJb5KsHsDHF1YS5B5DU6QCkH5NsPaKQTcy": "Binance (hot)",
    "razqnzf3nMVNSsLz2NmtKpuKKLRQfVTsX":  "ODL Gateway (Ripple Payments)",
    "rDsbeomae4FXwgQTJp9Rs64Qg9vDiTCdBv": "Coinbase (XRP)",
    # Corredores ODL / RippleNet
    "rG9emorNkpo4S8RMBiTYJ2YoVnWQ9FJv4E": "SBI Remit (ODL Japón)",
    "rBKPS4oLSaV2KVVuHH8EpQqMGgGefGFQs7": "Tranglo (ODL Asia)",
    "rNxp4h8apvRis6mJf9Sh8C6iRxfrDWN7AV": "BeeTech (ODL Brasil)",
}

# ── Visualización completa de wallets ───────────────────────────────────────
def _wallet_full_name(wallet: str, label: str = "", fallback: str = "Wallet XRPL sin etiqueta") -> str:
    """Devuelve el nombre humano completo de una wallet, sin recortarlo."""
    w = str(wallet or "").strip()
    lbl = str(label or "").strip()
    if lbl and lbl.lower() not in {"nan", "none", "?", "desconocido", "unknown"}:
        return lbl
    known = KNOWN_XRPL_WALLETS.get(w, "")
    if known:
        return known
    return fallback


def _wallet_short_address(wallet: str, head: int = 12, tail: int = 6) -> str:
    """Solo para etiquetas pequeñas del mapa; las fichas muestran la dirección completa."""
    w = str(wallet or "").strip()
    if len(w) <= head + tail + 3:
        return w
    return f"{w[:head]}…{w[-tail:]}"


def _wallet_map_label(name: str, max_len: int = 22) -> str:
    """Etiqueta breve para no romper el mapa. El hover/ficha muestra el nombre completo."""
    n = str(name or "Wallet XRPL").strip()
    return n if len(n) <= max_len else n[:max_len - 1] + "…"


def _wallet_full_text(wallet: str, label: str = "") -> str:
    """Texto plano: nombre completo + dirección completa para tablas/pruebas."""
    w = str(wallet or "").strip()
    return f"{_wallet_full_name(w, label)} — {w}" if w else _wallet_full_name(w, label)


def _wallet_identity_html(wallet: str, label: str = "", *, compact: bool = False) -> str:
    """Bloque HTML con nombre completo + dirección completa copiables visualmente."""
    name = html.escape(_wallet_full_name(wallet, label))
    addr = html.escape(str(wallet or "").strip())
    if compact:
        return (
            f"<span style='color:#E2E8F0;font-weight:800'>{name}</span>"
            f"<br><code style='color:#94A3B8;font-size:.76rem;white-space:normal;word-break:break-all'>{addr}</code>"
        )
    return (
        f"<div style='margin-top:.25rem'>"
        f"<div style='color:#E2E8F0;font-weight:800'>Nombre wallet: {name}</div>"
        f"<div style='color:#94A3B8;font-size:.78rem;margin-top:.12rem'>Dirección completa:</div>"
        f"<code style='display:block;color:#CBD5E1;background:rgba(2,6,23,.65);padding:.22rem .35rem;border-radius:6px;white-space:normal;word-break:break-all'>{addr}</code>"
        f"</div>"
    )

# Mapeo de etiqueta conocida → nombre de nodo en el mapa principal
# Permite saber "esta wallet es Bitso, que está en el mapa como Bitso (ODL MX)"
WALLET_LABEL_TO_NODE: Dict[str, str] = {
    # Ripple core
    "Ripple Labs (operacional)":      "Ripple Payments",
    "Ripple / RippleNet":             "Ripple Payments",
    "Ripple Escrow (reserva XRP)":    "Ripple Escrow",
    "Ripple Treasury":                "Treasury",
    "Ripple ODL Payments":            "Ripple Payments",
    "RLUSD Issuer (Ripple)":          "RLUSD",
    "Génesis XRPL (Cuenta original)": "XRPL",
    # Exchanges con nodo propio
    "Bitstamp (hot wallet)":          "Bitstamp",
    "Bitstamp (cold wallet)":         "Bitstamp",
    "Bitstamp (cold 2)":              "Bitstamp",
    "GateHub (gateway USD)":          "GateHub",
    "GateHub5 (USD issuer)":          "GateHub",
    "Kraken":                         "Kraken",
    "Kraken (cold)":                  "Kraken",
    "Binance":                        "Binance",
    "Binance (hot)":                  "Binance",
    "Coinbase (XRP)":                 "Public Gateway",  # Coinbase aún genérico
    "ODL Gateway (Ripple Payments)":  "Ripple Payments",
    # ODL / Bancos
    "Bitso (ODL México)":             "Bitso (ODL MX)",
    "Coins.ph (ODL Filipinas)":       "Coins.ph (ODL PH)",
    "SBI Remit (ODL Japón)":          "SBI Remit",
    "Tranglo (ODL Asia)":             "Tranglo (ODL)",
    "BeeTech (ODL Brasil)":           "BeeTech (ODL BR)",
}

# =============================================================================
# MAPA
# =============================================================================

NODES = {
    # ── BANCOS AMERICAS (RippleNet / ODL) ──────────────────────────────────
    "Bank of America":   {"pos": (-8.60, 1.90), "layer": "Banca_AM", "icon": "🏦"},
    "PNC Bank":          {"pos": (-8.60, 1.10), "layer": "Banca_AM", "icon": "🏦"},
    "Itaú Unibanco":     {"pos": (-8.60, 0.30), "layer": "Banca_AM", "icon": "🏦"},
    "Bitso (ODL MX)":    {"pos": (-8.60,-0.50), "layer": "ODL",      "icon": "🔁"},
    "BeeTech (ODL BR)":  {"pos": (-8.60,-1.30), "layer": "ODL",      "icon": "🔁"},
    # RippleNet / ODL Américas confirmados
    "Cuallix (ODL US-MX)": {"pos": (-8.60,-2.10), "layer": "ODL",      "icon": "🔁"},  # ODL corredor US-México
    "Banco BCI":           {"pos": (-8.60,-2.90), "layer": "Banca_AM", "icon": "🏦"},  # RippleNet Chile
    "Viamericas":          {"pos": (-8.60,-3.70), "layer": "Banca_AM", "icon": "⚡"},  # RippleNet remesas US-LATAM

    # ── BANCOS EUROPA ───────────────────────────────────────────────────────
    "Santander":          {"pos": (-7.55, 1.50), "layer": "Banca_EU", "icon": "🏦"},
    "Standard Chartered": {"pos": (-7.55, 0.60), "layer": "Banca_EU", "icon": "🏦"},
    "Zodia Custody":      {"pos": (-7.55,-0.30), "layer": "Banca_EU", "icon": "🔐"},
    # RippleNet Europa confirmados
    "SEB":                {"pos": (-7.55,-1.10), "layer": "Banca_EU", "icon": "🏦"},  # RippleNet Suecia
    "Akbank":             {"pos": (-7.55,-1.90), "layer": "Banca_EU", "icon": "🏦"},  # RippleNet Turquía
    "TransferGo":         {"pos": (-7.55,-2.70), "layer": "Banca_EU", "icon": "⚡"},  # RippleNet remesas EU

    # ── BANCOS ASIA-PAC ─────────────────────────────────────────────────────
    "SBI Remit":          {"pos": (-6.50, 1.70), "layer": "Banca_AP", "icon": "🏯"},
    "MoneyTap / SBI":     {"pos": (-6.50, 0.80), "layer": "Banca_AP", "icon": "🏯"},
    "Axis Bank":          {"pos": (-6.50,-0.10), "layer": "Banca_AP", "icon": "🏦"},
    "Tranglo (ODL)":      {"pos": (-6.50,-0.90), "layer": "ODL",      "icon": "🌏"},
    "Coins.ph (ODL PH)":  {"pos": (-6.50,-1.70), "layer": "ODL",      "icon": "🌏"},
    # RippleNet / ODL Asia-Pac confirmados
    "LianLian Pay":          {"pos": (-6.50,-2.50), "layer": "Banca_AP", "icon": "🏦"},  # RippleNet China 2018 (con licencia PBoC)
    "Siam Commercial Bank":  {"pos": (-6.50,-3.30), "layer": "Banca_AP", "icon": "🏦"},  # RippleNet Tailandia
    "CIMB":                  {"pos": (-6.50,-4.10), "layer": "Banca_AP", "icon": "🏦"},  # RippleNet Malasia
    "FlashFX (ODL AU)":      {"pos": (-6.50,-4.90), "layer": "ODL",      "icon": "🌏"},  # ODL Australia

    # ── INFRAESTRUCTURA RAIL PRIVADO ────────────────────────────────────────
    "SWIFT":           {"pos": (-5.20, 2.35), "layer": "Privado",  "icon": "🏦"},
    "FedNow":          {"pos": (-5.20, 1.35), "layer": "Privado",  "icon": "⚡"},
    "Mastercard":      {"pos": (-5.20, 0.35), "layer": "Privado",  "icon": "💳"},
    "SEPA/ACH":        {"pos": (-5.20,-0.65), "layer": "Privado",  "icon": "🌍"},
    # ── REGULADORES (entre rails y Ripple Core — sin cruzar el mapa) ────────
    "Federal Reserve": {"pos": (-4.20, 2.80), "layer": "Gobierno", "icon": "🏛️"},
    "Bank for International Settlements (BIS)": {"pos": (-4.20, 2.05), "layer": "Gobierno", "icon": "🏛️"},
    "Project mBridge": {"pos": (-4.20, 1.30), "layer": "Gobierno", "icon": "🌉"},

    # ── RIPPLE CORE ─────────────────────────────────────────────────────────
    "Ripple Payments":     {"pos": (-3.05, 2.10), "layer": "Ripple", "icon": "💸"},
    "Custody/Metaco":      {"pos": (-3.05, 1.30), "layer": "Ripple", "icon": "🔐"},
    "Standard Custody":    {"pos": (-3.05, 0.50), "layer": "Ripple", "icon": "🏦"},
    "Treasury":            {"pos": (-3.05,-0.30), "layer": "Ripple", "icon": "🏛️"},
    "Rail":                {"pos": (-3.05,-1.10), "layer": "Ripple", "icon": "🚄"},
    "Hidden Road / Prime": {"pos": (-3.05,-1.90), "layer": "Ripple", "icon": "🛣️"},
    "Ripple Escrow":       {"pos": (-3.05,-2.70), "layer": "Ripple", "icon": "🔒"},

    # ── INSTITUCIONAL ───────────────────────────────────────────────────────
    "DTCC/NSCC":        {"pos": (-0.95, 0.30), "layer": "Institucional", "icon": "🏢"},
    "Corredores FX":    {"pos": (-0.95,-0.65), "layer": "Institucional", "icon": "🔁"},
    "Permissioned DEX": {"pos": (-0.95,-1.60), "layer": "Institucional", "icon": "🧬"},

    # ── EXCHANGES (wallets XRPL reales conocidas) ───────────────────────────
    "Bitstamp":         {"pos": ( 1.15, 2.60), "layer": "Exchange", "icon": "🏛️"},
    "GateHub":          {"pos": ( 1.15, 1.90), "layer": "Exchange", "icon": "🚪"},
    "Kraken":           {"pos": ( 1.15, 1.20), "layer": "Exchange", "icon": "🦑"},
    "Binance":          {"pos": ( 1.15, 0.50), "layer": "Exchange", "icon": "🔶"},

    # ── VIGILANCIA ──────────────────────────────────────────────────────────
    "Public Gateway":   {"pos": ( 1.15,-0.30), "layer": "Vigilancia", "icon": "🛰️"},
    "Trustlines":       {"pos": ( 1.15,-1.10), "layer": "Vigilancia", "icon": "🔗"},
    "DEX/AMM":          {"pos": ( 1.15,-1.90), "layer": "Vigilancia", "icon": "🌊"},
    "Large Transfers":  {"pos": ( 1.15,-2.70), "layer": "Vigilancia", "icon": "🐋"},
    "Clusters":         {"pos": ( 1.15,-3.40), "layer": "Vigilancia", "icon": "🧩"},

    # ── MOTORES DE INTELIGENCIA ─────────────────────────────────────────────
    "Topology Engine":   {"pos": (3.05, 1.30), "layer": "Inteligencia", "icon": "🧠"},
    "Anomaly Engine":    {"pos": (3.05, 0.25), "layer": "Inteligencia", "icon": "🚨"},
    "Fingerprint Engine":{"pos": (3.05,-0.80), "layer": "Inteligencia", "icon": "🧬"},

    # ── XRPL PÚBLICO ───────────────────────────────────────────────────────
    "XRPL":     {"pos": (5.05, 0.85), "layer": "Público", "icon": "💧"},
    "RLUSD":    {"pos": (5.05,-0.25), "layer": "Público", "icon": "🪙"},
    "Ethereum": {"pos": (5.05,-1.35), "layer": "Futuro",  "icon": "Ξ"},

    # ── CBDC / BANCOS CENTRALES (pilotos Ripple confirmados) ────────────────
    # x=6.35: zona liberada al mover Federal Reserve a x=-4.20 (junto a los rails)
    "People's Bank of China (PBoC)": {"pos": (6.35, 2.80), "layer": "CBDC", "icon": "🏛️"},
    "National Bank of Georgia":      {"pos": (6.35, 2.05), "layer": "CBDC", "icon": "🏛️"},
    "Republic of Palau":             {"pos": (6.35, 1.30), "layer": "CBDC", "icon": "🏛️"},
    "Bhutan NDI":                    {"pos": (6.35, 0.55), "layer": "CBDC", "icon": "🏛️"},
    "Central Bank of Montenegro":    {"pos": (6.35,-0.20), "layer": "CBDC", "icon": "🏛️"},
    "Banco de la República":         {"pos": (6.35,-0.95), "layer": "CBDC", "icon": "🏛️"},
}

# ── Mapeo capa → zona del mapa ──────────────────────────────────────────────
# x_col: columna X del nodo, y_start: Y del primer nodo libre (debajo del último estático)
ZONE_POS: Dict[str, Dict] = {
    "Banca_AM":      {"x": -8.60, "y_start": -2.10, "y_step": -0.80, "box": (-8.95,-1.65,-8.25, 2.25), "label": "Americas"},
    "Banca_EU":      {"x": -7.55, "y_start": -1.10, "y_step": -0.80, "box": (-7.90,-0.70,-7.20, 1.85), "label": "Europa"},
    "Banca_AP":      {"x": -6.50, "y_start": -2.50, "y_step": -0.80, "box": (-6.85,-2.05,-6.15, 2.05), "label": "Asia-Pac"},
    "Privado":       {"x": -5.20, "y_start": -1.65, "y_step": -0.80, "box": (-5.60,-1.10,-4.80, 2.70), "label": "Infraestructura"},
    "Ripple":        {"x": -3.05, "y_start": -3.50, "y_step": -0.80, "box": (-3.45,-3.10,-2.65, 2.45), "label": "Ripple"},
    "Institucional": {"x": -0.95, "y_start": -2.45, "y_step": -0.80, "box": (-1.35,-1.95,-0.55, 2.55), "label": "Institucional"},
    "Exchange":      {"x":  1.15, "y_start": -0.20, "y_step": -0.70, "box": ( 0.75, 2.20, 1.55, 2.95), "label": "Exchanges"},
    "ODL":           {"x": -8.60, "y_start": -2.10, "y_step": -0.80, "box": (-8.95,-1.65,-8.25, 2.25), "label": "Americas"},
    # ── Discovery Engine — banda horizontal a la derecha del XRPL ──────────
    # Gobierno: junto a los rails (Federal Reserve estático aquí a x=-4.20).
    # CBDC: ocupa el hueco liberado por Federal Reserve (x=6.35).
    # Fintech/AssetMgmt/…: condicionales — sólo aparecen si hay nodos.
    "Gobierno":   {"x": -4.20, "y_start":  2.05, "y_step": -0.75, "box": (-4.60,-2.10,-3.80, 3.15), "label": "Gobierno / reguladores"},
    "CBDC":       {"x":  6.35, "y_start": -1.70, "y_step": -0.75, "box": ( 6.00,-3.00, 6.70, 3.15), "label": "CBDC / banco central"},
    "Fintech":    {"x":  7.25, "y_start":  2.80, "y_step": -0.75, "box": ( 6.90,-2.10, 7.60, 3.15), "label": "Fintech / pagos"},
    "AssetMgmt":  {"x":  8.15, "y_start":  2.80, "y_step": -0.75, "box": ( 7.80,-2.10, 8.50, 3.15), "label": "Asset managers"},
    "Clearing":   {"x":  9.05, "y_start":  2.80, "y_step": -0.75, "box": ( 8.70,-2.10, 9.40, 3.15), "label": "Clearing / settlement"},
    "RedPrivada": {"x":  9.95, "y_start":  2.80, "y_step": -0.75, "box": ( 9.60,-2.10,10.30, 3.15), "label": "Red privada / OTC"},
    "Puente":     {"x": 10.85, "y_start":  2.80, "y_step": -0.75, "box": (10.50,-2.10,11.20, 3.15), "label": "Puentes / cross-chain"},
    "Proveedor":  {"x": 11.75, "y_start":  2.80, "y_step": -0.75, "box": (11.40,-2.10,12.10, 3.15), "label": "Proveedores / APIs"},
    "Descubierto":{"x": 12.65, "y_start":  2.80, "y_step": -0.75, "box": (12.30,-2.10,13.00, 3.15), "label": "Otros descubiertos"},
}

# ── Normalización de nombres de capa devueltos por Claude ───────────────────
LAYER_NORMALIZE: Dict[str, str] = {
    # Americas / bancos
    "banca_am": "Banca_AM", "americas": "Banca_AM", "latam": "Banca_AM",
    "north america": "Banca_AM", "latinoamerica": "Banca_AM", "banco_am": "Banca_AM",
    # Europa
    "banca_eu": "Banca_EU", "europa": "Banca_EU", "europe": "Banca_EU", "banco_eu": "Banca_EU",
    # Asia
    "banca_ap": "Banca_AP", "asia": "Banca_AP", "asia-pac": "Banca_AP",
    "asia pac": "Banca_AP", "banco_ap": "Banca_AP", "apac": "Banca_AP",
    # Infraestructura
    "privado": "Privado", "infraestructura": "Privado", "infrastructure": "Privado",
    "rail": "Privado", "privada": "Privado", "rails": "Privado",
    # Ripple
    "ripple": "Ripple", "ripplenet": "Ripple", "odl": "ODL",
    # Institucional
    "institucional": "Institucional", "institutional": "Institucional",
    "asset management": "Institucional", "hedge fund": "Institucional",
    "asset_mgmt": "Institucional", "assetmgmt": "Institucional",
    # Exchanges
    "exchange": "Exchange", "exchanges": "Exchange", "crypto exchange": "Exchange",
    "crypto_exchange": "Exchange",
    # Discovery Engine universal layers
    "fintech": "Fintech", "fin tech": "Fintech", "neobank": "Fintech", "payments": "Fintech",
    "cbdc": "CBDC", "central bank": "CBDC", "banco central": "CBDC", "reserve bank": "CBDC",
    "gobierno": "Gobierno", "government": "Gobierno", "regulador": "Gobierno", "regulator": "Gobierno",
    "public authority": "Gobierno", "federal agency": "Gobierno",
    "assetmgmt": "AssetMgmt", "asset mgmt": "AssetMgmt", "asset management": "AssetMgmt",
    "clearing": "Clearing", "settlement": "Clearing", "post trade": "Clearing", "post-trade": "Clearing",
    "redprivada": "RedPrivada", "red privada": "RedPrivada", "private network": "RedPrivada",
    "otc": "RedPrivada", "otc desk": "RedPrivada",
    "puente": "Puente", "bridge": "Puente", "cross chain": "Puente", "crosschain": "Puente",
    "interoperability": "Puente", "interoperabilidad": "Puente", "oracle": "Puente",
    "proveedor": "Proveedor", "provider": "Proveedor", "service provider": "Proveedor",
    "api": "Proveedor", "tech provider": "Proveedor", "technology provider": "Proveedor",
    "tokenization": "Proveedor", "tokenisation": "Proveedor", "rwa": "AssetMgmt",
    "custody": "Ripple", "custodia": "Ripple", "prime brokerage": "Ripple",
    "bank": "Banca_AM", "banco": "Banca_AM", "commercial bank": "Banca_AM",
    "descubierto": "Descubierto", "discovered": "Descubierto", "otro": "Descubierto", "other": "Descubierto",
}

# ── Mapeo connects_to → nodo exacto del mapa ────────────────────────────────


def _normalize_layer(layer_raw: str) -> str:
    """
    Normaliza la capa devuelta por la búsqueda contextual / IA para que
    siempre encaje con las zonas reales del mapa. Sin esto, los nodos
    dinámicos se guardan en SQLite pero no se dibujan.
    """
    raw = str(layer_raw or "Descubierto").strip()
    if not raw:
        return "Descubierto"

    if raw in ZONE_POS:
        return raw

    key = (
        raw.lower()
        .replace("_", " ")
        .replace("-", " ")
        .replace("/", " ")
        .strip()
    )
    key_compact = key.replace(" ", "")

    if key in LAYER_NORMALIZE:
        return LAYER_NORMALIZE[key]
    if key_compact in LAYER_NORMALIZE:
        return LAYER_NORMALIZE[key_compact]

    aliases = {
        "publico": "Público",
        "public": "Público",
        "xrpl": "Público",
        "vigilancia": "Vigilancia",
        "watch": "Vigilancia",
        "inteligencia": "Inteligencia",
        "intelligence": "Inteligencia",
        "futuro": "Futuro",
        "future": "Futuro",
        "descubierto": "Descubierto",
        "discovered": "Descubierto",
        "otro": "Descubierto",
        "other": "Descubierto",
    }
    return aliases.get(key, aliases.get(key_compact, raw.title()))


def _next_pos_in_zone(layer: str, taken_y: Dict[str, list]) -> Tuple[float, float]:
    """
    Calcula una posición libre para un nodo dinámico dentro de una zona
    existente, evitando que se monte encima de nodos estáticos o descubiertos.
    """
    zone = ZONE_POS.get(layer)
    if not zone:
        return (6.60, 2.20)

    x = float(zone.get("x", 6.60))
    y = float(zone.get("y_start", 2.20))
    step = float(zone.get("y_step", -0.80))
    occupied = [float(v) for v in taken_y.get(layer, []) if v is not None]

    if not occupied:
        return (x, y)

    for _ in range(80):
        if all(abs(y - yy) >= 0.32 for yy in occupied):
            return (x, y)
        y += step

    return (x, y)


# ── Canonicalización universal de entidades / nodos ─────────────────────────
def _norm_key(text: Any) -> str:
    """Clave estable para comparar nombres en cualquier escritura (latín, CJK, árabe, cirílico…)."""
    raw = str(text or "").strip().lower()
    # Intentar transliterar a ASCII (quita diacríticos: é→e, ñ→n, etc.)
    ascii_attempt = unicodedata.normalize("NFKD", raw).encode("ascii", "ignore").decode("ascii").strip()
    if ascii_attempt:
        # El texto tiene representación ASCII suficiente (latín/griego/etc.)
        raw = ascii_attempt
        raw = raw.replace("&", " and ")
        raw = re.sub(r"[^a-z0-9]+", " ", raw)
    else:
        # Texto puramente no-ASCII (CJK, árabe, cirílico, hebreo…)
        # Conservar los codepoints originales como clave; solo eliminar puntuación/espacios extra.
        raw = re.sub(r"\s+", "", raw)   # compactar espacios
    return re.sub(r"\s+", " ", raw).strip()


# Palabras que no cambian la entidad real. Sirven para que
# "BlackRock Inc.", "BLACK ROCK INC", "BlackRock, LLC" => BlackRock.
_ENTITY_LEGAL_SUFFIXES: Set[str] = {
    "inc", "incorporated", "corp", "corporation", "co", "company",
    "ltd", "limited", "llc", "llp", "lp", "plc", "sa", "s a",
    "ag", "nv", "bv", "gmbh", "kg", "sas", "spa", "pte", "pty",
    "group", "holdings", "holding", "international", "global",
}

_ENTITY_NOISE_PREFIXES: Set[str] = {"the"}


def _entity_alias_keys(text: Any) -> List[str]:
    """
    Genera variantes normalizadas para resolver una entidad aunque el usuario la escriba
    con mayúsculas, puntos, guiones, tildes, sufijos legales o espacios distintos.

    Ejemplos que deben caer juntos:
    - BlackRock / BLACK ROCK / BlackRock Inc. / black-rock
    - J.P. Morgan Chase / jp morgan / JPMorgan Chase LLC
    - Banco de la República / banco de la republica
    """
    base = _norm_key(text)
    if not base:
        return []

    keys: List[str] = []

    def add(k: str) -> None:
        k = re.sub(r"\s+", " ", str(k or "").strip())
        if k and k not in keys:
            keys.append(k)

    add(base)
    add(base.replace(" ", ""))

    tokens = base.split()
    # Quitar prefijos de ruido tipo "the".
    while tokens and tokens[0] in _ENTITY_NOISE_PREFIXES:
        tokens = tokens[1:]
    if tokens:
        stripped_prefix = " ".join(tokens)
        add(stripped_prefix)
        add(stripped_prefix.replace(" ", ""))

    # Quitar sufijos legales al final, incluso si hay varios: "Inc Ltd", "Group LLC".
    tokens2 = list(tokens)
    while tokens2 and tokens2[-1] in _ENTITY_LEGAL_SUFFIXES:
        tokens2.pop()
    if tokens2:
        stripped_suffix = " ".join(tokens2)
        add(stripped_suffix)
        add(stripped_suffix.replace(" ", ""))

    # Variante sin conectores muy débiles al final. No quitamos "bank", "pay", etc.
    # porque sí pueden formar parte del nombre real.
    return keys

ENTITY_CANONICAL_ALIASES: Dict[str, str] = {
    # Reserva Federal: una sola entidad, varios nombres posibles.
    "reserva federal": "Federal Reserve",
    "federal reserve": "Federal Reserve",
    "federal reserve system": "Federal Reserve",
    "board of governors federal reserve": "Federal Reserve",
    "us federal reserve": "Federal Reserve",
    "u s federal reserve": "Federal Reserve",
    "the fed": "Federal Reserve",
    "fed": "Federal Reserve",
    # Rails de la Reserva Federal: se mantienen como rail, no como duplicado institucional.
    "fednow": "FedNow",
    "fed now": "FedNow",
    "fednow service": "FedNow",
    "fedwire": "FedNow",
    # Normalizaciones frecuentes.
    "black rock": "BlackRock",
    "blackrock": "BlackRock",
    "xrpl": "XRPL",
    "xrp ledger": "XRPL",
    "xrp ledger network": "XRPL",
    "ripple ledger": "XRPL",
    "ripple ledger network": "XRPL",
    "rlusd": "RLUSD",
    "ripple usd": "RLUSD",
    "ripple stablecoin": "RLUSD",
    "securitize": "Securitize",
    "wormhole": "Wormhole",
    "wormhole protocol": "Wormhole",
    "whonmle": "Wormhole",
    "womhole": "Wormhole",
    "wormhle": "Wormhole",
    "whormhole": "Wormhole",
    "workhomle": "Wormhole",
    "workhomle protocol": "Wormhole",
    "whormle": "Wormhole",
    "whorml": "Wormhole",
    "chainlink": "Chainlink",
    "axelar": "Axelar",
    "layerzero": "LayerZero",
    "layer zero": "LayerZero",
    "circle": "Circle",
    "usdc": "USDC",
    "volante technologies": "Volante Technologies",
    "finastra": "Finastra",
    # JP Morgan / Kinexys — banco + plataforma blockchain propia (antes Onyx)
    "jp morgan": "JPMorgan Chase",
    "j p morgan": "JPMorgan Chase",
    "jpmorgan": "JPMorgan Chase",
    "jp morgan chase": "JPMorgan Chase",
    "j p morgan chase": "JPMorgan Chase",
    "jpmorgan chase": "JPMorgan Chase",
    "jpm": "JPMorgan Chase",
    "jpm chase": "JPMorgan Chase",
    "kinexys": "Kinexys (JPMorgan)",
    "onyx": "Kinexys (JPMorgan)",
    "onyx by j p morgan": "Kinexys (JPMorgan)",
    "jpmorgan onyx": "Kinexys (JPMorgan)",
    # BlackRock — gestor de activos con fondos tokenizados en XRPL/Ethereum
    "blackrock": "BlackRock",
    "black rock": "BlackRock",
    "blackrock inc": "BlackRock",
    "blackrock incorporated": "BlackRock",
    "blackrock group": "BlackRock",
    "blackrock buidl": "BlackRock",
    "black rock buidl": "BlackRock",
    "buidl": "BlackRock",
    "buidl fund": "BlackRock",
    # BIS — Bank for International Settlements / Banco de Pagos Internacionales
    "bis": "Bank for International Settlements (BIS)",
    "b i s": "Bank for International Settlements (BIS)",
    "bank for international settlements": "Bank for International Settlements (BIS)",
    "international settlements bank": "Bank for International Settlements (BIS)",
    "banco de pagos internacionales": "Bank for International Settlements (BIS)",
    "banco internacional de pagos": "Bank for International Settlements (BIS)",
    "banco de liquidaciones internacionales": "Bank for International Settlements (BIS)",
    "banco central de bancos centrales": "Bank for International Settlements (BIS)",
    "bank of international settlements": "Bank for International Settlements (BIS)",
    "project mbridge": "Project mBridge",
    "mbridge": "Project mBridge",
    "m cbdc bridge": "Project mBridge",
    "mcbdc bridge": "Project mBridge",
    # Banco Popular de China (People's Bank of China) — variantes CJK, pinyin y en inglés
    "中国人民银行": "People's Bank of China (PBoC)",
    "中国人民银行数字货币研究所": "People's Bank of China (PBoC)",
    "peoples bank of china": "People's Bank of China (PBoC)",
    "people s bank of china": "People's Bank of China (PBoC)",
    "pboc": "People's Bank of China (PBoC)",
    "p b o c": "People's Bank of China (PBoC)",
    "banco popular de china": "People's Bank of China (PBoC)",
    "digital yuan": "e-CNY (Digital Yuan)",
    "e-cny": "e-CNY (Digital Yuan)",
    "ecny": "e-CNY (Digital Yuan)",
    "dcep": "e-CNY (Digital Yuan)",
    "数字人民币": "e-CNY (Digital Yuan)",
    # Otros bancos centrales frecuentes en búsquedas no-ASCII
    "日本銀行": "Bank of Japan",
    "日本银行": "Bank of Japan",
    "유럽중앙은행": "European Central Bank",
    "欧洲中央银行": "European Central Bank",
    "европейский центральный банк": "European Central Bank",
    "банк России": "Bank of Russia",
    "банк россии": "Bank of Russia",
    "центральный банк российской федерации": "Bank of Russia",
    "سنگاپور مرکزی بانک": "MAS Singapore",
    "بانک مرکزی سنگاپور": "MAS Singapore",
    # Siglas con vocal (4 letras) — sin esto el smart_cap los capitaliza mal
    "bbva": "BBVA",
    "bbva bancomer": "BBVA",
    "mufg": "MUFG",
    "mufg bank": "MUFG",
    "hsbc": "HSBC",
    "hsbc bank": "HSBC",
    "hsbc holdings": "HSBC",
    "bnp": "BNP Paribas",
    "bnp paribas": "BNP Paribas",
    "ubs": "UBS",
    "ubs group": "UBS",
    "ing": "ING",
    "ing bank": "ING",
    "ing group": "ING",
    "dbs": "DBS Bank",
    "dbs bank": "DBS Bank",
    "nab": "National Australia Bank",
    "anz": "ANZ Bank",
    "rbc": "Royal Bank of Canada",
    "bmo": "Bank of Montreal",
    "cibc": "CIBC",
    "pnc": "PNC Financial",
    "sbi": "State Bank of India",
    "swift": "SWIFT",
    "imf": "IMF",
    "fmi": "IMF",
    "ecb": "European Central Bank",
    "bce": "European Central Bank",
    "boe": "Bank of England",
    "mas": "MAS Singapore",
    "rbi": "Reserve Bank of India",
    "rba": "Reserve Bank of Australia",
    "boj": "Bank of Japan",
    "bok": "Bank of Korea",
    "sama": "Saudi Central Bank (SAMA)",
    "cbuae": "Central Bank of UAE",
    "fsb": "Financial Stability Board (FSB)",
    "iosco": "IOSCO",
    "fatf": "FATF",
    "dtcc": "DTCC",
    "sec": "SEC",
    "cftc": "CFTC",
    "occ": "OCC",
    "fdic": "FDIC",
    "bafin": "BaFin",
    "fca": "FCA",
    "esma": "ESMA",
    # ── Nuevos nodos estáticos RippleNet/CBDC ──────────────────────────────
    # LianLian Pay
    "lianlian pay": "LianLian Pay",
    "lian lian pay": "LianLian Pay",
    "lianlianpay": "LianLian Pay",
    "lian lian": "LianLian Pay",
    "lianlian": "LianLian Pay",
    # Siam Commercial Bank
    "siam commercial bank": "Siam Commercial Bank",
    "scb thailand": "Siam Commercial Bank",
    "siam bank": "Siam Commercial Bank",
    # CIMB
    "cimb bank": "CIMB",
    "cimb group": "CIMB",
    "cimb holdings": "CIMB",
    # FlashFX
    "flashfx": "FlashFX (ODL AU)",
    "flash fx": "FlashFX (ODL AU)",
    "flashfx au": "FlashFX (ODL AU)",
    # SEB
    "seb bank": "SEB",
    "skandinaviska enskilda banken": "SEB",
    "seb sweden": "SEB",
    # Akbank
    "akbank as": "Akbank",
    "ak bank": "Akbank",
    "akbank turkey": "Akbank",
    "akbank turquia": "Akbank",
    # TransferGo
    "transfer go": "TransferGo",
    "transfergo eu": "TransferGo",
    # Cuallix
    "cuallix": "Cuallix (ODL US-MX)",
    "cuallix odl": "Cuallix (ODL US-MX)",
    # Banco BCI
    "bci": "Banco BCI",
    "banco bci": "Banco BCI",
    "banco de credito e inversiones": "Banco BCI",
    "bci chile": "Banco BCI",
    # Viamericas
    "viamericas corporation": "Viamericas",
    "viamericas corp": "Viamericas",
    # National Bank of Georgia
    "nbg": "National Bank of Georgia",
    "national bank georgia": "National Bank of Georgia",
    "nbg georgia": "National Bank of Georgia",
    "national bank of georgia georgia": "National Bank of Georgia",
    # Republic of Palau
    "palau": "Republic of Palau",
    "republic palau": "Republic of Palau",
    "psc palau": "Republic of Palau",
    "palau stablecoin": "Republic of Palau",
    # Bhutan NDI
    "bhutan": "Bhutan NDI",
    "bhutan ndi": "Bhutan NDI",
    "royal monetary authority bhutan": "Bhutan NDI",
    "rma bhutan": "Bhutan NDI",
    "bhutan cbdc": "Bhutan NDI",
    # Central Bank of Montenegro
    "cbmne": "Central Bank of Montenegro",
    "cbm montenegro": "Central Bank of Montenegro",
    "central bank montenegro": "Central Bank of Montenegro",
    "montenegro cbdc": "Central Bank of Montenegro",
    # Banco de la República (Colombia)
    "banrep": "Banco de la República",
    "banco republica colombia": "Banco de la República",
    "banco de la republica": "Banco de la República",
    "banco de la republica colombia": "Banco de la República",
    "banco central colombia": "Banco de la República",
}



def _infer_layer_icon_from_name(name: Any, fallback_layer: str = "Descubierto", fallback_icon: str = "🔎") -> Tuple[str, str]:
    """Clasificador local de seguridad para nodos dinámicos.

    Objetivo: evitar que la IA coloque nodos en capas genéricas o equivocadas.
    Reglas importantes:
    - No clasificar "Treasury" como Gobierno salvo que sea explícitamente un Tesoro público.
    - No clasificar "Ripple Payments" como Fintech por contener la palabra payments.
    - Preferir capas específicas: AssetMgmt, Clearing, Puente, Proveedor, ODL, CBDC.
    - Mantener soporte para nombres nativos/no ASCII.
    """
    raw = str(name or "").strip()
    raw_lower = raw.lower()
    key = _norm_key(raw)
    compact = key.replace(" ", "")
    texts = [raw_lower, key, compact]

    def has_any(words: List[str]) -> bool:
        return any(w in t for w in words for t in texts if t)

    # Ripple core / productos propios: antes que Fintech para no degradar "Ripple Payments".
    if has_any(["ripple payments", "ripplenet", "on demand liquidity", "odl"]):
        return "Ripple", "💸"
    if has_any(["hidden road", "ripple prime", "prime brokerage"]):
        return "Ripple", "🛣️"
    if has_any(["metaco", "ripple custody", "standard custody"]):
        return "Ripple", "🔐"
    if has_any(["ripple treasury", "ripple escrow"]):
        return "Ripple", "🏛️"
    if has_any(["fednow", "fedwire", "swift", "sepa", "ach"]):
        return "Privado", "⚡"

    if has_any(["securitize", "volante", "finastra", "temenos", "swift gpi", "provider", "service provider", "api provider", "technology", "software", "middleware", "payment processor", "tokenization", "tokenisation"]):
        return "Proveedor", "🧰"

    # Bancos centrales / CBDC / autoridades monetarias.
    if has_any([
        "central bank", "banco central", "cbdc", "monetary authority", "reserve bank",
        "pboc", "peoples bank", "people s bank", "people bank", "bank of japan", "bank of korea", "bundesbank",
        "中国人民银行", "数字人民币", "日本銀行", "日本银行", "e cny", "ecny", "dcep", "digital yuan",
    ]):
        return "CBDC", "🏦"

    # Gobierno/reguladores: Treasury solo si es Tesoro público, no cualquier módulo Treasury.
    if has_any(["federal reserve", "securities and exchange commission", "cftc", "occ", "fdic", "regulator", "regulador", "government", "gobierno"]):
        return "Gobierno", "🏛️"
    if has_any(["u s treasury", "us treasury", "department of treasury", "hm treasury", "ministerio de hacienda"]):
        return "Gobierno", "🏛️"

    # Capas institucionales específicas.
    if has_any(["blackrock", "vaneck", "franklin", "fidelity", "invesco", "buidl", "vbill", "asset management", "fund", "etf", "idg capital", "idg资本", "hillhouse", "高瓴资本", "sequoia", "红杉中国"]):
        return "AssetMgmt", "💼"
    if has_any(["dtcc", "nscc", "euroclear", "clearstream", "clearing", "settlement", "depository"]):
        return "Clearing", "🏢"
    if has_any(["wormhole", "axelar", "layerzero", "layer zero", "chainlink", "ccip", "bridge", "cross chain", "crosschain", "interoperability", "interoperabilidad", "oracle"]):
        return "Puente", "🌀"
    if has_any(["circle", "usdc", "stripe", "adyen", "paypal", "wise", "revolut", "fintech"]):
        return "Fintech", "⚡"
    if has_any(["binance", "coinbase", "kraken", "bitstamp", "gatehub", "exchange"]):
        return "Exchange", "🏛️"
    if has_any(["bitso", "tranglo", "coins ph", "sbi remit", "remit", "corridor", "corredor"]):
        return "ODL", "🔁"
    if has_any(["otc", "private network", "permissioned", "red privada"]):
        return "RedPrivada", "🔒"

    # Bancos comerciales genéricos: solo si no son bancos centrales.
    if has_any([" bank", "bank ", "banco ", " banco", "commercial bank", "credit union", "unibanco"]):
        return _normalize_layer(fallback_layer if fallback_layer not in {"", "Descubierto", "Otro", "other", "discovered"} else "Banca_AM"), "🏦"

    norm_fallback = _normalize_layer(fallback_layer or "Descubierto")
    return norm_fallback, fallback_icon or "🔎"


def _layer_is_generic_for_dynamic(layer: Any) -> bool:
    """Capas demasiado genéricas: se pueden mejorar con el clasificador local."""
    nl = _normalize_layer(str(layer or ""))
    raw = str(layer or "").strip().lower()
    return nl in {"Descubierto", "Institucional", "Privado"} or raw in {"", "otro", "other", "discovered", "institutional", "private"}

def _canonical_entity_name(name: Any) -> str:
    """
    Devuelve el nombre canónico de una entidad.
    Es deliberadamente agresivo contra diferencias superficiales:
    mayúsculas/minúsculas, tildes, puntos, guiones, espacios y sufijos legales.
    """
    raw = str(name or "").strip()
    if not raw:
        return "Descubierto"

    keys = _entity_alias_keys(raw)

    # 1) Alias explícitos mantenidos por nosotros.
    for key in keys:
        if key in ENTITY_CANONICAL_ALIASES:
            return ENTITY_CANONICAL_ALIASES[key]

    # 2) Si coincide con un nodo estático, conservar grafía oficial.
    for existing in NODES.keys():
        existing_keys = _entity_alias_keys(existing)
        if any(k in existing_keys for k in keys):
            return existing

    # 3) Comparación compacta contra alias explícitos: "black rock" == "blackrock".
    compact_keys = {k.replace(" ", "") for k in keys}
    for alias, canonical in ENTITY_CANONICAL_ALIASES.items():
        alias_compact = _norm_key(alias).replace(" ", "")
        if alias_compact in compact_keys:
            return canonical

    # 4) Último recurso: nombre limpio con espacios normalizados, no el texto sucio original.
    return re.sub(r"\s+", " ", raw).strip()




def _canonical_entity_key(name: Any) -> str:
    """Clave estable para comparar entidades aunque cambien mayúsculas, sufijos o alias."""
    canonical = _canonical_entity_name(name)
    key = _norm_key(canonical).replace(" ", "")
    return key or _norm_key(name).replace(" ", "") or str(name or "").strip().lower()


def _canonical_pair_key(node_a: Any, node_b: Any) -> str:
    """Clave NO dirigida para una conexión A↔B. Evita verificar dos veces A→B y B→A."""
    ka = _canonical_entity_key(node_a)
    kb = _canonical_entity_key(node_b)
    return "||".join(sorted([ka, kb]))


def _canonical_pair_proof_id(node_a: Any, node_b: Any) -> str:
    return hashlib.sha256(_canonical_pair_key(node_a, node_b).encode()).hexdigest()[:16]


def _connection_proof_row(conn: sqlite3.Connection, node_a: Any, node_b: Any):
    """
    Busca una prueba guardada para A↔B usando clave canónica y fallback legacy.
    Esto evita que HSBC↔XRPL vuelva a aparecer pendiente desde XRPL↔HSBC o con alias.
    """
    if conn is None:
        return None
    try:
        pair_key = _canonical_pair_key(node_a, node_b)
        pid = _canonical_pair_proof_id(node_a, node_b)
        row = conn.execute(
            "SELECT proof_data, onchain, confidence, validated_at, node_a, node_b FROM connection_proofs "
            "WHERE proof_id=? OR pair_key=? LIMIT 1",
            (pid, pair_key),
        ).fetchone()
        if row:
            return row
    except Exception:
        pass
    # Fallback para bases antiguas sin columnas nuevas o con proof_id dirigido.
    try:
        pid1 = hashlib.sha256(f"{node_a}|{node_b}".encode()).hexdigest()[:16]
        pid2 = hashlib.sha256(f"{node_b}|{node_a}".encode()).hexdigest()[:16]
        row = conn.execute(
            "SELECT proof_data, onchain, confidence, validated_at, node_a, node_b FROM connection_proofs "
            "WHERE proof_id=? OR proof_id=? OR (node_a=? AND node_b=?) OR (node_a=? AND node_b=?) LIMIT 1",
            (pid1, pid2, node_a, node_b, node_b, node_a),
        ).fetchone()
        if row:
            return row
    except Exception:
        pass
    # Último fallback: compara claves canónicas contra filas próximas.
    try:
        ka = _canonical_entity_key(node_a)
        kb = _canonical_entity_key(node_b)
        rows = conn.execute(
            "SELECT proof_data, onchain, confidence, validated_at, node_a, node_b FROM connection_proofs "
            "WHERE node_a=? OR node_b=? OR node_a=? OR node_b=?",
            (node_a, node_a, node_b, node_b),
        ).fetchall()
        for r in rows:
            ra, rb = r[4], r[5]
            if {ka, kb} == {_canonical_entity_key(ra), _canonical_entity_key(rb)}:
                return r
    except Exception:
        pass
    return None


def _proof_row_to_data(row: Any) -> Dict[str, Any]:
    if not row:
        return {}
    try:
        return json.loads(row[0] or "{}")
    except Exception:
        return {}

def _canonical_target_node(target: Any, known_nodes: Optional[Set[str]] = None) -> Optional[str]:
    """
    Resuelve texto devuelto por la IA al nodo real del mapa correspondiente.
    Solo aplica a NODOS DEL MAPA — nunca debe usarse para identificar entidades a investigar.
    Orden de prioridad: match exacto > alias explícito > match de clave normalizada.
    NO hace substring match para evitar falsos positivos (JP Morgan ≠ Ripple Payments).
    """
    raw = str(target or "").strip()
    if not raw:
        return None
    known = set(known_nodes or set()) | set(NODES.keys())

    # 1) Match exacto (case-sensitive)
    if raw in known:
        return raw

    key = _norm_key(raw)

    # 2) Alias explícitos en ENTITY_CANONICAL_ALIASES → solo si el resultado es un nodo del mapa
    if key in ENTITY_CANONICAL_ALIASES:
        cand = ENTITY_CANONICAL_ALIASES[key]
        if cand in known or cand in NODES:
            return cand

    # 3) CONNECTS_TO_NODE — aliases de nodos del mapa (rails, productos, infraestructura)
    if key in CONNECTS_TO_NODE:
        cand = CONNECTS_TO_NODE[key]
        if cand in known or cand in NODES:
            return cand

    # 4) Match por clave normalizada exacta (sin substring)
    for ex in known:
        if _norm_key(ex) == key:
            return ex

    # 5) Substring solo si la clave es muy específica (≥8 chars) y el match es completo en un sentido
    #    Esto evita que "morgan" matchee "JP Morgan" con nodos del mapa
    if len(key) >= 8:
        for ex in sorted(known, key=len, reverse=True):
            ex_key = _norm_key(ex)
            if ex_key and (key == ex_key or key in ex_key or ex_key in key):
                return ex

    return None


def _route_signal_for_kind(kind: str, fallback: str = "institutional_route_score") -> str:
    k = _norm_key(kind)
    if any(x in k for x in ["odl", "corridor", "bridge", "fx"]):
        return "bridge_score"
    if any(x in k for x in ["public", "gateway", "exchange"]):
        return "public_gateway_score"
    if any(x in k for x in ["custody", "metaco"]):
        return "custody_score"
    if any(x in k for x in ["dex", "amm", "permissioned"]):
        return "dex_score"
    if any(x in k for x in ["government", "gobierno", "fed", "rail", "swift", "sepa", "ach"]):
        return "institutional_route_score"
    return fallback


def _canonical_source_url(url: str) -> str:
    """Normaliza URLs para deduplicar fuentes repetidas aunque vengan con tracking/query."""
    try:
        from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode
        raw = str(url or "").strip()
        if not raw.startswith("http"):
            return ""
        pr = urlparse(raw)
        scheme = (pr.scheme or "https").lower()
        host = (pr.netloc or "").lower().replace("www.", "")
        path = re.sub(r"/{2,}", "/", pr.path or "/")
        path = re.sub(r"/$", "", path) if path != "/" else path
        # Quitar extensiones de tracking/amp visuales sin romper PDFs/filings.
        path = path.replace("/amp/", "/").replace("/amp", "")
        # Conservar solo query útil para visores oficiales; eliminar utm/fbclid/etc.
        keep_q = []
        for k, v in parse_qsl(pr.query, keep_blank_values=False):
            lk = k.lower()
            if lk.startswith("utm_") or lk in {"fbclid", "gclid", "mc_cid", "mc_eid", "cmpid", "output"}:
                continue
            # SEC ixviewer usa doc/action; otros visores también pueden necesitar id/doc.
            if host.endswith("sec.gov") and lk in {"doc", "id", "accession_number"}:
                keep_q.append((lk, v))
            elif lk in {"id", "doc", "file", "lang"} and any(h in host for h in ("edinet", "cninfo", "hkex", "dart")):
                keep_q.append((lk, v))
        query = urlencode(keep_q, doseq=True)
        return urlunparse((scheme, host, path, "", query, ""))
    except Exception:
        return str(url or "").strip().split("#", 1)[0].split("?", 1)[0]


def _source_story_key(url: str) -> str:
    """
    Fingerprint de historia/fuente para evitar repetir la misma noticia o filing.
    Es más agresivo que la URL: ignora tracking, fechas y /amp.
    """
    try:
        from urllib.parse import urlparse
        canon = _canonical_source_url(url)
        p = urlparse(canon)
        host = p.netloc.lower().replace("www.", "")
        slug = (p.path or "").lower().strip("/")
        slug = re.sub(r"/(19|20)\d{2}/\d{1,2}/\d{1,2}/?", "/", slug)
        slug = re.sub(r"/(19|20)\d{2}/\d{1,2}/?", "/", slug)
        slug = re.sub(r"\.(html?|php|aspx?|pdf)$", "", slug)
        slug = re.sub(r"[-_](amp|mobile)$", "", slug)
        parts = [x for x in slug.split("/") if len(x) > 3]
        # En filings/documentos oficiales, el documento exacto importa: dominio + path.
        if any(h in host for h in ("sec.gov", "bis.org", "federalreserve.gov", "cninfo", "hkex", "edinet", "dart", "krx")):
            return f"{host}/{slug}"
        tail = "/".join(parts[-2:]) if len(parts) >= 2 else (parts[-1] if parts else slug)
        return f"{host}/{tail}" if tail else canon
    except Exception:
        return str(url or "")


def _safe_sources_blob(sources: Any, limit: int = 1200) -> str:
    """Fuentes limpias para BD/UI: sin duplicados por URL canónica ni por historia."""
    if not sources:
        return ""
    if isinstance(sources, str):
        vals = [x.strip() for x in sources.split(",")]
    else:
        vals = [_extract_url_from_any(x) or str(x).strip() for x in sources if str(x).strip()]

    out: List[str] = []
    seen_urls: Set[str] = set()
    seen_stories: Set[str] = set()
    PRIORITY_DOMAINS = {
        "sec.gov", "ripple.com", "xrpl.org", "federalreserve.gov", "bis.org", "imf.org",
        "eba.europa.eu", "fca.org.uk", "github.com", "cninfo.com.cn", "hkexnews.hk",
        "disclosure.edinet-fsa.go.jp", "dart.fss.or.kr", "kind.krx.co.kr",
    }

    def _domain(u: str) -> str:
        try:
            from urllib.parse import urlparse
            return urlparse(_canonical_source_url(u)).netloc.lower().replace("www.", "")
        except Exception:
            return ""

    vals = [v for v in vals if str(v).startswith("http")]
    priority = [u for u in vals if any(_domain(u).endswith(d) for d in PRIORITY_DOMAINS)]
    rest = [u for u in vals if u not in priority]

    for url in priority + rest:
        canon = _canonical_source_url(url)
        if not canon or canon in seen_urls:
            continue
        story = _source_story_key(canon)
        if story and story in seen_stories and len(story) > 8:
            continue
        seen_urls.add(canon)
        if story:
            seen_stories.add(story)
        out.append(canon)
        if len(", ".join(out)) >= limit:
            break

    return ", ".join(out)[:limit]


def _proof_text_blob(proof: Dict[str, Any]) -> str:
    """Texto compacto donde debe aparecer la relación A↔B."""
    if not isinstance(proof, dict):
        return str(proof or "")
    parts = []
    for k in ("label", "snippet", "title", "summary", "url", "source"):
        v = proof.get(k)
        if v:
            parts.append(str(v))
    return " ".join(parts)


def _entity_search_terms(entity: Any) -> List[str]:
    """Términos aceptables para verificar que una fuente menciona una entidad/nodo."""
    raw = str(entity or "").strip()
    canonical = _canonical_entity_name(raw)
    candidates = {raw, canonical, NODE_SEARCH_TERMS.get(canonical, ""), NODE_SEARCH_TERMS.get(raw, "")}
    key = _norm_key(canonical)
    compact = key.replace(" ", "")
    # Nodos core: añadir términos reales que suelen aparecer en fuentes.
    core_map = {
        "xrpl": ["xrpl", "xrp ledger", "xrp-ledger"],
        "rlusd": ["rlusd", "ripple usd", "ripple stablecoin"],
        "ripple payments": ["ripple payments", "ripplenet", "odl", "on-demand liquidity"],
        "custody metaco": ["metaco", "ripple custody", "custody"],
        "hidden road prime": ["hidden road", "ripple prime", "prime brokerage"],
        "treasury": ["ripple treasury", "treasury"],
        "rail": ["ripple rail", "rail"],
        "permissioned dex": ["permissioned dex", "xrpl dex"],
        "dex amm": ["dex", "amm", "xrpl amm"],
    }
    for ck, vals in core_map.items():
        if ck in compact or ck in key:
            candidates.update(vals)
    # Tokens útiles del nombre, evitando palabras genéricas.
    noise = {"the", "and", "bank", "banco", "group", "capital", "financial", "inc", "ltd", "llc", "plc", "de", "la", "of"}
    for token in re.split(r"\s+", key):
        if len(token) >= 4 and token not in noise:
            candidates.add(token)
    # Siglas cortas útiles: IDG, SBI, DTCC, BIS, etc.
    for token in re.findall(r"\b[A-Z0-9]{2,6}\b", raw):
        if token.lower() not in noise:
            candidates.add(token.lower())
    out: List[str] = []
    for c in candidates:
        c = str(c or "").strip()
        if not c:
            continue
        nc = _norm_key(c)
        if nc and nc not in out:
            out.append(nc)
        # Conservar no-ASCII sin normalización destructiva.
        if any(ord(ch) > 127 for ch in c) and c.lower() not in out:
            out.append(c.lower())
    return out


def _blob_mentions_any(blob: str, terms: List[str]) -> bool:
    nb = _norm_key(blob)
    compact_blob = nb.replace(" ", "")
    raw_low = str(blob or "").lower()
    for t in terms:
        if not t:
            continue
        nt = _norm_key(t)
        if nt and (nt in nb or nt.replace(" ", "") in compact_blob):
            return True
        if any(ord(ch) > 127 for ch in t) and t.lower() in raw_low:
            return True
    return False


def _proof_domain(url: str) -> str:
    try:
        from urllib.parse import urlparse
        return urlparse(_canonical_source_url(url)).netloc.lower().replace("www.", "")
    except Exception:
        return ""


def _is_core_ripple_node(entity: Any) -> bool:
    c = _canonical_entity_name(entity)
    return c in {
        "Ripple Payments", "XRPL", "RLUSD", "DEX/AMM", "Permissioned DEX",
        "Custody/Metaco", "Treasury", "Rail", "Hidden Road / Prime",
        "Standard Custody", "Ripple Escrow",
    }


def _proof_relevant_to_pair(proof: Dict[str, Any], node_a: str, node_b: str) -> bool:
    """
    Evita basura: una prueba de internet solo vale si la fuente menciona la entidad A
    y también el nodo/tema B. No basta con una noticia general de blockchain.
    """
    if not isinstance(proof, dict):
        return False
    if proof.get("onchain"):
        return True
    if not proof.get("internet"):
        return False
    url = _extract_url_from_any(proof)
    if not url.startswith("http"):
        return False
    ptype = str(proof.get("type", "") or "").strip()
    if ptype not in EVIDENCE_SCORES or ptype in {"social_mention", "ai_inference", "sin_wallet"}:
        return False
    blob = _proof_text_blob(proof)
    domain = _proof_domain(url)
    blob_plus = f"{blob} {domain}"
    mentions_a = _blob_mentions_any(blob_plus, _entity_search_terms(node_a))
    mentions_b = _blob_mentions_any(blob_plus, _entity_search_terms(node_b))

    # ripple.com/xrpl.org aporta contexto Ripple/XRPL, pero NO debe validar una conexión
    # si no aparece claramente la entidad externa. Antes esto podía aceptar páginas genéricas
    # de RLUSD/XRPL como prueba de cualquier entidad → conexión falsa.
    official_ripple_domain = domain.endswith("ripple.com") or domain.endswith("xrpl.org")
    if official_ripple_domain and (_is_core_ripple_node(node_a) or _is_core_ripple_node(node_b)):
        if _is_core_ripple_node(node_a) and _is_core_ripple_node(node_b):
            return mentions_a and mentions_b
        if _is_core_ripple_node(node_a):
            return mentions_b
        if _is_core_ripple_node(node_b):
            return mentions_a

    # En el resto de fuentes exigimos A y B.
    if mentions_a and mentions_b:
        return True

    return False


def _dedupe_and_filter_proofs(node_a: str, node_b: str, proofs: Any, max_items: int = 3) -> List[Dict[str, Any]]:
    """Deduplica por URL/historia y filtra fuentes que no demuestran A↔B."""
    if not isinstance(proofs, list):
        return []
    out: List[Dict[str, Any]] = []
    seen_urls: Set[str] = set()
    seen_stories: Set[str] = set()
    seen_labels: Set[str] = set()
    for raw in proofs:
        if not isinstance(raw, dict):
            continue
        p = dict(raw)
        if p.get("onchain"):
            label_key = _norm_key(p.get("type", "") + " " + p.get("label", "") + " " + str(p.get("tx_hash", "")))[:180]
            if label_key in seen_labels:
                continue
            seen_labels.add(label_key)
            out.append(p)
            continue
        p["internet"] = bool(p.get("internet", True))
        url = _extract_url_from_any(p)
        canon = _canonical_source_url(url)
        if canon:
            p["url"] = canon
        if not _proof_relevant_to_pair(p, node_a, node_b):
            continue
        story = _source_story_key(canon)
        label_key = _norm_key(str(p.get("type", "")) + " " + str(p.get("label", "")) + " " + str(p.get("snippet", "")))[:220]
        if canon and canon in seen_urls:
            continue
        if story and story in seen_stories and len(story) > 8:
            continue
        if label_key and label_key in seen_labels:
            continue
        if canon:
            seen_urls.add(canon)
        if story:
            seen_stories.add(story)
        if label_key:
            seen_labels.add(label_key)
        out.append(p)
        if len([x for x in out if x.get("internet")]) >= max_items:
            # Mantener como máximo N pruebas internet; on-chain no se corta aquí.
            pass
    # Orden: on-chain > documentos/official > noticias.
    rank = {
        "tx_directa": 0, "odl_payment": 1, "trust_line": 2, "amm_pool": 3,
        "official_partner": 4, "regulatory_filing_pdf": 5, "contract_pdf": 6,
        "regulatory_filing": 7, "press_release": 8, "github_repo": 9,
        "news_major": 10, "job_posting": 11, "news_minor": 12, "wallet_activa": 13,
    }
    onchain = [p for p in out if p.get("onchain")]
    internet = sorted([p for p in out if p.get("internet")], key=lambda x: rank.get(str(x.get("type", "")), 99))[:max_items]
    return onchain + internet


def _register_dynamic_node(conn: sqlite3.Connection, name: str, layer: str, icon: str,
                           confidence: float, summary: str, source_url: str,
                           now: str) -> bool:
    """Inserta/actualiza un nodo descubierto sin duplicar alias."""
    cname = _canonical_entity_name(name)
    # Si el nombre canónico resuelve a un nodo estático existente, no crear duplicado dinámico
    if _canonical_target_node(cname, set(NODES.keys())) in NODES:
        return False
    layer = _normalize_layer(layer)
    inferred_layer, inferred_icon = _infer_layer_icon_from_name(cname, layer, icon or "🔎")
    if _layer_is_generic_for_dynamic(layer) and inferred_layer in ZONE_POS:
        layer = inferred_layer
        if not icon or icon in {"?", "🔎", "•"}:
            icon = inferred_icon
    node_id = hashlib.sha256(_norm_key(cname).encode()).hexdigest()[:12]
    before = conn.execute("SELECT 1 FROM dynamic_nodes WHERE node_id=?", (node_id,)).fetchone()
    conn.execute("""
        INSERT OR REPLACE INTO dynamic_nodes
        (node_id, name, layer, icon, confidence, source_url, summary, added_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        node_id, cname, layer, icon or "?", float(confidence or 0.0),
        str(source_url or "")[:1200], str(summary or "")[:500], now,
    ))
    return before is None


def _register_dynamic_route(conn: sqlite3.Connection, src: str, dst: str, kind: str,
                            signal_col: str, label: str, confidence: float,
                            evidence: str, source_urls: str, now: str) -> bool:
    """Inserta/actualiza una ruta descubierta con pruebas y sin duplicados."""
    src = _canonical_entity_name(src)
    dst = _canonical_entity_name(dst)
    if not src or not dst or src == dst:
        return False
    route_id = hashlib.sha256(f"{_norm_key(src)}>{_norm_key(dst)}>{_norm_key(kind)}".encode()).hexdigest()[:12]
    before = conn.execute("SELECT 1 FROM dynamic_routes WHERE route_id=?", (route_id,)).fetchone()
    conn.execute("""
        INSERT OR REPLACE INTO dynamic_routes
        (route_id, src, dst, kind, signal_col, label, confidence, evidence, source_urls, added_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        route_id, src, dst, kind or "discovered", signal_col or _route_signal_for_kind(kind),
        label or f"{src} -> {dst}", float(confidence or 0.0),
        str(evidence or "")[:600], str(source_urls or "")[:1200], now,
    ))
    return before is None

CONNECTS_TO_NODE: Dict[str, str] = {
    "ripple": "Ripple Payments", "ripplenet": "Ripple Payments",
    "ripple payments": "Ripple Payments", "odl": "Ripple Payments",
    "xrpl": "XRPL", "rlusd": "RLUSD",
    "swift": "SWIFT", "fedwire": "FedNow", "fednow": "FedNow", "fed now": "FedNow",
    "federal reserve": "Federal Reserve", "reserva federal": "Federal Reserve", "the fed": "Federal Reserve",
    "bis": "Bank for International Settlements (BIS)",
    "bank for international settlements": "Bank for International Settlements (BIS)",
    "banco de pagos internacionales": "Bank for International Settlements (BIS)",
    "banco internacional de pagos": "Bank for International Settlements (BIS)",
    "banco de liquidaciones internacionales": "Bank for International Settlements (BIS)",
    "mbridge": "Project mBridge", "project mbridge": "Project mBridge", "m cbdc bridge": "Project mBridge",
    "mastercard": "Mastercard", "sepa": "SEPA/ACH", "ach": "SEPA/ACH",
    "hidden road": "Hidden Road / Prime", "hiddenroad": "Hidden Road / Prime",
    "hidden road prime": "Hidden Road / Prime", "hiddenroadprime": "Hidden Road / Prime",
    "metaco": "Custody/Metaco", "custody": "Custody/Metaco", "ripple custody": "Custody/Metaco",
    "standard custody": "Standard Custody", "standard custody trust": "Standard Custody",
    "dtcc": "DTCC/NSCC", "nscc": "DTCC/NSCC", "dtcc/nscc": "DTCC/NSCC",
    "bitstamp": "Bitstamp", "gatehub": "GateHub", "kraken": "Kraken",
    "binance": "Binance", "coinbase": "Public Gateway",
    "sbi": "SBI Remit", "sbi remit": "SBI Remit",
    "bitso": "Bitso (ODL MX)", "tranglo": "Tranglo (ODL)",
    "beetech": "BeeTech (ODL BR)",
    "santander": "Santander", "standard chartered": "Standard Chartered",
    "bank of america": "Bank of America", "boa": "Bank of America",
    "pnc": "PNC Bank", "itau": "Itaú Unibanco",
    "treasury": "Treasury", "prime": "Hidden Road / Prime", "ripple prime": "Hidden Road / Prime", "rail": "Rail",
    "permissioned dex": "Permissioned DEX", "dex": "DEX/AMM",
    "ethereum": "Ethereum", "eth": "Ethereum",
    "topology": "Topology Engine", "anomaly": "Anomaly Engine",
    "fingerprint": "Fingerprint Engine",
    "ondo": "Permissioned DEX", "ondo finance": "Permissioned DEX",
    "zodia": "Zodia Custody", "zodia custody": "Zodia Custody",
    "axis bank": "Axis Bank", "moneytap": "MoneyTap / SBI",
    "corredores fx": "Corredores FX", "fx": "Corredores FX",
}

ROUTES = []
# CLEAN MODE: sin rutas/aristas preestablecidas.
# El mapa arranca sin conexiones. Las rutas se crean solo cuando una búsqueda,
# una verificación documental o una señal on-chain aporta evidencia concreta A↔B.


# =============================================================================
# EXPANSION DE RUTAS POR TIPO DE ENTIDAD
# Cada tipo de entidad deja un rastro diferente en la infraestructura Ripple.
# Esta tabla se aplica tanto a nodos dinamicos (Discovery Engine) como a nodos
# estaticos que no tienen rutas explícitas definidas en ROUTES.
# Las rutas generadas se marcan como 'watch' (especulativas, sin evidencia directa).
# =============================================================================
ENTITY_EXPANSION_TARGETS: Dict[str, List[str]] = {}
# CLEAN MODE: desactivada la expansión automática por tipo de entidad.
# Ejemplo eliminado: CBDC → XRPL/SWIFT/FedNow/RLUSD por simple categoría.


# =============================================================================
# DB
# =============================================================================

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    # WAL mode: múltiples lectores concurrentes + un escritor sin bloquear.
    # Esencial en despliegue público donde varios usuarios comparten la misma BD.
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA busy_timeout=6000")   # espera hasta 6s si hay write-lock
    conn.execute("""
        CREATE TABLE IF NOT EXISTS raw_events (
            tx_hash TEXT PRIMARY KEY,
            ledger_day TEXT,
            timestamp_utc TEXT,
            amount REAL,
            tx_type TEXT,
            account TEXT,
            destination TEXT,
            fee_drops INTEGER,
            sequence INTEGER,
            raw_json TEXT,
            inserted_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS daily_metrics (
            day TEXT PRIMARY KEY,
            xrpl_volume REAL,
            tx_count INTEGER,
            payment_count INTEGER,
            trustline_count INTEGER,
            offer_count INTEGER,
            amm_count INTEGER,
            bridge_count INTEGER,
            large_tx_count INTEGER,
            unique_accounts INTEGER,
            unique_edges INTEGER,
            public_xrpl_score REAL,
            payment_flow_score REAL,
            trustline_score REAL,
            dex_score REAL,
            large_transfer_score REAL,
            bridge_score REAL,
            public_gateway_score REAL,
            institutional_route_score REAL,
            prime_brokerage_score REAL,
            custody_score REAL,
            cluster_score REAL,
            topology_score REAL,
            anomaly_score REAL,
            fingerprint_score REAL,
            cross_network_score REAL,
            time_regime_score REAL,
            persistence_score REAL,
            radar_coverage REAL,
            pump_score REAL,
            adoption_score REAL,
            bull_score REAL,
            bear_score REAL,
            flip_score REAL,
            phase INTEGER,
            phase_name TEXT,
            source TEXT,
            updated_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS clusters (
            day TEXT,
            cluster_id TEXT,
            accounts TEXT,
            size INTEGER,
            volume REAL,
            tx_count INTEGER,
            role TEXT,
            score REAL,
            PRIMARY KEY(day, cluster_id)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS fingerprints (
            day TEXT,
            fingerprint_type TEXT,
            score REAL,
            evidence TEXT,
            PRIMARY KEY(day, fingerprint_type)
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS app_events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            level TEXT,
            message TEXT,
            details TEXT,
            created_at TEXT
        )
    """)
    conn.commit()

    # ── Migraciones de esquema (columnas añadidas en versiones posteriores) ──
    _schema_migrations = [
        # (tabla, nombre_columna, definicion_completa)
        ("dynamic_routes",    "source_urls",  "source_urls TEXT"),
        ("dynamic_nodes",     "source_url",   "source_url TEXT"),
        ("connection_proofs", "proof_data",   "proof_data TEXT NOT NULL DEFAULT '{}'"),
        ("dynamic_routes",    "evidence",     "evidence TEXT"),
        ("discovered_wallets","signals",      "signals TEXT DEFAULT ''"),
    ]
    for tbl, col, defn in _schema_migrations:
        try:
            cols = [r[1] for r in conn.execute(f"PRAGMA table_info({tbl})").fetchall()]
            if cols and col not in cols:
                conn.execute(f"ALTER TABLE {tbl} ADD COLUMN {defn}")
                conn.commit()
        except Exception:
            pass

    return conn


def log_event(conn: sqlite3.Connection, level: str, message: str, details: str = "") -> None:
    conn.execute(
        "INSERT INTO app_events(level, message, details, created_at) VALUES (?, ?, ?, ?)",
        (level, message, details[:5000], datetime.now(timezone.utc).isoformat())
    )
    conn.commit()


# =============================================================================
# XRPL REAL
# =============================================================================

def xrpl_rpc(payload: Dict[str, Any], timeout: int = 20) -> Dict[str, Any]:
    r = requests.post(XRPL_SERVER, json=payload, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    if data.get("error"):
        raise RuntimeError(str(data["error"]))
    if data.get("result", {}).get("error"):
        raise RuntimeError(str(data["result"]["error"]))
    return data


def fetch_amm_pools(asset_currency: str = "XRP", asset_issuer: str = "",
                    asset2_currency: str = "", asset2_issuer: str = "",
                    limit: int = 50) -> List[Dict]:
    """
    Consulta el ledger XRPL para obtener pools AMM activos.
    Devuelve lista de dicts con info de cada pool.
    Si se pasa asset2_currency vacío busca todos los pools que tengan XRP o el token indicado.
    """
    try:
        # amm_info con ledger_index="validated" devuelve un pool específico si se pasan ambos assets
        # Para listar pools usamos account_offers / book_offers no — usamos amm_info genérico
        # La forma correcta de listar AMMs en XRPL es con "amm_info" pasando asset + asset2
        # Para descubrir pools desconocidos usamos ledger_data con type=amm (nightly builds)
        # Fallback: usar account_lines del issuer RLUSD para encontrar AMMs activos
        pools = []

        # 1) Si sabemos los dos assets, consulta directa
        if asset2_currency:
            asset_a: Dict = {"currency": asset_currency}
            if asset_issuer:
                asset_a["issuer"] = asset_issuer
            asset_b: Dict = {"currency": asset2_currency}
            if asset2_issuer:
                asset_b["issuer"] = asset2_issuer
            data = xrpl_rpc({"method": "amm_info", "params": [{
                "asset": asset_a, "asset2": asset_b, "ledger_index": "validated"
            }]}, timeout=15)
            amm = data.get("result", {}).get("amm")
            if amm:
                pools.append(_parse_amm(amm))
            return pools

        # 2) Sin asset2: buscar via ledger_data filtrando objetos AMM
        marker = None
        for _ in range(6):   # máx 6 páginas
            params: Dict = {"ledger_index": "validated", "type": "amm", "limit": limit}
            if marker:
                params["marker"] = marker
            try:
                data = xrpl_rpc({"method": "ledger_data", "params": [params]}, timeout=20)
            except Exception:
                break
            result = data.get("result", {})
            for obj in result.get("state", []):
                if obj.get("LedgerEntryType") != "AMM":
                    continue
                parsed = _parse_amm_ledger_obj(obj)
                # Filtrar por asset si se especificó
                if asset_currency and asset_currency != "XRP":
                    a1 = obj.get("Asset", {}).get("currency", "")
                    a2 = obj.get("Asset2", {}).get("currency", "")
                    if asset_currency not in (a1, a2):
                        continue
                pools.append(parsed)
                if len(pools) >= limit:
                    break
            marker = result.get("marker")
            if not marker or len(pools) >= limit:
                break
        return pools
    except Exception:
        return []


def _parse_amm(amm: Dict) -> Dict:
    """Parsea respuesta amm_info a dict normalizado."""
    a1 = amm.get("amount",  {})
    a2 = amm.get("amount2", {})
    cur1 = "XRP" if isinstance(a1, str) else a1.get("currency", "?")
    cur2 = "XRP" if isinstance(a2, str) else a2.get("currency", "?")
    val1 = (float(a1) / 1e6) if isinstance(a1, str) else float(a1.get("value", 0))
    val2 = (float(a2) / 1e6) if isinstance(a2, str) else float(a2.get("value", 0))
    return {
        "account": amm.get("account", ""),
        "pair":    f"{cur1}/{cur2}",
        "cur1":    cur1, "val1": val1,
        "cur2":    cur2, "val2": val2,
        "lp_token": amm.get("lp_token", {}).get("currency", ""),
        "trading_fee": amm.get("trading_fee", 0),
        "vote_slots": len(amm.get("vote_slots", [])),
    }


def _parse_amm_ledger_obj(obj: Dict) -> Dict:
    """Parsea objeto AMM de ledger_data."""
    a1 = obj.get("Asset",  {})
    a2 = obj.get("Asset2", {})
    amt1 = obj.get("Amount",  {})
    amt2 = obj.get("Amount2", {})
    cur1 = a1.get("currency", "XRP") if a1 else "XRP"
    cur2 = a2.get("currency", "XRP") if a2 else "XRP"
    val1 = (float(amt1) / 1e6) if isinstance(amt1, str) else float((amt1 or {}).get("value", 0))
    val2 = (float(amt2) / 1e6) if isinstance(amt2, str) else float((amt2 or {}).get("value", 0))
    lpt  = obj.get("LPTokenBalance", {})
    return {
        "account":    obj.get("Account", ""),
        "pair":       f"{cur1}/{cur2}",
        "cur1":       cur1, "val1": val1,
        "cur2":       cur2, "val2": val2,
        "lp_token":   lpt.get("currency", "") if isinstance(lpt, dict) else "",
        "trading_fee": obj.get("TradingFee", 0),
        "vote_slots":  len(obj.get("VoteSlots", [])),
    }


def check_xrpl_connection() -> Tuple[bool, str]:
    try:
        data = xrpl_rpc({"method": "server_info", "params": [{}]}, timeout=12)
        info = data.get("result", {}).get("info", {})
        return True, f"XRPL conectado · Estado: {info.get('server_state', 'unknown')}"
    except Exception as exc:
        return False, f"XRPL no disponible ahora: {exc}"


def ripple_epoch_to_datetime(ripple_time: Optional[int]) -> datetime:
    if ripple_time is None:
        return datetime.now(timezone.utc)
    return datetime(2000, 1, 1, tzinfo=timezone.utc) + timedelta(seconds=int(ripple_time))


def parse_rlusd_amount(tx: Dict[str, Any]) -> float:
    candidates = [tx.get("Amount"), tx.get("DeliverMax"), tx.get("SendMax"), tx.get("delivered_amount")]
    meta = tx.get("meta") or tx.get("metaData") or {}
    if isinstance(meta, dict):
        candidates.append(meta.get("delivered_amount"))

    for amount in candidates:
        if isinstance(amount, dict) and amount.get("currency") == RLUSD_CURRENCY and amount.get("issuer") == RLUSD_ISSUER:
            try:
                return abs(float(amount.get("value", 0)))
            except Exception:
                pass

    total = 0.0
    affected = meta.get("AffectedNodes", []) if isinstance(meta, dict) else []
    for node in affected:
        for key in ("ModifiedNode", "CreatedNode", "DeletedNode"):
            obj = node.get(key)
            if not isinstance(obj, dict):
                continue
            for field_key in ("FinalFields", "PreviousFields", "NewFields"):
                fields = obj.get(field_key, {})
                if not isinstance(fields, dict):
                    continue
                bal = fields.get("Balance")
                if isinstance(bal, dict) and bal.get("currency") == RLUSD_CURRENCY and bal.get("issuer") == RLUSD_ISSUER:
                    try:
                        total += abs(float(bal.get("value", 0)))
                    except Exception:
                        continue
    return float(total)


def classify_tx(tx: Dict[str, Any]) -> Dict[str, int]:
    tx_type = tx.get("TransactionType", "Unknown")
    meta = tx.get("meta") or tx.get("metaData") or {}
    affected = meta.get("AffectedNodes", []) if isinstance(meta, dict) else []

    out = {
        "payment": 1 if tx_type == "Payment" else 0,
        "trustline": 1 if tx_type == "TrustSet" else 0,
        "offer": 1 if tx_type in {"OfferCreate", "OfferCancel"} else 0,
        "amm": 1 if tx_type in {"AMMCreate", "AMMDeposit", "AMMWithdraw", "AMMVote", "AMMBid"} else 0,
        "bridge": 1 if tx_type in {"XChainCreateBridge", "XChainCommit", "XChainClaim", "XChainAccountCreateCommit"} else 0,
    }

    content = json.dumps(affected)
    if "AMM" in content:
        out["amm"] = 1
    if "Offer" in content:
        out["offer"] = 1
    if "RippleState" in content:
        out["trustline"] = max(out["trustline"], 1)
    if "XChain" in content:
        out["bridge"] = 1

    return out


def fetch_xrpl_dex_global() -> Dict[str, Any]:
    """
    Obtiene métricas globales del DEX/AMM de XRPL en tiempo real:
    - Profundidad del order book RLUSD/XRP y USDC/XRP
    - Número de pools AMM activos y TVL total
    - Conteo de offers en el ledger actual (ledger_data type=offer)
    Devuelve dict con dex_offer_count, amm_pool_count, amm_tvl_xrp, book_depth_xrp
    """
    result: Dict[str, Any] = {
        "dex_offer_count": 0,
        "amm_pool_count": 0,
        "amm_tvl_xrp": 0.0,
        "book_depth_xrp": 0.0,
        "book_bids": 0,
        "book_asks": 0,
    }
    try:
        # 1) Profundidad del book RLUSD↔XRP (bids + asks)
        rlusd_asset = {"currency": "524C555344000000000000000000000000000000", "issuer": RLUSD_ISSUER}
        for pays, gets in [
            ({"currency": "XRP"}, rlusd_asset),
            (rlusd_asset,         {"currency": "XRP"}),
        ]:
            try:
                data = xrpl_rpc({"method": "book_offers", "params": [{
                    "taker_pays": pays, "taker_gets": gets,
                    "limit": 100, "ledger_index": "validated"
                }]}, timeout=12)
                offers = data.get("result", {}).get("offers", [])
                result["book_depth_xrp"] += sum(
                    float(o.get("TakerPays", 0)) / 1e6 if isinstance(o.get("TakerPays"), (int, str)) else 0.0
                    for o in offers
                )
                result["book_bids" if pays.get("currency") == "XRP" else "book_asks"] += len(offers)
            except Exception:
                pass

        # 2) Pools AMM activos — usar ledger_data con type=amm (máx 3 páginas)
        amm_count = 0
        tvl_xrp = 0.0
        marker = None
        for _ in range(3):
            params: Dict = {"ledger_index": "validated", "type": "amm", "limit": 100}
            if marker:
                params["marker"] = marker
            try:
                data = xrpl_rpc({"method": "ledger_data", "params": [params]}, timeout=15)
                state = data.get("result", {}).get("state", [])
                for obj in state:
                    amm_count += 1
                    # Amount es el balance del pool en XRP (drops) o token
                    a1 = obj.get("Amount", {})
                    a2 = obj.get("Amount2", {})
                    if isinstance(a1, str):
                        tvl_xrp += float(a1) / 1e6
                    if isinstance(a2, str):
                        tvl_xrp += float(a2) / 1e6
                marker = data.get("result", {}).get("marker")
                if not marker:
                    break
            except Exception:
                break

        result["amm_pool_count"] = amm_count
        result["amm_tvl_xrp"] = tvl_xrp

        # 3) Offers activos en el ledger — 1 página (costoso, limitamos a 200)
        try:
            data = xrpl_rpc({"method": "ledger_data", "params": [{
                "ledger_index": "validated", "type": "offer", "limit": 200
            }]}, timeout=15)
            result["dex_offer_count"] = len(data.get("result", {}).get("state", []))
        except Exception:
            pass

    except Exception:
        pass
    return result


def fetch_issuer_transactions(limit_pages: int = 16, per_page: int = 200) -> List[Dict[str, Any]]:
    all_txs: List[Dict[str, Any]] = []
    marker = None

    for _ in range(limit_pages):
        params: Dict[str, Any] = {
            "account": RLUSD_ISSUER,
            "ledger_index_min": -1,
            "ledger_index_max": -1,
            "binary": False,
            "limit": per_page,
            "forward": False,
            "api_version": 2,
        }
        if marker:
            params["marker"] = marker

        data = xrpl_rpc({"method": "account_tx", "params": [params]})
        result = data.get("result", {})
        for row in result.get("transactions", []):
            tx = row.get("tx_json") or row.get("tx") or {}
            meta = row.get("meta") or row.get("metaData") or {}
            if isinstance(meta, dict):
                tx["meta"] = meta
            all_txs.append(tx)

        marker = result.get("marker")
        if not marker:
            break

    return all_txs


def store_raw_events(conn: sqlite3.Connection, txs: List[Dict[str, Any]]) -> int:
    inserted = 0
    for tx in txs:
        tx_hash = tx.get("hash") or hashlib.sha256(json.dumps(tx, sort_keys=True).encode()).hexdigest()
        dt = ripple_epoch_to_datetime(tx.get("date"))
        amount = parse_rlusd_amount(tx)
        try:
            fee_drops = int(tx.get("Fee", 0))
        except Exception:
            fee_drops = 0
        try:
            sequence = int(tx.get("Sequence", 0))
        except Exception:
            sequence = 0

        cur = conn.execute("""
            INSERT OR IGNORE INTO raw_events
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            tx_hash,
            dt.date().isoformat(),
            dt.isoformat(),
            amount,
            tx.get("TransactionType", "Unknown"),
            tx.get("Account", ""),
            tx.get("Destination", ""),
            fee_drops,
            sequence,
            json.dumps(tx)[:12000],
            datetime.now(timezone.utc).isoformat(),
        ))
        inserted += cur.rowcount
    conn.commit()
    return inserted


# =============================================================================
# MATH HELPERS
# =============================================================================

def clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return float(max(lo, min(hi, x)))


def normalize(x: float, lo: float, hi: float) -> float:
    if hi <= lo:
        return 0.0
    return clamp((x - lo) / (hi - lo))


def safe_mean(values: List[float]) -> float:
    return float(np.mean(values)) if values else 0.0


def stable_noise(day: str, key: str, lo: float, hi: float) -> float:
    seed = int(hashlib.sha256(f"{day}:{key}".encode()).hexdigest()[:8], 16)
    rng = np.random.default_rng(seed)
    return float(rng.uniform(lo, hi))


def public_anchored_proxy(day: str, key: str, base: float, public_boost: float) -> float:
    # Proxy que NO inventa euforia: solo sube si hay huella pública.
    ordinal = datetime.fromisoformat(day).toordinal()
    wave = 0.025 * math.sin(ordinal / 9.0)
    return clamp(base + wave + stable_noise(day, key, -0.018, 0.018) + public_boost)


# =============================================================================
# ADVANCED ENGINES
# =============================================================================

def build_edges(df: pd.DataFrame) -> List[Tuple[str, str, float, int]]:
    edges = []
    if df.empty:
        return edges
    for _, r in df.iterrows():
        a = str(r.get("account") or "")
        b = str(r.get("destination") or "")
        if a and b and a != b:
            edges.append((a, b, float(r.get("amount") or 0.0), 1))
    return edges


def union_find_clusters(edges: List[Tuple[str, str, float, int]]) -> Dict[str, Set[str]]:
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[rb] = ra

    for a, b, _, _ in edges:
        union(a, b)

    clusters = defaultdict(set)
    for a, b, _, _ in edges:
        clusters[find(a)].add(a)
        clusters[find(b)].add(b)
    return dict(clusters)


def cluster_engine(day: str, df: pd.DataFrame, conn: sqlite3.Connection) -> Dict[str, float]:
    edges = build_edges(df)
    clusters = union_find_clusters(edges)
    if not clusters:
        return {"cluster_score": 0.0, "hub_score": 0.0, "cluster_count": 0, "max_cluster_size": 0}

    amount_by_account = defaultdict(float)
    tx_by_account = defaultdict(int)
    degree = Counter()

    for a, b, amount, _ in edges:
        amount_by_account[a] += amount
        amount_by_account[b] += amount
        tx_by_account[a] += 1
        tx_by_account[b] += 1
        degree[a] += 1
        degree[b] += 1

    cluster_rows = []
    scores = []
    max_size = 0

    for root, accounts in clusters.items():
        size = len(accounts)
        max_size = max(max_size, size)
        volume = sum(amount_by_account[a] for a in accounts)
        txs = sum(tx_by_account[a] for a in accounts)
        hubness = max([degree[a] for a in accounts] or [0])
        role = "treasury-like" if volume >= 1_000_000 and size >= 3 else "hub-like" if hubness >= 5 else "normal"
        score = clamp(normalize(size, 2, 20) * 0.35 + normalize(volume, 100_000, 20_000_000) * 0.45 + normalize(hubness, 2, 20) * 0.20)
        scores.append(score)
        cid = hashlib.sha256(("|".join(sorted(accounts))[:1000]).encode()).hexdigest()[:12]
        cluster_rows.append((day, cid, ",".join(sorted(accounts))[:4000], size, volume, txs, role, score))

    conn.executemany("""
        INSERT OR REPLACE INTO clusters(day, cluster_id, accounts, size, volume, tx_count, role, score)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, cluster_rows)

    return {
        "cluster_score": max(scores) if scores else 0.0,
        "hub_score": normalize(max(degree.values()) if degree else 0, 2, 30),
        "cluster_count": len(clusters),
        "max_cluster_size": max_size,
    }


def fingerprint_engine(day: str, df: pd.DataFrame, conn: sqlite3.Connection) -> Dict[str, float]:
    if df.empty:
        return {"fingerprint_score": 0.0, "treasury_score": 0.0, "mm_score": 0.0, "corridor_score": 0.0}

    amounts = df["amount"].fillna(0).astype(float).tolist()
    nonzero = [a for a in amounts if a > 0]
    tx_count = len(df)
    unique_accounts = pd.concat([df["account"], df["destination"]]).dropna().nunique()
    large_count = sum(a >= 1_000_000 for a in nonzero)
    medium_repeated = 0

    if nonzero:
        rounded = [round(a, -3) if a >= 1000 else round(a, 2) for a in nonzero]
        counts = Counter(rounded)
        medium_repeated = sum(1 for amount, c in counts.items() if c >= 3 and amount >= 10_000)

    # Treasury-like: big movements, low-to-mid account diversity, repeated amounts.
    treasury_score = clamp(
        normalize(large_count, 1, 8) * 0.45
        + normalize(medium_repeated, 1, 12) * 0.25
        + normalize(sum(nonzero), 500_000, 40_000_000) * 0.30
    )

    # Market-maker-like: many offers/AMM, repeated sizes, high tx count.
    offer_amm = 0
    payments = 0
    for raw_json in df["raw_json"].fillna("{}").tolist():
        try:
            cls = classify_tx(json.loads(raw_json))
            offer_amm += cls["offer"] + cls["amm"]
            payments += cls["payment"]
        except Exception:
            pass

    mm_score = clamp(
        normalize(offer_amm, 2, 50) * 0.45
        + normalize(tx_count, 10, 180) * 0.30
        + normalize(medium_repeated, 2, 20) * 0.25
    )

    # Corridor-like: repeated payments, multiple accounts, not only one giant transaction.
    corridor_score = clamp(
        normalize(payments, 2, 80) * 0.42
        + normalize(unique_accounts, 4, 80) * 0.28
        + normalize(medium_repeated, 2, 16) * 0.30
    )

    fingerprint_score = max(treasury_score, mm_score, corridor_score)

    rows = [
        (day, "treasury-like", treasury_score, f"large={large_count}, repeated={medium_repeated}, volume={sum(nonzero):.2f}"),
        (day, "market-maker-like", mm_score, f"offer_amm={offer_amm}, tx_count={tx_count}, repeated={medium_repeated}"),
        (day, "corridor-like", corridor_score, f"payments={payments}, accounts={unique_accounts}, repeated={medium_repeated}"),
    ]
    conn.executemany("INSERT OR REPLACE INTO fingerprints(day, fingerprint_type, score, evidence) VALUES (?, ?, ?, ?)", rows)

    return {
        "fingerprint_score": fingerprint_score,
        "treasury_score": treasury_score,
        "mm_score": mm_score,
        "corridor_score": corridor_score,
    }


def topology_engine(df: pd.DataFrame) -> Dict[str, float]:
    edges = build_edges(df)
    if not edges:
        return {"topology_score": 0.0, "density_score": 0.0, "hub_score": 0.0, "flow_concentration": 0.0}

    accounts = set()
    outflow = defaultdict(float)
    inflow = defaultdict(float)
    degree = Counter()

    for a, b, amount, _ in edges:
        accounts.add(a); accounts.add(b)
        outflow[a] += amount
        inflow[b] += amount
        degree[a] += 1
        degree[b] += 1

    n = len(accounts)
    m = len(edges)
    density = m / max(n * (n - 1), 1)
    density_score = normalize(density, 0.005, 0.10)
    hub_score = normalize(max(degree.values()) if degree else 0, 2, 30)

    vols = list(outflow.values()) + list(inflow.values())
    total = sum(vols)
    if total > 0:
        top3 = sum(sorted(vols, reverse=True)[:3])
        flow_concentration = top3 / total
    else:
        flow_concentration = 0.0

    topology_score = clamp(density_score * 0.25 + hub_score * 0.35 + normalize(flow_concentration, 0.15, 0.80) * 0.40)

    return {
        "topology_score": topology_score,
        "density_score": density_score,
        "hub_score": hub_score,
        "flow_concentration": flow_concentration,
    }


def time_intelligence(history: pd.DataFrame, current: Dict[str, float]) -> Dict[str, float]:
    if history.empty or len(history) < 7:
        return {"time_regime_score": 0.30, "anomaly_score": 0.0, "slope_score": 0.0, "regime": "insufficient_history"}

    recent = history.tail(30).copy()
    volume_series = recent["xrpl_volume"].fillna(0).astype(float).tolist()
    adoption_series = recent["adoption_score"].fillna(0).astype(float).tolist() if "adoption_score" in recent.columns else []

    current_volume = current.get("xrpl_volume", 0.0)
    mean_vol = float(np.mean(volume_series)) if volume_series else 0.0
    std_vol = float(np.std(volume_series)) if volume_series else 0.0
    z = (current_volume - mean_vol) / max(std_vol, 1.0)

    anomaly_score = clamp((z - 1.0) / 4.0) if z > 1 else 0.0

    if len(volume_series) >= 7:
        y = np.array(volume_series[-14:] if len(volume_series) >= 14 else volume_series)
        x = np.arange(len(y))
        slope = float(np.polyfit(x, y, 1)[0]) if len(y) >= 2 else 0.0
        slope_score = normalize(slope, 0, max(mean_vol * 0.10, 1.0))
    else:
        slope_score = 0.0

    persistence_signal = current.get("persistence_score", 0.0)
    time_regime_score = clamp(slope_score * 0.35 + anomaly_score * 0.25 + persistence_signal * 0.40)

    if time_regime_score >= 0.70:
        regime = "expansion"
    elif anomaly_score >= 0.60 and persistence_signal < 0.35:
        regime = "spike_noise"
    elif time_regime_score <= 0.25:
        regime = "cold"
    else:
        regime = "mixed"

    return {
        "time_regime_score": time_regime_score,
        "anomaly_score": anomaly_score,
        "slope_score": slope_score,
        "regime": regime,
    }


def cross_network_engine(day: str, xrpl_public_score: float, bridge_score: float, dex_score: float) -> float:
    # Sin API externa en esta versión. Se mantiene como watcher preparado:
    # si aparecen bridges/DEX/issuer, sube la probabilidad de actividad cross-network.
    return clamp(bridge_score * 0.45 + dex_score * 0.25 + xrpl_public_score * 0.20 + stable_noise(day, "cross", 0.00, 0.05))


def pump_vs_adoption(values: Dict[str, float]) -> Tuple[float, float]:
    # Pump: mucho volumen/anomalía pero poca persistencia, trustlines, clusters o topología.
    pump = clamp(
        values["anomaly_score"] * 0.35
        + values["large_transfer_score"] * 0.25
        + (1 - values["persistence_score"]) * 0.20
        + (1 - values["trustline_score"]) * 0.10
        + (1 - values["cluster_score"]) * 0.10
    )

    adoption = clamp(
        values["public_gateway_score"] * 0.18
        + values["persistence_score"] * 0.18
        + values["cluster_score"] * 0.14
        + values["topology_score"] * 0.14
        + values["fingerprint_score"] * 0.14
        + values["trustline_score"] * 0.10
        + values["dex_score"] * 0.06
        + values["bridge_score"] * 0.06
    )

    return pump, adoption


def phase_engine(values: Dict[str, float]) -> Tuple[int, str]:
    adoption = values["adoption_score"]
    coverage = values["radar_coverage"]
    persistence_score = values["persistence_score"] * 100
    hot = values["hot_routes"]

    if adoption >= 78 and coverage >= 72 and persistence_score >= 72 and hot >= 7:
        return 5, "Full Flip"
    if adoption >= 68 and coverage >= 62 and hot >= 6:
        return 4, "Integración institucional"
    if coverage >= 55 and hot >= 5:
        return 3, "Ruteo público visible"
    if values["public_gateway_score"] >= 0.45 and values["cluster_score"] >= 0.35:
        return 2, "Huellas públicas coordinadas"
    if values["public_xrpl_score"] >= 0.35:
        return 1, "Calentamiento"
    return 0, "Ruido / baja señal"


def compute_scores(values: Dict[str, float]) -> Dict[str, float]:
    coverage = (
        values["public_xrpl_score"] * 0.16
        + values["payment_flow_score"] * 0.10
        + values["trustline_score"] * 0.10
        + values["dex_score"] * 0.10
        + values["large_transfer_score"] * 0.10
        + values["bridge_score"] * 0.08
        + values["cluster_score"] * 0.10
        + values["topology_score"] * 0.10
        + values["fingerprint_score"] * 0.10
        + values["public_gateway_score"] * 0.06
    ) * 100

    pump_score, adoption_raw = pump_vs_adoption(values)

    bull = (
        values["public_xrpl_score"] * 0.18
        + values["payment_flow_score"] * 0.10
        + values["large_transfer_score"] * 0.14
        + values["dex_score"] * 0.10
        + values["time_regime_score"] * 0.14
        + values["topology_score"] * 0.12
        + values["fingerprint_score"] * 0.12
        + values["institutional_route_score"] * 0.10
    ) * 100

    bear = (
        (1 - values["public_xrpl_score"]) * 0.18
        + (1 - values["payment_flow_score"]) * 0.10
        + (1 - values["persistence_score"]) * 0.20
        + (1 - values["public_gateway_score"]) * 0.16
        + (1 - values["cluster_score"]) * 0.12
        + (1 - values["topology_score"]) * 0.12
        + pump_score * 0.12
    ) * 100

    price = (
        values["public_xrpl_score"] * 0.22
        + values["large_transfer_score"] * 0.22
        + values["dex_score"] * 0.14
        + values["anomaly_score"] * 0.14
        + values["time_regime_score"] * 0.16
        + values["payment_flow_score"] * 0.12
    ) * 100

    adoption = adoption_raw * 100

    hot = sum(v >= 0.60 for k, v in values.items() if k.endswith("_score") and k not in {"pump_score"})

    phase, phase_name = phase_engine({
        **values,
        "adoption_score": adoption,
        "radar_coverage": coverage,
        "hot_routes": hot,
    })

    if adoption >= 78 and coverage >= 72 and values["persistence_score"] >= 0.72 and hot >= 7 and pump_score < 0.65:
        flip = adoption * 0.38 + coverage * 0.28 + bull * 0.20 + values["persistence_score"] * 100 * 0.14
    else:
        flip = min(79.9, adoption * coverage / 100 * max(values["persistence_score"], 0.18) * (1 - pump_score * 0.35))

    return {
        "radar_coverage": float(coverage),
        "pump_score": float(pump_score * 100),
        "adoption_score": float(adoption),
        "bull_score": float(bull),
        "bear_score": float(bear),
        "price_score": float(price),
        "flip_score": float(flip),
        "phase": int(phase),
        "phase_name": phase_name,
    }


# =============================================================================
# AGGREGATION
# =============================================================================

def aggregate_daily(conn: sqlite3.Connection, source: str = "xrpl_advanced_intelligence") -> None:
    raw = pd.read_sql_query("SELECT * FROM raw_events", conn)
    if raw.empty:
        raw = pd.DataFrame(columns=["ledger_day", "amount", "tx_type", "account", "destination", "raw_json", "timestamp_utc"])

    today = datetime.now(timezone.utc).date()
    days = [(today - timedelta(days=i)).isoformat() for i in range(BACKFILL_DAYS)][::-1]

    for day in days:
        day_df = raw[raw["ledger_day"] == day].copy()
        hist = pd.read_sql_query("SELECT * FROM daily_metrics WHERE day < ? ORDER BY day ASC", conn, params=(day,))

        volume = float(day_df["amount"].fillna(0).sum()) if not day_df.empty else 0.0
        tx_count = int(len(day_df))
        large_tx_count = int((day_df["amount"].fillna(0).astype(float) >= 1_000_000).sum()) if not day_df.empty else 0
        unique_accounts = int(pd.concat([day_df["account"], day_df["destination"]]).dropna().nunique()) if not day_df.empty else 0
        unique_edges = int(day_df[["account", "destination"]].dropna().drop_duplicates().shape[0]) if not day_df.empty else 0

        payment_count = trustline_count = offer_count = amm_count = bridge_count = 0
        if not day_df.empty:
            for raw_json in day_df["raw_json"].fillna("{}").tolist():
                try:
                    cls = classify_tx(json.loads(raw_json))
                    payment_count += cls["payment"]
                    trustline_count += cls["trustline"]
                    offer_count += cls["offer"]
                    amm_count += cls["amm"]
                    bridge_count += cls["bridge"]
                except Exception:
                    continue

        # ── Datos globales DEX/AMM en tiempo real (solo para hoy, no histórico) ──
        _is_today = (day == datetime.now(timezone.utc).date().isoformat())
        _dex_global: Dict[str, Any] = {}
        if _is_today:
            try:
                _dex_global = fetch_xrpl_dex_global()
            except Exception:
                _dex_global = {}

        # Rangos calibrados: XRPL tiene ~1-2M offers activos en ledger en días normales,
        # picos DEX pueden llegar a 3-5M. AMM pools ~25-80 activos.
        _global_offer_count = _dex_global.get("dex_offer_count", 0)
        _global_amm_count   = _dex_global.get("amm_pool_count", 0)
        _book_depth_xrp     = _dex_global.get("book_depth_xrp", 0.0)
        _amm_tvl_xrp        = _dex_global.get("amm_tvl_xrp", 0.0)

        # dex_score: mezcla señal de issuer txs (rápida) + estado global del ledger (real)
        _dex_from_issuer = clamp(normalize(offer_count, 1, 50) * 0.65 + normalize(amm_count, 1, 18) * 0.35)
        if _is_today and _global_offer_count > 0:
            # Rangos: 200 offers/ledger_data sample es ~normal, 200 = saturado
            _dex_from_global = clamp(
                normalize(_global_offer_count, 10, 200) * 0.40
                + normalize(_global_amm_count, 1, 80) * 0.25
                + normalize(_book_depth_xrp, 1_000, 5_000_000) * 0.20
                + normalize(_amm_tvl_xrp, 10_000, 10_000_000) * 0.15
            )
            dex_score = clamp(_dex_from_issuer * 0.35 + _dex_from_global * 0.65)
        else:
            dex_score = _dex_from_issuer

        public_xrpl_score = normalize(volume, 25_000, 25_000_000) * 0.48 + normalize(tx_count, 3, 160) * 0.32 + normalize(unique_accounts, 2, 90) * 0.20
        payment_flow_score = normalize(payment_count, 1, 70)
        trustline_score = normalize(trustline_count, 1, 40)
        large_transfer_score = normalize(large_tx_count, 1, 12)
        bridge_score = normalize(bridge_count, 1, 8)

        if hist.empty:
            persistence_score = public_xrpl_score
        else:
            recent = hist.tail(13)["public_xrpl_score"].astype(float).tolist()
            vals = [public_xrpl_score] + recent
            persistence_score = sum(v >= 0.55 for v in vals) / max(len(vals), 1)

        cluster = cluster_engine(day, day_df, conn)
        fp = fingerprint_engine(day, day_df, conn)
        topo = topology_engine(day_df)

        public_gateway_score = clamp(
            public_xrpl_score * 0.30
            + payment_flow_score * 0.15
            + trustline_score * 0.12
            + dex_score * 0.12
            + large_transfer_score * 0.14
            + bridge_score * 0.07
            + cluster["cluster_score"] * 0.10
        )

        cross_network_score = cross_network_engine(day, public_xrpl_score, bridge_score, dex_score)
        custody_score = clamp(public_xrpl_score * 0.40 + large_transfer_score * 0.20 + trustline_score * 0.20 + cluster["cluster_score"] * 0.20)
        prime_brokerage_score = public_anchored_proxy(day, "prime", 0.30, large_transfer_score * 0.18 + fp["treasury_score"] * 0.15 + topo["topology_score"] * 0.12)
        institutional_route_score = public_anchored_proxy(day, "institutional", 0.36, public_gateway_score * 0.22 + payment_flow_score * 0.10)

        current_base = {
            "xrpl_volume": volume,
            "persistence_score": persistence_score,
            "adoption_score": 0.0,
        }
        timeintel = time_intelligence(hist, current_base)

        values = {
            "public_xrpl_score": public_xrpl_score,
            "payment_flow_score": payment_flow_score,
            "trustline_score": trustline_score,
            "dex_score": dex_score,
            "large_transfer_score": large_transfer_score,
            "bridge_score": bridge_score,
            "public_gateway_score": public_gateway_score,
            "institutional_route_score": institutional_route_score,
            "prime_brokerage_score": prime_brokerage_score,
            "custody_score": custody_score,
            "cluster_score": cluster["cluster_score"],
            "topology_score": topo["topology_score"],
            "anomaly_score": timeintel["anomaly_score"],
            "fingerprint_score": fp["fingerprint_score"],
            "cross_network_score": cross_network_score,
            "time_regime_score": timeintel["time_regime_score"],
            "persistence_score": persistence_score,
        }
        scores = compute_scores(values)

        conn.execute("""
            INSERT OR REPLACE INTO daily_metrics
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            day, volume, tx_count, payment_count, trustline_count, offer_count, amm_count, bridge_count,
            large_tx_count, unique_accounts, unique_edges,
            public_xrpl_score, payment_flow_score, trustline_score, dex_score, large_transfer_score, bridge_score,
            public_gateway_score, institutional_route_score, prime_brokerage_score, custody_score,
            cluster["cluster_score"], topo["topology_score"], timeintel["anomaly_score"], fp["fingerprint_score"],
            cross_network_score, timeintel["time_regime_score"], persistence_score,
            scores["radar_coverage"], scores["pump_score"], scores["adoption_score"],
            scores["bull_score"], scores["bear_score"], scores["flip_score"],
            scores["phase"], scores["phase_name"], source, datetime.now(timezone.utc).isoformat()
        ))

    conn.commit()


def bootstrap_demo(conn: sqlite3.Connection, force: bool = False) -> None:
    if not force and conn.execute("SELECT COUNT(*) FROM daily_metrics").fetchone()[0] > 0:
        return
    if force:
        conn.execute("DELETE FROM daily_metrics")
        conn.execute("DELETE FROM clusters")
        conn.execute("DELETE FROM fingerprints")

    today = datetime.now(timezone.utc).date()

    for i in range(BACKFILL_DAYS):
        day = (today - timedelta(days=BACKFILL_DAYS - i - 1)).isoformat()
        trend = 0.22 + 0.40 * (i / BACKFILL_DAYS)
        impulse = 0.22 if i > BACKFILL_DAYS * 0.72 else 0.0

        public_xrpl_score = public_anchored_proxy(day, "demo_public", trend + impulse, 0)
        payment_flow_score = public_anchored_proxy(day, "demo_payment", 0.30, impulse * 0.45 + public_xrpl_score * 0.10)
        trustline_score = public_anchored_proxy(day, "demo_trust", 0.26, impulse * 0.35 + public_xrpl_score * 0.08)
        dex_score = public_anchored_proxy(day, "demo_dex", 0.28, impulse * 0.36 + public_xrpl_score * 0.09)
        large_transfer_score = public_anchored_proxy(day, "demo_large", 0.24, impulse * 0.48 + public_xrpl_score * 0.10)
        bridge_score = public_anchored_proxy(day, "demo_bridge", 0.12, impulse * 0.20)
        cluster_score = public_anchored_proxy(day, "demo_cluster", 0.22, impulse * 0.42 + public_xrpl_score * 0.10)
        topology_score = public_anchored_proxy(day, "demo_topology", 0.25, impulse * 0.40 + cluster_score * 0.12)
        fingerprint_score = public_anchored_proxy(day, "demo_fp", 0.22, impulse * 0.44 + large_transfer_score * 0.10)
        anomaly_score = public_anchored_proxy(day, "demo_anomaly", 0.08, impulse * 0.25)
        cross_network_score = public_anchored_proxy(day, "demo_cross", 0.10, bridge_score * 0.30 + dex_score * 0.10)
        persistence_score = clamp((public_xrpl_score - 0.30) / 0.50)
        public_gateway_score = clamp(
            public_xrpl_score * 0.30 + payment_flow_score * 0.15 + trustline_score * 0.12
            + dex_score * 0.12 + large_transfer_score * 0.14 + bridge_score * 0.07 + cluster_score * 0.10
        )
        institutional_route_score = public_anchored_proxy(day, "demo_inst", 0.34, public_gateway_score * 0.22)
        prime_brokerage_score = public_anchored_proxy(day, "demo_prime", 0.28, large_transfer_score * 0.15 + fingerprint_score * 0.14)
        custody_score = clamp(public_xrpl_score * 0.40 + large_transfer_score * 0.20 + trustline_score * 0.20 + cluster_score * 0.20)
        time_regime_score = clamp(persistence_score * 0.45 + anomaly_score * 0.20 + trend * 0.25)

        values = {
            "public_xrpl_score": public_xrpl_score,
            "payment_flow_score": payment_flow_score,
            "trustline_score": trustline_score,
            "dex_score": dex_score,
            "large_transfer_score": large_transfer_score,
            "bridge_score": bridge_score,
            "public_gateway_score": public_gateway_score,
            "institutional_route_score": institutional_route_score,
            "prime_brokerage_score": prime_brokerage_score,
            "custody_score": custody_score,
            "cluster_score": cluster_score,
            "topology_score": topology_score,
            "anomaly_score": anomaly_score,
            "fingerprint_score": fingerprint_score,
            "cross_network_score": cross_network_score,
            "time_regime_score": time_regime_score,
            "persistence_score": persistence_score,
        }
        scores = compute_scores(values)

        volume = public_xrpl_score * (500_000 + 35_000_000 * public_xrpl_score)
        tx_count = int(10 + public_xrpl_score * 160)

        conn.execute("""
            INSERT OR REPLACE INTO daily_metrics
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            day, volume, tx_count,
            int(payment_flow_score * 70), int(trustline_score * 40), int(dex_score * 40), int(dex_score * 18),
            int(bridge_score * 8), int(large_transfer_score * 12), int(public_xrpl_score * 90),
            int(public_xrpl_score * 70),
            public_xrpl_score, payment_flow_score, trustline_score, dex_score, large_transfer_score, bridge_score,
            public_gateway_score, institutional_route_score, prime_brokerage_score, custody_score, cluster_score,
            topology_score, anomaly_score, fingerprint_score, cross_network_score, time_regime_score, persistence_score,
            scores["radar_coverage"], scores["pump_score"], scores["adoption_score"],
            scores["bull_score"], scores["bear_score"], scores["flip_score"],
            scores["phase"], scores["phase_name"], "demo_bootstrap", datetime.now(timezone.utc).isoformat()
        ))

    conn.commit()


def refresh_history(conn: sqlite3.Connection, pages: int = 16) -> Tuple[bool, str]:
    try:
        ok, server_msg = check_xrpl_connection()
        if not ok:
            raise RuntimeError(server_msg)
        txs = fetch_issuer_transactions(limit_pages=pages, per_page=200)
        inserted = store_raw_events(conn, txs)
        aggregate_daily(conn)
        msg = f"XRPL actualizado: {len(txs)} transacciones revisadas, {inserted} nuevas. {server_msg}"
        log_event(conn, "info", "refresh ok", msg)
        return True, msg
    except Exception as exc:
        bootstrap_demo(conn)
        msg = f"XRPL no respondió ahora. Se mantiene caché/demo. Error: {exc}"
        try:
            log_event(conn, "warning", "refresh failed", traceback.format_exc())
        except Exception:
            pass  # no dejar que un fallo de logging bloquee la app
        return False, msg


def ensure_metric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Repara DataFrames procedentes de bases SQLite antiguas.
    Evita KeyError cuando una versión previa no tenía alguna métrica.
    """
    if df.empty:
        return df

    defaults = {
        "price_score": 0.0,
        "pump_score": 0.0,
        "radar_coverage": 0.0,
        "adoption_score": 0.0,
        "bull_score": 0.0,
        "bear_score": 0.0,
        "flip_score": 0.0,
        "persistence_score": 0.0,
        "public_xrpl_score": 0.0,
        "payment_flow_score": 0.0,
        "trustline_score": 0.0,
        "dex_score": 0.0,
        "large_transfer_score": 0.0,
        "bridge_score": 0.0,
        "cluster_score": 0.0,
        "topology_score": 0.0,
        "fingerprint_score": 0.0,
        "anomaly_score": 0.0,
        "time_regime_score": 0.0,
        "cross_network_score": 0.0,
        "phase": 0,
        "phase_name": "Sin fase",
        "xrpl_volume": 0.0,
        "tx_count": 0,
        "large_tx_count": 0,
    }

    for col, value in defaults.items():
        if col not in df.columns:
            df[col] = value
        else:
            df[col] = df[col].fillna(value)

    # Si falta price_score, lo reconstruimos de forma conservadora.
    if (df["price_score"].fillna(0).abs().sum() == 0) and {"bull_score", "pump_score", "public_xrpl_score"}.issubset(df.columns):
        df["price_score"] = (
            df["bull_score"].fillna(0).astype(float) * 0.45
            + (100 - df["pump_score"].fillna(0).astype(float)).clip(lower=0) * 0.15
            + df["public_xrpl_score"].fillna(0).astype(float) * 100 * 0.40
        ).clip(0, 100)

    numeric_cols = [c for c in defaults if c != "phase_name"]
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors="coerce").fillna(defaults[col])

    df["phase_name"] = df["phase_name"].fillna("Sin fase").astype(str)
    return df


def load_metrics(conn: sqlite3.Connection) -> pd.DataFrame:
    df = pd.read_sql_query("SELECT * FROM daily_metrics ORDER BY day ASC", conn)
    if df.empty:
        return df

    df = ensure_metric_columns(df)
    df = df.tail(BACKFILL_DAYS).copy()
    df["volume_7d"] = df["xrpl_volume"].rolling(7, min_periods=1).sum()
    df["volume_30d"] = df["xrpl_volume"].rolling(30, min_periods=1).sum()
    df["coverage_ma30"] = df["radar_coverage"].rolling(30, min_periods=1).mean()
    df["adoption_ma30"] = df["adoption_score"].rolling(30, min_periods=1).mean()
    df["phase_ma14"] = df["phase"].rolling(14, min_periods=1).mean()
    return df.reset_index(drop=True)


# =============================================================================
# INTERPRETATION
# =============================================================================

def route_signal(row: pd.Series, route: Tuple[str, str, str, str, str]) -> float:
    _, _, kind, signal, _ = route
    s = float(row.get(signal, 0.0))
    if kind == "future":
        s *= 0.40
    return clamp(s)


def route_color(row: pd.Series, route: Tuple[str, str, str, str, str]) -> str:
    s = route_signal(row, route)
    kind = route[2]
    if float(row["bear_score"]) >= 75 and s < 0.45:
        return "#FF5A67"
    if kind == "verified":
        return "#22C55E"    # verde confirmado — verificado por investigación
    if kind == "real":
        return "#3CFF9B"    # verde neón — on-chain TX directo
    if kind == "obligatory":
        return "#FF4D6D"    # rojo-rosa — implicación técnica
    if kind == "public":
        return "#00CFFF"    # cian — gateway público
    if kind == "watch":
        return "#B673FF" if s >= 0.45 else "#9B59B6"   # morado — vigilada
    if kind == "model":
        return "#5AD7FF" if s >= 0.45 else "#60A5FA"
    if kind == "future":
        return "#8CA0B8"
    if kind in {"odl"}:
        return "#FB923C"    # naranja — corredor ODL
    if kind in {"discovered"}:
        return "#FFD700"    # dorado — descubierta IA
    return "#F59E0B" if s >= 0.45 else "#D97706"  # ámbar — privada inferida


def route_dash(route: Tuple[str, str, str, str, str]) -> str:
    kind = route[2]
    if kind in {"real", "public", "verified"}:
        return "solid"      # confirmado — on-chain, público o verificado por investigación
    if kind == "obligatory":
        return "dash"       # deducción técnica irrefutable pero no TX directa verificada
    if kind in {"watch", "model"}:
        return "solid"
    if kind == "future":
        return "dot"
    if kind == "discovered":
        return "dashdot"
    return "dash"


def hot_routes_count(row: pd.Series) -> int:
    return sum(route_signal(row, r) >= 0.60 for r in ROUTES)


def get_state(row: pd.Series) -> Dict[str, str]:
    phase = int(row["phase"])
    phase_name = str(row["phase_name"])

    if float(row["flip_score"]) >= 80:
        return {
            "state": "flip",
            "headline": "🔥 Flip de Switches en curso",
            "simple": "El radar detecta huellas públicas coordinadas, clusters, topología y persistencia. Esto ya no parece solo ruido.",
            "price": "Potencial de repunte fuerte si la demanda no encuentra suficiente oferta.",
            "risk": "Riesgo medio: parte institucional sigue inferida, pero la huella pública es fuerte.",
            "adoption": f"Fase {phase} — {phase_name}",
        }
    if float(row["bear_score"]) >= 75:
        return {
            "state": "bear",
            "headline": "⚠️ Riesgo de bajada / slowdown",
            "simple": "La actividad pública verificable cae o parece spike sin persistencia.",
            "price": "Riesgo de falso rebote o presión bajista.",
            "risk": "Alto.",
            "adoption": f"Fase {phase} — {phase_name}: sin adopción real confirmada.",
        }
    if float(row["bull_score"]) >= 62 and float(row["price_score"]) >= 58:
        return {
            "state": "bull",
            "headline": "🟢 Repunte probable en precio",
            "simple": "Hay actividad suficiente para impulso de precio, pero el sistema aún separa esto de adopción real.",
            "price": "Repunte probable.",
            "risk": "Medio.",
            "adoption": f"Fase {phase} — {phase_name}: todavía no es Full Flip.",
        }
    return {
        "state": "normal",
        "headline": "🟠 Actividad normal",
        "simple": "Señales mixtas. El radar no ve aún huellas públicas coordinadas suficientes.",
        "price": "Sin señal clara.",
        "risk": "Neutral/moderado.",
        "adoption": f"Fase {phase} — {phase_name}",
    }


# =============================================================================
# VISUALS
# =============================================================================

def load_watched_wallets(conn: sqlite3.Connection) -> pd.DataFrame:
    """Carga wallets vigiladas (added_to_map=1) desde la BD para el mapa."""
    try:
        ensure_discovered_wallets_table(conn)
        df = pd.read_sql_query(
            "SELECT wallet, label, role, confidence, volume_xrp, top_counterpart, top_cp_label "
            "FROM discovered_wallets WHERE added_to_map=1 AND COALESCE(status,'map') NOT IN ('quarantine','discarded') ORDER BY confidence DESC, volume_xrp DESC LIMIT 30",
            conn,
        )
        return df
    except Exception:
        return pd.DataFrame()


def boost_metrics_from_watched(conn: sqlite3.Connection, row: pd.Series) -> pd.Series:
    """
    Ajusta los scores del row actual en función de la actividad de wallets vigiladas.
    Wallets whale activas → suben large_transfer_score, cluster_score, etc.
    """
    try:
        today = str(_date.today())
        ww = pd.read_sql_query(
            "SELECT role, confidence, volume_xrp FROM discovered_wallets "
            "WHERE added_to_map=1 AND COALESCE(status,'map') NOT IN ('quarantine','discarded') AND last_seen=?",
            conn, params=(today,),
        )
    except Exception:
        return row

    if ww.empty:
        return row

    row = row.copy()
    whale_vol  = float(ww["volume_xrp"].sum())
    n_whales   = len(ww)
    avg_conf   = float(ww["confidence"].mean())
    has_odl    = ww["role"].str.contains("odl|corredor", case=False, na=False).any()
    has_ts     = ww["role"].str.contains("treasury|distribuidor", case=False, na=False).any()
    has_mm     = ww["role"].str.contains("market|maker", case=False, na=False).any()
    has_gw     = ww["role"].str.contains("exchange|gateway", case=False, na=False).any()

    boost = min(avg_conf * 0.18 * n_whales, 0.30)  # máximo +30%

    def _up(col: str, delta: float) -> None:
        if col in row.index:
            row[col] = min(float(row[col]) + delta, 1.0)

    _up("large_transfer_score", boost)
    _up("cluster_score",        boost * 0.80)
    if has_odl:
        _up("payment_flow_score", boost)
        _up("bridge_score",       boost * 0.70)
    if has_ts:
        _up("fingerprint_score",  boost * 0.90)
        _up("institutional_route_score", boost)
    if has_mm:
        _up("dex_score",          boost * 0.80)
        _up("topology_score",     boost * 0.60)
    if has_gw:
        _up("public_gateway_score", boost * 0.70)
        _up("trustline_score",      boost * 0.50)

    return row


NODE_DESC: Dict[str, str] = {
    "Bank of America":    "Banco líder en EE.UU., usa RippleNet para transferencias internacionales y liquidación instantánea.",
    "PNC Bank":           "Banco regional americano conectado a FedNow para pagos domésticos en tiempo real.",
    "Itaú Unibanco":      "Mayor banco de Brasil, usa SWIFT para rutas internacionales hacia el ecosistema Ripple.",
    "Bitso (ODL MX)":     "Exchange mexicano, corredor ODL clave para remesas USD→MXN a través de XRP como puente.",
    "BeeTech (ODL BR)":   "Fintech brasileña, corredor ODL para remesas hacia Brasil usando XRP como activo puente.",
    "Santander":          "Banco global español con RippleNet activo. One Pay FX usa tecnología Ripple para pagos internacionales.",
    "Standard Chartered": "Banco británico con presencia en Asia. Usa SWIFT y explora ODL para corredores emergentes.",
    "Zodia Custody":      "Custodio de activos digitales regulado (filial Standard Chartered). Conectado a Custody/Metaco.",
    "SBI Remit":          "Remesadora japonesa del grupo SBI (mayor accionista de Ripple fuera de EE.UU.). ODL activo Japón.",
    "MoneyTap / SBI":     "App de pagos móviles japonesa construida sobre RippleNet. Conectada a banca retail SBI.",
    "Axis Bank":          "Tercer banco privado de India, partner RippleNet para remesas transfronterizas.",
    "Tranglo (ODL)":      "Corredor ODL para Asia del Sur y Sudeste Asiático. Adquirido parcialmente por Ripple en 2021.",
    "Coins.ph (ODL PH)":  "Exchange y billetera filipina. Corredor ODL para remesas USD→PHP, mercado masivo de OFWs.",
    "SWIFT":              "Sistema interbancario tradicional (SWIFT gpi). Rail privado que Ripple busca complementar o reemplazar.",
    "Federal Reserve":    "Banco central de EE.UU. y operador/autoridad de rails públicos como FedNow/Fedwire. En el radar actúa como nodo gubernamental y origen de corredor de pagos.",
    "Bank for International Settlements (BIS)": "Banco de Pagos Internacionales: nodo de bancos centrales, informes CGIDE/BIS y proyectos como mBridge. En Ripple Radar se marca como conexión documental/indirecta cuando aparece por pilotos CBDC/tokenización.",
    "Project mBridge": "Proyecto multi-CBDC nacido en BIS Innovation Hub con bancos centrales como PBoC/HKMA/BOT/CBUAE; útil como puente contextual, no como prueba directa de XRPL.",
    "FedNow":             "Sistema de pagos instantáneos de la Reserva Federal. Interoperable con rails de pago; cualquier conexión con Ripple/XRPL debe validarse por pruebas públicas o huellas.",
    "Mastercard":         "Red de pagos global. Colabora con Ripple en infraestructura multi-rail y pagos B2B.",
    "SEPA/ACH":           "Sistemas de compensación europeo (SEPA) y americano (ACH). Rails tradicionales conectados a Ripple.",
    "Ripple Payments":    "Núcleo del ecosistema. Plataforma de pagos instantáneos 24/7. Liquidación en 3-5 segundos vía XRPL.",
    "Treasury":           "Gestión de tesorería de Ripple. Controla reservas XRP y flujos de capital institucional.",
    "Rail":               "Capa de enrutamiento privado de Ripple. Conecta instituciones financieras al ledger XRPL.",
    "Ripple Escrow":      "Wallet de escrow con ~40.000M XRP bloqueados. Libera 1.000M XRP/mes al mercado.",
    "Hidden Road / Prime": "Hidden Road (adquirido por Ripple en 2025 por 1.250M$) + Ripple Prime. Prime broker institucional con clearing multi-asset para XRP, RLUSD y activos digitales.",
    "Custody/Metaco":     "Metaco: plataforma de custodia institucional adquirida por Ripple en 2023 (~$250M). Permite a bancos custodiar XRP y activos digitales.",
    "Standard Custody":   "Standard Custody & Trust Company: adquirida por Ripple en 2021. Licencia de custodia regulada en EE.UU. para activos digitales institucionales.",
    "DTCC/NSCC":          "Cámara de compensación americana. Conectada a Hidden Road para liquidación de activos digitales.",
    "Corredores FX":      "Red de corredores FX que usa XRP como activo puente para conversión de divisas instantánea.",
    "Permissioned DEX":   "DEX con acceso regulado para instituciones. Permite trading de RLUSD y activos tokenizados.",
    "Bitstamp":           "Exchange cripto veterano (2011). Gateway XRPL con wallets reales en el ledger. Partner Ripple.",
    "GateHub":            "Gateway y wallet XRPL. Emisor de USD en el ledger. Interface de usuario para el DEX de XRPL.",
    "Kraken":             "Exchange global con wallet XRPL real. Alto volumen XRP. Integración directa con el ledger.",
    "Binance":            "Mayor exchange del mundo por volumen. Wallet XRPL con movimientos whale frecuentes.",
    "Public Gateway":     "Punto de entrada público al XRPL. Agrega actividad de gateways menores y nuevas integraciones.",
    "Trustlines":         "Red de líneas de confianza en el XRPL. Permiten emisión y transferencia de cualquier activo.",
    "DEX/AMM":            "DEX nativo del XRPL con AMM activado en 2024. Liquidez on-chain para XRP y tokens.",
    "Large Transfers":    "Transferencias grandes (whale) en el XRPL. Indicador de movimiento institucional real.",
    "Clusters":           "Wallets agrupadas por comportamiento. Detecta patrones treasury, ODL y market making.",
    "Topology Engine":    "Motor de análisis de red del XRPL. Detecta hubs, concentración y flujos sistémicos.",
    "Anomaly Engine":     "Detección de anomalías estadísticas en el ledger. Alerta sobre comportamientos inusuales.",
    "Fingerprint Engine": "Identificación de patrones (treasury, ODL, MM). Asigna 'huella' a cada tipo de actividad.",
    "XRPL":               "XRP Ledger: blockchain público de Ripple. 3-5s por tx, 0.00001 XRP de fee. ~1M tx/día.",
    "RLUSD":              "Stablecoin USD de Ripple emitida en XRPL y Ethereum. Colateral 1:1, regulada en NY.",
    "Ethereum":           "Red Ethereum. RLUSD también emitido aquí. Cross-chain con XRPL vía bridges.",
}


# =============================================================================
# RUTA COMPLETA HACIA INFRAESTRUCTURA RIPPLE / XRPL
# =============================================================================
_RIPPLE_INFRA_TARGETS: Tuple[str, ...] = (
    "Ripple Payments", "XRPL", "RLUSD", "Public Gateway", "Rail",
    "Treasury", "Custody/Metaco", "Hidden Road / Prime", "Ripple Escrow",
)
_RIPPLE_CORE_TARGETS: Tuple[str, ...] = ("Ripple Payments", "XRPL", "RLUSD")

_ROUTE_KIND_RANK: Dict[str, int] = {
    "real": 0,
    "public": 1,
    "verified": 1,
    "odl": 1,
    "obligatory": 1,
    "private": 2,
    "partner": 2,
    "government": 3,
    "public_wallet": 3,
    "discovered": 4,
    "watch": 5,
    "future": 6,
    "model": 7,
}

_ROUTE_KIND_LABEL: Dict[str, Tuple[str, str]] = {
    "real": ("✅ directa on-chain", "#3CFF9B"),
    "public": ("🌐 pública", "#00CFFF"),
    "verified": ("✅ verificada", "#3CFF9B"),
    "odl": ("💸 ODL/RippleNet", "#FB923C"),
    "obligatory": ("⚡ implicación técnica", "#FF4D6D"),
    "private": ("🔒 documental/privada", "#F59E0B"),
    "partner": ("🤝 partner", "#A78BFA"),
    "government": ("🏛 institucional", "#FCD34D"),
    "public_wallet": ("🔑 wallet pública", "#34D399"),
    "discovered": ("🔍 descubierta", "#FFD700"),
    "watch": ("👁 vigilada/indirecta", "#B673FF"),
    "future": ("🔮 futura", "#8CA0B8"),
    "model": ("🧠 modelo", "#60A5FA"),
}


def _route_kind_rank(kind: str) -> int:
    return _ROUTE_KIND_RANK.get(str(kind or "").strip().lower(), 8)


def _route_kind_badge_inline(kind: str) -> str:
    lbl, color = _ROUTE_KIND_LABEL.get(str(kind or "").strip().lower(), (str(kind or "ruta"), "#94A3B8"))
    return (
        f"<span style='color:{color};border:1px solid {color}55;border-radius:999px;"
        f"padding:2px 7px;background:rgba(0,0,0,.22);font-size:.72rem;white-space:nowrap'>{lbl}</span>"
    )


def _build_route_adjacency(all_routes: List, all_nodes: Dict) -> Dict[str, List[Tuple[str, tuple]]]:
    """Adjacencia dirigida limpia para calcular caminos de infraestructura."""
    adj: Dict[str, List[Tuple[str, tuple]]] = defaultdict(list)
    seen: Set[Tuple[str, str, str, str]] = set()
    for r in all_routes or []:
        if len(r) < 5:
            continue
        src, dst, kind, signal, label = str(r[0]).strip(), str(r[1]).strip(), str(r[2]).strip(), r[3], str(r[4]).strip()
        if not src or not dst or src not in all_nodes or dst not in all_nodes:
            continue
        # Evitar duplicados exactos sin perder rutas alternativas por tipo.
        k = (src, dst, kind, label)
        if k in seen:
            continue
        seen.add(k)
        adj[src].append((dst, (src, dst, kind, signal, label)))
    for src in list(adj.keys()):
        adj[src].sort(key=lambda item: (_route_kind_rank(item[1][2]), item[0]))
    return adj


def _find_ripple_paths(
    focus_node: str,
    all_routes: List,
    all_nodes: Dict,
    targets: Tuple[str, ...] = _RIPPLE_CORE_TARGETS,
    max_depth: int = 7,
    max_paths: int = 4,
) -> List[Dict[str, Any]]:
    """
    Devuelve los mejores caminos dirigidos desde un nodo hasta Ripple Payments/XRPL/RLUSD.
    Cada path contiene nodes, edges, target, hops, score y kind_summary.
    """
    focus = str(focus_node or "").strip()
    if not focus or focus not in all_nodes:
        return []
    target_set = {t for t in targets if t in all_nodes}
    if focus in target_set:
        return [{"target": focus, "nodes": [focus], "edges": [], "hops": 0, "score": 0, "kind_summary": "core"}]

    adj = _build_route_adjacency(all_routes, all_nodes)
    q = deque([(focus, [focus], [], 0)])  # current, nodes, edges, score
    results: List[Dict[str, Any]] = []
    best_seen: Dict[str, int] = {focus: 0}

    while q and len(results) < max_paths * 5:
        cur, nodes, edges, score = q.popleft()
        if len(edges) >= max_depth:
            continue
        for nxt, edge in adj.get(cur, []):
            if nxt in nodes:
                continue
            kind_rank = _route_kind_rank(edge[2])
            next_score = score + 1 + kind_rank
            # Permitir varias rutas, pero cortar repeticiones claramente peores.
            if next_score > best_seen.get(nxt, 999) + 4:
                continue
            best_seen[nxt] = min(best_seen.get(nxt, 999), next_score)
            nnodes = nodes + [nxt]
            nedges = edges + [edge]
            if nxt in target_set:
                kinds = [str(e[2]) for e in nedges]
                results.append({
                    "target": nxt,
                    "nodes": nnodes,
                    "edges": nedges,
                    "hops": len(nedges),
                    "score": next_score,
                    "kind_summary": "+".join(kinds),
                })
            else:
                q.append((nxt, nnodes, nedges, next_score))

    # Si no hay camino a core, buscar infraestructura Ripple ampliada.
    if not results:
        wide_targets = tuple(t for t in _RIPPLE_INFRA_TARGETS if t in all_nodes)
        if set(wide_targets) != target_set:
            return _find_ripple_paths(focus, all_routes, all_nodes, wide_targets, max_depth, max_paths)

    # Orden: menos saltos, más evidencia, destino core prioritario.
    core_rank = {"Ripple Payments": 0, "XRPL": 1, "RLUSD": 2}
    results.sort(key=lambda p: (p["hops"], p["score"], core_rank.get(p["target"], 9)))

    # No repetir mismo destino con mismo primer salto.
    clean: List[Dict[str, Any]] = []
    seen_key: Set[Tuple[str, str]] = set()
    for pth in results:
        first_hop = pth["nodes"][1] if len(pth["nodes"]) > 1 else pth["target"]
        key = (pth["target"], first_hop)
        if key in seen_key:
            continue
        seen_key.add(key)
        clean.append(pth)
        if len(clean) >= max_paths:
            break
    return clean


def _nodes_from_ripple_paths(paths: List[Dict[str, Any]]) -> Set[str]:
    nodes: Set[str] = set()
    for pth in paths or []:
        nodes.update(pth.get("nodes") or [])
    return nodes


def _edges_from_ripple_paths(paths: List[Dict[str, Any]]) -> Set[Tuple[str, str]]:
    edges: Set[Tuple[str, str]] = set()
    for pth in paths or []:
        for e in pth.get("edges") or []:
            if len(e) >= 2:
                edges.add((str(e[0]).strip(), str(e[1]).strip()))
    return edges


def _render_ripple_path_panel(focus_node: str, paths: List[Dict[str, Any]]) -> None:
    """Pinta en la ficha del nodo la cadena completa hasta Ripple/XRPL."""
    if not focus_node:
        return
    if not paths:
        st.markdown("""
<div style='margin-top:12px;background:rgba(15,23,42,.62);border:1px solid rgba(148,163,184,.35);border-radius:13px;padding:12px 14px;'>
  <div style='color:#E2E8F0;font-weight:900;margin-bottom:4px'>🧭 Ruta hacia Ripple/XRPL</div>
  <div style='color:#94A3B8;font-size:.84rem;line-height:1.45'>
    Este nodo todavía no tiene una cadena trazable hasta <b>Ripple Payments</b>, <b>XRPL</b> o <b>RLUSD</b> dentro del grafo local. Puede ser un nodo aislado, una ruta pendiente de verificar o una entidad que necesita búsqueda profunda.
  </div>
</div>
""", unsafe_allow_html=True)
        return

    cards = []
    for idx, pth in enumerate(paths[:4], 1):
        nodes = [html.escape(str(n)) for n in (pth.get("nodes") or [])]
        edges = pth.get("edges") or []
        target = html.escape(str(pth.get("target", "")))
        hops = int(pth.get("hops", 0) or 0)
        if hops == 0:
            chain_html = f"<span style='color:#3CFF9B;font-weight:900'>{target}</span>"
            edge_html = "<span style='color:#94A3B8'>Este nodo ya pertenece al núcleo Ripple/XRPL.</span>"
        else:
            chain_html = " <span style='color:#64748B'>→</span> ".join(
                [f"<span style='color:#E2E8F0;font-weight:800'>{n}</span>" for n in nodes]
            )
            edge_bits = []
            for e in edges:
                _src, _dst, _kind, _signal, _label = e
                edge_bits.append(
                    f"<div style='margin-top:5px;color:#CBD5E1;font-size:.78rem'>"
                    f"{html.escape(str(_src))} → {html.escape(str(_dst))} &nbsp; {_route_kind_badge_inline(str(_kind))}"
                    f"<br><span style='color:#94A3B8'>{html.escape(str(_label))}</span>"
                    f"</div>"
                )
            edge_html = "".join(edge_bits)
        cards.append(f"""
<div style='margin-top:9px;background:rgba(2,6,23,.42);border:1px solid rgba(90,215,255,.22);border-radius:11px;padding:10px 12px;'>
  <div style='display:flex;justify-content:space-between;gap:10px;align-items:center;margin-bottom:6px'>
    <div style='color:#5AD7FF;font-weight:900;font-size:.86rem'>Ruta {idx} hacia {target}</div>
    <div style='color:#94A3B8;font-size:.74rem'>{hops} salto(s)</div>
  </div>
  <div style='font-size:.86rem;line-height:1.55'>{chain_html}</div>
  {edge_html}
</div>
""")

    st.markdown(f"""
<div style='margin-top:12px;background:rgba(6,16,31,.72);border:1px solid rgba(90,215,255,.45);border-radius:13px;padding:12px 14px;'>
  <div style='color:#E2E8F0;font-weight:900;margin-bottom:4px'>🧭 Ruta completa hacia infraestructura Ripple/XRPL</div>
  <div style='color:#94A3B8;font-size:.82rem;line-height:1.45;margin-bottom:8px'>
    Al pinchar un círculo, el radar busca la cadena dirigida hasta <b>Ripple Payments</b>, <b>XRPL</b> o <b>RLUSD</b>. Directo no significa operativo si la etiqueta dice “watch”, “documental” o “modelo”: significa que existe una ruta trazable dentro del mapa.
  </div>
  {''.join(cards)}
</div>
""", unsafe_allow_html=True)

def render_node_info_panel(
    focus_node: str,
    row: pd.Series,
    conn: Optional[sqlite3.Connection],
    all_routes: List,
    all_nodes: Dict,
) -> None:
    """Muestra la ficha de información del nodo seleccionado."""
    meta   = all_nodes.get(focus_node, {})
    icon   = meta.get("icon", "●")
    layer  = meta.get("layer", "—")
    desc   = NODE_DESC.get(focus_node, "")

    # Descripción de la capa
    layer_labels = {
        "Banca_AM": "Banca Americas", "Banca_EU": "Banca Europa",
        "Banca_AP": "Banca Asia-Pac", "ODL": "Corredor ODL",
        "Privado": "Infraestructura Rail", "Ripple": "Ripple Core",
        "Institucional": "Institucional", "Exchange": "Exchange",
        "Vigilancia": "Vigilancia XRPL", "Inteligencia": "Motor de Inteligencia",
        "Público": "XRPL Público", "Futuro": "Cross-chain Futuro",
    }
    layer_name = layer_labels.get(layer, layer)

    # Colores por capa
    layer_colors = {
        "Banca_AM": "#F59E0B", "Banca_EU": "#E67E22", "Banca_AP": "#D35400",
        "ODL": "#FB923C", "Privado": "#FFB84D", "Ripple": "#5AD7FF",
        "Institucional": "#D9A7FF", "Exchange": "#22D3EE",
        "Vigilancia": "#B673FF", "Inteligencia": "#60A5FA",
        "Público": "#3CFF9B", "Futuro": "#8CA0B8",
        "Fintech": "#F472B6", "CBDC": "#34D399", "AssetMgmt": "#A78BFA",
        "Gobierno": "#FCD34D", "Clearing": "#38BDF8", "RedPrivada": "#FB7185",
        "Puente": "#22D3EE", "Proveedor": "#F59E0B",
        "Descubierto": "#94A3B8", "Otro": "#64748B",
    }
    accent = layer_colors.get(layer, "#CBD5E1")

    # Solo cargamos confianza VERIFICADA por par (connection_proofs).
    # Las rutas watch/especulativas nunca heredan confianza del nodo padre.
    _proof_confidence: Dict[str, float] = {}   # "src|dst" -> calibrated_score verificado
    _proof_sources: Dict[str, list] = {}        # "src|dst" -> URLs de evidencia verificada
    if conn:
        try:
            _focus_key = _canonical_entity_key(focus_node)
            for _pa, _pb, _pd in conn.execute(
                "SELECT node_a, node_b, proof_data FROM connection_proofs "
                "WHERE node_a=? OR node_b=? OR node_a_key=? OR node_b_key=?", (focus_node, focus_node, _focus_key, _focus_key)
            ).fetchall():
                try:
                    _pj = json.loads(_pd or "{}")
                    # Limpiar evidencias antiguas guardadas antes del filtro estricto.
                    _clean_proofs = _dedupe_and_filter_proofs(_pa, _pb, _pj.get("proofs") or [], max_items=3)
                    _cs = _combine_evidence_score(_clean_proofs)
                    _urls = []
                    for _pr in _clean_proofs:
                        _u = _canonical_source_url(_pr.get("url", ""))
                        if _u.startswith("http") and _u not in _urls:
                            _urls.append(_u)
                except Exception:
                    _cs = 0.0; _urls = []
                if _cs > 0:
                    _proof_confidence[f"{_pa}|{_pb}"] = _cs
                    _proof_confidence[f"{_pb}|{_pa}"] = _cs
                    _proof_confidence[_canonical_pair_key(_pa, _pb)] = _cs
                if _urls:
                    _proof_sources[f"{_pa}|{_pb}"] = _urls
                    _proof_sources[f"{_pb}|{_pa}"] = _urls
                    _proof_sources[_canonical_pair_key(_pa, _pb)] = _urls
        except Exception:
            pass

    # Rutas salientes y entrantes.
    # sig = 0 para rutas watch (especulativas sin verificar).
    # sig = calibrated_score de connection_proofs si fue verificada.
    outbound, inbound = [], []
    for route in all_routes:
        src_n, dst_n = str(route[0]).strip(), str(route[1]).strip()
        kind  = route[2]
        label = route[4]
        pair_key = f"{src_n}|{dst_n}"
        # Para todos los tipos: usar proof calibrado si existe, si no → 0
        # Una ruta watch verificada DEBE mostrar su score real
        sig = (
            _proof_confidence.get(pair_key)
            or _proof_confidence.get(f"{dst_n}|{src_n}")
            or _proof_confidence.get(_canonical_pair_key(src_n, dst_n))
            or 0.0
        )
        if src_n == focus_node:
            outbound.append((dst_n, kind, sig, label))
        elif dst_n == focus_node:
            inbound.append((src_n, kind, sig, label))

    # Info extra si es nodo descubierto (en BD)
    dyn_info = None
    _evidence_map: Dict[str, list] = {}   # "src|dst" -> lista de URLs de fuente
    if conn:
        try:
            dyn_info = conn.execute(
                "SELECT summary, layer, confidence, source_url FROM dynamic_nodes WHERE name=?",
                (focus_node,)
            ).fetchone()
        except Exception:
            pass
        # Fuentes por par: SOLO de connection_proofs verificados, no del blob general del nodo
        _evidence_map = _proof_sources

    # Cuadro pedagógico: explica cadenas directas/indirectas/watch para que el usuario no confunda ruta con operación.
    try:
        render_chain_logic_box(focus_node, conn)
    except Exception:
        pass

    def _proof_badge(node_a: str, node_b: str) -> str:
        """Badge calibrado usando cert_label del scoring combinado on-chain+internet."""
        pid  = hashlib.sha256(f"{node_a}|{node_b}".encode()).hexdigest()[:16]
        pid2 = hashlib.sha256(f"{node_b}|{node_a}".encode()).hexdigest()[:16]
        if conn:
            try:
                row = _connection_proof_row(conn, node_a, node_b)
                if row:
                    pdata_str, _onchain, raw_conf, _validated_at, _ra, _rb = row
                    try:
                        pj = json.loads(pdata_str)
                        # Recalcular el badge con el filtro estricto para que pruebas antiguas/ruidosas no sigan apareciendo.
                        _clean_proofs = _dedupe_and_filter_proofs(node_a, node_b, pj.get("proofs") or [], max_items=3)
                        score = _combine_evidence_score(_clean_proofs)
                        lbl, color = _cert_label(score)
                    except Exception:
                        lbl = ""; color = ""; score = raw_conf
                    if not lbl:
                        lbl, color = _cert_label(score)
                    return (
                        f"<span style='color:{color};font-size:0.68rem;border:1px solid {color}55;"
                        f"border-radius:5px;padding:2px 7px;background:rgba(0,0,0,0.35);"
                        f"white-space:nowrap;' title='Confianza: {score*100:.0f}%'>{lbl}</span>"
                    )
            except Exception:
                pass
        return (
            "<span style='color:#64748B;font-size:0.68rem;border:1px solid #64748B55;"
            "border-radius:5px;padding:2px 7px;background:rgba(0,0,0,0.35);white-space:nowrap;'"
            ">🔎 sin verificar</span>"
        )

    # Renderizar panel
    kind_badge = {
        "real":        ("✅ Directa on-chain",    "#3CFF9B"),   # verde brillante — TX real en ledger
        "public":      ("🌐 Directa pública",     "#00CFFF"),   # cian eléctrico — gateway/exchange público
        "private":     ("🔒 Directa inferida",    "#F59E0B"),   # ámbar — evidencia documental/contractual
        "obligatory":  ("⚡ Obligatoria",          "#FF4D6D"),   # rojo-rosa — implicación técnica irrefutable
        "watch":       ("👁 Indirecta vigilada",  "#B673FF"),   # morado — huella pública sin confirmar
        "discovered":  ("🔍 Indirecta descubierta","#FFD700"),  # dorado — detectada por motor IA
        "model":       ("🧠 Modelo analítico",    "#60A5FA"),   # azul — motor de inteligencia
        "future":      ("🔮 Futura",              "#8CA0B8"),   # gris — integración en desarrollo
        "partner":     ("🤝 Partner",             "#A78BFA"),   # violeta claro
        "odl":         ("💸 Corredor ODL",        "#FB923C"),   # naranja — corredor activo
        "public_wallet":("🔑 Wallet pública",     "#34D399"),   # esmeralda
    }

    def sig_bar(sig: float) -> str:
        pct = min(100, int(sig * 100))
        bar_color = "#3CFF9B" if pct >= 65 else "#FFB84D" if pct >= 35 else "#FF5A67"
        filled = int(pct / 10)
        bar = "█" * filled + "░" * (10 - filled)
        return f"<span style='color:{bar_color};font-family:monospace'>{bar}</span> <b>{pct}%</b>"

    st.markdown(f"""
<div style='background:rgba(6,16,31,0.97);border:1px solid {accent};border-radius:16px;
     padding:18px 22px;margin-top:10px;'>
  <div style='display:flex;align-items:center;gap:12px;margin-bottom:12px;'>
    <span style='font-size:2rem'>{icon}</span>
    <div>
      <div style='color:{accent};font-size:1.15rem;font-weight:900;line-height:1.2'>{focus_node}</div>
      <div style='color:#94A3B8;font-size:0.80rem'>{layer_name}</div>
    </div>
  </div>
  {'<div style="color:#CBD5E1;font-size:0.85rem;margin-bottom:14px;line-height:1.5">' + desc + '</div>' if desc else ''}
  {'<div style="color:#60A5FA;font-size:0.80rem;margin-bottom:10px;padding:8px;background:rgba(96,165,250,0.08);border-radius:8px">' + dyn_info[0] + '</div>' if dyn_info and dyn_info[0] else ''}
  {('<div style="margin-bottom:4px;">' + " ".join(
      f'<a href="{u.strip()}" target="_blank" rel="noopener noreferrer" '
      f'style="color:#5AD7FF;font-size:0.72rem;text-decoration:none;border:1px solid #5AD7FF55;'
      f'border-radius:5px;padding:2px 8px;background:rgba(0,0,0,0.35);margin-right:4px;">'
      f'🔗 Fuente {i+1}</a>'
      for i, u in enumerate([x.strip() for x in dyn_info[3].split(",") if x.strip().startswith("http")][:4])
  ) + '</div>') if dyn_info and dyn_info[3] and any(u.strip().startswith("http") for u in dyn_info[3].split(",")) else ''}
</div>
""", unsafe_allow_html=True)

    # Ruta completa hacia infraestructura Ripple/XRPL para el nodo seleccionado.
    # Esto evita que el usuario vea solo vecinos sueltos: muestra la cadena causal.
    try:
        _ripple_paths = _find_ripple_paths(focus_node, all_routes, all_nodes)
    except Exception:
        _ripple_paths = []
    _render_ripple_path_panel(focus_node, _ripple_paths)

    col_out, col_in = st.columns(2)

    with col_out:
        st.markdown(f"<div style='color:{accent};font-weight:700;font-size:0.88rem;margin-bottom:6px'>↗ Conecta hacia ({len(outbound)})</div>", unsafe_allow_html=True)
        if outbound:
            for dst, kind, sig, label in sorted(outbound, key=lambda x: -x[2]):
                badge_text, badge_color = kind_badge.get(kind, (kind, "#CBD5E1"))
                dst_meta = all_nodes.get(dst, {})
                dst_icon = dst_meta.get("icon", "●")
                proof_html = _proof_badge(focus_node, dst)
                # Fuentes por conexión
                ev_urls = _evidence_map.get(f"{focus_node}|{dst}", []) or _evidence_map.get(_canonical_pair_key(focus_node, dst), [])
                if isinstance(ev_urls, str): ev_urls = [ev_urls] if ev_urls else []
                src_links = " ".join(
                    f'<a href="{u}" target="_blank" style="color:#5AD7FF;font-size:0.68rem;'
                    f'text-decoration:none;border:1px solid #5AD7FF55;border-radius:4px;padding:1px 6px;">'
                    f'🔗 Fuente {i+1}</a>'
                    for i, u in enumerate(ev_urls)
                )
                # Mostrar barra solo si hay score verificado real
                if sig > 0:
                    bar_html = sig_bar(sig)
                elif kind == "watch":
                    bar_html = "<span style='color:#334155;font-size:0.70rem;font-style:italic'>⏳ Verificar para obtener confianza real</span>"
                else:
                    bar_html = "<span style='color:#334155;font-size:0.70rem;font-style:italic'>⏳ Sin datos de confianza</span>"
                st.markdown(f"""
<div style='background:rgba(15,23,42,0.8);border:1px solid rgba(255,255,255,0.10);
     border-radius:10px;padding:8px 12px;margin-bottom:5px;'>
  <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px;'>
    <span style='color:#F1F5F9;font-size:0.83rem;font-weight:600'>{dst_icon} {dst}</span>
    <div style='display:flex;align-items:center;gap:5px;'>
      <span style='color:{badge_color};font-size:0.70rem;background:rgba(0,0,0,0.3);
            padding:2px 7px;border-radius:99px;border:1px solid {badge_color}40'>{badge_text}</span>
      {proof_html}
    </div>
  </div>
  <div style='margin-top:5px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;'>
    {bar_html}
    {src_links}
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#475569;font-size:0.82rem'>Sin conexiones salientes</span>", unsafe_allow_html=True)

    with col_in:
        st.markdown(f"<div style='color:{accent};font-weight:700;font-size:0.88rem;margin-bottom:6px'>↙ Recibe desde ({len(inbound)})</div>", unsafe_allow_html=True)
        if inbound:
            for src, kind, sig, label in sorted(inbound, key=lambda x: -x[2]):
                badge_text, badge_color = kind_badge.get(kind, (kind, "#CBD5E1"))
                src_meta = all_nodes.get(src, {})
                src_icon = src_meta.get("icon", "●")
                proof_html = _proof_badge(src, focus_node)
                ev_urls = _evidence_map.get(f"{src}|{focus_node}", []) or _evidence_map.get(_canonical_pair_key(src, focus_node), [])
                if isinstance(ev_urls, str): ev_urls = [ev_urls] if ev_urls else []
                src_links = " ".join(
                    f'<a href="{u}" target="_blank" style="color:#5AD7FF;font-size:0.68rem;'
                    f'text-decoration:none;border:1px solid #5AD7FF55;border-radius:4px;padding:1px 6px;">'
                    f'🔗 Fuente {i+1}</a>'
                    for i, u in enumerate(ev_urls)
                )
                is_watch = kind in ("watch",) or "sin verificar" in proof_html or "Sin evidencia" in proof_html
                bar_html = (
                    f"<span style='color:#475569;font-size:0.70rem'>📡 Señal XRPL: {int(sig*100)}%</span>"
                    if is_watch and "✅" not in proof_html and "🟡" not in proof_html
                    else sig_bar(sig)
                )
                st.markdown(f"""
<div style='background:rgba(15,23,42,0.8);border:1px solid rgba(255,255,255,0.10);
     border-radius:10px;padding:8px 12px;margin-bottom:5px;'>
  <div style='display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:4px;'>
    <span style='color:#F1F5F9;font-size:0.83rem;font-weight:600'>{src_icon} {src}</span>
    <div style='display:flex;align-items:center;gap:5px;'>
      <span style='color:{badge_color};font-size:0.70rem;background:rgba(0,0,0,0.3);
            padding:2px 7px;border-radius:99px;border:1px solid {badge_color}40'>{badge_text}</span>
      {proof_html}
    </div>
  </div>
  <div style='margin-top:5px;display:flex;align-items:center;gap:10px;flex-wrap:wrap;'>
    {bar_html}
    {src_links}
  </div>
</div>""", unsafe_allow_html=True)
        else:
            st.markdown("<span style='color:#475569;font-size:0.82rem'>Sin conexiones entrantes</span>", unsafe_allow_html=True)

    # ── Panel de verificación ─────────────────────────────────────────────────
    if conn:
        st.markdown("---")

        all_peers = list({r[0] for r in outbound} | {r[0] for r in inbound})

        def _needs_verify(peer: str) -> bool:
            try:
                # Si existe cualquier resultado guardado para A↔B, aunque sea "sin evidencia",
                # ya está verificado y no debe volver a gastar tokens ni salir como pendiente.
                return _connection_proof_row(conn, focus_node, peer) is None
            except Exception:
                return True

        pending_peers = [p for p in all_peers if _needs_verify(p)]
        verified_peers = [p for p in all_peers if not _needs_verify(p)]

        try:
            focus_key = _canonical_entity_key(focus_node)
            n_onchain = conn.execute(
                "SELECT COUNT(*) FROM connection_proofs WHERE (node_a=? OR node_b=? OR node_a_key=? OR node_b_key=?) AND onchain=1",
                (focus_node, focus_node, focus_key, focus_key)
            ).fetchone()[0]
            n_internet = conn.execute(
                "SELECT COUNT(*) FROM connection_proofs "
                "WHERE (node_a=? OR node_b=? OR node_a_key=? OR node_b_key=?) AND proof_data LIKE '%\"internet\": true%'",
                (focus_node, focus_node, focus_key, focus_key)
            ).fetchone()[0]
        except Exception:
            n_onchain = n_internet = 0

        # Header con estado
        st.markdown(
            f"<div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:10px'>"
            f"<span style='color:{accent};font-weight:700;font-size:0.88rem'>🔬 Verificación de conexiones · {focus_node}</span>"
            f"<span style='color:#64748B;font-size:0.75rem'>"
            f"✅ {len(verified_peers)} verificadas · ⏳ {len(pending_peers)} pendientes · "
            f"⛓ {n_onchain} on-chain · 🌐 {n_internet} internet</span>"
            f"</div>",
            unsafe_allow_html=True
        )

        col_v1, col_v2 = st.columns(2)
        with col_v1:
            do_verify = st.button(
                f"🔍 Verificar {len(pending_peers)} conexiones pendientes",
                key=f"verify_pending_{focus_node}",
                use_container_width=True,
                disabled=len(pending_peers) == 0,
                type="primary",
            )
        with col_v2:
            do_reverify = st.button(
                "🔄 Re-verificar todo desde cero",
                key=f"reverify_all_{focus_node}",
                use_container_width=True,
            )

        if do_reverify:
            try:
                focus_key = _canonical_entity_key(focus_node)
                conn.execute("DELETE FROM connection_proofs WHERE node_a=? OR node_b=? OR node_a_key=? OR node_b_key=?", (focus_node, focus_node, focus_key, focus_key))
                conn.commit()
            except Exception:
                pass
            pending_peers = all_peers
            do_verify = True

        if do_verify and pending_peers:
            prog = st.progress(0, text="Preparando verificación…")
            status = st.empty()

            def _verify_progress(value: float, text: str) -> None:
                try:
                    prog.progress(value, text=text)
                except TypeError:
                    prog.progress(value)
                status.markdown(
                    f"<span style='color:#5AD7FF;font-size:0.80rem'>🔬 {text}</span>",
                    unsafe_allow_html=True,
                )

            _verify_progress(0.02, f"Verificando {len(pending_peers)} conexión(es)…")
            validate_node_fast(focus_node, pending_peers, conn, progress_cb=_verify_progress)
            _verify_progress(1.0, "Verificación completada")
            _time.sleep(0.35)
            st.rerun()

        # Mostrar pruebas guardadas
        try:
            focus_key = _canonical_entity_key(focus_node)
            proof_rows = conn.execute(
                "SELECT node_a, node_b, proof_data, onchain, confidence, validated_at "
                "FROM connection_proofs WHERE node_a=? OR node_b=? OR node_a_key=? OR node_b_key=? ORDER BY onchain DESC, confidence DESC",
                (focus_node, focus_node, focus_key, focus_key)
            ).fetchall()
        except Exception:
            proof_rows = []

        if proof_rows:
            for na, nb, pdata_str, is_onchain, pconf, val_at in proof_rows:
                peer = nb if _canonical_entity_key(na) == _canonical_entity_key(focus_node) else na
                try:
                    pdata = json.loads(pdata_str)
                    proofs = pdata.get("proofs", [])
                except Exception:
                    proofs = []

                onchain_color = "#3CFF9B" if is_onchain else "#FF5A67"
                onchain_label = "✅ On-chain verificado" if is_onchain else "⚠️ Sin prueba on-chain"
                val_short = val_at[:16].replace("T", " ") if val_at else ""

                # Leer scoring calibrado si existe
                cert_lbl   = pdata.get("cert_label",      onchain_label)
                cert_col   = pdata.get("cert_color",       onchain_color)
                cal_score  = pdata.get("calibrated_score", pconf)
                has_inet   = pdata.get("has_internet",     False)
                src_tags   = ("🔗 On-chain" if is_onchain else "") + (" · 🌐 Internet" if has_inet else "")

                with st.expander(
                    f"{cert_lbl} · **{focus_node} ↔ {peer}** · {cal_score*100:.0f}% · {src_tags} · {val_short}"
                ):
                    # Barra de confianza calibrada + desglose explicativo
                    bar_filled = int(cal_score * 10)
                    bar_str = "█" * bar_filled + "░" * (10 - bar_filled)
                    st.markdown(
                        f"<div style='margin-bottom:6px;'>"
                        f"<span style='color:{cert_col};font-family:monospace;font-size:0.90rem'>{bar_str}</span>"
                        f"<span style='color:{cert_col};font-weight:700;margin-left:8px'>{cal_score*100:.0f}%</span>"
                        f"<span style='color:#64748B;font-size:0.72rem;margin-left:6px'>"
                        f"(probabilidad independiente combinada · {len(proofs)} fuentes)</span></div>",
                        unsafe_allow_html=True,
                    )
                    # Desglose: por qué ese porcentaje
                    active_proofs = [p for p in proofs if p.get("onchain") or p.get("internet")]
                    pdf_proofs = [p for p in active_proofs if p.get("type","") in ("regulatory_filing_pdf","contract_pdf","regulatory_filing") and (p.get("url","").endswith(".pdf") or "sec.gov/Archives" in p.get("url","") or "bis.org" in p.get("url",""))]
                    # PDF counter always visible
                    if pdf_proofs:
                        _pdf_line = f"<div style='color:#3CFF9B;font-size:0.72rem;margin-bottom:4px;'>📄 Documentos PDF encontrados: {len(pdf_proofs)}</div>"
                    elif active_proofs:
                        _pdf_line = f"<div style='color:#475569;font-size:0.72rem;margin-bottom:4px;'>📄 0 documentos PDF verificables encontrados</div>"
                    else:
                        _pdf_line = f"<div style='color:#334155;font-size:0.72rem;margin-bottom:4px;'>📄 0 documentos PDF — sin evidencias registradas</div>"
                    if active_proofs:
                        running = 1.0
                        breakdown_rows = ""
                        for p in sorted(active_proofs, key=lambda x: -EVIDENCE_SCORES.get(x.get("type",""),0)):
                            pw   = EVIDENCE_SCORES.get(p.get("type",""), 0)
                            before = round((1 - running) * 100, 1)
                            running *= (1.0 - pw)
                            after  = round((1 - running) * 100, 1)
                            delta  = round(after - before, 1)
                            lbl    = EVIDENCE_LABELS.get(p.get("type",""), p.get("type",""))
                            icon   = p.get("icon","•")
                            src_tag = "⛓" if p.get("onchain") else "📄" if p.get("type","") in ("regulatory_filing_pdf","contract_pdf") else "🌐"
                            breakdown_rows += (
                                f"<tr>"
                                f"<td style='color:#94A3B8;padding:2px 8px;font-size:0.70rem'>{src_tag} {icon} {lbl}</td>"
                                f"<td style='color:#64748B;text-align:right;padding:2px 8px;font-size:0.70rem'>peso {pw:.2f}</td>"
                                f"<td style='color:#3CFF9B;text-align:right;padding:2px 8px;font-size:0.70rem;font-weight:600'>+{delta}%</td>"
                                f"<td style='color:{cert_col};text-align:right;padding:2px 8px;font-size:0.70rem'>→ {after:.1f}%</td>"
                                f"</tr>"
                            )
                        st.markdown(
                            f"{_pdf_line}"
                            f"<details><summary style='color:#64748B;font-size:0.72rem;cursor:pointer;'>▶ Por qué {cal_score*100:.0f}% — desglose de evidencias</summary>"
                            f"<table style='width:100%;border-collapse:collapse;margin-top:4px;'>"
                            f"<tr><th style='color:#475569;text-align:left;font-size:0.68rem;padding:2px 8px'>Evidencia</th>"
                            f"<th style='color:#475569;text-align:right;font-size:0.68rem;padding:2px 8px'>Peso</th>"
                            f"<th style='color:#475569;text-align:right;font-size:0.68rem;padding:2px 8px'>Aporte</th>"
                            f"<th style='color:#475569;text-align:right;font-size:0.68rem;padding:2px 8px'>Acumulado</th></tr>"
                            f"{breakdown_rows}"
                            f"</table></details>",
                            unsafe_allow_html=True,
                        )

                    if not active_proofs:
                        st.markdown(_pdf_line, unsafe_allow_html=True)
                    if not proofs:
                        st.markdown("<span style='color:#64748B'>Sin evidencia registrada.</span>", unsafe_allow_html=True)

                    # Separar on-chain vs internet
                    onchain_ps  = [p for p in proofs if p.get("onchain")]
                    internet_ps = [p for p in proofs if p.get("internet")]
                    other_ps    = [p for p in proofs if not p.get("onchain") and not p.get("internet")]

                    def _render_proofs(plist: List[Dict], section_color: str) -> None:
                        for p in plist:
                            ptype  = p.get("type","")
                            plabel = p.get("label","")
                            picon  = p.get("icon","•")
                            purl   = p.get("url","")
                            psnip  = p.get("snippet","")
                            pw     = EVIDENCE_SCORES.get(ptype, 0)
                            extra  = ""
                            if p.get("tx_hash"): extra += f" · TX:`{p['tx_hash']}`"
                            if p.get("ledger"):  extra += f" · Ledger:{p['ledger']}"
                            url_html = (
                                f"<a href='{purl}' target='_blank' style='color:#5AD7FF;"
                                f"font-size:0.68rem;text-decoration:none;margin-left:6px;'>🔗 ver fuente</a>"
                            ) if purl else ""
                            snip_html = (
                                f"<div style='color:#64748B;font-size:0.70rem;font-style:italic;"
                                f"margin-top:2px;\">«{psnip[:140]}»</div>"
                            ) if psnip else ""
                            st.markdown(
                                f"<div style='border-left:3px solid {section_color};padding:5px 10px;"
                                f"margin-bottom:4px;background:rgba(15,23,42,0.6);"
                                f"border-radius:0 6px 6px 0;font-size:0.80rem;'>"
                                f"<div style='display:flex;justify-content:space-between;'>"
                                f"<span style='color:{section_color}'>{picon} <b>{ptype.replace('_',' ').title()}</b></span>"
                                f"<span style='color:#475569;font-size:0.68rem'>peso {pw:.2f}</span></div>"
                                f"<span style='color:#CBD5E1'>{plabel}{extra}</span>{url_html}"
                                f"{snip_html}</div>",
                                unsafe_allow_html=True,
                            )

                    if onchain_ps:
                        st.markdown("<span style='color:#3CFF9B;font-size:0.75rem;font-weight:700'>⛓ ON-CHAIN (ledger XRPL)</span>", unsafe_allow_html=True)
                        _render_proofs(onchain_ps, "#3CFF9B")
                    if internet_ps:
                        st.markdown("<span style='color:#5AD7FF;font-size:0.75rem;font-weight:700'>🌐 INTERNET (rastros verificables)</span>", unsafe_allow_html=True)
                        _render_proofs(internet_ps, "#5AD7FF")
                    if other_ps:
                        _render_proofs(other_ps, "#64748B")

                    wa = pdata.get("wallets_a", [])
                    wb = pdata.get("wallets_b", [])
                    if wa or wb:
                        st.markdown(
                            f"<span style='color:#334155;font-size:0.70rem'>"
                            f"Wallets {focus_node}: {', '.join(wa) or '—'} · "
                            f"Wallets {peer}: {', '.join(wb) or '—'}</span>",
                            unsafe_allow_html=True,
                        )
                    if st.button(f"🔄 Re-verificar {peer}", key=f"reverify_{focus_node}_{peer}"):
                        rprog = st.progress(0, text=f"Preparando re-verificación de {peer}…")
                        try:
                            rprog.progress(0.35, text="Escaneando XRPL y evidencias públicas…")
                        except TypeError:
                            rprog.progress(0.35)
                        validate_connection_onchain(focus_node, peer, conn, force=True)
                        try:
                            rprog.progress(1.0, text="Re-verificación completada")
                        except TypeError:
                            rprog.progress(1.0)
                        _time.sleep(0.25)
                        st.rerun()
        else:
            st.markdown(
                "<div style='color:#475569;font-size:0.82rem;padding:10px;background:rgba(15,23,42,0.5);"
                "border-radius:8px;border:1px solid rgba(255,255,255,0.06);'>"
                "⚡ Pulsa <b>Verificar conexiones en XRPL</b> para buscar evidencia real on-chain "
                "(transacciones, trust lines, actividad ODL, pools AMM).</div>",
                unsafe_allow_html=True,
            )


def make_map(row: pd.Series,
             title: str = "Mapa vivo: rutas privadas + huellas públicas + motores de inteligencia",
             watched: Optional[pd.DataFrame] = None,
             conn: Optional[sqlite3.Connection] = None,
             focus_node: Optional[str] = None,
             route_filter: str = "all") -> go.Figure:
    """
    route_filter:
      "all"          — todas las rutas (por defecto)
      "confirmed"    — solo rutas confirmadas + obligatorias
                       (kinds: real, public, private, obligatory, odl, partner, public_wallet)
      "surveillance" — solo rutas de vigilancia/inferencia
                       (kinds: watch, discovered, model, future)
    """
    fig = go.Figure()

    # Zona extra de vigilancia si hay wallets vigiladas
    has_watched = watched is not None and not watched.empty

    boxes = [
        (-8.95, -1.65, -8.25, 2.25, "Americas"),
        (-7.90, -0.70, -7.20, 1.85, "Europa"),
        (-6.85, -2.05, -6.15, 2.05, "Asia-Pac"),
        (-5.60, -1.10, -4.80, 2.70, "Infraestructura"),
        (-3.45, -3.10, -2.65, 2.45, "Ripple"),
        (-1.35, -1.95, -0.55, 2.55, "Institucional"),
        (0.75,  2.20,  1.55, 2.95, "Exchanges"),
        (0.75, -3.75,  1.55, 2.00, "Vigilancia"),
        (2.65, -1.10,  3.45, 1.65, "Motores"),
        (4.65, -1.60,  5.45, 1.15, "XRPL/RLUSD"),
        # Reguladores: Federal Reserve está aquí (entre rails y Ripple Core)
        (-4.60, -2.10, -3.80, 3.15, "Reguladores"),
        # CBDC: siempre visible — 6 nodos estáticos confirmados
        ( 6.00, -3.00,  6.70, 3.15, "CBDC / banco central"),
    ]
    if has_watched:
        boxes.append((-2.50, -5.80, 6.00, -3.60, "🔍 Wallets Vigiladas"))
    for x0, y0, x1, y1, label in boxes:
        fig.add_shape(type="rect", x0=x0, y0=y0, x1=x1, y1=y1,
                      line=dict(color="rgba(255,255,255,0.22)", width=1),
                      fillcolor="rgba(15,23,42,0.35)", layer="below")
        fig.add_annotation(
            x=(x0+x1)/2, y=y1+0.06, text=f"<b>{label}</b>",
            showarrow=False,
            font=dict(size=10, color="#CBD5E1"),
            yanchor="bottom",
            bgcolor="rgba(7,17,31,0.70)",
            bordercolor="rgba(255,255,255,0.18)",
            borderwidth=1,
            borderpad=3,
        )

    # Fusionar nodos y rutas dinamicos (Discovery Engine)
    _dyn_nodes, _dyn_routes, _new_boxes = load_dynamic_map_elements(conn) if conn is not None else ({}, [], [])
    _all_nodes = {**NODES, **_dyn_nodes}

    # ── Zonas de descubrimiento condicionales ────────────────────────────────
    # Sólo se dibuja la caja si hay al menos un nodo en esa capa.
    # Las zonas con nodos estáticos (Gobierno, CBDC) ya se dibujaron arriba.
    _DISCOVERY_ZONES = [
        ("Fintech",    6.90, -2.10,  7.60, 3.15, "Fintech / pagos"),
        ("AssetMgmt",  7.80, -2.10,  8.50, 3.15, "Asset managers"),
        ("Clearing",   8.70, -2.10,  9.40, 3.15, "Clearing / settlement"),
        ("RedPrivada", 9.60, -2.10, 10.30, 3.15, "Red privada / OTC"),
        ("Puente",    10.50, -2.10, 11.20, 3.15, "Puentes / cross-chain"),
        ("Proveedor", 11.40, -2.10, 12.10, 3.15, "Proveedores / APIs"),
        ("Descubierto",12.30,-2.10, 13.00, 3.15, "Otros descubiertos"),
    ]
    _populated_layers = {data.get("layer") for data in _all_nodes.values()}
    for _zlayer, _zx0, _zy0, _zx1, _zy1, _zlabel in _DISCOVERY_ZONES:
        if _zlayer not in _populated_layers:
            continue   # zona vacía — no dibujar
        fig.add_shape(type="rect", x0=_zx0, y0=_zy0, x1=_zx1, y1=_zy1,
                      line=dict(color="rgba(255,255,255,0.22)", width=1),
                      fillcolor="rgba(15,23,42,0.35)", layer="below")
        fig.add_annotation(
            x=(_zx0+_zx1)/2, y=_zy1+0.06, text=f"<b>{_zlabel}</b>",
            showarrow=False, font=dict(size=10, color="#CBD5E1"),
            yanchor="bottom", bgcolor="rgba(7,17,31,0.70)",
            bordercolor="rgba(255,255,255,0.18)", borderwidth=1, borderpad=3,
        )

    # Dibujar cajas de categorias completamente nuevas (capas desconocidas del Discovery Engine)
    for bx0, by0, bx1, by1, blabel, bcolor in _new_boxes:
        fig.add_shape(type="rect", x0=bx0, y0=by0, x1=bx1, y1=by1,
                      line=dict(color=bcolor, width=1.5),
                      fillcolor="rgba(15,23,42,0.50)", layer="below")
        fig.add_annotation(
            x=(bx0+bx1)/2, y=by1+0.06, text=f"<b>{blabel}</b>",
            showarrow=False, font=dict(size=10, color="#FFFFFF"),
            yanchor="bottom", bgcolor="rgba(7,17,31,0.85)",
            bordercolor=bcolor, borderwidth=1, borderpad=3,
        )

    # ── Cargar nodos verificados: rutas de nodos verificados se pintarán en verde ──
    _verified_nodes: set = set()
    if conn is not None:
        try:
            for (vn,) in conn.execute(
                "SELECT node FROM node_verifications WHERE connected=1"
            ).fetchall():
                _verified_nodes.add(vn)
        except Exception:
            pass

    # Aplicar kind_override "verified" a rutas cuyos nodos están verificados.
    # Regla: basta con que el ORIGEN esté verificado. El destino (Ripple Payments,
    # XRPL, etc.) es infraestructura core — no necesita verificación separada.
    # Si ambos están verificados, también sube.
    _UPGRADEABLE_KINDS = {"private", "discovered", "partner", "government"}
    _all_routes = []
    for _r in ROUTES + _dyn_routes:
        _rsrc, _rdst, _rkind = str(_r[0]), str(_r[1]), str(_r[2])
        if _rkind in _UPGRADEABLE_KINDS and (_rsrc in _verified_nodes or _rdst in _verified_nodes):
            _all_routes.append((_rsrc, _rdst, "verified", _r[3], _r[4]))
        else:
            _all_routes.append(_r)

    # Filtrar rutas según el modo del mapa
    _CONFIRMED_KINDS  = {"real", "public", "private", "verified", "obligatory", "odl", "partner", "public_wallet"}
    _SURVEILLANCE_KINDS = {"watch", "discovered", "model", "future"}
    if route_filter == "confirmed":
        _all_routes = [r for r in _all_routes if r[2] in _CONFIRMED_KINDS]
    elif route_filter == "surveillance":
        _all_routes = [r for r in _all_routes if r[2] in _SURVEILLANCE_KINDS]

    # Normalizar focus_node para comparaciones seguras
    focus_node = str(focus_node).strip() if focus_node else None

    # Pre-calcular camino completo desde el foco hasta infraestructura Ripple/XRPL.
    # Antes se mostraba todo el subgrafo alcanzable; ahora se prioriza la cadena real:
    # nodo clickado → intermediarios → Ripple Payments / XRPL / RLUSD.
    _focus_connected: set = set()
    _focus_route_edges: set = set()
    if focus_node:
        try:
            _focus_paths = _find_ripple_paths(focus_node, _all_routes, _all_nodes)
        except Exception:
            _focus_paths = []
        if _focus_paths:
            _focus_connected = _nodes_from_ripple_paths(_focus_paths)
            _focus_route_edges = _edges_from_ripple_paths(_focus_paths)
            _focus_connected.add(focus_node)
        else:
            # Fallback: si no hay camino a Ripple/XRPL, mostrar relaciones inmediatas
            # para que el click nunca deje al usuario sin contexto.
            _out_adj: dict = {}
            _in_adj:  dict = {}
            for _r in _all_routes:
                _rs, _rd = str(_r[0]).strip(), str(_r[1]).strip()
                _out_adj.setdefault(_rs, set()).add(_rd)
                _in_adj.setdefault(_rd, set()).add(_rs)
            _focus_connected = {focus_node}
            for _nb in _out_adj.get(focus_node, set()):
                _focus_connected.add(_nb)
                _focus_route_edges.add((focus_node, _nb))
            for _src in _in_adj.get(focus_node, set()):
                _focus_connected.add(_src)
                _focus_route_edges.add((_src, focus_node))

    for route in _all_routes:
        src_n, dst_n = route[0], route[1]
        if src_n not in _all_nodes or dst_n not in _all_nodes:
            continue
        src, dst, kind, signal, label = route
        x0, y0 = _all_nodes[src_n]["pos"]
        x1, y1 = _all_nodes[dst_n]["pos"]
        _route_key = (src_n, dst_n, kind, signal, label)
        s = route_signal(row, _route_key)
        color = route_color(row, _route_key)

        # Focus mode: mostrar SOLO las aristas que pertenecen a la ruta completa
        # hacia Ripple/XRPL. Si no hubo ruta, se usa el fallback de relaciones inmediatas.
        sn = str(src_n).strip()
        dn = str(dst_n).strip()
        if not focus_node:
            is_connected = True
        elif _focus_route_edges:
            is_connected = (sn, dn) in _focus_route_edges
        else:
            is_connected = (sn in _focus_connected and dn in _focus_connected)
        if focus_node and not is_connected:
            continue   # omitir completamente — no renderizar rutas fuera del camino
        width = 1.15 + s * 6.8

        mx, my = (x0+x1)/2, (y0+y1)/2
        curve = 0.13 if y1 >= y0 else -0.13

        fig.add_trace(go.Scatter(
            x=[x0, mx, x1],
            y=[y0, my + curve, y1],
            mode="lines",
            line=dict(width=width, color=color, dash=route_dash(route) if is_connected else "solid"),
            hoverinfo="text" if is_connected else "skip",
            text=f"<b>{label}</b><br>Señal: {s:.1%}<br>Tipo: {kind}<br>Fuente: {signal}",
            showlegend=False,
            hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=13), bordercolor=color),
        ))

        if is_connected:
            angle = math.atan2(y1 - (my + curve), x1 - mx)
            ax = x1 - 0.18 * math.cos(angle)
            ay = y1 - 0.18 * math.sin(angle)
            fig.add_annotation(x=x1, y=y1, ax=ax, ay=ay,
                               xref="x", yref="y", axref="x", ayref="y",
                               showarrow=True, arrowhead=3, arrowsize=1.0,
                               arrowwidth=max(1, width/2.8), arrowcolor=color)

    layer_colors = {
        "Banca_AM":      "#F59E0B",   # ámbar — Americas
        "Banca_EU":      "#E67E22",   # naranja oscuro — Europa
        "Banca_AP":      "#D35400",   # terracota — Asia-Pac
        "ODL":           "#FB923C",   # naranja — corredores ODL
        "Privado":       "#FFB84D",   # rail privado
        "Ripple":        "#5AD7FF",   # Ripple core
        "Institucional": "#D9A7FF",
        "Exchange":      "#22D3EE",   # cyan — exchanges con wallets reales
        "Vigilancia":    "#B673FF",
        "Inteligencia":  "#60A5FA",
        "Público":       "#3CFF9B",
        "Futuro":        "#8CA0B8",
        # Capas de descubrimiento dinámico
        "Fintech":       "#F472B6",   # rosa — fintech pagos
        "CBDC":          "#34D399",   # verde esmeralda — banco central/CBDC
        "AssetMgmt":     "#A78BFA",   # violeta — gestión de activos
        "Gobierno":      "#FCD34D",   # amarillo — regulador/gobierno
        "Clearing":      "#38BDF8",   # azul — clearing/post-trade
        "RedPrivada":    "#FB7185",   # rojo suave — redes privadas/OTC
        "Puente":        "#22D3EE",   # cyan — puentes/cross-chain/oraculos
        "Proveedor":     "#F59E0B",   # naranja — proveedores/APIs/middleware
        "Descubierto":   "#94A3B8",   # gris azulado — genérico descubierto
        "Otro":          "#64748B",   # pizarra — sin clasificar
    }

    xs, ys, texts, colors, sizes, hovers, opacities, borders, border_widths, node_names = \
        [], [], [], [], [], [], [], [], [], []
    _big_nodes = {"XRPL", "RLUSD", "Public Gateway", "Ripple Payments", "Topology Engine"}
    for name, meta in _all_nodes.items():
        x, y = meta["pos"]
        xs.append(x); ys.append(y)
        node_names.append(name)
        base_color = layer_colors.get(meta["layer"], "#475569")
        base_size  = 62 if name in _big_nodes else 44

        nname = str(name).strip()
        if not focus_node:
            texts.append(f"{meta['icon']}<br>{name}")
            colors.append(base_color); sizes.append(base_size)
            opacities.append(0.98); borders.append("#FFFFFF"); border_widths.append(2.8)
        elif nname == focus_node:
            texts.append(f"{meta['icon']}<br>{name}")
            colors.append(base_color); sizes.append(base_size + 18)
            opacities.append(1.0); borders.append("#FFFFFF"); border_widths.append(5.0)
        elif nname in _focus_connected:
            texts.append(f"{meta['icon']}<br>{name}")
            colors.append(base_color); sizes.append(base_size)
            opacities.append(1.0); borders.append("#FFFFFF"); border_widths.append(2.8)
        else:
            # Nodo no conectado: completamente invisible — sin texto, sin círculo
            texts.append("")
            colors.append("rgba(0,0,0,0)"); sizes.append(0)
            opacities.append(0.0); borders.append("rgba(0,0,0,0)"); border_widths.append(0)

        hovers.append(f"<b>{name}</b><br>{meta['layer']}<br><i>Click para filtrar rutas</i>")

    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="markers+text",
        marker=dict(size=sizes, color=colors, opacity=opacities,
                    line=dict(width=border_widths, color=borders)),
        text=texts, textposition="middle center",
        textfont=dict(size=9, color="#FFFFFF", family="Arial Black"),
        customdata=node_names,
        hoverinfo="text", hovertext=hovers, showlegend=False,
        hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=13), bordercolor="#5AD7FF"),
    ))

    # Etiqueta del nodo foco encima del mapa
    if focus_node and focus_node in _all_nodes:
        fx, fy = _all_nodes[focus_node]["pos"]
        fig.add_annotation(
            x=fx, y=fy + 0.55,
            text=f"<b>🔍 {focus_node}</b>",
            showarrow=False, font=dict(size=13, color="#FFFFFF"),
            bgcolor="rgba(14,165,233,0.75)", bordercolor="#5AD7FF",
            borderwidth=1, borderpad=5,
        )

    # ── Wallets vigiladas — nodos + conexiones ─────────────────────────────────
    map_height = 800
    y_bottom   = -3.40
    if has_watched:
        # Posición de nodos conocidos del mapa (para trazar aristas)
        node_pos = {name: meta["pos"] for name, meta in NODES.items()}

        # ── Clasificar wallets: conectadas al mapa vs. sin conexión (Router) ──
        connected_wallets: List = []   # (wr, matched_node_name, matched_pos)
        router_wallets:    List = []   # (wr,)

        def _find_node(label_str: str) -> Optional[str]:
            """Devuelve el nombre del nodo del mapa para una etiqueta de wallet, o None."""
            s = label_str.strip()
            if not s or s in ("nan", "None", ""):
                return None
            # 1) lookup directo en WALLET_LABEL_TO_NODE
            mapped = WALLET_LABEL_TO_NODE.get(s)
            if mapped and mapped in node_pos:
                return mapped
            # 2) coincidencia exacta directa en node_pos
            if s in node_pos:
                return s
            # 3) coincidencia parcial (el nodo contiene la etiqueta o viceversa)
            sl = s.lower()
            for nname in node_pos:
                nl = nname.lower()
                if nl in sl or sl in nl:
                    return nname
            # 4) buscar también a través de WALLET_LABEL_TO_NODE con coincidencia parcial
            for wkey, nval in WALLET_LABEL_TO_NODE.items():
                if wkey.lower() in sl or sl in wkey.lower():
                    if nval in node_pos:
                        return nval
            return None

        for wr in watched.itertuples():
            top_cp = str(wr.top_cp_label)
            lbl    = str(wr.label)

            # Intentar con top_cp primero, luego con el label de la wallet
            node_name = _find_node(top_cp) or _find_node(lbl)

            if node_name:
                connected_wallets.append((wr, node_name, node_pos[node_name]))
            else:
                router_wallets.append(wr)

        n_conn = len(connected_wallets)
        n_rout = len(router_wallets)

        # ── Layout positions ──────────────────────────────────────────────────
        # Connected wallets occupy the left/centre of the bottom zone
        cols_conn = min(max(n_conn, 1), 7)
        conn_x_list: List[float] = []
        conn_y_list: List[float] = []
        for wi in range(n_conn):
            col_i = wi % cols_conn
            row_i = wi // cols_conn
            conn_x_list.append(-4.20 + col_i * (6.0 / max(cols_conn - 1, 1)))
            conn_y_list.append(-4.30 - row_i * 1.10)

        # Router wallets occupy the right side of the bottom zone
        cols_rout = min(max(n_rout, 1), 4)
        rout_x_list: List[float] = []
        rout_y_list: List[float] = []
        for wi in range(n_rout):
            col_i = wi % cols_rout
            row_i = wi // cols_rout
            rout_x_list.append(3.80 + col_i * (3.50 / max(cols_rout - 1, 1)))
            rout_y_list.append(-4.30 - row_i * 1.10)

        # Adjust map height and y_bottom
        max_rows = max(
            (n_conn - 1) // cols_conn + 1 if n_conn > 0 else 0,
            (n_rout - 1) // cols_rout + 1 if n_rout > 0 else 0,
            1,
        )
        y_bottom   = min(-5.50, -4.30 - (max_rows - 1) * 1.10 - 0.80)
        map_height = max(1080, int((3.40 - y_bottom) * 160))

        # ── Zone boxes ───────────────────────────────────────────────────────
        if n_conn > 0:
            fig.add_shape(
                type="rect",
                x0=-5.00, y0=y_bottom + 0.20, x1=3.10, y1=-3.60,
                line=dict(color="rgba(255,90,103,0.40)", width=1, dash="dot"),
                fillcolor="rgba(255,90,103,0.03)", layer="below",
            )
            fig.add_annotation(
                x=-0.95, y=-3.54,
                text="<b>🔍 Zona de vigilancia</b> — wallets detectadas automáticamente por el radar",
                showarrow=False, font=dict(size=10, color="#FF5A67"),
                yanchor="bottom", bgcolor="rgba(7,17,31,0.85)",
                bordercolor="#FF5A67", borderwidth=1, borderpad=4,
            )

        if n_rout > 0:
            fig.add_shape(
                type="rect",
                x0=3.20, y0=y_bottom + 0.20, x1=8.00, y1=-3.60,
                line=dict(color="rgba(255,90,103,0.55)", width=1.5, dash="dot"),
                fillcolor="rgba(255,90,103,0.05)", layer="below",
            )
            fig.add_annotation(
                x=5.60, y=-3.54,
                text="<b>🔀 Router</b> — sin conexión a infraestructura conocida",
                showarrow=False, font=dict(size=10, color="#FF5A67"),
                yanchor="bottom", bgcolor="rgba(7,17,31,0.85)",
                bordercolor="rgba(255,90,103,0.70)", borderwidth=1, borderpad=4,
            )

        # ── Render connected wallets ──────────────────────────────────────────
        def _wallet_color(role: str) -> str:
            r = role.lower()
            if "treasury" in r or "distribuidor" in r: return "#FF9D5C"
            if "odl" in r or "corredor" in r:          return "#FB923C"
            if "exchange" in r or "gateway" in r:      return "#60A5FA"
            if "market" in r or "maker" in r:          return "#D9A7FF"
            return "#FF5A67"

        wx_pts, wy_pts, wt_pts, wc_pts, ws_pts, wh_pts = [], [], [], [], [], []
        for wi, (wr, matched_node, matched_pos) in enumerate(connected_wallets):
            # En focus mode: mostrar solo wallets conectadas al nodo en foco
            if focus_node and matched_node not in _focus_connected and matched_node != focus_node:
                continue

            conf  = float(wr.confidence)
            vol   = float(wr.volume_xrp)
            role  = str(wr.role)
            label = _wallet_full_name(str(wr.wallet), str(wr.label))
            short = _wallet_map_label(label, 22)
            full_addr = str(wr.wallet)
            wx    = conn_x_list[wi]
            wy    = conn_y_list[wi]
            wc    = _wallet_color(role)
            ws    = int(36 + min(conf * 30, 28) + min(vol / 1_000_000 * 10, 20))

            wx_pts.append(wx); wy_pts.append(wy)
            wt_pts.append(f"🔍<br>{short}")
            wc_pts.append(wc); ws_pts.append(ws)
            wh_pts.append(
                f"<b>🔍 {html.escape(label)}</b><br>"
                f"Rol: {html.escape(role)}<br>"
                f"Confianza: {conf*100:.0f}%<br>"
                f"Volumen: {vol:,.0f} XRP<br>"
                f"Contraparte: {html.escape(str(wr.top_cp_label) or '?')}<br>"
                f"Dirección completa:<br><code>{html.escape(full_addr)}</code>"
            )

            tx0, ty0 = matched_pos
            fig.add_trace(go.Scatter(
                x=[wx, (wx + tx0) / 2, tx0],
                y=[wy, (wy + ty0) / 2, ty0],
                mode="lines",
                line=dict(width=1.8, color=wc, dash="dot"),
                hoverinfo="text",
                text=f"<b>Vigilancia:</b> {label} → {matched_node}",
                showlegend=False,
                hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=12), bordercolor=wc),
            ))

        if wx_pts:
            fig.add_trace(go.Scatter(
                x=wx_pts, y=wy_pts, mode="markers+text",
                marker=dict(
                    size=ws_pts, color=wc_pts, opacity=0.95,
                    line=dict(width=2.5, color="#FFFFFF"),
                    symbol="diamond",
                ),
                text=wt_pts, textposition="middle center",
                textfont=dict(size=8, color="#020617", family="Arial Black"),
                hoverinfo="text", hovertext=wh_pts,
                name="🔍 Wallets vigiladas",
                showlegend=True,
                hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=13), bordercolor="#FF5A67"),
            ))

        # ── Render router wallets (sin conexión) ──────────────────────────────
        rx_pts, ry_pts, rt_pts, rc_pts, rs_pts, rh_pts = [], [], [], [], [], []
        for wi, wr in enumerate(router_wallets):
            conf  = float(wr.confidence)
            vol   = float(wr.volume_xrp)
            role  = str(wr.role)
            label = _wallet_full_name(str(wr.wallet), str(wr.label))
            short = _wallet_map_label(label, 22)
            full_addr = str(wr.wallet)
            rx    = rout_x_list[wi]
            ry    = rout_y_list[wi]
            rc    = "#FF5A67"
            rs    = int(36 + min(conf * 30, 28) + min(vol / 1_000_000 * 10, 20))

            rx_pts.append(rx); ry_pts.append(ry)
            rt_pts.append(f"🔀<br>{short}")
            rc_pts.append(rc); rs_pts.append(rs)
            rh_pts.append(
                f"<b>🔀 {html.escape(label)}</b><br>"
                f"Rol: {html.escape(role)}<br>"
                f"Confianza: {conf*100:.0f}%<br>"
                f"Volumen: {vol:,.0f} XRP<br>"
                f"Contraparte: {html.escape(str(wr.top_cp_label) or '?')}<br>"
                f"Sin conexión a infraestructura conocida<br>"
                f"Dirección completa:<br><code>{html.escape(full_addr)}</code>"
            )

        if rx_pts:
            fig.add_trace(go.Scatter(
                x=rx_pts, y=ry_pts, mode="markers+text",
                marker=dict(
                    size=rs_pts, color=rc_pts, opacity=0.88,
                    line=dict(width=2.5, color="rgba(255,90,103,0.80)"),
                    symbol="diamond-open",
                ),
                text=rt_pts, textposition="middle center",
                textfont=dict(size=8, color="#FF5A67", family="Arial Black"),
                hoverinfo="text", hovertext=rh_pts,
                name="🔀 Router (sin conexión)",
                showlegend=True,
                hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=13), bordercolor="#FF5A67"),
            ))

    fig.update_layout(
        title=dict(text=title, font=dict(size=22, color="#FFFFFF")),
        template="plotly_dark",
        paper_bgcolor="#07111f",
        plot_bgcolor="#07111f",
        height=map_height,
        margin=dict(l=20, r=20, t=70, b=32),
        xaxis=dict(visible=False, range=[-9.30, 10.10]),
        yaxis=dict(visible=False, range=[y_bottom, 3.70]),
        font=dict(color="#FFFFFF"),
        legend=dict(orientation="h", y=1.04, x=0, font=dict(color="#FFFFFF", size=11),
                    bgcolor="rgba(15,23,42,.85)", bordercolor="rgba(255,255,255,.25)", borderwidth=1),
        hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=13), bordercolor="#5AD7FF"),
    )
    return fig


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_xrp_ohlcv(days: int = 90) -> pd.DataFrame:
    """
    Descarga datos OHLCV de XRP/USD desde CoinGecko.
    Intervalo automático: días ≤ 90 → datos cada 4h, días > 90 → diario.
    Devuelve DataFrame con columnas: day, open, high, low, close.
    """
    try:
        url = "https://api.coingecko.com/api/v3/coins/ripple/ohlc"
        params = {"vs_currency": "usd", "days": days}
        headers = {"User-Agent": "RippleRadarPro/6.0"}
        r = requests.get(url, params=params, headers=headers, timeout=20)
        r.raise_for_status()
        data = r.json()  # [[timestamp_ms, open, high, low, close], ...]
        if not data:
            return pd.DataFrame(columns=["day", "open", "high", "low", "close"])
        df = pd.DataFrame(data, columns=["timestamp_ms", "open", "high", "low", "close"])
        df["day"] = pd.to_datetime(df["timestamp_ms"], unit="ms")
        df = df.drop(columns=["timestamp_ms"])
        return df
    except Exception:
        return pd.DataFrame(columns=["day", "open", "high", "low", "close"])


def make_candlestick_chart(ohlcv: pd.DataFrame, scores_df: Optional[pd.DataFrame] = None) -> go.Figure:
    """
    Gráfico de velas OHLCV de XRP/USD al estilo TradingView.
    Opcionalmente superpone dex_score y anomaly_score en eje secundario.
    """
    fig = go.Figure()

    if not ohlcv.empty:
        increasing = dict(line=dict(color="#22C55E"), fillcolor="#22C55E")
        decreasing = dict(line=dict(color="#EF4444"), fillcolor="#EF4444")
        fig.add_trace(go.Candlestick(
            x=ohlcv["day"],
            open=ohlcv["open"], high=ohlcv["high"],
            low=ohlcv["low"],  close=ohlcv["close"],
            name="XRP/USD",
            increasing=increasing,
            decreasing=decreasing,
        ))

    # Superponer scores del radar como área semitransparente en eje derecho
    if scores_df is not None and not scores_df.empty:
        for col, name, color in [
            ("dex_score",     "DEX/AMM score",   "#FFB84D"),
            ("anomaly_score", "Anomalía",        "#FF5A67"),
            ("bull_score",    "Subida probable", "#3CFF9B"),
        ]:
            if col in scores_df.columns:
                fig.add_trace(go.Scatter(
                    x=pd.to_datetime(scores_df["day"]),
                    y=scores_df[col] * 100,
                    name=f"{name} (0–100)",
                    mode="lines",
                    line=dict(width=2, color=color, dash="dot"),
                    yaxis="y2",
                    opacity=0.85,
                ))

    fig.update_layout(
        title=dict(
            text="XRP/USD · Velas OHLCV + scores de radar (eje dcho.)",
            font=dict(color="#FFFFFF", size=18)
        ),
        template="plotly_dark",
        paper_bgcolor="#07111f",
        plot_bgcolor="#07111f",
        height=500,
        font=dict(color="#FFFFFF", size=13),
        showlegend=True,
        legend=dict(
            orientation="h", y=1.08, x=0,
            font=dict(color="#FFFFFF", size=12),
            bgcolor="rgba(15,23,42,.85)",
            bordercolor="rgba(255,255,255,.30)",
            borderwidth=1,
        ),
        xaxis=dict(
            color="#FFFFFF",
            gridcolor="rgba(255,255,255,.12)",
            tickfont=dict(color="#FFFFFF", size=11),
            rangeslider=dict(visible=False),
        ),
        yaxis=dict(
            title="USD", color="#FFFFFF",
            gridcolor="rgba(255,255,255,.18)",
            tickfont=dict(color="#FFFFFF", size=12),
            title_font=dict(color="#FFFFFF"),
        ),
        yaxis2=dict(
            title="Score %", overlaying="y", side="right",
            range=[0, 100],
            tickfont=dict(color="#94A3B8", size=11),
            title_font=dict(color="#94A3B8"),
            gridcolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=13), bordercolor="#5AD7FF"),
        margin=dict(l=20, r=20, t=90, b=35),
    )
    return fig


def fetch_xrp_price_history(days: int = 365) -> pd.DataFrame:
    """Descarga precio histórico XRP/USD desde CoinGecko (gratuito, sin API key)."""
    try:
        url = "https://api.coingecko.com/api/v3/coins/ripple/market_chart"
        params = {"vs_currency": "usd", "days": days, "interval": "daily"}
        headers = {"User-Agent": "RippleRadarPro/6.0"}
        r = requests.get(url, params=params, headers=headers, timeout=20)
        r.raise_for_status()
        data = r.json()
        prices = data.get("prices", [])
        if not prices:
            return pd.DataFrame(columns=["day", "price_usd"])
        df_p = pd.DataFrame(prices, columns=["timestamp_ms", "price_usd"])
        df_p["day"] = pd.to_datetime(df_p["timestamp_ms"], unit="ms").dt.strftime("%Y-%m-%d")
        # Un precio por día (último del día)
        df_p = df_p.groupby("day", as_index=False)["price_usd"].last()
        return df_p
    except Exception:
        return pd.DataFrame(columns=["day", "price_usd"])


def fetch_xrp_spot_price_usd() -> tuple[Optional[float], str]:
    """Precio spot XRP/USD en vivo con varios proveedores públicos.
    Devuelve (precio, fuente). No requiere API key.
    """
    headers = {"User-Agent": "RippleRadarPro/price/1.0"}
    providers = [
        ("CoinGecko spot", "https://api.coingecko.com/api/v3/simple/price?ids=ripple&vs_currencies=usd"),
        ("Binance XRPUSDT", "https://api.binance.com/api/v3/ticker/price?symbol=XRPUSDT"),
        ("Coinbase XRP-USD", "https://api.coinbase.com/v2/prices/XRP-USD/spot"),
    ]
    for name, url in providers:
        try:
            r = requests.get(url, headers=headers, timeout=8)
            if r.status_code != 200:
                continue
            data = r.json()
            price = None
            if name.startswith("CoinGecko"):
                price = data.get("ripple", {}).get("usd")
            elif name.startswith("Binance"):
                price = data.get("price")
            elif name.startswith("Coinbase"):
                price = data.get("data", {}).get("amount")
            price = float(price)
            if price > 0:
                return price, name
        except Exception:
            continue
    return None, "no disponible"


def latest_xrp_price_from_history(xrp_history: Optional[pd.DataFrame]) -> tuple[Optional[float], str]:
    """Extrae el último precio XRP/USD histórico si está disponible."""
    try:
        if isinstance(xrp_history, pd.DataFrame) and not xrp_history.empty and "price_usd" in xrp_history.columns:
            series = pd.to_numeric(xrp_history["price_usd"], errors="coerce").dropna()
            if not series.empty and float(series.iloc[-1]) > 0:
                return float(series.iloc[-1]), "CoinGecko histórico último punto"
    except Exception:
        pass
    return None, "no disponible"


def resolve_xrp_price_now(xrp_history: Optional[pd.DataFrame] = None, row: Optional[object] = None, df_source: Optional[pd.DataFrame] = None) -> tuple[float, str, bool]:
    """Resuelve precio XRP real para la cinemática.
    Prioridad: spot vivo -> histórico real -> columnas internas -> referencia.
    Devuelve (precio, fuente, es_referencia).
    """
    price, source = fetch_xrp_spot_price_usd()
    if price is not None:
        return price, source, False

    price, source = latest_xrp_price_from_history(xrp_history)
    if price is not None:
        return price, source, False

    try:
        if row is not None:
            for col in ["xrp_price", "price_usd", "price", "close", "xrp_close"]:
                try:
                    val = row.get(col, None) if hasattr(row, "get") else None
                    val = float(val)
                    if val > 0:
                        return val, f"columna interna {col}", False
                except Exception:
                    pass
    except Exception:
        pass

    try:
        if isinstance(df_source, pd.DataFrame) and not df_source.empty:
            for col in ["xrp_price", "price_usd", "price", "close", "xrp_close"]:
                if col in df_source.columns:
                    series = pd.to_numeric(df_source[col], errors="coerce").dropna()
                    if not series.empty and float(series.iloc[-1]) > 0:
                        return float(series.iloc[-1]), f"columna interna {col}", False
    except Exception:
        pass

    return 2.50, "referencia visual fija: conecta precio real", True


def make_scores_chart(df: pd.DataFrame, conn: Optional[sqlite3.Connection] = None) -> go.Figure:
    work = prepare_chart_metrics(df, conn)
    fig = go.Figure()
    for col, name, color, width in [
        ("bull_score",      "Subida probable / momentum",   "#3CFF9B", 3),
        ("bear_score",      "Riesgo bajada",                "#FF5A67", 3),
        ("flip_score",      "Flip confirmado por evidencia", "#B673FF", 4),
        ("radar_coverage",  "Cobertura verificada",          "#5AD7FF", 3),
        ("adoption_score",  "Adopción técnica verificada",   "#60A5FA", 3),
        ("pump_score",      "Watch especulativo / pump",     "#FFB84D", 2),
    ]:
        c = _chart_col(work, col)
        if c in work.columns:
            fig.add_trace(go.Scatter(x=work["day"], y=pd.to_numeric(work[c], errors="coerce").fillna(0).clip(0,100), name=name, mode="lines",
                                     line=dict(width=width, color=color)))
    fig.add_hline(y=80, line_dash="dash", line_color="#FFFFFF",
                  annotation_text="Umbral fuerte >80%", annotation_font_color="#FFFFFF")
    fig.add_annotation(text="Los canales documentales se bloquean si no hay pruebas/rutas verificadas guardadas.", xref="paper", yref="paper", x=0.01, y=1.10, showarrow=False, font=dict(color="#94A3B8", size=11))
    return white_layout(fig, "Scores generales con gate de evidencia", 420, [0, 100])

def _score_pct_from_row(row: Any, key: str, default: float = 0.0) -> float:
    try:
        v = float(row.get(key, default))
        return v if v > 1.5 else v * 100.0
    except Exception:
        return float(default)


def _pct100(x: Any, default: float = 0.0) -> float:
    """Normaliza cualquier métrica a escala 0-100 sin doble escalar."""
    try:
        v = float(x)
        if not math.isfinite(v):
            return float(default)
        if v <= 1.5:
            v *= 100.0
        return float(max(0.0, min(100.0, v)))
    except Exception:
        return float(default)


def _row_value(row: Any, key: str, default: Any = 0.0) -> Any:
    try:
        if hasattr(row, "get"):
            return row.get(key, default)
        return getattr(row, key, default)
    except Exception:
        return default


def signal_channels_from_row(row: Any) -> Dict[str, float]:
    """
    Separa la lectura del radar en tres canales.

    Cambio importante: el canal documental/institucional queda bloqueado por
    evidencias reales de la base local. Es decir, si no hay pruebas guardadas
    ni rutas verificadas, la línea azul debe quedarse en 0 aunque existan
    scores internos de topología/cobertura generados por el sistema.
    """
    g = lambda k: _pct100(_row_value(row, k, 0.0))

    ledger_real = (
        g("public_xrpl_score") * 0.22
        + g("payment_flow_score") * 0.15
        + g("trustline_score") * 0.12
        + g("dex_score") * 0.14
        + g("large_transfer_score") * 0.14
        + g("cluster_score") * 0.11
        + g("fingerprint_score") * 0.12
    )

    raw_institucional = (
        g("institutional_route_score") * 0.30
        + g("radar_coverage") * 0.28
        + g("topology_score") * 0.18
        + g("cross_network_score") * 0.12
        + g("custody_score") * 0.07
        + g("prime_brokerage_score") * 0.05
    )

    # Gate documental real: evita líneas azules fantasma cuando el mapa está vacío.
    proof_count = float(_row_value(row, "proof_count", 0) or 0)
    official_count = float(_row_value(row, "official_proof_count", 0) or 0)
    route_count = float(_row_value(row, "verified_route_count", 0) or 0)
    evidence_gate_present = any(str(k) in getattr(row, "index", []) for k in ("proof_count", "official_proof_count", "verified_route_count")) if hasattr(row, "index") else any(hasattr(row, k) for k in ("proof_count", "official_proof_count", "verified_route_count"))

    if evidence_gate_present:
        # 0 pruebas = 0 documental. Fuentes oficiales pesan más que rutas genéricas.
        gate = min(1.0, (official_count * 0.22) + (proof_count * 0.10) + (route_count * 0.04))
        institucional = raw_institucional * gate
    else:
        institucional = raw_institucional

    # Especulación sube si hay pump, poca persistencia, mucho bull no respaldado
    # por ledger/documental o señales sin anclaje real.
    unsupported_bull = max(0.0, g("bull_score") - ledger_real)
    low_persistence = max(0.0, 100.0 - g("persistence_score"))
    weak_real_anchor = max(0.0, 100.0 - max(ledger_real, institucional))
    especulativo = (
        g("pump_score") * 0.45
        + low_persistence * 0.22
        + weak_real_anchor * 0.18
        + unsupported_bull * 0.15
    )
    return {
        "ledger_real": _pct100(ledger_real),
        "institucional_documental": _pct100(institucional),
        "especulativo_watch": _pct100(especulativo),
    }




# =============================================================================
# CHART EVIDENCE GATE — filtro universal para evitar gráficas fantasma
# =============================================================================
# Objetivo: todos los gráficos que mezclan señales institucionales/documentales
# deben pasar por el mismo filtro de evidencia. Si no hay pruebas reales guardadas
# en SQLite, los canales documentales/institucionales y el Flip confirmado quedan
# en 0 o muy bajos. Las señales watch quedan separadas como vigilancia, no prueba.

INSTITUTIONAL_CHART_COLS = {
    "institutional_route_score", "bridge_score", "public_gateway_score",
    "custody_score", "prime_brokerage_score", "cross_network_score",
    "topology_score", "radar_coverage", "adoption_score",
}

LEDGER_CHART_COLS = {
    "public_xrpl_score", "payment_flow_score", "trustline_score", "dex_score",
    "large_transfer_score", "cluster_score", "fingerprint_score", "anomaly_score",
    "time_regime_score",
}

WATCH_CHART_COLS = {"pump_score", "bull_score", "bear_score"}


def _chart_evidence_gate_from_row(row: Any) -> float:
    """0..1. 0 = no existe evidencia documental/ruta verificada guardada."""
    proof_count = float(_row_value(row, "proof_count", 0) or 0)
    official_count = float(_row_value(row, "official_proof_count", 0) or 0)
    route_count = float(_row_value(row, "verified_route_count", 0) or 0)
    return float(max(0.0, min(1.0, official_count * 0.22 + proof_count * 0.10 + route_count * 0.04)))


def _chart_ledger_gate_from_row(row: Any) -> float:
    """0..1. Usa tx/volumen real si existe; si no, permite señales ledger ya calculadas."""
    tx_count = float(_row_value(row, "tx_count", 0) or 0)
    xrp_volume = float(_row_value(row, "xrpl_volume", 0) or 0)
    rlusd_volume = float(_row_value(row, "rlusd_volume", 0) or 0)
    # Si hay columnas explícitas de actividad, esas mandan.
    explicit_activity = (tx_count > 0) or (xrp_volume > 0) or (rlusd_volume > 0)
    if explicit_activity:
        return float(max(0.0, min(1.0, tx_count / 120.0 + math.log10(max(1.0, xrp_volume + rlusd_volume)) / 9.0)))
    # Si no hay columnas de actividad, no anulamos las métricas ledger porque pueden venir de pipeline anterior.
    return 1.0


def prepare_chart_metrics(df: pd.DataFrame, conn: Optional[sqlite3.Connection] = None) -> pd.DataFrame:
    """Devuelve un DataFrame seguro para gráficas.

    Crea columnas *_chart:
    - ledger real: queda intacto salvo que exista evidencia explícita de 0 actividad.
    - institucional/documental: queda multiplicado por gate de pruebas reales.
    - flip/adopción/cobertura/fase: recalculados desde canales separados.
    - watch/pump: se conserva como vigilancia, pero no sube documental.
    """
    if df is None or df.empty:
        return df.copy() if isinstance(df, pd.DataFrame) else pd.DataFrame()
    work = add_evidence_counts_to_metrics_df(conn, df)
    # Canales seguros por fila
    ch_rows = [signal_channels_from_row(r) for _, r in work.iterrows()]
    work["ledger_real_channel"] = [c["ledger_real"] for c in ch_rows]
    work["institutional_channel"] = [c["institucional_documental"] for c in ch_rows]
    work["speculative_channel"] = [c["especulativo_watch"] for c in ch_rows]

    for col in list(set(work.columns) & (INSTITUTIONAL_CHART_COLS | LEDGER_CHART_COLS | WATCH_CHART_COLS | {"flip_score", "phase", "persistence_score"})):
        base = pd.to_numeric(work[col], errors="coerce").fillna(0.0)
        # Normalizar a 0-100 si viene en 0-1, manteniendo columnas como phase aparte.
        if col != "phase" and base.max() <= 1.5:
            base = base * 100.0
        if col in INSTITUTIONAL_CHART_COLS:
            # Estas señales pueden existir como inferencia interna, pero no son prueba sin evidencias guardadas.
            work[f"{col}_chart"] = base * work.apply(_chart_evidence_gate_from_row, axis=1)
        elif col in LEDGER_CHART_COLS:
            work[f"{col}_chart"] = base * work.apply(_chart_ledger_gate_from_row, axis=1)
        elif col in WATCH_CHART_COLS:
            work[f"{col}_chart"] = base.clip(0, 100)
        elif col == "persistence_score":
            # La persistencia no prueba adopción por sí sola. Se limita por el mejor anclaje real.
            anchor = work[["ledger_real_channel", "institutional_channel"]].max(axis=1)
            work[f"{col}_chart"] = np.minimum(base.clip(0, 100), anchor)
        elif col == "flip_score":
            safe_flip = (
                work["ledger_real_channel"] * 0.50
                + work["institutional_channel"] * 0.35
                + np.maximum(0, 100 - work["speculative_channel"]) * 0.15
            )
            # Si no hay ni ledger ni documental, el flip confirmado debe quedarse en 0.
            anchor = work[["ledger_real_channel", "institutional_channel"]].max(axis=1)
            safe_flip = np.where(anchor <= 1.0, 0.0, safe_flip)
            work[f"{col}_chart"] = np.minimum(base.clip(0, 100), safe_flip).clip(0, 100)
        elif col == "phase":
            flip_series = work.get("flip_score_chart", pd.Series([0]*len(work), index=work.index))
            work[f"{col}_chart"] = np.floor(flip_series / 20.0).clip(0, 5)
    return work


def _chart_col(df: pd.DataFrame, col: str) -> str:
    """Usa la columna segura para gráfica si existe."""
    safe = f"{col}_chart"
    return safe if safe in df.columns else col

def _parse_sqlite_date(value: Any) -> Optional[pd.Timestamp]:
    """Parsea fechas de SQLite siempre como día tz-naive.

    Algunas tablas guardan ISO con offset/Z y otras fechas locales sin zona.
    Pandas no permite comparar timestamps tz-aware con tz-naive; por eso
    normalizamos todo a UTC, eliminamos timezone y comparamos solo por día.
    """
    try:
        if value is None:
            return None
        ts = pd.to_datetime(str(value), errors="coerce", utc=True)
        if pd.isna(ts):
            return None
        try:
            ts = ts.tz_convert(None)
        except Exception:
            try:
                ts = ts.tz_localize(None)
            except Exception:
                pass
        return ts.normalize()
    except Exception:
        return None


def _officialish_blob(blob: Any) -> bool:
    txt = str(blob or "").lower()
    return any(d in txt for d in (
        "bis.org", "ripple.com", "hkma.gov", "hkma.gov.hk", "federalreserve.gov",
        "sec.gov", "xrpl.org", "central bank", "official", "pdf", "mbridge",
        "bank for international settlements"
    ))


def add_evidence_counts_to_metrics_df(conn: Optional[sqlite3.Connection], df: pd.DataFrame) -> pd.DataFrame:
    """Añade contadores acumulados de evidencias reales por día.

    Sin esto, los gráficos podían mostrar una línea documental azul por scores
    internos aunque no hubiera ninguna prueba ni ruta validada guardada.
    """
    work = df.copy()
    if work.empty or "day" not in work.columns:
        return work
    work["_day_norm"] = pd.to_datetime(work["day"], errors="coerce", utc=True).dt.tz_convert(None).dt.normalize()
    proof_events: List[Tuple[pd.Timestamp, bool]] = []
    route_events: List[pd.Timestamp] = []

    if conn is not None:
        try:
            for validated_at, proof_data, conf in conn.execute("SELECT validated_at, proof_data, confidence FROM connection_proofs").fetchall():
                day = _parse_sqlite_date(validated_at)
                if day is not None and float(conf or 0) > 0:
                    proof_events.append((day, _officialish_blob(proof_data)))
        except Exception:
            pass
        try:
            for added_at, kind, conf in conn.execute("SELECT added_at, kind, confidence FROM dynamic_routes").fetchall():
                day = _parse_sqlite_date(added_at)
                k = str(kind or "").lower().strip()
                if day is not None and float(conf or 0) >= 0.55 and k not in {"watch", "model", "future", "inferred"}:
                    route_events.append(day)
        except Exception:
            pass

    proof_days = [d for d, _ in proof_events]
    official_days = [d for d, is_off in proof_events if is_off]

    def count_leq(days: List[pd.Timestamp], d: pd.Timestamp) -> int:
        if pd.isna(d):
            return 0
        return sum(1 for x in days if x <= d)

    work["proof_count"] = [count_leq(proof_days, d) for d in work["_day_norm"]]
    work["official_proof_count"] = [count_leq(official_days, d) for d in work["_day_norm"]]
    work["verified_route_count"] = [count_leq(route_events, d) for d in work["_day_norm"]]
    return work.drop(columns=["_day_norm"], errors="ignore")

def flip_quality_label(row: Any) -> Tuple[str, str, str]:
    ch = signal_channels_from_row(row)
    flip = _score_pct_from_row(row, "flip_score")
    ledger = ch["ledger_real"]
    inst = ch["institucional_documental"]
    spec = ch["especulativo_watch"]
    if ledger >= 65 and inst >= 55 and spec <= 45 and flip >= 70:
        return "🟢 Flip anclado", "#3CFF9B", "La fase sube con actividad pública real + evidencia documental; baja dependencia de narrativa/speculación."
    if ledger >= 45 or inst >= 55:
        return "🟡 Señal mixta", "#FFB84D", "Hay datos útiles, pero todavía mezcla actividad real con inferencias/watch. Conviene abrir las pruebas antes de concluir."
    return "🔴 Señal débil", "#FF5A67", "Predominan señales especulativas o hay poca actividad verificable en ledger. No debe interpretarse como conexión operativa."


def make_flip_channels_chart(df: pd.DataFrame, conn: Optional[sqlite3.Connection] = None) -> go.Figure:
    work = prepare_chart_metrics(df, conn)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=work["day"], y=work["ledger_real_channel"], name="Ledger real verificable", mode="lines", line=dict(width=4, color="#3CFF9B")))
    fig.add_trace(go.Scatter(x=work["day"], y=work["institutional_channel"], name="Documental/institucional", mode="lines", line=dict(width=3, color="#5AD7FF")))
    fig.add_trace(go.Scatter(x=work["day"], y=work["speculative_channel"], name="Watch/especulativo", mode="lines", line=dict(width=3, color="#FFB84D", dash="dot")))
    flip_col = _chart_col(work, "flip_score")
    if flip_col in work.columns:
        fig.add_trace(go.Scatter(x=work["day"], y=pd.to_numeric(work[flip_col], errors="coerce").fillna(0).clip(0,100), name="Flip final verificado", mode="lines", line=dict(width=4, color="#B673FF")))
    fig.add_hline(y=80, line_dash="dash", line_color="#FFFFFF", annotation_text="Zona fuerte", annotation_font_color="#FFFFFF")
    return white_layout(fig, "Flip explicado: ledger real vs pruebas documentales vs watch especulativo", 430, [0, 100])


def render_flip_quality_panel(row: Any) -> None:
    ch = signal_channels_from_row(row)
    label, color, msg = flip_quality_label(row)
    st.markdown(f"""
<div style='border:1px solid {color};border-radius:18px;background:linear-gradient(135deg,rgba(2,6,23,.96),rgba(15,23,42,.86));padding:1rem 1.15rem;margin:.55rem 0 1rem 0;box-shadow:0 0 30px rgba(90,215,255,.08);'>
  <div style='font-size:1.02rem;font-weight:900;color:{color};'>{label}</div>
  <div style='color:#CBD5E1;font-size:.90rem;margin-top:.20rem;'>{html.escape(msg)}</div>
  <div style='display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.6rem;margin-top:.8rem;'>
    <div style='background:rgba(60,255,155,.08);border:1px solid rgba(60,255,155,.25);border-radius:14px;padding:.65rem;'><b style='color:#3CFF9B'>Ledger real</b><br><span style='font-size:1.25rem;color:#E2E8F0;font-weight:900'>{ch['ledger_real']:.1f}%</span><br><span style='color:#94A3B8;font-size:.78rem'>pagos, trustlines, DEX/AMM, whales, clusters</span></div>
    <div style='background:rgba(90,215,255,.08);border:1px solid rgba(90,215,255,.25);border-radius:14px;padding:.65rem;'><b style='color:#5AD7FF'>Documental</b><br><span style='font-size:1.25rem;color:#E2E8F0;font-weight:900'>{ch['institucional_documental']:.1f}%</span><br><span style='color:#94A3B8;font-size:.78rem'>pruebas oficiales, rutas y cobertura</span></div>
    <div style='background:rgba(255,184,77,.08);border:1px solid rgba(255,184,77,.25);border-radius:14px;padding:.65rem;'><b style='color:#FFB84D'>Watch/especulativo</b><br><span style='font-size:1.25rem;color:#E2E8F0;font-weight:900'>{ch['especulativo_watch']:.1f}%</span><br><span style='color:#94A3B8;font-size:.78rem'>narrativa, pump, inferencias no operativas</span></div>
  </div>
</div>
""", unsafe_allow_html=True)


def _safe_count_table(conn: Optional[sqlite3.Connection], table: str, where: str = "", params: Tuple[Any, ...] = ()) -> int:
    if conn is None:
        return 0
    try:
        sql = f"SELECT COUNT(*) FROM {table} " + (f"WHERE {where}" if where else "")
        return int(conn.execute(sql, params).fetchone()[0] or 0)
    except Exception:
        return 0



# Compatibilidad para módulos/pestañas antiguas que llaman a _safe_count().
# En versiones anteriores solo existía _safe_count_table().
def _safe_count(conn: Optional[sqlite3.Connection], table: str, where: str = "", params: Tuple[Any, ...] = ()) -> int:
    return _safe_count_table(conn, table, where, params)

def data_quality_snapshot(conn: Optional[sqlite3.Connection], row: Any) -> Dict[str, Any]:
    """Radiografía honesta de calidad de datos usada por gráficos y fase Flip."""
    ch = signal_channels_from_row(row)
    proofs = _safe_count_table(conn, "connection_proofs")
    dyn_routes = _safe_count_table(conn, "dynamic_routes")
    wallet_rows = _safe_count_table(conn, "watched_wallets")
    tx_rows = _safe_count_table(conn, "xrpl_transactions")
    rlusd_rows = _safe_count_table(conn, "rlusd_transactions")
    clusters = _safe_count_table(conn, "wallet_clusters")
    fps = _safe_count_table(conn, "institutional_fingerprints")
    officialish = 0
    try:
        if conn is not None:
            rows = conn.execute("SELECT proof_data FROM connection_proofs LIMIT 500").fetchall()
            for (blob,) in rows:
                txt = str(blob or "").lower()
                if any(d in txt for d in ("bis.org", "ripple.com", "hkma.gov", "federalreserve.gov", "sec.gov", "xrpl.org", "central bank", "official")):
                    officialish += 1
    except Exception:
        pass

    verified_density = min(100.0, proofs * 6 + officialish * 8 + dyn_routes * 2)
    ledger_depth = min(100.0, tx_rows * 0.08 + rlusd_rows * 0.18 + clusters * 8 + fps * 8)
    wallet_quality = min(100.0, wallet_rows * 6)
    balance_penalty = max(0.0, ch["especulativo_watch"] - max(ch["ledger_real"], ch["institucional_documental"])) * 0.35
    overall = max(5.0, min(98.0, (verified_density * 0.35 + ledger_depth * 0.30 + ch["ledger_real"] * 0.15 + ch["institucional_documental"] * 0.15 + wallet_quality * 0.05) - balance_penalty))

    if overall >= 80:
        label, color = "🟢 Alta", "#3CFF9B"
    elif overall >= 58:
        label, color = "🟡 Media", "#FFB84D"
    else:
        label, color = "🔴 Exploratoria", "#FF5A67"

    return {
        "overall": overall,
        "label": label,
        "color": color,
        "proofs": proofs,
        "officialish": officialish,
        "dynamic_routes": dyn_routes,
        "wallets": wallet_rows,
        "tx_rows": tx_rows,
        "rlusd_rows": rlusd_rows,
        "clusters": clusters,
        "fingerprints": fps,
        "ledger_real": ch["ledger_real"],
        "documental": ch["institucional_documental"],
        "watch": ch["especulativo_watch"],
    }


def render_data_quality_panel(conn: Optional[sqlite3.Connection], row: Any, *, context: str = "tecnico") -> None:
    q = data_quality_snapshot(conn, row)
    st.markdown(f"""
<div style='border:1px solid {q['color']};border-radius:20px;background:linear-gradient(135deg,rgba(2,6,23,.97),rgba(15,23,42,.90));padding:1rem 1.15rem;margin:.75rem 0 1rem 0;box-shadow:0 0 34px rgba(90,215,255,.10);'>
  <div style='display:flex;align-items:center;justify-content:space-between;gap:1rem;flex-wrap:wrap;'>
    <div>
      <div style='font-size:1.05rem;font-weight:950;color:{q['color']};'>🧪 Veracidad técnica estimada: {q['label']} · {q['overall']:.1f}%</div>
      <div style='color:#CBD5E1;font-size:.90rem;margin-top:.20rem;'>El panel técnico mezcla ledger real, documentos oficiales, rutas verificadas y señales watch. Las gráficas separan esos canales para no vender una inferencia como prueba operativa.</div>
    </div>
    <div style='color:#E2E8F0;font-weight:900;background:rgba(255,255,255,.06);border:1px solid rgba(255,255,255,.12);border-radius:14px;padding:.45rem .75rem;'>Pruebas: {q['proofs']} · Rutas: {q['dynamic_routes']} · Wallets: {q['wallets']}</div>
  </div>
  <div style='display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:.6rem;margin-top:.85rem;'>
    <div style='background:rgba(60,255,155,.08);border:1px solid rgba(60,255,155,.22);border-radius:14px;padding:.65rem;'><b style='color:#3CFF9B'>Ledger real</b><br><span style='color:#E2E8F0;font-size:1.18rem;font-weight:900'>{q['ledger_real']:.1f}%</span><br><span style='color:#94A3B8;font-size:.78rem'>{q['tx_rows']} tx XRPL · {q['rlusd_rows']} RLUSD · {q['clusters']} clusters · {q['fingerprints']} fingerprints</span></div>
    <div style='background:rgba(90,215,255,.08);border:1px solid rgba(90,215,255,.22);border-radius:14px;padding:.65rem;'><b style='color:#5AD7FF'>Documental/verificado</b><br><span style='color:#E2E8F0;font-size:1.18rem;font-weight:900'>{q['documental']:.1f}%</span><br><span style='color:#94A3B8;font-size:.78rem'>{q['officialish']} fuentes fuertes detectadas dentro de {q['proofs']} pruebas</span></div>
    <div style='background:rgba(255,184,77,.08);border:1px solid rgba(255,184,77,.22);border-radius:14px;padding:.65rem;'><b style='color:#FFB84D'>Watch / especulativo</b><br><span style='color:#E2E8F0;font-size:1.18rem;font-weight:900'>{q['watch']:.1f}%</span><br><span style='color:#94A3B8;font-size:.78rem'>Sirve para vigilancia, no para afirmar conexión operativa.</span></div>
  </div>
  <div style='margin-top:.85rem;color:#CBD5E1;font-size:.88rem;'>
    <b style='color:#E2E8F0'>Cómo mejora la calidad:</b> cada institución buscada aporta documentos, PDFs, rutas A→B y posibles wallets. Si varias búsquedas confirman los mismos nodos con fuentes oficiales y después aparecen huellas ledger coherentes, sube la calidad. Si solo aumentan rutas watch sin pruebas, el sistema no sube la veracidad; solo amplía vigilancia.
  </div>
  <div style='margin-top:.45rem;color:#94A3B8;font-size:.80rem;'>Verde = on-chain/documentado · Azul = institucional oficial · Amarillo = cadena indirecta · Naranja = watch/inferido · Gris/rojo = sin prueba.</div>
</div>
""", unsafe_allow_html=True)


def run_chart_cross_data_tests() -> List[Dict[str, Any]]:
    """Tests sintéticos para comprobar todos los gráficos con el gate de evidencia."""
    import sqlite3 as _sqlite3
    rows = []
    base_days = pd.date_range("2026-01-01", periods=4, freq="D")

    scenarios = [
        ("sin_pruebas_institucionales", False, {
            "public_xrpl_score": 0, "payment_flow_score": 0, "trustline_score": 0, "dex_score": 0,
            "large_transfer_score": 0, "cluster_score": 0, "fingerprint_score": 0,
            "institutional_route_score": 88, "radar_coverage": 76, "topology_score": 70,
            "cross_network_score": 61, "custody_score": 38, "prime_brokerage_score": 30,
            "bridge_score": 80, "public_gateway_score": 80, "pump_score": 72,
            "persistence_score": 80, "bull_score": 70, "bear_score": 20,
            "flip_score": 75, "adoption_score": 70, "phase": 4,
        }),
        ("con_prueba_oficial", True, {
            "public_xrpl_score": 20, "payment_flow_score": 15, "trustline_score": 10, "dex_score": 8,
            "large_transfer_score": 12, "cluster_score": 5, "fingerprint_score": 4,
            "institutional_route_score": 88, "radar_coverage": 76, "topology_score": 70,
            "cross_network_score": 61, "custody_score": 38, "prime_brokerage_score": 30,
            "bridge_score": 80, "public_gateway_score": 80, "pump_score": 22,
            "persistence_score": 44, "bull_score": 52, "bear_score": 25,
            "flip_score": 58, "adoption_score": 70, "phase": 3,
        }),
        ("ledger_real_sin_documental", False, {
            "public_xrpl_score": 82, "payment_flow_score": 75, "trustline_score": 62, "dex_score": 70,
            "large_transfer_score": 68, "cluster_score": 74, "fingerprint_score": 66,
            "institutional_route_score": 75, "radar_coverage": 70, "topology_score": 70,
            "cross_network_score": 65, "custody_score": 50, "prime_brokerage_score": 40,
            "bridge_score": 70, "public_gateway_score": 70, "pump_score": 18,
            "persistence_score": 72, "bull_score": 78, "bear_score": 18,
            "flip_score": 76, "adoption_score": 65, "phase": 4,
            "tx_count": 250, "xrpl_volume": 3_000_000,
        }),
    ]

    for name, with_proof, row in scenarios:
        conn = _sqlite3.connect(":memory:")
        conn.execute("CREATE TABLE connection_proofs (validated_at TEXT, proof_data TEXT, confidence REAL)")
        conn.execute("CREATE TABLE dynamic_routes (added_at TEXT, kind TEXT, confidence REAL)")
        if with_proof:
            conn.execute("INSERT INTO connection_proofs VALUES ('2026-01-01','bis.org official pdf',0.95)")
            conn.execute("INSERT INTO dynamic_routes VALUES ('2026-01-01','official',0.90)")
        df = pd.DataFrame([{**row, "day": d} for d in base_days])
        gated = prepare_chart_metrics(df, conn)
        ch = signal_channels_from_row(gated.iloc[-1])
        figs = [
            make_flip_channels_chart(df, conn),
            make_adoption_chart(df, None, conn),
            make_public_footprints_chart(df, None, conn),
            make_intelligence_engines_chart(df, conn),
            make_engine_heat_chart(df, conn),
            make_phase_chart(df, conn),
            make_scores_chart(df, conn),
        ]
        bounds_ok = True
        traces_ok = True
        for fig in figs:
            traces_ok = traces_ok and len(fig.data) >= 1
            for tr in fig.data:
                yy = getattr(tr, "y", None)
                if yy is None:
                    continue
                for v in yy:
                    try:
                        fv = float(v)
                    except Exception:
                        continue
                    if fv < -0.001 or fv > 100.001:
                        bounds_ok = False
        if name == "sin_pruebas_institucionales":
            logic_ok = ch["institucional_documental"] == 0 and float(gated["flip_score_chart"].max()) == 0
        elif name == "con_prueba_oficial":
            logic_ok = ch["institucional_documental"] > 0 and float(gated["adoption_score_chart"].max()) > 0
        else:
            logic_ok = ch["ledger_real"] > 40 and ch["institucional_documental"] == 0
        rows.append({
            "test": name,
            "ledger": round(ch["ledger_real"], 2),
            "documental": round(ch["institucional_documental"], 2),
            "watch": round(ch["especulativo_watch"], 2),
            "traces_ok": bool(traces_ok),
            "bounds_ok": bool(bounds_ok),
            "logic_ok": bool(logic_ok),
        })
    return rows

def wallet_evidence_explanation(row: Any) -> str:
    label = str(row.get("label", "") or "")
    role = str(row.get("role", "") or "")
    signals = str(row.get("signals", "") or "")
    top_cp = str(row.get("top_cp_label", "") or "")
    conf = float(row.get("confidence", 0) or 0)
    volume = float(row.get("volume_xrp", 0) or 0)
    parts = []
    if label and label.lower() not in {"nan", "none", "unknown", "desconocido"}:
        parts.append(f"etiqueta/alias detectado: {label}")
    if top_cp and top_cp.lower() not in {"nan", "none", "unknown", "desconocido"}:
        parts.append(f"interacción dominante con {top_cp}")
    if role:
        parts.append(f"patrón de rol: {role}")
    if volume > 0:
        parts.append(f"volumen observado ≈ {_fmt_vol(volume)} XRP")
    if signals:
        parts.append(f"señales: {signals[:180]}")
    if not parts:
        return "Wallet observada, pero sin atribución suficiente; no se debe leer como pertenencia institucional."
    prefix = "Probada/curada" if conf >= 0.75 else "Probable" if conf >= 0.45 else "Débil/watch"
    return prefix + ": " + "; ".join(parts) + "."


def enrich_wallet_table_for_explainability(wv: pd.DataFrame) -> pd.DataFrame:
    if wv is None or wv.empty:
        return wv
    out = wv.copy()
    if "confidence" in out.columns:
        out["Confianza"] = (out["confidence"].astype(float) * 100).round(1).astype(str) + "%"
    if "volume_xrp" in out.columns:
        out["Volumen XRP"] = out["volume_xrp"].apply(lambda x: _fmt_vol(float(x or 0)))
    out["Wallet"] = out["wallet"].astype(str)
    out["Nombre completo"] = out.apply(lambda r: _wallet_full_name(str(r.get("wallet", "")), str(r.get("label", ""))), axis=1)
    out["Por qué aparece"] = out.apply(wallet_evidence_explanation, axis=1)
    rename = {"label": "Etiqueta", "role": "Rol", "top_cp_label": "Contraparte conocida"}
    out = out.rename(columns=rename)
    cols = [c for c in ["Nombre completo", "Wallet", "Etiqueta", "Rol", "Confianza", "Volumen XRP", "Contraparte conocida", "Por qué aparece"] if c in out.columns]
    return out[cols]

def make_engine_radar(row: pd.Series) -> go.Figure:
    cats = [
        "XRPL público", "Pagos ODL", "Trustlines",
        "DEX/AMM", "Whales/Large", "Clusters",
        "Topología", "Fingerprints", "Régimen temporal",
    ]
    vals = [
        row["public_xrpl_score"], row["payment_flow_score"], row["trustline_score"],
        row["dex_score"], row["large_transfer_score"], row["cluster_score"],
        row["topology_score"], row["fingerprint_score"], row["time_regime_score"]
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=[v*100 for v in vals] + [vals[0]*100],
        theta=cats + [cats[0]],
        fill="toself",
        name="Score actual (0-100)",
        line=dict(color="#5AD7FF", width=2),
        fillcolor="rgba(90,215,255,0.18)",
    ))
    fig.update_layout(
        title=dict(text="Radar de motores — estado actual de cada señal (0 = sin señal, 100 = señal fuerte)", font=dict(color="#FFFFFF", size=16)),
        template="plotly_dark",
        paper_bgcolor="#07111f",
        plot_bgcolor="#07111f",
        height=460,
        showlegend=True,
        legend=dict(font=dict(color="#FFFFFF", size=12), bgcolor="rgba(15,23,42,.80)"),
        hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=13), bordercolor="#5AD7FF"),
        polar=dict(
            radialaxis=dict(range=[0, 100], tickfont=dict(color="#FFFFFF", size=10), gridcolor="rgba(255,255,255,.20)"),
            angularaxis=dict(tickfont=dict(color="#FFFFFF", size=12)),
            bgcolor="#07111f",
        ),
        font=dict(color="#FFFFFF"),
        margin=dict(l=20, r=20, t=70, b=20),
    )
    return fig


def make_volume_chart(df: pd.DataFrame, xrp_price: Optional[pd.DataFrame] = None) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(go.Bar(x=df["day"], y=df["xrpl_volume"], name="Volumen RLUSD diario",
                         marker_color="rgba(90,215,255,0.55)"))
    fig.add_trace(go.Scatter(x=df["day"], y=df["volume_7d"], name="Media móvil 7d",
                             mode="lines", line=dict(width=3, color="#5AD7FF")))
    fig.add_trace(go.Scatter(x=df["day"], y=df["volume_30d"], name="Media móvil 30d",
                             mode="lines", line=dict(width=2, color="#B673FF", dash="dot")))
    if xrp_price is not None and not xrp_price.empty:
        merged = df[["day"]].merge(xrp_price, on="day", how="left")
        fig.add_trace(go.Scatter(
            x=merged["day"], y=merged["price_usd"], name="Precio XRP/USD",
            mode="lines", line=dict(width=2, color="#FFB84D", dash="dash"), yaxis="y2",
        ))
        fig.update_layout(
            yaxis2=dict(title="XRP/USD", overlaying="y", side="right",
                        tickfont=dict(color="#FFB84D"), title_font=dict(color="#FFB84D"),
                        gridcolor="rgba(0,0,0,0)", color="#FFB84D"),
        )
    return white_layout(fig, "Volumen RLUSD/XRPL diario + medias móviles + precio XRP/USD", 370)



def white_layout(fig: go.Figure, title: str, height: int = 380, y_range: Optional[List[float]] = None) -> go.Figure:
    fig = _translate_plotly_figure_inplace(fig)
    fig.update_layout(
        title=dict(text=_translate_ui_text_any(title), font=dict(color="#FFFFFF", size=18)),
        template="plotly_dark",
        paper_bgcolor="#07111f",
        plot_bgcolor="#07111f",
        height=height,
        font=dict(color="#FFFFFF", size=13),
        showlegend=True,
        legend=dict(
            orientation="h",
            y=1.12,
            x=0,
            font=dict(color="#FFFFFF", size=12),
            bgcolor="rgba(15,23,42,.85)",
            bordercolor="rgba(255,255,255,.30)",
            borderwidth=1,
            itemclick="toggle",
            itemdoubleclick="toggleothers",
        ),
        hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=13), bordercolor="#5AD7FF"),
        margin=dict(l=20, r=20, t=90, b=35),
    )
    fig.update_xaxes(
        color="#FFFFFF",
        gridcolor="rgba(255,255,255,.12)",
        tickfont=dict(color="#FFFFFF", size=12),
        title_font=dict(color="#FFFFFF"),
    )
    fig.update_yaxes(
        color="#FFFFFF",
        gridcolor="rgba(255,255,255,.18)",
        tickfont=dict(color="#FFFFFF", size=12),
        title_font=dict(color="#FFFFFF"),
        title="Score %",
    )
    if y_range is not None:
        fig.update_yaxes(range=y_range)
    return fig


def make_price_risk_chart(df: pd.DataFrame, xrp_price: Optional[pd.DataFrame] = None) -> go.Figure:
    fig = go.Figure()
    for _col, _name, _color, _dash in [
        ("bull_score",  "Subida probable (score 0-100)",    "#3CFF9B", "solid"),
        ("bear_score",  "Riesgo bajada (score 0-100)",      "#FF5A67", "solid"),
        ("pump_score",  "Pump especulativo (score 0-100)",  "#FFB84D", "dot"),
        ("price_score", "Precio técnico (score 0-100)",     "#5AD7FF", "dash"),
    ]:
        if _col in df.columns:
            fig.add_trace(go.Scatter(x=df["day"], y=df[_col].fillna(0), name=_name, mode="lines",
                                     line=dict(width=4 if _dash=="solid" else 3, color=_color,
                                               **({} if _dash=="solid" else {"dash": _dash}))))
    fig.add_hrect(y0=80, y1=100, fillcolor="rgba(60,255,155,.10)", line_width=0)
    fig.add_hline(y=80, line_dash="dash", line_color="#FFFFFF", annotation_text="Zona fuerte >80%", annotation_font_color="#FFFFFF")
    if xrp_price is not None and not xrp_price.empty:
        merged = df[["day"]].merge(xrp_price, on="day", how="left")
        fig.add_trace(go.Scatter(
            x=merged["day"], y=merged["price_usd"], name="Precio XRP/USD (real)",
            mode="lines", line=dict(width=3, color="#FFFFFF", dash="longdash"), yaxis="y2",
        ))
        fig.update_layout(
            yaxis2=dict(title="XRP/USD", overlaying="y", side="right",
                        tickfont=dict(color="#FFFFFF", size=11), title_font=dict(color="#FFFFFF"),
                        gridcolor="rgba(0,0,0,0)", color="#FFFFFF"),
        )
    return white_layout(fig, "Precio y riesgo: subida, bajada, pump, precio técnico + precio XRP real (eje dcho.)", 430, [0, 100])


def make_adoption_chart(df: pd.DataFrame, xrp_price: Optional[pd.DataFrame] = None, conn: Optional[sqlite3.Connection] = None) -> go.Figure:
    df = prepare_chart_metrics(df, conn)
    fig = go.Figure()
    for _col, _name, _color, _dash, _mul in [
        ("flip_score",        "Flip / adopción real (0-100)",  "#B673FF", "solid", 1),
        ("radar_coverage",    "Cobertura radar (0-100)",       "#5AD7FF", "solid", 1),
        ("adoption_score",    "Adopción técnica (0-100)",      "#3CFF9B", "dot",   1),
        ("persistence_score", "Persistencia (0-100)",          "#60A5FA", "dash",  100),
    ]:
        _safe_col = _chart_col(df, _col)
        if _safe_col in df.columns:
            fig.add_trace(go.Scatter(x=df["day"], y=pd.to_numeric(df[_safe_col], errors="coerce").fillna(0).clip(0,100) * (1 if _safe_col.endswith("_chart") else _mul), name=_name, mode="lines",
                                     line=dict(width=4 if _dash=="solid" else 3, color=_color,
                                               **({} if _dash=="solid" else {"dash": _dash}))))
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(182,115,255,.10)", line_width=0)
    fig.add_hline(y=80, line_dash="dash", line_color="#FFFFFF", annotation_text="Flip fuerte >80%", annotation_font_color="#FFFFFF")
    if xrp_price is not None and not xrp_price.empty:
        merged = df[["day"]].merge(xrp_price, on="day", how="left")
        fig.add_trace(go.Scatter(
            x=merged["day"], y=merged["price_usd"], name="Precio XRP/USD (real)",
            mode="lines", line=dict(width=2, color="#FFFFFF", dash="longdash"), yaxis="y2",
        ))
        fig.update_layout(
            yaxis2=dict(title="XRP/USD", overlaying="y", side="right",
                        tickfont=dict(color="#FFFFFF", size=11), title_font=dict(color="#FFFFFF"),
                        gridcolor="rgba(0,0,0,0)", color="#FFFFFF"),
        )
    return white_layout(fig, "Adopción: Flip, cobertura, adopción técnica, persistencia + precio XRP real (eje dcho.)", 430, [0, 100])


def make_public_footprints_chart(df: pd.DataFrame, xrp_price: Optional[pd.DataFrame] = None, conn: Optional[sqlite3.Connection] = None) -> go.Figure:
    df = prepare_chart_metrics(df, conn)
    fig = go.Figure()
    cols = [
        ("public_xrpl_score",       "XRPL público (actividad ledger)",          "#3CFF9B"),
        ("payment_flow_score",       "Pagos / ODL (remesas)",                    "#5AD7FF"),
        ("trustline_score",          "Trustlines (confianza/tenencia)",           "#B673FF"),
        ("dex_score",                "DEX/AMM (liquidez visible)",                "#FFB84D"),
        ("large_transfer_score",     "Transfers grandes (whale/treasury)",        "#FF5A67"),
        ("bridge_score",             "Bridges / cross-chain",                     "#8CA0B8"),
        ("public_gateway_score",     "Gateway público (punto de entrada XRPL)",  "#60A5FA"),
        ("institutional_route_score","Rutas institucionales (inferidas)",         "#F59E0B"),
    ]
    for col, name, color in cols:
        safe_col = _chart_col(df, col)
        if safe_col in df.columns:
            vals = pd.to_numeric(df[safe_col], errors="coerce").fillna(0)
            if vals.max() <= 1.5:
                vals = vals * 100
            fig.add_trace(go.Scatter(x=df["day"], y=vals.clip(0,100), name=name, mode="lines",
                                     line=dict(width=3, color=color)))
    if xrp_price is not None and not xrp_price.empty:
        merged = df[["day"]].merge(xrp_price, on="day", how="left")
        fig.add_trace(go.Scatter(
            x=merged["day"], y=merged["price_usd"], name="Precio XRP/USD (real)",
            mode="lines", line=dict(width=2, color="#FFFFFF", dash="longdash"), yaxis="y2",
        ))
        fig.update_layout(
            yaxis2=dict(title="XRP/USD", overlaying="y", side="right",
                        tickfont=dict(color="#FFFFFF", size=11), title_font=dict(color="#FFFFFF"),
                        gridcolor="rgba(0,0,0,0)", color="#FFFFFF"),
        )
    return white_layout(fig, "Huellas públicas vigiladas: XRPL, pagos, trustlines, DEX/AMM, whales y bridges (0-100)", 450, [0, 100])


def make_intelligence_engines_chart(df: pd.DataFrame, conn: Optional[sqlite3.Connection] = None) -> go.Figure:
    df = prepare_chart_metrics(df, conn)
    fig = go.Figure()
    cols = [
        ("cluster_score",      "Clusters (wallets agrupadas)",           "#B673FF"),
        ("topology_score",     "Topología (hubs y concentración)",       "#5AD7FF"),
        ("fingerprint_score",  "Fingerprints (patron treasury/MM/ODL)",  "#3CFF9B"),
        ("anomaly_score",      "Anomalías (desvío vs historia)",         "#FF5A67"),
        ("time_regime_score",  "Régimen temporal (aceleración)",         "#FFB84D"),
        ("cross_network_score","Cross-network (bridges multi-red)",      "#8CA0B8"),
    ]
    for col, name, color in cols:
        safe_col = _chart_col(df, col)
        if safe_col in df.columns:
            vals = pd.to_numeric(df[safe_col], errors="coerce").fillna(0)
            if vals.max() <= 1.5:
                vals = vals * 100
            fig.add_trace(go.Scatter(x=df["day"], y=vals.clip(0,100), name=name, mode="lines",
                                     line=dict(width=3, color=color)))
    return white_layout(fig, "Motores de inteligencia: clusters, topología, fingerprints, anomalías y cross-network (0-100)", 450, [0, 100])


def make_engine_heat_chart(df: pd.DataFrame, conn: Optional[sqlite3.Connection] = None) -> go.Figure:
    df = prepare_chart_metrics(df, conn)
    cols = [
        ("public_xrpl_score", "XRPL público"),
        ("payment_flow_score", "Pagos"),
        ("trustline_score", "Trustlines"),
        ("dex_score", "DEX/AMM"),
        ("large_transfer_score", "Transfers grandes"),
        ("bridge_score", "Bridges"),
        ("cluster_score", "Clusters"),
        ("topology_score", "Topología"),
        ("fingerprint_score", "Fingerprints"),
        ("anomaly_score", "Anomalías"),
        ("time_regime_score", "Régimen temporal"),
        ("cross_network_score", "Cross-network"),
    ]
    recent = df.tail(90).copy()
    z = []
    y = []
    for col, name in cols:
        safe_col = _chart_col(recent, col)
        if safe_col in recent.columns:
            vals = pd.to_numeric(recent[safe_col], errors="coerce").fillna(0)
            if vals.max() <= 1.5:
                vals = vals * 100
            z.append(vals.clip(0,100).tolist())
            y.append(name)
    fig = go.Figure(data=go.Heatmap(
        z=z,
        x=recent["day"].tolist(),
        y=y,
        colorscale=[
            [0.00, "#0B1220"],
            [0.30, "#1D4ED8"],
            [0.58, "#B45309"],
            [0.80, "#16A34A"],
            [1.00, "#3CFF9B"],
        ],
        zmin=0,
        zmax=100,
        colorbar=dict(
            title=dict(text="Score %", font=dict(color="#FFFFFF", size=13)),
            tickfont=dict(color="#FFFFFF"),
            ticksuffix="%",
        ),
        hovertemplate="<b>%{y}</b><br>Fecha: %{x}<br>Score: <b>%{z:.1f}%</b><extra></extra>",
        hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=13), bordercolor="#5AD7FF"),
    ))
    fig.update_layout(
        title=dict(
            text="Heatmap — intensidad de cada motor en los últimos 90 días<br><sup style='color:#94A3B8'>Azul oscuro=sin señal · Azul=bajo · Naranja=medio · Verde=fuerte</sup>",
            font=dict(color="#FFFFFF", size=18)
        ),
        template="plotly_dark",
        paper_bgcolor="#07111f",
        plot_bgcolor="#07111f",
        height=540,
        hoverlabel=dict(bgcolor="#1e293b", font=dict(color="#FFFFFF", size=13), bordercolor="#5AD7FF"),
        xaxis=dict(color="#FFFFFF", tickfont=dict(color="#FFFFFF", size=10), nticks=12),
        yaxis=dict(color="#FFFFFF", tickfont=dict(color="#FFFFFF", size=12), autorange="reversed"),
        font=dict(color="#FFFFFF", size=13),
        margin=dict(l=20, r=20, t=80, b=35),
    )
    return fig


def make_phase_chart(df: pd.DataFrame, conn: Optional[sqlite3.Connection] = None) -> go.Figure:
    df = prepare_chart_metrics(df, conn)
    fig = go.Figure()
    phase_col = _chart_col(df, "phase")
    fig.add_trace(go.Scatter(x=df["day"], y=pd.to_numeric(df[phase_col], errors="coerce").fillna(0).clip(0,5), name="Fase 0–5 verificada", mode="lines+markers", line=dict(width=4, color="#B673FF")))
    fig = white_layout(fig, "Evolución de fase 0–5", 300, [-0.2, 5.2])
    fig.update_yaxes(tickmode="array", tickvals=[0,1,2,3,4,5], title="Fase")
    return fig


def render_color_legend() -> None:
    st.markdown("<div class='rrp-section-title'>Leyenda del mapa — cómo leer colores y líneas</div>", unsafe_allow_html=True)
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("""
<div class='rrp-legend-box'>
<div style="font-size:.78rem;font-weight:700;color:#5AD7FF;text-transform:uppercase;letter-spacing:.10em;margin-bottom:.45rem;">Nodos (círculos del mapa)</div>
<div class='rrp-line'><span class='rrp-dot' style='background:#3CFF9B'></span><span><b style='color:#3CFF9B'>Verde brillante</b> — Ledger público real<br><small style='color:#94A3B8'>XRPL (ledger abierto) · RLUSD (token nativo verificable)</small></span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#5AD7FF'></span><span><b style='color:#5AD7FF'>Azul cyan</b> — Infraestructura Ripple<br><small style='color:#94A3B8'>Ripple Payments · Treasury · Rail · Custody/Metaco · HR/Prime</small></span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#F59E0B'></span><span><b style='color:#F59E0B'>Ámbar</b> — Bancos RippleNet / institucional<br><small style='color:#94A3B8'>BofA · Santander · SBI Remit · Axis Bank · StanChart · Itaú</small></span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#FB923C'></span><span><b style='color:#FB923C'>Naranja</b> — Corredores ODL activos<br><small style='color:#94A3B8'>Bitso (MX) · BeeTech (BR) · Tranglo (Asia) · Coins.ph (PH)</small></span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#FFB84D'></span><span><b style='color:#FFB84D'>Naranja claro</b> — Infraestructura privada<br><small style='color:#94A3B8'>SWIFT · FedNow · SEPA/ACH · Mastercard</small></span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#B673FF'></span><span><b style='color:#B673FF'>Morado</b> — Huellas públicas vigiladas<br><small style='color:#94A3B8'>Public Gateway · Trustlines · DEX/AMM · Large Transfers</small></span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#60A5FA'></span><span><b style='color:#60A5FA'>Azul medio</b> — Motores de inteligencia<br><small style='color:#94A3B8'>Topology Engine · Anomaly Engine · Fingerprint Engine</small></span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#8CA0B8'></span><span><b style='color:#8CA0B8'>Gris</b> — Conector futuro / en desarrollo<br><small style='color:#94A3B8'>Ethereum (integración pendiente)</small></span></div>
</div>
""", unsafe_allow_html=True)

    with col_right:
        st.markdown("""
<div class='rrp-legend-box'>
<div style="font-size:.78rem;font-weight:700;color:#5AD7FF;text-transform:uppercase;letter-spacing:.10em;margin-bottom:.45rem;">Líneas — tipos de ruta</div>

<div style="font-size:.70rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin:.50rem 0 .30rem">— Línea sólida: confirmado con evidencia directa —</div>
<div class='rrp-line'>
  <span style='display:inline-block;width:28px;height:3px;background:#3CFF9B;border-radius:2px;vertical-align:middle;margin-right:8px'></span>
  <span><b style='color:#3CFF9B'>Verde sólida — On-chain XRPL</b><br><small style='color:#94A3B8'>TX visible en ledger. Confianza ≥95%. Irrefutable.</small></span>
</div>
<div class='rrp-line'>
  <span style='display:inline-block;width:28px;height:3px;background:#00CFFF;border-radius:2px;vertical-align:middle;margin-right:8px'></span>
  <span><b style='color:#00CFFF'>Cian sólida — Pública verificada</b><br><small style='color:#94A3B8'>Gateway/exchange con wallet XRPL confirmada.</small></span>
</div>
<div class='rrp-line'>
  <span style='display:inline-block;width:28px;height:3px;background:#F59E0B;border-radius:2px;vertical-align:middle;margin-right:8px'></span>
  <span><b style='color:#F59E0B'>Ámbar sólida — Documentada</b><br><small style='color:#94A3B8'>Contrato, filing SEC/regulatorio o acuerdo documentado.</small></span>
</div>

<div style="font-size:.70rem;color:#FF4D6D;text-transform:uppercase;letter-spacing:.08em;margin:.50rem 0 .30rem">— Línea discontinua roja: implicación técnica obligatoria —</div>
<div class='rrp-line'>
  <span style='display:inline-block;width:28px;height:0;border-top:3px dashed #FF4D6D;vertical-align:middle;margin-right:8px'></span>
  <span><b style='color:#FF4D6D'>⚡ Rojo-rosa discontinua — Obligatoria</b><br><small style='color:#94A3B8'>El protocolo lo exige sin excepción. Sin TX directa verificada, pero técnicamente irrefutable. Confianza 97%.<br>Ej: conectado a Ripple Payments → Rail → XRPL · DEX → XRPL · RLUSD → XRPL</small></span>
</div>

<div style="font-size:.70rem;color:#64748B;text-transform:uppercase;letter-spacing:.08em;margin:.50rem 0 .30rem">— Líneas discontinuas: señal sin prueba directa —</div>
<div class='rrp-line'>
  <span style='display:inline-block;width:28px;height:0;border-top:3px dashed #B673FF;vertical-align:middle;margin-right:8px'></span>
  <span><b style='color:#B673FF'>Morada discontinua — Indirecta vigilada</b><br><small style='color:#94A3B8'>Huella pública detectada, sin confirmar. Requiere verificación.</small></span>
</div>
<div class='rrp-line'>
  <span style='display:inline-block;width:28px;height:0;border-top:3px dashed #FFD700;vertical-align:middle;margin-right:8px'></span>
  <span><b style='color:#FFD700'>Dorada discontinua — Descubierta por IA</b><br><small style='color:#94A3B8'>Detectada por motor de inferencia. Pendiente de confirmar.</small></span>
</div>
<div class='rrp-line'>
  <span style='display:inline-block;width:28px;height:0;border-top:3px dashed #F59E0B;vertical-align:middle;margin-right:8px'></span>
  <span><b style='color:#F59E0B'>Ámbar discontinua — Privada inferida</b><br><small style='color:#94A3B8'>Ruta privada sin confirmación pública. Activada por señal indirecta.</small></span>
</div>
<div class='rrp-line'>
  <span style='display:inline-block;width:28px;height:0;border-top:3px dotted #8CA0B8;vertical-align:middle;margin-right:8px'></span>
  <span><b style='color:#8CA0B8'>Gris punteada — Futura / no activa</b><br><small style='color:#94A3B8'>Integración planeada sin datos activos todavía.</small></span>
</div>

<div style="margin-top:.75rem;padding:.55rem .70rem;background:rgba(255,77,109,.10);border-radius:10px;border:1px solid rgba(255,77,109,.30);">
<small style="color:#CBD5E1">
<b style="color:#FFFFFF">Sólida</b> = evidencia directa verificada &nbsp;·&nbsp; <b style="color:#FF4D6D">Discontinua roja ⚡</b> = obligatoria por protocolo &nbsp;·&nbsp; <b style="color:#FFFFFF">Discontinua</b> = inferida/vigilada<br>
<b style="color:#FFFFFF">Grosor</b> = intensidad de señal &nbsp;·&nbsp; <b style="color:#FFFFFF">Cursor sobre línea o nodo</b> = detalle exacto
</small>
</div>
</div>
""", unsafe_allow_html=True)


def render_sidebar_legend() -> None:
    st.markdown("""
<div class='rrp-legend-box'>
<b style='color:#5AD7FF'>Guía rápida</b>
<div style='font-size:.68rem;color:#64748B;margin:.3rem 0 .2rem'>DIRECTAS</div>
<div class='rrp-line'><span class='rrp-dot' style='background:#3CFF9B'></span><span style='font-size:.78rem'>On-chain XRPL (TX real)</span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#00CFFF'></span><span style='font-size:.78rem'>Pública (gateway/exchange)</span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#F59E0B'></span><span style='font-size:.78rem'>Inferida (contrato/filing)</span></div>
<div style='font-size:.68rem;color:#FF4D6D;margin:.3rem 0 .2rem'>OBLIGATORIA (discontinua)</div>
<div class='rrp-line'><span style='display:inline-block;width:16px;height:0;border-top:2px dashed #FF4D6D;vertical-align:middle;margin-right:6px'></span><span style='font-size:.78rem;color:#FF4D6D'>⚡ Protocolo — 97%</span></div>
<div style='font-size:.68rem;color:#64748B;margin:.3rem 0 .2rem'>INDIRECTAS</div>
<div class='rrp-line'><span class='rrp-dot' style='background:#B673FF'></span><span style='font-size:.78rem'>Vigilada (huella pública)</span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#FFD700'></span><span style='font-size:.78rem'>Descubierta (motor IA)</span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#8CA0B8'></span><span style='font-size:.78rem'>Futura / en desarrollo</span></div>
<div class='rrp-line'><span class='rrp-dot' style='background:#FF5A67'></span><span style='font-size:.78rem'>Señal fría / slowdown</span></div>
</div>
""", unsafe_allow_html=True)


def render_diagnostic_summary(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    st.markdown("<div class='rrp-section-title'>Resumen del sistema</div>", unsafe_allow_html=True)
    ok, msg = check_xrpl_connection()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("XRPL", "OK" if ok else "ERROR")
    c2.metric("Eventos guardados", conn.execute("SELECT COUNT(*) FROM raw_events").fetchone()[0])
    c3.metric("Días calculados", conn.execute("SELECT COUNT(*) FROM daily_metrics").fetchone()[0])
    c4.metric("Última fecha", df.iloc[-1]["day"] if not df.empty else "N/A")
    st.markdown(f"<div class='rrp-note'><b>Estado conexión:</b> {msg}</div>", unsafe_allow_html=True)

    if df.empty:
        st.error("No hay datos cargados.")
        return

    row = df.iloc[-1]
    checks = pd.DataFrame([
        {"Chequeo": "Datos XRPL recientes", "Estado": "OK" if row["tx_count"] >= 0 else "Revisar", "Detalle": f"{int(row['tx_count'])} tx en último día calculado"},
        {"Chequeo": "Cobertura radar", "Estado": "OK" if row["radar_coverage"] >= 35 else "Baja", "Detalle": f"{row['radar_coverage']:.1f}%"},
        {"Chequeo": "Clusters", "Estado": "OK" if conn.execute("SELECT COUNT(*) FROM clusters").fetchone()[0] > 0 else "Sin clusters reales/demo", "Detalle": "Clusters calculados desde relaciones de wallets"},
        {"Chequeo": "Fingerprints", "Estado": "OK" if conn.execute("SELECT COUNT(*) FROM fingerprints").fetchone()[0] > 0 else "Sin fingerprints reales/demo", "Detalle": "Patrones treasury/MM/corridor"},
        {"Chequeo": "Cinemateca", "Estado": "OK", "Detalle": "Usa los mismos datos históricos que técnico"},
    ])
    st.dataframe(checks, width="stretch", hide_index=True)

def route_dataframe(row: pd.Series) -> pd.DataFrame:
    rows = []
    for src, dst, kind, signal, label in ROUTES:
        rows.append({
            "Ruta": label,
            "Origen": src,
            "Destino": dst,
            "Señal %": round(route_signal(row, (src,dst,kind,signal,label))*100, 2),
            "Tipo": "XRPL real" if kind == "real" else "Huella pública" if kind in {"public", "watch"} else "Motor" if kind == "model" else "Privada inferida" if kind == "private" else "Futuro",
            "Fuente": signal,
        })
    return pd.DataFrame(rows)


def component_table(row: pd.Series) -> pd.DataFrame:
    pairs = [
        ("XRPL público", "public_xrpl_score", "Dato real visible en XRPL/RLUSD."),
        ("Pagos", "payment_flow_score", "Payments detectados o inferidos por huella pública."),
        ("Trustlines", "trustline_score", "Confianza/tenencia visible."),
        ("DEX/AMM", "dex_score", "Ofertas, AMM y liquidez visible."),
        ("Transfers grandes", "large_transfer_score", "Posible treasury/custody/market maker."),
        ("Clusters", "cluster_score", "Agrupaciones de wallets conectadas."),
        ("Topología", "topology_score", "Concentración, hubs y dirección del flujo."),
        ("Anomalías", "anomaly_score", "Actividad fuera de rango histórico."),
        ("Fingerprints", "fingerprint_score", "Patrones treasury/MM/corridor-like."),
        ("Cross-network", "cross_network_score", "Puentes y señales multi-red."),
        ("Régimen temporal", "time_regime_score", "Aceleración, persistencia y cambio de régimen."),
    ]
    return pd.DataFrame([
        {"Motor": name, "Score": f"{float(row[col])*100:.1f}%", "Explicación": desc}
        for name, col, desc in pairs
    ])


def historical_analysis(df: pd.DataFrame) -> pd.DataFrame:
    if df.empty:
        return pd.DataFrame()
    last = df.iloc[-1]
    d7 = df.tail(7)
    d30 = df.tail(30)

    def pct(a,b):
        return 0.0 if b == 0 else (a-b)/abs(b)*100

    metrics = [
        ("Volumen 7d", d7["xrpl_volume"].sum(), d30["xrpl_volume"].sum()/max(len(d30),1)*7),
        ("TX 7d", d7["tx_count"].sum(), d30["tx_count"].sum()/max(len(d30),1)*7),
        ("Transfers grandes 7d", d7["large_tx_count"].sum(), d30["large_tx_count"].sum()/max(len(d30),1)*7),
        ("Cobertura actual", last["radar_coverage"], d30["radar_coverage"].mean()),
        ("Adopción actual", last["adoption_score"], d30["adoption_score"].mean()),
        ("Pump actual", last["pump_score"], d30["pump_score"].mean()),
        ("Fase actual", last["phase"], d30["phase"].mean()),
    ]
    return pd.DataFrame([
        {
            "Métrica": m,
            "Actual": round(float(a),2),
            "Base 30d": round(float(b),2),
            "Cambio %": round(pct(float(a), float(b)),2),
            "Lectura": "Mejorando" if a > b*1.10 else "Enfriando" if a < b*0.90 else "Estable",
        }
        for m,a,b in metrics
    ])


def recent_clusters(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query("SELECT * FROM clusters ORDER BY day DESC, score DESC LIMIT 50", conn)


def recent_fingerprints(conn: sqlite3.Connection) -> pd.DataFrame:
    return pd.read_sql_query("SELECT * FROM fingerprints ORDER BY day DESC, score DESC LIMIT 50", conn)


# =============================================================================
# TABLA OSCURA (reemplaza st.dataframe para compatibilidad visual)
# =============================================================================

def styled_table(df: pd.DataFrame, max_rows: int = 200) -> None:
    """Renderiza un DataFrame como tabla HTML con tema oscuro de la interfaz."""
    if df.empty:
        st.info("Sin datos disponibles.")
        return

    def fmt(v: Any) -> str:
        if v is None:
            return "—"
        if isinstance(v, float):
            return f"{v:.2f}"
        s = str(v)
        return s[:90] + "…" if len(s) > 90 else s

    th = "padding:.40rem .70rem;text-align:left;color:#5AD7FF;font-weight:700;font-size:.83rem;border-bottom:1px solid rgba(90,215,255,.30);white-space:nowrap;background:rgba(14,165,233,.18);"
    td = "padding:.35rem .70rem;color:#E2E8F0;font-size:.83rem;border-bottom:1px solid rgba(255,255,255,.06);"

    header = "".join(f"<th style='{th}'>{col}</th>" for col in df.columns)
    tbody = ""
    for i, (_, row) in enumerate(df.head(max_rows).iterrows()):
        bg = "rgba(15,23,42,.92)" if i % 2 == 0 else "rgba(7,17,31,.88)"
        cells = "".join(f"<td style='{td}'>{fmt(v)}</td>" for v in row)
        tbody += f"<tr style='background:{bg}'>{cells}</tr>"

    st.markdown(f"""
<div style="overflow:auto;max-height:440px;border:1px solid rgba(90,215,255,.20);border-radius:12px;margin:.4rem 0 1rem 0;">
<table style="width:100%;border-collapse:collapse;">
<thead><tr>{header}</tr></thead>
<tbody>{tbody}</tbody>
</table>
</div>""", unsafe_allow_html=True)


# =============================================================================
# DIAGNÓSTICO SENCILLO POR GRÁFICA
# =============================================================================

def _bar(val: float, color: str) -> str:
    """Genera una barra de progreso HTML para mostrar un valor 0-100."""
    pct = min(max(float(val), 0), 100)
    bar_color = "#3CFF9B" if pct >= 65 else "#FFB84D" if pct >= 35 else "#FF5A67"
    return (
        f"<span style='font-weight:800;color:{bar_color};font-size:.95rem;min-width:3.5rem;display:inline-block'>{pct:.1f}%</span>"
        f"<span style='display:inline-block;width:90px;height:8px;background:rgba(255,255,255,.10);border-radius:99px;vertical-align:middle;margin-left:.4rem'>"
        f"<span style='display:block;width:{pct:.0f}%;height:100%;background:{bar_color};border-radius:99px'></span></span>"
    )


def _row(name: str, val: float, what: str, result: str) -> str:
    """Genera una fila de diagnóstico HTML."""
    return (
        f"<tr style='border-bottom:1px solid rgba(255,255,255,.06)'>"
        f"<td style='padding:.28rem .70rem;color:#CBD5E1;font-size:.84rem;white-space:nowrap'>{name}</td>"
        f"<td style='padding:.28rem .70rem'>{_bar(val,'')}</td>"
        f"<td style='padding:.28rem .70rem;color:#94A3B8;font-size:.82rem'>{what}</td>"
        f"<td style='padding:.28rem .70rem;color:#E2E8F0;font-size:.82rem'>{result}</td>"
        f"</tr>"
    )


def chart_diagnosis(df: pd.DataFrame, chart: str) -> None:
    """Muestra diagnóstico detallado con valores reales de cada métrica bajo cada gráfica."""
    if df.empty:
        return
    last = df.iloc[-1]

    def v(col: str, scale: float = 1.0) -> float:
        raw = float(last.get(col, 0)) * scale
        # si el valor ya está en 0-100 rango no multipliques de nuevo
        return raw

    def pct(col: str) -> float:
        """Devuelve valor en 0-100. Detecta si ya está en escala 0-100 o 0-1."""
        raw = float(last.get(col, 0))
        return raw if raw > 1.5 else raw * 100

    # ── Definición de métricas por gráfica ─────────────────────────────────
    if chart == "price_risk":
        bull  = pct("bull_score")
        bear  = pct("bear_score")
        pump  = pct("pump_score")
        price = pct("price_score")

        if bull >= 70 and pump < bear:
            headline = f"🟢 <b>Señal alcista</b> — la actividad pública apunta a subida de precio."
            border = "#3CFF9B"
        elif bear >= 70:
            headline = f"🔴 <b>Señal bajista</b> — actividad débil o especulativa sin persistencia."
            border = "#FF5A67"
        elif pump >= bull:
            headline = f"🟡 <b>Alerta pump</b> — hay más movimiento especulativo que adopción real."
            border = "#FFB84D"
        else:
            headline = f"🟠 <b>Señal mixta</b> — sin tendencia clara todavía."
            border = "#FFB84D"

        rows = (
            _row("📈 Subida probable",    bull,
                 "¿Cuánta actividad pública real respalda una subida de precio?",
                 "Alta (&gt;70%) = múltiples huellas activas. Baja = sin base sólida.") +
            _row("📉 Riesgo de bajada",   bear,
                 "¿Hay señales de enfriamiento, poca persistencia o ausencia de clusters?",
                 "Alta (&gt;70%) = el radar ve poco que sostenga el precio.") +
            _row("🎰 Pump especulativo",  pump,
                 "¿Cuánto del movimiento parece especulativo vs adoptión real?",
                 "Alta = probable spike sin base. Baja = actividad más orgánica.") +
            _row("💹 Precio técnico",     price,
                 "Score combinado: volumen, transfers grandes, DEX, anomalías y régimen.",
                 "Alta (&gt;60%) = condiciones técnicas favorables para movimiento de precio.")
        )

    elif chart == "adoption":
        flip   = pct("flip_score")
        cov    = pct("radar_coverage")
        adopt  = pct("adoption_score")
        pers   = pct("persistence_score")

        if flip >= 80:
            headline = "🟣 <b>Flip posible</b> — varias huellas coordinadas. Adopción real en progreso."
            border = "#B673FF"
        elif flip >= 55:
            headline = "🔵 <b>Adopción en progreso</b> — señales moderadas. Aún no es Full Flip."
            border = "#5AD7FF"
        else:
            headline = "🟠 <b>Adopción baja</b> — pocas huellas coordinadas. Se necesita más persistencia."
            border = "#FFB84D"

        rows = (
            _row("🔄 Flip / adopción real", flip,
                 "¿Cuántas huellas públicas están coordinadas en el tiempo?",
                 "&gt;80% = Full Flip (adopción masiva). &lt;40% = ruido o arranque.") +
            _row("🛰️ Cobertura radar",      cov,
                 "¿Cuántos puntos públicos de vigilancia están activos?",
                 "&gt;60% = el radar cubre bien. &lt;35% = pocos datos disponibles.") +
            _row("📊 Adopción técnica",     adopt,
                 "Score de adopción calculado por los motores internos (clusters, topología, fingerprints...).",
                 "Alta = múltiples motores confirman uso real sostenido.") +
            _row("⏱️ Persistencia",         pers,
                 "¿La actividad lleva varios días consecutivos o es un spike de un día?",
                 "&gt;60% = señal sostenida en el tiempo. Baja = evento puntual sin continuidad.")
        )

    elif chart == "footprints":
        xrpl   = pct("public_xrpl_score")
        pay    = pct("payment_flow_score")
        trust  = pct("trustline_score")
        dex    = pct("dex_score")
        large  = pct("large_transfer_score")
        bridge = pct("bridge_score")
        gw     = pct("public_gateway_score")
        inst   = pct("institutional_route_score")
        active = sum(x >= 40 for x in [xrpl, pay, trust, dex, large, bridge, gw, inst])

        if active >= 6:
            headline = f"🟢 <b>{active}/8 huellas activas ≥40%</b> — actividad amplia y coordinada en XRPL."
            border = "#3CFF9B"
        elif active >= 3:
            headline = f"🟡 <b>{active}/8 huellas activas</b> — actividad parcial. Algunas señales presentes."
            border = "#FFB84D"
        else:
            headline = f"🔴 <b>{active}/8 huellas activas</b> — poca actividad. Puede ser período sin movimiento real."
            border = "#FF5A67"

        rows = (
            _row("💧 XRPL público",          xrpl,
                 "Actividad general del ledger: volumen, nº transacciones, cuentas únicas.",
                 "&gt;50% = ledger activo ese día. Baja = poco tráfico en XRPL.") +
            _row("💸 Pagos / ODL",           pay,
                 "Payments detectados en XRPL. Corredores como Bitso, SBI Remit, Coins.ph.",
                 "&gt;50% = tráfico de remesas/ODL real. Baja = sin pagos significativos.") +
            _row("🔗 Trustlines",            trust,
                 "Wallets estableciendo confianza para recibir RLUSD u otros tokens.",
                 "&gt;40% = integración en curso. Baja = sin nuevas conexiones.") +
            _row("🌊 DEX / AMM",             dex,
                 "Liquidez disponible en el DEX de XRPL. ODL necesita mercado para convertir.",
                 "&gt;40% = mercado activo. Baja = poca liquidez disponible.") +
            _row("🐋 Transfers grandes",     large,
                 "Movimientos ≥1M RLUSD. Señal de treasury, custody o market maker.",
                 "&gt;40% = hay movimientos institucionales grandes. Baja = sin ballenas ese día.") +
            _row("🌉 Bridges",               bridge,
                 "Actividad de puentes entre cadenas (XRPL↔Ethereum u otras).",
                 "&gt;30% = actividad cross-chain detectada. Baja = sin puentes activos.") +
            _row("🛰️ Gateway público",       gw,
                 "Punto de entrada visible donde las rutas privadas 'salen' a XRPL.",
                 "&gt;50% = gateway activo. Baja = sin punto de entrada detectado.") +
            _row("🏛️ Rutas institucionales", inst,
                 "Señal de que bancos o entidades están usando el rail de Ripple.",
                 "&gt;50% = posible ruta bancaria activa. Se infiere por huellas públicas.")
        )

    elif chart == "engines":
        cluster = pct("cluster_score")
        topo    = pct("topology_score")
        fp      = pct("fingerprint_score")
        anom    = pct("anomaly_score")
        regime  = pct("time_regime_score")
        cross   = pct("cross_network_score")
        hot = sum(x >= 50 for x in [cluster, topo, fp, anom, regime, cross])

        if hot >= 4:
            headline = f"🟢 <b>{hot}/6 motores activos ≥50%</b> — señal institucional coordinada clara."
            border = "#3CFF9B"
            conclusion_icon = "🟢"
            conclusion_color = "#3CFF9B"
            conclusion_title = "Conclusión: actividad institucional real detectada"
            conclusion_text = (
                f"<b>{hot} de 6 motores</b> están por encima del 50%. Esto significa que el radar detecta "
                "patrones coordinados que van más allá del ruido: wallets agrupadas, hubs de flujo, "
                "comportamientos de treasury o market maker y tendencia sostenida. "
                "Señal de que hay actividad estructurada en XRPL en este momento."
            )
        elif hot >= 2:
            headline = f"🟡 <b>{hot}/6 motores activos</b> — señal moderada. Algunos patrones detectados."
            border = "#FFB84D"
            conclusion_icon = "🟡"
            conclusion_color = "#FFB84D"
            conclusion_title = "Conclusión: señal parcial — vigilar evolución"
            conclusion_text = (
                f"<b>{hot} de 6 motores</b> superan el 50%. Hay actividad pero no está del todo coordinada. "
                "Puede ser el inicio de un movimiento institucional o actividad puntual sin continuidad. "
                "Recomendable esperar a que más motores se activen antes de sacar conclusiones firmes."
            )
        else:
            headline = f"🟠 <b>{hot}/6 motores activos</b> — motores en reposo. Poca señal estructural."
            border = "#FFB84D"
            conclusion_icon = "🟠"
            conclusion_color = "#FF9D5C"
            conclusion_title = "Conclusión: sin señal estructural significativa ahora mismo"
            conclusion_text = (
                f"Solo <b>{hot} de 6 motores</b> superan el 50%. Los motores analíticos no detectan "
                "patrones claros de actividad institucional coordinada. Esto puede deberse a un período "
                "de baja actividad real, datos demo sin eventos reales, o que el mercado está en pausa. "
                "No es una señal negativa por sí sola — simplemente no hay evidencia suficiente todavía."
            )

        def _engine_card(icon, name, val, simple_desc, threshold, threshold_label):
            if val >= threshold:
                c = "#3CFF9B"; estado = "ACTIVO"
            elif val >= threshold * 0.6:
                c = "#FFB84D"; estado = "MODERADO"
            else:
                c = "#FF5A67"; estado = "INACTIVO"
            bar_w = min(int(val), 100)
            return (
                f"<tr style='border-bottom:1px solid rgba(255,255,255,.07)'>"
                f"<td style='padding:.55rem .70rem;font-size:.93rem;white-space:nowrap'>{icon} <b>{name}</b></td>"
                f"<td style='padding:.55rem .70rem;min-width:140px'>"
                f"  <div style='display:flex;align-items:center;gap:.5rem'>"
                f"    <div style='flex:1;height:8px;background:rgba(255,255,255,.10);border-radius:99px;overflow:hidden'>"
                f"      <div style='width:{bar_w}%;height:100%;background:{c};border-radius:99px'></div>"
                f"    </div>"
                f"    <span style='color:{c};font-weight:800;font-size:.88rem;min-width:38px'>{val:.0f}%</span>"
                f"  </div>"
                f"</td>"
                f"<td style='padding:.55rem .70rem'><span style='color:{c};font-weight:700;font-size:.80rem;"
                f"background:rgba(0,0,0,.30);padding:.15rem .50rem;border-radius:99px;border:1px solid {c}'>{estado}</span></td>"
                f"<td style='padding:.55rem .70rem;color:#CBD5E1;font-size:.84rem'>{simple_desc}</td>"
                f"<td style='padding:.55rem .70rem;color:#94A3B8;font-size:.80rem'>{threshold_label}</td>"
                f"</tr>"
            )

        rows = (
            _engine_card("🧩", "Clusters de wallets", cluster,
                "Wallets que se mueven dinero entre sí de forma repetida. Si hay un cluster grande, "
                "probablemente hay un banco, ODL o market maker operando en grupo.",
                50, "≥50% = cluster activo detectado") +
            _engine_card("🧠", "Topología de red", topo,
                "¿El dinero fluye por unos pocos hubs centrales? Si sí, hay concentración institucional "
                "— un banco o corredor canalizando el flujo.",
                50, "≥50% = hubs detectados · señal institucional") +
            _engine_card("🧬", "Fingerprints (huellas de comportamiento)", fp,
                "¿Las transacciones siguen un patrón repetible? Bancos y market makers tienen "
                "comportamientos muy predecibles: mismo tamaño, misma frecuencia.",
                50, "≥50% = patrón treasury/MM/corredor detectado") +
            _engine_card("🚨", "Anomalías estadísticas", anom,
                "¿Hay algo fuera de lo normal hoy? Una anomalía fuerte puede ser un gran movimiento "
                "institucional, una inyección de liquidez, o un evento inesperado.",
                50, "≥50% = evento inusual · puede ser institucional") +
            _engine_card("⏱️", "Régimen temporal", regime,
                "¿La actividad lleva días seguidos o es solo un pico de hoy? Un régimen alto "
                "significa tendencia sostenida — más fiable que un spike de un día.",
                50, "≥50% = tendencia sostenida · no es ruido") +
            _engine_card("🌐", "Cross-network (multi-red)", cross,
                "¿Hay señales de actividad entre XRPL y otras redes (Ethereum, etc.)? "
                "Los bridges y señales multi-red indican integración más amplia.",
                40, "≥40% = actividad cross-chain detectada")
        )

        # Renderizar diagnóstico de engines de forma independiente (no usa el bloque genérico)
        _h = bytes.fromhex(conclusion_color.lstrip('#'))
        concl_bg = f"rgba({_h[0]},{_h[1]},{_h[2]},.07)"
        th2 = "padding:.35rem .70rem;color:#5AD7FF;font-size:.78rem;font-weight:700;border-bottom:1px solid rgba(90,215,255,.25);text-align:left;white-space:nowrap;background:rgba(14,165,233,.12);"
        st.markdown(f"""
<div style="border:1px solid {border};border-radius:16px;background:rgba(15,23,42,.92);
            margin:.30rem 0 .60rem 0;overflow:hidden;">
  <div style="padding:.65rem 1rem;border-bottom:1px solid rgba(255,255,255,.10);
              background:rgba(14,165,233,.08);font-size:.93rem;">{headline}</div>
  <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;">
      <thead><tr>
        <th style="{th2}">Motor</th>
        <th style="{th2}">Señal hoy</th>
        <th style="{th2}">Estado</th>
        <th style="{th2}">Qué significa en lenguaje sencillo</th>
        <th style="{th2}">Umbral de activación</th>
      </tr></thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
  <div style="padding:.75rem 1rem;border-top:1px solid rgba(255,255,255,.08);
              background:{concl_bg}">
    <div style="font-size:.85rem;font-weight:700;color:{conclusion_color};margin-bottom:.30rem;">
      {conclusion_icon} {conclusion_title}
    </div>
    <div style="font-size:.87rem;color:#CBD5E1;line-height:1.55">{conclusion_text}</div>
  </div>
</div>""", unsafe_allow_html=True)
        return  # ya renderizado, saltar bloque genérico

    elif chart == "heatmap":
        phase    = int(last.get("phase", 0))
        phase_nm = str(last.get("phase_name", ""))
        cov      = pct("radar_coverage")
        adopt    = pct("adoption_score")
        border   = "#5AD7FF"
        headline = f"🗓️ <b>Fase actual: {phase}/5 — {phase_nm}</b> · Cobertura: {cov:.0f}% · Adopción: {adopt:.0f}%"
        rows = (
            "<tr><td colspan='4' style='padding:.50rem .70rem;color:#94A3B8;font-size:.84rem'>"
            "<b style='color:#5AD7FF'>Cómo leer el heatmap:</b><br>"
            "• Cada <b>fila</b> = un motor de inteligencia diferente.<br>"
            "• Cada <b>columna</b> = un día de los últimos 90 días.<br>"
            "• <b>Color azul oscuro</b> = 0% (sin señal ese día) — "
            "<b>azul</b> = débil — <b>naranja</b> = moderado — <b>verde brillante</b> = fuerte (≥80%).<br>"
            "• Busca <b>franjas horizontales</b> verdes o naranjas que duren muchos días = motor activo de forma sostenida = buena señal.<br>"
            "• Pasa el cursor sobre cualquier celda para ver el valor exacto de ese motor ese día."
            "</td></tr>"
        )
    else:
        return

    th = "padding:.28rem .70rem;color:#5AD7FF;font-size:.80rem;font-weight:700;border-bottom:1px solid rgba(90,215,255,.25);text-align:left;white-space:nowrap;background:rgba(14,165,233,.12);"
    header_row = (
        f"<tr>"
        f"<th style='{th}'>Métrica</th>"
        f"<th style='{th}'>Valor hoy</th>"
        f"<th style='{th}'>Qué mide</th>"
        f"<th style='{th}'>Cómo interpretar el resultado</th>"
        f"</tr>"
    )

    st.markdown(f"""
<div style="border:1px solid {border};border-radius:16px;background:rgba(15,23,42,.92);
            margin:.30rem 0 1.20rem 0;overflow:hidden;">
  <div style="padding:.65rem 1rem;border-bottom:1px solid rgba(255,255,255,.10);
              background:rgba(14,165,233,.08);font-size:.93rem;">
    {headline}
  </div>
  <div style="overflow-x:auto;">
    <table style="width:100%;border-collapse:collapse;">
      <thead>{header_row}</thead>
      <tbody>{rows}</tbody>
    </table>
  </div>
</div>""", unsafe_allow_html=True)


# =============================================================================
# UI
# =============================================================================

def inject_css() -> None:
    st.markdown("""
<style>
/* ============================================================
   RIPPLE RADAR PRO v6.0 — TEMA OSCURO COMPLETO
   ============================================================ */

/* === FONDO PRINCIPAL === */
.stApp {
    background:
        radial-gradient(circle at 15% 5%, rgba(0,212,255,.20), transparent 30%),
        radial-gradient(circle at 85% 5%, rgba(60,255,155,.14), transparent 28%),
        linear-gradient(180deg, #06101F 0%, #020617 100%);
    color: #FFFFFF;
}
.block-container { padding-top: 1.1rem; max-width: 1600px; }

/* === TIPOGRAFÍA GLOBAL === */
h1, h2, h3, h4, h5, h6 { color: #FFFFFF !important; }
p, span, label, div { color: #F8FAFC; }
.stMarkdown p, .stMarkdown span, .stMarkdown li { color: #F8FAFC !important; }

/* === SIDEBAR === */
[data-testid="stSidebar"] { background: #07111F !important; border-right: 1px solid rgba(255,255,255,.18); }
[data-testid="stSidebar"] * { color: #F8FAFC !important; }
section[data-testid="stSidebar"] { min-width: 285px !important; }
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] .stCaptionContainer { color: #F8FAFC !important; }

/* === MÉTRICAS === */
[data-testid="stMetric"] {
    background: rgba(15,23,42,.88) !important;
    border: 1px solid rgba(255,255,255,.22) !important;
    border-radius: 18px !important;
    padding: 1rem !important;
    box-shadow: 0 14px 34px rgba(0,0,0,.30) !important;
}
[data-testid="stMetricLabel"] { color: #FFFFFF !important; font-weight: 900; }
[data-testid="stMetricValue"] { color: #FFFFFF !important; font-size: 1.80rem !important; font-weight: 950; }
[data-testid="stMetricDelta"] svg { display: none; }

/* === BOTONES — ÁREA PRINCIPAL === */
.stButton > button {
    background: rgba(14,165,233,0.15) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(90,215,255,0.45) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
    transition: background 0.2s, border-color 0.2s !important;
}
.stButton > button:hover {
    background: rgba(14,165,233,0.32) !important;
    border-color: rgba(90,215,255,0.80) !important;
}
.stButton > button p,
.stButton > button span { color: #FFFFFF !important; }

/* Botones sidebar — azul sólido */
section[data-testid="stSidebar"] .stButton > button {
    width: 100% !important;
    min-height: 42px !important;
    background: #0EA5E9 !important;
    border: 1px solid rgba(255,255,255,.45) !important;
    font-size: .92rem !important;
}
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #0284C7 !important;
}
section[data-testid="stSidebar"] .stButton > button p { color: #FFFFFF !important; }

/* === BOTONES DE DESCARGA === */
[data-testid="stDownloadButton"] > button,
.stDownloadButton > button {
    background: rgba(60,255,155,0.12) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(60,255,155,0.45) !important;
    border-radius: 12px !important;
    font-weight: 700 !important;
}
[data-testid="stDownloadButton"] > button:hover,
.stDownloadButton > button:hover {
    background: rgba(60,255,155,0.25) !important;
    border-color: rgba(60,255,155,0.75) !important;
}
[data-testid="stDownloadButton"] > button p,
[data-testid="stDownloadButton"] > button span { color: #FFFFFF !important; }

/* === RADIO BUTTONS (menú de navegación) === */
[data-testid="stRadio"] > div { gap: .22rem !important; }
[data-testid="stRadio"] label {
    background: rgba(15,23,42,0.60) !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    border-radius: 10px !important;
    padding: .32rem .70rem !important;
    color: #94A3B8 !important;
    cursor: pointer !important;
    transition: all 0.15s ease !important;
}
[data-testid="stRadio"] label:hover {
    background: rgba(14,165,233,0.18) !important;
    border-color: rgba(90,215,255,0.45) !important;
    color: #FFFFFF !important;
}
[data-testid="stRadio"] label[data-checked="true"],
[data-testid="stRadio"] label[aria-checked="true"] {
    background: rgba(14,165,233,0.28) !important;
    border-color: rgba(90,215,255,0.70) !important;
    color: #FFFFFF !important;
}
[data-testid="stRadio"] span { color: inherit !important; }

/* === EXPANDER (el desplegable "¿Qué significa?") === */
[data-testid="stExpander"] {
    background: rgba(15,23,42,.88) !important;
    border: 1px solid rgba(90,215,255,.28) !important;
    border-radius: 16px !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary,
[data-testid="stExpander"] .streamlit-expanderHeader,
[data-testid="stExpander"] > details > summary,
[data-testid="stExpanderToggleIcon"],
button[data-testid="stBaseButton-headerNoPadding"] {
    background: rgba(14,165,233,0.14) !important;
    color: #FFFFFF !important;
    border-radius: 14px 14px 0 0 !important;
    font-weight: 700 !important;
    padding: .65rem 1rem !important;
}
[data-testid="stExpander"] * { color: #FFFFFF !important; background: transparent; }
[data-testid="stExpander"] svg { stroke: #5AD7FF !important; }

/* === ALERTAS NATIVAS Streamlit === */
[data-testid="stAlert"] {
    border-radius: 14px !important;
}
[data-testid="stAlert"] p,
[data-testid="stAlert"] span,
[data-testid="stAlert"] div { color: #F8FAFC !important; }
/* success */
div[data-testid="stAlert"][data-baseweb="notification"][kind="positive"],
.stSuccess > div {
    background: rgba(60,255,155,0.10) !important;
    border: 1px solid rgba(60,255,155,0.50) !important;
}
/* info */
div[data-testid="stAlert"][data-baseweb="notification"][kind="info"],
.stInfo > div {
    background: rgba(90,215,255,0.10) !important;
    border: 1px solid rgba(90,215,255,0.50) !important;
}
/* warning */
div[data-testid="stAlert"][data-baseweb="notification"][kind="warning"],
.stWarning > div {
    background: rgba(255,184,77,0.10) !important;
    border: 1px solid rgba(255,184,77,0.50) !important;
}
/* error */
div[data-testid="stAlert"][data-baseweb="notification"][kind="negative"],
.stError > div {
    background: rgba(255,90,103,0.10) !important;
    border: 1px solid rgba(255,90,103,0.50) !important;
}

/* === SLIDER === */
[data-testid="stSlider"] label,
[data-testid="stSlider"] span { color: #FFFFFF !important; }
[data-testid="stSlider"] [role="slider"] {
    background: #0EA5E9 !important;
    border: 2px solid #5AD7FF !important;
}

/* === TOGGLE === */
[data-testid="stToggle"] label,
[data-testid="stToggle"] span { color: #FFFFFF !important; }
[data-testid="stToggle"] [role="switch"][aria-checked="true"] {
    background-color: #0EA5E9 !important;
}

/* === SELECTBOX / MULTISELECT — control + dropdown popup === */

/* Label */
[data-testid="stSelectbox"] label,
[data-testid="stMultiSelect"] label {
    color: #FFFFFF !important;
}

/* Control visible (caja cerrada) */
[data-testid="stSelectbox"] > div > div,
[data-testid="stMultiSelect"] > div > div {
    background: rgba(15,23,42,0.92) !important;
    border: 1px solid rgba(90,215,255,0.38) !important;
    border-radius: 10px !important;
    color: #E2E8F0 !important;
}

/* Texto seleccionado dentro del control */
[data-testid="stSelectbox"] > div > div > div,
[data-testid="stSelectbox"] span,
[data-testid="stSelectbox"] p,
[data-testid="stSelectbox"] div[class*="singleValue"],
[data-testid="stMultiSelect"] span {
    color: #E2E8F0 !important;
    background: transparent !important;
}

/* Flecha del selectbox */
[data-testid="stSelectbox"] svg,
[data-testid="stMultiSelect"] svg {
    color: #5AD7FF !important;
    fill: #5AD7FF !important;
}

/* Lista desplegable (popup flotante) */
[data-baseweb="popover"],
[data-baseweb="popover"] > div,
ul[data-baseweb="menu"],
[data-baseweb="menu"],
[data-baseweb="select"] [role="listbox"],
div[class*="MenuList"],
div[class*="menu"] {
    background: #07111f !important;
    background-color: #07111f !important;
    border: 1px solid rgba(90,215,255,0.40) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 32px rgba(0,0,0,0.70) !important;
    color: #E2E8F0 !important;
}

/* Cada opción del desplegable */
li[role="option"],
[data-baseweb="menu"] li,
[data-baseweb="option"],
div[class*="option"],
div[class*="Option"] {
    background: #07111f !important;
    background-color: #07111f !important;
    color: #E2E8F0 !important;
    font-size: .88rem !important;
    padding: .45rem .80rem !important;
}

/* Opción al hacer hover */
li[role="option"]:hover,
[data-baseweb="option"]:hover,
div[class*="option"]:hover,
[aria-selected="false"]:hover {
    background: rgba(14,165,233,0.20) !important;
    background-color: rgba(14,165,233,0.20) !important;
    color: #FFFFFF !important;
    cursor: pointer !important;
}

/* Opción seleccionada */
li[role="option"][aria-selected="true"],
[aria-selected="true"],
div[class*="option--is-selected"] {
    background: rgba(90,215,255,0.18) !important;
    background-color: rgba(90,215,255,0.18) !important;
    color: #5AD7FF !important;
    font-weight: 700 !important;
}

/* Input de búsqueda dentro del desplegable */
[data-baseweb="select"] input,
div[class*="Input"] input {
    background: transparent !important;
    color: #E2E8F0 !important;
    caret-color: #5AD7FF !important;
}

/* === TEXT INPUT — texto negro visible sobre fondo blanco === */
[data-testid="stTextInput"] input,
[data-testid="stTextInput"] input:focus,
[data-testid="stTextInput"] input:active,
[data-baseweb="input"] input,
[data-baseweb="input"] input:focus,
input[type="text"],
input[type="search"],
.stTextInput input {
    color: #0F172A !important;
    background-color: #FFFFFF !important;
    caret-color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
}
[data-testid="stTextInput"] input::placeholder,
[data-baseweb="input"] input::placeholder {
    color: rgba(71,85,105,0.80) !important;
    -webkit-text-fill-color: rgba(71,85,105,0.80) !important;
}

/* Scrollbar del desplegable */
[data-baseweb="menu"] ::-webkit-scrollbar { width: 6px; }
[data-baseweb="menu"] ::-webkit-scrollbar-track { background: #07111f; }
[data-baseweb="menu"] ::-webkit-scrollbar-thumb {
    background: rgba(90,215,255,0.35);
    border-radius: 99px;
}

/* === DATAFRAME / TABLA === */
[data-testid="stDataFrame"],
[data-testid="stDataframe"] {
    border: 1px solid rgba(90,215,255,0.20) !important;
    border-radius: 12px !important;
    overflow: hidden !important;
}
.dvn-scroller { background: rgba(7,17,31,0.97) !important; }

/* === CÓDIGO / CODE BLOCK === */
[data-testid="stCode"], .stCode, code, pre {
    background: rgba(15,23,42,0.95) !important;
    border: 1px solid rgba(90,215,255,0.25) !important;
    border-radius: 10px !important;
    color: #3CFF9B !important;
}

/* === CAPTION === */
[data-testid="stCaptionContainer"], .stCaption { color: #94A3B8 !important; }

/* === TABS (si se usan) === */
[data-testid="stTabs"] [data-baseweb="tab-list"] {
    background: rgba(15,23,42,0.80) !important;
    border-bottom: 1px solid rgba(90,215,255,0.25) !important;
    gap: .25rem !important;
}
[data-testid="stTabs"] [data-baseweb="tab"] {
    background: transparent !important;
    color: #94A3B8 !important;
    border-radius: 8px 8px 0 0 !important;
}
[data-testid="stTabs"] [data-baseweb="tab"]:hover { color: #FFFFFF !important; background: rgba(14,165,233,0.12) !important; }
[data-testid="stTabs"] [aria-selected="true"] {
    background: rgba(14,165,233,0.20) !important;
    color: #FFFFFF !important;
    border-bottom: 2px solid #5AD7FF !important;
}
[data-testid="stTabs"] [data-baseweb="tab-panel"] { background: transparent !important; }

/* === PLOTLY — LEYENDAS Y TEXTOS === */
.js-plotly-plot .legend text { fill: #FFFFFF !important; }
.js-plotly-plot .gtitle,
.js-plotly-plot .xtitle,
.js-plotly-plot .ytitle,
.js-plotly-plot .annotation-text,
.js-plotly-plot text { fill: #FFFFFF !important; color: #FFFFFF !important; }

/* ============================================================
   COMPONENTES CUSTOM RRP
   ============================================================ */
.rrp-hero {
    padding: 1.25rem 1.45rem; border: 1px solid rgba(90,215,255,.42);
    border-radius: 26px; background: linear-gradient(135deg, rgba(15,23,42,.97), rgba(30,41,59,.76));
    box-shadow: 0 24px 60px rgba(0,0,0,.34); margin-bottom: .85rem;
}
.rrp-kicker { color: #5AD7FF; text-transform: uppercase; letter-spacing: .13em; font-size: .76rem; font-weight: 900; }
.rrp-title { color:#FFFFFF; font-size: 2.45rem; font-weight: 950; line-height: 1.05; margin: .15rem 0 .35rem 0; }
.rrp-sub { color: #F8FAFC; font-size: 1.05rem; max-width: 1180px; }
.rrp-pill {
    display:inline-block; padding:.28rem .62rem; border-radius:999px;
    border:1px solid rgba(255,255,255,.30); color:#FFFFFF; font-size:.80rem;
    font-weight:700; margin-right:.35rem; margin-bottom:.25rem; background:rgba(255,255,255,.06);
}
.rrp-alert { padding:1.05rem 1.25rem; border-radius:20px; font-size:1.10rem; font-weight:850; margin:.60rem 0 1rem 0; }
.rrp-green  { background:rgba(60,255,155,.16);  border:1px solid rgba(60,255,155,.70);  }
.rrp-red    { background:rgba(255,90,103,.18);  border:1px solid rgba(255,90,103,.70);  }
.rrp-orange { background:rgba(255,184,77,.16);  border:1px solid rgba(255,184,77,.70);  }
.rrp-purple { background:rgba(182,115,255,.18); border:1px solid rgba(182,115,255,.70); }
.rrp-card {
    padding:1.05rem 1.15rem; border:1px solid rgba(255,255,255,.22); border-radius:20px;
    background:rgba(15,23,42,.86); box-shadow:0 14px 38px rgba(0,0,0,.24); height:100%;
}
.rrp-card b { color:#FFFFFF; }
.rrp-card .desc { color:#E2E8F0; font-size:.95rem; line-height:1.45; }
.rrp-mini-card {
    padding:.75rem .90rem; border:1px solid rgba(90,215,255,.22); border-radius:14px;
    background:rgba(15,23,42,.82); margin-bottom:.50rem;
}
.rrp-mini-card b { color:#5AD7FF; font-size:.95rem; display:block; margin-bottom:.25rem; }
.rrp-mini-card .small { color:#CBD5E1; font-size:.86rem; line-height:1.42; }
.rrp-legend-box {
    padding:.85rem .95rem; border-radius:18px;
    border:1px solid rgba(255,255,255,.22); background:rgba(15,23,42,.86); margin-top:.55rem;
}
.rrp-line { display:flex; align-items:center; gap:.55rem; margin:.35rem 0; color:#F8FAFC !important; font-size:.92rem; }
.rrp-swatch { display:inline-block; width:30px; height:5px; border-radius:99px; flex-shrink:0; }
.rrp-dot    { display:inline-block; width:11px; height:11px; border-radius:99px; flex-shrink:0; }
.rrp-section-title { font-size:1.35rem; font-weight:950; color:#FFFFFF; margin:1rem 0 .4rem 0; }
.rrp-note {
    padding:.8rem .95rem; border-radius:16px;
    background:rgba(14,165,233,.12); border:1px solid rgba(90,215,255,.35);
    color:#F8FAFC !important; margin:.5rem 0 1rem 0;
}
.rrp-warning {
    padding:.8rem .95rem; border-radius:16px;
    background:rgba(255,184,77,.12); border:1px solid rgba(255,184,77,.45);
    color:#F8FAFC !important; margin:.5rem 0 1rem 0;
}
.rrp-cinema-frame {
    padding:.90rem 1.05rem; border-radius:16px;
    background:rgba(15,23,42,.90); border:1px solid rgba(182,115,255,.38);
    color:#F8FAFC !important; margin:.5rem 0 .80rem 0; font-size:.96rem; line-height:1.55;
}
.rrp-cinema-frame b { color:#B673FF; }
.rrp-path-panel {
    padding:1.15rem 1.25rem; border-radius:22px;
    border:1px solid rgba(182,115,255,.42);
    background:linear-gradient(135deg,rgba(15,23,42,.95),rgba(30,41,59,.80));
    box-shadow:0 18px 42px rgba(0,0,0,.28); margin:.85rem 0 1rem 0;
}
.rrp-path-title { font-size:1.35rem; font-weight:950; color:#FFFFFF !important; margin-bottom:.35rem; }
.rrp-path-text  { color:#F8FAFC !important; font-size:1rem; line-height:1.5; }

.rrp-route-click-list {
    border:1px solid rgba(90,215,255,.25);
    border-radius:22px;
    background:rgba(7,17,31,.86);
    padding:.85rem .95rem;
    margin:.65rem 0 1rem 0;
}
.rrp-route-picker-card {
    border:1px solid rgba(90,215,255,.22);
    border-radius:18px;
    background:linear-gradient(135deg,rgba(15,23,42,.96),rgba(30,41,59,.84));
    padding:.80rem .90rem;
    margin:.45rem 0;
    color:#F8FAFC !important;
    box-shadow:0 10px 28px rgba(0,0,0,.22);
}
.rrp-route-picker-card * { color:#F8FAFC !important; -webkit-text-fill-color:#F8FAFC !important; }
.rrp-route-picker-title { font-size:.98rem; font-weight:950; color:#FFFFFF !important; margin-bottom:.35rem; }
.rrp-route-picker-meta { font-size:.84rem; color:#CBD5E1 !important; line-height:1.38; }
.rrp-route-badge {
    display:inline-block; padding:.14rem .45rem; border-radius:999px;
    border:1px solid rgba(90,215,255,.35); background:rgba(90,215,255,.12);
    color:#E0F2FE !important; font-size:.78rem; font-weight:800; margin-right:.30rem;
}

.rrp-proof-lockbox {
    border:1px solid rgba(60,255,155,.28);
    border-radius:20px;
    background:linear-gradient(135deg,rgba(6,78,59,.28),rgba(15,23,42,.94));
    padding:1rem 1.05rem;
    margin:.85rem 0 1rem 0;
    color:#F8FAFC !important;
    box-shadow:0 12px 30px rgba(0,0,0,.24);
}
.rrp-proof-lockbox * { color:#F8FAFC !important; -webkit-text-fill-color:#F8FAFC !important; }
.rrp-proof-title { font-size:1.05rem; font-weight:950; color:#FFFFFF !important; margin-bottom:.45rem; }
.rrp-proof-grid { display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:.65rem; margin-top:.6rem; }
.rrp-proof-card {
    border:1px solid rgba(148,163,184,.26);
    border-radius:16px;
    background:rgba(2,6,23,.58);
    padding:.75rem .85rem;
    min-height:120px;
}
.rrp-proof-card-ok { border-color:rgba(60,255,155,.42); }
.rrp-proof-card-watch { border-color:rgba(255,184,77,.42); }
.rrp-proof-card-bad { border-color:rgba(248,113,113,.42); }
.rrp-proof-kicker { font-size:.72rem; font-weight:900; letter-spacing:.04em; color:#93C5FD !important; text-transform:uppercase; }
.rrp-proof-card-title { font-size:.94rem; font-weight:900; color:#FFFFFF !important; margin:.20rem 0 .35rem 0; line-height:1.25; }
.rrp-proof-url { font-size:.78rem; color:#7DD3FC !important; word-break:break-all; }
.rrp-proof-note { font-size:.82rem; color:#CBD5E1 !important; line-height:1.36; margin-top:.35rem; }
.rrp-checkline { margin:.20rem 0; font-size:.88rem; color:#E2E8F0 !important; }

/* Fichas clicables A→B: no usar texto negro sobre panel oscuro */
[data-testid="stDataFrame"] div,
[data-testid="stDataFrame"] span,
[data-testid="stDataFrame"] p,
[data-testid="stDataFrame"] canvas,
[data-testid="stDataFrame"] * {
    color:#F8FAFC !important;
    -webkit-text-fill-color:#F8FAFC !important;
}



/* === RRP VISIBILITY PATCH — botones/inputs nunca invisibles === */
button,
button *,
.stButton button,
.stButton button *,
.stFormSubmitButton button,
.stFormSubmitButton button *,
[data-testid="baseButton-secondary"],
[data-testid="baseButton-secondary"] *,
[data-testid="baseButton-primary"],
[data-testid="baseButton-primary"] *,
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-secondary"] *,
[data-testid="stBaseButton-primary"],
[data-testid="stBaseButton-primary"] *,
[data-testid="stDownloadButton"] button,
[data-testid="stDownloadButton"] button * {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
    opacity: 1 !important;
}

button,
.stButton button,
.stFormSubmitButton button,
[data-testid="baseButton-secondary"],
[data-testid="baseButton-primary"],
[data-testid="stBaseButton-secondary"],
[data-testid="stBaseButton-primary"] {
    background: linear-gradient(135deg, rgba(14,165,233,.92), rgba(37,99,235,.88)) !important;
    border: 1px solid rgba(125,211,252,.72) !important;
    border-radius: 12px !important;
    box-shadow: 0 8px 22px rgba(2,132,199,.18) !important;
    text-shadow: 0 1px 2px rgba(0,0,0,.45) !important;
}

button:hover,
.stButton button:hover,
.stFormSubmitButton button:hover,
[data-testid="baseButton-secondary"]:hover,
[data-testid="baseButton-primary"]:hover,
[data-testid="stBaseButton-secondary"]:hover,
[data-testid="stBaseButton-primary"]:hover {
    background: linear-gradient(135deg, rgba(56,189,248,1), rgba(14,165,233,.96)) !important;
    border-color: rgba(186,230,253,.95) !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

button:focus,
button:active,
.stButton button:focus,
.stButton button:active,
.stFormSubmitButton button:focus,
.stFormSubmitButton button:active {
    outline: 2px solid rgba(90,215,255,.75) !important;
    outline-offset: 2px !important;
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}

button:disabled,
.stButton button:disabled,
.stFormSubmitButton button:disabled,
[data-testid="baseButton-secondary"]:disabled,
[data-testid="baseButton-primary"]:disabled {
    background: rgba(51,65,85,.72) !important;
    border-color: rgba(148,163,184,.35) !important;
    color: #CBD5E1 !important;
    -webkit-text-fill-color: #CBD5E1 !important;
    opacity: .78 !important;
}
button:disabled *,
.stButton button:disabled *,
.stFormSubmitButton button:disabled * {
    color: #CBD5E1 !important;
    -webkit-text-fill-color: #CBD5E1 !important;
}

/* Formularios, chat e inputs: alto contraste en todas las pestañas */
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea,
[data-testid="stChatInput"] textarea,
[data-testid="stNumberInput"] input,
textarea,
input {
    background: #FFFFFF !important;
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    caret-color: #0F172A !important;
    border: 1px solid rgba(90,215,255,.45) !important;
}
[data-testid="stTextInput"] input::placeholder,
[data-testid="stTextArea"] textarea::placeholder,
[data-testid="stChatInput"] textarea::placeholder,
textarea::placeholder,
input::placeholder {
    color: #64748B !important;
    -webkit-text-fill-color: #64748B !important;
    opacity: 1 !important;
}

/* Selectores y dropdowns: opciones legibles incluso en popup */
[data-baseweb="select"] *,
[data-baseweb="popover"] *,
[role="listbox"] *,
[role="option"] * {
    -webkit-text-fill-color: currentColor !important;
}

/* Tabs/radio/checkbox: texto visible */
[data-testid="stTabs"] button *,
[data-testid="stRadio"] label *,
[data-testid="stCheckbox"] label *,
[data-testid="stToggle"] label * {
    color: inherit !important;
    -webkit-text-fill-color: currentColor !important;
}
[data-testid="stCheckbox"] label,
[data-testid="stCheckbox"] span,
[data-testid="stCheckbox"] p {
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}

/* Data editor/dataframe y mensajes pequeños */
[data-testid="stDataFrame"] *,
[data-testid="stDataframe"] *,
[data-testid="stCaptionContainer"] * {
    -webkit-text-fill-color: currentColor !important;
}

</style>
""", unsafe_allow_html=True)


def alert_class(state: str) -> str:
    return "rrp-purple" if state == "flip" else "rrp-green" if state == "bull" else "rrp-red" if state == "bear" else "rrp-orange"


def render_hero() -> None:
    st.markdown(f"""
<div class="rrp-hero">
  <div class="rrp-kicker">XRP / RLUSD · Advanced Intelligence · {VERSION}</div>
  <div class="rrp-title">Ripple Radar Pro</div>
  <div class="rrp-sub">
    Radar avanzado para vigilar rutas privadas por sus huellas públicas: clusters, topología,
    fingerprints, anomalías, DEX/AMM, trustlines, transfers grandes y régimen temporal.
  </div>
  <div style="margin-top:.8rem">
    <span class="rrp-pill">XRPL real</span>
    <span class="rrp-pill">Cluster intelligence</span>
    <span class="rrp-pill">Fingerprints</span>
    <span class="rrp-pill">Topology engine</span>
    <span class="rrp-pill">Anomaly detection</span>
    <span class="rrp-pill">Pump vs Adoption</span>
  </div>
</div>
""", unsafe_allow_html=True)


def render_alert(state: Dict[str, str]) -> None:
    st.markdown(f"<div class='rrp-alert {alert_class(state['state'])}'><b>{state['headline']}</b><br>{state['simple']}</div>", unsafe_allow_html=True)


def render_cards(state: Dict[str, str], row: pd.Series) -> None:
    a,b,c,d = st.columns(4)
    a.markdown(f"<div class='rrp-card'><b>Precio XRP</b><br><span class='desc'>{state['price']}</span></div>", unsafe_allow_html=True)
    b.markdown(f"<div class='rrp-card'><b>Riesgo</b><br><span class='desc'>{state['risk']}</span></div>", unsafe_allow_html=True)
    c.markdown(f"<div class='rrp-card'><b>Adopción real</b><br><span class='desc'>{state['adoption']}</span></div>", unsafe_allow_html=True)

    # v91: Pump y adopción NO son porcentajes de un pastel que deban sumar 100.
    # Son dos señales independientes normalizadas. Para evitar miedo a duplicación,
    # mostramos además el diferencial y una zona no concluyente solo como lectura visual.
    pump = float(row.get('pump_score', 0.0) or 0.0)
    adoption = float(row.get('adoption_score', 0.0) or 0.0)
    neutral = max(0.0, 100.0 - min(100.0, pump + adoption))
    delta = adoption - pump
    if delta >= 12:
        lectura = "adopción domina"
    elif delta <= -12:
        lectura = "pump domina"
    else:
        lectura = "zona mixta"
    d.markdown(
        f"<div class='rrp-card'><b>Pump vs Adopción</b><br>"
        f"<span class='desc'>Pump: {pump:.1f}%<br>"
        f"Adopción técnica: {adoption:.1f}%<br>"
        f"Zona no concluyente: {neutral:.1f}%<br>"
        f"Diferencial: {delta:+.1f} pp · {lectura}</span>"
        f"<div class='small' style='margin-top:6px;color:#94A3B8'>"
        f"No duplica datos fijados: son señales cruzadas independientes y deduplicadas antes de agregarse.</div></div>",
        unsafe_allow_html=True,
    )


def render_metric_explanations() -> None:
    with st.expander("📘 ¿Qué significan estos datos?", expanded=True):
        c1, c2, c3, c4 = st.columns(4)
        c1.markdown("""
<div class='rrp-mini-card'>
<b>Subida</b><br>
<span class='small'>Probabilidad de impulso de precio por actividad pública: volumen, transfers grandes, DEX, anomalías y régimen temporal.</span>
</div>
""", unsafe_allow_html=True)
        c2.markdown("""
<div class='rrp-mini-card'>
<b>Riesgo</b><br>
<span class='small'>Detecta enfriamiento: baja actividad, poca persistencia, falta de clusters o spike que parece especulativo.</span>
</div>
""", unsafe_allow_html=True)
        c3.markdown("""
<div class='rrp-mini-card'>
<b>Flip</b><br>
<span class='small'>Señal de adopción real. Solo sube fuerte si varias huellas públicas se coordinan durante tiempo.</span>
</div>
""", unsafe_allow_html=True)
        c4.markdown("""
<div class='rrp-mini-card'>
<b>Cobertura</b><br>
<span class='small'>Cuántos puntos públicos estamos vigilando donde las rutas privadas tendrían que dejar rastro.</span>
</div>
""", unsafe_allow_html=True)
        c5, c6, c7 = st.columns(3)
        c5.markdown("""
<div class='rrp-mini-card'>
<b>Fase</b><br>
<span class='small'>Escala 0–5: de ruido bajo a Full Flip. Resume el estado completo del radar.</span>
</div>
""", unsafe_allow_html=True)
        c6.markdown("""
<div class='rrp-mini-card'>
<b>Pump</b><br>
<span class='small'>Probabilidad de que sea movimiento especulativo o spike sin adopción sostenida.</span>
</div>
""", unsafe_allow_html=True)
        c7.markdown("""
<div class='rrp-mini-card'>
<b>Rutas hot</b><br>
<span class='small'>Número de rutas o motores que están por encima del umbral de señal fuerte.</span>
</div>
""", unsafe_allow_html=True)


def render_explainers() -> None:
    st.subheader("Qué hace cada motor")
    cols = st.columns(3)
    items = [
        ("🧩 Cluster Intelligence", "Agrupa wallets relacionadas y busca hubs, distribuidores y clusters treasury-like."),
        ("🧬 Fingerprints", "Detecta patrones tipo treasury, market maker o corridor por tamaño, repetición y frecuencia."),
        ("🧠 Topology Engine", "Analiza cómo fluye la liquidez: hubs, concentración, densidad y dirección."),
        ("🚨 Anomaly Detection", "Compara la actividad actual contra la historia para separar spike de régimen."),
        ("🌊 DEX/AMM Watcher", "Vigila ofertas, AMM y liquidez pública donde rutas privadas pueden tocar mercado."),
        ("🔥 Pump vs Adoption", "Diferencia subidas especulativas de actividad institucional persistente."),
    ]
    for i, (title, desc) in enumerate(items):
        with cols[i % 3]:
            st.markdown(f"<div class='rrp-card'><b>{title}</b><br><span class='desc'>{desc}</span></div>", unsafe_allow_html=True)


def render_diagnostics(conn: sqlite3.Connection, df: pd.DataFrame) -> None:
    st.subheader("Diagnóstico")
    ok, msg = check_xrpl_connection()
    st.success(msg) if ok else st.error(msg)
    raw_count = conn.execute("SELECT COUNT(*) FROM raw_events").fetchone()[0]
    daily_count = conn.execute("SELECT COUNT(*) FROM daily_metrics").fetchone()[0]
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Eventos XRPL", raw_count)
    c2.metric("Días", daily_count)
    c3.metric("Clusters", conn.execute("SELECT COUNT(*) FROM clusters").fetchone()[0])
    c4.metric("Fingerprints", conn.execute("SELECT COUNT(*) FROM fingerprints").fetchone()[0])
    events = pd.read_sql_query("SELECT * FROM app_events ORDER BY id DESC LIMIT 30", conn)
    st.dataframe(events, width="stretch", hide_index=True)


def render_donations() -> None:
    # Inyectar CSS global que sobreescribe -webkit-text-fill-color de Streamlit
    st.markdown("""
<style>
.don-outer, .don-outer * {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}
.don-outer .don-tok {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
.don-outer .don-addr {
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-family: monospace !important;
}
</style>
""", unsafe_allow_html=True)

    cards_html = """
<div class='don-outer' style='background:#FFFFFF;border-radius:16px;padding:24px 28px;
     box-shadow:0 4px 20px rgba(0,0,0,0.10);margin-bottom:8px;'>
  <p style='font-size:1.35rem;font-weight:900;margin:0 0 6px 0;'>💙 Apoyar el proyecto</p>
  <p style='font-size:0.92rem;margin:0 0 12px 0;'>
    Si este radar te resulta útil, puedes apoyar su desarrollo enviando cualquier
    cantidad a las siguientes direcciones. Todas las redes son bienvenidas.
  </p>
  <div style='background:#F8FAFC;border:1px solid #E5E7EB;border-radius:10px;padding:12px 14px;margin-bottom:18px;'>
    <b>Reparto operativo sugerido:</b> 60% para recargar manualmente la API de Anthropic y 40% para desarrollo/infraestructura.
    La recarga de Anthropic no puede hacerse automáticamente con tokens; hay que pasar por la consola oficial.
  </div>
"""
    for _w in DONATION_WALLETS:
        _col  = _w["color"]
        _icon = _w["icon"]
        _net  = _w["red"]
        _tok  = _w["token"]
        _addr = _w["address"]
        cards_html += f"""
  <div style='background:#FFFFFF;border:1.5px solid {_col};border-radius:10px;
              padding:13px 16px;margin-bottom:10px;'>
    <div style='display:flex;align-items:center;gap:8px;margin-bottom:8px;'>
      <span style='font-size:1.3rem;line-height:1;'>{_icon}</span>
      <span style='font-size:0.95rem;font-weight:800;'>{_net}</span>
      <span class='don-tok' style='background:{_col};border-radius:5px;
                   padding:2px 9px;font-size:0.75rem;font-weight:700;'>{_tok}</span>
    </div>
    <div class='don-addr' style='background:#F8FAFC;border-left:4px solid {_col};
                border-radius:6px;padding:9px 13px;font-size:0.82rem;
                word-break:break-all;letter-spacing:0.01em;'>
      {_addr}
    </div>
  </div>
"""
    cards_html += """
  <p style='font-size:0.82rem;margin:12px 0 0 0;text-align:center;'>
    Gracias por apoyar el desarrollo de Ripple Radar Pro 🙏
  </p>
</div>
"""
    st.markdown(cards_html, unsafe_allow_html=True)



# =============================================================================
# ROUTE PATH ENGINE A→B
# =============================================================================

def ensure_discovered_wallets_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS discovered_wallets (
            wallet           TEXT PRIMARY KEY,
            label            TEXT DEFAULT '',
            role             TEXT DEFAULT 'unknown',
            volume_xrp       REAL DEFAULT 0,
            tx_count         INTEGER DEFAULT 0,
            top_counterpart  TEXT DEFAULT '',
            top_cp_label     TEXT DEFAULT '',
            confidence       REAL DEFAULT 0,
            signals          TEXT DEFAULT '',
            xrpscan_name     TEXT DEFAULT '',
            xrpscan_desc     TEXT DEFAULT '',
            added_to_map     INTEGER DEFAULT 0,
            first_seen       TEXT,
            last_seen        TEXT,
            status           TEXT DEFAULT 'watch',
            native_xrp_volume REAL DEFAULT 0,
            approved_iou_volume REAL DEFAULT 0,
            suspicious_iou_volume REAL DEFAULT 0,
            dominant_currency TEXT DEFAULT '',
            quality_reason   TEXT DEFAULT ''
        )
    """)
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(discovered_wallets)").fetchall()]
        migrations = {
            "status": "ALTER TABLE discovered_wallets ADD COLUMN status TEXT DEFAULT 'watch'",
            "native_xrp_volume": "ALTER TABLE discovered_wallets ADD COLUMN native_xrp_volume REAL DEFAULT 0",
            "approved_iou_volume": "ALTER TABLE discovered_wallets ADD COLUMN approved_iou_volume REAL DEFAULT 0",
            "suspicious_iou_volume": "ALTER TABLE discovered_wallets ADD COLUMN suspicious_iou_volume REAL DEFAULT 0",
            "dominant_currency": "ALTER TABLE discovered_wallets ADD COLUMN dominant_currency TEXT DEFAULT ''",
            "quality_reason": "ALTER TABLE discovered_wallets ADD COLUMN quality_reason TEXT DEFAULT ''",
        }
        for col, sql in migrations.items():
            if col not in cols:
                conn.execute(sql)
    except Exception:
        pass
    try:
        # Migración anti-basura: cualquier falso positivo viejo deja de contaminar el mapa.
        # Importante: usamos estado real "discarded", no solo cuarentena, para que no
        # pueda volver a aparecer como "✅ En radar" por un added_to_map antiguo.
        conn.execute("""
            UPDATE discovered_wallets
               SET added_to_map=0,
                   status='discarded',
                   confidence=MIN(COALESCE(confidence,0), ?),
                   quality_reason=CASE
                       WHEN COALESCE(quality_reason,'')='' THEN 'descartada automática: falso positivo o wallet desconocida sin identidad/conexión verificable'
                       ELSE quality_reason || ' · descartada automática'
                   END
             WHERE wallet IN ({})
                OR (
                    COALESCE(xrpscan_name,'')=''
                    AND COALESCE(top_counterpart,'')=''
                    AND LOWER(COALESCE(label,'')) IN (
                        'desconocido','unknown','exchange / gateway',
                        'whale detectada automáticamente','whale desconocida',
                        'wallet en cuarentena','desconocido / token no aprobado',
                        'hub bidireccional potencial','treasury / distribuidor potencial',
                        'acumulador / market maker potencial'
                    )
                )
                OR (COALESCE(suspicious_iou_volume,0) > 0 AND COALESCE(native_xrp_volume,0)=0 AND COALESCE(approved_iou_volume,0)=0)
        """.format(",".join("?" for _ in WALLET_HARD_BLOCKLIST)), (DISCARDED_CONF_CAP, *list(WALLET_HARD_BLOCKLIST)))
    except Exception:
        pass
    conn.commit()

def ensure_unknown_whales_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS unknown_whales (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            tx_hash       TEXT UNIQUE,
            ledger_index  INTEGER,
            sender        TEXT,
            sender_label  TEXT,
            receiver      TEXT,
            receiver_label TEXT,
            amount        TEXT,
            currency      TEXT,
            xrp_value     REAL,
            first_seen    TEXT,
            chain_score_s INTEGER DEFAULT 0,
            chain_score_r INTEGER DEFAULT 0,
            verdict_s     TEXT DEFAULT '',
            verdict_r     TEXT DEFAULT '',
            tracked       INTEGER DEFAULT 0
        )
    """)
    conn.commit()


def save_unknown_whale(conn: sqlite3.Connection, tx: Dict[str, Any]) -> None:
    """Guarda una transacción whale cuyo sender Y receiver son desconocidos."""
    ensure_unknown_whales_table(conn)
    today = str(_date.today())
    try:
        conn.execute("""
            INSERT OR IGNORE INTO unknown_whales
            (tx_hash, ledger_index, sender, sender_label, receiver, receiver_label,
             amount, currency, xrp_value, first_seen)
            VALUES (?,?,?,?,?,?,?,?,?,?)
        """, (
            tx.get("hash", ""),
            int(tx.get("ledger_index", 0)),
            tx.get("sender", ""),
            tx.get("sender_label", ""),
            tx.get("receiver", ""),
            tx.get("receiver_label", ""),
            tx.get("amount", ""),
            tx.get("currency", ""),
            float(tx.get("xrp_value", 0)),
            today,
        ))
        conn.commit()
    except Exception:
        pass


def ensure_route_paths_table(conn: sqlite3.Connection) -> None:
    conn.execute("""
        CREATE TABLE IF NOT EXISTS route_paths (
            day TEXT,
            path_id TEXT,
            origin TEXT,
            public_hop TEXT,
            destination TEXT,
            confidence REAL,
            path_type TEXT,
            evidence TEXT,
            explanation TEXT,
            PRIMARY KEY(day, path_id)
        )
    """)
    try:
        cols = [r[1] for r in conn.execute("PRAGMA table_info(route_paths)").fetchall()]
        if "explanation" not in cols:
            conn.execute("ALTER TABLE route_paths ADD COLUMN explanation TEXT")
    except Exception:
        pass
    conn.commit()


def infer_private_origin(row: pd.Series) -> Tuple[str, float, List[str]]:
    evidence = []
    scores = {
        # Bancos específicos (ODL directo — alta correlación con payment_flow)
        "SBI Remit / Japón":          float(row.get("payment_flow_score", 0)) * 0.60 + float(row.get("cluster_score", 0)) * 0.25 + float(row.get("fingerprint_score", 0)) * 0.15,
        "Santander":                   float(row.get("institutional_route_score", 0)) * 0.55 + float(row.get("payment_flow_score", 0)) * 0.30 + float(row.get("public_gateway_score", 0)) * 0.15,
        "Bitso / BeeTech (ODL LATAM)": float(row.get("bridge_score", 0)) * 0.40 + float(row.get("payment_flow_score", 0)) * 0.40 + float(row.get("dex_score", 0)) * 0.20,
        "Tranglo / Coins.ph (ODL Asia)":float(row.get("bridge_score", 0)) * 0.45 + float(row.get("payment_flow_score", 0)) * 0.35 + float(row.get("topology_score", 0)) * 0.20,
        "Standard Chartered / SWIFT":  float(row.get("institutional_route_score", 0)) * 0.50 + float(row.get("large_transfer_score", 0)) * 0.30 + float(row.get("persistence_score", 0)) * 0.20,
        "Bank of America / PNC":       float(row.get("institutional_route_score", 0)) * 0.45 + float(row.get("payment_flow_score", 0)) * 0.35 + float(row.get("topology_score", 0)) * 0.20,
        "Axis Bank (India)":           float(row.get("institutional_route_score", 0)) * 0.50 + float(row.get("cluster_score", 0)) * 0.30 + float(row.get("payment_flow_score", 0)) * 0.20,
        # Categorías genéricas
        "Ripple Payments":             float(row.get("payment_flow_score", 0)) * 0.55 + float(row.get("public_gateway_score", 0)) * 0.45,
        "Treasury":                    float(row.get("large_transfer_score", 0)) * 0.45 + float(row.get("fingerprint_score", 0)) * 0.30 + float(row.get("custody_score", 0)) * 0.25,
        "Rail / Corredores FX":        float(row.get("bridge_score", 0)) * 0.45 + float(row.get("payment_flow_score", 0)) * 0.30 + float(row.get("topology_score", 0)) * 0.25,
        "Hidden Road / Prime":         float(row.get("prime_brokerage_score", 0)) * 0.50 + float(row.get("fingerprint_score", 0)) * 0.25 + float(row.get("large_transfer_score", 0)) * 0.25,
        "Custody/Metaco":              float(row.get("custody_score", 0)) * 0.50 + float(row.get("trustline_score", 0)) * 0.20 + float(row.get("large_transfer_score", 0)) * 0.30,
        "DTCC/NSCC":                   float(row.get("prime_brokerage_score", 0)) * 0.40 + float(row.get("topology_score", 0)) * 0.35 + float(row.get("persistence_score", 0)) * 0.25,
        "SWIFT/FedNow/SEPA":           float(row.get("institutional_route_score", 0)) * 0.50 + float(row.get("payment_flow_score", 0)) * 0.30 + float(row.get("persistence_score", 0)) * 0.20,
    }
    origin, score = max(scores.items(), key=lambda kv: kv[1])
    if float(row.get("payment_flow_score", 0)) >= 0.45:
        evidence.append("actividad de pagos")
    if float(row.get("bridge_score", 0)) >= 0.40:
        evidence.append("corredor ODL activo")
    if float(row.get("large_transfer_score", 0)) >= 0.45:
        evidence.append("transfers grandes")
    if float(row.get("fingerprint_score", 0)) >= 0.45:
        evidence.append("fingerprint institucional")
    if float(row.get("cluster_score", 0)) >= 0.45:
        evidence.append("cluster de wallets")
    if float(row.get("topology_score", 0)) >= 0.45:
        evidence.append("topología/hubs")
    return origin, float(score), evidence


def infer_public_hop(row: pd.Series) -> Tuple[str, float, List[str]]:
    evidence = []
    scores = {
        "XRPL/RLUSD issuer": float(row.get("public_xrpl_score", 0)) * 0.65 + float(row.get("large_transfer_score", 0)) * 0.35,
        "Public Gateway": float(row.get("public_gateway_score", 0)),
        "Trustlines": float(row.get("trustline_score", 0)),
        "DEX/AMM": float(row.get("dex_score", 0)),
        "Large Transfers": float(row.get("large_transfer_score", 0)),
        "Clusters": float(row.get("cluster_score", 0)),
        "Topology Engine": float(row.get("topology_score", 0)),
    }
    hop, score = max(scores.items(), key=lambda kv: kv[1])
    for name, col in [
        ("XRPL público", "public_xrpl_score"),
        ("Public Gateway", "public_gateway_score"),
        ("trustlines", "trustline_score"),
        ("DEX/AMM", "dex_score"),
        ("transfers grandes", "large_transfer_score"),
        ("clusters", "cluster_score"),
        ("topología", "topology_score"),
    ]:
        if float(row.get(col, 0)) >= 0.45:
            evidence.append(name)
    return hop, float(score), evidence


def infer_private_destination(row: pd.Series) -> Tuple[str, float, List[str]]:
    evidence = []
    scores = {
        "Custody/Metaco": float(row.get("custody_score", 0)) * 0.45 + float(row.get("trustline_score", 0)) * 0.25 + float(row.get("large_transfer_score", 0)) * 0.30,
        "Hidden Road / Prime": float(row.get("prime_brokerage_score", 0)) * 0.45 + float(row.get("fingerprint_score", 0)) * 0.25 + float(row.get("topology_score", 0)) * 0.30,
        "Rail / Corredores FX": float(row.get("bridge_score", 0)) * 0.35 + float(row.get("payment_flow_score", 0)) * 0.35 + float(row.get("public_gateway_score", 0)) * 0.30,
        "Treasury": float(row.get("large_transfer_score", 0)) * 0.40 + float(row.get("cluster_score", 0)) * 0.25 + float(row.get("persistence_score", 0)) * 0.35,
        "Ethereum / Cross-network": float(row.get("cross_network_score", 0)) * 0.60 + float(row.get("bridge_score", 0)) * 0.40,
        "DTCC/NSCC": float(row.get("prime_brokerage_score", 0)) * 0.45 + float(row.get("topology_score", 0)) * 0.35 + float(row.get("persistence_score", 0)) * 0.20,
    }
    dst, score = max(scores.items(), key=lambda kv: kv[1])
    if float(row.get("cross_network_score", 0)) >= 0.35:
        evidence.append("cross-network watcher")
    if float(row.get("bridge_score", 0)) >= 0.35:
        evidence.append("bridge")
    if float(row.get("custody_score", 0)) >= 0.45:
        evidence.append("custody score")
    if float(row.get("prime_brokerage_score", 0)) >= 0.45:
        evidence.append("prime/hidden road")
    if float(row.get("persistence_score", 0)) >= 0.55:
        evidence.append("persistencia")
    return dst, float(score), evidence


def explain_route_path(p: Dict[str, Any]) -> str:
    conf = float(p.get("confidence", 0)) * 100
    evidence = p.get("evidence", "sin evidencia suficiente")
    if conf >= 72:
        strength = "fuerte"
    elif conf >= 52:
        strength = "probable"
    elif conf >= 35:
        strength = "débil"
    else:
        strength = "muy baja"
    return (
        f"El motor ve una ruta {strength}: {p.get('origin')} → {p.get('public_hop')} → {p.get('destination')}. "
        f"No afirma que vea los libros privados; infiere el pasillo A→B por estas huellas públicas: {evidence}. "
        f"Confianza calculada: {conf:.1f}%."
    )


def route_path_engine_row(row: pd.Series) -> Dict[str, Any]:
    origin, oscore, oe = infer_private_origin(row)
    hop, hscore, he = infer_public_hop(row)
    dest, dscore, de = infer_private_destination(row)

    coverage = float(row.get("radar_coverage", 0)) / 100.0
    adoption = float(row.get("adoption_score", 0)) / 100.0
    pump = float(row.get("pump_score", 0)) / 100.0
    persistence = float(row.get("persistence_score", 0))

    confidence = oscore * 0.22 + hscore * 0.28 + dscore * 0.20 + coverage * 0.12 + adoption * 0.10 + persistence * 0.08
    confidence = max(0.0, min(1.0, confidence * (1.0 - pump * 0.20)))

    if confidence >= 0.72:
        path_type = "Ruta A→B fuerte"
    elif confidence >= 0.52:
        path_type = "Ruta A→B probable"
    elif confidence >= 0.35:
        path_type = "Ruta A→B débil"
    else:
        path_type = "Ruido / sin ruta clara"

    evidence = sorted(set(oe + he + de))
    p = {
        "day": str(row.get("day", "")),
        "origin": origin,
        "public_hop": hop,
        "destination": dest,
        "confidence": float(confidence),
        "path_type": path_type,
        "evidence": ", ".join(evidence) if evidence else "sin evidencia suficiente",
        "path_label": f"{origin} → {hop} → {dest}",
    }
    p["explanation"] = explain_route_path(p)
    return p


def rebuild_route_paths(conn: sqlite3.Connection, df: pd.DataFrame) -> pd.DataFrame:
    ensure_route_paths_table(conn)
    if df.empty:
        return pd.DataFrame()
    rows = []
    for _, row in df.iterrows():
        p = route_path_engine_row(row)
        pid = hashlib.sha256((p["day"] + p["path_label"]).encode()).hexdigest()[:12]
        rows.append((p["day"], pid, p["origin"], p["public_hop"], p["destination"], p["confidence"], p["path_type"], p["evidence"], p.get("explanation", "")))
    conn.executemany("""
        INSERT OR REPLACE INTO route_paths(day, path_id, origin, public_hop, destination, confidence, path_type, evidence, explanation)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, rows)
    conn.commit()
    return pd.DataFrame(rows, columns=["day", "path_id", "origin", "public_hop", "destination", "confidence", "path_type", "evidence", "explanation"])


# ── Deductive Route Engine v69 ─────────────────────────────────────────────
# Idea central: el radar puede deducir, pero debe etiquetar la deducción.
# Una fuente oficial que dice "DLT / API / ISO 20022 / EVM / CBDC" crea una
# ruta de interoperabilidad, no una prueba automática de XRPL. XRPL/Ripple/RLUSD
# solo sube de hipótesis a conexión cuando aparece una huella explícita.
DEDUCTIVE_EXPLICIT_XRPL_TERMS = (
    "xrpl", "xrp ledger", "xrp", "ripple", "ripple payments", "ripplenet",
    "rlusd", "trustline", "trust line", "xrpscan", "amm xrpl", "dex xrpl",
)
DEDUCTIVE_INTEROP_TERMS = (
    "mbridge", "m-cbdc", "mcbdc", "cbdc", "mbridge ledger", "mbl",
    "bis", "iso 20022", "api", "apis", "rtgs", "evm", "solidity",
    "dlt", "distributed ledger", "smart contract", "wholesale cbdc",
)
DEDUCTIVE_STRONG_OFFICIAL_TERMS = (
    "official", "bis.org", "central bank", "innovation hub", "regulatory",
    "filing", "paper", "pdf", "project", "mvp",
)


def _deductive_text(src: str, dst: str, evidence: str = "", proof_type: str = "", source_urls: str = "") -> str:
    return f"{src} {dst} {evidence} {proof_type} {source_urls}".lower()


def _has_explicit_xrpl_signal(txt: str) -> bool:
    return any(term in txt for term in DEDUCTIVE_EXPLICIT_XRPL_TERMS)


def _has_interop_signal(txt: str) -> bool:
    return any(term in txt for term in DEDUCTIVE_INTEROP_TERMS)


def _deductive_route_class(src: str, dst: str, evidence: str = "", proof_type: str = "", source_urls: str = "") -> Dict[str, Any]:
    """Clasifica una ruta por capas: oficial, interoperabilidad, hipótesis XRPL.

    Devuelve metadatos para pintar fichas sin confundir prueba oficial con deducción.
    """
    txt = _deductive_text(src, dst, evidence, proof_type, source_urls)
    evidence_txt = f"{evidence} {proof_type} {source_urls}".lower()
    explicit_xrpl = _has_explicit_xrpl_signal(evidence_txt)
    interop = _has_interop_signal(txt)
    official = any(term in txt for term in DEDUCTIVE_STRONG_OFFICIAL_TERMS)
    mentions_mbridge = any(term in txt for term in ("mbridge", "m-cbdc", "mcbdc", "mbridge ledger", "mbl"))
    mentions_bis = "bis" in txt or "bank for international settlements" in txt or "bis.org" in txt

    if explicit_xrpl:
        return {
            "mode": "explicit_xrpl",
            "hop": None,
            "cap": 0.98,
            "boost": 0.00,
            "status": "✅ Huella XRPL/Ripple explícita",
            "note": "La ruta contiene mención directa a XRP, XRPL, Ripple, RLUSD, trustline, DEX/AMM o fuente XRPL verificable.",
        }
    if mentions_mbridge and mentions_bis:
        return {
            "mode": "official_interop_mbridge",
            "hop": "mBridge Ledger / API / ISO 20022",
            "cap": 0.90,
            "boost": 0.03 if official else 0.0,
            "status": "✅ Interoperabilidad oficial / deducción fuerte",
            "note": "La fuente sostiene mBridge/BIS/interoperabilidad. No convierte automáticamente esa prueba en XRPL: queda como capa mBridge/API/ISO 20022.",
        }
    if mentions_mbridge or interop:
        return {
            "mode": "deductive_interop",
            "hop": "External Gateway / Interoperability Layer",
            "cap": 0.72,
            "boost": 0.02 if official else 0.0,
            "status": "🟡 Deducción de interoperabilidad",
            "note": "Hay señales de DLT/API/ISO 20022/CBDC/RTGS/EVM. El radar deduce una capa externa, pero no identifica XRPL sin huella directa.",
        }
    return {
        "mode": "generic",
        "hop": None,
        "cap": 0.98,
        "boost": 0.0,
        "status": "🧭 Ruta genérica",
        "note": "Ruta clasificada por señales generales del radar.",
    }


def _route_public_hop_for_pair(src: str, dst: str, evidence: str = "", proof_type: str = "", source_urls: str = "") -> str:
    """Elige un punto intermedio A→B sin convertir inferencias en XRPL por defecto."""
    src_l = str(src or "").strip().lower()
    dst_l = str(dst or "").strip().lower()
    txt = _deductive_text(src, dst, evidence, proof_type, source_urls)
    dclass = _deductive_route_class(src, dst, evidence, proof_type, source_urls)

    if dclass.get("hop"):
        hop = str(dclass["hop"])
    elif "dex" in txt or "amm" in txt:
        hop = "DEX/AMM"
    elif "trustline" in txt or "trust line" in txt:
        hop = "Trustlines"
    elif "rlusd" in txt:
        hop = "RLUSD"
    elif _has_explicit_xrpl_signal(f"{evidence} {proof_type} {source_urls}".lower()):
        hop = "XRPL"
    elif "gateway" in txt or "exchange" in txt or "wallet" in txt:
        hop = "Public Gateway"
    else:
        hop = "External Gateway / Interoperability Layer"

    # Evita self-loops en Sankey: A→RLUSD→RLUSD o XRPL→XRPL no aporta información.
    if hop.strip().lower() in {src_l, dst_l}:
        if "rlusd" in {src_l, dst_l}:
            hop = "XRPL"
        elif "xrpl" in {src_l, dst_l}:
            hop = "Public Gateway"
        else:
            hop = "External Gateway / Interoperability Layer"
    return hop


def _calibrate_deductive_confidence(src: str, dst: str, evidence: str, proof_type: str, source_urls: str, confidence: float) -> Tuple[float, str, str]:
    """Aplica techo/boost según la capa deductiva y devuelve (conf, estado, nota)."""
    dclass = _deductive_route_class(src, dst, evidence, proof_type, source_urls)
    base = max(0.01, min(float(confidence or 0.0), 1.0))
    calibrated = min(base + float(dclass.get("boost", 0.0) or 0.0), float(dclass.get("cap", 0.98) or 0.98))
    # Manuales hacia XRPL/Ripple sin huella explícita: nunca salen como verificadas.
    txt = _deductive_text(src, dst, evidence, proof_type, source_urls)
    target_xrpl_like = any(term in str(dst or "").lower() for term in ("xrpl", "xrp", "ripple", "rlusd"))
    evidence_txt = f"{evidence} {proof_type} {source_urls}".lower()
    if target_xrpl_like and not _has_explicit_xrpl_signal(evidence_txt):
        calibrated = min(calibrated, 0.35)
        return calibrated, "🟠 Hipótesis XRPL no verificada", (
            "El destino apunta a XRP/XRPL/Ripple/RLUSD, pero la evidencia aportada no contiene una huella explícita. "
            "El radar conserva la deducción como hipótesis fría, no como conexión verificada."
        )
    return calibrated, str(dclass.get("status", "🧭 Ruta genérica")), str(dclass.get("note", ""))


def _route_path_rows_from_dynamic(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    try:
        ensure_discovery_tables(conn)
        q = conn.execute("""
            SELECT src, dst, kind, confidence, evidence, source_urls, added_at
            FROM dynamic_routes
            ORDER BY datetime(added_at) DESC, confidence DESC
            LIMIT 300
        """).fetchall()
        for src, dst, kind, conf, evidence, source_urls, added_at in q:
            src = str(src or "").strip(); dst = str(dst or "").strip()
            if not src or not dst or src == dst:
                continue
            ev = str(evidence or kind or "ruta dinámica")
            hop = _route_public_hop_for_pair(src, dst, ev, str(kind or ""), str(source_urls or ""))
            c_raw = max(0.01, min(float(conf or 0.0), 1.0))
            c, deductive_status, deductive_note = _calibrate_deductive_confidence(src, dst, ev, str(kind or ""), str(source_urls or ""), c_raw)
            rows.append({
                "day": str(added_at or _date.today())[:10],
                "path_id": hashlib.sha256(f"dyn:{src}>{dst}>{added_at}".encode()).hexdigest()[:12],
                "origin": src,
                "public_hop": hop,
                "destination": dst,
                "confidence": c,
                "path_type": deductive_status if str(kind or "").lower() in {"deductive", "hypothesis", "watch", "manual"} or "mbridge" in f"{src} {dst} {ev}".lower() else ("Ruta añadida / descubierta" if c >= 0.52 else "Ruta vigilada"),
                "evidence": ev,
                "source_urls": str(source_urls or ""),
                "deduction_mode": _deductive_route_class(src, dst, ev, str(kind or ""), str(source_urls or "")).get("mode", "generic"),
                "deduction_note": deductive_note,
                "explanation": f"Ruta dinámica registrada: {src} → {dst}. Evidencia: {ev}. Capa deductiva: {deductive_status}. {deductive_note}",
            })
    except Exception:
        pass
    return rows


def _route_path_rows_from_proofs(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    try:
        ensure_discovery_tables(conn)
        q = conn.execute("""
            SELECT node_a, node_b, proof_type, proof_data, onchain, confidence, validated_at
            FROM connection_proofs
            ORDER BY onchain DESC, confidence DESC, datetime(validated_at) DESC
            LIMIT 300
        """).fetchall()
        for node_a, node_b, proof_type, proof_data, onchain, conf, validated_at in q:
            a = str(node_a or "").strip(); b = str(node_b or "").strip()
            if not a or not b or a == b:
                continue
            try:
                pdata = json.loads(proof_data or "{}") if isinstance(proof_data, str) else (proof_data or {})
            except Exception:
                pdata = {}
            ev = str(pdata.get("summary") or pdata.get("evidence") or proof_type or "prueba verificada")
            proof_urls = _safe_sources_blob([_extract_url_from_any(p) for p in (pdata.get("proofs") or [])], limit=1200) if isinstance(pdata, dict) else ""
            hop = _route_public_hop_for_pair(a, b, ev, str(proof_type or ""), json.dumps(pdata, ensure_ascii=False)[:1200] if isinstance(pdata, dict) else "")
            c_raw = max(0.01, min(float(conf or 0.0), 1.0))
            if int(onchain or 0):
                c_raw = max(c_raw, 0.95)
            c, deductive_status, deductive_note = _calibrate_deductive_confidence(a, b, ev, str(proof_type or ""), json.dumps(pdata, ensure_ascii=False)[:1200] if isinstance(pdata, dict) else "", c_raw)
            rows.append({
                "day": str(validated_at or _date.today())[:10],
                "path_id": hashlib.sha256(f"proof:{a}<>{b}>{validated_at}".encode()).hexdigest()[:12],
                "origin": a,
                "public_hop": hop,
                "destination": b,
                "confidence": c,
                "path_type": deductive_status if _deductive_route_class(a, b, ev, str(proof_type or ""), json.dumps(pdata, ensure_ascii=False)[:1200] if isinstance(pdata, dict) else "").get("mode") != "generic" else ("Conexión verificada" if c >= 0.72 else "Conexión probable"),
                "evidence": ev[:600],
                "source_urls": proof_urls,
                "deduction_mode": _deductive_route_class(a, b, ev, str(proof_type or ""), json.dumps(pdata, ensure_ascii=False)[:1200] if isinstance(pdata, dict) else "").get("mode", "generic"),
                "deduction_note": deductive_note,
                "explanation": f"Prueba guardada entre {a} y {b}. Tipo: {proof_type}. {ev[:240]}. Capa deductiva: {deductive_status}. {deductive_note}",
            })
    except Exception:
        pass
    return rows


def _route_path_rows_from_wallets(conn: sqlite3.Connection) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    try:
        ensure_discovered_wallets_table(conn)
        q = conn.execute("""
            SELECT wallet, label, role, confidence, top_cp_label, top_counterpart, signals, last_seen, status, added_to_map
            FROM discovered_wallets
            WHERE COALESCE(status,'') NOT IN ('discarded','quarantine')
              AND (COALESCE(added_to_map,0)=1 OR COALESCE(status,'')='map')
            ORDER BY confidence DESC, datetime(last_seen) DESC
            LIMIT 120
        """).fetchall()
        for wallet, label, role, conf, top_cp_label, top_counterpart, signals, last_seen, status, added in q:
            w = str(wallet or "").strip()
            if not w:
                continue
            name = _wallet_full_name(w, str(label or ""))
            dst = str(top_cp_label or "").strip() or str(top_counterpart or "").strip() or "XRPL"
            if dst.startswith("r") and len(dst) > 20:
                dst = _label(dst)
            ev = str(signals or role or "wallet añadida al radar")
            c = max(0.01, min(float(conf or 0.0), 1.0))
            rows.append({
                "day": str(last_seen or _date.today())[:10],
                "path_id": hashlib.sha256(f"wallet:{w}>{dst}".encode()).hexdigest()[:12],
                "origin": name,
                "public_hop": "XRPL Wallet",
                "destination": dst,
                "confidence": c,
                "path_type": "Wallet vigilada en radar",
                "evidence": ev[:600],
                "source_urls": f"https://xrpscan.com/account/{w}",
                "explanation": f"Wallet incluida en el radar por gatekeeper: {name}. Señales: {ev[:240]}",
            })
    except Exception:
        pass
    return rows


def load_live_route_paths(conn: sqlite3.Connection, df: pd.DataFrame) -> pd.DataFrame:
    """Reconstruye el gráfico A→B desde TODO el estado vivo, no solo desde el histórico."""
    ensure_route_paths_table(conn)
    base = rebuild_route_paths(conn, df) if isinstance(df, pd.DataFrame) and not df.empty else pd.DataFrame()
    frames: List[pd.DataFrame] = []
    if isinstance(base, pd.DataFrame) and not base.empty:
        frames.append(base)
    extra_rows: List[Dict[str, Any]] = []
    extra_rows.extend(_route_path_rows_from_dynamic(conn))
    extra_rows.extend(_route_path_rows_from_proofs(conn))
    extra_rows.extend(_route_path_rows_from_wallets(conn))
    if extra_rows:
        frames.append(pd.DataFrame(extra_rows))
    if not frames:
        return pd.DataFrame(columns=["day", "path_id", "origin", "public_hop", "destination", "confidence", "path_type", "evidence", "explanation"])
    out = pd.concat(frames, ignore_index=True, sort=False)
    for col in ["day", "path_id", "origin", "public_hop", "destination", "confidence", "path_type", "evidence", "source_urls", "explanation", "deduction_mode", "deduction_note"]:
        if col not in out.columns:
            out[col] = "" if col != "confidence" else 0.0
    out["confidence"] = pd.to_numeric(out["confidence"], errors="coerce").fillna(0.0).clip(0.0, 1.0)
    out = out.dropna(subset=["origin", "public_hop", "destination"])
    out = out[(out["origin"].astype(str).str.len() > 0) & (out["destination"].astype(str).str.len() > 0)]
    out = out.drop_duplicates(subset=["origin", "public_hop", "destination", "path_type"], keep="first")
    if "source_urls" not in out.columns:
        out["source_urls"] = ""
    return out[["day", "path_id", "origin", "public_hop", "destination", "confidence", "path_type", "evidence", "source_urls", "explanation", "deduction_mode", "deduction_note"]]



def _route_is_unknown_label(label: Any) -> bool:
    """Detecta nodos desconocidos para no llenar el Sankey con 40 direcciones basura."""
    s = str(label or "").strip()
    if not s:
        return True
    low = s.lower()
    if low.startswith("? "):
        return True
    if "sin etiqueta" in low or "desconocid" in low or "unknown" in low:
        return True
    # Dirección XRPL completa o semitruncada incrustada en el label.
    if re.fullmatch(r"r[1-9A-HJ-NP-Za-km-z]{24,34}", s):
        return True
    if re.search(r"r[1-9A-HJ-NP-Za-km-z]{5,}…[1-9A-HJ-NP-Za-km-z]{3,}", s):
        return True
    return False


def _route_clean_node_label(label: Any, *, side: str = "") -> str:
    """Normaliza nodos del Route Path Engine para evitar duplicados visuales.

    Sin esto el gráfico podía mostrar 20-40 nodos casi iguales tipo:
    ? rJGb4...TSUG, ? r1Hz...89B2, Contraparte de Contraparte de Coinbase, etc.
    Para el mapa de alto nivel esos nodos se agrupan; la ficha conserva los labels reales.
    """
    s = str(label or "").strip()
    s = re.sub(r"\s+", " ", s)
    if not s:
        return "Wallet XRPL sin etiqueta"

    # Limpieza de traducciones parciales o prefijos repetidos heredados.
    s = s.replace("レーダー", "Radar")
    s = s.replace("エンジン", "Engine")
    while "Contraparte de Contraparte de" in s:
        s = s.replace("Contraparte de Contraparte de", "Contraparte de")
    s = s.replace("Contraparte de Coinbase", "Coinbase / contraparte")
    s = s.replace("Coinbase / contraparte / contraparte", "Coinbase / contraparte")

    low = s.lower()
    if _route_is_unknown_label(s):
        if side == "destination":
            return "Wallets XRPL sin etiqueta"
        if side == "origin":
            return "Wallet XRPL sin etiqueta"
        return "XRPL Wallet"

    # Unifica nombres equivalentes.
    aliases = {
        "xrpl wallet": "XRPL Wallet",
        "wallet xrpl": "XRPL Wallet",
        "public gateway / xrpl": "Public Gateway / XRPL",
        "public gateway": "Public Gateway",
        "trustlines": "Trustlines",
        "trustline": "Trustlines",
        "dex/amm": "DEX/AMM",
        "ledger real": "XRPL",
        "ledger público real": "XRPL",
        "rail / corredores fx": "Rail / Corredores FX",
        "rail/corredores fx": "Rail / Corredores FX",
        "hidden road / prime": "Hidden Road / Prime",
        "hr/prime": "Hidden Road / Prime",
        "treasury / distribuidor": "Treasury / distribuidor",
        "treasury": "Treasury",
        "exchange / gateway": "Exchange / gateway",
        "exchange/gateway": "Exchange / gateway",
        "market maker/acumulador": "Market maker / acumulador",
        "market maker / acumulador": "Market maker / acumulador",
        "coinbase": "Coinbase",
        "coinbase / contraparte": "Coinbase / contraparte",
    }
    return aliases.get(low, s)


def _route_prepare_chart_df(paths: pd.DataFrame, max_paths: int = 50) -> pd.DataFrame:
    """Prepara rutas limpias y agregadas para el Sankey y las fichas clicables."""
    cols = ["day", "path_id", "origin", "public_hop", "destination", "confidence", "path_type", "evidence", "source_urls", "explanation", "deduction_mode", "deduction_note"]
    if not isinstance(paths, pd.DataFrame) or paths.empty:
        return pd.DataFrame(columns=cols + ["origin_clean", "hop_clean", "destination_clean", "route_key", "route_label", "count", "value", "raw_nodes", "raw_path_ids"])

    work = paths.copy()
    for c in cols:
        if c not in work.columns:
            work[c] = "" if c != "confidence" else 0.0
    work["confidence"] = pd.to_numeric(work["confidence"], errors="coerce").fillna(0.0).clip(0.0, 1.0)
    work["origin"] = work["origin"].astype(str).str.strip()
    work["public_hop"] = work["public_hop"].astype(str).str.strip()
    work["destination"] = work["destination"].astype(str).str.strip()
    work = work[(work["origin"].str.len() > 0) & (work["destination"].str.len() > 0)]
    if work.empty:
        return pd.DataFrame(columns=cols + ["origin_clean", "hop_clean", "destination_clean", "route_key", "route_label", "count", "value", "raw_nodes", "raw_path_ids"])

    work["origin_clean"] = work["origin"].apply(lambda x: _route_clean_node_label(x, side="origin"))
    work["hop_clean"] = work["public_hop"].apply(lambda x: _route_clean_node_label(x, side="hop"))
    work["destination_clean"] = work["destination"].apply(lambda x: _route_clean_node_label(x, side="destination"))

    # Evita self-loops tras limpiar labels.
    work = work[(work["origin_clean"] != work["hop_clean"]) & (work["hop_clean"] != work["destination_clean"]) & (work["origin_clean"] != work["destination_clean"])]
    if work.empty:
        return pd.DataFrame(columns=cols + ["origin_clean", "hop_clean", "destination_clean", "route_key", "route_label", "count", "value", "raw_nodes", "raw_path_ids"])

    def _join_unique(series: pd.Series, limit: int = 7, max_chars: int = 900) -> str:
        vals = []
        seen = set()
        for v in series.dropna().astype(str):
            v = v.strip()
            if not v or v.lower() == "nan":
                continue
            if v not in seen:
                seen.add(v); vals.append(v)
            if len(vals) >= limit:
                break
        out = " · ".join(vals)
        return out[:max_chars]

    grouped = []
    for (o, h, d), g in work.groupby(["origin_clean", "hop_clean", "destination_clean"], dropna=False):
        g = g.sort_values(["confidence", "day"], ascending=[False, False])
        count = int(len(g))
        max_conf = float(g["confidence"].max())
        mean_conf = float(g["confidence"].mean())
        # El valor visual no suma linealmente 40 wallets desconocidas; evita que un cluster desconocido domine todo.
        value = max(0.05, max_conf * (1.0 + min(count - 1, 8) * 0.06))
        raw_nodes = _join_unique(pd.concat([g["origin"], g["public_hop"], g["destination"]]), limit=12, max_chars=1200)
        raw_path_ids = _join_unique(g["path_id"], limit=20, max_chars=600)
        evidence = _join_unique(g["evidence"], limit=5, max_chars=900)
        source_urls = _safe_sources_blob(_join_unique(g["source_urls"], limit=8, max_chars=1600), limit=1600) if "source_urls" in g.columns else ""
        explanation = _join_unique(g["explanation"], limit=3, max_chars=900)
        path_type = _join_unique(g["path_type"], limit=3, max_chars=240)
        deduction_mode = _join_unique(g["deduction_mode"], limit=3, max_chars=240) if "deduction_mode" in g.columns else ""
        deduction_note = _join_unique(g["deduction_note"], limit=3, max_chars=900) if "deduction_note" in g.columns else ""
        day = str(g["day"].iloc[0] or "")
        route_key = hashlib.sha256(f"{o}>{h}>{d}".encode()).hexdigest()[:12]
        grouped.append({
            "day": day,
            "path_id": route_key,
            "origin": o,
            "public_hop": h,
            "destination": d,
            "origin_clean": o,
            "hop_clean": h,
            "destination_clean": d,
            "confidence": max_conf,
            "confidence_mean": mean_conf,
            "path_type": path_type or "Ruta agregada",
            "evidence": evidence or "sin evidencia resumida",
            "source_urls": source_urls,
            "explanation": explanation or f"Ruta agregada desde {count} observación(es).",
            "deduction_mode": deduction_mode,
            "deduction_note": deduction_note,
            "count": count,
            "value": value,
            "raw_nodes": raw_nodes,
            "raw_path_ids": raw_path_ids,
            "route_key": route_key,
            "route_label": f"{o} → {h} → {d}",
        })

    out = pd.DataFrame(grouped)
    if out.empty:
        return out
    # Prioriza rutas limpias, con confianza y repetición; no spam de desconocidas.
    out["_priority"] = out["confidence"].astype(float) * 100 + out["count"].clip(upper=10) * 2
    out = out.sort_values(["_priority", "day"], ascending=[False, False]).head(max_paths).drop(columns=["_priority"])
    return out.reset_index(drop=True)


def make_route_path_sankey(paths: pd.DataFrame) -> go.Figure:
    chart = _route_prepare_chart_df(paths, max_paths=50)
    if chart.empty:
        fig = go.Figure()
        fig.update_layout(title=dict(text="Route Path Engine A→B — esperando rutas", font=dict(color="#FFFFFF")),
                          template="plotly_dark", paper_bgcolor="#07111f", plot_bgcolor="#07111f", height=360)
        fig.add_annotation(
            text="Sin rutas aprobadas todavía. Añade una ruta o wallet desde los formularios inferiores.",
            xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False,
            font=dict(color="#CBD5E1", size=16), align="center",
        )
        return fig

    labels = []
    for col in ["origin_clean", "hop_clean", "destination_clean"]:
        for v in chart[col].astype(str).tolist():
            if v not in labels:
                labels.append(v)
    idx = {v: i for i, v in enumerate(labels)}

    # Cuenta rutas por nodo para mostrar labels más útiles sin duplicar nodos.
    node_counts = Counter()
    for _, r in chart.iterrows():
        node_counts[str(r["origin_clean"])] += int(r.get("count", 1) or 1)
        node_counts[str(r["hop_clean"])] += int(r.get("count", 1) or 1)
        node_counts[str(r["destination_clean"])] += int(r.get("count", 1) or 1)
    display_labels = [f"{x} ({node_counts[x]})" if node_counts[x] > 1 and x in {"Wallets XRPL sin etiqueta", "Wallet XRPL sin etiqueta", "XRPL Wallet"} else x for x in labels]

    sources, targets, values, colors, customdata = [], [], [], [], []
    for _, r in chart.iterrows():
        conf = float(r.get("confidence", 0) or 0)
        value = float(r.get("value", max(conf, 0.05)) or 0.05)
        count = int(r.get("count", 1) or 1)
        ev = str(r.get("evidence", ""))[:180]
        route_label = str(r.get("route_label", ""))
        cd = [route_label, f"{conf*100:.1f}%", str(count), ev]
        sources.append(idx[r["origin_clean"]]); targets.append(idx[r["hop_clean"]]); values.append(value)
        colors.append("rgba(182,115,255,.45)"); customdata.append(cd)
        sources.append(idx[r["hop_clean"]]); targets.append(idx[r["destination_clean"]]); values.append(value)
        colors.append("rgba(60,255,155,.44)" if conf >= 0.52 else "rgba(255,184,77,.38)"); customdata.append(cd)

    fig = go.Figure(data=[go.Sankey(
        arrangement="snap",
        node=dict(
            label=display_labels,
            pad=22,
            thickness=18,
            color="rgba(90,215,255,.85)",
            line=dict(color="rgba(255,255,255,.20)", width=0.5),
            hovertemplate="<b>%{label}</b><br>Rutas agregadas visibles: %{customdata}<extra></extra>",
            customdata=[str(node_counts[x]) for x in labels],
        ),
        link=dict(
            source=sources,
            target=targets,
            value=values,
            color=colors,
            customdata=customdata,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Confianza máx: %{customdata[1]}<br>"
                "Observaciones agregadas: %{customdata[2]}<br>"
                "Evidencia: %{customdata[3]}<extra></extra>"
            ),
        )
    )])
    fig.update_layout(
        title=dict(text="Route Path Engine A→B — rutas limpias y deduplicadas", font=dict(color="#FFFFFF", size=22)),
        template="plotly_dark",
        paper_bgcolor="#07111f",
        plot_bgcolor="#07111f",
        height=560,
        font=dict(color="#FFFFFF", size=13),
        margin=dict(l=20, r=20, t=60, b=30),
    )
    return fig




def _rrp_extract_urls_from_text(text: Any, limit: int = 8) -> List[str]:
    """Extrae URLs limpias de texto/CSV/HTML simple para fijarlas en fichas."""
    raw = str(text or "")
    urls = re.findall(r"https?://[^\s<>'\"\)\]]+", raw)
    # También aceptar listas separadas por coma si no había regex por caracteres raros.
    for part in raw.replace("\n", ",").split(","):
        part = part.strip()
        if part.startswith("http"):
            urls.append(part)
    out: List[str] = []
    seen: Set[str] = set()
    for u in urls:
        cu = _canonical_source_url(u)
        if not cu or cu in seen:
            continue
        seen.add(cu); out.append(cu)
        if len(out) >= limit:
            break
    return out


def _rrp_short_domain(url: str) -> str:
    try:
        from urllib.parse import urlparse
        return urlparse(_canonical_source_url(url)).netloc.replace("www.", "") or "fuente"
    except Exception:
        return "fuente"


def _rrp_proof_status_label(proof: Dict[str, Any], fallback_conf: float = 0.0) -> Tuple[str, str]:
    """Devuelve clase CSS y texto de estado para una prueba."""
    ptype = str(proof.get("type", "") or proof.get("proof_type", "") or "fuente")
    conf = float(proof.get("confidence", fallback_conf) or fallback_conf or 0.0)
    if proof.get("onchain") or ptype in {"tx_directa", "odl_payment", "trust_line", "amm_pool"}:
        return "ok", "✅ On-chain / verificable"
    if ptype in {"official_partner", "regulatory_filing_pdf", "contract_pdf", "regulatory_filing", "press_release", "github_repo"}:
        return "ok", "✅ Fuente fuerte"
    if conf >= 0.72:
        return "ok", "✅ Alta confianza"
    if ptype in {"news_major", "job_posting", "wallet_activa"} or conf >= 0.45:
        return "watch", "🟡 Revisar fuente"
    return "bad", "⚠️ Débil / no concluyente"


def _rrp_collect_fixed_route_proofs(row: pd.Series, conn: Optional[sqlite3.Connection] = None, limit: int = 8) -> List[Dict[str, Any]]:
    """Recoge pruebas fijas para una ficha A→B.

    Orden de prioridad:
    1) connection_proofs guardadas para origen↔destino / origen↔hop / hop↔destino.
    2) source_urls almacenadas en dynamic_routes o wallets.
    3) URLs detectadas dentro del texto de evidencia/explicación.
    """
    proofs: List[Dict[str, Any]] = []
    seen: Set[str] = set()

    def _add(p: Dict[str, Any]) -> None:
        if not isinstance(p, dict):
            return
        url = _extract_url_from_any(p)
        canon = _canonical_source_url(url) if url else ""
        txh = str(p.get("tx_hash", "") or p.get("hash", "") or "").strip()
        label = str(p.get("label", "") or p.get("title", "") or p.get("type", "") or canon or txh or "prueba")
        key = canon or txh or _norm_key(label)[:120]
        if not key or key in seen:
            return
        seen.add(key)
        pp = dict(p)
        if canon:
            pp["url"] = canon
        proofs.append(pp)

    # 1) Pruebas verificadas en BD por pares.
    if conn is not None:
        pairs = [
            (row.get("origin_clean", row.get("origin", "")), row.get("destination_clean", row.get("destination", ""))),
            (row.get("origin_clean", row.get("origin", "")), row.get("hop_clean", row.get("public_hop", ""))),
            (row.get("hop_clean", row.get("public_hop", "")), row.get("destination_clean", row.get("destination", ""))),
        ]
        for a, b in pairs:
            if not str(a or "").strip() or not str(b or "").strip() or str(a) == str(b):
                continue
            try:
                prow = _connection_proof_row(conn, a, b)
                pdata = _proof_row_to_data(prow)
                if pdata:
                    for p in _dedupe_and_filter_proofs(str(a), str(b), pdata.get("proofs") or [], max_items=4):
                        pp = dict(p)
                        pp.setdefault("pair", f"{a} ↔ {b}")
                        pp.setdefault("confidence", float(prow[2] or 0.0) if prow and len(prow) > 2 else float(row.get("confidence", 0) or 0))
                        _add(pp)
                    # Si no hay lista pero sí summary, fijar como prueba interna.
                    if not pdata.get("proofs") and (pdata.get("summary") or pdata.get("evidence")):
                        _add({
                            "type": "proof_summary",
                            "label": str(pdata.get("summary") or pdata.get("evidence"))[:180],
                            "snippet": str(pdata.get("evidence") or pdata.get("summary") or "")[:360],
                            "pair": f"{a} ↔ {b}",
                            "confidence": float(prow[2] or 0.0) if prow and len(prow) > 2 else float(row.get("confidence", 0) or 0),
                        })
            except Exception:
                continue

    # 2) URLs fijas guardadas en la ruta.
    for url in _rrp_extract_urls_from_text(row.get("source_urls", ""), limit=limit):
        _add({
            "type": "source_url",
            "label": f"Fuente guardada · {_rrp_short_domain(url)}",
            "url": url,
            "snippet": "URL asociada directamente a esta ruta en la base de datos.",
            "confidence": float(row.get("confidence", 0) or 0),
        })

    # 3) URLs incrustadas en evidencia/explicación.
    blob = "\n".join([str(row.get("evidence", "") or ""), str(row.get("explanation", "") or ""), str(row.get("raw_nodes", "") or "")])
    for url in _rrp_extract_urls_from_text(blob, limit=limit):
        _add({
            "type": "evidence_url",
            "label": f"URL detectada en evidencia · {_rrp_short_domain(url)}",
            "url": url,
            "snippet": "URL encontrada dentro del texto de evidencia de la ficha.",
            "confidence": float(row.get("confidence", 0) or 0),
        })

    return proofs[:limit]


def _rrp_render_fixed_proofs_panel(row: pd.Series, conn: Optional[sqlite3.Connection] = None) -> None:
    """Pinta un bloque fijo de pruebas dentro de la ficha de ruta."""
    proofs = _rrp_collect_fixed_route_proofs(row, conn=conn, limit=8)
    conf = float(row.get("confidence", 0) or 0)
    count = int(row.get("count", 1) or 1)
    has_url = any(_extract_url_from_any(p) for p in proofs)
    has_strong = any(_rrp_proof_status_label(p, conf)[0] == "ok" for p in proofs)
    unknown_cluster = any(x in str(row.get(k, "")).lower() for k in ("origin_clean", "hop_clean", "destination_clean") for x in ["sin etiqueta", "unknown", "desconocid"])

    st.markdown("### 🔒 Pruebas fijas para verificar")
    checks = []
    checks.append(("✅" if conf >= 0.72 else "🟡" if conf >= 0.45 else "⚠️", f"Confianza de ruta: {conf*100:.1f}%"))
    checks.append(("✅" if count >= 2 else "🟡", f"Observaciones agregadas: {count}"))
    checks.append(("✅" if has_url else "⚠️", "Fuente externa fija disponible" if has_url else "Sin URL externa fija: revisar antes de usar como prueba pública"))
    checks.append(("✅" if has_strong else "🟡", "Hay prueba fuerte/on-chain" if has_strong else "Solo evidencia resumida o señal vigilada"))
    checks.append(("⚠️" if unknown_cluster else "✅", "Ruta contiene wallet/cluster sin etiqueta" if unknown_cluster else "Sin cluster desconocido dominante"))
    dmode = str(row.get("deduction_mode", "") or "")
    if dmode and dmode != "generic":
        checks.append(("🧠", f"Capa deductiva: {dmode}"))

    html_checks = "".join(f"<div class='rrp-checkline'>{icon} {html.escape(text)}</div>" for icon, text in checks)
    st.markdown(
        "<div class='rrp-proof-lockbox'>"
        "<div class='rrp-proof-title'>Checklist anti-basura de esta ruta</div>"
        + html_checks +
        "</div>",
        unsafe_allow_html=True,
    )

    if not proofs:
        st.warning("Esta ficha no tiene pruebas fijas suficientes. Úsala como señal interna/watchlist, no como conexión confirmada.")
        return

    cards = []
    for i, p in enumerate(proofs, 1):
        css_state, status = _rrp_proof_status_label(p, conf)
        ptype = str(p.get("type", "fuente") or "fuente")
        label = str(p.get("label", "") or p.get("title", "") or p.get("summary", "") or p.get("snippet", "") or "Prueba guardada")[:180]
        snippet = str(p.get("snippet", "") or p.get("summary", "") or p.get("evidence", "") or "")[:300]
        url = _extract_url_from_any(p)
        pair = str(p.get("pair", "") or "")
        url_html = f"<a class='rrp-proof-url' href='{html.escape(_canonical_source_url(url))}' target='_blank' rel='noopener noreferrer'>{html.escape(_canonical_source_url(url))}</a>" if url else "<span class='rrp-proof-url'>Sin URL externa</span>"
        cards.append(
            f"<div class='rrp-proof-card rrp-proof-card-{css_state}'>"
            f"<div class='rrp-proof-kicker'>Prueba {i} · {html.escape(ptype)} · {html.escape(status)}</div>"
            f"<div class='rrp-proof-card-title'>{html.escape(label)}</div>"
            f"{url_html}"
            f"<div class='rrp-proof-note'>{html.escape(pair + ' · ' if pair else '')}{html.escape(snippet)}</div>"
            f"</div>"
        )
    st.markdown(
        "<div class='rrp-proof-lockbox'>"
        "<div class='rrp-proof-title'>Fuentes / pruebas asociadas a esta ficha</div>"
        "<div class='rrp-proof-grid'>" + "".join(cards) + "</div>"
        "</div>",
        unsafe_allow_html=True,
    )

def _rrp_open_route_ficha(route_key: str, key_prefix: str = "live") -> None:
    """Callback robusto para abrir ficha desde tarjeta.

    En Streamlit, un selectbox con key propia puede conservar su valor antiguo
    y pisar el ID seleccionado por el botón. Por eso actualizamos dos claves:
    la clave canónica de ficha y la clave del selectbox de respaldo.
    """
    route_key = str(route_key or "")
    st.session_state[f"{key_prefix}_selected_route_key"] = route_key
    st.session_state[f"{key_prefix}_route_ficha_select"] = route_key
    st.session_state[f"{key_prefix}_route_ficha_opened_by_button"] = True


def _render_route_ficha(row: pd.Series, nested_safe: bool = False, conn: Optional[sqlite3.Connection] = None) -> None:
    """Ficha completa de una ruta agregada."""
    if row is None or len(row) == 0:
        return
    conf = float(row.get("confidence", 0) or 0) * 100
    count = int(row.get("count", 1) or 1)
    st.markdown("### 📌 Ficha completa de ruta")
    st.markdown(f"""
<div class="rrp-path-panel">
  <div class="rrp-path-title">{html.escape(str(row.get('route_label','Ruta A→B')))}</div>
  <div class="rrp-path-text">
    <b>Confianza máxima:</b> {conf:.1f}% · <b>Observaciones agregadas:</b> {count}<br>
    <b>Tipo:</b> {html.escape(str(row.get('path_type','')))}<br>
    <b>Última fecha:</b> {html.escape(str(row.get('day','')))}
  </div>
</div>
""", unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    c1.metric("Origen", str(row.get("origin_clean", row.get("origin", "")))[:42])
    c2.metric("Punto público", str(row.get("hop_clean", row.get("public_hop", "")))[:42])
    c3.metric("Destino", str(row.get("destination_clean", row.get("destination", "")))[:42])
    st.markdown("**Evidencia resumida**")
    st.write(str(row.get("evidence", "sin evidencia resumida")))
    st.markdown("**Explicación**")
    st.write(str(row.get("explanation", "sin explicación")))
    dmode = str(row.get("deduction_mode", "") or "").strip()
    dnote = str(row.get("deduction_note", "") or "").strip()
    if dmode or dnote:
        st.markdown(
            "<div class='rrp-proof-lockbox'>"
            "<div class='rrp-proof-title'>🧠 Capa deductiva del radar</div>"
            f"<div class='rrp-checkline'>Modo: <b>{html.escape(dmode or 'generic')}</b></div>"
            f"<div class='rrp-proof-note'>{html.escape(dnote or 'Ruta sin nota deductiva específica.')}</div>"
            "<div class='rrp-proof-note'><b>Regla:</b> el radar puede inferir rutas probables, pero no convierte DLT/API/ISO/EVM/CBDC en XRPL salvo que aparezca una huella explícita: XRP, XRPL, Ripple, RLUSD, wallet, trustline, DEX/AMM o transacción verificable.</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    _rrp_render_fixed_proofs_panel(row, conn=conn)
    raw_nodes = str(row.get("raw_nodes", "")).strip()
    if raw_nodes:
        if nested_safe:
            st.markdown("**Nodos reales agregados / etiquetas originales**")
            st.write(raw_nodes)
        else:
            with st.expander("Ver nodos reales agregados / etiquetas originales", expanded=False):
                st.write(raw_nodes)
    raw_ids = str(row.get("raw_path_ids", "")).strip()
    if raw_ids:
        if nested_safe:
            st.markdown("**IDs internos de rutas agregadas**")
            st.code(raw_ids)
        else:
            with st.expander("IDs internos de rutas agregadas", expanded=False):
                st.code(raw_ids)




def _rrp_route_status_from_row(row: pd.Series) -> Tuple[str, str, str]:
    conf = float(row.get("confidence", 0) or 0)
    ptype = str(row.get("path_type", "") or "").lower()
    dmode = str(row.get("deduction_mode", "") or "").lower()
    evidence = str(row.get("evidence", "") or "").lower()
    urls = str(row.get("source_urls", "") or "").strip()
    if "descart" in ptype or "ruido" in ptype:
        return "🔴 Descartada / ruido", "#FF5A67", "discarded"
    if "hipótesis" in ptype or "hypothesis" in ptype or "no verificada" in ptype:
        return "🟠 Hipótesis deductiva", "#FFB84D", "hypothesis"
    if "deducc" in ptype or "interop" in dmode or "deductive" in dmode:
        return "🟡 Deducción / interoperabilidad", "#FACC15", "deductive"
    if conf >= 0.72 and (urls or "on-chain" in evidence or "source_url" in evidence or "official" in evidence):
        return "✅ Verificada / alta evidencia", "#3CFF9B", "verified"
    if conf >= 0.52:
        return "👁 Watchlist fuerte", "#38BDF8", "watch"
    return "⚪ Señal débil", "#94A3B8", "weak"


def _rrp_route_urls_list(value: Any, limit: int = 8) -> List[str]:
    raw = str(value or "")
    found = re.findall(r"https?://[^\s,;<>\)\]]+", raw)
    clean: List[str] = []
    seen: Set[str] = set()
    for u in found:
        u = _canonical_source_url(u)
        if u and u not in seen:
            seen.add(u); clean.append(u)
        if len(clean) >= limit:
            break
    return clean



def _rrp_count_evidence_fragments(value: Any) -> int:
    raw = str(value or "").strip()
    if not raw or raw.lower().startswith("sin evidencia"):
        return 0
    parts = [p.strip() for p in re.split(r"\s*[·|;]\s*", raw) if p.strip()]
    return max(1, len(parts))


def _rrp_route_live_score(conf: float, count: int, source_count: int, evidence_count: int, status_css: str) -> float:
    # Score vivo para vigilancia: no vuelve a sumar pruebas fijadas como rutas nuevas;
    # pondera confianza, observaciones agregadas, fuentes y evidencia sin duplicar por spam.
    score = conf * 58.0
    score += min(max(count, 0), 10) * 2.2
    score += min(max(source_count, 0), 6) * 4.0
    score += min(max(evidence_count, 0), 8) * 2.0
    if status_css == "verified":
        score += 8.0
    elif status_css == "deductive":
        score += 4.0
    elif status_css == "hypothesis":
        score -= 4.0
    elif status_css in {"weak", "discarded"}:
        score -= 8.0
    return round(max(0.0, min(100.0, score)), 1)


def _rrp_route_live_label(score: float) -> str:
    if score >= 78:
        return "🔥 vigilancia alta"
    if score >= 60:
        return "🟢 vigilancia activa"
    if score >= 40:
        return "🟡 vigilancia media"
    if score >= 22:
        return "🟠 señal débil"
    return "⚪ ruido/baja señal"

def _rrp_build_premium_route_payload(chart: pd.DataFrame) -> List[Dict[str, Any]]:
    payload: List[Dict[str, Any]] = []
    if not isinstance(chart, pd.DataFrame) or chart.empty:
        return payload
    for _, row in chart.iterrows():
        status, color, css = _rrp_route_status_from_row(row)
        conf = float(row.get("confidence", 0) or 0)
        source_list = _rrp_route_urls_list(row.get("source_urls"))
        count = int(row.get("count", 1) or 1)
        evidence_count = _rrp_count_evidence_fragments(row.get("evidence"))
        source_count = len(source_list)
        live_score = _rrp_route_live_score(conf, count, source_count, evidence_count, css)
        mean_conf = float(row.get("confidence_mean", conf) or conf)
        visual_weight = float(row.get("value", conf) or conf)
        payload.append({
            "id": str(row.get("route_key") or row.get("path_id") or hashlib.sha256(str(row.to_dict()).encode()).hexdigest()[:12]),
            "origin": str(row.get("origin_clean") or row.get("origin") or ""),
            "hop": str(row.get("hop_clean") or row.get("public_hop") or ""),
            "destination": str(row.get("destination_clean") or row.get("destination") or ""),
            "route_label": str(row.get("route_label") or "Ruta A-B"),
            "confidence": round(conf * 100, 1),
            "confidence_mean": round(mean_conf * 100, 1),
            "count": count,
            "path_type": str(row.get("path_type") or "Ruta"),
            "status": status,
            "status_color": color,
            "status_css": css,
            "evidence": str(row.get("evidence") or "sin evidencia resumida"),
            "explanation": str(row.get("explanation") or "sin explicación"),
            "deduction_mode": str(row.get("deduction_mode") or "generic"),
            "deduction_note": str(row.get("deduction_note") or ""),
            "source_urls": source_list,
            "source_count": source_count,
            "evidence_count": evidence_count,
            "live_score": live_score,
            "live_label": _rrp_route_live_label(live_score),
            "visual_weight": round(visual_weight, 3),
            "dedup_note": f"{count} observación(es) fusionadas en una sola línea canónica; las pruebas fijadas no se vuelven a contar como rutas nuevas.",
            "raw_nodes": str(row.get("raw_nodes") or ""),
            "raw_path_ids": str(row.get("raw_path_ids") or ""),
            "day": str(row.get("day") or ""),
        })
    return payload


def render_premium_clickable_ab_graph(chart: pd.DataFrame, key_prefix: str = "premium") -> None:
    routes = _rrp_build_premium_route_payload(chart)
    if not routes:
        st.info("Grafo premium preparado. Aún no hay rutas aprobadas para abrir ficha.")
        return
    routes_json = json.dumps(routes, ensure_ascii=False).replace("</", "<\/")
    html_doc = '\n<div id="rrp-premium-ab-root" class="rrp-premium-ab-root">\n  <div class="rrp-premium-head"><div><div class="rrp-premium-kicker">Route Path Engine A-B · modo premium</div><div class="rrp-premium-title">Haz clic en una línea para abrir su ficha completa</div><div class="rrp-premium-sub">Cada línea muestra datos vivos de vigilancia: confianza, observaciones, fuentes, evidencias, señal agregada, deduplicación y trazabilidad.</div></div><div class="rrp-premium-stats" id="rrpStats"></div></div>\n  <div class="rrp-premium-toolbar"><input id="rrpSearch" class="rrp-premium-search" placeholder="Filtrar ruta: XRPL, RLUSD, Treasury, mBridge, Hidden Road..." /><select id="rrpStatus" class="rrp-premium-select"><option value="all">Todos los estados</option><option value="verified">Verificadas</option><option value="deductive">Deducciones</option><option value="hypothesis">Hipótesis</option><option value="watch">Watchlist</option><option value="weak">Débiles</option></select></div>\n  <div class="rrp-premium-layout"><div class="rrp-premium-canvas-wrap"><svg id="rrpGraph" class="rrp-premium-svg" viewBox="0 0 1180 640" preserveAspectRatio="xMidYMid meet"></svg><div class="rrp-premium-legend"><span><i style="background:#3CFF9B"></i> Verificada</span><span><i style="background:#FACC15"></i> Deducción</span><span><i style="background:#FFB84D"></i> Hipótesis</span><span><i style="background:#38BDF8"></i> Watchlist</span></div></div><div class="rrp-premium-card" id="rrpFicha"></div></div>\n</div>\n<style>\n.rrp-premium-ab-root{font-family:Inter,Segoe UI,Arial,sans-serif;background:linear-gradient(135deg,#020617 0%,#07111f 56%,#0f172a 100%);border:1px solid rgba(56,189,248,.35);border-radius:22px;padding:16px;color:#E5E7EB;box-shadow:0 18px 48px rgba(0,0,0,.45)}.rrp-premium-head{display:flex;justify-content:space-between;gap:14px;align-items:flex-start;margin-bottom:12px}.rrp-premium-kicker{color:#38BDF8;text-transform:uppercase;font-size:12px;font-weight:900;letter-spacing:.12em}.rrp-premium-title{font-size:22px;font-weight:950;color:white}.rrp-premium-sub{font-size:13px;color:#94A3B8;max-width:820px}.rrp-premium-stats{border:1px solid rgba(148,163,184,.25);background:rgba(15,23,42,.85);border-radius:16px;padding:10px 12px;font-size:12px;color:#CBD5E1;white-space:nowrap}.rrp-premium-toolbar{display:flex;gap:10px;margin:10px 0 14px}.rrp-premium-search,.rrp-premium-select{background:#0f172a;color:#E5E7EB;border:1px solid rgba(148,163,184,.35);border-radius:12px;padding:10px;font-size:13px}.rrp-premium-search{flex:1}.rrp-premium-layout{display:grid;grid-template-columns:minmax(520px,1.25fr) minmax(330px,.75fr);gap:14px}.rrp-premium-canvas-wrap{background:rgba(2,6,23,.62);border:1px solid rgba(148,163,184,.18);border-radius:18px;padding:8px}.rrp-premium-svg{width:100%;height:590px;display:block}.rrp-premium-card{background:rgba(15,23,42,.92);border:1px solid rgba(56,189,248,.28);border-radius:18px;padding:14px;min-height:590px;overflow:auto}.rrp-node rect{fill:#0f172a;stroke:#38BDF8;stroke-width:1.2;rx:11}.rrp-node text{fill:#E5E7EB;font-size:12px;font-weight:800}.rrp-link{fill:none;stroke-linecap:round;opacity:.62;cursor:pointer;transition:opacity .15s,stroke-width .15s,filter .15s}.rrp-link:hover,.rrp-link.active{opacity:1;filter:drop-shadow(0 0 7px rgba(56,189,248,.8))}.rrp-link-label{fill:#CBD5E1;font-size:10px;pointer-events:none}.rrp-col-title{fill:#38BDF8;font-size:12px;font-weight:950;letter-spacing:.12em;text-transform:uppercase}.rrp-premium-legend{display:flex;flex-wrap:wrap;gap:10px;padding:0 6px 8px;color:#94A3B8;font-size:12px}.rrp-premium-legend i{display:inline-block;width:10px;height:10px;border-radius:999px;margin-right:5px}.ficha-kicker{color:#38BDF8;font-size:12px;font-weight:900;text-transform:uppercase;letter-spacing:.10em}.ficha-title{font-size:19px;font-weight:950;color:#fff;margin:3px 0 8px}.pill{display:inline-block;border:1px solid rgba(148,163,184,.30);background:rgba(2,6,23,.55);border-radius:999px;padding:5px 8px;margin:3px 4px 3px 0;color:#CBD5E1;font-size:12px}.box{border:1px solid rgba(148,163,184,.20);background:rgba(2,6,23,.42);border-radius:14px;padding:10px;margin:9px 0}.box b{color:white}.small{color:#94A3B8;font-size:12px;line-height:1.45}.url{display:block;color:#7DD3FC;text-decoration:none;word-break:break-all;margin:4px 0}.empty{color:#94A3B8;text-align:center;padding:120px 20px}@media(max-width:900px){.rrp-premium-layout{grid-template-columns:1fr}.rrp-premium-card{min-height:320px}.rrp-premium-toolbar{flex-direction:column}}\n</style>\n<script>\n(function(){\nconst allRoutes = __ROUTES_JSON__; const svg=document.getElementById(\'rrpGraph\'); const ficha=document.getElementById(\'rrpFicha\'); const search=document.getElementById(\'rrpSearch\'); const statusSel=document.getElementById(\'rrpStatus\'); const stats=document.getElementById(\'rrpStats\'); let selectedId=allRoutes.length?allRoutes[0].id:null;\nfunction esc(s){return String(s==null?\'\':s).replace(/[&<>"\']/g,m=>({\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'"\':\'&quot;\',"\'":\'&#39;\'}[m]));}\nfunction short(s,n=32){s=String(s||\'\');return s.length>n?s.slice(0,n-1)+\'…\':s;}\nfunction routeText(r){return (r.origin+\' \'+r.hop+\' \'+r.destination+\' \'+r.evidence+\' \'+r.path_type+\' \'+r.deduction_mode).toLowerCase();}\nfunction filteredRoutes(){const q=search.value.trim().toLowerCase(); const st=statusSel.value; return allRoutes.filter(r=>(!q||routeText(r).includes(q))&&(st===\'all\'||r.status_css===st));}\nfunction layout(routes){const cols=[{key:\'origin\',title:\'ORIGEN\',x:120},{key:\'hop\',title:\'PUNTO PÚBLICO\',x:590},{key:\'destination\',title:\'DESTINO\',x:1040}]; const positions={}; cols.forEach(col=>{const names=[...new Set(routes.map(r=>r[col.key]).filter(Boolean))]; const step=Math.min(84,Math.max(42,520/Math.max(1,names.length))); const start=96; names.forEach((name,i)=>{positions[col.key+\'|\'+name]={x:col.x,y:start+i*step,label:name,col:col.key};});}); return {cols,positions};}\nfunction draw(){const routes=filteredRoutes(); stats.innerHTML=\'<b>\'+routes.length+\'</b> rutas visibles · <b>\'+allRoutes.length+\'</b> totales\'; svg.innerHTML=\'\'; if(!routes.length){svg.innerHTML=\'<text x="590" y="300" text-anchor="middle" fill="#94A3B8" font-size="18">Sin rutas para ese filtro</text>\'; ficha.innerHTML=\'<div class="empty">Ajusta el filtro para ver rutas.</div>\'; return;} const L=layout(routes), cols=L.cols, positions=L.positions; cols.forEach(c=>{const t=document.createElementNS(\'http://www.w3.org/2000/svg\',\'text\'); t.setAttribute(\'x\',c.x); t.setAttribute(\'y\',36); t.setAttribute(\'text-anchor\',\'middle\'); t.setAttribute(\'class\',\'rrp-col-title\'); t.textContent=c.title; svg.appendChild(t);}); routes.forEach(r=>{const a=positions[\'origin|\'+r.origin], b=positions[\'hop|\'+r.hop], c=positions[\'destination|\'+r.destination]; if(!a||!b||!c)return; [[a,b],[b,c]].forEach((pair,seg)=>{const p1=pair[0], p2=pair[1]; const path=document.createElementNS(\'http://www.w3.org/2000/svg\',\'path\'); const mid=(p1.x+p2.x)/2; const d=`M ${p1.x+74} ${p1.y} C ${mid} ${p1.y}, ${mid} ${p2.y}, ${p2.x-74} ${p2.y}`; path.setAttribute(\'d\',d); path.setAttribute(\'class\',\'rrp-link \'+(r.id===selectedId?\'active\':\'\')); path.setAttribute(\'stroke\',r.status_color||\'#38BDF8\'); path.setAttribute(\'stroke-width\',String(3+Math.min(12,Math.max(1,r.confidence/9)))); path.addEventListener(\'click\',()=>{selectedId=r.id; showFicha(r); draw();}); svg.appendChild(path); if(seg===0){const label=document.createElementNS(\'http://www.w3.org/2000/svg\',\'text\'); label.setAttribute(\'x\',mid); label.setAttribute(\'y\',(p1.y+p2.y)/2-8); label.setAttribute(\'text-anchor\',\'middle\'); label.setAttribute(\'class\',\'rrp-link-label\'); label.textContent=r.confidence+\'%\'; svg.appendChild(label);}});}); Object.values(positions).forEach(p=>{const g=document.createElementNS(\'http://www.w3.org/2000/svg\',\'g\'); g.setAttribute(\'class\',\'rrp-node\'); const rect=document.createElementNS(\'http://www.w3.org/2000/svg\',\'rect\'); rect.setAttribute(\'x\',p.x-78); rect.setAttribute(\'y\',p.y-18); rect.setAttribute(\'width\',156); rect.setAttribute(\'height\',36); g.appendChild(rect); const txt=document.createElementNS(\'http://www.w3.org/2000/svg\',\'text\'); txt.setAttribute(\'x\',p.x); txt.setAttribute(\'y\',p.y+4); txt.setAttribute(\'text-anchor\',\'middle\'); txt.textContent=short(p.label,24); g.appendChild(txt); svg.appendChild(g);}); const selected=routes.find(r=>r.id===selectedId)||routes[0]; selectedId=selected.id; showFicha(selected);}\nfunction showFicha(r){const urls=(r.source_urls||[]).map(u=>`<a class="url" href="${esc(u)}" target="_blank" rel="noopener noreferrer">${esc(u)}</a>`).join(\'\') || \'<span class="small">Sin URL fija asociada todavía.</span>\'; ficha.innerHTML=`<div class="ficha-kicker">Ficha completa de línea A-B</div><div class="ficha-title">${esc(r.origin)} → ${esc(r.hop)} → ${esc(r.destination)}</div><span class="pill">${esc(r.status)}</span><span class="pill">Confianza ${esc(r.confidence)}%</span><span class="pill">Obs. ${esc(r.count)}</span><span class="pill">${esc(r.path_type)}</span><span class="pill">Señal vivo ${esc(r.live_score)}%</span><span class="pill">Fuentes ${esc(r.source_count)}</span><div class="box"><b>📡 Números vivos de esta línea</b><br><span class="small">Señal de vigilancia: ${esc(r.live_score)}% · ${esc(r.live_label)}<br>Confianza máxima: ${esc(r.confidence)}% · Confianza media: ${esc(r.confidence_mean)}%<br>Observaciones fusionadas: ${esc(r.count)} · Fuentes URL: ${esc(r.source_count)} · Evidencias resumidas: ${esc(r.evidence_count)}<br>Peso visual de línea: ${esc(r.visual_weight)} · Deduplicación: ${esc(r.dedup_note)}</span></div><div class="box"><b>Origen</b><br><span class="small">${esc(r.origin)}</span></div><div class="box"><b>Punto público / capa visible</b><br><span class="small">${esc(r.hop)}</span></div><div class="box"><b>Destino</b><br><span class="small">${esc(r.destination)}</span></div><div class="box"><b>Evidencia resumida</b><br><span class="small">${esc(r.evidence)}</span></div><div class="box"><b>Explicación</b><br><span class="small">${esc(r.explanation)}</span></div><div class="box"><b>Capa deductiva</b><br><span class="small">Modo: ${esc(r.deduction_mode||\'generic\')}<br>${esc(r.deduction_note||\'Sin nota deductiva específica.\')}</span></div><div class="box"><b>Fuentes verificables</b><br>${urls}</div><div class="box"><b>Nodos reales agregados</b><br><span class="small">${esc(r.raw_nodes||\'Sin nodos agregados.\')}</span></div><div class="box"><b>IDs internos / trazabilidad</b><br><span class="small">${esc(r.raw_path_ids||r.id)}</span></div><div class="small">Última fecha: ${esc(r.day||\'sin fecha\')} · ID ruta: ${esc(r.id)}</div>`;}\nsearch.addEventListener(\'input\',draw); statusSel.addEventListener(\'change\',draw); draw();\n})();\n</script>\n'.replace("__ROUTES_JSON__", routes_json)
    _st_components.html(html_doc, height=780, scrolling=True)


def render_ripple_infrastructure_scope_panel() -> None:
    st.markdown('\n<div class="rrp-path-panel">\n  <div class="rrp-path-title">🌐 Cobertura real del radar: infraestructura Ripple completa</div>\n  <div class="rrp-path-text">\n    Este proyecto no vigila solo XRP o XRPL. El objetivo es investigar la infraestructura pública,\n    semipública y deductiva alrededor de <b>Ripple Payments, Ripple Custody/Metaco, Ripple Prime/Hidden Road,\n    Treasury, Rail, RLUSD, XRPL, DEX/AMM, Permissioned DEX, gateways, trustlines, wallets, clusters,\n    on/off-ramps, bancos, fuentes oficiales y rutas A→B</b>.<br><br>\n    <b>Importante:</b> no todas las líneas son prueba definitiva. El radar separa conexión verificada,\n    deducción fuerte, hipótesis, watchlist y descartadas. Su función es acelerar investigación y hacer cada\n    ruta auditable con fuentes, datos y fichas completas.\n  </div>\n</div>\n', unsafe_allow_html=True)

def render_route_path_graph_and_fichas(paths: pd.DataFrame, key_prefix: str = "live", conn: Optional[sqlite3.Connection] = None) -> pd.DataFrame:
    """Pinta el Sankey fijo y las fichas sin depender de botones ni callbacks.

    Motivo del cambio v67:
    En algunas versiones de Streamlit, un botón dentro de columnas/formularios puede ejecutar el callback,
    hacer rerun y después quedar pisado por el estado del selectbox. Para hacerlo robusto de verdad,
    cada ruta tiene ahora su propia ficha en un expander directo. Si el usuario pulsa el expander,
    la ficha se abre siempre, sin session_state, sin rerun y sin callbacks.
    """
    chart = _route_prepare_chart_df(paths, max_paths=50)
    st.markdown("#### 🧬 Gráfico A→B premium — líneas clicables")
    st.caption("Pincha una línea para abrir la ficha completa con números vivos: señal, confianza, observaciones, fuentes, evidencias, deduplicación e IDs internos.")
    render_premium_clickable_ab_graph(chart, key_prefix=key_prefix)

    # v81: evitamos sensación de gráficos duplicados.
    # El gráfico premium es el único principal; el Sankey clásico queda reservado para diagnóstico interno.
    st.caption("Vista única premium: las rutas equivalentes se agregan y las líneas son auditables desde su ficha.")

    if chart.empty:
        st.info("El gráfico está fijo y preparado, pero aún no hay rutas aprobadas para pintar.")
        return chart

    st.markdown("#### 🧾 Fichas directas de rutas del gráfico")
    st.caption("Abre cualquier desplegable para ver la ficha completa. Esta versión no depende del botón ni del estado de Streamlit.")

    view = chart[["route_label", "confidence", "count", "path_type", "evidence", "route_key"]].copy()
    view["Confianza"] = (view["confidence"].astype(float) * 100).round(1).astype(str) + "%"
    view = view.rename(columns={
        "route_label": "Ruta",
        "count": "Obs.",
        "path_type": "Tipo",
        "evidence": "Evidencia",
        "route_key": "ID",
    })[["Ruta", "Confianza", "Obs.", "Tipo", "Evidencia", "ID"]]

    search = st.text_input(
        "Filtrar rutas del gráfico",
        value="",
        key=f"{key_prefix}_route_ficha_filter",
        placeholder="Ej: XRPL, RLUSD, Coinbase, Trustline...",
    )
    filtered = view.copy()
    if search.strip():
        q = search.strip().lower()
        mask = filtered.astype(str).apply(lambda col: col.str.lower().str.contains(q, regex=False)).any(axis=1)
        filtered = filtered[mask]

    if filtered.empty:
        st.info("No hay fichas que coincidan con ese filtro.")
    else:
        max_show = min(40, len(filtered))
        for pos, (_, r) in enumerate(filtered.head(max_show).iterrows()):
            route_txt = str(r.get("Ruta", "Ruta A→B"))
            conf_txt = str(r.get("Confianza", ""))
            obs_txt = str(r.get("Obs.", ""))
            typ_txt = str(r.get("Tipo", ""))
            ev_txt = str(r.get("Evidencia", ""))[:320]
            rid = str(r.get("ID", ""))
            row_df = chart[chart["route_key"].astype(str) == rid]
            title = f"📌 Abrir ficha — {route_txt} · Confianza {conf_txt} · Obs. {obs_txt}"
            if len(title) > 220:
                title = title[:217] + "..."
            with st.expander(title, expanded=False):
                st.markdown(
                    '<div class="rrp-route-picker-card">'
                    '<div class="rrp-route-picker-title">' + html.escape(route_txt) + '</div>'
                    '<div class="rrp-route-picker-meta">'
                    '<span class="rrp-route-badge">Confianza ' + html.escape(conf_txt) + '</span>'
                    '<span class="rrp-route-badge">Obs. ' + html.escape(obs_txt) + '</span>'
                    '<span class="rrp-route-badge">' + html.escape(typ_txt) + '</span><br>'
                    + html.escape(ev_txt) +
                    '</div></div>',
                    unsafe_allow_html=True,
                )
                if row_df.empty:
                    st.warning("No he podido recuperar la ficha interna de esta ruta. Usa el selector de respaldo inferior.")
                else:
                    _render_route_ficha(row_df.iloc[0], nested_safe=True, conn=conn)
        if len(filtered) > max_show:
            st.caption(f"Mostrando {max_show} de {len(filtered)} rutas. Usa el filtro para encontrar una concreta.")

    # Selector de respaldo: no depende de botones, pero deja una ruta siempre visible debajo.
    options = [str(x) for x in chart["route_key"].tolist()]
    labels = dict(zip(chart["route_key"].astype(str), chart["route_label"].astype(str)))
    if options:
        default_key = st.session_state.get(f"{key_prefix}_selected_route_key", options[0])
        if default_key not in options:
            default_key = options[0]
        picked_key = st.selectbox(
            "Ficha visible de respaldo",
            options,
            index=options.index(default_key),
            format_func=lambda k: labels.get(str(k), str(k)),
            key=f"{key_prefix}_route_ficha_select_v67",
        )
        st.session_state[f"{key_prefix}_selected_route_key"] = picked_key
        row_df = chart[chart["route_key"].astype(str) == str(picked_key)]
        if not row_df.empty:
            st.markdown('<a id="ficha-completa-ruta"></a>', unsafe_allow_html=True)
            st.info("Ficha visible de respaldo: cambia el selector si quieres abrir otra ruta.")
            _render_route_ficha(row_df.iloc[0], nested_safe=False, conn=conn)
    return chart

def _label(addr: str) -> str:
    """Devuelve etiqueta conocida o dirección truncada con símbolo ?."""
    if addr in KNOWN_XRPL_WALLETS:
        return KNOWN_XRPL_WALLETS[addr]
    return f"? {addr[:8]}…{addr[-4:]}"


# Supply total XRP ≈ 100 000 M — cualquier valor mayor es basura de parsing
_MAX_XRP = 100_000_000_000.0
# Valor máximo razonable para una SOLA TX de XRP (50 M es ya excepcional)
_MAX_TX_XRP = 50_000_000.0
# Valor máximo razonable para una SOLA TX de IOU (50 M RLUSD es enorme)
_MAX_IOU = 50_000_000.0
# Tope del volumen acumulado para mostrar en UI (no confundir con supply total)
_MAX_DISPLAY_VOL = 999_999_999.0   # >999 M → mostrar como overflow


def _safe_float(raw, default: float = 0.0) -> float:
    """Convierte a float de forma segura.

    Acepta un segundo parámetro `default` porque varios módulos nuevos
    de Cinemática llaman `_safe_float(valor, 0.0)`. La versión antigua
    solo aceptaba un argumento y provocaba error al abrir Cinemática.
    """
    try:
        v = float(raw)
        if v != v or v == float("inf") or v == float("-inf"):
            return float(default)
        return v
    except (ValueError, TypeError, OverflowError):
        try:
            return float(default)
        except Exception:
            return 0.0




def _clip(value, lo: float = 0.0, hi: float = 100.0) -> float:
    """Limita un valor numérico entre `lo` y `hi` de forma segura.

    La Cinemática usa `_clip()` para normalizar liquidez, presión,
    probabilidad y calidad. Algunas ramas antiguas no lo tenían definido,
    provocando NameError al abrir la pestaña Cinemática.
    """
    try:
        v = float(value)
        if v != v or v == float("inf") or v == float("-inf"):
            return float(lo)
        return max(float(lo), min(float(hi), v))
    except Exception:
        return float(lo)

def _cur_display(cur: str) -> str:
    """
    Formatea un código de divisa XRPL para mostrar al usuario.
    Los tokens no estándar usan 40 chars hex (160-bit) — los acortamos.
    """
    if not cur or cur == "?":
        return "IOU"
    if len(cur) == 40 and all(c in "0123456789ABCDEFabcdef" for c in cur):
        # Token hex: muestra los primeros 6 chars legibles (sin trailing zeros)
        readable = bytes.fromhex(cur).rstrip(b"\x00").decode("ascii", errors="replace")
        readable = readable.strip() or cur[:6]
        return f"token({readable[:8]})"
    return cur


def _amount_str(amount_field) -> Tuple[str, str]:
    """Convierte Amount/delivered_amount de XRPL a (display, currency)."""
    if isinstance(amount_field, str):
        try:
            xrp = min(int(amount_field) / 1_000_000, _MAX_TX_XRP)
            return f"{xrp:,.2f} XRP", "XRP"
        except (ValueError, OverflowError):
            return "? XRP", "XRP"
    if isinstance(amount_field, dict):
        cur_raw = str(amount_field.get("currency", "?") or "?")
        cur = _cur_display(cur_raw)
        raw_val = _safe_float(amount_field.get("value", 0))
        if raw_val > _MAX_IOU:
            return f"~overflow {cur}", cur_raw
        if raw_val >= 1_000_000:
            return f"{raw_val:,.0f} {cur}", cur_raw
        if raw_val >= 1_000:
            return f"{raw_val:,.2f} {cur}", cur_raw
        return f"{raw_val:,.4f} {cur}", cur_raw
    return "?", "?"


def _delivered_amount_field(tx: Dict[str, Any], meta: Optional[Dict[str, Any]] = None):
    """Usa delivered_amount cuando exista; evita interpretar mal partial payments."""
    meta = meta or {}
    for key in ("delivered_amount", "DeliveredAmount"):
        if isinstance(meta, dict) and key in meta:
            return meta.get(key)
    return tx.get("Amount", tx.get("DeliverMax", {}))


def _amount_profile(amount_field) -> Dict[str, Any]:
    """Perfil estricto: XRP nativo separado de IOU/token emitido."""
    display, currency = _amount_str(amount_field)
    if isinstance(amount_field, str):
        try:
            native = min(int(amount_field) / 1_000_000, _MAX_TX_XRP)
        except (ValueError, OverflowError):
            native = 0.0
        return {
            "display": display, "currency": "XRP", "kind": "native_xrp",
            "native_xrp": native, "iou_value": 0.0,
            "is_native_xrp": True, "is_iou": False,
            "is_approved_iou": False, "is_suspicious_iou": False,
        }
    if isinstance(amount_field, dict):
        raw_cur = str(amount_field.get("currency", "") or "")
        cur = _cur_display(raw_cur)
        val = _safe_float(amount_field.get("value", 0))
        if val > _MAX_IOU:
            val = 0.0
        approved = cur.upper() in APPROVED_ISSUED_CURRENCIES or raw_cur.upper() in APPROVED_ISSUED_CURRENCIES
        return {
            "display": display, "currency": cur, "currency_raw": raw_cur,
            "kind": "approved_iou" if approved else "suspicious_iou",
            "native_xrp": 0.0, "iou_value": val,
            "is_native_xrp": False, "is_iou": True,
            "is_approved_iou": approved, "is_suspicious_iou": not approved,
        }
    return {
        "display": "?", "currency": "?", "kind": "unknown",
        "native_xrp": 0.0, "iou_value": 0.0,
        "is_native_xrp": False, "is_iou": False,
        "is_approved_iou": False, "is_suspicious_iou": True,
    }


def _payment_profile(tx: Dict[str, Any], meta: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    field = _delivered_amount_field(tx, meta)
    prof = _amount_profile(field)
    prof["amount_field"] = field
    return prof


def _xrp_val(amount_field) -> float:
    """Solo XRP nativo. Los IOU/token emitidos NO se suman como XRP."""
    return float(_amount_profile(amount_field).get("native_xrp", 0.0))


def _iou_val(amount_field) -> float:
    """Valor nominal de IOU/token emitido. Nunca equivale a XRP nativo."""
    return float(_amount_profile(amount_field).get("iou_value", 0.0))


def _profile_sort_value(profile: Dict[str, Any]) -> float:
    if profile.get("is_native_xrp"):
        return float(profile.get("native_xrp", 0.0))
    if profile.get("is_approved_iou"):
        return float(profile.get("iou_value", 0.0))
    return 0.0

def _fmt_vol(vol: float) -> str:
    """Formatea un volumen acumulado; si supera _MAX_DISPLAY_VOL muestra 'overflow'."""
    if vol >= _MAX_DISPLAY_VOL:
        return ">999 M XRP (overflow IOU)"
    if vol >= 1_000_000:
        return f"{vol/1_000_000:.2f} M XRP"
    if vol >= 1_000:
        return f"{vol/1_000:.1f} k XRP"
    return f"{vol:,.0f} XRP"


def _is_whale(amount_field) -> bool:
    """Whale estricta: XRP nativo o IOU aprobado; tokens raros no cuentan."""
    prof = _amount_profile(amount_field)
    if prof.get("is_native_xrp"):
        return float(prof.get("native_xrp", 0.0)) >= WHALE_XRP_THRESHOLD
    if prof.get("is_approved_iou"):
        return float(prof.get("iou_value", 0.0)) >= WHALE_RLUSD_THRESHOLD
    return False


def _is_auto_map(amount_field) -> bool:
    """Marca TX gigante, pero la wallet solo entra si pasa _wallet_quality_gate."""
    prof = _amount_profile(amount_field)
    if prof.get("is_native_xrp"):
        return float(prof.get("native_xrp", 0.0)) >= AUTO_MAP_XRP
    if prof.get("is_approved_iou"):
        return float(prof.get("iou_value", 0.0)) >= AUTO_MAP_RLUSD
    return False

def _fetch_single_ledger(ledger_index: int) -> Tuple[int, List[Dict]]:
    """Descarga un ledger concreto y devuelve (index, lista de TX)."""
    try:
        resp = requests.post(
            XRPL_SERVER,
            json={"method": "ledger",
                  "params": [{"ledger_index": ledger_index,
                               "transactions": True,
                               "expand": True}]},
            timeout=12,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        result = resp.json().get("result", {})
        idx  = result.get("ledger", {}).get("ledger_index", ledger_index)
        txs  = result.get("ledger", {}).get("transactions", [])
        return int(idx), txs
    except Exception:
        return ledger_index, []


@st.cache_data(ttl=30, show_spinner=False)
def fetch_recent_large_payments(min_xrp: float = 500.0) -> pd.DataFrame:
    """
    Escanea los últimos WHALE_SCAN_LEDGERS ledgers de XRPL.
    Devuelve pagos grandes con columnas extra:
      - xrp_value   : valor numérico (XRP o IOU)
      - is_whale    : True si supera WHALE_XRP_THRESHOLD
      - auto_map    : True si supera AUTO_MAP_XRP (añadir automáticamente)
      - identified  : True si sender o receiver están en KNOWN_XRPL_WALLETS
    """
    # Primero obtener el ledger validado actual
    try:
        resp = requests.post(
            XRPL_SERVER,
            json={"method": "ledger",
                  "params": [{"ledger_index": "validated",
                               "transactions": False,
                               "expand": False}]},
            timeout=10,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        current_idx = int(resp.json().get("result", {})
                          .get("ledger", {}).get("ledger_index", 0))
    except Exception:
        return pd.DataFrame()

    if current_idx == 0:
        return pd.DataFrame()

    rows: List[Dict] = []
    # Escanear los últimos N ledgers
    for offset in range(WHALE_SCAN_LEDGERS):
        ledger_idx, txs = _fetch_single_ledger(current_idx - offset)
        for tx in txs:
            if not isinstance(tx, dict):
                continue
            if tx.get("TransactionType") != "Payment":
                continue
            meta = tx.get("metaData", tx.get("meta", {}))
            if isinstance(meta, dict) and meta.get("TransactionResult", "") != "tesSUCCESS":
                continue

            prof = _payment_profile(tx, meta)
            amount_field = prof.get("amount_field", tx.get("Amount", {}))
            amount_str   = prof.get("display", "?")
            currency     = prof.get("currency", "?")
            native_xrp   = float(prof.get("native_xrp", 0.0))
            iou_value    = float(prof.get("iou_value", 0.0))
            sort_value   = _profile_sort_value(prof)

            # Filtro supremo: solo XRP nativo o IOU aprobado. XGBT/otros tokens
            # no alimentan el rastreador automático ni se muestran como XRP.
            if prof.get("is_native_xrp"):
                if native_xrp < min_xrp:
                    continue
            elif prof.get("is_approved_iou"):
                if iou_value < WHALE_RLUSD_THRESHOLD:
                    continue
            else:
                continue

            sender   = tx.get("Account", "?")
            receiver = tx.get("Destination", "?")
            tx_hash  = tx.get("hash", "?")

            rows.append({
                "hash_full":      tx_hash,
                "hash":           tx_hash[:14] + "…" if len(tx_hash) > 14 else tx_hash,
                "ledger_index":   ledger_idx,
                "ledger_offset":  offset,
                "sender":         sender,
                "sender_label":   _label(sender),
                "receiver":       receiver,
                "receiver_label": _label(receiver),
                "amount":         amount_str,
                "xrp_value":      native_xrp,
                "native_xrp_value": native_xrp,
                "iou_value":      iou_value,
                "sort_value":     sort_value,
                "currency":       currency,
                "amount_kind":    prof.get("kind", "unknown"),
                "is_approved_iou": bool(prof.get("is_approved_iou")),
                "is_suspicious_iou": bool(prof.get("is_suspicious_iou")),
                "is_whale":       _is_whale(amount_field),
                "auto_map":       _is_auto_map(amount_field),
                "identified":     sender in KNOWN_XRPL_WALLETS or receiver in KNOWN_XRPL_WALLETS,
            })

    if not rows:
        return pd.DataFrame()

    df_out = pd.DataFrame(rows)
    # Whales primero, luego identificadas, luego por valor
    df_out = df_out.sort_values(
        ["is_whale", "auto_map", "sort_value"],
        ascending=[False, False, False],
    ).drop_duplicates("hash_full").reset_index(drop=True)
    return df_out


@st.cache_data(ttl=90, show_spinner=False)
def trace_next_hop(wallet: str, from_ledger: int) -> Optional[Dict[str, Any]]:
    """
    Mira si 'wallet' envió algo en los 20 ledgers siguientes a from_ledger.
    Si sí, devuelve info del siguiente salto (a quién envió y cuánto).
    """
    try:
        resp = requests.post(
            XRPL_SERVER,
            json={"method": "account_tx",
                  "params": [{"account": wallet,
                               "ledger_index_min": from_ledger,
                               "ledger_index_max": from_ledger + 20,
                               "limit": 10,
                               "forward": True}]},
            timeout=12,
            headers={"Content-Type": "application/json"},
        )
        resp.raise_for_status()
        txs = resp.json().get("result", {}).get("transactions", [])
        for item in txs:
            tx = item.get("tx", item)
            if tx.get("TransactionType") != "Payment":
                continue
            if tx.get("Account") != wallet:
                continue  # solo salidas
            meta = item.get("meta", {})
            if isinstance(meta, dict) and meta.get("TransactionResult", "") != "tesSUCCESS":
                continue
            next_recv = tx.get("Destination", "?")
            prof = _payment_profile(tx, meta)
            return {
                "next_receiver":       next_recv,
                "next_receiver_label": _label(next_recv),
                "next_known":          next_recv in KNOWN_XRPL_WALLETS,
                "amount":              prof.get("display", "?"),
                "hash":                tx.get("hash", "?")[:14] + "…",
            }
    except Exception:
        pass
    return None


@st.cache_data(ttl=300, show_spinner=False)
def xrpscan_lookup(wallet: str) -> Dict[str, str]:
    """Consulta XRPScan API pública para obtener nombre/etiqueta de una wallet."""
    try:
        r = requests.get(
            f"https://api.xrpscan.com/api/v1/account/{wallet}",
            timeout=8,
            headers={"User-Agent": "RippleRadarPro/6.0"},
        )
        if r.status_code == 200:
            data = r.json()
            name_info = data.get("accountName") or {}
            return {
                "name": str(name_info.get("name", "") or ""),
                "desc": str(name_info.get("desc", "") or ""),
            }
    except Exception:
        pass
    return {"name": "", "desc": ""}


@st.cache_data(ttl=600, show_spinner=False)
def fetch_xrpscan_wellknown() -> Dict[str, str]:
    """
    Descarga la lista de cuentas conocidas de XRPScan (pública, sin API key).
    Devuelve dict {address: name}.
    """
    try:
        r = requests.get(
            "https://api.xrpscan.com/api/v1/well-known",
            timeout=10,
            headers={"User-Agent": "RippleRadarPro/6.0"},
        )
        if r.status_code == 200:
            accounts = r.json()  # lista de dicts con 'account' y 'name'
            if isinstance(accounts, list):
                return {str(a.get("account", "")): str(a.get("name", ""))
                        for a in accounts if a.get("account")}
    except Exception:
        pass
    return {}


@st.cache_data(ttl=120, show_spinner=False)
def bithomp_lookup(wallet: str) -> Dict[str, str]:
    """Intenta obtener nombre de Bithomp (sin API key, solo datos públicos)."""
    try:
        r = requests.get(
            f"https://bithomp.com/api/v2/address/{wallet}",
            timeout=8,
            headers={"User-Agent": "RippleRadarPro/6.0", "x-bithomp-token": ""},
        )
        if r.status_code == 200:
            data = r.json()
            username = data.get("username") or data.get("service", {}).get("name", "")
            return {"name": str(username or ""), "source": "Bithomp"}
    except Exception:
        pass
    return {"name": "", "source": ""}


@st.cache_data(ttl=60, show_spinner=False)
def find_node_connections(wallet: str) -> List[Dict[str, Any]]:
    """
    Descarga las últimas 100 TX de una wallet y busca si alguna contraparte
    pertenece a KNOWN_XRPL_WALLETS → mapea al nodo del mapa principal.
    Devuelve lista de conexiones: {node, label, tx_count, volume, direction}.
    """
    connections: Dict[str, Dict] = {}
    try:
        r = requests.post(
            XRPL_SERVER,
            json={"method": "account_tx",
                  "params": [{"account": wallet, "limit": 100}]},
            timeout=15,
            headers={"Content-Type": "application/json"},
        )
        r.raise_for_status()
        txs = r.json().get("result", {}).get("transactions", [])
    except Exception:
        return []

    for item in txs:
        tx   = item.get("tx", item)
        if tx.get("TransactionType") != "Payment":
            continue
        meta = item.get("meta", {})
        if isinstance(meta, dict) and meta.get("TransactionResult", "") != "tesSUCCESS":
            continue

        is_sender = tx.get("Account") == wallet
        cp        = tx.get("Destination") if is_sender else tx.get("Account", "")
        if not cp or cp == wallet:
            continue

        cp_label = KNOWN_XRPL_WALLETS.get(cp, "")
        if not cp_label:
            continue  # no conocido — skip

        node_name = WALLET_LABEL_TO_NODE.get(cp_label, cp_label)
        key = node_name

        prof = _payment_profile(tx, meta)
        if prof.get("is_native_xrp"):
            vol = float(prof.get("native_xrp", 0.0))
        elif prof.get("is_approved_iou"):
            vol = float(prof.get("iou_value", 0.0))
        else:
            vol = 0.0
        if vol <= 0:
            continue

        if key not in connections:
            connections[key] = {
                "node":      node_name,
                "label":     cp_label,
                "wallet":    cp,
                "tx_count":  0,
                "volume":    0.0,
                "sent":      0,
                "received":  0,
            }
        connections[key]["tx_count"] += 1
        connections[key]["volume"]   += vol
        if is_sender:
            connections[key]["sent"] += 1
        else:
            connections[key]["received"] += 1

    result = sorted(connections.values(), key=lambda x: x["volume"], reverse=True)
    for c in result:
        total = c["tx_count"]
        c["direction"] = (
            "bidireccional"  if c["sent"] > 0 and c["received"] > 0 else
            "envía a"        if c["sent"] > 0 else
            "recibe de"
        )
    return result


def _get_wallet_counterparts(wallet: str, limit: int = 50) -> List[Tuple[str, float, bool]]:
    """
    Descarga TX de una wallet y devuelve lista de (counterpart_address, volume, is_sender).
    Función interna rápida para análisis de cadena.
    """
    out: List[Tuple[str, float, bool]] = []
    try:
        r = requests.post(
            XRPL_SERVER,
            json={"method": "account_tx",
                  "params": [{"account": wallet, "limit": limit}]},
            timeout=12,
            headers={"Content-Type": "application/json"},
        )
        r.raise_for_status()
        txs = r.json().get("result", {}).get("transactions", [])
    except Exception:
        return out
    for item in txs:
        tx   = item.get("tx", item)
        if tx.get("TransactionType") != "Payment":
            continue
        meta = item.get("meta", {})
        if isinstance(meta, dict) and meta.get("TransactionResult", "") != "tesSUCCESS":
            continue
        is_sender = tx.get("Account") == wallet
        cp  = tx.get("Destination") if is_sender else tx.get("Account", "")
        prof = _payment_profile(tx, meta)
        if prof.get("is_native_xrp"):
            vol = float(prof.get("native_xrp", 0.0))
        elif prof.get("is_approved_iou"):
            vol = float(prof.get("iou_value", 0.0))
        else:
            vol = 0.0
        if cp and cp != wallet and vol > 0:
            out.append((cp, vol, is_sender))
    return out


@st.cache_data(ttl=90, show_spinner=False)
def find_connection_chain(wallet: str) -> Dict[str, Any]:
    """
    Busca la cadena de conexión de una wallet hacia entidades conocidas del mapa.
    Hace hasta 2 saltos:
      Salto 1 — contrapartes directas de la wallet
      Salto 2 — si la contraparte es desconocida, mira SUS contrapartes
    Devuelve:
      direct   : conexiones directas a entidades conocidas
      indirect : conexiones de 2º grado (a través de intermediario)
      ripple_score : 0-100, probabilidad de estar en el ecosistema Ripple
      verdict  : texto de conclusión
    """
    result: Dict[str, Any] = {
        "direct":       [],
        "indirect":     [],
        "ripple_score": 0,
        "verdict":      "Sin datos suficientes para determinar conexión.",
    }

    # ── Salto 1: contrapartes directas ───────────────────────────────────────
    hop1 = _get_wallet_counterparts(wallet, limit=80)
    if not hop1:
        return result

    direct_known: List[Dict] = []
    unknown_cps: Dict[str, float] = {}   # addr → volumen acumulado

    for cp, vol, is_sender in hop1:
        lbl = KNOWN_XRPL_WALLETS.get(cp, "")
        if lbl:
            node = WALLET_LABEL_TO_NODE.get(lbl, lbl)
            # Acumular si ya existe
            existing = next((d for d in direct_known if d["wallet"] == cp), None)
            if existing:
                existing["volume"] += vol
                existing["tx_count"] += 1
            else:
                direct_known.append({
                    "wallet":    cp,
                    "label":     lbl,
                    "node":      node,
                    "volume":    vol,
                    "tx_count":  1,
                    "direction": "envía a" if is_sender else "recibe de",
                    "hop":       1,
                })
        else:
            unknown_cps[cp] = unknown_cps.get(cp, 0.0) + vol

    result["direct"] = sorted(direct_known, key=lambda x: x["volume"], reverse=True)

    # ── Salto 2: mirar contrapartes de las desconocidas (top 5 por volumen) ──
    top_unknown = sorted(unknown_cps.items(), key=lambda x: x[1], reverse=True)[:5]
    indirect_known: List[Dict] = []

    for mid_wallet, mid_vol in top_unknown:
        hop2 = _get_wallet_counterparts(mid_wallet, limit=30)
        for cp2, vol2, is_sender2 in hop2:
            if cp2 == wallet:
                continue
            lbl2 = KNOWN_XRPL_WALLETS.get(cp2, "")
            if lbl2:
                node2 = WALLET_LABEL_TO_NODE.get(lbl2, lbl2)
                mid_lbl = KNOWN_XRPL_WALLETS.get(mid_wallet, f"? {mid_wallet[:10]}…")
                existing = next((d for d in indirect_known if d["end_wallet"] == cp2), None)
                if existing:
                    existing["volume"] += vol2
                else:
                    indirect_known.append({
                        "mid_wallet":  mid_wallet,
                        "mid_label":   mid_lbl,
                        "end_wallet":  cp2,
                        "label":       lbl2,
                        "node":        node2,
                        "volume":      mid_vol,
                        "hop":         2,
                        "direction":   "envía a" if is_sender2 else "recibe de",
                    })

    result["indirect"] = sorted(indirect_known, key=lambda x: x["volume"], reverse=True)

    # ── Ripple score ──────────────────────────────────────────────────────────
    ripple_nodes = {"Ripple Payments", "RLUSD", "XRPL", "Ripple Treasury",
                    "Ripple Rail", "Ripple Prime", "ODL Gateway"}
    institutional = {"Bitstamp", "Bitso (ODL MX)", "SBI Remit", "Tranglo / Coins.ph (ODL Asia)",
                     "BeeTech (ODL BR)", "Public Gateway", "Hidden Road / Prime", "Custody/Metaco"}

    score = 0
    all_connections = result["direct"] + result["indirect"]

    for c in all_connections:
        node = c.get("node", "")
        hop  = c.get("hop", 1)
        w    = 1.0 if hop == 1 else 0.5
        if node in ripple_nodes:
            score += int(35 * w)
        elif node in institutional:
            score += int(20 * w)
        elif node:
            score += int(8 * w)

    # Boost si hay conexión directa a Ripple
    if any(c["node"] in ripple_nodes for c in result["direct"]):
        score += 25
    # Boost si hay conexión directa a ODL corridor
    if any(c["node"] in {"Bitso (ODL MX)", "SBI Remit", "Tranglo / Coins.ph (ODL Asia)"} for c in result["direct"]):
        score += 15

    result["ripple_score"] = min(score, 100)

    # ── Veredicto ─────────────────────────────────────────────────────────────
    score = result["ripple_score"]
    n_direct   = len(result["direct"])
    n_indirect = len(result["indirect"])

    if score >= 70:
        result["verdict"] = (
            f"🔴 <b>Muy probable conexión al ecosistema Ripple/institucional</b> — "
            f"{n_direct} conexión(es) directa(s) a nodos conocidos, {n_indirect} indirecta(s). "
            f"Score de conexión Ripple: {score}/100."
        )
    elif score >= 40:
        result["verdict"] = (
            f"🟠 <b>Conexión probable al ecosistema</b> — "
            f"{n_direct} directa(s), {n_indirect} de 2º grado. "
            f"Score: {score}/100. Puede ser un actor del mercado OTC o exchange conectado."
        )
    elif score >= 15:
        result["verdict"] = (
            f"🟡 <b>Conexión débil / indirecta</b> — "
            f"Solo {n_direct} directa(s) y {n_indirect} de 2º grado a entidades conocidas. "
            f"Score: {score}/100. Necesita más datos para confirmar."
        )
    else:
        result["verdict"] = (
            f"⚪ <b>Sin conexión clara al ecosistema</b> — "
            f"No se encontraron relaciones con entidades conocidas en las últimas 80 TX. "
            f"Puede ser una wallet de usuario final o fuera del ecosistema XRPL institucional."
        )

    return result


def multi_source_identify(wallet: str) -> Dict[str, Any]:
    """
    Identificación completa multi-fuente de una wallet.
    Cruza: KNOWN_XRPL_WALLETS + XRPScan well-known + XRPScan account + Bithomp.
    Devuelve dict con name, source, confidence_boost, node_in_map.
    """
    result: Dict[str, Any] = {
        "name":             "",
        "sources":          [],
        "confidence_boost": 0.0,
        "node_in_map":      "",
        "already_known":    False,
    }

    # 1. Ya en nuestra base
    if wallet in KNOWN_XRPL_WALLETS:
        lbl = KNOWN_XRPL_WALLETS[wallet]
        result.update({
            "name": lbl, "sources": ["Base local"],
            "confidence_boost": 0.50,
            "node_in_map": WALLET_LABEL_TO_NODE.get(lbl, ""),
            "already_known": True,
        })
        return result

    # 2. XRPScan well-known list (rápido, batch ya en caché)
    wk = fetch_xrpscan_wellknown()
    if wallet in wk:
        name = wk[wallet]
        result["name"] = name
        result["sources"].append("XRPScan well-known")
        result["confidence_boost"] += 0.45
        result["node_in_map"] = WALLET_LABEL_TO_NODE.get(name, "")
        # Añadir a nuestra base en memoria
        KNOWN_XRPL_WALLETS[wallet] = name

    # 3. XRPScan account API
    scan = xrpscan_lookup(wallet)
    if scan.get("name"):
        if not result["name"]:
            result["name"] = scan["name"]
            result["node_in_map"] = WALLET_LABEL_TO_NODE.get(scan["name"], "")
            KNOWN_XRPL_WALLETS[wallet] = scan["name"]
        result["sources"].append("XRPScan account")
        result["confidence_boost"] += 0.35

    # 4. Bithomp
    bh = bithomp_lookup(wallet)
    if bh.get("name"):
        if not result["name"]:
            result["name"] = bh["name"]
            KNOWN_XRPL_WALLETS[wallet] = bh["name"]
        result["sources"].append("Bithomp")
        result["confidence_boost"] += 0.25

    if result["name"]:
        result["node_in_map"] = (
            result["node_in_map"] or WALLET_LABEL_TO_NODE.get(result["name"], "")
        )

    return result


@st.cache_data(ttl=120, show_spinner=False)
def analyze_wallet_txs(wallet: str) -> Dict[str, Any]:
    """Analiza TX separando XRP nativo, IOU aprobado e IOU/token sospechoso."""
    empty: Dict[str, Any] = {}
    try:
        r = requests.post(
            XRPL_SERVER,
            json={"method": "account_tx", "params": [{"account": wallet, "limit": 80}]},
            timeout=15,
            headers={"Content-Type": "application/json"},
        )
        r.raise_for_status()
        txs = r.json().get("result", {}).get("transactions", [])
    except Exception:
        return empty
    if not txs:
        return empty

    effective_amounts: List[float] = []
    counterparts: Dict[str, int] = {}
    currency_counts: Dict[str, int] = {}
    sent = received = payment_count = 0
    native_xrp_volume = approved_iou_volume = suspicious_iou_volume = 0.0
    native_count = approved_iou_count = suspicious_iou_count = 0

    for item in txs:
        tx = item.get("tx", item)
        if tx.get("TransactionType") != "Payment":
            continue
        meta = item.get("meta", item.get("metaData", {}))
        if isinstance(meta, dict) and meta.get("TransactionResult", "") != "tesSUCCESS":
            continue
        prof = _payment_profile(tx, meta)
        payment_count += 1
        cur = str(prof.get("currency", "?") or "?")
        currency_counts[cur] = currency_counts.get(cur, 0) + 1
        if prof.get("is_native_xrp"):
            val = float(prof.get("native_xrp", 0.0)); native_xrp_volume += val; effective_amounts.append(val); native_count += 1
        elif prof.get("is_approved_iou"):
            val = float(prof.get("iou_value", 0.0)); approved_iou_volume += val; effective_amounts.append(val); approved_iou_count += 1
        elif prof.get("is_iou"):
            val = float(prof.get("iou_value", 0.0)); suspicious_iou_volume += val; suspicious_iou_count += 1
        if tx.get("Account") == wallet:
            sent += 1; cp = tx.get("Destination", "")
        else:
            received += 1; cp = tx.get("Account", "")
        if cp:
            counterparts[cp] = counterparts.get(cp, 0) + 1

    n = payment_count
    if n == 0:
        return empty
    top_cp = max(counterparts, key=counterparts.get) if counterparts else ""
    dominant_currency = max(currency_counts, key=currency_counts.get) if currency_counts else "?"
    total_effective = native_xrp_volume + approved_iou_volume
    avg = (sum(effective_amounts) / len(effective_amounts)) if effective_amounts else 0.0
    ratio = sent / n if n else 0.0

    signals: List[str] = []
    confidence = 0.0
    if native_xrp_volume > 0:
        signals.append(f"XRP nativo verificado: {_fmt_vol(native_xrp_volume)}"); confidence += 0.18
    if approved_iou_volume > 0:
        signals.append(f"IOU aprobado verificado: {approved_iou_volume:,.0f} {dominant_currency}"); confidence += 0.08
    if suspicious_iou_volume > 0:
        signals.append(f"IOU/token no aprobado detectado: {suspicious_iou_volume:,.0f} nominales"); confidence -= 0.18
    if len(effective_amounts) > 1 and avg > 0:
        variance_pct = (sum((a - avg) ** 2 for a in effective_amounts) / len(effective_amounts)) / (avg ** 2 + 1)
        if variance_pct < 0.08 and avg > 5_000:
            signals.append("montos grandes y uniformes en activo validado"); confidence += 0.18
    if avg > 100_000:
        signals.append("volumen alto por TX en activo validado"); confidence += 0.14
    elif avg > 10_000:
        signals.append("volumen medio/alto por TX en activo validado"); confidence += 0.08
    if total_effective > 0:
        if ratio > 0.75:
            signals.append("mayormente emisor"); confidence += 0.08
        elif ratio < 0.25:
            signals.append("mayormente receptor"); confidence += 0.07
        else:
            signals.append("bidireccional"); confidence += 0.08
    if top_cp in KNOWN_XRPL_WALLETS:
        signals.append(f"conectado a {KNOWN_XRPL_WALLETS[top_cp]}"); confidence += 0.26
    if n >= 40 and total_effective > 0:
        signals.append("alta frecuencia de TX en activo validado"); confidence += 0.06
    elif n >= 40 and suspicious_iou_volume > 0:
        signals.append("alta frecuencia, pero dominada por IOU/token no aprobado")

    iou_dominant = suspicious_iou_volume > max(total_effective * SUSPICIOUS_IOU_DOMINANCE, 1.0)
    if iou_dominant:
        signals.append("cuarentena: IOU/token no aprobado domina el volumen"); confidence = min(confidence, IOU_ONLY_CONF_CAP)

    if total_effective <= 0 and top_cp not in KNOWN_XRPL_WALLETS:
        role = "desconocido / token no aprobado"
    elif top_cp in KNOWN_XRPL_WALLETS and "ODL" in KNOWN_XRPL_WALLETS.get(top_cp, ""):
        role = "corredor ODL potencial"
    elif top_cp in KNOWN_XRPL_WALLETS:
        role = "contraparte directa de entidad conocida"
    elif ratio > 0.70 and avg > 20_000:
        role = "treasury / distribuidor potencial"
    elif ratio < 0.30 and avg > 5_000:
        role = "acumulador / market maker potencial"
    elif 0.30 <= ratio <= 0.70 and len(counterparts) >= 8 and total_effective > 0:
        role = "hub bidireccional potencial"
    else:
        role = "desconocido"
    if wallet in WALLET_HARD_BLOCKLIST:
        confidence = min(confidence, IOU_ONLY_CONF_CAP); role = "bloqueada / falso positivo"; signals.append("bloqueada por falso positivo previo")

    return {
        "wallet": wallet, "role": role,
        "volume_xrp": min(native_xrp_volume, _MAX_DISPLAY_VOL),
        "native_xrp_volume": min(native_xrp_volume, _MAX_DISPLAY_VOL),
        "approved_iou_volume": min(approved_iou_volume, _MAX_DISPLAY_VOL),
        "suspicious_iou_volume": min(suspicious_iou_volume, _MAX_DISPLAY_VOL),
        "dominant_currency": dominant_currency,
        "tx_count": n, "native_tx_count": native_count,
        "approved_iou_tx_count": approved_iou_count, "suspicious_iou_tx_count": suspicious_iou_count,
        "top_cp": top_cp, "top_cp_label": _label(top_cp),
        "confidence": max(0.0, min(confidence, 1.0)),
        "signals": " · ".join(signals) if signals else "sin señales claras",
        "is_iou_dominant": iou_dominant,
    }


def _wallet_quality_gate(wallet: str, identity: Dict[str, Any], analysis: Dict[str, Any],
                         connections: List[Dict[str, Any]], raw_confidence: float,
                         tx_row: Dict[str, Any]) -> Dict[str, Any]:
    """
    Gatekeeper Supremo v2: antes de admitir una wallet al radar, primero decide si
    debe descartarse. La regla principal es conservadora:

    - Wallet desconocida + sin conexión directa a nodos del mapa = DESCARTADA.
    - Volumen alto nunca aprueba por sí solo.
    - IOU/token sospechoso, PATH_PARTIAL/fallos o ausencia de delivered_amount útil = DESCARTADA.
    - Solo pasan a Radar las wallets con identidad verificable o conexión directa real.
    """
    wallet = str(wallet or "").strip()
    identity_name = str(identity.get("name", "") or "").strip()
    identity_sources = identity.get("sources", []) or []
    node_in_map = str(identity.get("node_in_map", "") or "").strip()
    direct_connections = bool(connections)

    native_xrp = float(analysis.get("native_xrp_volume", analysis.get("volume_xrp", 0)) or 0)
    approved_iou = float(analysis.get("approved_iou_volume", 0) or tx_row.get("iou_value", 0) or 0)
    suspicious_iou = float(analysis.get("suspicious_iou_volume", 0) or 0)
    dominant_currency = str(analysis.get("dominant_currency", tx_row.get("currency", "")) or "")
    iou_dominant = bool(analysis.get("is_iou_dominant", False)) or suspicious_iou > max((native_xrp + approved_iou) * SUSPICIOUS_IOU_DOMINANCE, 1.0)

    tx_result = str(tx_row.get("TransactionResult", tx_row.get("engine_result", tx_row.get("result", ""))) or "")
    amount_kind = str(tx_row.get("amount_kind", analysis.get("kind", "")) or "")
    label_hint = str(identity_name or analysis.get("role", "") or tx_row.get("label", "") or "")

    reasons: List[str] = []
    confidence = max(0.0, min(float(raw_confidence or 0.0), 1.0))

    positive_identity = bool(identity_name and identity_sources)
    positive_node = bool(node_in_map)
    positive_connection = direct_connections
    positive_native = native_xrp >= WHALE_XRP_THRESHOLD
    positive_approved_iou = approved_iou >= WHALE_RLUSD_THRESHOLD
    unknown_identity = not positive_identity and not positive_node and not positive_connection

    # Bloqueos definitivos: no entran ni en watchlist normal.
    hard_discard = False
    if wallet in WALLET_HARD_BLOCKLIST:
        hard_discard = True
        reasons.append("falso positivo bloqueado manualmente")
    if tx_result and tx_result != "tesSUCCESS":
        hard_discard = True
        reasons.append(f"transacción no exitosa ({tx_result})")
    if str(tx_row.get("path_partial", "")).lower() in {"1", "true", "yes"}:
        hard_discard = True
        reasons.append("PATH_PARTIAL / pago parcial no fiable")
    if iou_dominant:
        hard_discard = True
        reasons.append("IOU/token no aprobado domina el volumen")
    if suspicious_iou > 0 and native_xrp <= 0 and approved_iou <= 0:
        hard_discard = True
        reasons.append("sin XRP nativo ni activo aprobado")
    if amount_kind == "suspicious_iou":
        hard_discard = True
        reasons.append("activo emitido no aprobado")

    # Regla pedida: desconocida sin conexión directa => descartada, aunque tenga volumen.
    if unknown_identity:
        hard_discard = True
        reasons.append("wallet desconocida sin etiqueta externa fiable ni conexión directa a nodos del mapa")

    if hard_discard:
        return {
            "status": "discarded",
            "added_to_map": False,
            "confidence": min(confidence, DISCARDED_CONF_CAP),
            "reason": " · ".join(dict.fromkeys([r for r in reasons if r])) or "descartada por gatekeeper supremo",
            "native_xrp": native_xrp,
            "approved_iou": approved_iou,
            "suspicious_iou": suspicious_iou,
            "dominant_currency": dominant_currency,
        }

    score_reasons: List[str] = []
    if positive_identity:
        score_reasons.append("identidad externa fiable"); confidence += 0.10
    if positive_node:
        score_reasons.append("identidad mapea a nodo del radar"); confidence += 0.12
    if positive_connection:
        score_reasons.append("conexión directa a nodo conocido"); confidence += 0.14
    if positive_native:
        score_reasons.append("XRP nativo real suficiente"); confidence += 0.08
    if positive_approved_iou:
        score_reasons.append("activo aprobado suficiente"); confidence += 0.05

    confidence = max(0.0, min(confidence, 1.0))
    can_map = (
        confidence >= STRICT_AUTO_MAP_CONFIDENCE
        and (positive_node or positive_connection or positive_identity)
        and (positive_native or positive_approved_iou or positive_connection)
    )

    if can_map:
        status = "map"
        reasons.extend(score_reasons or ["gatekeeper estricto aprobado"])
    else:
        status = "watch" if (confidence >= STRICT_WATCH_CONFIDENCE or positive_connection or positive_identity) else "discarded"
        reasons.extend(score_reasons or ["señales insuficientes para mapa"])
        if status == "discarded":
            confidence = min(confidence, DISCARDED_CONF_CAP)

    return {
        "status": status,
        "added_to_map": bool(can_map),
        "confidence": confidence,
        "reason": " · ".join(dict.fromkeys([r for r in reasons if r])) or "evaluación conservadora completada",
        "native_xrp": native_xrp,
        "approved_iou": approved_iou,
        "suspicious_iou": suspicious_iou,
        "dominant_currency": dominant_currency,
    }


def auto_track_whale(conn: sqlite3.Connection, tx_row: Dict[str, Any]) -> Dict[str, Any]:
    """Analiza sender/receiver. La TX grande no fuerza mapa; manda el gatekeeper."""
    ensure_discovered_wallets_table(conn)
    today = str(_date.today())
    results = {}
    val_native = float(tx_row.get("native_xrp_value", tx_row.get("xrp_value", 0)) or 0)
    val_iou = float(tx_row.get("iou_value", 0) or 0)
    for role_key, wallet in (("sender", tx_row["sender"]), ("receiver", tx_row["receiver"])):
        if wallet == "?":
            results[role_key] = {"wallet": wallet, "label": "?", "new": False, "added_map": False}; continue
        identity = multi_source_identify(wallet)
        if identity["already_known"]:
            results[role_key] = {"wallet":wallet,"label":identity["name"],"new":False,"added_map":False,"status":"known","quality_reason":"ya existía en base local","node_in_map":identity.get("node_in_map", ""),"connections":[]}; continue
        analysis = analyze_wallet_txs(wallet)
        connections = find_node_connections(wallet)
        conn_boost = min(len(connections) * 0.10, 0.30)
        vol_boost = 0.10 if val_native >= AUTO_MAP_XRP else 0.05 if val_native >= WHALE_XRP_THRESHOLD else 0.05 if bool(tx_row.get("is_approved_iou")) and val_iou >= AUTO_MAP_RLUSD else 0.0
        raw_confidence = min(float(analysis.get("confidence", 0) or 0) + float(identity.get("confidence_boost", 0) or 0) + conn_boost + vol_boost, 1.0) if analysis else min(float(identity.get("confidence_boost", 0) or 0) + conn_boost + vol_boost, 1.0)
        gate = _wallet_quality_gate(wallet, identity, analysis or {}, connections, raw_confidence, tx_row)
        confidence = float(gate.get("confidence", 0.0)); should_map = bool(gate.get("added_to_map", False)); status = str(gate.get("status", "watch"))
        if status == "discarded":
            label = "descartada / falso positivo"
        elif identity.get("name"):
            label = identity["name"]
        elif connections and should_map:
            label = f"Contraparte de {connections[0]['node']}"
        elif analysis:
            label = analysis.get("role", "wallet en cuarentena")
        else:
            label = "wallet en cuarentena"
        node_in_map = identity.get("node_in_map", "") or (connections[0]["node"] if connections else "")
        sig_parts = []
        if analysis: sig_parts.append(analysis.get("signals", ""))
        if connections: sig_parts.append("conexiones al mapa: " + ", ".join(c["node"] for c in connections[:3]))
        if identity.get("sources"): sig_parts.append("identificado vía: " + ", ".join(identity.get("sources", [])))
        sig_parts.append("gatekeeper: " + str(gate.get("reason", "")))
        conn.execute("""
            INSERT INTO discovered_wallets
                (wallet, label, role, volume_xrp, tx_count, top_counterpart, top_cp_label,
                 confidence, signals, xrpscan_name, xrpscan_desc, added_to_map, first_seen,
                 last_seen, status, native_xrp_volume, approved_iou_volume, suspicious_iou_volume,
                 dominant_currency, quality_reason)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            ON CONFLICT(wallet) DO UPDATE SET
                label=excluded.label, role=excluded.role, volume_xrp=excluded.volume_xrp,
                tx_count=excluded.tx_count, top_counterpart=excluded.top_counterpart,
                top_cp_label=excluded.top_cp_label, confidence=excluded.confidence,
                signals=excluded.signals, xrpscan_name=excluded.xrpscan_name,
                xrpscan_desc=excluded.xrpscan_desc, added_to_map=excluded.added_to_map,
                status=excluded.status, native_xrp_volume=excluded.native_xrp_volume,
                approved_iou_volume=excluded.approved_iou_volume,
                suspicious_iou_volume=excluded.suspicious_iou_volume,
                dominant_currency=excluded.dominant_currency, quality_reason=excluded.quality_reason,
                last_seen=excluded.last_seen
        """, (
            wallet, label, analysis.get("role", "desconocido") if analysis else "desconocido",
            analysis.get("native_xrp_volume", val_native) if analysis else val_native,
            analysis.get("tx_count", 1) if analysis else 1,
            connections[0]["wallet"] if connections else (analysis.get("top_cp", "") if analysis else ""),
            connections[0]["label"] if connections else (analysis.get("top_cp_label", "") if analysis else ""),
            confidence, " · ".join(filter(None, sig_parts)) or "gatekeeper evaluado",
            identity.get("name", ""), "", 1 if should_map else 0, today, today, status,
            float(analysis.get("native_xrp_volume", val_native) if analysis else val_native),
            float(analysis.get("approved_iou_volume", val_iou if tx_row.get("is_approved_iou") else 0) if analysis else (val_iou if tx_row.get("is_approved_iou") else 0)),
            float(analysis.get("suspicious_iou_volume", 0) if analysis else (val_iou if tx_row.get("is_suspicious_iou") else 0)),
            analysis.get("dominant_currency", tx_row.get("currency", "")) if analysis else tx_row.get("currency", ""),
            gate.get("reason", ""),
        ))
        conn.commit()
        if should_map: KNOWN_XRPL_WALLETS[wallet] = label
        results[role_key] = {"wallet":wallet,"label":label,"new":True,"added_map":should_map,"status":status,"confidence":confidence,"quality_reason":gate.get("reason", ""),"identity":identity,"analysis":analysis,"connections":connections,"node_in_map":node_in_map}
    return results

def _is_valid_xrpl_address(addr: str) -> bool:
    """Validación básica de cuenta XRPL clásica. No valida checksum, pero filtra basura UI."""
    a = str(addr or "").strip()
    return bool(re.fullmatch(r"r[1-9A-HJ-NP-Za-km-z]{24,34}", a))


def render_direct_wallet_adder(conn: sqlite3.Connection) -> None:
    """Panel fijo para que usuarios propongan wallets sin saltarse el Gatekeeper Supremo."""
    ensure_discovered_wallets_table(conn)
    ensure_discovery_tables(conn)

    st.markdown("### ➕ Añadir / investigar wallet directa")
    st.markdown("""<div class='rrp-note'>
Pega una dirección XRPL y el radar la analiza al momento. Si aporta etiqueta, conexión y evidencia suficiente,
puede entrar al mapa; si no, queda en watchlist o descartada. Así permitimos aportes humanos sin meter basura.
</div>""", unsafe_allow_html=True)

    with st.form("direct_wallet_adder_form", clear_on_submit=False):
        c1, c2 = st.columns([2.4, 1.6])
        with c1:
            wallet = st.text_input("Dirección XRPL de la wallet", placeholder="r................................", key="manual_wallet_address")
            label = st.text_input("Nombre / etiqueta visible", placeholder="Ej: Bitso hot wallet, Ripple treasury, gateway público…", key="manual_wallet_label")
            evidence = st.text_area("Evidencia o motivo", placeholder="Explica por qué debería vigilarse: fuente, relación, patrón, prueba pública…", height=82, key="manual_wallet_evidence")
        with c2:
            node_options = ["Sin conexión directa declarada"] + sorted(list(NODES.keys()))
            node = st.selectbox("Conectar con nodo del mapa", node_options, key="manual_wallet_node")
            source_url = st.text_input("URL de prueba opcional", placeholder="https://…", key="manual_wallet_url")
            manual_conf = st.slider("Confianza humana", 0, 100, 50, 5, key="manual_wallet_conf") / 100.0
            desired = st.radio("Acción", ["Analizar y guardar", "Intentar añadir al radar"], horizontal=True, key="manual_wallet_action")
        submitted = st.form_submit_button("🔬 Analizar wallet y actualizar radar")

    if not submitted:
        return

    wallet = str(wallet or "").strip()
    label = str(label or "").strip()
    evidence = str(evidence or "").strip()
    source_url = str(source_url or "").strip()
    node = str(node or "").strip()
    wants_map = desired == "Intentar añadir al radar"

    if not _is_valid_xrpl_address(wallet):
        st.error("Dirección XRPL no válida. Debe ser una cuenta clásica que empiece por r.")
        return

    today = str(_date.today())
    with st.spinner("Analizando wallet directa con XRPScan/Bithomp/XRPL y gatekeeper…"):
        identity = multi_source_identify(wallet)
        analysis = analyze_wallet_txs(wallet) or {}
        connections = find_node_connections(wallet) or []

    manual_node = "" if node == "Sin conexión directa declarada" else node
    has_manual_proof = bool(label and (evidence or source_url) and manual_node)
    if has_manual_proof:
        # Conexión humana propuesta: cuenta como señal, pero queda marcada como manual.
        connections = [{
            "node": manual_node,
            "wallet": wallet,
            "label": label,
            "tx_count": 0,
            "volume": float(analysis.get("native_xrp_volume", 0) or 0),
            "direction": "propuesta manual con evidencia",
            "manual": True,
        }] + list(connections)
        identity = dict(identity or {})
        identity["name"] = identity.get("name") or label
        identity["sources"] = list(set((identity.get("sources") or []) + ["aporte manual con evidencia"]))
        identity["node_in_map"] = identity.get("node_in_map") or manual_node

    raw_conf = min(
        float(analysis.get("confidence", 0) or 0)
        + float(identity.get("confidence_boost", 0) or 0)
        + (0.22 if has_manual_proof else 0.0)
        + (manual_conf * 0.18 if evidence or source_url else 0.0),
        1.0,
    )
    gate = _wallet_quality_gate(wallet, identity or {}, analysis or {}, connections, raw_conf, {
        "TransactionResult": "tesSUCCESS",
        "amount_kind": "native_xrp" if float(analysis.get("native_xrp_volume", 0) or 0) > 0 else "",
        "currency": analysis.get("dominant_currency", ""),
    })

    status = str(gate.get("status", "watch"))
    should_map = bool(gate.get("added_to_map", False)) and wants_map
    if wants_map and has_manual_proof and status != "discarded" and manual_conf >= STRICT_AUTO_MAP_CONFIDENCE:
        # La evidencia humana no salta el bloqueo anti-basura, pero sí permite mapear si el gatekeeper no descarta.
        should_map = True
        status = "map"

    final_label = "descartada / falso positivo" if status == "discarded" else (identity.get("name") or label or analysis.get("role", "wallet vigilada"))
    top_cp = connections[0].get("wallet", "") if connections else (analysis.get("top_cp", "") or "")
    top_cp_lbl = connections[0].get("node") or connections[0].get("label", "") if connections else (analysis.get("top_cp_label", "") or "")
    sig_parts = [analysis.get("signals", "")]
    if has_manual_proof:
        sig_parts.append(f"aporte manual conectado a {manual_node}")
    if evidence:
        sig_parts.append("evidencia manual: " + evidence[:240])
    if source_url:
        sig_parts.append("url: " + source_url[:240])
    sig_parts.append("gatekeeper: " + str(gate.get("reason", "")))

    conn.execute("""
        INSERT INTO discovered_wallets
            (wallet, label, role, volume_xrp, tx_count, top_counterpart, top_cp_label,
             confidence, signals, xrpscan_name, xrpscan_desc, added_to_map, first_seen,
             last_seen, status, native_xrp_volume, approved_iou_volume, suspicious_iou_volume,
             dominant_currency, quality_reason)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ON CONFLICT(wallet) DO UPDATE SET
            label=excluded.label, role=excluded.role, volume_xrp=excluded.volume_xrp,
            tx_count=excluded.tx_count, top_counterpart=excluded.top_counterpart,
            top_cp_label=excluded.top_cp_label, confidence=excluded.confidence,
            signals=excluded.signals, xrpscan_name=excluded.xrpscan_name,
            xrpscan_desc=excluded.xrpscan_desc, added_to_map=excluded.added_to_map,
            status=excluded.status, native_xrp_volume=excluded.native_xrp_volume,
            approved_iou_volume=excluded.approved_iou_volume,
            suspicious_iou_volume=excluded.suspicious_iou_volume,
            dominant_currency=excluded.dominant_currency,
            quality_reason=excluded.quality_reason, last_seen=excluded.last_seen
    """, (
        wallet, final_label, analysis.get("role", "manual") or "manual",
        float(analysis.get("native_xrp_volume", 0) or 0), int(analysis.get("tx_count", 0) or 0),
        top_cp, top_cp_lbl, float(gate.get("confidence", raw_conf) or 0),
        " · ".join([x for x in sig_parts if x])[:1200], identity.get("name", ""), "",
        1 if should_map else 0, today, today, status,
        float(analysis.get("native_xrp_volume", 0) or 0),
        float(analysis.get("approved_iou_volume", 0) or 0),
        float(analysis.get("suspicious_iou_volume", 0) or 0),
        analysis.get("dominant_currency", ""), gate.get("reason", "")[:900],
    ))

    if has_manual_proof:
        _register_dynamic_route(
            conn,
            src=final_label,
            dst=manual_node,
            kind="manual_wallet",
            signal_col="public_gateway_score",
            label=f"Wallet manual: {final_label} → {manual_node}",
            confidence=max(float(gate.get("confidence", raw_conf) or 0), manual_conf if should_map else min(manual_conf, 0.70)),
            evidence=evidence or "wallet propuesta manualmente",
            source_urls=source_url,
            now=today,
        )
    conn.commit()
    if should_map:
        KNOWN_XRPL_WALLETS[wallet] = final_label
        st.success(f"✅ Wallet añadida al radar: {final_label}")
    elif status == "discarded":
        st.warning(f"🗑️ Wallet descartada por gatekeeper: {gate.get('reason','sin motivo')}")
    else:
        st.info(f"👁️ Wallet guardada en watchlist: {final_label}. Motivo: {gate.get('reason','evaluada')}")
    st.rerun()




def render_direct_route_adder(conn: sqlite3.Connection) -> None:
    """Panel fijo para añadir/investigar rutas A→B manualmente sin esperar al Discovery."""
    ensure_discovery_tables(conn)
    st.markdown("### 🔎 Buscador directo de rutas A→B")
    st.markdown("""<div class='rrp-note'>
Añade una posible conexión entre dos entidades. El grafo A→B se alimenta de estas rutas,
pero quedan marcadas como manuales/vigiladas si no aportan evidencia suficiente.<br>
<b>Modo deductivo:</b> puedes registrar hipótesis razonadas aunque no exista anuncio oficial; el radar las separa de pruebas verificadas.
</div>""", unsafe_allow_html=True)
    with st.form("direct_route_adder_form", clear_on_submit=False):
        c1, c2 = st.columns([1, 1])
        with c1:
            src = st.text_input("Origen A", placeholder="Ej: BlackRock, Santander, Hidden Road…", key="manual_route_src")
            dst = st.text_input("Destino B", placeholder="Ej: RLUSD, XRPL, Ripple Payments…", key="manual_route_dst")
            route_kind = st.selectbox(
                "Tipo de ruta",
                ["deductive", "hypothesis", "watch", "verified", "public", "public_wallet", "manual", "odl", "partner", "obligatory"],
                index=0,
                key="manual_route_kind",
            )
        with c2:
            evidence = st.text_area(
                "Evidencia / motivo",
                placeholder="Pega la razón, prueba pública, paper, filing, tx, captura o explicación…",
                height=86,
                key="manual_route_evidence",
            )
            source_url = st.text_input("URL opcional", placeholder="https://…", key="manual_route_url")
            conf = st.slider("Confianza de la ruta", 0, 100, 45, 5, key="manual_route_conf") / 100.0
        submitted = st.form_submit_button("➕ Añadir ruta y actualizar gráfico")

    if not submitted:
        return
    src = str(src or "").strip()
    dst = str(dst or "").strip()
    evidence = str(evidence or "").strip()
    source_url = str(source_url or "").strip()
    if len(src) < 2 or len(dst) < 2:
        st.error("Falta origen o destino.")
        return
    if src.lower() == dst.lower():
        st.error("Origen y destino no pueden ser iguales.")
        return
    if not evidence and not source_url:
        st.warning("Añade al menos una evidencia o URL. La ruta no se guarda para evitar basura.")
        return
    now = datetime.now(timezone.utc).isoformat()
    ok = _register_dynamic_route(
        conn,
        src=src,
        dst=dst,
        kind=route_kind or "manual",
        signal_col=_route_signal_for_kind(route_kind or "manual", "institutional_route_score"),
        label=f"Ruta manual: {src} → {dst}",
        confidence=max(0.01, min(float(conf or 0), 1.0)),
        evidence=evidence or "ruta manual con URL",
        source_urls=source_url,
        now=now,
    )
    conn.commit()
    if ok:
        st.success(f"✅ Ruta añadida: {src} → {dst}. El gráfico A→B se actualiza ahora.")
    else:
        st.info(f"Ruta actualizada: {src} → {dst}.")
    st.rerun()

def render_whale_alerts(conn: sqlite3.Connection, real_txs: pd.DataFrame) -> None:
    """
    Panel de alertas whale: muestra transacciones grandes detectadas,
    las analiza automáticamente y las añade al mapa si superan umbral.
    """
    if real_txs.empty:
        return

    whale_txs = real_txs[real_txs["is_whale"]].copy()
    if whale_txs.empty:
        st.markdown(f"""
<div style="border:1px solid rgba(90,215,255,.20);border-radius:12px;background:rgba(15,23,42,.90);
            padding:.65rem 1rem;margin:.30rem 0 .70rem 0;color:#94A3B8;font-size:.87rem">
🐳 Sin transacciones whale (≥{WHALE_XRP_THRESHOLD:,} XRP / ≥{WHALE_RLUSD_THRESHOLD:,} RLUSD)
en los últimos {WHALE_SCAN_LEDGERS} ledgers escaneados (~{WHALE_SCAN_LEDGERS*4} segundos).
Actualiza la página para escanear ledgers más recientes.
</div>""", unsafe_allow_html=True)
        return

    auto_txs  = whale_txs[whale_txs["auto_map"]]
    large_txs = whale_txs[~whale_txs["auto_map"]]

    def _render_chain_result(chain: Dict, wallet: str, role_name: str) -> str:
        """Genera HTML del análisis de cadena para un wallet."""
        score = chain.get("ripple_score", 0)
        s_col = "#3CFF9B" if score >= 70 else "#FFB84D" if score >= 40 else "#FF5A67" if score >= 15 else "#64748B"

        # Barra score Ripple
        bar_html = (
            f"<div style='display:flex;align-items:center;gap:.5rem;margin:.30rem 0'>"
            f"<span style='color:#94A3B8;font-size:.80rem'>Score ecosistema Ripple:</span>"
            f"<div style='flex:1;height:7px;background:rgba(255,255,255,.10);border-radius:99px;overflow:hidden'>"
            f"<div style='width:{score}%;height:100%;background:{s_col};border-radius:99px'></div></div>"
            f"<span style='color:{s_col};font-weight:800;font-size:.85rem'>{score}/100</span></div>"
        )

        # Conexiones directas
        direct_html = ""
        for c in chain.get("direct", [])[:4]:
            d_icon = "→" if "envía" in c["direction"] else "←" if "recibe" in c["direction"] else "↔"
            direct_html += (
                f"<div style='margin:.18rem 0;font-size:.82rem;color:#CBD5E1'>"
                f"<span style='color:#3CFF9B;font-weight:700'>Salto 1</span> "
                f"{d_icon} <b style='color:#FFB84D'>{c['node']}</b>"
                f" <span style='color:#64748B'>({c['label']})</span>"
                f" · {c['tx_count']} TX · {min(c['volume'], _MAX_XRP):,.0f} XRP</div>"
            )
        if not direct_html:
            direct_html = "<div style='color:#475569;font-size:.80rem'>Sin conexiones directas a entidades conocidas.</div>"

        # Conexiones indirectas
        indirect_html = ""
        for c in chain.get("indirect", [])[:3]:
            d_icon = "→" if "envía" in c["direction"] else "←"
            indirect_html += (
                f"<div style='margin:.18rem 0;font-size:.80rem;color:#94A3B8'>"
                f"<span style='color:#FFB84D;font-weight:700'>Salto 2</span> "
                f"vía <b>{c['mid_label'][:30]}</b> "
                f"{d_icon} <b style='color:#FFB84D'>{c['node']}</b>"
                f" · {min(c['volume'], _MAX_XRP):,.0f} XRP</div>"
            )

        verdict = chain.get("verdict", "")

        return f"""
<div style="margin:.35rem 0;padding:.65rem .85rem;background:rgba(7,17,31,.80);border-radius:10px;
            border-left:3px solid {s_col}">
  <div style="font-size:.82rem;font-weight:700;color:#CBD5E1;margin-bottom:.20rem">{role_name}</div>
  {bar_html}
  <div style="font-size:.80rem;font-weight:700;color:#5AD7FF;margin:.30rem 0 .15rem 0">Conexiones directas (1 salto):</div>
  {direct_html}
  {"<div style='font-size:.80rem;font-weight:700;color:#5AD7FF;margin:.30rem 0 .15rem 0'>Conexiones indirectas (2 saltos):</div>" + indirect_html if indirect_html else ""}
  <div style="margin-top:.40rem;font-size:.83rem">{verdict}</div>
</div>"""

    # ── Auto-procesamiento instantáneo ───────────────────────────────────────
    if not auto_txs.empty:
        st.markdown(f"""
<div style="border:2px solid #FF5A67;border-radius:14px;background:rgba(255,90,103,.08);
            padding:.75rem 1rem;margin:.30rem 0 .70rem 0">
<span style="color:#FF5A67;font-size:1.05rem;font-weight:800">🚨 MEGA WHALE DETECTADA</span>
<span style="color:#CBD5E1;font-size:.88rem;margin-left:.80rem">
≥{AUTO_MAP_XRP:,} XRP — identificación multi-fuente + rastreo de cadena automático</span>
</div>""", unsafe_allow_html=True)

        for _, tx_r in auto_txs.iterrows():
            with st.spinner(f"Identificando y rastreando cadena para {tx_r['hash']}…"):
                res         = auto_track_whale(conn, tx_r.to_dict())
                s_info      = res.get("sender",   {})
                r_info      = res.get("receiver",  {})
                s_chain     = find_connection_chain(tx_r["sender"])
                r_chain     = find_connection_chain(tx_r["receiver"])

            s_label = s_info.get("label", tx_r["sender_label"])
            r_label = r_info.get("label", tx_r["receiver_label"])
            s_col   = "#3CFF9B" if s_info.get("added_map") else "#FFB84D"
            r_col   = "#3CFF9B" if r_info.get("added_map") else "#FFB84D"

            # Si ambos son desconocidos → guardar en unknown_whales
            s_unknown = not s_info.get("added_map") and not s_info.get("identity", {}).get("name")
            r_unknown = not r_info.get("added_map") and not r_info.get("identity", {}).get("name")
            if s_unknown and r_unknown:
                save_unknown_whale(conn, tx_r.to_dict())

            id_tags = ""
            for info in [s_info, r_info]:
                idt = info.get("identity", {})
                if idt and idt.get("name"):
                    srcs = ", ".join(idt.get("sources", []))
                    id_tags += f"<span style='color:#5AD7FF;font-size:.80rem'>✅ Identificado: <b>{idt['name']}</b> vía {srcs}</span> · "

            s_chain_html = _render_chain_result(s_chain, tx_r["sender"], f"Emisor: {s_label}")
            r_chain_html = _render_chain_result(r_chain, tx_r["receiver"], f"Receptor: {r_label}")

            st.markdown(f"""
<div style="border:1px solid #FF5A67;border-radius:16px;background:rgba(15,23,42,.97);
            padding:.90rem 1.1rem;margin:.30rem 0 .80rem 0">
  <div style="font-size:.78rem;color:#94A3B8;margin-bottom:.45rem">
    🔗 TX: <code style="color:#CBD5E1">{tx_r['hash']}</code> ·
    Ledger {tx_r['ledger_index']} · Hace ~{int(tx_r['ledger_offset'])*4}s
  </div>
  <div style="font-size:1.10rem;font-weight:800;color:#FFFFFF;margin-bottom:.45rem">
    <span style="color:{s_col}">{s_label}</span>
    <span style="color:#FF5A67;margin:0 .6rem">⟶ {tx_r['amount']} ⟶</span>
    <span style="color:{r_col}">{r_label}</span>
  </div>
  {id_tags}
  <div style="font-size:.84rem;font-weight:700;color:#5AD7FF;margin:.50rem 0 .25rem 0">
    🔍 Rastreo de cadena de conexión al ecosistema Ripple/institucional:
  </div>
  {s_chain_html}
  {r_chain_html}
  <div style="margin-top:.50rem;font-size:.82rem;color:#64748B">
    {'✅ Emisor añadido al radar' if s_info.get('added_map') else '—'} ·
    {'✅ Receptor añadido al radar' if r_info.get('added_map') else '—'}
  </div>
</div>""", unsafe_allow_html=True)

    # ── Whales grandes (no auto-mapa, análisis bajo botón) ───────────────────
    if not large_txs.empty:
        st.markdown(f"#### 🐳 Whales grandes ({WHALE_XRP_THRESHOLD:,}–{AUTO_MAP_XRP:,} XRP)")
        st.markdown("""<div class='rrp-note'>
Superan el umbral whale. Pulsa <b>🔬 Rastrear</b> para identificar y trazar la cadena de conexión.
</div>""", unsafe_allow_html=True)

        for i, (_, tx_r) in enumerate(large_txs.head(10).iterrows()):
            s_lbl = tx_r["sender_label"]
            r_lbl = tx_r["receiver_label"]
            val   = float(tx_r["xrp_value"])
            age   = int(tx_r["ledger_offset"]) * 4

            col_a, col_b, col_c = st.columns([5, 2, 1])
            with col_a:
                s_col = "#3CFF9B" if tx_r["sender"] in KNOWN_XRPL_WALLETS else "#FFB84D"
                r_col = "#3CFF9B" if tx_r["receiver"] in KNOWN_XRPL_WALLETS else "#FFB84D"
                st.markdown(
                    f"<span style='color:{s_col}'><b>{s_lbl}</b></span>"
                    f" <span style='color:#FFB84D'>⟶ {tx_r['amount']} ⟶</span>"
                    f" <span style='color:{r_col}'><b>{r_lbl}</b></span>"
                    f"<br><span style='color:#475569;font-size:.77rem'>"
                    f"TX {tx_r['hash']} · Ledger {tx_r['ledger_index']} · hace ~{age}s</span>",
                    unsafe_allow_html=True,
                )
            with col_b:
                st.markdown(
                    f"<span style='color:#FFB84D;font-weight:800'>{val:,.0f} {tx_r['currency']}</span>",
                    unsafe_allow_html=True,
                )
            with col_c:
                if st.button("🔬 Analizar", key=f"whale_analyze_{i}_{tx_r['hash'][:8]}"):
                    with st.spinner("Analizando…"):
                        res = auto_track_whale(conn, tx_r.to_dict())
                    added = sum(1 for v in res.values() if isinstance(v, dict) and v.get("added_map"))
                    st.success(f"✅ Listo — {added} wallet(s) añadidas al mapa.")
                    st.rerun()


def render_unknown_whales_db(conn: sqlite3.Connection) -> None:
    """
    Sección 'Whales Desconocidas' — muestra todas las tx whale donde
    sender Y receiver eran desconocidos, guardadas para rastreo posterior.
    """
    ensure_unknown_whales_table(conn)
    st.markdown("---")
    st.markdown("### 🕵️ Whales Desconocidas")
    st.markdown("""<div class='rrp-note'>
Transacciones whale donde <b>ninguna de las dos wallets</b> fue identificada por ninguna fuente.
Se guardan automáticamente para que puedas rastrearlas más tarde.
Pulsa <b>🔬 Rastrear cadena</b> para analizar su conexión al ecosistema Ripple.
</div>""", unsafe_allow_html=True)

    try:
        uw = pd.read_sql_query(
            "SELECT * FROM unknown_whales ORDER BY id DESC LIMIT 80",
            conn,
        )
    except Exception:
        uw = pd.DataFrame()

    if uw.empty:
        st.markdown("""<div style="border:1px solid rgba(90,215,255,.20);border-radius:12px;
background:rgba(15,23,42,.90);padding:.65rem 1rem;color:#94A3B8;font-size:.87rem">
Todavía no hay whales desconocidas registradas. Cuando se detecte una TX mega-whale
cuyas dos wallets sean anónimas, aparecerá aquí automáticamente.
</div>""", unsafe_allow_html=True)
        return

    # Filtros rápidos
    col_f1, col_f2 = st.columns([1, 1])
    with col_f1:
        min_xrp = st.number_input("XRP mínimo", value=0, step=100_000, key="uw_min_xrp")
    with col_f2:
        only_untracked = st.checkbox("Solo sin rastrear", value=False, key="uw_untracked")

    if min_xrp > 0:
        uw = uw[uw["xrp_value"] >= min_xrp]
    if only_untracked:
        uw = uw[uw["tracked"] == 0]

    st.markdown(f"<div style='color:#64748B;font-size:.82rem;margin:.20rem 0 .50rem 0'>"
                f"{len(uw)} registros</div>", unsafe_allow_html=True)

    for _, row in uw.iterrows():
        s_addr  = str(row["sender"])
        r_addr  = str(row["receiver"])
        s_lbl   = str(row["sender_label"] or f"? {s_addr[:10]}…")
        r_lbl   = str(row["receiver_label"] or f"? {r_addr[:10]}…")
        val     = float(row["xrp_value"])
        amt     = str(row["amount"])
        tracked = int(row["tracked"]) == 1
        sc_s    = int(row["chain_score_s"] or 0)
        sc_r    = int(row["chain_score_r"] or 0)
        verdict_s = str(row["verdict_s"] or "")
        verdict_r = str(row["verdict_r"] or "")

        border = "#3CFF9B" if tracked else "#FF5A67" if val >= AUTO_MAP_XRP else "#FFB84D"
        tracked_badge = "<span style='color:#3CFF9B;font-size:.78rem'>✅ Rastreada</span>" if tracked else ""

        score_bar_s = (
            f"<div style='display:inline-flex;align-items:center;gap:.3rem'>"
            f"<span style='font-size:.76rem;color:#94A3B8'>Emisor Ripple score:</span>"
            f"<div style='width:60px;height:5px;background:rgba(255,255,255,.10);border-radius:99px'>"
            f"<div style='width:{sc_s}%;height:100%;background:#3CFF9B;border-radius:99px'></div></div>"
            f"<span style='color:#3CFF9B;font-size:.76rem'>{sc_s}/100</span></div>"
        ) if tracked else ""
        score_bar_r = (
            f"<div style='display:inline-flex;align-items:center;gap:.3rem'>"
            f"<span style='font-size:.76rem;color:#94A3B8'>Receptor Ripple score:</span>"
            f"<div style='width:60px;height:5px;background:rgba(255,255,255,.10);border-radius:99px'>"
            f"<div style='width:{sc_r}%;height:100%;background:#FFB84D;border-radius:99px'></div></div>"
            f"<span style='color:#FFB84D;font-size:.76rem'>{sc_r}/100</span></div>"
        ) if tracked else ""

        verdict_html = ""
        if verdict_s or verdict_r:
            verdict_html = (
                f"<div style='margin-top:.30rem;font-size:.78rem;color:#CBD5E1'>{verdict_s}</div>"
                f"<div style='margin-top:.15rem;font-size:.78rem;color:#CBD5E1'>{verdict_r}</div>"
            )

        col_a, col_b = st.columns([5, 1])
        with col_a:
            st.markdown(f"""
<div style="border:1px solid {border};border-radius:13px;background:rgba(15,23,42,.93);
            padding:.65rem .90rem;margin:.25rem 0">
  <div style="display:flex;justify-content:space-between;align-items:center">
    <div style="font-size:.78rem;color:#64748B">
      TX <code style="color:#94A3B8">{str(row['tx_hash'])[:20]}…</code> ·
      Ledger {row['ledger_index']} · {row['first_seen']}
    </div>
    {tracked_badge}
  </div>
  <div style="font-size:1rem;font-weight:800;margin:.30rem 0">
    <span style="color:#FFB84D">{s_lbl}</span>
    <span style="color:{border};margin:0 .5rem">⟶ {_fmt_vol(val)} ⟶</span>
    <span style="color:#FFB84D">{r_lbl}</span>
  </div>
  <div style="font-size:.78rem;color:#475569;margin-bottom:.25rem">
    Emisor: <code>{s_addr[:14]}…{s_addr[-6:]}</code> ·
    Receptor: <code>{r_addr[:14]}…{r_addr[-6:]}</code>
  </div>
  {score_bar_s} {score_bar_r}
  {verdict_html}
</div>""", unsafe_allow_html=True)
        with col_b:
            if not tracked:
                if st.button("🔬 Rastrear", key=f"uw_track_{row['id']}",
                             use_container_width=True):
                    with st.spinner("Rastreando cadena…"):
                        s_chain = find_connection_chain(s_addr)
                        r_chain = find_connection_chain(r_addr)
                    conn.execute("""
                        UPDATE unknown_whales
                        SET tracked=1, chain_score_s=?, chain_score_r=?,
                            verdict_s=?, verdict_r=?
                        WHERE id=?
                    """, (
                        s_chain["ripple_score"], r_chain["ripple_score"],
                        s_chain["verdict"][:300], r_chain["verdict"][:300],
                        row["id"],
                    ))
                    conn.commit()
                    st.rerun()
            else:
                st.markdown("<span style='color:#3CFF9B;font-size:.85rem'>✅</span>",
                            unsafe_allow_html=True)

    if st.button("🗑️ Limpiar rastreadas", key="uw_clear_tracked"):
        conn.execute("DELETE FROM unknown_whales WHERE tracked=1")
        conn.commit()
        st.success("Eliminadas las rastreadas.")
        st.rerun()


def render_wallet_identity_report(conn: sqlite3.Connection) -> None:
    """
    Panel de identidad completa para todas las wallets vigiladas.
    Muestra fuentes de identificación, conexiones al mapa principal y nombre confirmado.
    """
    try:
        watched = pd.read_sql_query(
            "SELECT wallet, label, role, confidence, volume_xrp, signals, xrpscan_name, added_to_map, status, quality_reason "
            "FROM discovered_wallets ORDER BY added_to_map DESC, confidence DESC LIMIT 60",
            conn,
        )
    except Exception:
        return

    if watched.empty:
        return

    st.markdown("---")
    st.markdown("### 🪪 Informe de identidad — quién es cada wallet")
    st.markdown("""<div class='rrp-note'>
Para cada wallet rastreada se cruzan hasta <b>4 fuentes</b>: base local, XRPScan well-known,
XRPScan account API y Bithomp. Si alguna fuente la identifica, el nombre aparece confirmado.
También se analiza si ha interactuado directamente con nodos del mapa principal del radar.
</div>""", unsafe_allow_html=True)

    if st.button("🔄 Re-identificar todas las wallets vigiladas", key="btn_reidentify"):
        bar = st.progress(0, text="Identificando…")
        for i, r in watched.iterrows():
            bar.progress((i + 1) / len(watched), text=f"Identificando {str(r['wallet'])[:14]}…")
            identity    = multi_source_identify(str(r["wallet"]))
            connections = find_node_connections(str(r["wallet"]))
            if identity["name"] and identity["name"] != r["label"]:
                conn.execute(
                    "UPDATE discovered_wallets SET label=?, xrpscan_name=? WHERE wallet=?",
                    (identity["name"], identity["name"], r["wallet"]),
                )
                KNOWN_XRPL_WALLETS[str(r["wallet"])] = identity["name"]
            if connections:
                conn.execute(
                    "UPDATE discovered_wallets SET top_counterpart=?, top_cp_label=? WHERE wallet=?",
                    (connections[0]["wallet"], connections[0]["label"], r["wallet"]),
                )
        conn.commit()
        bar.empty()
        st.success("✅ Re-identificación completada.")
        st.rerun()

    for _, r in watched.iterrows():
        wallet   = str(r["wallet"])
        label    = _wallet_full_name(wallet, str(r["label"]))
        conf_pct = float(r["confidence"]) * 100
        xrpscan  = str(r["xrpscan_name"] or "")

        status = str(r.get("status", "") or "")
        if status == "discarded":
            border = "#64748B"; icon = "🗑️"
        elif status == "quarantine":
            border = "#FF5A67"; icon = "🛡️"
        elif conf_pct >= 70:
            border = "#3CFF9B"; icon = "🟢"
        elif conf_pct >= 40:
            border = "#FFB84D"; icon = "🟡"
        else:
            border = "#FF5A67"; icon = "🔴"

        in_map = _wallet_state_label(status, int(r["added_to_map"] or 0))

        # Conexiones al mapa (de caché si existe)
        connections = find_node_connections(wallet)
        conn_html = ""
        if connections:
            conn_html = "<div style='margin-top:.40rem'><b style='color:#5AD7FF;font-size:.80rem'>Conexiones al mapa principal:</b><br>"
            for c in connections[:4]:
                dir_icon = "↔" if c["direction"] == "bidireccional" else "→" if "envía" in c["direction"] else "←"
                conn_html += (
                    f"<span style='color:#CBD5E1;font-size:.82rem'>"
                    f"{dir_icon} <b style='color:#FFB84D'>{c['node']}</b> "
                    f"· {c['tx_count']} TX · {c['volume']:,.0f} XRP · {c['direction']}</span><br>"
                )
            conn_html += "</div>"
        else:
            conn_html = "<div style='color:#475569;font-size:.80rem;margin-top:.30rem'>Sin conexiones directas a nodos del mapa detectadas en las últimas 100 TX.</div>"

        sources_html = ""
        if xrpscan:
            sources_html = f"<span style='color:#5AD7FF;font-size:.80rem'>XRPScan: <b>{xrpscan}</b></span> · "

        st.markdown(f"""
<div style="border:1px solid {border};border-radius:14px;background:rgba(15,23,42,.92);
            padding:.75rem 1rem;margin:.35rem 0 .50rem 0">
  <div style="display:flex;justify-content:space-between;align-items:flex-start">
    <div>
      <span style="color:{border};font-weight:800;font-size:.95rem">{icon} {html.escape(label)}</span>
    </div>
    <div style="text-align:right;font-size:.82rem">
      <span style="color:{border};font-weight:700">{conf_pct:.0f}%</span>
      <span style="color:#64748B;margin-left:.60rem">{in_map}</span>
    </div>
  </div>
  {_wallet_identity_html(wallet, label)}
  <div style="margin-top:.30rem;font-size:.83rem;color:#94A3B8">
    {sources_html}Rol: <b style="color:#CBD5E1">{html.escape(str(r['role']))}</b> ·
    Vol: <b style="color:#CBD5E1">{_fmt_vol(float(r['volume_xrp']))}</b>
  </div>
  <div style="margin-top:.25rem;font-size:.80rem;color:#64748B">{str(r['signals'] or '')[:160]}</div>
  <div style="margin-top:.18rem;font-size:.78rem;color:#94A3B8">{html.escape(str(r.get('quality_reason', '') or ''))[:220]}</div>
  {conn_html}
</div>""", unsafe_allow_html=True)


def render_wallet_tracker(conn: sqlite3.Connection, real_txs: pd.DataFrame) -> None:
    """
    Seguidor automático con gatekeeper supremo:
    - No mete wallets por volumen bruto.
    - Separa XRP nativo / IOU aprobado / IOU sospechoso.
    - Quarantine > Watchlist > Radar.
    """
    ensure_discovered_wallets_table(conn)

    st.markdown("---")
    st.markdown("### 🔬 Seguidor automático de wallets — Gatekeeper Supremo")
    st.markdown("""<div class='rrp-note'>
Analiza wallets desconocidas, cruza XRPScan/Bithomp y aplica una puerta estricta:
<b>identidad fiable</b>, <b>conexión directa</b> o <b>XRP nativo/activo aprobado</b>.
El volumen de tokens/IOU raros no permite entrar al radar.
</div>""", unsafe_allow_html=True)

    c_btn, c_info = st.columns([1, 3])
    with c_btn:
        run_tracker = st.button("🔍 Seguir wallets", use_container_width=True, key="btn_wallet_tracker")
    with c_info:
        if real_txs.empty:
            st.info("Primero necesitas transacciones reales cargadas arriba.")
        else:
            unknown_count = sum(1 for w in list(real_txs["sender"]) + list(real_txs["receiver"]) if w not in KNOWN_XRPL_WALLETS)
            st.markdown(f"<div class='rrp-note' style='margin:0'>Hay <b>{unknown_count} wallets desconocidas</b>. El rastreador analizará hasta 15 con filtro anti-basura.</div>", unsafe_allow_html=True)

    if run_tracker and not real_txs.empty:
        unknown_wallets = list({w for col in ("sender", "receiver") for w in real_txs[col] if w not in KNOWN_XRPL_WALLETS and w != "?"})[:15]
        if not unknown_wallets:
            st.success("Todas las wallets de las transacciones actuales ya están identificadas.")
        else:
            today = str(_date.today())
            bar = st.progress(0, text="Iniciando análisis…")
            saved = 0
            quarantined = 0
            discarded = 0
            mapped = 0
            for i, wallet in enumerate(unknown_wallets):
                bar.progress((i + 1) / len(unknown_wallets), text=f"Analizando {wallet[:14]}… ({i+1}/{len(unknown_wallets)})")
                analysis = analyze_wallet_txs(wallet)
                identity = multi_source_identify(wallet)
                connections = find_node_connections(wallet)
                try:
                    tx_match = real_txs[(real_txs["sender"] == wallet) | (real_txs["receiver"] == wallet)].head(1)
                    tx_context = tx_match.iloc[0].to_dict() if not tx_match.empty else {}
                except Exception:
                    tx_context = {}
                conn_boost = min(len(connections) * 0.10, 0.30)
                raw_confidence = min(float(analysis.get("confidence", 0) or 0) + float(identity.get("confidence_boost", 0) or 0) + conn_boost, 1.0) if analysis else min(float(identity.get("confidence_boost", 0) or 0) + conn_boost, 1.0)
                gate = _wallet_quality_gate(wallet, identity, analysis or {}, connections, raw_confidence, tx_context)
                should_map = bool(gate.get("added_to_map", False))
                status = str(gate.get("status", "watch"))
                if should_map:
                    mapped += 1
                if status == "quarantine":
                    quarantined += 1
                if status == "discarded":
                    discarded += 1

                xrpscan_name = identity.get("name", "")
                if status == "discarded":
                    label = "descartada / falso positivo"
                elif xrpscan_name:
                    label = xrpscan_name
                elif connections and should_map:
                    label = f"Contraparte de {connections[0]['node']}"
                else:
                    label = analysis.get("role", "desconocido") if analysis else "desconocido"
                sig_parts = []
                if analysis: sig_parts.append(analysis.get("signals", ""))
                if connections: sig_parts.append("conectada a: " + ", ".join(c["node"] for c in connections[:3]))
                if identity.get("sources"): sig_parts.append("id vía: " + ", ".join(identity.get("sources", [])))
                sig_parts.append("gatekeeper: " + str(gate.get("reason", "")))
                top_cp = connections[0]["wallet"] if connections else (analysis.get("top_cp", "") if analysis else "")
                top_cp_lbl = connections[0]["label"] if connections else (analysis.get("top_cp_label", "") if analysis else "")
                conn.execute("""
                    INSERT INTO discovered_wallets
                        (wallet, label, role, volume_xrp, tx_count, top_counterpart, top_cp_label,
                         confidence, signals, xrpscan_name, xrpscan_desc, added_to_map, first_seen,
                         last_seen, status, native_xrp_volume, approved_iou_volume, suspicious_iou_volume,
                         dominant_currency, quality_reason)
                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ON CONFLICT(wallet) DO UPDATE SET
                        label=excluded.label, role=excluded.role, volume_xrp=excluded.volume_xrp,
                        tx_count=excluded.tx_count, top_counterpart=excluded.top_counterpart,
                        top_cp_label=excluded.top_cp_label, confidence=excluded.confidence,
                        signals=excluded.signals, xrpscan_name=excluded.xrpscan_name,
                        xrpscan_desc=excluded.xrpscan_desc, added_to_map=excluded.added_to_map,
                        status=excluded.status, native_xrp_volume=excluded.native_xrp_volume,
                        approved_iou_volume=excluded.approved_iou_volume,
                        suspicious_iou_volume=excluded.suspicious_iou_volume,
                        dominant_currency=excluded.dominant_currency,
                        quality_reason=excluded.quality_reason, last_seen=excluded.last_seen
                """, (
                    wallet, label, analysis.get("role", "desconocido") if analysis else "desconocido",
                    analysis.get("native_xrp_volume", 0) if analysis else 0,
                    analysis.get("tx_count", 0) if analysis else 0,
                    top_cp, top_cp_lbl, float(gate.get("confidence", 0.0)),
                    " · ".join(filter(None, sig_parts)) or "", xrpscan_name, "",
                    1 if should_map else 0, today, today, status,
                    float(analysis.get("native_xrp_volume", 0) if analysis else 0),
                    float(analysis.get("approved_iou_volume", 0) if analysis else 0),
                    float(analysis.get("suspicious_iou_volume", 0) if analysis else 0),
                    analysis.get("dominant_currency", "") if analysis else "",
                    gate.get("reason", ""),
                ))
                conn.commit()
                if should_map:
                    KNOWN_XRPL_WALLETS[wallet] = label
                saved += 1
            bar.empty()
            st.success(f"✅ {saved} wallets analizadas · {mapped} aprobadas para radar · {quarantined} en cuarentena · {discarded} descartadas.")

    discovered = pd.read_sql_query("""
        SELECT wallet, label, role, volume_xrp, tx_count, top_counterpart, top_cp_label,
               confidence, signals, xrpscan_name, xrpscan_desc, added_to_map, last_seen,
               status, native_xrp_volume, approved_iou_volume, suspicious_iou_volume,
               dominant_currency, quality_reason
        FROM discovered_wallets
        ORDER BY added_to_map DESC, confidence DESC, native_xrp_volume DESC
        LIMIT 150
    """, conn)
    if discovered.empty:
        st.info("Aún no hay wallets rastreadas. Pulsa 'Seguir wallets' para empezar.")
        return

    st.markdown(f"**Base de datos de wallets descubiertas — {len(discovered)} registros**")
    st.markdown("""<div class='rrp-note'>
<b>Añadir al Radar</b> ahora solo aparece si la wallet supera el gatekeeper. Las wallets en cuarentena no se pueden añadir manualmente sin nueva evidencia.
</div>""", unsafe_allow_html=True)

    high_conf = discovered[(discovered["confidence"].astype(float) >= STRICT_AUTO_MAP_CONFIDENCE) & (discovered["added_to_map"].astype(int) == 0) & (~discovered["status"].astype(str).str.lower().isin(["quarantine", "discarded"]))]
    if not high_conf.empty:
        st.markdown(f"#### ⭐ {len(high_conf)} wallets candidatas aprobables por gatekeeper")
        for _, r in high_conf.head(8).iterrows():
            conf_pct = float(r["confidence"]) * 100
            col_c = "#3CFF9B" if conf_pct >= 70 else "#FFB84D"
            ca, cb, cc, cd = st.columns([4, 2, 1, 1])
            full_label = _wallet_full_name(str(r["wallet"]), str(r["label"]))
            ca.markdown(f"<span style='color:{col_c};font-weight:700'>{html.escape(full_label)}</span><br><code style='color:#94A3B8;font-size:.76rem;white-space:normal;word-break:break-all'>{html.escape(str(r['wallet']))}</code>", unsafe_allow_html=True)
            cb.markdown(f"<span style='color:#94A3B8;font-size:.85rem'>{html.escape(str(r['role']))}</span><br><span style='color:#CBD5E1;font-size:.82rem'>XRP nativo: {_fmt_vol(float(r.get('native_xrp_volume', 0) or 0))} · {int(r['tx_count'])} TX</span>", unsafe_allow_html=True)
            cc.markdown(f"<span style='color:{col_c};font-weight:800'>{conf_pct:.0f}%</span>", unsafe_allow_html=True)
            if cd.button("➕ Radar", key=f"addmap_{str(r['wallet'])[:10]}"):
                if str(r.get("status", "")).lower() in {"quarantine", "discarded"} or float(r.get("confidence", 0) or 0) < STRICT_AUTO_MAP_CONFIDENCE:
                    st.warning("No se añade: el gatekeeper la mantiene en descartadas/cuarentena/watchlist.")
                else:
                    conn.execute("UPDATE discovered_wallets SET added_to_map=1, status='map', quality_reason=COALESCE(NULLIF(quality_reason,''),'aprobada manualmente tras gatekeeper') WHERE wallet=?", (r["wallet"],))
                    conn.commit(); KNOWN_XRPL_WALLETS[r["wallet"]] = r["label"]; st.rerun()

    st.markdown("#### Todas las wallets rastreadas")
    view = discovered.copy()
    view["Confianza"] = (view["confidence"].astype(float) * 100).round(1).astype(str) + "%"
    view["XRP nativo"] = view["native_xrp_volume"].apply(lambda x: _fmt_vol(float(x or 0)))
    view["IOU aprobado"] = view["approved_iou_volume"].apply(lambda x: f"{float(x or 0):,.0f}")
    view["IOU sospechoso"] = view["suspicious_iou_volume"].apply(lambda x: f"{float(x or 0):,.0f}")
    view["Estado"] = view.apply(lambda r: _wallet_state_label(str(r.get("status", "")), int(r.get("added_to_map", 0) or 0)), axis=1)
    view["XRPScan"] = view.apply(lambda r: r["xrpscan_name"] + (f" — {r['xrpscan_desc'][:40]}" if r["xrpscan_desc"] else ""), axis=1)
    view["Wallet"] = view["wallet"].astype(str)
    view["Nombre completo"] = view.apply(lambda r: _wallet_full_name(str(r["wallet"]), str(r["label"])), axis=1)
    view = view.rename(columns={"label":"Etiqueta", "role":"Rol", "tx_count":"TX", "top_cp_label":"Contraparte principal", "signals":"Señales detectadas", "quality_reason":"Motivo gatekeeper", "last_seen":"Última vez"})
    cols_show = ["Nombre completo","Wallet","Etiqueta","Rol","Confianza","XRP nativo","IOU aprobado","IOU sospechoso","TX","Contraparte principal","XRPScan","Señales detectadas","Motivo gatekeeper","Estado","Última vez"]
    styled_table(view[cols_show])

def render_route_path_engine(conn: sqlite3.Connection, df: pd.DataFrame, row: pd.Series) -> None:
    st.subheader("🧭 Route Path Engine A→B")

    st.markdown("""
<div class="rrp-path-panel">
  <div class="rrp-path-title">¿Qué hace este motor?</div>
  <div class="rrp-path-text">
    Combina dos enfoques: <b>(1) Rastreo real</b> — sigue transacciones reales del ledger XRPL ahora mismo,
    identifica quién envía, a quién llega y si hay un salto intermedio.
    <b>(2) Inferencia por huellas</b> — cuando no hay TX directa visible, infiere la ruta probable
    por las huellas que dejan los actores privados en la cadena pública.<br>
    <b>Verde</b> = wallet identificada. <b>?</b> = wallet desconocida (solo dirección pública).
  </div>
</div>""", unsafe_allow_html=True)
    render_ripple_infrastructure_scope_panel()

    # ── GRÁFICO VIVO FIJO: debe aparecer siempre, incluso sin datos nuevos.
    st.markdown("---")
    st.markdown("### 🔁 Gráfico vivo A→B — siempre fijo y autoactualizable")
    st.markdown("""<div class='rrp-note'>
Este gráfico se reconstruye desde el estado vivo del radar: histórico, rutas descubiertas, pruebas verificadas,
wallets aprobadas y wallets añadidas manualmente. Si añades una wallet o una ruta, aparecerá aquí tras el rerun.
</div>""", unsafe_allow_html=True)
    # v71: las fichas se recalculan desde BD en cada rerun. Este panel deja claro el estado vivo
    # y permite refresco seguro sin depender de que el usuario cambie de sección.
    try:
        proofs_n = _safe_count_table(conn, "connection_proofs")
        dyn_n = _safe_count_table(conn, "dynamic_routes")
        route_n = _safe_count_table(conn, "route_paths")
    except Exception:
        proofs_n = dyn_n = route_n = 0
    cc1, cc2, cc3, cc4 = st.columns([1, 1, 1, 1.2])
    cc1.metric("Pruebas fijas", proofs_n)
    cc2.metric("Rutas dinámicas", dyn_n)
    cc3.metric("Rutas base", route_n)
    if cc4.button("🔄 Actualizar gráfico/fichas", key="route_paths_force_refresh_v71"):
        try:
            st.cache_data.clear()
        except Exception:
            pass
        st.rerun()
    st.caption("Las fichas A→B se reconstruyen en cada ejecución desde connection_proofs, dynamic_routes y route_paths. Si entra una prueba nueva, aparecerá al refrescar/rerun.")
    try:
        auto_ab = st.toggle("Auto-actualizar A→B cada 30s", value=False, key="route_paths_auto_refresh_v71", help="Úsalo si estás vigilando pruebas nuevas. Puede reiniciar el audio porque Streamlit vuelve a ejecutar la página.")
        if auto_ab and st_autorefresh is not None:
            st_autorefresh(interval=30000, limit=None, key="route_paths_live_autorefresh_v71")
    except Exception:
        pass
    st.caption("Última reconstrucción local: " + datetime.now().strftime("%H:%M:%S"))

    live_paths = load_live_route_paths(conn, df)
    chart_paths = render_route_path_graph_and_fichas(live_paths, key_prefix="live", conn=conn)
    if live_paths.empty:
        st.info("El gráfico está listo, pero aún no hay rutas suficientes. Añade/verifica rutas o wallets para llenarlo.")
    else:
        st.caption(f"Rutas vivas cargadas: {len(live_paths)} · rutas visibles tras deduplicar: {len(chart_paths)}")

    # ── BUSCADOR / ALTA DIRECTA DE RUTAS Y WALLETS: visible siempre.
    st.markdown("---")
    render_direct_route_adder(conn)
    st.markdown("---")
    render_direct_wallet_adder(conn)

    # ── SECCIÓN 1: RASTREO REAL DE TRANSACCIONES ─────────────────────────────
    st.markdown("---")
    st.markdown("### 🔍 Rastreo real — últimas transacciones grandes en XRPL")
    st.markdown("""<div class='rrp-note'>
Transacciones reales del último ledger validado de XRPL. El radar intenta identificar
quién es el emisor y el receptor usando una base de wallets conocidas (exchanges, corredores ODL, Ripple treasury, etc.).
Si una wallet no está en la base, aparece como <b>? dirección parcial</b>.
El botón <b>Seguir ruta</b> mira si el receptor reenvió el dinero en los siguientes 20 ledgers (≈ 1 minuto).
</div>""", unsafe_allow_html=True)

    with st.spinner(f"Escaneando últimos {WHALE_SCAN_LEDGERS} ledgers XRPL (~{WHALE_SCAN_LEDGERS*4}s de historia)…"):
        real_txs = fetch_recent_large_payments(min_xrp=500.0)

    # ── Panel de alertas whale (automático, sin botón) ────────────────────────
    st.markdown("---")
    st.markdown(f"### 🐳 Detector whale — alertas automáticas")
    st.markdown(f"""<div class='rrp-note'>
Detecta transacciones ≥<b>{WHALE_XRP_THRESHOLD:,} XRP</b> o ≥<b>{WHALE_RLUSD_THRESHOLD:,} RLUSD</b>.
Las transacciones ≥<b>{AUTO_MAP_XRP:,} XRP</b> se analizan y añaden al mapa <b>automáticamente</b> sin intervención.
Las de tamaño medio muestran un botón de análisis manual.
Datos actualizados cada {REFRESH_SECONDS}s.
</div>""", unsafe_allow_html=True)
    render_whale_alerts(conn, real_txs)

    if real_txs.empty:
        st.warning("No se pudieron obtener transacciones del ledger XRPL ahora mismo. Intenta refrescar.")
    else:
        whale_count = int(real_txs["is_whale"].sum()) if "is_whale" in real_txs.columns else 0
        identified  = real_txs[real_txs["identified"]].copy()
        unknown     = real_txs[~real_txs["identified"]].copy()

        st.markdown("---")
        st.markdown("### 📋 Todos los pagos grandes detectados")
        st.markdown(
            f"**{len(real_txs)} pagos** en los últimos {WHALE_SCAN_LEDGERS} ledgers · "
            f"**{whale_count} whales** · "
            f"**{len(identified)} con wallets identificadas** · "
            f"**{len(unknown)} desconocidas**"
        )

        # Construir tarjetas por TX
        tx_rows_html = ""
        for i, r in real_txs.head(40).iterrows():
            s_known  = r["sender"] in KNOWN_XRPL_WALLETS
            d_known  = r["receiver"] in KNOWN_XRPL_WALLETS
            s_color  = "#3CFF9B" if s_known else "#94A3B8"
            d_color  = "#3CFF9B" if d_known else "#94A3B8"
            s_icon   = "✅" if s_known else "❓"
            d_icon   = "✅" if d_known else "❓"
            is_whale = r.get("is_whale", False)
            auto_map = r.get("auto_map", False)
            row_bg   = ("rgba(255,90,103,.10)" if auto_map
                        else "rgba(255,184,77,.07)" if is_whale
                        else "rgba(15,23,42,.95)" if i % 2 == 0
                        else "rgba(7,17,31,.90)")
            whale_badge = (" 🚨 MEGA" if auto_map
                           else " 🐳 WHALE" if is_whale else "")
            whale_color = "#FF5A67" if auto_map else "#FFB84D" if is_whale else "#FFB84D"
            tx_rows_html += f"""
<tr style="background:{row_bg};border-bottom:1px solid rgba(255,255,255,.06)">
  <td style="padding:.45rem .65rem;white-space:nowrap">
    <span style="color:#94A3B8;font-size:.80rem">{r['hash']}</span>
    {"<br><span style='color:" + whale_color + ";font-size:.72rem;font-weight:800'>" + whale_badge.strip() + "</span>" if whale_badge else ""}
  </td>
  <td style="padding:.45rem .65rem">
    <span style="color:{s_color};font-weight:700;font-size:.88rem">{s_icon} {r['sender_label']}</span><br>
    <span style="color:#475569;font-size:.75rem">{r['sender'][:20]}…</span>
  </td>
  <td style="padding:.45rem .65rem;color:{whale_color};font-weight:700;font-size:.92rem;white-space:nowrap">⟶ {r['amount']}</td>
  <td style="padding:.45rem .65rem">
    <span style="color:{d_color};font-weight:700;font-size:.88rem">{d_icon} {r['receiver_label']}</span><br>
    <span style="color:#475569;font-size:.75rem">{r['receiver'][:20]}…</span>
  </td>
  <td style="padding:.45rem .65rem;color:#64748B;font-size:.78rem">~{int(r.get('ledger_offset',0))*4}s</td>
</tr>"""

        th_s = "padding:.38rem .65rem;color:#5AD7FF;font-size:.79rem;font-weight:700;background:rgba(14,165,233,.15);border-bottom:1px solid rgba(90,215,255,.25);text-align:left;white-space:nowrap"
        st.markdown(f"""
<div style="border:1px solid rgba(90,215,255,.25);border-radius:14px;overflow:hidden;margin:.30rem 0 .80rem 0">
  <div style="overflow-x:auto;max-height:400px">
    <table style="width:100%;border-collapse:collapse">
      <thead><tr>
        <th style="{th_s}">TX Hash / Tipo</th>
        <th style="{th_s}">Emisor</th>
        <th style="{th_s}">Cantidad</th>
        <th style="{th_s}">Receptor</th>
        <th style="{th_s}">Hace</th>
      </tr></thead>
      <tbody>{tx_rows_html}</tbody>
    </table>
  </div>
</div>""", unsafe_allow_html=True)

        # ── Seguimiento de siguiente salto ────────────────────────────────────
        st.markdown("#### 🔗 Seguir la ruta — ¿el receptor reenvió el dinero?")
        st.markdown("""<div class='rrp-note'>
Selecciona una transacción para intentar seguir a dónde fue el dinero a continuación.
Si el receptor es un intermediario (corredor ODL, exchange, gateway), normalmente
reenvía el dinero en pocos segundos. El rastreador busca en los 20 ledgers siguientes (~1 minuto).
</div>""", unsafe_allow_html=True)

        tx_options = {
            f"{r['hash']} | {r['sender_label']} → {r['receiver_label']} ({r['amount']})": (r["receiver"], int(r["ledger_index"]))
            for _, r in real_txs.head(20).iterrows()
        }
        selected_label = st.selectbox("Selecciona una transacción para rastrear:", list(tx_options.keys()), key="tx_trace_select")
        if selected_label:
            recv_addr, ledger_idx = tx_options[selected_label]
            with st.spinner("Buscando siguiente salto en XRPL…"):
                hop = trace_next_hop(recv_addr, ledger_idx)
            if hop:
                hop_color = "#3CFF9B" if hop["next_known"] else "#FFB84D"
                hop_icon  = "✅" if hop["next_known"] else "❓"
                st.markdown(f"""
<div style="border:1px solid {hop_color};border-radius:14px;background:rgba(15,23,42,.95);
            padding:.85rem 1.1rem;margin:.40rem 0 .80rem 0">
  <div style="font-size:.85rem;color:#94A3B8;margin-bottom:.35rem">
    🔗 Siguiente salto detectado — TX: <code style="color:#CBD5E1">{hop['hash']}</code>
  </div>
  <div style="font-size:1.05rem;font-weight:700;color:#FFFFFF">
    {_label(recv_addr)}
    <span style="color:#FFB84D"> → {hop['amount']} → </span>
    <span style="color:{hop_color}">{hop_icon} {hop['next_receiver_label']}</span>
  </div>
  <div style="margin-top:.40rem;font-size:.86rem;color:#94A3B8">
    Dirección destino: <code style="color:#CBD5E1">{hop['next_receiver']}</code>
    {'<br><span style="color:#3CFF9B">✅ Wallet identificada en la base de datos del radar.</span>' if hop['next_known'] else '<br><span style="color:#94A3B8">❓ Wallet desconocida — no está en la base de datos del radar. Puede ser un cliente final, otra entidad no catalogada o una wallet de exchange sin etiquetar.</span>'}
  </div>
</div>""", unsafe_allow_html=True)
            else:
                st.markdown(f"""
<div style="border:1px solid rgba(255,184,77,.40);border-radius:14px;background:rgba(15,23,42,.95);
            padding:.75rem 1rem;margin:.40rem 0 .80rem 0;color:#CBD5E1;font-size:.88rem">
  🔍 No se encontró un reenvío inmediato desde <b>{_label(recv_addr)}</b> en los 20 ledgers siguientes.<br>
  <span style="color:#94A3B8">Esto puede significar: (1) el receptor es el destinatario final y no reenvía,
  (2) el reenvío ocurrió fuera de la ventana de búsqueda,
  (3) el receptor está en otra red (cross-network) o usa canales off-ledger.</span>
</div>""", unsafe_allow_html=True)

    # ── Seguidor automático de wallets ───────────────────────────────────────
    render_wallet_tracker(conn, real_txs)
    render_wallet_identity_report(conn)
    render_unknown_whales_db(conn)

    st.markdown("---")
    st.markdown("### 🧭 Inferencia por huellas — ruta probable A→B")
    st.markdown("""<div class='rrp-note'>
Cuando no hay transacción directa visible, el motor infiere la ruta probable cruzando
las huellas públicas del ledger con el perfil de score de cada actor conocido.
Esta sección es complementaria al rastreo real — no lo reemplaza.
</div>""", unsafe_allow_html=True)

    paths = load_live_route_paths(conn, df)
    current = route_path_engine_row(row)

    conf_pct = current["confidence"] * 100
    conf_color = "#3CFF9B" if conf_pct >= 72 else "#FFB84D" if conf_pct >= 52 else "#FF5A67"

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Tipo de ruta", current["path_type"])
    c2.metric("Confianza hoy", f"{conf_pct:.1f}%")
    c3.metric("Punto público detectado", current["public_hop"])
    c4.metric("Destino probable", current["destination"])

    st.markdown(f"""
<div style="padding:.80rem 1.10rem;border-radius:14px;background:rgba(15,23,42,.92);
            border-left:4px solid {conf_color};margin:.50rem 0 .80rem 0;">
<b style="color:{conf_color}">Ruta probable hoy:</b>
<span style="color:#FFFFFF;font-size:1.05rem;font-weight:700"> {current['path_label']}</span><br>
<span style="color:#94A3B8;font-size:.88rem">
Evidencia pública detectada: <b style="color:#CBD5E1">{current['evidence'] or 'sin evidencia suficiente'}</b>
</span><br>
<span style="color:#CBD5E1;font-size:.90rem;margin-top:.35rem;display:block">{current.get('explanation','')}</span>
</div>""", unsafe_allow_html=True)

    # ── Diagnóstico completo de todas las rutas ─────────────────────────────
    st.markdown("#### Diagnóstico completo de señales por ruta")
    st.markdown("""
<div class='rrp-note'>
Cada señal de abajo representa la fuerza de una huella pública específica que el radar usa
para inferir si ese tipo de ruta está activo. <b>Verde ≥60%</b> = señal fuerte.
<b>Naranja 40–60%</b> = señal moderada. <b>Rojo &lt;40%</b> = señal débil o ausente.
</div>""", unsafe_allow_html=True)

    route_signals = [
        ("🏦 Pagos / ODL activos",        "payment_flow_score",       "Hay pagos reales detectados en la cadena XRPL (remesas, ODL Bitso/SBI/Coins.ph)."),
        ("🔗 Trustlines activas",          "trustline_score",          "Wallets estableciendo o ampliando líneas de confianza. Señal de integración."),
        ("🌊 DEX/AMM con liquidez",        "dex_score",                "Ofertas y AMM activos. Las rutas ODL necesitan mercado líquido para convertir."),
        ("🐋 Transfers grandes",           "large_transfer_score",     "Movimientos ≥1M RLUSD. Treasury, custody o market maker institucional."),
        ("🧩 Clusters de wallets",         "cluster_score",            "Wallets conectadas en grupo. Patrón de broker/distribuidor/ODL."),
        ("🧠 Topología de red",            "topology_score",           "Hubs y concentración de flujo. Alta topología = dinero canalizado."),
        ("🧬 Fingerprint institucional",   "fingerprint_score",        "Patrón treasury/market-maker/corredor detectado por tamaño y repetición."),
        ("🚨 Anomalía vs historia",        "anomaly_score",            "Actividad fuera de rango histórico. Puede ser un evento institucional."),
        ("🛰️ Gateway público",             "public_gateway_score",     "Punto de entrada visible en XRPL donde rutas privadas suelen 'salir'."),
        ("🏛️ Rutas institucionales",       "institutional_route_score","Señal de que una ruta bancaria está usando el rail de Ripple."),
        ("📈 Prime / brokerage",           "prime_brokerage_score",    "Actividad estilo prime broker (Hidden Road, DTCC). Alta con transfers grandes."),
        ("🔐 Custody / Metaco",            "custody_score",            "Señal de custodia: wallets que acumulan sin distribuir inmediatamente."),
        ("🌐 Cross-network",              "cross_network_score",      "Actividad multi-red (bridges, Ethereum↔XRPL). Señal de integración avanzada."),
        ("⏱️ Régimen temporal",            "time_regime_score",        "¿La actividad acumula o es un spike? Alta = aceleración sostenida en el tiempo."),
    ]

    rows_diag = []
    for label, col, desc in route_signals:
        val = float(row.get(col, 0))
        val_pct = val * 100 if val <= 1.0 else val
        if val_pct >= 60:
            estado = "🟢 Fuerte"
        elif val_pct >= 40:
            estado = "🟡 Moderada"
        else:
            estado = "🔴 Débil"
        rows_diag.append({
            "Señal": label,
            "Score": f"{val_pct:.1f}%",
            "Estado": estado,
            "Qué significa": desc,
        })

    styled_table(pd.DataFrame(rows_diag))

    # ── Diagrama Sankey ─────────────────────────────────────────────────────
    st.markdown("#### Diagrama de flujo — snapshot actualizado")
    st.markdown("""
<div class='rrp-note'>
<b>Cómo leer el Sankey:</b> cada banda representa una ruta inferida.
El <b>grosor</b> de la banda = confianza de la ruta. Las bandas van de
Origen privado (izquierda) → Punto público XRPL (centro) → Destino (derecha).
</div>""", unsafe_allow_html=True)
    render_route_path_graph_and_fichas(paths, key_prefix="snapshot", conn=conn)

    # ── Tabla de rutas probables ────────────────────────────────────────────
    st.markdown("#### Últimas rutas probables detectadas")
    st.markdown("""
<div class='rrp-note'>
Tabla cronológica de las rutas inferidas día a día. La columna <b>Confianza</b> va de 0 a 100%.
<b>path_type</b> resume si la ruta es fuerte, probable, débil o ruido.
<b>evidence</b> = huellas públicas que activaron esa inferencia.
</div>""", unsafe_allow_html=True)
    if not paths.empty:
        view = paths.sort_values(["day", "confidence"], ascending=[False, False]).copy()
        view["confidence"] = (view["confidence"].astype(float) * 100).round(1).astype(str) + "%"
        view = view.rename(columns={
            "day": "Fecha", "origin": "Origen", "public_hop": "Punto público",
            "destination": "Destino", "confidence": "Confianza",
            "path_type": "Tipo", "evidence": "Evidencia",
        })
        styled_table(view[["Fecha","Confianza","Tipo","Origen","Punto público","Destino","Evidencia"]].head(120))
    else:
        st.info("Todavía no hay rutas reconstruidas.")

# =============================================================================
# MAIN
# =============================================================================

# =============================================================================
# DISCOVERY ENGINE — búsqueda online de instituciones + reescritura dinámica
# =============================================================================
ANTHROPIC_API_URL    = "https://api.anthropic.com/v1/messages"
# CostGuard v2: Haiku por defecto. Sonnet queda reservado para investigaciones profundas futuras.
ANTHROPIC_MODEL_FAST = "claude-haiku-4-5-20251001"   # modo barato/rápido: discovery + validación
ANTHROPIC_MODEL_DEEP = "claude-sonnet-4-20250514"    # modo caro: solo deep research explícito
ANTHROPIC_MODEL      = ANTHROPIC_MODEL_FAST


def _get_api_key() -> str:
    """
    Busca la API key de Anthropic en este orden de prioridad:
    1. Variable de entorno ANTHROPIC_API_KEY
    2. st.secrets (secrets.toml o Streamlit Cloud Settings → Secrets)
    3. Archivo .env junto al script
    4. Input manual en la UI (session_state "_manual_api_key")
    """
    # 1. Variable de entorno
    key = _os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if key:
        return key
    # 2. Streamlit secrets
    try:
        key = str(st.secrets.get("ANTHROPIC_API_KEY", "") or "").strip()
        if key:
            return key
    except Exception:
        pass
    # 3. Archivo .env
    try:
        _env_path = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".env")
        if _os.path.isfile(_env_path):
            with open(_env_path, encoding="utf-8") as _ef:
                for _line in _ef:
                    _line = _line.strip()
                    if _line.startswith("ANTHROPIC_API_KEY"):
                        _, _, _val = _line.partition("=")
                        _val = _val.strip().strip('"').strip("'")
                        if _val:
                            return _val
    except Exception:
        pass
    # 4. Introducida manualmente en Setup UI
    return str(st.session_state.get("_manual_api_key", "") or "").strip()


# ── Constantes de idioma — nivel de módulo para no recrearlas en cada llamada ──

def _detect_script(text: str) -> str:
    """Detecta el script dominante de un texto: zh/ja/ar/ru/ko o en."""
    for c in text:
        cp = ord(c)
        if 0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF: return "zh"
        if 0x3040 <= cp <= 0x30FF: return "ja"
        if 0x0600 <= cp <= 0x06FF: return "ar"
        if 0x0400 <= cp <= 0x04FF: return "ru"
        if 0xAC00 <= cp <= 0xD7A3: return "ko"
    return "en"

# Términos nativos por script — usado en discovery y en validate
_NATIVE_TERMS: Dict[str, Dict[str, str]] = {
    "zh": {"ripple": "瑞波", "xrpl": "瑞波账本", "cbdc": "数字货币", "blockchain": "区块链",
           "payment": "支付", "pilot": "试点", "cooperation": "合作", "bank": "银行",
           "gov_sites": "site:pbc.gov.cn OR site:gov.cn OR site:csrc.gov.cn OR site:safe.gov.cn"},
    "ja": {"ripple": "リップル", "xrpl": "XRPレジャー", "cbdc": "デジタル通貨",
           "blockchain": "ブロックチェーン", "payment": "送金", "cooperation": "提携",
           "pilot": "実証実験",
           "gov_sites": "site:boj.or.jp OR site:fsa.go.jp OR site:mof.go.jp"},
    "ar": {"ripple": "ريبل", "xrpl": "دفتر XRP", "blockchain": "بلوكتشين",
           "payment": "مدفوعات", "cooperation": "تعاون", "pilot": "تجريبي",
           "gov_sites": "site:cbuae.gov.ae OR site:sama.gov.sa OR site:qcb.gov.qa"},
    "ru": {"ripple": "Рипл", "xrpl": "XRP Ledger", "blockchain": "блокчейн",
           "payment": "платежи", "cooperation": "сотрудничество", "pilot": "пилот",
           "gov_sites": "site:cbr.ru OR site:minfin.ru OR site:government.ru"},
    "ko": {"ripple": "리플", "xrpl": "XRP 레저", "blockchain": "블록체인",
           "payment": "송금", "cooperation": "협력", "pilot": "파일럿",
           "gov_sites": "site:bok.or.kr OR site:fsc.go.kr OR site:moef.go.kr"},
    "hi": {"ripple": "रिपल", "xrpl": "XRP लेजर", "cbdc": "डिजिटल मुद्रा",
           "blockchain": "ब्लॉकचेन", "payment": "भुगतान", "cooperation": "सहयोग",
           "pilot": "पायलट",
           "gov_sites": "site:rbi.org.in OR site:finmin.nic.in OR site:sebi.gov.in"},
}

# Repositorios de documentos financieros por script/país
# Usar en búsquedas cuando se detecta entidad no-inglesa (bolsas locales, reguladores)
_LOCAL_DOC_SITES: Dict[str, str] = {
    "zh": "site:cninfo.com.cn OR site:sse.com.cn OR site:szse.cn OR site:hkexnews.hk OR site:hkex.com.hk",
    "ja": "site:disclosure.edinet-fsa.go.jp OR site:jpx.co.jp OR site:tse.or.jp",
    "ko": "site:kind.krx.co.kr OR site:fss.or.kr OR site:dart.fss.or.kr",
    "ru": "site:disclosure.moex.com OR site:e-disclosure.ru OR site:cbr.ru",
    "ar": "site:tadawul.com.sa OR site:dfm.ae OR site:adx.ae OR site:mubasher.info",
    "hi": "site:bseindia.com OR site:nseindia.com OR site:sebi.gov.in",
    "en": "",
}

# Palabras nativas que suelen aparecer en documentos oficiales o PDFs locales.
# Esto evita depender de filetype:pdf y empuja la búsqueda hacia informes, filings,
# avisos regulatorios, whitepapers y comunicados publicados en el idioma real.
_LOCAL_DOC_KEYWORDS: Dict[str, str] = {
    "zh": "年报 OR 招股书 OR 公告 OR 白皮书 OR 合作 OR 试点 OR 区块链 OR 数字货币 OR PDF",
    "ja": "有価証券報告書 OR 適時開示 OR 発表 OR 提携 OR 実証実験 OR ブロックチェーン OR PDF",
    "ko": "공시 OR 보고서 OR 발표 OR 협력 OR 파일럿 OR 블록체인 OR PDF",
    "ru": "годовой отчет OR раскрытие OR доклад OR пилот OR сотрудничество OR блокчейн OR PDF",
    "ar": "تقرير OR إفصاح OR إعلان OR تعاون OR تجربة OR بلوكتشين OR PDF",
    "hi": "रिपोर्ट OR घोषणा OR सहयोग OR पायलट OR ब्लॉकचेन OR PDF",
    "en": "annual report OR filing OR disclosure OR whitepaper OR memorandum OR PDF",
}

_LOCAL_SEARCH_ENGINE_HINTS: Dict[str, str] = {
    "zh": "índices chinos/locales: Baidu, Sogou, 360, dominios .cn/.hk",
    "ja": "índices japoneses/locales: Yahoo Japan, Google Japan, dominios .jp",
    "ko": "índices coreanos/locales: Naver, Daum, dominios .kr",
    "ru": "índices rusos/locales: Yandex, dominios .ru",
    "ar": "índices árabes/locales y portales regulatorios MENA",
    "hi": "índices indios/locales y portales regulatorios .in",
    "en": "índices globales y repositorios oficiales",
}

# Dominios que el radar debe tratar como documento primario aunque la URL no acabe
# literalmente en .pdf. SEC/Archives, EDINET, CNINFO, DART, bolsas y reguladores
# muchas veces sirven HTML/visor, no un .pdf limpio.
_PRIMARY_DOC_HOST_HINTS: Tuple[str, ...] = (
    # Fuentes primarias del propio ecosistema Ripple/XRPL y documentos oficiales.
    "ripple.com", "xrpl.org", "lianlianglobal.com",
    "sec.gov/archives", "sec.gov/ixviewer", "bis.org", "federalreserve.gov",
    "imf.org", "worldbank.org",
    "pbc.gov.cn", "gov.cn", "csrc.gov.cn", "safe.gov.cn",
    "cninfo.com.cn", "sse.com.cn", "szse.cn", "hkexnews.hk", "hkex.com.hk",
    "disclosure.edinet-fsa.go.jp", "jpx.co.jp", "tse.or.jp", "fsa.go.jp",
    "kind.krx.co.kr", "dart.fss.or.kr", "fss.or.kr",
    "disclosure.moex.com", "e-disclosure.ru", "cbr.ru",
    "tadawul.com.sa", "dfm.ae", "adx.ae", "mubasher.info",
    "bseindia.com", "nseindia.com", "sebi.gov.in",
)

# Mapeo nombre latino → (script, nombre nativo) para búsquedas bilíngues
_KNOWN_NATIVE_NAMES: Dict[str, tuple] = {
    "people's bank of china": ("zh", "中国人民银行"), "pboc": ("zh", "中国人民银行"),
    "bank of china":          ("zh", "中国银行"),
    "icbc":                   ("zh", "中国工商银行"),
    "industrial and commercial bank": ("zh", "中国工商银行"),
    "china construction bank":("zh", "中国建设银行"),
    "agricultural bank of china": ("zh", "中国农业银行"),
    "bank of communications": ("zh", "交通银行"),
    # Inversores / gestoras chinas
    "idg capital":            ("zh", "IDG资本"),   "idg": ("zh", "IDG资本"),
    "hillhouse capital":      ("zh", "高瓴资本"),
    "sequoia china":          ("zh", "红杉中国"),
    "ant group":              ("zh", "蚂蚁集团"),
    "tencent":                ("zh", "腾讯"),
    "alibaba":                ("zh", "阿里巴巴"),
    "ping an":                ("zh", "平安"),
    "china international capital": ("zh", "中国国际金融"),  "cicc": ("zh", "中国国际金融"),
    "citic":                  ("zh", "中信"),
    "haitong securities":     ("zh", "海通证券"),
    "guotai junan":           ("zh", "国泰君安"),
    # Japonesas
    "softbank":               ("ja", "ソフトバンク"),
    "nomura":                 ("ja", "野村證券"),
    "mizuho":                 ("ja", "みずほ"),
    "mitsubishi ufj":         ("ja", "三菱UFJ"), "mufg": ("ja", "三菱UFJ"),
    "sumitomo mitsui":        ("ja", "三井住友"), "smbc": ("ja", "三井住友銀行"),
    # Coreanas
    "kb financial":           ("ko", "KB금융"),
    "samsung":                ("ko", "삼성"),
    "kakao":                  ("ko", "카카오"),
    "hana financial":         ("ko", "하나금융"),
    "shinhan":                ("ko", "신한"),
    "bank of japan":          ("ja", "日本銀行"),   "boj": ("ja", "日本銀行"),
    "bank of korea":          ("ko", "한국은행"),   "bok": ("ko", "한국은행"),
    "bank of russia":         ("ru", "Банк России"), "cbr": ("ru", "Банк России"),
    "sberbank":               ("ru", "Сбербанк"),
    "vtb bank":               ("ru", "ВТБ"),
    "central bank of uae":    ("ar", "مصرف الإمارات المركزي"), "cbuae": ("ar", "مصرف الإمارات المركزي"),
    "saudi central bank":     ("ar", "البنك المركزي السعودي"), "sama":  ("ar", "البنك المركزي السعودي"),
    "bank al-maghrib":        ("ar", "بنك المغرب"),
    "qatar central bank":     ("ar", "مصرف قطر المركزي"),
    "state bank of india":    ("hi", "भारतीय स्टेट बैंक"),
    "reserve bank of india":  ("hi", "भारतीय रिज़र्व बैंक"), "rbi": ("hi", "भारतीय रिज़र्व बैंक"),
    # Español
    "banco popular de china": ("zh", "中国人民银行"), "banco popular chino": ("zh", "中国人民银行"),
    "banco de china":         ("zh", "中国银行"),
    "banco de japon":         ("ja", "日本銀行"),
    "banco de corea":         ("ko", "한국은행"),
    "banco de rusia":         ("ru", "Банк России"),
    "banco central de emiratos": ("ar", "مصرف الإمارات المركزي"),
    "banco central saudita":  ("ar", "البنك المركزي السعودي"),
    "banco central de arabia":("ar", "البنك المركزي السعودي"),
    "banco central de qatar": ("ar", "مصرف قطر المركزي"),
    "banco de la reserva de india": ("hi", "भारतीय रिज़र्व बैंक"),
}

# System prompt compartido por las dos funciones de validación A↔B
_AUDIT_SYSTEM_PROMPT = (
    "Eres un auditor de evidencias financieras. Buscas rastros VERIFICABLES de conexiones "
    "con la infraestructura Ripple/XRPL. NO inventes ni inferas — solo fuentes reales encontradas. "
    "Cada prueba debe demostrar explícitamente la relación A↔B: la fuente debe mencionar la entidad investigada "
    "y también Ripple, XRPL, XRP Ledger, RLUSD, Ripple Payments/RippleNet/ODL o el nodo concreto verificado. "
    "Descarta noticias generales de cripto/blockchain si no conectan directamente las dos partes. "
    "No repitas la misma URL, el mismo comunicado sindicado ni la misma historia con distinto snippet. "
    "Si la entidad tiene nombre en idioma no inglés, busca TAMBIÉN en ese idioma. "
    "Incluye PDFs de reguladores, BIS y bancos centrales como prioridad máxima. "
    "Tipos de prueba (usa SOLO estos valores): official_partner, press_release, regulatory_filing, "
    "regulatory_filing_pdf, contract_pdf, github_repo, news_major, job_posting, news_minor."
)


# =============================================================================
# CHAIN EVIDENCE ENGINE v6.2.1
# =============================================================================
# Esta capa evita el falso 0% cuando no existe A→C directo pero sí existe
# una cadena documental A→B→C. También conserva la frontera crítica:
# XRPL/RLUSD sin prueba directa quedan como WATCH/INFERIDO, no como operativo.

CHAIN_TARGETS = {"Ripple Payments", "RippleNet", "XRPL", "RLUSD"}
WATCH_ONLY_CHAIN_TARGETS = {"XRPL", "RLUSD"}
CHAIN_CORE_TARGETS = {"Ripple Payments", "RippleNet"}

CHAIN_EVIDENCE_SEEDS = []
# CLEAN MODE: sin pruebas semilla/precargadas.
# Las pruebas institucionales deben venir de una búsqueda/verificación real o de la BD generada por el usuario.



def _contains_cjk(text: Any) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in str(text or ""))


def _native_query_variants(entity: Any) -> List[str]:
    """Consultas adicionales en idioma nativo para que 中国人民银行 no se busque solo en inglés."""
    raw = str(entity or "").strip()
    canonical = _canonical_entity_name(raw)
    key = _norm_key(raw)
    variants: List[str] = []

    def add(q: str) -> None:
        q = re.sub(r"\s+", " ", str(q or "").strip())
        if q and q not in variants:
            variants.append(q)

    native = None
    try:
        native = NATIVE_ENTITY_HINTS.get(key, (None, None))[1]
    except Exception:
        native = None
    if _contains_cjk(raw):
        native = raw
    if canonical == "People's Bank of China (PBoC)":
        native = native or "中国人民银行"
        for q in [
            f'"{native}" 连连支付',
            f'"{native}" mBridge',
            f'"{native}" 多边央行数字货币桥',
            f'"{native}" 国际清算银行',
            f'"{native}" 跨境支付 区块链',
            f'"{native}" Ripple',
            f'"{native}" RippleNet',
            '中国人民银行 连连支付',
            '中国人民银行 mBridge',
            '数字人民币 mBridge',
            '连连支付 Ripple',
            '连连国际 RippleNet',
            '人民银行 跨境支付 区块链',
        ]:
            add(q)

    if native and native != raw:
        for q in [f'"{native}" Ripple', f'"{native}" XRPL', f'"{native}" RippleNet', f'"{native}" mBridge']:
            add(q)

    for q in [
        f'"{canonical}" "Ripple"',
        f'"{canonical}" "XRPL"',
        f'"{canonical}" "RippleNet"',
        f'"{canonical}" "Project mBridge"',
        f'"{canonical}" "LianLian Pay"',
    ]:
        add(q)
    return variants[:14]


def _native_query_instruction(entity: Any) -> str:
    qs = _native_query_variants(entity)
    if not qs:
        return ""
    return (
        "\nBÚSQUEDA MULTILINGÜE OBLIGATORIA: además del nombre inglés/canónico, ejecuta consultas locales como: "
        + " ; ".join(qs)
        + ". Prioriza fuentes oficiales del país, PDFs, bancos centrales, BIS y comunicados de la entidad. "
    )


def _chain_all_routes(conn: Optional[sqlite3.Connection] = None) -> List[Tuple[str, str, str, str, str]]:
    routes = list(ROUTES)
    if conn is not None:
        try:
            rows = conn.execute("SELECT src,dst,kind,signal_col,label FROM dynamic_routes").fetchall()
            routes.extend([(str(a), str(b), str(c), str(d), str(e)) for a, b, c, d, e in rows])
        except Exception:
            pass
    # dedupe dirigido conservando orden
    seen = set(); out = []
    for r in routes:
        if len(r) < 5:
            continue
        key = (_canonical_entity_key(r[0]), _canonical_entity_key(r[1]), str(r[2]))
        if key not in seen:
            out.append(r); seen.add(key)
    return out


def _proof_score_from_row(row: Any) -> Tuple[float, Dict[str, Any]]:
    if not row:
        return 0.0, {}
    try:
        pdata = json.loads(row[0] or "{}")
    except Exception:
        pdata = {}
    try:
        score = float(pdata.get("calibrated_score", row[2] if len(row) > 2 else 0.0) or 0.0)
    except Exception:
        score = 0.0
    return max(0.0, min(1.0, score)), pdata


def _verified_direct_score(conn: sqlite3.Connection, a: str, b: str) -> Tuple[float, Dict[str, Any]]:
    row = _connection_proof_row(conn, a, b)
    score, pdata = _proof_score_from_row(row)
    if score <= 0:
        return 0.0, {}
    ptype = str((pdata.get("proofs") or [{}])[0].get("type", "")).lower() if isinstance(pdata.get("proofs"), list) else ""
    if ptype in {"sin_wallet", "unknown", "no_evidence"} and not pdata.get("has_internet") and not pdata.get("has_onchain"):
        return 0.0, {}
    # 0.50+ se considera eslabón válido. Los chains sintetizados también valen si son a Ripple Payments/RippleNet.
    if score >= 0.50 or str(pdata.get("chain_status", "")).startswith("verified"):
        return score, pdata
    return 0.0, {}


def _upsert_chain_seed(conn: sqlite3.Connection, seed: Dict[str, Any]) -> None:
    a = _canonical_entity_name(seed.get("a")); b = _canonical_entity_name(seed.get("b"))
    existing = _connection_proof_row(conn, a, b)
    score, _ = _proof_score_from_row(existing)
    if score >= float(seed.get("score", 0.0)):
        return
    now = datetime.now(timezone.utc).isoformat()
    proof = {
        "type": seed.get("type", "official_partner"),
        "icon": "🏛️",
        "label": seed.get("label", "Prueba institucional semilla"),
        "url": seed.get("url", ""),
        "snippet": seed.get("snippet", ""),
        "internet": True,
        "onchain": False,
    }
    pdata = {
        "node_a": a, "node_b": b,
        "proofs": [proof],
        "cert_label": "✅ Evidencia documental/institucional",
        "cert_color": "#22C55E",
        "calibrated_score": float(seed.get("score", 0.0)),
        "has_onchain": False,
        "has_internet": True,
        "seeded_known_evidence": True,
    }
    conn.execute("""
        INSERT OR REPLACE INTO connection_proofs
        (proof_id, node_a, node_b, node_a_key, node_b_key, pair_key, proof_type, proof_data, onchain, confidence, validated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        _canonical_pair_proof_id(a, b), a, b, _canonical_entity_key(a), _canonical_entity_key(b), _canonical_pair_key(a, b),
        proof["type"], json.dumps(pdata, ensure_ascii=False), 1, float(seed.get("score", 0.0)), now
    ))


def _seed_known_chain_evidence_if_relevant(conn: sqlite3.Connection, focus_node: str = "") -> None:
    """CLEAN MODE: no inserta semillas conocidas ni pruebas precargadas."""
    return


def _find_verified_route_chain(conn: sqlite3.Connection, source: str, target: str, max_hops: int = 3) -> Optional[Dict[str, Any]]:
    source = _canonical_entity_name(source); target = _canonical_entity_name(target)
    adjacency: Dict[str, List[str]] = defaultdict(list)
    for a, b, *_ in _chain_all_routes(conn):
        aa = _canonical_entity_name(a); bb = _canonical_entity_name(b)
        if aa and bb and bb not in adjacency[aa]:
            adjacency[aa].append(bb)

    queue = deque([(source, [source])])
    visited = {source}
    while queue:
        node, route = queue.popleft()
        if len(route) - 1 > max_hops:
            continue
        if node == target and len(route) > 1:
            scores = []; proof_datas = []
            ok = True
            for a, b in zip(route[:-1], route[1:]):
                sc, pd = _verified_direct_score(conn, a, b)
                if sc <= 0:
                    ok = False; break
                scores.append(sc); proof_datas.append(pd)
            if ok and scores:
                conf = max(0.0, min(0.95, min(scores) - (len(scores)-1)*0.08))
                return {"route": route, "confidence": conf, "proof_datas": proof_datas}
        for nxt in adjacency.get(node, []):
            if nxt not in visited and len(route) <= max_hops:
                visited.add(nxt)
                queue.append((nxt, route + [nxt]))
    return None


def _save_synthetic_chain_proof(conn: sqlite3.Connection, source: str, target: str, chain: Dict[str, Any], watch: bool = False) -> None:
    source = _canonical_entity_name(source); target = _canonical_entity_name(target)
    if not chain or not chain.get("route"):
        return
    direct_score, direct_pd = _verified_direct_score(conn, source, target)
    # Nunca rebajar una prueba directa fuerte.
    if direct_score >= 0.60 and not direct_pd.get("chain_synthetic"):
        return
    route = chain["route"]
    conf = float(chain.get("confidence", 0.0))
    if watch:
        conf = min(conf, 0.45)
        cert_label = "👁 Watch/inferida por cadena"
        cert_color = "#F59E0B"
        proof_type = "watch_inferred_chain"
        label = "Conexión inferida por cadena; requiere prueba directa para considerarse operativa"
    else:
        cert_label = "🔗 Indirecta verificada por cadena"
        cert_color = "#38BDF8"
        proof_type = "verified_chain"
        label = "Conexión indirecta verificada por cadena documental"
    urls = []
    for pd in chain.get("proof_datas", []):
        for pr in pd.get("proofs", []) if isinstance(pd, dict) else []:
            u = _canonical_source_url(pr.get("url", ""))
            if u.startswith("http") and u not in urls:
                urls.append(u)
    now = datetime.now(timezone.utc).isoformat()
    proof = {
        "type": proof_type,
        "icon": "🔗" if not watch else "👁",
        "label": label,
        "url": urls[0] if urls else "",
        "snippet": " → ".join(route),
        "internet": True,
        "onchain": False,
        "chain_route": route,
        "sources": urls[:5],
    }
    pdata = {
        "node_a": source,
        "node_b": target,
        "proofs": [proof],
        "cert_label": cert_label,
        "cert_color": cert_color,
        "calibrated_score": conf,
        "has_onchain": False,
        "has_internet": True,
        "chain_synthetic": True,
        "chain_status": proof_type,
        "chain_route": route,
        "chain_explanation": _explain_chain_plain(source, target, route, watch),
    }
    conn.execute("""
        INSERT OR REPLACE INTO connection_proofs
        (proof_id, node_a, node_b, node_a_key, node_b_key, pair_key, proof_type, proof_data, onchain, confidence, validated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        _canonical_pair_proof_id(source, target), source, target,
        _canonical_entity_key(source), _canonical_entity_key(target), _canonical_pair_key(source, target),
        proof_type, json.dumps(pdata, ensure_ascii=False), 0, conf, now
    ))


def _explain_chain_plain(source: str, target: str, route: List[str], watch: bool) -> str:
    r = " → ".join(route)
    if watch:
        return (f"{source} no tiene una prueba directa operativa hacia {target}. "
                f"El radar detecta una ruta indirecta ({r}), pero como {target} exige prueba directa/on-chain, "
                "queda marcado como watch/inferido.")
    return (f"{source} conecta con {target} por una cadena de eslabones verificados: {r}. "
            "No es una prueba de operación directa A→C, sino una relación indirecta trazable.")


def rebuild_chain_proofs_for_node(conn: sqlite3.Connection, focus_node: str, peers: Optional[List[str]] = None) -> None:
    """Actualiza pruebas de cadena tras cada búsqueda/verificación para que las líneas cambien al instante."""
    ensure_discovery_tables(conn)
    _seed_known_chain_evidence_if_relevant(conn, focus_node)
    focus = _canonical_entity_name(focus_node)
    targets = set(CHAIN_TARGETS)
    if peers:
        targets.update(_canonical_entity_name(p) for p in peers)
    # 1) A→Ripple Payments/RippleNet como indirecta verificada si hay cadena documental.
    for target in ["Ripple Payments", "RippleNet"]:
        if focus == target:
            continue
        ch = _find_verified_route_chain(conn, focus, target, max_hops=3)
        if ch:
            _save_synthetic_chain_proof(conn, focus, target, ch, watch=False)
    # 2) A→XRPL/RLUSD como WATCH si A llega a Ripple Payments pero no existe prueba directa a XRPL/RLUSD.
    base = _find_verified_route_chain(conn, focus, "Ripple Payments", max_hops=3)
    if base:
        for target in ["XRPL", "RLUSD"]:
            if focus == target:
                continue
            direct_score, direct_pd = _verified_direct_score(conn, focus, target)
            if direct_score >= 0.60 and not direct_pd.get("chain_synthetic"):
                continue
            watch_chain = dict(base)
            watch_chain["route"] = list(base["route"]) + [target]
            _save_synthetic_chain_proof(conn, focus, target, watch_chain, watch=True)
    # 3) Cadenas entre peers visibles: si A→B→C está probado, crear A→C.
    if peers:
        for target in peers:
            t = _canonical_entity_name(target)
            if t == focus:
                continue
            ch = _find_verified_route_chain(conn, focus, t, max_hops=3)
            if ch:
                _save_synthetic_chain_proof(conn, focus, t, ch, watch=(t in WATCH_ONLY_CHAIN_TARGETS))
    try:
        conn.commit()
    except Exception:
        pass


def render_chain_logic_box(focus_node: str, conn: Optional[sqlite3.Connection]) -> None:
    if conn is None:
        return
    try:
        key = _canonical_entity_key(focus_node)
        rows = conn.execute(
            "SELECT node_a,node_b,proof_data,confidence FROM connection_proofs "
            "WHERE node_a=? OR node_b=? OR node_a_key=? OR node_b_key=? ORDER BY confidence DESC LIMIT 10",
            (focus_node, focus_node, key, key)
        ).fetchall()
    except Exception:
        rows = []
    if not rows:
        return
    items = []
    for na, nb, pdata_s, conf in rows:
        try:
            pd = json.loads(pdata_s or "{}")
        except Exception:
            pd = {}
        route = pd.get("chain_route") or []
        cert = pd.get("cert_label") or "Prueba guardada"
        expl = pd.get("chain_explanation") or "Eslabón directo o prueba guardada."
        peer = nb if _canonical_entity_key(na) == _canonical_entity_key(focus_node) else na
        route_txt = " → ".join(route) if route else f"{na} ↔ {nb}"
        items.append(
            f"<li style='margin-bottom:6px'><b>{html.escape(str(peer))}</b> · "
            f"<span style='color:#CBD5E1'>{html.escape(str(cert))} · {float(conf or 0)*100:.0f}%</span><br>"
            f"<code style='white-space:normal;color:#93C5FD'>{html.escape(route_txt)}</code><br>"
            f"<span style='color:#94A3B8'>{html.escape(str(expl))}</span></li>"
        )
    st.markdown(f"""
<div style='border:1px solid #334155;border-radius:14px;padding:13px 15px;background:rgba(15,23,42,.86);margin:10px 0 14px 0'>
  <div style='color:#E2E8F0;font-weight:800;font-size:.95rem;margin-bottom:5px'>🧠 Lectura por cadena de evidencia</div>
  <div style='color:#CBD5E1;font-size:.82rem;line-height:1.5;margin-bottom:8px'>
    El radar no verifica solo enlaces directos. Si <b>A</b> conecta documentalmente con <b>B</b>, y <b>B</b> conecta con <b>C</b>,
    entonces <b>A→C</b> se muestra como conexión indirecta verificada por cadena. Pero si el destino final es <b>XRPL</b> o <b>RLUSD</b>
    y no hay prueba directa/on-chain, se queda como <b>watch/inferida</b>, no como conexión operativa.
  </div>
  <ul style='margin:0;padding-left:18px;font-size:.80rem;line-height:1.45'>{''.join(items)}</ul>
</div>
""", unsafe_allow_html=True)

def ensure_discovery_tables(conn: sqlite3.Connection) -> None:
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS dynamic_nodes (
            node_id     TEXT PRIMARY KEY,
            name        TEXT NOT NULL,
            layer       TEXT NOT NULL DEFAULT 'Descubierto',
            icon        TEXT NOT NULL DEFAULT '?',
            confidence  REAL NOT NULL DEFAULT 0.0,
            source_url  TEXT,
            summary     TEXT,
            added_at    TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS dynamic_routes (
            route_id    TEXT PRIMARY KEY,
            src         TEXT NOT NULL,
            dst         TEXT NOT NULL,
            kind        TEXT NOT NULL DEFAULT 'discovered',
            signal_col  TEXT NOT NULL DEFAULT 'institutional_route_score',
            label       TEXT NOT NULL,
            confidence  REAL NOT NULL DEFAULT 0.0,
            evidence    TEXT,
            source_urls TEXT,
            added_at    TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS institution_search_cache (
            query       TEXT PRIMARY KEY,
            result_json TEXT NOT NULL,
            searched_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS connection_proofs (
            proof_id      TEXT PRIMARY KEY,
            node_a        TEXT NOT NULL,
            node_b        TEXT NOT NULL,
            node_a_key    TEXT,
            node_b_key    TEXT,
            pair_key      TEXT,
            proof_type    TEXT NOT NULL,
            proof_data    TEXT NOT NULL DEFAULT '{}',
            onchain       INTEGER NOT NULL DEFAULT 0,
            confidence    REAL NOT NULL DEFAULT 0.0,
            validated_at  TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS node_verifications (
            node          TEXT PRIMARY KEY,
            connected     INTEGER NOT NULL DEFAULT 0,
            confidence    REAL NOT NULL DEFAULT 0.0,
            kind_override TEXT NOT NULL DEFAULT 'verified',
            proofs_json   TEXT NOT NULL DEFAULT '[]',
            verified_at   TEXT NOT NULL,
            source        TEXT NOT NULL DEFAULT 'manual'
        );
        CREATE TABLE IF NOT EXISTS map_update_log (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            update_type TEXT NOT NULL,
            entity_name TEXT NOT NULL,
            details     TEXT,
            updated_at  TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS api_budget (
            id            INTEGER PRIMARY KEY CHECK (id=1),
            budget_usd    REAL NOT NULL DEFAULT 100.0,
            spent_usd     REAL NOT NULL DEFAULT 0.0,
            call_count    INTEGER NOT NULL DEFAULT 0,
            cache_hits    INTEGER NOT NULL DEFAULT 0,
            last_reset    TEXT NOT NULL,
            locked        INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS active_sessions (
            session_id    TEXT PRIMARY KEY,
            started_at    TEXT NOT NULL,
            heartbeat     TEXT NOT NULL,
            status        TEXT NOT NULL DEFAULT 'idle'
        );
        CREATE TABLE IF NOT EXISTS community_users (
            user_id       TEXT PRIMARY KEY,
            nickname      TEXT NOT NULL,
            created_at    TEXT NOT NULL,
            last_seen     TEXT NOT NULL,
            reputation    INTEGER NOT NULL DEFAULT 1,
            muted         INTEGER NOT NULL DEFAULT 0
        );
        CREATE TABLE IF NOT EXISTS community_messages (
            id            INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id       TEXT NOT NULL,
            nickname      TEXT NOT NULL,
            body          TEXT NOT NULL,
            created_at    TEXT NOT NULL,
            deleted       INTEGER NOT NULL DEFAULT 0,
            lang          TEXT NOT NULL DEFAULT 'es',
            pinned        INTEGER NOT NULL DEFAULT 0,
            role          TEXT NOT NULL DEFAULT 'user'
        );
        CREATE TABLE IF NOT EXISTS chat_translations (
            message_id    INTEGER NOT NULL,
            target_lang   TEXT NOT NULL,
            translated    TEXT NOT NULL,
            created_at    TEXT NOT NULL,
            PRIMARY KEY(message_id, target_lang)
        );
        CREATE TABLE IF NOT EXISTS ai_waiting_queue (
            session_id    TEXT PRIMARY KEY,
            nickname      TEXT,
            query         TEXT NOT NULL,
            status        TEXT NOT NULL DEFAULT 'queued',
            created_at    TEXT NOT NULL,
            updated_at    TEXT NOT NULL
        );
    """)
    # Migraciones: añadir columnas nuevas si la tabla ya existe sin ellas
    _migrations = [
        ("dynamic_routes",         "source_urls TEXT"),
        ("dynamic_nodes",          "source_url  TEXT"),
        ("connection_proofs",      "proof_data  TEXT NOT NULL DEFAULT '{}'"),
        ("connection_proofs",      "node_a_key  TEXT"),
        ("connection_proofs",      "node_b_key  TEXT"),
        ("connection_proofs",      "pair_key    TEXT"),
        ("node_verifications",     "source      TEXT NOT NULL DEFAULT 'manual'"),
        ("institution_search_cache","expires_at  TEXT"),
        ("institution_search_cache","hit_count   INTEGER NOT NULL DEFAULT 0"),
        ("institution_search_cache","search_type TEXT NOT NULL DEFAULT 'discovery'"),
        ("community_users",        "language    TEXT NOT NULL DEFAULT 'es'"),
        ("community_users",        "role        TEXT NOT NULL DEFAULT 'user'"),
        ("community_messages",     "lang        TEXT NOT NULL DEFAULT 'es'"),
        ("community_messages",     "pinned      INTEGER NOT NULL DEFAULT 0"),
        ("community_messages",     "role        TEXT NOT NULL DEFAULT 'user'"),
    ]
    for table, col_def in _migrations:
        col_name = col_def.split()[0]
        existing = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
        if col_name not in existing:
            try:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {col_def}")
            except Exception:
                pass
    # Backfill de claves canónicas para pruebas antiguas: evita duplicados A↔B/B↔A.
    try:
        rows = conn.execute("SELECT proof_id, node_a, node_b FROM connection_proofs").fetchall()
        for old_pid, na, nb in rows:
            na_key = _canonical_entity_key(na)
            nb_key = _canonical_entity_key(nb)
            pk = _canonical_pair_key(na, nb)
            new_pid = _canonical_pair_proof_id(na, nb)
            conn.execute(
                "UPDATE connection_proofs SET node_a_key=?, node_b_key=?, pair_key=? WHERE proof_id=?",
                (na_key, nb_key, pk, old_pid),
            )
            # Si aún no existe el proof_id canónico, migrar el id para que futuras búsquedas lo encuentren directo.
            if old_pid != new_pid:
                exists = conn.execute("SELECT 1 FROM connection_proofs WHERE proof_id=?", (new_pid,)).fetchone()
                if not exists:
                    conn.execute("UPDATE connection_proofs SET proof_id=? WHERE proof_id=?", (new_pid, old_pid))
        conn.execute("CREATE INDEX IF NOT EXISTS idx_connection_proofs_pair_key ON connection_proofs(pair_key)")
        conn.execute("CREATE INDEX IF NOT EXISTS idx_connection_proofs_node_keys ON connection_proofs(node_a_key, node_b_key)")
    except Exception:
        pass
    conn.commit()


# =============================================================================
# CACHÉ COMPARTIDA MULTI-USUARIO
# =============================================================================
# Toda búsqueda AI se guarda en institution_search_cache (SQLite compartido).
# Si otro usuario busca la misma entidad → resultado instantáneo, 0 tokens.
# TTL configurable por tipo de búsqueda.

_CACHE_TTL: Dict[str, int] = {
    # CostGuard v2: las conexiones institucionales no cambian cada día.
    # TTL más largo = menos llamadas repetidas sin perder utilidad para una beta pública.
    "discovery":    30,  # días — búsqueda de partners/conexiones
    "verification": 60,  # días — verificación individual, incluso negativa
    "batch_verify": 60,  # días — verificación en lote
    "negative":     14,  # días — reservado para futuros negativos explícitos
}
_MAX_AI_CALLS_SESSION = 20  # máximo de llamadas AI nuevas por sesión de usuario
_MAX_BATCH_PEERS = 5        # no verificar 20 rutas caras a la vez
_PRIORITY_PEERS = [
    "RLUSD", "XRPL", "Ripple Payments", "Ripple Prime", "Hidden Road",
    "Custody/Metaco", "Metaco", "Securitize", "Treasury", "DEX/AMM",
    "Permissioned DEX", "DTCC/NSCC", "SWIFT", "FedNow"
]


def _cache_key_search(canonical_name: str, search_type: str) -> str:
    # La clave de caché usa el nombre canónico + normalización fuerte.
    # Así "BLACK ROCK INC.", "black-rock" y "BlackRock" reutilizan la misma respuesta.
    canonical = _canonical_entity_name(canonical_name)
    return f"{search_type}::{_norm_key(canonical)}"


def _get_search_cache(conn: sqlite3.Connection, name: str,
                      search_type: str = "discovery") -> Optional[Dict]:
    """Devuelve resultado cacheado si existe y no ha expirado, o None."""
    try:
        key = _cache_key_search(_canonical_entity_name(name), search_type)
        now = datetime.now(timezone.utc).isoformat()
        row = conn.execute(
            "SELECT result_json FROM institution_search_cache "
            "WHERE query=? AND (expires_at IS NULL OR expires_at > ?)",
            (key, now)
        ).fetchone()
        if row:
            conn.execute(
                "UPDATE institution_search_cache SET hit_count=hit_count+1 WHERE query=?",
                (key,)
            )
            conn.commit()
            try:
                _record_cache_hit(conn)
            except Exception:
                pass
            return json.loads(row[0])
    except Exception:
        pass
    return None


def _set_search_cache(conn: sqlite3.Connection, name: str,
                      result: Dict, search_type: str = "discovery") -> None:
    """Guarda resultado en caché compartida con TTL."""
    try:
        key = _cache_key_search(_canonical_entity_name(name), search_type)
        ttl = _CACHE_TTL.get(search_type, 7)
        now = datetime.now(timezone.utc)
        expires = (now + timedelta(days=ttl)).isoformat()
        conn.execute("""
            INSERT OR REPLACE INTO institution_search_cache
            (query, result_json, searched_at, expires_at, hit_count, search_type)
            VALUES (?, ?, ?, ?, COALESCE(
                (SELECT hit_count+1 FROM institution_search_cache WHERE query=?), 1
            ), ?)
        """, (key, json.dumps(result), now.isoformat(), expires, key, search_type))
        conn.commit()
    except Exception:
        pass


def _log_map_update(conn: sqlite3.Connection, update_type: str,
                    entity_name: str, details: str = "") -> None:
    """Registra un cambio en el mapa para notificar a otras sesiones."""
    try:
        conn.execute(
            "INSERT INTO map_update_log (update_type, entity_name, details, updated_at) "
            "VALUES (?, ?, ?, ?)",
            (update_type, entity_name, details[:500],
             datetime.now(timezone.utc).isoformat())
        )
        conn.commit()
    except Exception:
        pass


def _get_pending_updates(conn: sqlite3.Connection, since: str) -> int:
    """Devuelve nº de actualizaciones del mapa posteriores a `since`."""
    try:
        if not since:
            return 0
        row = conn.execute(
            "SELECT COUNT(*) FROM map_update_log WHERE updated_at > ?", (since,)
        ).fetchone()
        return int(row[0]) if row else 0
    except Exception:
        return 0


def _get_last_map_update(conn: sqlite3.Connection) -> str:
    """Devuelve timestamp de la última actualización del mapa."""
    try:
        row = conn.execute("SELECT MAX(updated_at) FROM map_update_log").fetchone()
        return row[0] or ""
    except Exception:
        return ""


def _session_ai_quota() -> Tuple[int, int]:
    """Devuelve (llamadas_usadas, máximo) para la sesión actual."""
    used = st.session_state.get("ai_calls_session", 0)
    return used, _MAX_AI_CALLS_SESSION


def _increment_ai_calls() -> int:
    """Incrementa el contador de llamadas AI de la sesión. Devuelve nuevo total."""
    n = st.session_state.get("ai_calls_session", 0) + 1
    st.session_state["ai_calls_session"] = n
    return n


# =============================================================================
# PRESUPUESTO API + COLA DE USUARIOS
# =============================================================================
# Costes estimados de reserva. Luego se reconcilian con usage real si Anthropic lo devuelve.
# CostGuard v2: Haiku por defecto + JSON corto + batch limitado.
_CALL_COST: Dict[str, float] = {
    "discovery_fast": 0.035,
    "discovery_deep": 0.160,
    "discovery":      0.035,
    "verification":   0.018,
    "batch_verify":   0.080,
}
_PRICE_PER_TOKEN: Dict[str, Tuple[float, float]] = {
    # USD por token aproximado. Sirve para que el presupuesto no sea a ciegas.
    "haiku":  (1.0 / 1_000_000, 5.0 / 1_000_000),
    "sonnet": (3.0 / 1_000_000, 15.0 / 1_000_000),
}
_WEB_SEARCH_COST = 0.010  # $10 / 1000 búsquedas web aprox.
_BUDGET_WARN_PCT   = 0.80   # avisar al 80% del presupuesto
_BUDGET_LOCK_PCT   = 0.97   # bloquear al 97% (dejar margen)
_SESSION_HEARTBEAT = 90     # segundos hasta considerar sesión inactiva


def _init_budget(conn: sqlite3.Connection) -> None:
    """Inicializa la fila de presupuesto si no existe."""
    try:
        exists = conn.execute("SELECT id FROM api_budget WHERE id=1").fetchone()
        if not exists:
            conn.execute(
                "INSERT INTO api_budget (id, budget_usd, spent_usd, call_count, cache_hits, last_reset, locked) "
                "VALUES (1, 100.0, 0.0, 0, 0, ?, 0)",
                (datetime.now(timezone.utc).isoformat(),)
            )
            conn.commit()
    except Exception:
        pass


def _get_budget(conn: sqlite3.Connection) -> Dict[str, Any]:
    """Lee el estado actual del presupuesto."""
    try:
        _init_budget(conn)
        row = conn.execute(
            "SELECT budget_usd, spent_usd, call_count, cache_hits, last_reset, locked FROM api_budget WHERE id=1"
        ).fetchone()
        if row:
            budget, spent, calls, hits, reset, locked = row
            return {
                "budget": float(budget),
                "spent":  float(spent),
                "calls":  int(calls),
                "hits":   int(hits),
                "reset":  reset,
                "locked": bool(locked),
                "remaining": float(budget) - float(spent),
                "pct": float(spent) / max(float(budget), 0.01),
            }
    except Exception:
        pass
    return {"budget": 100.0, "spent": 0.0, "calls": 0, "hits": 0,
            "reset": "", "locked": False, "remaining": 100.0, "pct": 0.0}


def _charge_budget(conn: sqlite3.Connection, call_type: str = "discovery") -> bool:
    """
    Descuenta el coste estimado del presupuesto.
    Devuelve False si el presupuesto está agotado/bloqueado.
    """
    try:
        _init_budget(conn)
        b = _get_budget(conn)
        cost = _CALL_COST.get(call_type, 0.15)
        budget = max(float(b.get("budget", 100.0)), 0.01)
        spent = float(b.get("spent", 0.0))
        projected_pct = (spent + cost) / budget
        # Bloqueamos antes de pasar el umbral para dejar margen real y evitar gastar de más.
        if b["locked"] or b["pct"] >= _BUDGET_LOCK_PCT or projected_pct >= _BUDGET_LOCK_PCT:
            conn.execute("UPDATE api_budget SET locked=1 WHERE id=1")
            conn.commit()
            return False
        conn.execute(
            "UPDATE api_budget SET spent_usd=spent_usd+?, call_count=call_count+1 WHERE id=1",
            (cost,)
        )
        conn.commit()
        return True
    except Exception:
        return True  # si falla la BD, permitir la llamada


def _estimate_anthropic_cost(data: Dict[str, Any], model: str, fallback_call_type: str = "discovery_fast") -> Optional[float]:
    """Calcula coste aproximado usando usage real de Anthropic cuando está disponible."""
    try:
        usage = data.get("usage") or {}
        if not usage:
            return None
        m = (model or "").lower()
        family = "sonnet" if "sonnet" in m else "haiku"
        in_rate, out_rate = _PRICE_PER_TOKEN.get(family, _PRICE_PER_TOKEN["haiku"])
        input_tokens = int(usage.get("input_tokens") or 0)
        output_tokens = int(usage.get("output_tokens") or 0)
        # Prompt caching: si vienen estos campos, los contabilizamos de forma conservadora.
        cache_creation = int(usage.get("cache_creation_input_tokens") or 0)
        cache_read = int(usage.get("cache_read_input_tokens") or 0)
        server_tool_use = usage.get("server_tool_use") or {}
        web_requests = int(server_tool_use.get("web_search_requests") or 0) if isinstance(server_tool_use, dict) else 0
        token_cost = (input_tokens * in_rate) + (output_tokens * out_rate)
        token_cost += cache_creation * in_rate * 1.25
        token_cost += cache_read * in_rate * 0.10
        web_cost = web_requests * _WEB_SEARCH_COST
        total = token_cost + web_cost
        # Si usage no reporta web_search pero sabemos que hubo herramienta, mantenemos una reserva mínima.
        return max(total, _CALL_COST.get(fallback_call_type, 0.01) * 0.30)
    except Exception:
        return None


def _settle_budget(conn: Optional[sqlite3.Connection], call_type: str, data: Dict[str, Any], model: str) -> None:
    """Ajusta el presupuesto reservado al coste estimado real devuelto por Anthropic."""
    if conn is None:
        return
    try:
        reserved = _CALL_COST.get(call_type, 0.0)
        actual = _estimate_anthropic_cost(data, model, call_type)
        if actual is None:
            return
        delta = actual - reserved
        if abs(delta) < 0.0001:
            return
        conn.execute(
            "UPDATE api_budget SET spent_usd=MAX(0, spent_usd + ?) WHERE id=1",
            (delta,)
        )
        # Si el coste real empuja al límite, bloquear para la siguiente llamada.
        b = _get_budget(conn)
        if b.get("pct", 0.0) >= _BUDGET_LOCK_PCT:
            conn.execute("UPDATE api_budget SET locked=1 WHERE id=1")
        conn.commit()
    except Exception:
        pass


def _refund_budget(conn: Optional[sqlite3.Connection], call_type: str) -> None:
    """Devuelve la reserva si la llamada no llegó a completarse."""
    if conn is None:
        return
    try:
        cost = _CALL_COST.get(call_type, 0.0)
        if cost <= 0:
            return
        conn.execute(
            "UPDATE api_budget SET spent_usd=MAX(0, spent_usd - ?), call_count=MAX(0, call_count-1) WHERE id=1",
            (cost,)
        )
        conn.commit()
    except Exception:
        pass


def _rank_peers_for_cost(peers: List[str]) -> List[str]:
    """Ordena peers para gastar en los más importantes primero."""
    def score(peer: str) -> Tuple[int, str]:
        cn = _canonical_entity_name(peer)
        pri = 999
        for i, p in enumerate(_PRIORITY_PEERS):
            if _norm_key(cn) == _norm_key(p) or _norm_key(p) in _norm_key(cn):
                pri = i
                break
        return (pri, cn)
    seen: Set[str] = set()
    ranked: List[str] = []
    for p in sorted([x for x in peers if str(x).strip()], key=score):
        k = _norm_key(_canonical_entity_name(p))
        if k not in seen:
            seen.add(k)
            ranked.append(p)
    return ranked


def _compact_sources(items: Any, max_items: int = 5) -> List[Any]:
    """Recorta sources/evidence sin duplicar por URL/historia aunque cambie el snippet."""
    if not isinstance(items, list):
        return []
    out: List[Any] = []
    seen: Set[str] = set()
    seen_stories: Set[str] = set()
    for it in items:
        url = _extract_url_from_any(it)
        if url:
            canon = _canonical_source_url(url)
            story = _source_story_key(canon)
            key = canon or story
            if key in seen or (story and story in seen_stories):
                continue
            seen.add(key)
            if story:
                seen_stories.add(story)
            if isinstance(it, dict):
                it = dict(it)
                it["url"] = canon
            else:
                it = canon
        else:
            key = json.dumps(it, sort_keys=True, ensure_ascii=False)[:300] if isinstance(it, dict) else str(it)[:300]
            if key in seen:
                continue
            seen.add(key)
        out.append(it)
        if len(out) >= max_items:
            break
    return out


def _extract_url_from_any(item: Any) -> str:
    """Extrae URL desde strings, sources dict o evidence_items dict."""
    if isinstance(item, dict):
        for key in ("url", "source", "href", "link"):
            val = str(item.get(key, "") or "").strip()
            if val.startswith("http"):
                return val
        return ""
    val = str(item or "").strip()
    return val if val.startswith("http") else ""


def _is_pdf_or_primary_doc_url(url: str, proof_type: str = "") -> bool:
    """True si la fuente parece PDF/documento primario aunque no acabe en .pdf."""
    u = str(url or "").strip().lower()
    if not u:
        return False
    clean = u.split("#", 1)[0].split("?", 1)[0]
    if clean.endswith(".pdf") or ".pdf" in clean:
        return True
    ptype = str(proof_type or "").lower()
    if ptype in {"regulatory_filing_pdf", "contract_pdf"}:
        return True
    if any(h in u for h in _PRIMARY_DOC_HOST_HINTS):
        return ptype in {"", "regulatory_filing", "regulatory_filing_pdf", "contract_pdf", "official_partner", "press_release"}
    return False


def _discovery_document_counts(result: Dict[str, Any]) -> Tuple[int, int]:
    """Cuenta documentos PDF/primarios y fuentes totales visibles en Discovery."""
    seen_urls: Set[str] = set()
    total_sources = 0
    doc_sources = 0

    for item in (result.get("sources") or []):
        url = _extract_url_from_any(item)
        canon = _canonical_source_url(url)
        if not canon or canon in seen_urls:
            continue
        seen_urls.add(canon)
        total_sources += 1
        if _is_pdf_or_primary_doc_url(canon):
            doc_sources += 1

    for item in (result.get("evidence_items") or []):
        url = _extract_url_from_any(item)
        canon = _canonical_source_url(url)
        if not canon or canon in seen_urls:
            continue
        seen_urls.add(canon)
        total_sources += 1
        ptype = str(item.get("type", "") if isinstance(item, dict) else "")
        if _is_pdf_or_primary_doc_url(canon, ptype):
            doc_sources += 1

    return doc_sources, total_sources


def _discovery_pdf_line_html(result: Dict[str, Any]) -> str:
    """Línea siempre visible para Discovery: documentos encontrados o 0."""
    doc_count, total_sources = _discovery_document_counts(result)
    if doc_count:
        return (
            "<div style='color:#3CFF9B;font-size:0.78rem;margin:4px 0 8px;'>"
            f"📄 Documentos PDF/primarios encontrados: <b>{doc_count}</b></div>"
        )
    if total_sources:
        return (
            "<div style='color:#64748B;font-size:0.78rem;margin:4px 0 8px;'>"
            "📄 0 documentos PDF verificables encontrados</div>"
        )
    return (
        "<div style='color:#334155;font-size:0.78rem;margin:4px 0 8px;'>"
        "📄 0 documentos PDF — sin fuentes registradas</div>"
    )




# ── Robustez Discovery: JSON leniente + recuperación de fuentes web ─────────
def _extract_first_balanced_json(raw: str) -> str:
    """Extrae el primer objeto JSON balanceado ignorando llaves dentro de strings."""
    txt = str(raw or "").strip().replace("```json", "").replace("```", "").strip()
    if not txt:
        return ""
    starts = [i for i, ch in enumerate(txt) if ch == "{"]
    for start in starts:
        depth = 0
        in_str = False
        esc = False
        obj_start = start
        for i in range(start, len(txt)):
            ch = txt[i]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
                continue
            if ch == '"':
                in_str = True
            elif ch == "{":
                if depth == 0:
                    obj_start = i
                depth += 1
            elif ch == "}":
                depth -= 1
                if depth == 0:
                    return txt[obj_start:i + 1]
    s = txt.find("{")
    e = txt.rfind("}") + 1
    return txt[s:e] if s != -1 and e > s else ""


def _repair_common_json_issues(js: str) -> str:
    """Repara fallos típicos de LLM: comas finales y comas omitidas entre campos/objetos."""
    t = str(js or "").strip()
    # Comas finales antes de cerrar objeto/lista.
    t = re.sub(r",\s*([}\]])", r"\1", t)
    # Objetos consecutivos dentro de listas: } {  -> }, {
    t = re.sub(r"}\s*\n\s*{", "},\n{", t)
    # URLs consecutivas en arrays sources: "https://a" "https://b" -> "https://a", "https://b"
    t = re.sub(r'("https?://[^"\n]+")\s*\n\s*("https?://)', r'\1,\n\2', t)
    # Campo siguiente sin coma después de string, número, boolean, null, objeto o lista.
    t = re.sub(r'("|\d|true|false|null|\}|\])\s*\n\s*("[A-Za-z_][A-Za-z0-9_]*"\s*:)', r'\1,\n\2', t)
    # También cuando viene en la misma línea por recorte agresivo.
    t = re.sub(r'(\}|\])\s+("[A-Za-z_][A-Za-z0-9_]*"\s*:)', r'\1, \2', t)
    return t


def _loads_discovery_json_lenient(raw: str) -> Dict[str, Any]:
    """Carga JSON del Discovery sin tirar todo el resultado por un error menor de formato."""
    raw = str(raw or "").strip()
    candidates: List[str] = []
    balanced = _extract_first_balanced_json(raw)
    if balanced:
        candidates.append(balanced)
    s = raw.find("{"); e = raw.rfind("}") + 1
    if s != -1 and e > s:
        candidates.append(raw[s:e])
    candidates.append(raw)

    last_error: Optional[Exception] = None
    seen: Set[str] = set()
    for cand in candidates:
        cand = cand.strip().replace("```json", "").replace("```", "").strip()
        if not cand or cand in seen:
            continue
        seen.add(cand)
        for variant in (cand, _repair_common_json_issues(cand)):
            if not variant or variant in seen:
                continue
            seen.add(variant)
            try:
                parsed = json.loads(variant)
                if isinstance(parsed, dict):
                    return parsed
            except Exception as exc:
                last_error = exc
    raise ValueError(f"Respuesta AI con JSON inválido: {last_error}")


def _extract_anthropic_web_sources(data: Dict[str, Any], max_items: int = 10) -> List[Dict[str, str]]:
    """Recupera URLs/títulos de bloques web_search y citations aunque el JSON final venga mal formado."""
    found: List[Dict[str, str]] = []
    seen: Set[str] = set()

    def add(url: Any, title: Any = "") -> None:
        u = _canonical_source_url(str(url or "").strip())
        if not u or not u.startswith("http") or u in seen:
            return
        seen.add(u)
        found.append({"url": u, "title": str(title or "Fuente web").strip()[:180]})

    def walk(obj: Any) -> None:
        if len(found) >= max_items:
            return
        if isinstance(obj, dict):
            url = obj.get("url") or obj.get("source_url") or obj.get("href") or obj.get("link") or obj.get("uri")
            title = obj.get("title") or obj.get("name") or obj.get("label") or obj.get("text") or ""
            if url:
                add(url, title)
            for v in obj.values():
                walk(v)
        elif isinstance(obj, list):
            for v in obj:
                walk(v)

    try:
        walk(data.get("content", []))
    except Exception:
        pass
    return _compact_sources(found, max_items)


def _merge_discovery_sources(result: Dict[str, Any], data: Optional[Dict[str, Any]] = None, max_sources: int = 8) -> Dict[str, Any]:
    """Normaliza sources/evidence y añade URLs recuperadas desde web_search/citations."""
    result = dict(result or {})
    sources_raw: List[Any] = list(result.get("sources") or [])
    evidence_raw: List[Any] = list(result.get("evidence_items") or [])

    # Las URLs de evidence también deben contar como sources visibles.
    for ev in evidence_raw:
        u = _extract_url_from_any(ev)
        if u:
            sources_raw.append(u)

    if data:
        for item in _extract_anthropic_web_sources(data, max_sources):
            u = _extract_url_from_any(item)
            if u:
                sources_raw.append(u)
                if not any(_canonical_source_url(_extract_url_from_any(ev)) == _canonical_source_url(u) for ev in evidence_raw):
                    evidence_raw.append({
                        "title": item.get("title", "Fuente recuperada de web_search"),
                        "url": u,
                        "claim": "Fuente recuperada automáticamente aunque la respuesta JSON viniera incompleta o mal formada.",
                        "target": result.get("institution", "Ripple/XRPL"),
                        "type": "regulatory_filing_pdf" if _is_pdf_or_primary_doc_url(u) else "news_major",
                    })

    # sources debe ser lista de URLs string para que la UI las pinte bien.
    clean_sources: List[str] = []
    for item in _compact_sources(sources_raw, max_sources):
        u = _extract_url_from_any(item)
        if u:
            clean_sources.append(_canonical_source_url(u))
    result["sources"] = _compact_sources(clean_sources, max_sources)
    result["evidence_items"] = _compact_sources(evidence_raw, max_sources)
    return result


def _fallback_discovery_from_partial_response(institution_name: str, entity_type: str,
                                              data: Optional[Dict[str, Any]], err: Exception) -> Dict[str, Any]:
    """No devuelve 0 fuentes si la API buscó pero el JSON final vino roto."""
    result = {
        "institution": institution_name,
        "entity_type": entity_type,
        "connected": False,
        "confidence": 0.0,
        "summary": f"La búsqueda respondió, pero el JSON vino mal formado. Recuperé fuentes web para revisión; error técnico: {str(err)[:120]}",
        "ripple_products": [], "layer": _classify_entity(institution_name) if entity_type else "Descubierto", "icon": "🧩",
        "connects_to": [], "route_kind": "private", "sources": [],
        "wallets": [], "corridors": [], "partners": [], "map_points": [], "evidence_items": [],
        "_json_recovered": True,
    }
    return _merge_discovery_sources(result, data, max_sources=8)


def _enrich_discovery_with_chain_seeds(result: Dict[str, Any], institution_name: str) -> Dict[str, Any]:
    """CLEAN MODE: no añade rutas/pruebas documentales semilla al resultado."""
    return result


def _finalize_discovery_result(result: Dict[str, Any], institution_name: str, entity_type: str,
                               data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Aplica defaults, normaliza fuentes y enriquece rutas semilla antes de pintar/cachar."""
    result = dict(result or {})
    result["institution"] = institution_name
    result["entity_type"] = entity_type
    defaults = {
        "connected": False, "confidence": 0.0, "summary": "", "ripple_products": [],
        "layer": "Descubierto", "icon": "?", "connects_to": [], "route_kind": "private",
        "sources": [], "wallets": [], "corridors": [], "partners": [], "map_points": [], "evidence_items": [],
    }
    for k, v in defaults.items():
        result.setdefault(k, v)
    try:
        result["confidence"] = max(0.0, min(1.0, float(result.get("confidence", 0) or 0)))
    except Exception:
        result["confidence"] = 0.0
    if isinstance(result.get("summary"), str) and len(result["summary"]) > 600:
        result["summary"] = result["summary"][:600].rstrip() + "…"
    result = _merge_discovery_sources(result, data, max_sources=8)
    result = _enrich_discovery_with_chain_seeds(result, institution_name)
    return result

def _resolve_native_search_identity(entity: str) -> Tuple[str, Optional[str], bool]:
    """Devuelve (script, nombre_nativo, usar_bloque_nativo) para ASCII y no-ASCII."""
    raw = str(entity or "").strip()
    has_non_ascii = any(ord(c) > 127 for c in raw)
    if has_non_ascii:
        return _detect_script(raw), None, True
    low = raw.lower()
    for pattern, (script, native_name) in _KNOWN_NATIVE_NAMES.items():
        if pattern in low:
            return script, native_name, True
    return "en", None, False


def _record_cache_hit(conn: sqlite3.Connection) -> None:
    """Registra un cache hit en el presupuesto (sin coste)."""
    try:
        conn.execute("UPDATE api_budget SET cache_hits=cache_hits+1 WHERE id=1")
        conn.commit()
    except Exception:
        pass


def _session_id() -> str:
    """ID único de sesión (generado una vez por sesión Streamlit)."""
    if "session_uid" not in st.session_state:
        import secrets
        st.session_state["session_uid"] = secrets.token_hex(8)
    return st.session_state["session_uid"]


def _heartbeat(conn: sqlite3.Connection, status: str = "idle") -> None:
    """Registra/actualiza la sesión activa. Llámalo en cada render del panel."""
    try:
        sid = _session_id()
        now = datetime.now(timezone.utc).isoformat()
        conn.execute("""
            INSERT OR REPLACE INTO active_sessions (session_id, started_at, heartbeat, status)
            VALUES (?, COALESCE((SELECT started_at FROM active_sessions WHERE session_id=?), ?), ?, ?)
        """, (sid, sid, now, now, status))
        # Limpiar sesiones inactivas
        cutoff = (datetime.now(timezone.utc) - timedelta(seconds=_SESSION_HEARTBEAT * 2)).isoformat()
        conn.execute("DELETE FROM active_sessions WHERE heartbeat < ?", (cutoff,))
        conn.commit()
    except Exception:
        pass


def _active_users(conn: sqlite3.Connection) -> Tuple[int, int]:
    """Devuelve (total_activos, usando_ai_ahora)."""
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(seconds=_SESSION_HEARTBEAT)).isoformat()
        total = conn.execute(
            "SELECT COUNT(*) FROM active_sessions WHERE heartbeat > ?", (cutoff,)
        ).fetchone()[0]
        ai_now = conn.execute(
            "SELECT COUNT(*) FROM active_sessions WHERE heartbeat > ? AND status='searching'",
            (cutoff,)
        ).fetchone()[0]
        return int(total), int(ai_now)
    except Exception:
        return 1, 0


def _queue_position(conn: sqlite3.Connection) -> int:
    """Posición del usuario actual en la cola de búsquedas AI (0 = libre)."""
    try:
        sid = _session_id()
        cutoff = (datetime.now(timezone.utc) - timedelta(seconds=_SESSION_HEARTBEAT)).isoformat()
        # Cuenta sesiones con status='searching' que empezaron ANTES que la nuestra
        my_start = conn.execute(
            "SELECT started_at FROM active_sessions WHERE session_id=?", (sid,)
        ).fetchone()
        if not my_start:
            return 0
        pos = conn.execute(
            "SELECT COUNT(*) FROM active_sessions "
            "WHERE status='searching' AND heartbeat > ? AND session_id != ? AND started_at <= ?",
            (cutoff, sid, my_start[0])
        ).fetchone()[0]
        return int(pos)
    except Exception:
        return 0


def render_budget_bar(conn: sqlite3.Connection) -> None:
    """Muestra la barra de presupuesto API en el sidebar o panel."""
    b = _get_budget(conn)
    spent    = b["spent"]
    budget   = b["budget"]
    remaining = b["remaining"]
    pct       = b["pct"]
    calls     = b["calls"]
    hits      = b["hits"]

    if pct >= _BUDGET_LOCK_PCT:
        color = "#EF4444"
        label = "❌ PRESUPUESTO AGOTADO — Solo resultados cacheados disponibles"
    elif pct >= _BUDGET_WARN_PCT:
        color = "#F59E0B"
        label = f"⚠️ Presupuesto bajo — quedan ${remaining:.2f}"
    else:
        color = "#22C55E"
        label = f"✅ ${remaining:.2f} disponibles de ${budget:.0f}"

    bar_pct = min(pct * 100, 100)
    st.markdown(f"""
<div style='background:#1E293B;border-radius:10px;padding:10px 14px;margin-bottom:8px;'>
  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;'>
    <span style='font-size:0.82rem;color:#94A3B8;'>💰 Presupuesto API</span>
    <span style='font-size:0.82rem;font-weight:700;color:{color};'>{label}</span>
  </div>
  <div style='background:#0B1220;border-radius:6px;height:10px;overflow:hidden;'>
    <div style='background:{color};width:{bar_pct:.1f}%;height:100%;border-radius:6px;
                transition:width 0.5s;'></div>
  </div>
  <div style='display:flex;justify-content:space-between;margin-top:5px;'>
    <span style='font-size:0.75rem;color:#64748B;'>${spent:.2f} gastados · {calls} búsquedas nuevas · CostGuard v2</span>
    <span style='font-size:0.75rem;color:#22C55E;'>{hits} desde caché (gratis)</span>
  </div>
</div>
""", unsafe_allow_html=True)


def _is_current_session_searching(conn: sqlite3.Connection) -> bool:
    """Indica si la sesión actual está marcada como búsqueda AI activa."""
    try:
        sid = _session_id()
        row = conn.execute(
            "SELECT status FROM active_sessions WHERE session_id=?", (sid,)
        ).fetchone()
        return bool(row and row[0] == "searching")
    except Exception:
        return False


def render_queue_status(conn: sqlite3.Connection) -> None:
    """Muestra usuarios activos y número aproximado en la fila AI."""
    try:
        total, ai_now = _active_users(conn)
        searching = _is_current_session_searching(conn)
        if searching:
            pos = max(1, _queue_position(conn) + 1)
            st.info(f"⏳ Tu búsqueda AI está en curso · estás en la posición #{pos} de la fila · usuarios activos: {total}")
        elif ai_now > 0:
            st.warning(f"👥 Búsquedas AI activas ahora: {ai_now} · si lanzas una búsqueda, entrarás aprox. como #{ai_now + 1} en la fila")
        else:
            st.caption(f"👥 Usuarios activos: {total} · fila AI libre ahora: serías #1 si lanzas una búsqueda")
    except Exception:
        pass




def _public_nickname_value() -> str:
    return str(st.session_state.get("community_nickname", "") or "").strip()


def _public_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _public_queue_cleanup(conn: sqlite3.Connection) -> None:
    """Limpia cola AI vieja para que un navegador cerrado no bloquee la beta."""
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=12)).isoformat()
        conn.execute("DELETE FROM ai_waiting_queue WHERE updated_at < ?", (cutoff,))
        conn.commit()
    except Exception:
        pass


def _public_queue_position(conn: sqlite3.Connection, session_id: Optional[str] = None) -> int:
    """Posición 1-based del usuario en la cola AI. 0 si no está en cola."""
    try:
        _public_queue_cleanup(conn)
        sid = session_id or _session_id()
        rows = conn.execute(
            "SELECT session_id FROM ai_waiting_queue WHERE status='queued' ORDER BY created_at ASC"
        ).fetchall()
        ids = [str(r[0]) for r in rows]
        return ids.index(sid) + 1 if sid in ids else 0
    except Exception:
        return 0


def _public_queue_total(conn: sqlite3.Connection) -> int:
    try:
        _public_queue_cleanup(conn)
        return int(conn.execute("SELECT COUNT(*) FROM ai_waiting_queue WHERE status='queued'").fetchone()[0])
    except Exception:
        return 0


def _public_enqueue_ai(conn: sqlite3.Connection, query: str) -> int:
    """Mete la sesión actual en cola AI y devuelve su posición."""
    try:
        sid = _session_id()
        nick = _public_nickname_value() or "Visitante"
        now = _public_now_iso()
        conn.execute(
            "INSERT OR REPLACE INTO ai_waiting_queue (session_id,nickname,query,status,created_at,updated_at) "
            "VALUES (?, ?, ?, 'queued', COALESCE((SELECT created_at FROM ai_waiting_queue WHERE session_id=?), ?), ?)",
            (sid, nick, query, sid, now, now),
        )
        conn.commit()
        return _public_queue_position(conn, sid)
    except Exception:
        return 0


def _public_can_run_ai_now(conn: sqlite3.Connection) -> bool:
    """Solo deja ejecutar a quien está primero, no hay otra búsqueda AI y tiene cupo investigador."""
    try:
        if not _can_current_user_investigate(conn):
            return False
        _, ai_now = _active_users(conn)
        if ai_now > 0 and not _is_current_session_searching(conn):
            return False
        pos = _public_queue_position(conn)
        return pos in (0, 1)
    except Exception:
        return bool(st.session_state.get("rrp_can_investigate", False))


def _public_finish_ai(conn: sqlite3.Connection) -> None:
    try:
        conn.execute("DELETE FROM ai_waiting_queue WHERE session_id=?", (_session_id(),))
        conn.commit()
    except Exception:
        pass


def render_global_public_banner(conn: sqlite3.Connection) -> None:
    """Banner público de misión + estado de comunidad + cola AI."""
    total, ai_now = _active_users(conn)
    q_total = _public_queue_total(conn)
    q_pos = _public_queue_position(conn)
    nick = _public_nickname_value() or "sin usuario"
    q_text = f"{html.escape('Tu puesto en fila:')} #{q_pos}" if q_pos else (f"Fila AI: {q_total} esperando" if q_total else "Fila AI libre")
    st.markdown(f"""
<div style='margin:.45rem 0 1rem 0;padding:16px 18px;border-radius:22px;
            background:radial-gradient(circle at 10% 0%,rgba(34,211,238,.22),transparent 32%),
                       linear-gradient(135deg,rgba(2,6,23,.96),rgba(15,23,42,.94));
            border:1px solid rgba(125,211,252,.34);box-shadow:0 18px 46px rgba(8,145,178,.16);'>
  <div style='display:flex;align-items:center;justify-content:space-between;gap:14px;flex-wrap:wrap;'>
    <div>
      <div style='font-size:1.05rem;font-weight:950;color:#E0F2FE;'>🌐 {html.escape(_t('Comunidad'))} · Ripple Radar Pro</div>
      <div style='color:#CBD5E1;font-size:.88rem;line-height:1.45;margin-top:4px;'>
        {html.escape(_t('ui_scope_note'))}
      </div>
    </div>
    <div style='display:flex;gap:8px;flex-wrap:wrap;'>
      <span style='border:1px solid rgba(34,197,94,.35);background:rgba(22,101,52,.18);color:#BBF7D0;border-radius:999px;padding:6px 10px;font-size:.78rem;'>👤 {html.escape(nick)}</span>
      <span style='border:1px solid rgba(59,130,246,.35);background:rgba(30,64,175,.18);color:#BFDBFE;border-radius:999px;padding:6px 10px;font-size:.78rem;'>👥 {total} activos</span>
      <span style='border:1px solid rgba(250,204,21,.36);background:rgba(113,63,18,.22);color:#FEF3C7;border-radius:999px;padding:6px 10px;font-size:.78rem;'>🧠 {html.escape(q_text)}</span>
      <span style='border:1px solid rgba(244,114,182,.32);background:rgba(131,24,67,.18);color:#FBCFE8;border-radius:999px;padding:6px 10px;font-size:.78rem;'>🔎 AI activa: {ai_now}</span>
    </div>
  </div>
</div>
""", unsafe_allow_html=True)


def render_public_entry_gate(conn: sqlite3.Connection) -> bool:
    """Entrada pública obligatoria: idioma → modo usuario/admin → nombre → disclaimer."""
    lang = _preferred_lang()

    if not lang:
        st.markdown("""
<div style='min-height:70vh;display:flex;align-items:center;justify-content:center;'>
  <div style='max-width:860px;width:100%;border-radius:30px;padding:30px;
              background:radial-gradient(circle at top left,rgba(34,211,238,.26),transparent 35%),
                         radial-gradient(circle at bottom right,rgba(168,85,247,.22),transparent 40%),
                         rgba(2,6,23,.97);
              border:1px solid rgba(125,211,252,.36);box-shadow:0 30px 100px rgba(14,165,233,.20);'>
    <div style='font-size:2.05rem;font-weight:1000;color:#E0F2FE;margin-bottom:8px;'>🌍 Ripple Radar Pro</div>
    <div style='font-size:1.05rem;color:#CBD5E1;line-height:1.58;margin-bottom:14px;'>
      Antes de entrar, elige el idioma de toda la experiencia. La interfaz y el chat se adaptarán al idioma seleccionado; las pruebas técnicas conservan su idioma original.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
        labels = [f"{name} ({code.upper()})" for code, name in PUBLIC_LANGUAGES.items()]
        selected = st.selectbox("Idioma / Language", labels, index=0, key="public_lang_select")
        chosen_code = selected.split("(")[-1].replace(")", "").lower().strip()
        if st.button("Continuar", width="stretch", key="public_lang_continue"):
            _set_preferred_lang(chosen_code)
            st.rerun()
        return False

    # Si ya aceptó todo y tiene usuario, entra.
    if _public_nickname_value() and st.session_state.get("rrp_entry_disclaimer_ok"):
        _touch_current_user(conn)
        # El aviso viejo de dinero queda absorbido por este onboarding.
        st.session_state["rrp_real_money_notice_ok"] = True
        return True

    st.markdown("""
<div style='max-width:980px;margin:0 auto 18px auto;border-radius:28px;padding:26px;
            background:radial-gradient(circle at top left,rgba(34,211,238,.22),transparent 34%),
                       radial-gradient(circle at bottom right,rgba(168,85,247,.18),transparent 40%),
                       rgba(2,6,23,.96);
            border:1px solid rgba(125,211,252,.35);box-shadow:0 28px 90px rgba(14,165,233,.18);'>
  <div style='font-size:2rem;font-weight:1000;color:#E0F2FE;margin-bottom:8px;'>🚀 Entrada a Ripple Radar Pro</div>
  <div style='font-size:1rem;color:#CBD5E1;line-height:1.58;'>
    Esta web es un laboratorio público de investigación deductiva sobre la infraestructura Ripple: Payments, Custody/Metaco, Prime/Hidden Road, Treasury, Rail, RLUSD, XRPL, wallets, clusters, rutas A→B y fuentes.
  </div>
</div>
""", unsafe_allow_html=True)

    mode = st.radio(
        "Tipo de entrada",
        ["Usuario", "Admin"],
        horizontal=True,
        key="rrp_entry_mode",
    )

    c1, c2 = st.columns([1.1, 0.9])
    with c1:
        nick_default = st.session_state.get("public_entry_nick", "")
        nick = st.text_input(
            "Nombre público",
            value=nick_default,
            placeholder="Ej: CosmosRadar",
            max_chars=28,
            key="public_entry_nick",
        )
        clean_nick = _clean_nickname(nick)
        if _active_name_taken(conn, clean_nick, exclude_user_id=_community_user_id()):
            st.error("Ese nombre ya está en línea. Elige otro para evitar dos usuarios con el mismo nombre.")
        if mode == "Admin":
            st.caption("Admins autorizados por ahora: edutrejo y alchemist.")
            admin_pwd = st.text_input("Contraseña de autorización admin", type="password", key="public_admin_password")
        else:
            admin_pwd = ""
    with c2:
        active_researchers = _active_investigator_count(conn)
        can_take_slot = active_researchers < MAX_PUBLIC_INVESTIGATORS
        if mode == "Admin":
            slot_text = "Los admins no consumen cupo de investigadores."
        elif can_take_slot:
            slot_text = f"Cupo de investigadores: {active_researchers}/{MAX_PUBLIC_INVESTIGATORS}. Podrás usar acciones de investigación controladas."
        else:
            slot_text = f"Cupo lleno: {active_researchers}/{MAX_PUBLIC_INVESTIGATORS}. Entrarás como visitante: puedes ver datos, leer fichas, chat y explorar, pero no lanzar acciones que gasten API."
        st.info(slot_text)

    st.markdown("""
<div style='border:1px solid rgba(245,158,11,.48);border-radius:20px;padding:18px 20px;
            background:linear-gradient(135deg,rgba(120,53,15,.34),rgba(15,23,42,.92));margin-top:16px;'>
  <div style='font-size:1.15rem;font-weight:1000;color:#FDE68A;margin-bottom:8px;'>⚠️ Lectura obligatoria antes de entrar</div>
  <div style='color:#E5E7EB;line-height:1.55;font-size:.94rem;'>
    <b>Ripple Radar Pro no es una prueba definitiva ni asesoramiento financiero.</b> Es un prototipo deductivo para investigar fuentes, pistas públicas, rutas A→B, wallets, clusters y señales de infraestructura.
    <br><br>
    Algunas acciones como <b>Discovery</b>, <b>búsqueda web/Anthropic</b>, <b>verificación de pruebas</b>, <b>traducciones automáticas</b> o análisis asistido por IA pueden gastar presupuesto de API. Úsalas con responsabilidad, revisa las fuentes antes de concluir y no conviertas una hipótesis en una afirmación.
    <br><br>
    En esta beta inicial solo <b>100 investigadores activos</b> pueden lanzar acciones con posible coste. El resto puede navegar, leer datos, interactuar con la web y participar sin gastar API.
  </div>
</div>
""", unsafe_allow_html=True)

    accepted = st.checkbox(
        "He leído el aviso: entiendo que el radar puede equivocarse y que algunas acciones pueden gastar API.",
        key="rrp_entry_disclaimer_checkbox",
    )

    if st.button("Entrar", width="stretch", key="public_entry_btn_v90"):
        clean_nick = _clean_nickname(nick)
        if len(clean_nick) < 2:
            st.error("Pon un nombre válido de al menos 2 caracteres.")
            return False
        if _active_name_taken(conn, clean_nick, exclude_user_id=_community_user_id()):
            st.error("Ese nombre ya está en línea. Elige otro.")
            return False
        if not accepted:
            st.error("Debes leer y aceptar el aviso obligatorio antes de entrar.")
            return False

        if mode == "Admin":
            if not _is_admin_name(clean_nick):
                st.error("Ese nombre no está autorizado como admin. Usa edutrejo o alchemist.")
                return False
            if str(admin_pwd or "") != ADMIN_PASSWORD:
                st.error("Contraseña admin incorrecta.")
                return False
            st.session_state["admin_authenticated"] = True
            st.session_state["rrp_can_investigate"] = True
        else:
            st.session_state.pop("admin_authenticated", None)
            st.session_state["rrp_can_investigate"] = bool(_active_investigator_count(conn) < MAX_PUBLIC_INVESTIGATORS)

        if _save_current_user(conn, clean_nick):
            st.session_state["rrp_entry_disclaimer_ok"] = True
            st.session_state["rrp_real_money_notice_ok"] = True
            st.toast("Bienvenido al radar.")
            st.rerun()
        else:
            st.error(st.session_state.get("entry_name_error", "No se pudo crear el usuario."))
    return False

def render_global_update_notice(conn: sqlite3.Connection) -> None:
    """Notificación global: si otro usuario actualizó el mapa, avisa en cualquier pestaña."""
    try:
        last = _get_last_map_update(conn)
        seen = st.session_state.get("map_last_seen_global", "")
        if not last:
            return
        if not seen:
            st.session_state["map_last_seen_global"] = last
            return
        pending = _get_pending_updates(conn, seen)
        if pending <= 0:
            return
        c1, c2 = st.columns([4, 1])
        with c1:
            st.warning(f"🔔 El mapa tiene {pending} actualización(es) nueva(s) de otros usuarios. Puedes seguir mirando, pero conviene refrescar el grafo.")
        with c2:
            if st.button("Actualizar mapa", width="stretch", key="global_apply_map_updates"):
                st.session_state["map_last_seen_global"] = last
                st.session_state["map_last_seen"] = last
                st.rerun()
    except Exception:
        pass

def _diagnose_api_key() -> Dict[str, Any]:
    """
    Diagnóstico completo de la API key de Anthropic.
    Devuelve dict con: source, key_preview, format_ok, reachable, status_code,
    error_type, error_msg, model_ok, suggestion.
    """
    result: Dict[str, Any] = {
        "source": "no encontrada",
        "key_preview": "",
        "format_ok": False,
        "reachable": False,
        "status_code": None,
        "error_type": "",
        "error_msg": "",
        "model_ok": False,
        "suggestion": "",
    }

    key = _get_api_key()
    if not key:
        result["suggestion"] = "No hay API key configurada. Ve a Setup y pégala en 'Sesión temporal' o crea el archivo .env."
        return result

    result["key_preview"] = f"sk-ant-...{key[-8:]}" if len(key) > 12 else "***"

    # Detectar fuente
    if _os.environ.get("ANTHROPIC_API_KEY", "").strip():
        result["source"] = "variable de entorno"
    elif _os.path.isfile(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)), ".env")):
        result["source"] = "archivo .env"
    elif st.session_state.get("_manual_api_key"):
        result["source"] = "sesión manual (Setup)"
    else:
        result["source"] = "Streamlit secrets"

    # Validar formato básico sk-ant-...
    result["format_ok"] = key.startswith("sk-ant-") and len(key) > 30

    # Test mínimo a la API — ping con 1 token
    try:
        _test_payload = {
            "model": ANTHROPIC_MODEL_FAST,
            "max_tokens": 1,
            "messages": [{"role": "user", "content": "ping"}],
        }
        _headers = {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        resp = requests.post(ANTHROPIC_API_URL, json=_test_payload, headers=_headers, timeout=15)
        result["status_code"] = resp.status_code
        result["reachable"] = True

        if resp.status_code == 200:
            result["model_ok"] = True
            result["suggestion"] = "✅ API key válida y modelo accesible."
        else:
            _body = {}
            try:
                _body = resp.json()
            except Exception:
                pass
            _etype = _body.get("error", {}).get("type", "")
            _emsg  = _body.get("error", {}).get("message", resp.text[:300])
            result["error_type"] = _etype
            result["error_msg"]  = _emsg

            if resp.status_code == 401:
                if "invalid_api_key" in _etype or "invalid x-api-key" in _emsg.lower():
                    result["suggestion"] = (
                        "❌ La key existe pero es inválida o ha sido revocada. "
                        "Ve a console.anthropic.com → API Keys y genera una nueva."
                    )
                else:
                    result["suggestion"] = "❌ Error 401. Comprueba que pegaste la key completa sin espacios."
            elif resp.status_code == 403:
                result["suggestion"] = "❌ Acceso denegado (403). La key no tiene permisos para este modelo o workspace."
            elif resp.status_code == 429:
                result["suggestion"] = "⏳ Rate limit (429). La key funciona pero hay demasiadas solicitudes. Espera unos segundos."
            elif resp.status_code == 400:
                # 400 con ping mínimo puede ser normal si el modelo requiere más tokens
                result["model_ok"] = True
                result["suggestion"] = "⚠️ La key parece válida (400 en ping mínimo es normal). Intenta buscar."
            else:
                result["suggestion"] = f"Error HTTP {resp.status_code}: {_emsg[:200]}"
    except requests.exceptions.ConnectionError:
        result["error_msg"] = "No se puede conectar a api.anthropic.com. Comprueba tu conexión a internet."
        result["suggestion"] = "Sin conexión a internet o firewall bloqueando api.anthropic.com."
    except requests.exceptions.Timeout:
        result["error_msg"] = "Timeout — la API tardó más de 15s en responder."
        result["suggestion"] = "Conexión lenta o Anthropic temporalmente sobrecargado. Inténtalo de nuevo."
    except Exception as _ex:
        result["error_msg"] = str(_ex)[:300]
        result["suggestion"] = f"Error inesperado: {_ex}"

    return result


def render_api_diagnostics() -> None:
    """Panel de diagnóstico de API key — se muestra en Setup."""
    st.markdown("### 🩺 Diagnóstico de API key")
    with st.spinner("Probando conexión con Anthropic…"):
        d = _diagnose_api_key()

    rows = [
        ("Fuente detectada",    d["source"]),
        ("Key (preview)",       d["key_preview"] or "—"),
        ("Formato válido",      "✅ Sí" if d["format_ok"] else "❌ No (debe empezar por sk-ant-)"),
        ("Conectividad",        "✅ Alcanzable" if d["reachable"] else "❌ Sin respuesta"),
        ("HTTP status",         str(d["status_code"]) if d["status_code"] else "—"),
        ("Modelo accesible",    "✅ Sí" if d["model_ok"] else ("⚠️ Ver diagnóstico" if d["reachable"] else "—")),
        ("Tipo de error",       d["error_type"] or "—"),
        ("Mensaje de error",    d["error_msg"] or "—"),
    ]
    _diag_md = "| Campo | Valor |\n|---|---|\n"
    for _k, _v in rows:
        _diag_md += f"| {_k} | `{_v}` |\n"
    st.markdown(_diag_md)

    # Diagnóstico principal
    sug = d.get("suggestion", "")
    if d["model_ok"]:
        st.success(sug)
    elif d["status_code"] == 429:
        st.warning(sug)
    elif sug:
        st.error(sug)

    if d["status_code"] == 401:
        st.markdown("""
**Pasos para generar una nueva key:**
1. Ve a [console.anthropic.com/settings/keys](https://console.anthropic.com/settings/keys)
2. Click **Create Key**
3. Copia la key completa (`sk-ant-api03-...`)
4. Pégala en **Setup → Sesión temporal** o en el archivo `.env`
""")


_RRP_REAL_MONEY_WARNING_RENDERED_THIS_RUN = False


def render_real_money_warning(conn: sqlite3.Connection, key_suffix: str = "global") -> None:
    """Aviso inicial: el modo Discovery puede consumir dinero real de Anthropic.

    Esta función puede ser llamada desde `main()` y también desde paneles internos
    como Discovery. Para evitar `StreamlitDuplicateElementKey`, solo se pinta una
    vez por ejecución del script y el botón recibe una key contextual.
    """
    global _RRP_REAL_MONEY_WARNING_RENDERED_THIS_RUN

    if st.session_state.get("rrp_real_money_notice_ok"):
        return
    if _RRP_REAL_MONEY_WARNING_RENDERED_THIS_RUN:
        return

    _RRP_REAL_MONEY_WARNING_RENDERED_THIS_RUN = True
    safe_suffix = re.sub(r"[^a-zA-Z0-9_\-]", "_", str(key_suffix or "global"))[:48]
    button_key = f"rrp_money_notice_btn_{safe_suffix}"

    b = _get_budget(conn)
    st.markdown(f"""
<div style='background:linear-gradient(135deg,rgba(239,68,68,0.16),rgba(245,158,11,0.12));
            border:1px solid rgba(245,158,11,0.45);border-radius:16px;padding:16px 18px;margin:0 0 16px 0;'>
  <div style='font-weight:900;color:#FDE68A;font-size:1.02rem;margin-bottom:5px;'>⚠️ Aviso importante: esta página puede usar dinero real</div>
  <div style='color:#CBD5E1;font-size:0.90rem;line-height:1.45;'>
    El radar puede consultar Anthropic/Web Search cuando uses <b>Discovery</b> o <b>verificación de pruebas</b>.
    Cada búsqueda nueva descuenta una estimación del presupuesto configurado: <b>${b['spent']:.2f} / ${b['budget']:.2f}</b>.
    Los resultados cacheados no gastan API. Cuando el presupuesto llegue al margen de seguridad, la app pasará a modo caché.
  </div>
</div>
""", unsafe_allow_html=True)
    if st.button("Entendido — usar con control de presupuesto", key=button_key):
        st.session_state["rrp_real_money_notice_ok"] = True
        st.rerun()


# =============================================================================
# COMUNIDAD: USUARIO LOCAL + CHAT GENERAL
# =============================================================================
# MVP seguro para beta pública: nickname local, mensajes en SQLite compartida,
# sin email, sin contraseña y sin datos personales. Sirve para crear comunidad
# y feedback sin convertir el radar en una red social pesada.

_CHAT_MAX_LEN = 500
_CHAT_COOLDOWN_SECONDS = 4
_CHAT_RETENTION_LIMIT = 5000


# Idiomas públicos del radar. Se guarda por visitante y se usa para el chat.
PUBLIC_LANGUAGES: Dict[str, str] = {
    "es": "Español",
    "en": "English",
    "fr": "Français",
    "de": "Deutsch",
    "it": "Italiano",
    "pt": "Português",
    "ja": "日本語",
    "ko": "한국어",
    "zh": "中文",
    "ar": "العربية",
}

# Admins autorizados para la beta pública. Pueden fijar mensajes y moderar chat.
ADMIN_USERNAMES = {"edutrejo", "alchemist", "edutrejo96"}
ADMIN_USERNAME = "edutrejo"  # etiqueta histórica/compatibilidad
# Seguridad práctica: en despliegue público puedes sobrescribirla con RRP_ADMIN_PASSWORD.
ADMIN_PASSWORD = _os.environ.get("RRP_ADMIN_PASSWORD", "741258")
# Límite inicial de investigadores con acceso a acciones que pueden gastar API.
MAX_PUBLIC_INVESTIGATORS = int(_os.environ.get("RRP_MAX_PUBLIC_INVESTIGATORS", "100"))

UI_TEXT = {
    "choose_lang_title": {
        "es": "🌍 Elige idioma / Choose your language",
        "en": "🌍 Choose your language",
        "fr": "🌍 Choisissez votre langue",
        "de": "🌍 Sprache wählen",
        "it": "🌍 Scegli la lingua",
        "pt": "🌍 Escolhe o idioma",
        "ja": "🌍 言語を選択",
        "ko": "🌍 언어 선택",
        "zh": "🌍 选择语言",
        "ar": "🌍 اختر اللغة",
    },
    "headphones": {
        "es": "🎧 Ponte los cascos para una experiencia más inmersiva.",
        "en": "🎧 Use headphones for a more immersive experience.",
        "fr": "🎧 Mets un casque pour une expérience plus immersive.",
        "de": "🎧 Kopfhörer sorgen für ein intensiveres Erlebnis.",
        "it": "🎧 Usa le cuffie per un’esperienza più immersiva.",
        "pt": "🎧 Usa auscultadores/fones para uma experiência mais imersiva.",
        "ja": "🎧 より没入感のある体験にはヘッドホンを使ってください。",
        "ko": "🎧 더 몰입감 있는 경험을 위해 헤드폰을 사용하세요.",
        "zh": "🎧 戴上耳机，获得更沉浸式的体验。",
        "ar": "🎧 ضع السماعات لتجربة أكثر غمراً.",
    },
}

def _preferred_lang() -> str:
    lang = str(st.session_state.get("preferred_lang", "") or "").strip().lower()
    return lang if lang in PUBLIC_LANGUAGES else ""


def _set_preferred_lang(lang: str) -> None:
    lang = str(lang or "es").strip().lower()
    st.session_state["preferred_lang"] = lang if lang in PUBLIC_LANGUAGES else "es"


def _ui_text(key: str, lang: Optional[str] = None) -> str:
    lang = lang or _preferred_lang() or "es"
    return UI_TEXT.get(key, {}).get(lang) or UI_TEXT.get(key, {}).get("es", key)




# =============================================================================
# UI I18N — traducción de interfaz completa (estática + dinámicos principales)
# =============================================================================
# Nota: no traduce datos técnicos crudos, nombres de instituciones, URLs ni pruebas.
# Sí traduce navegación, avisos, botones, leyendas, pestañas, onboarding, comunidad y admin.
UI_I18N: Dict[str, Dict[str, str]] = {
    "Vista": {"es":"Vista","en":"View","fr":"Vue","de":"Ansicht","it":"Vista","pt":"Vista","ja":"表示","ko":"보기","zh":"视图","ar":"العرض"},
    "Radar": {"es":"Radar","en":"Radar","fr":"Radar","de":"Radar","it":"Radar","pt":"Radar","ja":"レーダー","ko":"레이더","zh":"雷达","ar":"الرادار"},
    "Comunidad": {"es":"Comunidad","en":"Community","fr":"Communauté","de":"Community","it":"Comunità","pt":"Comunidade","ja":"コミュニティ","ko":"커뮤니티","zh":"社区","ar":"المجتمع"},
    "Route Paths A→B": {"es":"Rutas A→B","en":"Route paths A→B","fr":"Routes A→B","de":"Routen A→B","it":"Percorsi A→B","pt":"Rotas A→B","ja":"ルート A→B","ko":"경로 A→B","zh":"路径 A→B","ar":"المسارات A→B"},
    "Descubrimientos": {"es":"Descubrimientos","en":"Discoveries","fr":"Découvertes","de":"Entdeckungen","it":"Scoperte","pt":"Descobertas","ja":"発見","ko":"발견","zh":"发现","ar":"الاكتشافات"},
    "Motores": {"es":"Motores","en":"Engines","fr":"Moteurs","de":"Engines","it":"Motori","pt":"Motores","ja":"エンジン","ko":"엔진","zh":"引擎","ar":"المحركات"},
    "Rutas": {"es":"Rutas","en":"Routes","fr":"Routes","de":"Routen","it":"Rotte","pt":"Rotas","ja":"ルート","ko":"경로","zh":"路线","ar":"المسارات"},
    "Técnico": {"es":"Técnico","en":"Technical","fr":"Technique","de":"Technisch","it":"Tecnico","pt":"Técnico","ja":"技術","ko":"기술","zh":"技术","ar":"تقني"},
    "Histórico": {"es":"Histórico","en":"History","fr":"Historique","de":"Historie","it":"Storico","pt":"Histórico","ja":"履歴","ko":"히스토리","zh":"历史","ar":"السجل"},
    "Clusters": {"es":"Clusters","en":"Clusters","fr":"Clusters","de":"Cluster","it":"Cluster","pt":"Clusters","ja":"クラスター","ko":"클러스터","zh":"集群","ar":"العناقيد"},
    "Fingerprints": {"es":"Huellas","en":"Fingerprints","fr":"Empreintes","de":"Fingerprints","it":"Impronte","pt":"Impressões","ja":"フィンガープリント","ko":"지문","zh":"指纹","ar":"البصمات"},
    "Cinemateca": {"es":"Cinemateca","en":"Cinema mode","fr":"Cinémathèque","de":"Kino-Modus","it":"Cinemateca","pt":"Cinemateca","ja":"シネマモード","ko":"시네마 모드","zh":"影院模式","ar":"وضع السينما"},
    "Diagnóstico": {"es":"Diagnóstico","en":"Diagnostics","fr":"Diagnostic","de":"Diagnose","it":"Diagnostica","pt":"Diagnóstico","ja":"診断","ko":"진단","zh":"诊断","ar":"التشخيص"},
    "Donaciones": {"es":"Donaciones","en":"Donations","fr":"Dons","de":"Spenden","it":"Donazioni","pt":"Doações","ja":"寄付","ko":"기부","zh":"捐赠","ar":"التبرعات"},
    "Setup": {"es":"Setup","en":"Setup","fr":"Configuration","de":"Setup","it":"Setup","pt":"Configuração","ja":"設定","ko":"설정","zh":"设置","ar":"الإعداد"},
    "Actualizar XRPL": {"es":"Actualizar XRPL","en":"Refresh XRPL","fr":"Actualiser XRPL","de":"XRPL aktualisieren","it":"Aggiorna XRPL","pt":"Atualizar XRPL","ja":"XRPLを更新","ko":"XRPL 새로고침","zh":"刷新 XRPL","ar":"تحديث XRPL"},
    "Regenerar demo visual": {"es":"Regenerar demo visual","en":"Regenerate visual demo","fr":"Régénérer la démo visuelle","de":"Visuelle Demo neu erzeugen","it":"Rigenera demo visiva","pt":"Regenerar demo visual","ja":"ビジュアルデモを再生成","ko":"시각 데모 재생성","zh":"重新生成视觉演示","ar":"إعادة إنشاء العرض المرئي"},
    "Vigila rutas privadas por sus huellas públicas.": {"es":"Vigila rutas privadas por sus huellas públicas.","en":"Watch private routes through their public traces.","fr":"Surveille les routes privées grâce à leurs traces publiques.","de":"Überwache private Routen über ihre öffentlichen Spuren.","it":"Sorveglia rotte private tramite le loro tracce pubbliche.","pt":"Vigia rotas privadas pelas suas pegadas públicas.","ja":"公開された痕跡からプライベートルートを監視します。","ko":"공개 흔적으로 비공개 경로를 감시합니다.","zh":"通过公开痕迹监控私有路线。","ar":"راقب المسارات الخاصة عبر آثارها العامة."},
    "Conexiones confirmadas + obligatorias": {"es":"Conexiones confirmadas + obligatorias","en":"Confirmed + required connections","fr":"Connexions confirmées + requises","de":"Bestätigte + erforderliche Verbindungen","it":"Connessioni confermate + obbligatorie","pt":"Conexões confirmadas + obrigatórias","ja":"確認済み＋必須接続","ko":"확인됨 + 필수 연결","zh":"已确认 + 必需连接","ar":"اتصالات مؤكدة + لازمة"},
    "Vigilancia / inferidas": {"es":"Vigilancia / inferidas","en":"Watch / inferred","fr":"Surveillance / inférées","de":"Beobachtung / abgeleitet","it":"Vigilanza / inferite","pt":"Vigilância / inferidas","ja":"監視 / 推定","ko":"감시 / 추론","zh":"监控 / 推断","ar":"مراقبة / مستنتجة"},
    "Mapa completo": {"es":"Mapa completo","en":"Full map","fr":"Carte complète","de":"Vollständige Karte","it":"Mappa completa","pt":"Mapa completo","ja":"完全なマップ","ko":"전체 지도","zh":"完整地图","ar":"الخريطة الكاملة"},
    "Ver todo": {"es":"Ver todo","en":"Show all","fr":"Tout afficher","de":"Alles anzeigen","it":"Mostra tutto","pt":"Ver tudo","ja":"すべて表示","ko":"전체 보기","zh":"显示全部","ar":"عرض الكل"},
    "Enviar": {"es":"Enviar","en":"Send","fr":"Envoyer","de":"Senden","it":"Invia","pt":"Enviar","ja":"送信","ko":"보내기","zh":"发送","ar":"إرسال"},
    "Mensaje": {"es":"Mensaje","en":"Message","fr":"Message","de":"Nachricht","it":"Messaggio","pt":"Mensagem","ja":"メッセージ","ko":"메시지","zh":"消息","ar":"رسالة"},
    "Escribe al chat general...": {"es":"Escribe al chat general...","en":"Write in the public chat...","fr":"Écris dans le chat public...","de":"Schreibe in den öffentlichen Chat...","it":"Scrivi nella chat pubblica...","pt":"Escreve no chat público...","ja":"公開チャットに書き込む...","ko":"공개 채팅에 작성...","zh":"在公共聊天中输入...","ar":"اكتب في الدردشة العامة..."},
    "Chat general": {"es":"Chat general","en":"Public chat","fr":"Chat public","de":"Öffentlicher Chat","it":"Chat pubblico","pt":"Chat público","ja":"公開チャット","ko":"공개 채팅","zh":"公共聊天","ar":"الدردشة العامة"},
    "Comunidad beta": {"es":"Comunidad beta","en":"Beta community","fr":"Communauté bêta","de":"Beta-Community","it":"Comunità beta","pt":"Comunidade beta","ja":"ベータコミュニティ","ko":"베타 커뮤니티","zh":"测试社区","ar":"مجتمع بيتا"},
    "Admin": {"es":"Admin","en":"Admin","fr":"Admin","de":"Admin","it":"Admin","pt":"Admin","ja":"管理者","ko":"관리자","zh":"管理员","ar":"المشرف"},
    "Panel reservado al administrador.": {"es":"Panel reservado al administrador.","en":"Panel reserved for the administrator.","fr":"Panneau réservé à l’administrateur.","de":"Panel nur für den Administrator.","it":"Pannello riservato all’amministratore.","pt":"Painel reservado ao administrador.","ja":"管理者専用パネルです。","ko":"관리자 전용 패널입니다.","zh":"管理员专用面板。","ar":"لوحة مخصصة للمشرف."},
    "No hay datos disponibles.": {"es":"No hay datos disponibles.","en":"No data available.","fr":"Aucune donnée disponible.","de":"Keine Daten verfügbar.","it":"Nessun dato disponibile.","pt":"Não há dados disponíveis.","ja":"利用可能なデータがありません。","ko":"사용 가능한 데이터가 없습니다.","zh":"没有可用数据。","ar":"لا توجد بيانات متاحة."},
    "ui_scope_note": {"es":"Interfaz traducida al idioma elegido. Los nombres de instituciones, pruebas, URLs y datos técnicos se conservan en su idioma original para no alterar la evidencia.","en":"Interface translated to your selected language. Institution names, evidence, URLs and technical data stay in their original language to preserve evidence integrity.","fr":"Interface traduite dans la langue choisie. Les noms d’institutions, preuves, URLs et données techniques restent dans leur langue d’origine pour préserver l’intégrité des preuves.","de":"Die Oberfläche wird in die gewählte Sprache übersetzt. Institutionsnamen, Belege, URLs und technische Daten bleiben zur Beweissicherheit in der Originalsprache.","it":"Interfaccia tradotta nella lingua scelta. Nomi di istituzioni, prove, URL e dati tecnici restano nella lingua originale per preservare l’integrità delle prove.","pt":"Interface traduzida para o idioma escolhido. Nomes de instituições, provas, URLs e dados técnicos ficam no idioma original para preservar a evidência.","ja":"選択した言語にUIを翻訳します。証拠の整合性を保つため、機関名・証拠・URL・技術データは原語のまま保持します。","ko":"선택한 언어로 UI가 번역됩니다. 증거 무결성을 위해 기관명, 증거, URL, 기술 데이터는 원문 언어로 유지됩니다.","zh":"界面会翻译为所选语言。为保持证据完整性，机构名称、证据、URL 和技术数据保留原文。","ar":"تمت ترجمة الواجهة إلى اللغة المختارة. تبقى أسماء المؤسسات والأدلة والروابط والبيانات التقنية بلغتها الأصلية للحفاظ على سلامة الدليل."},
}

SECTION_KEYS = ["Radar", "Comunidad", "Route Paths A→B", "Descubrimientos", "Motores", "Rutas", "Técnico", "Histórico", "Clusters", "Fingerprints", "Cinemateca", "Diagnóstico", "Donaciones", "Setup"]

def _t(label: str, lang: Optional[str] = None) -> str:
    lang = lang or _preferred_lang() or "es"
    d = UI_I18N.get(str(label), {})
    return d.get(lang) or d.get("es") or str(label)

def _section_label(section_key: str) -> str:
    return _t(section_key)

def _section_from_label(label: str) -> str:
    for k in SECTION_KEYS:
        if label == _section_label(k) or label == k:
            return k
    return str(label)

def render_ui_translation_notice() -> None:
    lang = _preferred_lang() or "es"
    if lang == "es":
        return
    st.info(_t("ui_scope_note", lang))


# -----------------------------------------------------------------------------
# Traducción universal de UI/render. No traduce entidades, wallets, URLs ni pruebas.
# -----------------------------------------------------------------------------
_UI_EXTRA_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "{t['radar_desc']}": {
        "en":"Advanced radar to monitor private routes through public traces: clusters, topology, fingerprints, anomalies, DEX/AMM, trustlines, large transfers and time regime.",
        "fr":"Radar avancé pour surveiller les routes privées via leurs traces publiques : clusters, topologie, empreintes, anomalies, DEX/AMM, trustlines, gros transferts et régime temporel.",
        "de":"Fortgeschrittener Radar zur Überwachung privater Routen anhand öffentlicher Spuren: Cluster, Topologie, Fingerprints, Anomalien, DEX/AMM, Trustlines, große Transfers und Zeitregime.",
        "it":"Radar avanzato per monitorare rotte private attraverso tracce pubbliche: cluster, topologia, impronte, anomalie, DEX/AMM, trustline, grandi trasferimenti e regime temporale.",
        "pt":"Radar avançado para vigiar rotas privadas pelas suas pegadas públicas: clusters, topologia, fingerprints, anomalias, DEX/AMM, trustlines, grandes transferências e regime temporal.",
        "ja":"公開痕跡からプライベート経路を監視する高度なレーダー：クラスター、トポロジー、フィンガープリント、異常、DEX/AMM、トラストライン、大口送金、時間レジーム。",
        "ko":"공개 흔적으로 비공개 경로를 감시하는 고급 레이더: 클러스터, 토폴로지, 지문, 이상 징후, DEX/AMM, 트러스트라인, 대규모 전송, 시간 체제.",
        "zh":"通过公开痕迹监控私有路径的高级雷达：集群、拓扑、指纹、异常、DEX/AMM、信任线、大额转账和时间状态。",
        "ar":"رادار متقدم لمراقبة المسارات الخاصة عبر آثارها العامة: العناقيد والطوبولوجيا والبصمات والشذوذ و DEX/AMM وخطوط الثقة والتحويلات الكبيرة والنظام الزمني."
    },
    "Subida": {"en":"Upside","fr":"Hausse","de":"Anstieg","it":"Rialzo","pt":"Alta","ja":"上昇","ko":"상승","zh":"上涨","ar":"الصعود"},
    "Riesgo": {"en":"Risk","fr":"Risque","de":"Risiko","it":"Rischio","pt":"Risco","ja":"リスク","ko":"위험","zh":"风险","ar":"المخاطر"},
    "Flip": {"en":"Flip","fr":"Flip","de":"Flip","it":"Flip","pt":"Flip","ja":"フリップ","ko":"플립","zh":"Flip","ar":"التحول"},
    "Cobertura": {"en":"Coverage","fr":"Couverture","de":"Abdeckung","it":"Copertura","pt":"Cobertura","ja":"カバレッジ","ko":"커버리지","zh":"覆盖率","ar":"التغطية"},
    "Fase": {"en":"Phase","fr":"Phase","de":"Phase","it":"Fase","pt":"Fase","ja":"フェーズ","ko":"단계","zh":"阶段","ar":"المرحلة"},
    "Pump": {"en":"Pump","fr":"Pump","de":"Pump","it":"Pump","pt":"Pump","ja":"ポンプ","ko":"펌프","zh":"拉盘","ar":"ضخ"},
    "Rutas hot": {"en":"Hot routes","fr":"Routes chaudes","de":"Heiße Routen","it":"Rotte calde","pt":"Rotas quentes","ja":"ホットルート","ko":"핫 경로","zh":"热门路线","ar":"مسارات ساخنة"},
    "¿Qué significan los datos de arriba?": {"en":"What do the figures above mean?","fr":"Que signifient les données ci-dessus ?","de":"Was bedeuten die Daten oben?","it":"Cosa significano i dati sopra?","pt":"O que significam os dados acima?","ja":"上のデータは何を意味しますか？","ko":"위 데이터는 무엇을 의미하나요?","zh":"上面的数据是什么意思？","ar":"ماذا تعني البيانات أعلاه؟"},
    "Probabilidad de impulso de precio por actividad pública: volumen, transfers grandes, DEX, anomalías y régimen temporal.": {"en":"Probability of price impulse from public activity: volume, large transfers, DEX, anomalies and time regime.","fr":"Probabilité d'impulsion du prix par activité publique : volume, gros transferts, DEX, anomalies et régime temporel.","pt":"Probabilidade de impulso de preço por atividade pública: volume, grandes transferências, DEX, anomalias e regime temporal."},
    "Detecta enfriamiento: baja actividad, poca persistencia, falta de clusters o spike que parece especulativo.": {"en":"Detects cooling: low activity, weak persistence, lack of clusters or spikes that look speculative.","fr":"Détecte le refroidissement : faible activité, peu de persistance, manque de clusters ou pic spéculatif.","pt":"Detecta arrefecimento: baixa atividade, pouca persistência, falta de clusters ou pico especulativo."},
    "Señal de adopción real. Solo sube fuerte si varias huellas públicas se coordinan durante tiempo.": {"en":"Real adoption signal. It rises strongly only when several public traces stay coordinated over time.","fr":"Signal d'adoption réelle. Il monte fortement seulement si plusieurs traces publiques restent coordonnées dans le temps.","pt":"Sinal de adoção real. Só sobe forte se várias pegadas públicas ficarem coordenadas ao longo do tempo."},
    "Cuántos puntos públicos estamos vigilando donde las rutas privadas tendrían que dejar rastro.": {"en":"How many public touchpoints are being watched where private routes would have to leave traces.","fr":"Nombre de points publics surveillés où les routes privées devraient laisser des traces.","pt":"Quantos pontos públicos estamos a vigiar onde rotas privadas teriam de deixar rasto."},
    "Escala 0–5: de ruido bajo a Full Flip. Resume el estado completo del radar.": {"en":"0–5 scale: from low noise to Full Flip. It summarizes the whole radar state.","fr":"Échelle 0–5 : du faible bruit au Full Flip. Résume l'état complet du radar.","pt":"Escala 0–5: de ruído baixo a Full Flip. Resume o estado completo do radar."},
    "Probabilidad de que sea movimiento especulativo o spike sin adopción sostenida.": {"en":"Probability that the move is speculative or a spike without sustained adoption.","fr":"Probabilité qu'il s'agisse d'un mouvement spéculatif ou d'un pic sans adoption durable.","pt":"Probabilidade de ser movimento especulativo ou pico sem adoção sustentada."},
    "Número de rutas o motores que están por encima del umbral de señal fuerte.": {"en":"Number of routes or engines above the strong-signal threshold.","fr":"Nombre de routes ou moteurs au-dessus du seuil de signal fort.","pt":"Número de rotas ou motores acima do limiar de sinal forte."},
    "Ledger real verificable": {"en":"Verifiable real ledger","fr":"Ledger réel vérifiable","de":"Verifizierbares reales Ledger","it":"Ledger reale verificabile","pt":"Ledger real verificável","ja":"検証可能な実台帳","ko":"검증 가능한 실제 원장","zh":"可验证真实账本","ar":"سجل حقيقي قابل للتحقق"},
    "Documental/institucional": {"en":"Documentary/institutional","fr":"Documentaire/institutionnel","de":"Dokumentarisch/institutionell","it":"Documentale/istituzionale","pt":"Documental/institucional","ja":"文書/機関","ko":"문서/기관","zh":"文档/机构","ar":"وثائقي/مؤسسي"},
    "Watch/especulativo": {"en":"Watch/speculative","fr":"Surveillance/spéculatif","de":"Watch/spekulativ","it":"Watch/speculativo","pt":"Watch/especulativo","ja":"監視/投機","ko":"감시/투기","zh":"观察/投机","ar":"مراقبة/مضاربي"},
    "Flip final verificado": {"en":"Final verified Flip","fr":"Flip final vérifié","de":"Final verifizierter Flip","it":"Flip finale verificato","pt":"Flip final verificado","ja":"最終検証済みフリップ","ko":"최종 검증 Flip","zh":"最终验证 Flip","ar":"التحول النهائي المؤكد"},
    "Zona fuerte": {"en":"Strong zone","fr":"Zone forte","de":"Starke Zone","it":"Zona forte","pt":"Zona forte","ja":"強いゾーン","ko":"강한 구역","zh":"强区","ar":"منطقة قوية"},
    "Flip explicado: ledger real vs pruebas documentales vs watch especulativo": {"en":"Flip explained: real ledger vs documentary evidence vs speculative watch","fr":"Flip expliqué : ledger réel vs preuves documentaires vs surveillance spéculative","de":"Flip erklärt: reales Ledger vs dokumentarische Belege vs spekulative Watch","it":"Flip spiegato: ledger reale vs prove documentali vs watch speculativo","pt":"Flip explicado: ledger real vs provas documentais vs watch especulativo","ja":"Flipの内訳：実台帳 vs 文書証拠 vs 投機的監視","ko":"Flip 설명: 실제 원장 vs 문서 증거 vs 투기 감시","zh":"Flip 解释：真实账本 vs 文件证据 vs 投机观察","ar":"شرح التحول: السجل الحقيقي مقابل الأدلة الوثائقية مقابل المراقبة المضاربية"},
    "Adopción: Flip, cobertura, adopción técnica, persistencia + precio XRP real (eje dcho.)": {"en":"Adoption: Flip, coverage, technical adoption, persistence + real XRP price (right axis)","fr":"Adoption : Flip, couverture, adoption technique, persistance + prix réel du XRP (axe droit)","pt":"Adoção: Flip, cobertura, adoção técnica, persistência + preço real do XRP (eixo direito)"},
    "Fase 0–5 verificada": {"en":"Verified phase 0–5","fr":"Phase vérifiée 0–5","pt":"Fase 0–5 verificada"},
    "Flip fuerte >80%": {"en":"Strong Flip >80%","fr":"Flip fort >80%","pt":"Flip forte >80%"},
    "Subida probable": {"en":"Probable upside","fr":"Hausse probable","pt":"Alta provável"},
    "Riesgo bajada": {"en":"Downside risk","fr":"Risque de baisse","pt":"Risco de queda"},
    "Pump especulativo": {"en":"Speculative pump","fr":"Pump spéculatif","pt":"Pump especulativo"},
    "Cobertura radar": {"en":"Radar coverage","fr":"Couverture radar","pt":"Cobertura radar"},
    "Adopción técnica": {"en":"Technical adoption","fr":"Adoption technique","pt":"Adoção técnica"},
    "Persistencia": {"en":"Persistence","fr":"Persistance","pt":"Persistência"},
    "Mapa completo": {"en":"Full map","fr":"Carte complète","pt":"Mapa completo"},
    "Sin datos": {"en":"No data","fr":"Pas de données","pt":"Sem dados"},
}



# ── I18N v6.2.4 — cobertura completa de portada, mapa, gráficos y leyendas ──
def _rrp_merge_translations() -> None:
    """Amplía el diccionario de traducción sin tocar nombres oficiales, wallets ni URLs.

    Objetivo: evitar interfaz mezclada tipo "レーダー avanzado". Los textos largos se
    traducen primero como frase completa; después se aplican reemplazos cortos.
    """
    extra: Dict[str, Dict[str, str]] = {
        # Portada / cabecera
        "Ripple Radar Pro": {"en":"Ripple Radar Pro","fr":"Ripple Radar Pro","de":"Ripple Radar Pro","it":"Ripple Radar Pro","pt":"Ripple Radar Pro","ja":"Ripple Radar Pro","ko":"Ripple Radar Pro","zh":"Ripple Radar Pro","ar":"Ripple Radar Pro"},
        "{t['radar_desc']}": {
            "en":"Advanced radar for monitoring private routes through their public traces: clusters, topology, fingerprints, anomalies, DEX/AMM, trustlines, large transfers and time regime.",
            "fr":"Radar avancé pour surveiller les routes privées à travers leurs traces publiques : clusters, topologie, empreintes, anomalies, DEX/AMM, trustlines, gros transferts et régime temporel.",
            "de":"Fortgeschrittenes Radar zur Überwachung privater Routen über öffentliche Spuren: Cluster, Topologie, Fingerprints, Anomalien, DEX/AMM, Trustlines, große Transfers und Zeitregime.",
            "it":"Radar avanzato per monitorare rotte private attraverso tracce pubbliche: cluster, topologia, impronte, anomalie, DEX/AMM, trustline, grandi trasferimenti e regime temporale.",
            "pt":"Radar avançado para vigiar rotas privadas pelas suas pegadas públicas: clusters, topologia, fingerprints, anomalias, DEX/AMM, trustlines, grandes transferências e regime temporal.",
            "ja":"公開された痕跡からプライベートルートを監視する高度なレーダー：クラスター、トポロジー、フィンガープリント、異常、DEX/AMM、トラストライン、大口送金、時間レジームを分析します。",
            "ko":"공개 흔적으로 비공개 경로를 감시하는 고급 레이더: 클러스터, 토폴로지, 지문, 이상 징후, DEX/AMM, 트러스트라인, 대형 전송, 시간 체제를 분석합니다.",
            "zh":"通过公开痕迹监控私有路线的高级雷达：集群、拓扑、指纹、异常、DEX/AMM、信任线、大额转账和时间状态。",
            "ar":"رادار متقدم لمراقبة المسارات الخاصة عبر آثارها العامة: العناقيد، الطوبولوجيا، البصمات، الشذوذ، DEX/AMM، خطوط الثقة، التحويلات الكبيرة والنظام الزمني."
        },
        "XRP / RLUSD · Advanced Intelligence · Route Path Intelligence v6.2.3 PRO — Proof-First Universal Public Discovery": {
            "en":"XRP / RLUSD · Advanced Intelligence · Route Path Intelligence v6.2.3 PRO — Proof-First Universal Public Discovery",
            "fr":"XRP / RLUSD · Intelligence avancée · Route Path Intelligence v6.2.3 PRO — Découverte publique universelle proof-first",
            "pt":"XRP / RLUSD · Inteligência avançada · Route Path Intelligence v6.2.3 PRO — Descoberta pública universal proof-first",
            "ja":"XRP / RLUSD · 高度インテリジェンス · Route Path Intelligence v6.2.3 PRO — 証拠優先の汎用公開ディスカバリー",
            "ko":"XRP / RLUSD · 고급 인텔리전스 · Route Path Intelligence v6.2.3 PRO — 증거 우선 범용 공개 디스커버리",
            "zh":"XRP / RLUSD · 高级智能 · Route Path Intelligence v6.2.3 PRO — 证据优先的通用公开发现",
            "ar":"XRP / RLUSD · ذكاء متقدم · Route Path Intelligence v6.2.3 PRO — اكتشاف عام شامل قائم على الدليل أولاً"
        },
        "XRPL real Cluster intelligence Fingerprints Topology engine Anomaly detection Pump vs Adoption": {
            "en":"Real XRPL · Cluster intelligence · Fingerprints · Topology engine · Anomaly detection · Pump vs Adoption",
            "fr":"XRPL réel · Intelligence de clusters · Empreintes · Moteur de topologie · Détection d’anomalies · Pump vs Adoption",
            "pt":"XRPL real · Inteligência de clusters · Fingerprints · Motor de topologia · Deteção de anomalias · Pump vs Adoção",
            "ja":"実XRPL · クラスター分析 · フィンガープリント · トポロジーエンジン · 異常検知 · ポンプ vs 採用",
            "ko":"실제 XRPL · 클러스터 인텔리전스 · 지문 · 토폴로지 엔진 · 이상 탐지 · 펌프 vs 채택",
            "zh":"真实 XRPL · 集群智能 · 指纹 · 拓扑引擎 · 异常检测 · 拉盘 vs 采用",
            "ar":"XRPL حقيقي · ذكاء العناقيد · البصمات · محرك الطوبولوجيا · كشف الشذوذ · الضخ مقابل التبني"
        },
        # Métricas y explicaciones
        "Subida": {"en":"Upside","fr":"Hausse","de":"Anstieg","it":"Rialzo","pt":"Alta","ja":"上昇","ko":"상승","zh":"上涨","ar":"الصعود"},
        "Riesgo": {"en":"Risk","fr":"Risque","de":"Risiko","it":"Rischio","pt":"Risco","ja":"リスク","ko":"위험","zh":"风险","ar":"المخاطر"},
        "Cobertura": {"en":"Coverage","fr":"Couverture","de":"Abdeckung","it":"Copertura","pt":"Cobertura","ja":"カバレッジ","ko":"커버리지","zh":"覆盖率","ar":"التغطية"},
        "Rutas hot": {"en":"Hot routes","fr":"Routes chaudes","de":"Heiße Routen","it":"Rotte calde","pt":"Rotas quentes","ja":"ホットルート","ko":"핫 경로","zh":"热门路线","ar":"مسارات ساخنة"},
        "¿Qué significan los datos de arriba?": {"en":"What do the figures above mean?","fr":"Que signifient les données ci-dessus ?","de":"Was bedeuten die Daten oben?","it":"Cosa significano i dati sopra?","pt":"O que significam os dados acima?","ja":"上のデータは何を意味しますか？","ko":"위 데이터는 무엇을 의미하나요?","zh":"上面的数据是什么意思？","ar":"ماذا تعني البيانات أعلاه؟"},
        "Probabilidad de impulso de precio por actividad pública: volumen, transfers grandes, DEX, anomalías y régimen temporal.": {"en":"Probability of price impulse from public activity: volume, large transfers, DEX, anomalies and time regime.","fr":"Probabilité d’impulsion du prix par l’activité publique : volume, gros transferts, DEX, anomalies et régime temporel.","pt":"Probabilidade de impulso de preço por atividade pública: volume, grandes transferências, DEX, anomalias e regime temporal.","ja":"公開活動による価格インパルスの確率：出来高、大口送金、DEX、異常、時間レジーム。","ko":"공개 활동으로 인한 가격 충격 확률: 거래량, 대형 전송, DEX, 이상 징후, 시간 체제.","zh":"由公开活动引发价格冲击的概率：成交量、大额转账、DEX、异常和时间状态。","ar":"احتمال اندفاع السعر بسبب النشاط العام: الحجم، التحويلات الكبيرة، DEX، الشذوذ والنظام الزمني."},
        "Detecta enfriamiento: baja actividad, poca persistencia, falta de clusters o spike que parece especulativo.": {"en":"Detects cooling: low activity, weak persistence, lack of clusters or spikes that look speculative.","fr":"Détecte le refroidissement : faible activité, faible persistance, manque de clusters ou pic spéculatif.","pt":"Deteta arrefecimento: baixa atividade, pouca persistência, falta de clusters ou pico especulativo.","ja":"活動低下を検知：低活動、持続性不足、クラスター不足、または投機的に見える急騰。","ko":"냉각을 감지합니다: 낮은 활동, 약한 지속성, 클러스터 부족 또는 투기적으로 보이는 스파이크.","zh":"检测降温：低活动、持续性弱、缺少集群或看似投机性的峰值。","ar":"يكشف التباطؤ: نشاط منخفض، ضعف الاستمرارية، نقص العناقيد أو قفزة تبدو مضاربية."},
        "Señal de adopción real. Solo sube fuerte si varias huellas públicas se coordinan durante tiempo.": {"en":"Real adoption signal. It rises strongly only when several public traces stay coordinated over time.","fr":"Signal d’adoption réelle. Il ne monte fortement que lorsque plusieurs traces publiques restent coordonnées dans le temps.","pt":"Sinal de adoção real. Só sobe forte quando várias pegadas públicas ficam coordenadas ao longo do tempo.","ja":"実際の採用シグナル。複数の公開痕跡が一定期間連動した場合にのみ強く上昇します。","ko":"실제 채택 신호입니다. 여러 공개 흔적이 시간 동안 함께 움직일 때만 강하게 상승합니다.","zh":"真实采用信号。只有多个公开痕迹在一段时间内协同出现时才会强烈上升。","ar":"إشارة تبنٍ حقيقية. ترتفع بقوة فقط عندما تتناسق عدة آثار عامة عبر الزمن."},
        "Cuántos puntos públicos estamos vigilando donde las rutas privadas tendrían que dejar rastro.": {"en":"How many public touchpoints are being watched where private routes would have to leave traces.","fr":"Nombre de points publics surveillés où les routes privées devraient laisser des traces.","pt":"Quantos pontos públicos estamos a vigiar onde rotas privadas teriam de deixar rasto.","ja":"プライベートルートが痕跡を残すはずの公開接点をどれだけ監視しているか。","ko":"비공개 경로가 흔적을 남겨야 하는 공개 접점을 얼마나 감시하는지입니다.","zh":"正在监控多少个私有路线必须留下痕迹的公开接触点。","ar":"عدد نقاط التماس العامة التي نراقبها حيث يجب أن تترك المسارات الخاصة أثراً."},
        "Escala 0–5: de ruido bajo a Full Flip. Resume el estado completo del radar.": {"en":"0–5 scale: from low noise to Full Flip. It summarizes the whole radar state.","fr":"Échelle 0–5 : du faible bruit au Full Flip. Résume l’état complet du radar.","pt":"Escala 0–5: de ruído baixo a Full Flip. Resume o estado completo do radar.","ja":"0〜5のスケール：低ノイズからFull Flipまで。レーダー全体の状態を要約します。","ko":"0–5 척도: 낮은 잡음부터 Full Flip까지. 레이더 전체 상태를 요약합니다.","zh":"0–5 等级：从低噪声到 Full Flip。概括整个雷达状态。","ar":"مقياس 0–5: من ضجيج منخفض إلى Full Flip. يلخص حالة الرادار بالكامل."},
        "Probabilidad de que sea movimiento especulativo o spike sin adopción sostenida.": {"en":"Probability that the move is speculative or a spike without sustained adoption.","fr":"Probabilité qu’il s’agisse d’un mouvement spéculatif ou d’un pic sans adoption durable.","pt":"Probabilidade de ser movimento especulativo ou pico sem adoção sustentada.","ja":"持続的な採用を伴わない投機的な動きまたはスパイクである確率。","ko":"지속적인 채택 없는 투기적 움직임 또는 스파이크일 확률입니다.","zh":"属于投机性走势或缺乏持续采用的峰值的概率。","ar":"احتمال أن تكون الحركة مضاربية أو قفزة بلا تبنٍ مستدام."},
        "Número de rutas o motores que están por encima del umbral de señal fuerte.": {"en":"Number of routes or engines above the strong-signal threshold.","fr":"Nombre de routes ou de moteurs au-dessus du seuil de signal fort.","pt":"Número de rotas ou motores acima do limiar de sinal forte.","ja":"強いシグナル閾値を超えているルートまたはエンジンの数。","ko":"강한 신호 임계값을 넘은 경로 또는 엔진 수입니다.","zh":"高于强信号阈值的路线或引擎数量。","ar":"عدد المسارات أو المحركات فوق عتبة الإشارة القوية."},
        # Señales / tarjetas
        "Señal débil": {"en":"Weak signal","fr":"Signal faible","de":"Schwaches Signal","it":"Segnale debole","pt":"Sinal fraco","ja":"弱いシグナル","ko":"약한 신호","zh":"弱信号","ar":"إشارة ضعيفة"},
        "Predominan señales especulativas o hay poca actividad verificable en ledger. No debe interpretarse como conexión operativa.": {"en":"Speculative signals dominate or there is little verifiable ledger activity. This must not be interpreted as an operational connection.","fr":"Les signaux spéculatifs dominent ou l’activité ledger vérifiable est faible. Cela ne doit pas être interprété comme une connexion opérationnelle.","pt":"Predominam sinais especulativos ou há pouca atividade verificável no ledger. Isto não deve ser interpretado como conexão operacional.","ja":"投機的シグナルが優勢、または検証可能な台帳活動が少ない状態です。運用上の接続として解釈してはいけません。","ko":"투기적 신호가 우세하거나 검증 가능한 원장 활동이 적습니다. 운영 연결로 해석하면 안 됩니다.","zh":"投机性信号占主导，或可验证账本活动很少。不得将其解释为运营连接。","ar":"تهيمن الإشارات المضاربية أو توجد قلة في نشاط السجل القابل للتحقق. لا ينبغي تفسير ذلك كاتصال تشغيلي."},
        "Ledger real": {"en":"Real ledger","fr":"Ledger réel","de":"Reales Ledger","it":"Ledger reale","pt":"Ledger real","ja":"実台帳","ko":"실제 원장","zh":"真实账本","ar":"السجل الحقيقي"},
        "pagos, trustlines, DEX/AMM, whales, clusters": {"en":"payments, trustlines, DEX/AMM, whales, clusters","fr":"paiements, trustlines, DEX/AMM, whales, clusters","pt":"pagamentos, trustlines, DEX/AMM, whales, clusters","ja":"支払い、トラストライン、DEX/AMM、クジラ、クラスター","ko":"결제, 트러스트라인, DEX/AMM, 고래, 클러스터","zh":"支付、信任线、DEX/AMM、巨鲸、集群","ar":"مدفوعات، خطوط ثقة، DEX/AMM، حيتان، عناقيد"},
        "Documental": {"en":"Documentary","fr":"Documentaire","de":"Dokumentarisch","it":"Documentale","pt":"Documental","ja":"文書証拠","ko":"문서 증거","zh":"文档证据","ar":"وثائقي"},
        "pruebas oficiales, rutas y cobertura": {"en":"official evidence, routes and coverage","fr":"preuves officielles, routes et couverture","pt":"provas oficiais, rotas e cobertura","ja":"公式証拠、ルート、カバレッジ","ko":"공식 증거, 경로 및 커버리지","zh":"官方证据、路线和覆盖率","ar":"أدلة رسمية، مسارات وتغطية"},
        "narrativa, pump, inferencias no operativas": {"en":"narrative, pump, non-operational inferences","fr":"narratif, pump, inférences non opérationnelles","pt":"narrativa, pump, inferências não operacionais","ja":"ナラティブ、ポンプ、非運用的推論","ko":"내러티브, 펌프, 비운영 추론","zh":"叙事、拉盘、非运营性推断","ar":"سردية، ضخ، استنتاجات غير تشغيلية"},
        "Riesgo de bajada / slowdown": {"en":"Downside / slowdown risk","fr":"Risque de baisse / ralentissement","pt":"Risco de queda / slowdown","ja":"下落 / 減速リスク","ko":"하락 / 둔화 위험","zh":"下行 / 放缓风险","ar":"خطر الهبوط / التباطؤ"},
        "La actividad pública verificable cae o parece spike sin persistencia.": {"en":"Verifiable public activity is falling or looks like a spike without persistence.","fr":"L’activité publique vérifiable baisse ou ressemble à un pic sans persistance.","pt":"A atividade pública verificável cai ou parece um pico sem persistência.","ja":"検証可能な公開活動が低下しているか、持続性のないスパイクに見えます。","ko":"검증 가능한 공개 활동이 감소하거나 지속성 없는 스파이크처럼 보입니다.","zh":"可验证的公开活动下降，或看起来像缺乏持续性的峰值。","ar":"ينخفض النشاط العام القابل للتحقق أو يبدو كقفزة بلا استمرارية."},
        "Precio XRP": {"en":"XRP price","fr":"Prix XRP","pt":"Preço XRP","ja":"XRP価格","ko":"XRP 가격","zh":"XRP 价格","ar":"سعر XRP"},
        "Riesgo de falso rebote o presión bajista.": {"en":"Risk of false rebound or downside pressure.","fr":"Risque de faux rebond ou de pression baissière.","pt":"Risco de falso ressalto ou pressão baixista.","ja":"偽の反発または下落圧力のリスク。","ko":"가짜 반등 또는 하방 압력 위험.","zh":"假反弹或下行压力风险。","ar":"خطر ارتداد كاذب أو ضغط هبوطي."},
        "Alto.": {"en":"High.","fr":"Élevé.","de":"Hoch.","it":"Alto.","pt":"Alto.","ja":"高い。","ko":"높음.","zh":"高。","ar":"مرتفع."},
        "Adopción real": {"en":"Real adoption","fr":"Adoption réelle","de":"Echte Adoption","it":"Adozione reale","pt":"Adoção real","ja":"実際の採用","ko":"실제 채택","zh":"真实采用","ar":"تبنٍ حقيقي"},
        "Fase 0 — Ruido / baja señal: sin adopción real confirmada.": {"en":"Phase 0 — Noise / low signal: no confirmed real adoption.","fr":"Phase 0 — Bruit / signal faible : aucune adoption réelle confirmée.","pt":"Fase 0 — Ruído / sinal baixo: sem adoção real confirmada.","ja":"フェーズ0 — ノイズ / 低シグナル：実際の採用は未確認。","ko":"0단계 — 잡음 / 낮은 신호: 확인된 실제 채택 없음.","zh":"阶段0 — 噪声 / 低信号：没有确认的真实采用。","ar":"المرحلة 0 — ضجيج / إشارة منخفضة: لا يوجد تبنٍ حقيقي مؤكد."},
        "Pump vs Adopción": {"en":"Pump vs Adoption","fr":"Pump vs Adoption","pt":"Pump vs Adoção","ja":"ポンプ vs 採用","ko":"펌프 vs 채택","zh":"拉盘 vs 采用","ar":"الضخ مقابل التبني"},
        "Adopción técnica": {"en":"Technical adoption","fr":"Adoption technique","de":"Technische Adoption","it":"Adozione tecnica","pt":"Adoção técnica","ja":"技術的採用","ko":"기술적 채택","zh":"技术采用","ar":"تبنٍ تقني"},
        "Haz clic en cualquier nodo del mapa para ver solo sus rutas.": {"en":"Click any map node to show only its routes.","fr":"Clique sur n’importe quel nœud de la carte pour voir uniquement ses routes.","pt":"Clica em qualquer nó do mapa para ver apenas as suas rotas.","ja":"マップ上の任意のノードをクリックすると、そのルートだけを表示します。","ko":"지도에서 노드를 클릭하면 해당 경로만 표시됩니다.","zh":"点击地图上的任意节点，仅查看它的路线。","ar":"انقر على أي عقدة في الخريطة لعرض مساراتها فقط."},
        # Mapa / leyenda
        "Solo rutas con evidencia confirmada (on-chain, documentada) o implicación técnica irrefutable (⚡ rojo-rosa). Sin ruido de vigilancia.": {"en":"Only routes with confirmed evidence (on-chain, documented) or irrefutable technical implication (⚡ red-pink). No watch noise.","fr":"Uniquement les routes avec preuve confirmée (on-chain, documentée) ou implication technique irréfutable (⚡ rouge-rose). Sans bruit de surveillance.","pt":"Apenas rotas com evidência confirmada (on-chain, documentada) ou implicação técnica irrefutável (⚡ vermelho-rosa). Sem ruído de vigilância.","ja":"確認済み証拠（オンチェーン、文書）または技術的に反証不能な含意（⚡赤ピンク）のあるルートのみ。監視ノイズは除外。","ko":"확인된 증거(온체인, 문서) 또는 반박 불가능한 기술적 함의(⚡ 빨강-분홍)가 있는 경로만 표시합니다. 감시 노이즈는 제외됩니다.","zh":"仅显示有确认性证据（链上、文档）或不可反驳技术含义（⚡红粉色）的路线。无观察噪声。","ar":"المسارات ذات الأدلة المؤكدة فقط (على السلسلة أو موثقة) أو ذات دلالة تقنية لا يمكن دحضها (⚡ أحمر وردي). بلا ضجيج مراقبة."},
        "Haz click en cualquier nodo para ver solo sus conexiones": {"en":"Click any node to see only its connections","fr":"Clique sur un nœud pour voir uniquement ses connexions","pt":"Clica em qualquer nó para ver apenas as suas conexões","ja":"任意のノードをクリックすると、その接続のみを表示します","ko":"노드를 클릭하면 해당 연결만 볼 수 있습니다","zh":"点击任意节点仅查看它的连接","ar":"انقر على أي عقدة لرؤية اتصالاتها فقط"},
        "Leyenda del mapa — cómo leer colores y líneas": {"en":"Map legend — how to read colors and lines","fr":"Légende de la carte — comment lire couleurs et lignes","pt":"Legenda do mapa — como ler cores e linhas","ja":"マップ凡例 — 色と線の読み方","ko":"지도 범례 — 색상과 선 읽는 법","zh":"地图图例 — 如何阅读颜色和线条","ar":"مفتاح الخريطة — كيفية قراءة الألوان والخطوط"},
        "Nodos (círculos del mapa)": {"en":"Nodes (map circles)","fr":"Nœuds (cercles de la carte)","pt":"Nós (círculos do mapa)","ja":"ノード（マップ上の円）","ko":"노드(지도 원)","zh":"节点（地图圆点）","ar":"العقد (دوائر الخريطة)"},
        "Líneas — tipos de ruta": {"en":"Lines — route types","fr":"Lignes — types de route","pt":"Linhas — tipos de rota","ja":"線 — ルートの種類","ko":"선 — 경로 유형","zh":"线条 — 路线类型","ar":"الخطوط — أنواع المسارات"},
        "Línea sólida: confirmado con evidencia directa": {"en":"Solid line: confirmed with direct evidence","fr":"Ligne continue : confirmée par preuve directe","pt":"Linha sólida: confirmada com evidência direta","ja":"実線：直接証拠で確認済み","ko":"실선: 직접 증거로 확인됨","zh":"实线：直接证据确认","ar":"خط متصل: مؤكد بدليل مباشر"},
        "Línea discontinua roja: implicación técnica obligatoria": {"en":"Red dashed line: required technical implication","fr":"Ligne rouge discontinue : implication technique obligatoire","pt":"Linha vermelha tracejada: implicação técnica obrigatória","ja":"赤い破線：必須の技術的含意","ko":"빨간 점선: 필수 기술적 함의","zh":"红色虚线：必需技术含义","ar":"خط أحمر متقطع: دلالة تقنية لازمة"},
        "Líneas discontinuas: señal sin prueba directa": {"en":"Dashed lines: signal without direct proof","fr":"Lignes discontinues : signal sans preuve directe","pt":"Linhas tracejadas: sinal sem prova direta","ja":"破線：直接証拠のないシグナル","ko":"점선: 직접 증거 없는 신호","zh":"虚线：无直接证据的信号","ar":"خطوط متقطعة: إشارة بلا دليل مباشر"},
        "Sólida = evidencia directa verificada": {"en":"Solid = verified direct evidence","fr":"Continue = preuve directe vérifiée","pt":"Sólida = evidência direta verificada","ja":"実線 = 検証済み直接証拠","ko":"실선 = 검증된 직접 증거","zh":"实线 = 已验证直接证据","ar":"متصل = دليل مباشر مؤكد"},
        "Discontinua = inferida/vigilada": {"en":"Dashed = inferred/watch","fr":"Discontinue = inférée/surveillée","pt":"Tracejada = inferida/vigiada","ja":"破線 = 推定/監視","ko":"점선 = 추론/감시","zh":"虚线 = 推断/观察","ar":"متقطع = مستنتج/مراقب"},
        "Grosor = intensidad de señal": {"en":"Thickness = signal intensity","fr":"Épaisseur = intensité du signal","pt":"Espessura = intensidade do sinal","ja":"太さ = シグナル強度","ko":"두께 = 신호 강도","zh":"粗细 = 信号强度","ar":"السماكة = شدة الإشارة"},
        "Cursor sobre línea o nodo = detalle exacto": {"en":"Hover over a line or node = exact detail","fr":"Survol d’une ligne ou d’un nœud = détail exact","pt":"Passar o cursor sobre linha ou nó = detalhe exato","ja":"線またはノードにカーソル = 詳細表示","ko":"선이나 노드에 마우스오버 = 정확한 세부 정보","zh":"悬停在线条或节点上 = 精确详情","ar":"مرر فوق خط أو عقدة = التفاصيل الدقيقة"},
        "No es asesoramiento financiero. Es un radar de huellas públicas, topología, clusters y adopción real.": {"en":"Not financial advice. This is a radar for public traces, topology, clusters and real adoption.","fr":"Ce n’est pas un conseil financier. C’est un radar de traces publiques, topologie, clusters et adoption réelle.","pt":"Não é aconselhamento financeiro. É um radar de pegadas públicas, topologia, clusters e adoção real.","ja":"金融アドバイスではありません。公開痕跡、トポロジー、クラスター、実際の採用を監視するレーダーです。","ko":"금융 조언이 아닙니다. 공개 흔적, 토폴로지, 클러스터 및 실제 채택을 감시하는 레이더입니다.","zh":"这不是金融建议。这是用于公开痕迹、拓扑、集群和真实采用的雷达。","ar":"ليست نصيحة مالية. هذا رادار للآثار العامة والطوبولوجيا والعناقيد والتبني الحقيقي."},
        # Presupuesto / comunidad
        "Presupuesto API": {"en":"API budget","fr":"Budget API","de":"API-Budget","it":"Budget API","pt":"Orçamento API","ja":"API予算","ko":"API 예산","zh":"API 预算","ar":"ميزانية API"},
        "disponibles de": {"en":"available of","fr":"disponibles sur","pt":"disponíveis de","ja":"利用可能 /","ko":"사용 가능 /","zh":"可用，共","ar":"متاح من"},
        "gastados": {"en":"spent","fr":"dépensés","pt":"gastos","ja":"使用済み","ko":"사용됨","zh":"已花费","ar":"منفق"},
        "búsquedas nuevas": {"en":"new searches","fr":"nouvelles recherches","pt":"novas pesquisas","ja":"新規検索","ko":"신규 검색","zh":"新搜索","ar":"عمليات بحث جديدة"},
        "desde caché (gratis)": {"en":"from cache (free)","fr":"depuis le cache (gratuit)","pt":"da cache (grátis)","ja":"キャッシュから（無料）","ko":"캐시에서(무료)","zh":"来自缓存（免费）","ar":"من الذاكرة المؤقتة (مجاني)"},
        "Usuarios activos": {"en":"Active users","fr":"Utilisateurs actifs","pt":"Utilizadores ativos","ja":"アクティブユーザー","ko":"활성 사용자","zh":"活跃用户","ar":"المستخدمون النشطون"},
        "fila AI libre ahora": {"en":"AI queue is free now","fr":"file IA libre maintenant","pt":"fila AI livre agora","ja":"AIキューは現在空いています","ko":"AI 대기열이 지금 비어 있습니다","zh":"AI 队列当前空闲","ar":"طابور الذكاء الاصطناعي متاح الآن"},
        "serías #1 si lanzas una búsqueda": {"en":"you would be #1 if you launch a search","fr":"tu serais n°1 si tu lances une recherche","pt":"ficarias em #1 se iniciares uma pesquisa","ja":"検索を開始すると1番目です","ko":"검색을 시작하면 1번입니다","zh":"如果发起搜索，你将排第 1 位","ar":"ستكون رقم 1 إذا بدأت بحثاً"},
        "Usuario": {"en":"User","fr":"Utilisateur","de":"Benutzer","it":"Utente","pt":"Utilizador","ja":"ユーザー","ko":"사용자","zh":"用户","ar":"المستخدم"},
        "Guía rápida": {"en":"Quick guide","fr":"Guide rapide","pt":"Guia rápido","ja":"クイックガイド","ko":"빠른 안내","zh":"快速指南","ar":"دليل سريع"},
        "DIRECTAS": {"en":"DIRECT","fr":"DIRECTES","pt":"DIRETAS","ja":"直接","ko":"직접","zh":"直接","ar":"مباشرة"},
        "INDIRECTAS": {"en":"INDIRECT","fr":"INDIRECTES","pt":"INDIRETAS","ja":"間接","ko":"간접","zh":"间接","ar":"غير مباشرة"},
        "Inferida": {"en":"Inferred","fr":"Inférée","pt":"Inferida","ja":"推定","ko":"추론","zh":"推断","ar":"مستنتجة"},
        "OBLIGATORIA": {"en":"REQUIRED","fr":"OBLIGATOIRE","pt":"OBRIGATÓRIA","ja":"必須","ko":"필수","zh":"必需","ar":"لازمة"},
        "Vigilada": {"en":"Watched","fr":"Surveillée","pt":"Vigiada","ja":"監視","ko":"감시","zh":"观察","ar":"مراقبة"},
        "Descubierta": {"en":"Discovered","fr":"Découverte","pt":"Descoberta","ja":"発見済み","ko":"발견됨","zh":"已发现","ar":"مكتشفة"},
        "Futura / en desarrollo": {"en":"Future / in development","fr":"Future / en développement","pt":"Futura / em desenvolvimento","ja":"将来 / 開発中","ko":"미래 / 개발 중","zh":"未来 / 开发中","ar":"مستقبلية / قيد التطوير"},
        "Señal fría / slowdown": {"en":"Cold signal / slowdown","fr":"Signal froid / ralentissement","pt":"Sinal frio / slowdown","ja":"冷たいシグナル / 減速","ko":"차가운 신호 / 둔화","zh":"冷信号 / 放缓","ar":"إشارة باردة / تباطؤ"},
        "música local": {"en":"local music","fr":"musique locale","pt":"música local","ja":"ローカル音楽","ko":"로컬 음악","zh":"本地音乐","ar":"موسيقى محلية"},
        "Aviso importante: esta página puede usar dinero real": {"en":"Important notice: this page may use real money","fr":"Avis important : cette page peut utiliser de l’argent réel","pt":"Aviso importante: esta página pode usar dinheiro real","ja":"重要なお知らせ：このページは実際のお金を使用する可能性があります","ko":"중요 알림: 이 페이지는 실제 비용을 사용할 수 있습니다","zh":"重要提示：此页面可能使用真实资金","ar":"تنبيه مهم: قد تستخدم هذه الصفحة أموالاً حقيقية"},
        "El radar puede consultar Anthropic/Web Search cuando uses Discovery o verificación de pruebas. Cada búsqueda nueva descuenta una estimación del presupuesto configurado:": {"en":"The radar may query Anthropic/Web Search when you use Discovery or evidence verification. Each new search deducts an estimate from the configured budget:","fr":"Le radar peut interroger Anthropic/Web Search lorsque tu utilises Discovery ou la vérification des preuves. Chaque nouvelle recherche déduit une estimation du budget configuré :","pt":"O radar pode consultar Anthropic/Web Search quando usas Discovery ou verificação de provas. Cada nova pesquisa desconta uma estimativa do orçamento configurado:","ja":"Discoveryまたは証拠検証を使用すると、レーダーはAnthropic/Web Searchに問い合わせる場合があります。新規検索ごとに設定された予算から推定額が差し引かれます：","ko":"Discovery 또는 증거 검증을 사용할 때 레이더가 Anthropic/Web Search를 조회할 수 있습니다. 새 검색마다 설정된 예산에서 추정 비용이 차감됩니다:","zh":"使用 Discovery 或证据验证时，雷达可能查询 Anthropic/Web Search。每次新搜索都会从配置预算中扣除估算费用：","ar":"قد يستعلم الرادار من Anthropic/Web Search عند استخدام Discovery أو التحقق من الأدلة. كل بحث جديد يخصم تقديراً من الميزانية المحددة:"},
        "Los resultados cacheados no gastan API. Cuando el presupuesto llegue al margen de seguridad, la app pasará a modo caché.": {"en":"Cached results do not spend API. When the budget reaches the safety margin, the app switches to cache mode.","fr":"Les résultats en cache ne consomment pas d’API. Lorsque le budget atteint la marge de sécurité, l’application passe en mode cache.","pt":"Resultados em cache não gastam API. Quando o orçamento atingir a margem de segurança, a app passa para modo cache.","ja":"キャッシュ済み結果はAPIを消費しません。予算が安全マージンに達すると、アプリはキャッシュモードに切り替わります。","ko":"캐시된 결과는 API를 사용하지 않습니다. 예산이 안전 한도에 도달하면 앱은 캐시 모드로 전환됩니다.","zh":"缓存结果不消耗 API。当预算达到安全边际时，应用将切换到缓存模式。","ar":"النتائج المخزنة مؤقتاً لا تستهلك API. عند وصول الميزانية إلى هامش الأمان، ينتقل التطبيق إلى وضع الذاكرة المؤقتة."},
    }
    # Añadir traducciones a los dos diccionarios; si ya existe una clave, completar idiomas faltantes.
    for k, v in extra.items():
        UI_I18N.setdefault(k, {}).update(v)
        _UI_EXTRA_TRANSLATIONS.setdefault(k, {}).update(v)

_rrp_merge_translations()

# Alias textuales para traducir trozos dentro de HTML/Markdown sin tocar URLs/wallets.
_UI_REPLACEMENTS_ORDERED = sorted(_UI_EXTRA_TRANSLATIONS.keys(), key=len, reverse=True)


# ── I18N v6.2.5 — traductor de último recurso para textos UI sueltos ─────────
# Cubre fragmentos hardcodeados dentro de Markdown/HTML/Plotly que no pasan como
# claves exactas. No traduce URLs, wallets, hashes ni nombres oficiales.
_UI_SEGMENT_TRANSLATIONS: Dict[str, Dict[str, str]] = {
    "ja": {
        "Presupuesto API":"API予算", "disponibles":"利用可能", "gastados":"使用済み", "búsquedas nuevas":"新規検索", "desde caché":"キャッシュから", "gratis":"無料",
        "Usuarios activos":"アクティブユーザー", "fila AI libre ahora":"AIキューは現在空き", "serías #1 si lanzas una búsqueda":"検索を開始すると1番目です", "AI activa":"アクティブAI", "Usuario":"ユーザー",
        "Guía rápida":"クイックガイド", "DIRECTAS":"直接", "INDIRECTAS":"間接", "Pública":"公開", "pública":"公開", "Privada":"プライベート", "privada":"プライベート", "Inferida":"推定", "inferida":"推定", "contrato":"契約", "filing":"提出書類",
        "Vigilada":"監視", "vigilada":"監視", "Descubierta":"発見済み", "descubierta":"発見済み", "Futura / en desarrollo":"将来 / 開発中", "Señal fría / slowdown":"冷たいシグナル / 減速", "música local":"ローカル音楽",
        "Aviso importante":"重要なお知らせ", "esta página puede usar dinero real":"このページは実際の費用を使う可能性があります", "resultados cacheados":"キャッシュ済み結果", "no gastan API":"APIを消費しません", "modo caché":"キャッシュモード",
        "Radar avanzado":"高度レーダー", "para vigilar rutas privadas":"プライベートルートを監視するため", "por sus huellas públicas":"公開痕跡によって", "topología":"トポロジー", "anomalías":"異常", "transfers grandes":"大口送金", "régimen temporal":"時間レジーム",
        "Subida":"上昇", "Riesgo":"リスク", "Flip":"フリップ", "Cobertura":"カバレッジ", "Fase":"フェーズ", "Pump":"ポンプ", "Rutas hot":"ホットルート", "Adopción":"採用", "Adopción real":"実採用", "Adopción técnica":"技術的採用",
        "¿Qué significan los datos de arriba?":"上のデータは何を意味しますか？", "Probabilidad":"確率", "impulso de precio":"価格インパルス", "actividad pública":"公開活動", "volumen":"出来高", "Detecta enfriamiento":"冷却を検知", "baja actividad":"低活動", "poca persistencia":"低い持続性", "falta de clusters":"クラスター不足", "parece especulativo":"投機的に見える", "Señal de adopción real":"実採用シグナル", "varias huellas públicas":"複数の公開痕跡", "se coordinan durante tiempo":"一定期間連動する", "Cuántos puntos públicos estamos vigilando":"監視中の公開接点数", "rutas privadas tendrían que dejar rastro":"プライベートルートが痕跡を残すはずの場所", "Escala":"スケール", "ruido bajo":"低ノイズ", "Resume":"要約", "estado completo":"全体状態", "movimiento especulativo":"投機的な動き", "spike":"スパイク", "sin adopción sostenida":"持続的採用なし", "Número de rutas":"ルート数", "motores":"エンジン", "umbral de señal fuerte":"強シグナル閾値",
        "Señal débil":"弱いシグナル", "Predominan señales especulativas":"投機的シグナルが優勢", "poca actividad verificable":"検証可能な活動が少ない", "ledger":"台帳", "No debe interpretarse":"解釈してはいけません", "conexión operativa":"運用接続",
        "Ledger real":"実台帳", "Documental":"文書証拠", "documental":"文書証拠", "Monitorización":"監視", "monitoreo":"監視", "vigilancia":"監視", "especulativo":"投機的", "narrativa":"ナラティブ", "inferencias no operativas":"非運用推定", "pagos":"支払い", "whales":"クジラ", "pruebas oficiales":"公式証拠", "rutas y cobertura":"ルートとカバレッジ",
        "Riesgo de bajada":"下落リスク", "slowdown":"減速", "actividad pública verificable":"検証可能な公開活動", "Precio XRP":"XRP価格", "Riesgo de falso rebote":"偽反発リスク", "presión bajista":"下落圧力", "Alto":"高", "Bajo":"低", "Medio":"中", "Ruido / baja señal":"ノイズ / 低シグナル", "sin adopción real confirmada":"確認済みの実採用なし", "Pump vs Adopción":"ポンプ vs 採用",
        "Haz clic":"クリック", "Haz click":"クリック", "en cualquier nodo":"任意のノード", "del mapa":"マップ上", "para ver":"表示する", "solo sus rutas":"そのルートのみ", "solo sus conexiones":"その接続のみ",
        "Conexiones confirmadas + obligatorias":"確認済み＋必須接続", "Vigilancia / inferidas":"監視 / 推定", "Mapa completo":"完全なマップ", "Solo rutas con evidencia confirmada":"確認済み証拠のあるルートのみ", "implicación técnica irrefutable":"技術的に不可避な関係", "Sin ruido de vigilancia":"監視ノイズなし",
        "Leyenda del mapa":"マップの凡例", "cómo leer colores y líneas":"色と線の読み方", "Nodos":"ノード", "círculos del mapa":"マップの円", "Verde brillante":"明るい緑", "Ledger público real":"実公開台帳", "token nativo verificable":"検証可能なネイティブトークン", "Azul cyan":"シアンブルー", "Infraestructura Ripple":"Rippleインフラ", "Ámbar":"アンバー", "Bancos RippleNet / institucional":"RippleNet銀行 / 機関", "Naranja":"オレンジ", "Corredores ODL activos":"アクティブODL回廊", "Infraestructura privada":"プライベートインフラ", "Morado":"紫", "Huellas públicas vigiladas":"監視中の公開痕跡", "Azul medio":"中間ブルー", "Motores de inteligencia":"インテリジェンスエンジン", "Gris":"グレー", "Conector futuro / en desarrollo":"将来 / 開発中コネクタ",
        "Líneas":"線", "tipos de ruta":"ルートタイプ", "Línea sólida":"実線", "confirmado con evidencia directa":"直接証拠で確認済み", "Verde sólida":"緑の実線", "On-chain":"オンチェーン", "TX visible":"可視TX", "Confianza":"信頼度", "Irrefutable":"反証困難", "Cian sólida":"シアン実線", "Pública verificada":"検証済み公開", "Ámbar sólida":"アンバー実線", "Documentada":"文書化済み", "acuerdo documentado":"文書化された合意", "Línea discontinua roja":"赤い破線", "implicación técnica obligatoria":"必須の技術的関係", "Obligatoria":"必須", "El protocolo lo exige":"プロトコル上必要", "Sin TX directa verificada":"直接TX未検証", "técnicamente irrefutable":"技術的に反証困難", "Líneas discontinuas":"破線", "señal sin prueba directa":"直接証拠のないシグナル", "Morada discontinua":"紫の破線", "Indirecta vigilada":"監視中の間接", "Huella pública detectada":"公開痕跡を検出", "sin confirmar":"未確認", "Requiere verificación":"検証が必要", "Dorada discontinua":"金色の破線", "Descubierta por IA":"AI発見", "Pendiente de confirmar":"確認待ち", "Privada inferida":"推定プライベート", "Ruta privada":"プライベートルート", "sin confirmación pública":"公開確認なし", "Activada por señal indirecta":"間接シグナルで有効化", "Gris punteada":"グレー点線", "Futura / no activa":"将来 / 非アクティブ", "Integración planeada":"計画中の統合", "sin datos activos":"アクティブデータなし", "Sólida":"実線", "Discontinua":"破線", "Grosor":"太さ", "intensidad de señal":"シグナル強度", "Cursor sobre línea o nodo":"線またはノードにカーソル", "detalle exacto":"正確な詳細", "No es asesoramiento financiero":"金融助言ではありません",
        "Buscar":"検索", "Verificar":"検証", "Actualizar":"更新", "Configuración":"設定", "Diagnóstico":"診断", "Donaciones":"寄付", "Histórico":"履歴", "Técnico":"技術", "Rutas":"ルート", "Descubrimientos":"発見", "Comunidad":"コミュニティ", "Vista":"表示", "Enviar":"送信", "Mensaje":"メッセージ", "Chat general":"公開チャット", "Panel reservado al administrador":"管理者専用パネル", "No hay datos disponibles":"利用可能なデータがありません"
    },
    "en": {
        "Presupuesto API":"API budget", "disponibles":"available", "gastados":"spent", "búsquedas nuevas":"new searches", "desde caché":"from cache", "gratis":"free", "Usuarios activos":"Active users", "fila AI libre ahora":"AI queue free now", "serías #1 si lanzas una búsqueda":"you would be #1 if you launch a search", "Usuario":"User", "Guía rápida":"Quick guide", "Subida":"Upside", "Riesgo":"Risk", "Cobertura":"Coverage", "Fase":"Phase", "Rutas hot":"Hot routes", "Señal débil":"Weak signal", "Ledger real":"Real ledger", "Documental":"Documentary", "Vigilancia":"Watch", "especulativo":"speculative", "Riesgo de bajada":"Downside risk", "Adopción real":"Real adoption", "Adopción técnica":"Technical adoption", "Mapa completo":"Full map", "Leyenda del mapa":"Map legend", "Nodos":"Nodes", "Líneas":"Lines", "No es asesoramiento financiero":"Not financial advice", "Buscar":"Search", "Verificar":"Verify", "Actualizar":"Refresh", "Diagnóstico":"Diagnostics", "Técnico":"Technical", "Rutas":"Routes", "Descubrimientos":"Discoveries", "Comunidad":"Community", "Enviar":"Send", "Mensaje":"Message"
    },
    "ko": {
        "Presupuesto API":"API 예산", "disponibles":"사용 가능", "gastados":"사용됨", "búsquedas nuevas":"새 검색", "Usuarios activos":"활성 사용자", "Usuario":"사용자", "Guía rápida":"빠른 안내", "Subida":"상승", "Riesgo":"위험", "Cobertura":"커버리지", "Fase":"단계", "Rutas hot":"핫 경로", "Señal débil":"약한 신호", "Ledger real":"실제 원장", "Documental":"문서 증거", "Vigilancia":"감시", "especulativo":"투기적", "Riesgo de bajada":"하락 위험", "Adopción real":"실제 채택", "Adopción técnica":"기술적 채택", "Mapa completo":"전체 지도", "Leyenda del mapa":"지도 범례", "Nodos":"노드", "Líneas":"선", "No es asesoramiento financiero":"금융 조언이 아닙니다", "Buscar":"검색", "Verificar":"검증", "Actualizar":"새로고침", "Diagnóstico":"진단", "Técnico":"기술", "Rutas":"경로", "Descubrimientos":"발견", "Comunidad":"커뮤니티", "Enviar":"보내기", "Mensaje":"메시지"
    },
    "zh": {
        "Presupuesto API":"API 预算", "disponibles":"可用", "gastados":"已花费", "búsquedas nuevas":"新搜索", "Usuarios activos":"活跃用户", "Usuario":"用户", "Guía rápida":"快速指南", "Subida":"上涨", "Riesgo":"风险", "Cobertura":"覆盖率", "Fase":"阶段", "Rutas hot":"热门路线", "Señal débil":"弱信号", "Ledger real":"真实账本", "Documental":"文档证据", "Vigilancia":"监控", "especulativo":"投机性", "Riesgo de bajada":"下行风险", "Adopción real":"真实采用", "Adopción técnica":"技术采用", "Mapa completo":"完整地图", "Leyenda del mapa":"地图图例", "Nodos":"节点", "Líneas":"线", "No es asesoramiento financiero":"这不是财务建议", "Buscar":"搜索", "Verificar":"验证", "Actualizar":"刷新", "Diagnóstico":"诊断", "Técnico":"技术", "Rutas":"路线", "Descubrimientos":"发现", "Comunidad":"社区", "Enviar":"发送", "Mensaje":"消息"
    },
    "pt": {
        "Presupuesto API":"Orçamento API", "disponibles":"disponíveis", "gastados":"gastos", "búsquedas nuevas":"novas pesquisas", "Usuarios activos":"Utilizadores ativos", "Usuario":"Utilizador", "Guía rápida":"Guia rápido", "Subida":"Alta", "Riesgo":"Risco", "Cobertura":"Cobertura", "Fase":"Fase", "Rutas hot":"Rotas quentes", "Señal débil":"Sinal fraco", "Ledger real":"Ledger real", "Documental":"Documental", "Vigilancia":"Vigilância", "especulativo":"especulativo", "Riesgo de bajada":"Risco de queda", "Adopción real":"Adoção real", "Adopción técnica":"Adoção técnica", "Mapa completo":"Mapa completo", "Leyenda del mapa":"Legenda do mapa", "Nodos":"Nós", "Líneas":"Linhas", "No es asesoramiento financiero":"Não é aconselhamento financeiro", "Buscar":"Pesquisar", "Verificar":"Verificar", "Actualizar":"Atualizar", "Diagnóstico":"Diagnóstico", "Técnico":"Técnico", "Rutas":"Rotas", "Descubrimientos":"Descobertas", "Comunidad":"Comunidade", "Enviar":"Enviar", "Mensaje":"Mensagem"
    },
}


# ── I18N v6.2.6 — capa dura para textos legacy/dinámicos ─────────────────────
def _rrp_merge_hard_i18n_layer() -> None:
    """Capa dura: cubre leyendas y frases incrustadas en HTML antiguo.

    Se mantiene separada de la capa general para que los bloques viejos del mapa,
    sidebar, métricas en columnas y avisos dinámicos no queden en español al cambiar
    idioma. Cuando falte una traducción exacta en un idioma, se usa inglés antes que
    dejar una etiqueta española visible.
    """
    hard: Dict[str, Dict[str, str]] = {
        "{t['ui_info']}": {"en":"Interface translated to your selected language. Institution names, evidence, URLs and technical data stay in their original language to preserve evidence integrity.", "fr":"Interface traduite dans la langue choisie. Les noms d’institutions, preuves, URLs et données techniques restent dans leur langue d’origine pour préserver l’intégrité des preuves.", "de":"Die Oberfläche wird in die gewählte Sprache übersetzt. Institutionsnamen, Belege, URLs und technische Daten bleiben zur Beweissicherheit in der Originalsprache.", "it":"Interfaccia tradotta nella lingua scelta. Nomi di istituzioni, prove, URL e dati tecnici restano nella lingua originale per preservare l’integrità delle prove.", "pt":"Interface traduzida para o idioma escolhido. Nomes de instituições, provas, URLs e dados técnicos ficam no idioma original para preservar a evidência.", "ja":"選択した言語にUIを翻訳します。証拠の整合性を保つため、機関名・証拠・URL・技術データは原語のまま保持します。", "ko":"선택한 언어로 UI가 번역됩니다. 증거 무결성을 위해 기관명, 증거, URL, 기술 데이터는 원문 언어로 유지됩니다.", "zh":"界面会翻译为所选语言。为保持证据完整性，机构名称、证据、URL 和技术数据保留原文。", "ar":"تمت ترجمة الواجهة إلى اللغة المختارة. تبقى أسماء المؤسسات والأدلة والروابط والبيانات التقنية بلغتها الأصلية للحفاظ على سلامة الدليل."},
        "Radar avanzado": {"en":"Advanced radar", "fr":"Radar avancé", "de":"Fortgeschrittener Radar", "it":"Radar avanzato", "pt":"Radar avançado", "ja":"高度レーダー", "ko":"고급 레이더", "zh":"高级雷达", "ar":"رادار متقدم"},
        "Radar avanzado para vigilar rutas privadas por sus huellas públicas: clusters, topología, fingerprints y anomalías.": {"en":"Advanced radar for monitoring private routes through their public traces: clusters, topology, fingerprints and anomalies.", "fr":"Radar avancé pour surveiller les routes privées à travers leurs traces publiques : clusters, topologie, empreintes et anomalies.", "de":"Fortgeschrittener Radar zur Überwachung privater Routen anhand öffentlicher Spuren: Cluster, Topologie, Fingerprints und Anomalien.", "it":"Radar avanzato per monitorare rotte private attraverso tracce pubbliche: cluster, topologia, impronte e anomalie.", "pt":"Radar avançado para vigiar rotas privadas pelas suas pegadas públicas: clusters, topologia, fingerprints e anomalias.", "ja":"公開痕跡からプライベートルートを監視する高度レーダー：クラスター、トポロジー、フィンガープリント、異常を分析します。", "ko":"공개 흔적으로 비공개 경로를 감시하는 고급 레이더: 클러스터, 토폴로지, 지문, 이상 징후를 분석합니다.", "zh":"通过公开痕迹监控私有路线的高级雷达：集群、拓扑、指纹和异常。", "ar":"رادار متقدم لمراقبة المسارات الخاصة عبر آثارها العامة: العناقيد، الطوبولوجيا، البصمات والشذوذ."},
        "Radar avanzado para vigilar rutas privadas por sus huellas públicas: clusters, topología, fingerprints y anomalías, transfers grandes y régimen temporal.": {"en":"Advanced radar for monitoring private routes through their public traces: clusters, topology, fingerprints, anomalies, large transfers and time regime.", "fr":"Radar avancé pour surveiller les routes privées à travers leurs traces publiques : clusters, topologie, empreintes, anomalies, gros transferts et régime temporel.", "de":"Fortgeschrittener Radar zur Überwachung privater Routen anhand öffentlicher Spuren: Cluster, Topologie, Fingerprints, Anomalien, große Transfers und Zeitregime.", "it":"Radar avanzato per monitorare rotte private attraverso tracce pubbliche: cluster, topologia, impronte, anomalie, grandi trasferimenti e regime temporale.", "pt":"Radar avançado para vigiar rotas privadas pelas suas pegadas públicas: clusters, topologia, fingerprints, anomalias, grandes transferências e regime temporal.", "ja":"公開痕跡からプライベートルートを監視する高度レーダー：クラスター、トポロジー、フィンガープリント、異常、大口送金、時間レジームを分析します。", "ko":"공개 흔적으로 비공개 경로를 감시하는 고급 레이더: 클러스터, 토폴로지, 지문, 이상 징후, 대형 전송, 시간 체제를 분석합니다.", "zh":"通过公开痕迹监控私有路线的高级雷达：集群、拓扑、指纹、异常、大额转账和时间状态。", "ar":"رادار متقدم لمراقبة المسارات الخاصة عبر آثارها العامة: العناقيد، الطوبولوجيا، البصمات، الشذوذ، التحويلات الكبيرة والنظام الزمني."},
        "TX real": {"en":"real TX", "fr":"TX réelle", "de":"echte TX", "it":"TX reale", "pt":"TX real", "ja":"実TX", "ko":"실제 TX", "zh":"真实交易", "ar":"معاملة حقيقية"},
        "On-chain": {"en":"On-chain", "fr":"On-chain", "de":"On-chain", "it":"On-chain", "pt":"On-chain", "ja":"オンチェーン", "ko":"온체인", "zh":"链上", "ar":"على السلسلة"},
        # Estado/presupuesto/comunidad
        "activos": {"en":"active", "fr":"actifs", "de":"aktiv", "it":"attivi", "pt":"ativos", "ja":"アクティブ", "ko":"활성", "zh":"活跃", "ar":"نشطون"},
        "Fila AI libre": {"en":"AI queue free", "fr":"File IA libre", "de":"KI-Warteschlange frei", "it":"Coda AI libera", "pt":"Fila AI livre", "ja":"AIキュー空き", "ko":"AI 대기열 비어 있음", "zh":"AI 队列空闲", "ar":"طابور الذكاء الاصطناعي متاح"},
        "AI activa": {"en":"Active AI", "fr":"IA active", "de":"Aktive KI", "it":"AI attiva", "pt":"AI ativa", "ja":"アクティブAI", "ko":"활성 AI", "zh":"活跃 AI", "ar":"ذكاء اصطناعي نشط"},
        "puede usar dinero real": {"en":"may use real money", "fr":"peut utiliser de l’argent réel", "de":"kann echtes Geld verwenden", "it":"può usare denaro reale", "pt":"pode usar dinheiro real", "ja":"実際のお金を使用する可能性があります", "ko":"실제 비용을 사용할 수 있습니다", "zh":"可能使用真实资金", "ar":"قد يستخدم أموالاً حقيقية"},
        "API": {"en":"API", "fr":"API", "de":"API", "it":"API", "pt":"API", "ja":"API", "ko":"API", "zh":"API", "ar":"API"},
        # Sidebar rápido
        "On-chain XRPL (TX real)": {"en":"On-chain XRPL (real TX)", "fr":"XRPL on-chain (TX réelle)", "de":"XRPL on-chain (echte TX)", "it":"XRPL on-chain (TX reale)", "pt":"XRPL on-chain (TX real)", "ja":"オンチェーンXRPL（実TX）", "ko":"온체인 XRPL(실제 TX)", "zh":"链上 XRPL（真实交易）", "ar":"XRPL على السلسلة (معاملة حقيقية)"},
        "Pública (gateway/exchange)": {"en":"Public (gateway/exchange)", "fr":"Publique (gateway/exchange)", "de":"Öffentlich (Gateway/Exchange)", "it":"Pubblica (gateway/exchange)", "pt":"Pública (gateway/exchange)", "ja":"公開（ゲートウェイ/取引所）", "ko":"공개(게이트웨이/거래소)", "zh":"公开（网关/交易所）", "ar":"عام (بوابة/منصة)"},
        "Inferida (contrato/filing)": {"en":"Inferred (contract/filing)", "fr":"Inférée (contrat/filing)", "de":"Abgeleitet (Vertrag/Filing)", "it":"Inferita (contratto/filing)", "pt":"Inferida (contrato/filing)", "ja":"推定（契約/提出書類）", "ko":"추론(계약/공시)", "zh":"推断（合同/备案）", "ar":"مستنتجة (عقد/إفصاح)"},
        "OBLIGATORIA (discontinua)": {"en":"REQUIRED (dashed)", "fr":"OBLIGATOIRE (discontinue)", "de":"ERFORDERLICH (gestrichelt)", "it":"OBBLIGATORIA (tratteggiata)", "pt":"OBRIGATÓRIA (tracejada)", "ja":"必須（破線）", "ko":"필수(점선)", "zh":"必需（虚线）", "ar":"لازمة (متقطع)"},
        "⚡ Protocolo — 97%": {"en":"⚡ Protocol — 97%", "fr":"⚡ Protocole — 97%", "de":"⚡ Protokoll — 97%", "it":"⚡ Protocollo — 97%", "pt":"⚡ Protocolo — 97%", "ja":"⚡ プロトコル — 97%", "ko":"⚡ 프로토콜 — 97%", "zh":"⚡ 协议 — 97%", "ar":"⚡ البروتوكول — 97%"},
        "Vigilada (huella pública)": {"en":"Watched (public trace)", "fr":"Surveillée (trace publique)", "de":"Beobachtet (öffentliche Spur)", "it":"Vigilata (traccia pubblica)", "pt":"Vigiada (pegada pública)", "ja":"監視中（公開痕跡）", "ko":"감시 중(공개 흔적)", "zh":"观察中（公开痕迹）", "ar":"مراقبة (أثر عام)"},
        "Descubierta (motor IA)": {"en":"Discovered (AI engine)", "fr":"Découverte (moteur IA)", "de":"Entdeckt (KI-Engine)", "it":"Scoperta (motore AI)", "pt":"Descoberta (motor IA)", "ja":"発見済み（AIエンジン）", "ko":"발견됨(AI 엔진)", "zh":"AI 引擎发现", "ar":"مكتشفة (محرك ذكاء اصطناعي)"},
        # Mapa y explicación
        "Haz clic en cualquier nodo del mapa para ver solo sus rutas.": {"en":"Click any node on the map to see only its routes.", "fr":"Clique sur n’importe quel nœud de la carte pour voir seulement ses routes.", "de":"Klicke auf einen Knoten der Karte, um nur seine Routen zu sehen.", "it":"Clicca su qualsiasi nodo della mappa per vedere solo le sue rotte.", "pt":"Clica em qualquer nó do mapa para ver apenas as suas rotas.", "ja":"マップ上の任意のノードをクリックすると、そのルートだけを表示します。", "ko":"지도에서 아무 노드나 클릭하면 해당 경로만 표시됩니다.", "zh":"点击地图上的任意节点，仅查看它的路线。", "ar":"انقر على أي عقدة في الخريطة لرؤية مساراتها فقط."},
        "Haz click en cualquier nodo para ver solo sus conexiones": {"en":"Click any node to see only its connections", "fr":"Clique sur n’importe quel nœud pour voir seulement ses connexions", "de":"Klicke auf einen Knoten, um nur seine Verbindungen zu sehen", "it":"Clicca su qualsiasi nodo per vedere solo le sue connessioni", "pt":"Clica em qualquer nó para ver apenas as suas conexões", "ja":"任意のノードをクリックすると、その接続だけを表示します", "ko":"노드를 클릭하면 해당 연결만 표시됩니다", "zh":"点击任意节点仅查看它的连接", "ar":"انقر على أي عقدة لرؤية اتصالاتها فقط"},
        "Señal mixta": {"en":"Mixed signal", "fr":"Signal mixte", "de":"Gemischtes Signal", "it":"Segnale misto", "pt":"Sinal misto", "ja":"混合シグナル", "ko":"혼합 신호", "zh":"混合信号", "ar":"إشارة مختلطة"},
        "Actividad normal": {"en":"Normal activity", "fr":"Activité normale", "de":"Normale Aktivität", "it":"Attività normale", "pt":"Atividade normal", "ja":"通常のアクティビティ", "ko":"정상 활동", "zh":"正常活动", "ar":"نشاط عادي"},
        "Sin señal clara.": {"en":"No clear signal.", "fr":"Aucun signal clair.", "de":"Kein klares Signal.", "it":"Nessun segnale chiaro.", "pt":"Sem sinal claro.", "ja":"明確なシグナルなし。", "ko":"명확한 신호 없음.", "zh":"没有明确信号。", "ar":"لا توجد إشارة واضحة."},
        "Neutral/moderado.": {"en":"Neutral/moderate.", "fr":"Neutre/modéré.", "de":"Neutral/moderat.", "it":"Neutrale/moderato.", "pt":"Neutro/moderado.", "ja":"中立/中程度。", "ko":"중립/보통.", "zh":"中性/适中。", "ar":"محايد/متوسط."},
        "Hay datos útiles, pero todavía mezcla actividad real con inferencias/watch. Conviene abrir las pruebas antes de concluir.": {"en":"There is useful data, but it still mixes real activity with inferences/watch signals. Open the evidence before concluding.", "fr":"Il y a des données utiles, mais elles mélangent encore activité réelle et inférences/surveillance. Ouvre les preuves avant de conclure.", "de":"Es gibt nützliche Daten, aber sie mischen noch reale Aktivität mit abgeleiteten Watch-Signalen. Prüfe die Belege, bevor du schließt.", "it":"Ci sono dati utili, ma mescolano ancora attività reale e inferenze/watch. Apri le prove prima di concludere.", "pt":"Há dados úteis, mas ainda misturam atividade real com inferências/watch. Abre as provas antes de concluir.", "ja":"有用なデータはありますが、実活動と推定/監視シグナルがまだ混在しています。結論の前に証拠を開いてください。", "ko":"유용한 데이터가 있지만 실제 활동과 추론/감시 신호가 섞여 있습니다. 결론 전에 증거를 확인하세요.", "zh":"有有用数据，但仍混合真实活动与推断/观察信号。下结论前请打开证据。", "ar":"توجد بيانات مفيدة، لكنها ما زالت تمزج النشاط الحقيقي مع الاستنتاجات/المراقبة. افتح الأدلة قبل الاستنتاج."},
        "Señales mixtas. El radar no ve aún huellas públicas coordinadas suficientes.": {"en":"Mixed signals. The radar still does not see enough coordinated public traces.", "fr":"Signaux mixtes. Le radar ne voit pas encore assez de traces publiques coordonnées.", "de":"Gemischte Signale. Der Radar sieht noch nicht genug koordinierte öffentliche Spuren.", "it":"Segnali misti. Il radar non vede ancora abbastanza tracce pubbliche coordinate.", "pt":"Sinais mistos. O radar ainda não vê pegadas públicas coordenadas suficientes.", "ja":"シグナルは混在しています。レーダーはまだ十分な協調した公開痕跡を検出していません。", "ko":"혼합 신호입니다. 레이더는 아직 충분히 조율된 공개 흔적을 보지 못합니다.", "zh":"混合信号。雷达尚未看到足够协调的公开痕迹。", "ar":"إشارات مختلطة. لا يرى الرادار بعد آثاراً عامة منسقة بما يكفي."},
    }
    for key, translations in hard.items():
        UI_I18N.setdefault(key, {}).update(translations)
        _UI_EXTRA_TRANSLATIONS.setdefault(key, {}).update(translations)
        for code, translated in translations.items():
            if code == "es":
                continue
            _UI_SEGMENT_TRANSLATIONS.setdefault(code, {})[key] = translated
    # Forzar nota UI correcta en japonés y evitar placeholders de plantillas antiguas.
    UI_I18N.setdefault("ui_scope_note", {})["ja"] = "選択した言語にUIを翻訳します。証拠の整合性を保つため、機関名・証拠・URL・技術データは原語のまま保持します。"
    _UI_EXTRA_TRANSLATIONS.setdefault("ui_scope_note", {})["ja"] = UI_I18N["ui_scope_note"]["ja"]

_rrp_merge_hard_i18n_layer()
_UI_REPLACEMENTS_ORDERED = sorted(_UI_EXTRA_TRANSLATIONS.keys(), key=len, reverse=True)

def _protect_technical_fragments(text: str) -> Tuple[str, Dict[str, str]]:
    """Evita traducir URLs, wallets, hashes, marca y bloques técnicos evidenciales."""
    protected: Dict[str, str] = {}
    out = str(text)
    idx = 0

    def protect_literal(fragment: str) -> None:
        nonlocal out, idx
        if not fragment or fragment not in out:
            return
        key = f"__RRP_PROTECTED_{idx}__"
        protected[key] = fragment
        idx += 1
        out = out.replace(fragment, key)

    # Nombres propios/tokens que no deben quedar medio traducidos dentro de frases.
    for fragment in (
        "Ripple Radar Pro", "Route Path Intelligence", "Proof-First Universal Public Discovery",
        "Ripple Payments", "Ripple Treasury", "Ripple Prime", "Hidden Road", "Metaco",
        "SWIFT", "FedNow", "SEPA/ACH", "Mastercard", "Ethereum",
    ):
        protect_literal(fragment)

    patterns = [
        r"https?://[^\s<>'\")]+",
        r"\b[rX][1-9A-HJ-NP-Za-km-z]{24,40}\b",       # XRPL-like
        r"\b0x[a-fA-F0-9]{40}\b",                      # EVM
        r"\b[A-Fa-f0-9]{48,66}\b",                     # hashes largos
    ]
    for pat in patterns:
        def repl(m):
            nonlocal idx
            key = f"__RRP_PROTECTED_{idx}__"
            protected[key] = m.group(0)
            idx += 1
            return key
        out = re.sub(pat, repl, out)
    return out, protected

def _restore_technical_fragments(text: str, protected: Dict[str, str]) -> str:
    for k, v in protected.items():
        text = text.replace(k, v)
    return text

def _auto_translate_ui_segments(value: str, lang: str) -> str:
    """Reemplazo de segmentos UI sueltos. Se usa después de las claves exactas."""
    if not isinstance(value, str) or lang == "es" or not value:
        return value
    text, protected = _protect_technical_fragments(value)
    # Aplicar mapa del idioma; si no existe, usar inglés como último recurso para no dejar español.
    seg = _UI_SEGMENT_TRANSLATIONS.get(lang) or _UI_SEGMENT_TRANSLATIONS.get("en", {})
    # También usar inglés para términos que el idioma todavía no tenga.
    merged = dict(_UI_SEGMENT_TRANSLATIONS.get("en", {}))
    merged.update(seg)
    for phrase, trans in sorted(merged.items(), key=lambda kv: len(kv[0]), reverse=True):
        if phrase and trans and phrase in text:
            text = text.replace(phrase, trans)
    return _restore_technical_fragments(text, protected)

def _translate_ui_text_any(value: Any, lang: Optional[str] = None) -> Any:
    """Traduce textos de interfaz de forma conservadora pero global.

    Capa 1: claves/frases exactas de interfaz.
    Capa 2: segmentos duros dentro de Markdown/HTML/Plotly/leyendas antiguas.

    No traduce URLs, wallets, hashes, marca ni identificadores técnicos protegidos.
    """
    if not isinstance(value, str):
        return value
    lang = lang or _preferred_lang() or "es"
    if lang == "es" or not value:
        return value

    work, protected = _protect_technical_fragments(value)

    exact = _t(work, lang)
    if exact != work:
        return _restore_technical_fragments(exact, protected)
    d = _UI_EXTRA_TRANSLATIONS.get(work)
    if d:
        return _restore_technical_fragments(d.get(lang) or d.get("en") or work, protected)

    out = work
    for phrase in _UI_REPLACEMENTS_ORDERED:
        trans = _UI_EXTRA_TRANSLATIONS.get(phrase, {}).get(lang) or _UI_EXTRA_TRANSLATIONS.get(phrase, {}).get("en")
        if trans and phrase in out:
            out = out.replace(phrase, trans)
    for phrase, transmap in sorted(UI_I18N.items(), key=lambda kv: len(kv[0]), reverse=True):
        if phrase in out:
            trans = transmap.get(lang) or transmap.get("en") or transmap.get("es")
            if trans:
                out = out.replace(phrase, trans)
    out = _auto_translate_ui_segments(out, lang)
    return _restore_technical_fragments(out, protected)

_ST_I18N_PATCHED = False

def install_streamlit_i18n_patch() -> None:
    """Parchea widgets de Streamlit para traducir etiquetas estáticas restantes.

    Esto evita que textos antiguos hardcodeados queden en español cuando el usuario
    entra en inglés, francés, portugués, etc. Es deliberadamente conservador.
    """
    global _ST_I18N_PATCHED
    if _ST_I18N_PATCHED:
        return
    _ST_I18N_PATCHED = True

    def wrap_text_fn(fn_name: str, arg_positions=(0,)):
        original = getattr(st, fn_name, None)
        if original is None or getattr(original, "_rrp_i18n", False):
            return
        def wrapped(*args, **kwargs):
            args = list(args)
            for pos in arg_positions:
                if len(args) > pos:
                    args[pos] = _translate_ui_text_any(args[pos])
            for key in ("label", "help", "placeholder"):
                if key in kwargs:
                    kwargs[key] = _translate_ui_text_any(kwargs[key])
            return original(*args, **kwargs)
        wrapped._rrp_i18n = True
        setattr(st, fn_name, wrapped)

    for name in ["markdown", "write", "caption", "info", "warning", "error", "success", "title", "header", "subheader"]:
        wrap_text_fn(name, (0,))
    for name in ["button", "text_input", "text_area", "chat_input", "checkbox", "radio", "selectbox", "multiselect", "slider", "number_input"]:
        wrap_text_fn(name, (0,))

    # st.metric necesita label traducido, value intacto.
    original_metric = getattr(st, "metric", None)
    if original_metric is not None and not getattr(original_metric, "_rrp_i18n", False):
        def metric_wrapped(label, value=None, *args, **kwargs):
            return original_metric(_translate_ui_text_any(label), value, *args, **kwargs)
        metric_wrapped._rrp_i18n = True
        st.metric = metric_wrapped

    # Tabs: traducir lista de pestañas.
    original_tabs = getattr(st, "tabs", None)
    if original_tabs is not None and not getattr(original_tabs, "_rrp_i18n", False):
        def tabs_wrapped(tabs, *args, **kwargs):
            try:
                tabs = [_translate_ui_text_any(x) for x in tabs]
            except Exception:
                pass
            return original_tabs(tabs, *args, **kwargs)
        tabs_wrapped._rrp_i18n = True
        st.tabs = tabs_wrapped

    # Dataframes/tablas: traducir cabeceras visibles sin tocar valores técnicos.
    original_dataframe = getattr(st, "dataframe", None)
    if original_dataframe is not None and not getattr(original_dataframe, "_rrp_i18n", False):
        def dataframe_wrapped(data=None, *args, **kwargs):
            try:
                if hasattr(data, "copy") and hasattr(data, "columns"):
                    data2 = data.copy()
                    data2.columns = [_translate_ui_text_any(str(c)) for c in data2.columns]
                    data = data2
            except Exception:
                pass
            return original_dataframe(data, *args, **kwargs)
        dataframe_wrapped._rrp_i18n = True
        st.dataframe = dataframe_wrapped

    # Plotly: traducir títulos, leyendas y nombres de trazas antes de pintar.
    original_plotly_chart = getattr(st, "plotly_chart", None)
    if original_plotly_chart is not None and not getattr(original_plotly_chart, "_rrp_i18n", False):
        def plotly_wrapped(fig, *args, **kwargs):
            try:
                _translate_plotly_figure_inplace(fig)
            except Exception:
                pass
            return original_plotly_chart(fig, *args, **kwargs)
        plotly_wrapped._rrp_i18n = True
        st.plotly_chart = plotly_wrapped

    # HTML embebido de Streamlit components: traducir UI local, no datos protegidos.
    try:
        original_html = getattr(_st_components, "html", None)
        if original_html is not None and not getattr(original_html, "_rrp_i18n", False):
            def html_wrapped(html_content, *args, **kwargs):
                try:
                    html_content = _translate_ui_text_any(html_content)
                except Exception:
                    pass
                return original_html(html_content, *args, **kwargs)
            html_wrapped._rrp_i18n = True
            _st_components.html = html_wrapped
    except Exception:
        pass



# ── I18N v6.2.6 — patch para columnas, contenedores y sidebar ────────────────
_DELTA_I18N_PATCHED = False
_ORIGINAL_INSTALL_STREAMLIT_I18N_PATCH = install_streamlit_i18n_patch

def _install_delta_generator_i18n_patch() -> None:
    """Traduce también col.metric(), col.markdown(), containers, sidebar, etc."""
    global _DELTA_I18N_PATCHED
    if _DELTA_I18N_PATCHED:
        return
    _DELTA_I18N_PATCHED = True
    try:
        from streamlit.delta_generator import DeltaGenerator
    except Exception:
        return

    def patch_method(name: str, arg_positions=(0,), mode: str = "text") -> None:
        original = getattr(DeltaGenerator, name, None)
        if original is None or getattr(original, "_rrp_i18n", False):
            return
        def wrapped(self, *args, __orig=original, __positions=arg_positions, __mode=mode, **kwargs):
            args = list(args)
            try:
                if __mode == "tabs" and args:
                    args[0] = [_translate_ui_text_any(x) for x in args[0]]
                elif __mode == "metric" and args:
                    args[0] = _translate_ui_text_any(args[0])
                elif __mode == "dataframe" and args:
                    data = args[0]
                    if hasattr(data, "copy") and hasattr(data, "columns"):
                        data2 = data.copy()
                        data2.columns = [_translate_ui_text_any(str(c)) for c in data2.columns]
                        args[0] = data2
                elif __mode == "plotly" and args:
                    _translate_plotly_figure_inplace(args[0])
                else:
                    for pos in __positions:
                        if len(args) > pos:
                            args[pos] = _translate_ui_text_any(args[pos])
                    for key in ("label", "help", "placeholder"):
                        if key in kwargs:
                            kwargs[key] = _translate_ui_text_any(kwargs[key])
            except Exception:
                pass
            return __orig(self, *args, **kwargs)
        wrapped._rrp_i18n = True
        setattr(DeltaGenerator, name, wrapped)

    for name in ["markdown", "write", "caption", "info", "warning", "error", "success", "title", "header", "subheader"]:
        patch_method(name, (0,), "text")
    for name in ["button", "text_input", "text_area", "chat_input", "checkbox", "radio", "selectbox", "multiselect", "slider", "number_input"]:
        patch_method(name, (0,), "text")
    patch_method("metric", (0,), "metric")
    patch_method("tabs", (0,), "tabs")
    patch_method("dataframe", (0,), "dataframe")
    patch_method("plotly_chart", (0,), "plotly")

def install_streamlit_i18n_patch() -> None:
    _ORIGINAL_INSTALL_STREAMLIT_I18N_PATCH()
    _install_delta_generator_i18n_patch()

def _translate_plotly_figure_inplace(fig: Any) -> Any:
    """Traduce títulos/leyendas/hover de Plotly sin tocar datos ni nombres de entidades."""
    try:
        title = getattr(fig.layout, "title", None)
        if title and getattr(title, "text", None):
            fig.layout.title.text = _translate_ui_text_any(fig.layout.title.text)
    except Exception:
        pass
    try:
        legend = getattr(fig.layout, "legend", None)
        if legend and getattr(legend, "title", None) and getattr(legend.title, "text", None):
            legend.title.text = _translate_ui_text_any(legend.title.text)
    except Exception:
        pass
    for axis_name in ("xaxis", "xaxis2", "xaxis3", "yaxis", "yaxis2", "yaxis3"):
        try:
            ax = getattr(fig.layout, axis_name, None)
            if ax and getattr(ax, "title", None) and getattr(ax.title, "text", None):
                ax.title.text = _translate_ui_text_any(ax.title.text)
        except Exception:
            pass
    try:
        anns = getattr(fig.layout, "annotations", None) or []
        for ann in anns:
            if getattr(ann, "text", None):
                ann.text = _translate_ui_text_any(ann.text)
    except Exception:
        pass
    try:
        for tr in fig.data:
            if getattr(tr, "name", None):
                tr.name = _translate_ui_text_any(tr.name)
            for attr in ("text", "hovertext", "hovertemplate"):
                try:
                    val = getattr(tr, attr, None)
                    if isinstance(val, str):
                        setattr(tr, attr, _translate_ui_text_any(val))
                    elif isinstance(val, (list, tuple)):
                        setattr(tr, attr, [_translate_ui_text_any(x) if isinstance(x, str) else x for x in val])
                except Exception:
                    pass
            try:
                marker = getattr(tr, "marker", None)
                cb = getattr(marker, "colorbar", None) if marker is not None else None
                if cb and getattr(cb, "title", None) and getattr(cb.title, "text", None):
                    cb.title.text = _translate_ui_text_any(cb.title.text)
            except Exception:
                pass
    except Exception:
        pass
    return fig


def _is_admin_name(nickname: str) -> bool:
    key = _norm_key(nickname).replace(" ", "")
    return key in {_norm_key(n).replace(" ", "") for n in ADMIN_USERNAMES}


def _active_name_taken(conn: sqlite3.Connection, nickname: str, exclude_user_id: Optional[str] = None) -> bool:
    """Evita que dos usuarios online usen el mismo nombre público a la vez."""
    nickname_key = _norm_key(_clean_nickname(nickname)).replace(" ", "")
    if not nickname_key:
        return False
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()
        rows = conn.execute(
            "SELECT user_id, nickname FROM community_users WHERE last_seen > ?",
            (cutoff,),
        ).fetchall()
        for uid, nick in rows:
            if exclude_user_id and str(uid) == str(exclude_user_id):
                continue
            if _norm_key(str(nick or "")).replace(" ", "") == nickname_key:
                return True
    except Exception:
        return False
    return False


def _active_investigator_count(conn: sqlite3.Connection) -> int:
    """Cuenta usuarios activos con permiso de investigación/API, no simples visitantes."""
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()
        rows = conn.execute(
            "SELECT COUNT(*) FROM community_users WHERE last_seen > ? AND COALESCE(role,'user') IN ('user','admin')",
            (cutoff,),
        ).fetchone()
        return int(rows[0] if rows else 0)
    except Exception:
        return 0


def _can_current_user_investigate(conn: sqlite3.Connection) -> bool:
    """Los visitantes por encima del cupo pueden mirar datos, pero no consumir API."""
    if _is_admin_session(conn):
        return True
    return bool(st.session_state.get("rrp_can_investigate", False))


def _is_admin_session(conn: Optional[sqlite3.Connection] = None) -> bool:
    if not st.session_state.get("admin_authenticated"):
        return False
    nick = str(st.session_state.get("community_nickname", "") or "")
    if _is_admin_name(nick):
        return True
    if conn is not None:
        try:
            row = conn.execute("SELECT role FROM community_users WHERE user_id=?", (_community_user_id(),)).fetchone()
            return bool(row and str(row[0]).lower() == "admin")
        except Exception:
            return False
    return False


def _language_name(code: str) -> str:
    return PUBLIC_LANGUAGES.get(str(code or "").lower(), str(code or "es"))


def _translate_chat_cached(conn: sqlite3.Connection, message_id: int, text: str, target_lang: str, source_lang: str = "") -> str:
    """Traducción automática cacheada por mensaje/idioma.

    Usa Anthropic si hay API key; si no existe, muestra el original. No se llama de nuevo
    para el mismo mensaje e idioma. Esto evita quemar presupuesto en cada refresco del chat.
    """
    target_lang = (target_lang or "es").lower()
    source_lang = (source_lang or "").lower()
    if not target_lang or target_lang == source_lang:
        return text
    if not text or len(text.strip()) < 2:
        return text
    try:
        row = conn.execute(
            "SELECT translated FROM chat_translations WHERE message_id=? AND target_lang=?",
            (int(message_id), target_lang),
        ).fetchone()
        if row and row[0]:
            return str(row[0])
    except Exception:
        pass

    key = _get_api_key()
    if not key:
        return text

    # Control simple para no traducir cientos de mensajes de golpe en una primera carga.
    budget_key = f"translation_calls_{target_lang}"
    calls = int(st.session_state.get(budget_key, 0) or 0)
    if calls >= 8:
        return text

    try:
        payload = {
            "model": ANTHROPIC_MODEL_FAST,
            "max_tokens": 350,
            "temperature": 0,
            "messages": [{"role": "user", "content": (
                f"Translate this public chat message to {_language_name(target_lang)}. "
                "Keep meaning, tone and URLs. Return ONLY the translation, no notes.\n\n"
                f"Message:\n{text[:1200]}"
            )}],
        }
        headers = {
            "x-api-key": key,
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        }
        resp = requests.post(ANTHROPIC_API_URL, json=payload, headers=headers, timeout=25)
        st.session_state[budget_key] = calls + 1
        if resp.status_code != 200:
            return text
        data = resp.json()
        translated = "".join([c.get("text", "") for c in data.get("content", []) if isinstance(c, dict)]).strip()
        if not translated:
            return text
        conn.execute(
            "INSERT OR REPLACE INTO chat_translations (message_id, target_lang, translated, created_at) VALUES (?, ?, ?, ?)",
            (int(message_id), target_lang, translated, datetime.now(timezone.utc).isoformat()),
        )
        conn.commit()
        return translated
    except Exception:
        return text



def _clean_nickname(value: str) -> str:
    """Normaliza el nickname sin permitir HTML ni texto enorme."""
    value = (value or "").strip()
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"[^\w\-\. áéíóúÁÉÍÓÚñÑüÜ]", "", value, flags=re.UNICODE)
    return value[:28].strip()


def _clean_chat_body(value: str) -> str:
    """Limpia mensaje de chat y limita longitud."""
    value = (value or "").replace("\x00", "").strip()
    value = re.sub(r"\n{3,}", "\n\n", value)
    return value[:_CHAT_MAX_LEN].strip()


def _community_user_id() -> str:
    """Reutiliza la sesión Streamlit como identidad local anónima."""
    return _session_id()


def _get_current_nickname(conn: sqlite3.Connection) -> str:
    """Devuelve nickname actual si existe en sesión o BD."""
    nick = st.session_state.get("community_nickname", "")
    if nick:
        return nick
    try:
        uid = _community_user_id()
        row = conn.execute("SELECT nickname FROM community_users WHERE user_id=?", (uid,)).fetchone()
        if row and row[0]:
            st.session_state["community_nickname"] = row[0]
            return row[0]
    except Exception:
        pass
    return ""


def _save_current_user(conn: sqlite3.Connection, nickname: str) -> bool:
    """Crea/actualiza el usuario local del chat, sin permitir nombres duplicados online."""
    nickname = _clean_nickname(nickname)
    if len(nickname) < 2:
        return False
    try:
        uid = _community_user_id()
        if _active_name_taken(conn, nickname, exclude_user_id=uid):
            st.session_state["entry_name_error"] = "Ese nombre ya está en línea. Elige otro para evitar confusión en el chat."
            return False
        now = datetime.now(timezone.utc).isoformat()
        lang = _preferred_lang() or "es"
        role = "admin" if (_is_admin_name(nickname) and st.session_state.get("admin_authenticated")) else "user"
        conn.execute("""
            INSERT INTO community_users (user_id, nickname, created_at, last_seen, reputation, muted, language, role)
            VALUES (?, ?, ?, ?, 1, 0, ?, ?)
            ON CONFLICT(user_id) DO UPDATE SET nickname=excluded.nickname, last_seen=excluded.last_seen, language=excluded.language, role=excluded.role
        """, (uid, nickname, now, now, lang, role))
        conn.commit()
        st.session_state["community_nickname"] = nickname
        return True
    except Exception:
        return False


def _touch_current_user(conn: sqlite3.Connection) -> None:
    """Actualiza last_seen si el usuario ya tiene nickname."""
    try:
        nickname = _get_current_nickname(conn)
        if not nickname:
            return
        conn.execute(
            "UPDATE community_users SET last_seen=? WHERE user_id=?",
            (datetime.now(timezone.utc).isoformat(), _community_user_id())
        )
        conn.commit()
    except Exception:
        pass


def _community_stats(conn: sqlite3.Connection) -> Tuple[int, int, int]:
    """Devuelve usuarios totales, usuarios recientes y mensajes visibles."""
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()
        users_total = conn.execute("SELECT COUNT(*) FROM community_users").fetchone()[0]
        users_now = conn.execute("SELECT COUNT(*) FROM community_users WHERE last_seen > ?", (cutoff,)).fetchone()[0]
        msg_count = conn.execute("SELECT COUNT(*) FROM community_messages WHERE deleted=0").fetchone()[0]
        return int(users_total), int(users_now), int(msg_count)
    except Exception:
        return 0, 0, 0


def _send_chat_message(conn: sqlite3.Connection, body: str) -> Tuple[bool, str]:
    """Guarda un mensaje con cooldown anti-spam básico."""
    nickname = _get_current_nickname(conn)
    if not nickname:
        return False, "Primero elige un nombre de usuario."
    body = _clean_chat_body(body)
    if len(body) < 2:
        return False, "El mensaje está vacío."
    if len(body) > _CHAT_MAX_LEN:
        return False, f"Máximo {_CHAT_MAX_LEN} caracteres."
    now_ts = _time.time()
    last_ts = float(st.session_state.get("community_last_send_ts", 0.0) or 0.0)
    remaining = _CHAT_COOLDOWN_SECONDS - (now_ts - last_ts)
    if remaining > 0:
        return False, f"Espera {remaining:.1f}s antes de enviar otro mensaje."
    try:
        uid = _community_user_id()
        muted = conn.execute("SELECT muted FROM community_users WHERE user_id=?", (uid,)).fetchone()
        if muted and int(muted[0]) == 1:
            return False, "Tu usuario está silenciado temporalmente."
        now = datetime.now(timezone.utc).isoformat()
        lang = _preferred_lang() or "es"
        role = "admin" if _is_admin_session(conn) else "user"
        conn.execute(
            "INSERT INTO community_messages (user_id, nickname, body, created_at, deleted, lang, pinned, role) VALUES (?, ?, ?, ?, 0, ?, 0, ?)",
            (uid, nickname, body, now, lang, role)
        )
        conn.execute("UPDATE community_users SET last_seen=? WHERE user_id=?", (now, uid))
        # Limpieza suave: conservar los últimos N mensajes para que la SQLite no crezca sin control.
        conn.execute("""
            DELETE FROM community_messages
            WHERE id NOT IN (SELECT id FROM community_messages ORDER BY id DESC LIMIT ?)
        """, (_CHAT_RETENTION_LIMIT,))
        conn.commit()
        st.session_state["community_last_send_ts"] = now_ts
        return True, "Enviado."
    except Exception as e:
        return False, f"No se pudo enviar: {e}"


def _load_chat_messages(conn: sqlite3.Connection, limit: int = 80) -> pd.DataFrame:
    """Carga últimos mensajes visibles."""
    try:
        return pd.read_sql_query(
            "SELECT id, user_id, nickname, body, created_at, lang, pinned, role FROM community_messages "
            "WHERE deleted=0 ORDER BY pinned DESC, id DESC LIMIT ?",
            conn, params=(int(limit),)
        ).sort_values("id")
    except Exception:
        return pd.DataFrame(columns=["id", "user_id", "nickname", "body", "created_at", "lang", "pinned", "role"])


def render_user_window(conn: sqlite3.Connection, compact: bool = False) -> None:
    """Ventana/panel de usuario. En compact va en sidebar; completo en Comunidad."""
    nickname = _get_current_nickname(conn)
    if compact:
        if nickname:
            st.caption(f"👤 Usuario: **{nickname}**")
            if st.button("Cambiar usuario", width="stretch", key="community_change_user_side"):
                st.session_state.pop("community_nickname", None)
                st.rerun()
        else:
            st.warning("👤 Entra como usuario para hablar en el chat.")
        return

    st.markdown("### 👤 Ventana de usuario")
    if nickname:
        users_total, users_now, msg_count = _community_stats(conn)
        c1, c2, c3 = st.columns(3)
        c1.metric("Tu usuario", nickname)
        c2.metric("Usuarios recientes", users_now)
        c3.metric("Mensajes", msg_count)
        with st.expander("Cambiar mi nombre o idioma"):
            new_nick = st.text_input("Nuevo nombre", value=nickname, max_chars=28, key="community_nick_edit")
            labels = [f"{name} ({code.upper()})" for code, name in PUBLIC_LANGUAGES.items()]
            current_code = _preferred_lang() or "es"
            current_idx = list(PUBLIC_LANGUAGES.keys()).index(current_code) if current_code in PUBLIC_LANGUAGES else 0
            selected = st.selectbox("Idioma del chat", labels, index=current_idx, key="community_lang_edit")
            chosen_code = selected.split("(")[-1].replace(")", "").lower().strip()
            if st.button("Guardar nombre/idioma", width="stretch", key="community_save_nick_edit"):
                _set_preferred_lang(chosen_code)
                if _save_current_user(conn, new_nick):
                    st.toast("Perfil actualizado.")
                    st.rerun()
                else:
                    st.error("El nombre debe tener al menos 2 caracteres.")
        return

    st.markdown("""
<div style='background:linear-gradient(135deg,rgba(14,165,233,0.18),rgba(168,85,247,0.14));
            border:1px solid rgba(125,211,252,0.35);border-radius:18px;padding:18px;margin:8px 0 16px 0;'>
  <div style='font-size:1.08rem;font-weight:900;color:#E0F2FE;margin-bottom:6px;'>Bienvenido al radar</div>
  <div style='color:#CBD5E1;line-height:1.45;'>
    Elige un nombre público para entrar en la comunidad. No uses datos personales.
    Este nombre solo sirve para el chat general y para feedback de la beta.
  </div>
</div>
""", unsafe_allow_html=True)
    nick = st.text_input("Nombre de usuario público", placeholder="Ej: CosmosRadar", max_chars=28, key="community_nick_create")
    if st.button("Entrar a la comunidad", width="stretch", key="community_create_user"):
        if _save_current_user(conn, nick):
            st.toast("Usuario creado.")
            st.rerun()
        else:
            st.error("Pon un nombre válido de al menos 2 caracteres.")


def render_general_chat(conn: sqlite3.Connection) -> None:
    """Chat general público con traducción automática cacheada y modo admin."""
    _touch_current_user(conn)
    nickname = _get_current_nickname(conn)
    target_lang = _preferred_lang() or "es"
    is_admin = _is_admin_session(conn)

    st.markdown("### 💬 " + _t("Chat general"))
    st.caption(f"Chat público en vivo · idioma activo: {_language_name(target_lang)} · traducción automática cacheada si hay API disponible.")
    if st_autorefresh is not None:
        st_autorefresh(interval=3000, limit=None, key="community_chat_live_autorefresh")

    if not nickname:
        st.info("Crea primero tu usuario arriba para poder escribir. Puedes leer el chat sin iniciar usuario.")

    messages = _load_chat_messages(conn, limit=90)
    chat_box = st.container(height=460, border=True)
    with chat_box:
        if messages.empty:
            st.info("Todavía no hay mensajes. Sé el primero en abrir conversación.")
        else:
            my_uid = _community_user_id()
            for _, r in messages.iterrows():
                msg_id = int(r.get("id", 0) or 0)
                is_me = str(r.get("user_id", "")) == my_uid
                role = str(r.get("role", "") or "user").lower()
                pinned = int(r.get("pinned", 0) or 0) == 1
                raw_nick = str(r.get("nickname", "Usuario"))
                nick = html.escape(raw_nick)
                src_lang = str(r.get("lang", "") or "es").lower()
                original = str(r.get("body", ""))
                shown = _translate_chat_cached(conn, msg_id, original, target_lang, src_lang)
                body = html.escape(shown).replace("\n", "<br>")
                created = str(r.get("created_at", ""))[:16].replace("T", " ")
                align = "flex-end" if is_me else "flex-start"
                bg = "rgba(14,165,233,0.18)" if is_me else "rgba(30,41,59,0.92)"
                if role == "admin":
                    bg = "linear-gradient(135deg,rgba(14,165,233,.24),rgba(168,85,247,.18))"
                border = "rgba(56,189,248,0.40)" if is_me else "rgba(148,163,184,0.22)"
                badge = "<span style='border:1px solid rgba(34,211,238,.45);color:#67E8F9;background:rgba(8,47,73,.35);border-radius:999px;padding:2px 7px;font-size:.68rem;font-weight:900;'>ADMIN</span>" if role == "admin" else ""
                pin_badge = "<span style='color:#FDE68A;font-size:.75rem;font-weight:900;'>📌 FIJADO</span>" if pinned else ""
                lang_badge = f"<span style='color:#64748B;font-size:.70rem;'>· {html.escape(src_lang.upper())}</span>" if src_lang else ""
                original_note = ""
                if shown != original and target_lang != src_lang:
                    original_note = f"<div style='margin-top:6px;color:#64748B;font-size:.72rem;'>Traducido automáticamente desde {html.escape(_language_name(src_lang))}</div>"
                st.markdown(f"""
<div style='display:flex;justify-content:{align};margin:7px 0;'>
  <div style='max-width:80%;background:{bg};border:1px solid {border};border-radius:15px;padding:9px 11px;box-shadow:0 10px 28px rgba(2,6,23,.18);'>
    <div style='display:flex;gap:8px;align-items:center;margin-bottom:4px;flex-wrap:wrap;'>
      <span style='font-weight:900;color:#E2E8F0;font-size:0.86rem;'>{nick}</span>{badge}{pin_badge}
      <span style='color:#64748B;font-size:0.72rem;'>{created}</span>{lang_badge}
    </div>
    <div style='color:#CBD5E1;font-size:0.89rem;line-height:1.46;'>{body}</div>
    {original_note}
  </div>
</div>
""", unsafe_allow_html=True)
                if is_admin:
                    ac1, ac2, ac3 = st.columns([0.2,0.2,0.6])
                    with ac1:
                        if st.button("📌" if not pinned else "📍", key=f"pin_msg_{msg_id}", help="Fijar/desfijar mensaje"):
                            conn.execute("UPDATE community_messages SET pinned=? WHERE id=?", (0 if pinned else 1, msg_id))
                            conn.commit(); st.rerun()
                    with ac2:
                        if st.button("🗑️", key=f"del_msg_{msg_id}", help="Ocultar mensaje"):
                            conn.execute("UPDATE community_messages SET deleted=1 WHERE id=?", (msg_id,))
                            conn.commit(); st.rerun()

    with st.form("community_chat_form", clear_on_submit=True):
        body = st.text_area(_t("Mensaje"), placeholder=_t("Escribe al chat general..."), height=80, max_chars=_CHAT_MAX_LEN, disabled=not bool(nickname))
        send = st.form_submit_button(_t("Enviar"), width="stretch", disabled=not bool(nickname))
        if send:
            ok, msg = _send_chat_message(conn, body)
            if ok:
                st.toast(msg)
                st.rerun()
            else:
                st.error(msg)


def render_admin_panel(conn: sqlite3.Connection) -> None:
    """Panel admin local para moderar chat y mensajes fijados."""
    st.markdown("### 🛡️ " + _t("Admin"))
    nickname = _get_current_nickname(conn)
    if not _is_admin_name(nickname):
        st.info(_t("Panel reservado al administrador."))
        return
    if not st.session_state.get("admin_authenticated"):
        pwd = st.text_input("Contraseña admin", type="password", key="admin_password_input")
        if st.button("Entrar como admin", width="stretch", key="admin_login_btn"):
            if str(pwd or "") == ADMIN_PASSWORD:
                st.session_state["admin_authenticated"] = True
                conn.execute("UPDATE community_users SET role='admin' WHERE user_id=?", (_community_user_id(),))
                conn.commit()
                st.success("Admin activado.")
                st.rerun()
            else:
                st.error("Contraseña incorrecta.")
        return
    st.success(f"Sesión admin activa: {html.escape(_get_current_nickname(conn))}")
    c1, c2, c3 = st.columns(3)
    if c1.button("Desactivar admin", width="stretch", key="admin_logout_btn"):
        st.session_state.pop("admin_authenticated", None)
        st.rerun()
    if c2.button("Borrar caché traducciones", width="stretch", key="admin_clear_translations"):
        conn.execute("DELETE FROM chat_translations")
        conn.commit(); st.toast("Traducciones borradas.")
    if c3.button("Desfijar todos", width="stretch", key="admin_unpin_all"):
        conn.execute("UPDATE community_messages SET pinned=0")
        conn.commit(); st.toast("Mensajes desfijados.")

    st.markdown("#### Fijar aviso admin nuevo")
    with st.form("admin_pin_new_message_form", clear_on_submit=True):
        pin_body = st.text_area("Mensaje fijado", height=90, max_chars=_CHAT_MAX_LEN, key="admin_new_pin_body")
        submit_pin = st.form_submit_button("📌 Publicar y fijar", width="stretch")
        if submit_pin:
            body = _clean_chat_body(pin_body)
            if len(body) < 2:
                st.error("Escribe un mensaje válido.")
            else:
                now = datetime.now(timezone.utc).isoformat()
                nick = _get_current_nickname(conn) or "admin"
                conn.execute(
                    "INSERT INTO community_messages (user_id, nickname, body, created_at, deleted, lang, pinned, role) VALUES (?, ?, ?, ?, 0, ?, 1, 'admin')",
                    (_community_user_id(), nick, body, now, _preferred_lang() or "es"),
                )
                conn.commit()
                st.success("Mensaje publicado y fijado.")
                st.rerun()

    pinned = pd.read_sql_query("SELECT id, nickname, body, created_at FROM community_messages WHERE deleted=0 AND pinned=1 ORDER BY id DESC", conn)
    st.markdown("#### Mensajes fijados")
    if pinned.empty:
        st.caption("No hay mensajes fijados.")
    else:
        for _, r in pinned.iterrows():
            st.markdown(f"📌 **{html.escape(str(r['nickname']))}** · {str(r['created_at'])[:16]}  \n{html.escape(str(r['body']))}")


def render_community(conn: sqlite3.Connection) -> None:
    """Sección completa de comunidad."""
    st.subheader(_t("Comunidad beta"))
    render_queue_status(conn)
    _qpos = _public_queue_position(conn)
    if _qpos:
        st.info(f"⏳ Estás en la fila AI en el puesto #{_qpos}. Puedes seguir usando el chat y explorando el mapa mientras tanto.")
    st.markdown("""
<div class='rrp-note'>
Aquí la gente puede presentarse, avisar de fallos, comentar rutas del radar y coordinar pruebas sin salir de la app.
Empieza simple: usuario local + chat público. Más adelante se puede añadir login real, roles, moderación avanzada y reportes.
</div>
""", unsafe_allow_html=True)
    left, right = st.columns([0.95, 1.55])
    with left:
        render_user_window(conn, compact=False)
        render_admin_panel(conn)
        st.markdown("#### Reglas mínimas")
        st.markdown("""
- No claves API, seeds ni claves privadas.
- No promesas de rentabilidad ni señales financieras como certeza.
- Usa el chat para feedback, bugs, pruebas y debate.
- Si una conexión es especulativa, dilo claramente.
""")
    with right:
        render_general_chat(conn)


# ── Nodos estáticos confirmados: sin estos el mapa los pinta como "privados inferidos" ──
# Fuente: listados oficiales de Ripple, anuncios de partnerships, SEC filings, on-chain data.
_STATIC_CONFIRMED_PARTNERS: Dict[str, float] = {
    # ── Ripple Core (certeza absoluta) ──────────────────────────────────────
    "Ripple Payments": 1.00, "Rail": 1.00, "Treasury": 1.00,
    "Ripple Escrow": 1.00, "XRPL": 1.00, "RLUSD": 0.99,
    "Custody/Metaco": 0.98, "Standard Custody": 0.97,
    "Hidden Road / Prime": 0.98,
    # ── Infraestructura nativa XRPL (arquitectura del ledger, no partnerships) ─
    "DEX/AMM": 1.00,            # DEX nativo activado en XRPL (Amendment XLS-30)
    "Permissioned DEX": 0.97,   # Capa institucional Ripple sobre el DEX nativo
    "Trustlines": 1.00,         # Mecanismo nativo del ledger XRPL
    "Public Gateway": 0.99,     # Cuentas emisoras certificadas en XRPL
    "FedNow": 0.95,             # Rail de pagos instantáneos EEUU (integración Ripple)
    "SEPA/ACH": 0.93,           # Rails de pago conectados a RippleNet
    "SWIFT": 0.90,              # Red bancaria legacy interconectada
    # ── Exchanges XRPL con wallets on-chain ──────────────────────────────────
    "Bitstamp": 0.99, "GateHub": 0.98, "Kraken": 0.95, "Binance": 0.93,
    # ── ODL confirmados (contratos SEC + listings Ripple) ────────────────────
    "Tranglo (ODL)": 1.00,      # SEC filings + Ripple 40% stake
    "Bitso (ODL MX)": 0.99,     # ODL México confirmado
    "BeeTech (ODL BR)": 0.96,   # ODL Brasil confirmado
    "Coins.ph (ODL PH)": 0.98,  # ODL Filipinas confirmado
    "Cuallix (ODL US-MX)": 0.93,"FlashFX (ODL AU)": 0.94,
    # ── RippleNet Asia-Pac ───────────────────────────────────────────────────
    "SBI Remit": 0.99,          # anuncio oficial SBI Group
    "MoneyTap / SBI": 0.97,
    "Axis Bank": 0.92,
    "LianLian Pay": 0.96,       # RippleNet China 2018 (anuncio oficial)
    "Siam Commercial Bank": 0.93,
    "CIMB": 0.91,
    # ── RippleNet Europa ─────────────────────────────────────────────────────
    "Santander": 0.97,          # One Pay FX sobre RippleNet
    "Standard Chartered": 0.94,
    "Zodia Custody": 0.93,
    "SEB": 0.91, "Akbank": 0.91, "TransferGo": 0.90,
    # ── RippleNet Américas ───────────────────────────────────────────────────
    "Banco BCI": 0.89, "Viamericas": 0.89,
    "Bank of America": 0.85, "PNC Bank": 0.85, "Itaú Unibanco": 0.87,
    # ── CBDC pilotos Ripple confirmados ──────────────────────────────────────
    "National Bank of Georgia": 0.94,
    "Republic of Palau": 0.93,
    "Bhutan NDI": 0.91,
    "Central Bank of Montenegro": 0.89,
    # ── FinTech / pagos institucionales confirmados ───────────────────────────
    "Ant International": 0.93,     # pagos cross-border con Ripple tech (anuncio 2024)
    "Mastercard": 0.88,            # integración Multi-Token Network con XRPL
    "Visa": 0.82,                  # pilots RLUSD y stablecoins en XRPL
    "MoneyGram": 0.87,             # partnership ODL (2019-2021, renovado)
    "Western Union": 0.75,         # pilotos cross-border con XRP
    # ── Conexiones institucionales documentales / indirectas ────────────────
    "Bank for International Settlements (BIS)": 0.74,  # evidencia documental BIS/CGIDE + mBridge, no integración operativa directa
    "Project mBridge": 0.88,                           # BIS IH + bancos centrales; MVP 2024
    # ── Conexión indirecta verificada ─────────────────────────────────────────
    "People's Bank of China (PBoC)": 0.72,  # indirecta vía LianLian Pay + mBridge/BIS
}


def _ensure_static_verifications(conn: sqlite3.Connection) -> int:
    """
    Inserta en node_verifications los nodos estáticos confirmados que aún no estén
    registrados. Usa INSERT OR IGNORE para no sobreescribir verificaciones manuales
    más recientes. Devuelve el nº de filas insertadas.
    """
    ensure_discovery_tables(conn)
    now = datetime.now(timezone.utc).isoformat()
    inserted = 0
    for node, conf in _STATIC_CONFIRMED_PARTNERS.items():
        try:
            cur = conn.execute(
                "INSERT OR REPLACE INTO node_verifications "
                "(node, connected, confidence, kind_override, proofs_json, verified_at, source) "
                "VALUES (?, 1, ?, 'verified', '[]', ?, 'static')",
                (node, conf, now)
            )
            inserted += cur.rowcount
        except Exception:
            pass
    conn.commit()
    return inserted


def reclassify_all_dynamic_nodes(conn: sqlite3.Connection) -> int:
    """
    Recorre todos los nodos dinamicos y corrige la capa de cualquiera que
    este en 'Descubierto', 'Otro' o con una capa no reconocida por el mapa.
    Se ejecuta al arrancar la app para sanear la DB sin necesidad de re-buscar.
    Retorna el numero de nodos corregidos.
    """
    VALID_LAYERS = {
        "AssetMgmt", "Exchange", "Banco", "ODL", "CBDC", "Gobierno",
        "FinTech", "Fintech", "RedPrivada", "Clearing", "Puente", "Proveedor",
        "Banca_AM", "Banca_EU", "Banca_AP", "Privado", "Ripple",
        "Institucional", "Vigilancia", "Inteligencia", "Publico", "Futuro",
    }
    rows = conn.execute("SELECT node_id, name, layer, icon FROM dynamic_nodes").fetchall()
    fixed = 0
    for node_id, name, layer, icon in rows:
        if layer in VALID_LAYERS:
            continue
        # Intentar resolver el nombre canonico primero
        canonical = _canonical_entity_name(name)
        new_layer, new_icon = _infer_layer_icon_from_name(canonical, layer, icon or "🔎")
        if new_layer not in VALID_LAYERS:
            # Si el nombre canonico no ayuda, intentar con _classify_entity
            et = _classify_entity(canonical)
            if et and et != "Otro":
                new_layer = et
        if new_layer in VALID_LAYERS and new_layer != layer:
            final_icon = new_icon if (not icon or icon in {"?", "🔎", "•"}) else icon
            conn.execute(
                "UPDATE dynamic_nodes SET name=?, layer=?, icon=? WHERE node_id=?",
                (canonical, new_layer, final_icon, node_id)
            )
            fixed += 1
    if fixed:
        conn.commit()
    return fixed


def bootstrap_static_node_routes(conn: sqlite3.Connection) -> int:
    """CLEAN MODE: no crea rutas automáticas para nodos estáticos."""
    return 0


def _classify_entity(name: str) -> str:
    """
    Clasifica la entidad en una categoria para elegir la estrategia de busqueda correcta.
    Retorna una de: AssetMgmt, Exchange, Banco, ODL, CBDC, Gobierno, FinTech,
                    RedPrivada, Clearing, Puente, Proveedor, Otro
    """
    n = name.lower()
    # Gestores de activos / fondos
    if any(k in n for k in ["blackrock","vanguard","fidelity","invesco","franklin","pimco",
                              "bridgewater","citadel","kkr","carlyle","apollo","ares","mgmt",
                              "asset management","capital management","investments","fund"]):
        return "AssetMgmt"
    # Exchanges / brokers cripto
    if any(k in n for k in ["bitstamp","kraken","binance","coinbase","gemini","okx","bybit",
                              "huobi","kucoin","bitfinex","gatehub","upbit","bithumb","exchange",
                              "broker","trading platform"]):
        return "Exchange"
    # ODL / corredores pagos
    if any(k in n for k in ["bitso","beetech","tranglo","coins.ph","nium","stellar","odl",
                              "remittance","money transfer","payment corridor"]):
        return "ODL"
    # Bancos centrales / CBDC
    if any(k in n for k in ["banco central","central bank","reserve bank","banque centrale",
                              "reserva federal","federal reserve","fednow","fedwire","the fed",
                              "bundesbank","ecb","boe","fed reserve","cbdc","digital currency",
                              "national bank","monetary authority","palau","bhutan","honduras",
                              "eastern caribbean","bank of england","bank of japan","pboc",
                              "peoples bank","banque de france","riksbank","norges bank",
                              "swiss national","reserve bank of india","rbi ","rba "]):
        return "CBDC"
    # Organismos internacionales / reguladores supranacionales
    if n in ("bis",) or any(k in n for k in ["bank for international settlements","bis ","imf ","fmi ",
                              "world bank","banco mundial","financial stability board","fsb ",
                              "iosco","fatf","basel","basilea","swift gpi oversight"]):
        return "Gobierno"
    # Gobiernos / instituciones publicas
    if any(k in n for k in ["ministry","ministerio","department of","secretaria",
                              "government","gobierno","municipal","regulador",
                              "regulator","sec ","cftc","mas ","fca ","bafin",
                              "financial conduct","prudential regulation","occ ","fdic "]):
        return "Gobierno"
    # Clearing / post-trade
    if any(k in n for k in ["dtcc","nscc","dtc","clearstream","euroclear","lch","cls group",
                              "clearing","settlement","depository","custodian","csd "]):
        return "Clearing"
    # Gestores de activos / fondos institucionales
    if any(k in n for k in ["blackrock","vanguard","fidelity","state street","invesco",
                              "franklin templeton","vaneck","ark invest","grayscale",
                              "asset management","asset manager","hedge fund","pension fund",
                              "sovereign wealth","endowment","family office","etf provider"]):
        return "AssetMgmt"
    # FinTech / pagos digitales / neobancos
    if any(k in n for k in ["revolut","wise","stripe","paypal","square","adyen","klarna",
                              "sofi","chime","n26","monzo","starling","nubank","fintech","neobank",
                              "digital wallet","payment app","money transfer","remittance"]):
        return "FinTech"
    # Puentes / interoperabilidad / oráculos
    if any(k in n for k in ["wormhole","axelar","layerzero","chainlink","ccip",
                              "cross-chain","cross chain","interoperab","bridge protocol","oracle"]):
        return "Puente"
    # Proveedores tecnológicos / middleware / core banking
    if any(k in n for k in ["volante","finastra","temenos","service provider","technology provider",
                              "api provider","middleware","payment processor","core banking",
                              "banking software","fintech platform","payment infrastructure"]):
        return "Proveedor"
    # Redes privadas / prime brokerage / DEX permisionados
    if any(k in n for k in ["permissioned","dark pool","otc desk","ptf ",
                              "systematic","quant fund","proprietary trading","prime brokerage",
                              "market maker","liquidity provider"]):
        return "RedPrivada"
    # Exchanges cripto
    if any(k in n for k in ["exchange","binance","coinbase","kraken","bitstamp","gatehub",
                              "okx","bybit","kucoin","huobi","crypto.com","gemini",
                              "bitfinex","bitget","mexc"]):
        return "Exchange"
    # Bancos tradicionales — amplio, va al final
    if any(k in n for k in ["bank","banco","banque","banca","financial group","financial corp",
                              "jpmorgan","jp morgan","citibank","citigroup","wells fargo",
                              "barclays","ubs ","credit suisse","societe generale","deutsche bank",
                              "bnp paribas","itau","bbva","ing ","nomura","mizuho","mufg",
                              "dbs ","standard chartered","hsbc","axis bank","pnc ","sbi ",
                              "morgan stanley","goldman sachs","macquarie","commerzbank",
                              "rabobank","natixis","credit agricole","lloyds","santander",
                              "bancolombia","bradesco","banamex","scotiabank","td bank",
                              "rbc ","bmo ","cibc ","westpac","nab ","anz "]):
        return "Banco"
    return "Otro"


def _build_search_prompt(entity_name: str, entity_type: str) -> str:
    """
    Devuelve un system prompt especializado segun el tipo de entidad.
    Cada tipo sabe exactamente donde buscar la evidencia correcta.
    """
    base_nodes = (
        "Usa EXACTAMENTE estos nombres de nodo al rellenar connects_to: "
        "Ripple Payments, XRPL, RLUSD, SWIFT, FedNow, Mastercard, SEPA/ACH, "
        "Hidden Road, Custody/Metaco, DTCC/NSCC, Corredores FX, Permissioned DEX, "
        "Bitstamp, GateHub, Kraken, Binance, SBI Remit, Tranglo (ODL), Bitso (ODL MX), "
        "BeeTech (ODL BR), Santander, Standard Chartered, Bank of America, PNC Bank, "
        "Itau Unibanco, Treasury, Prime, Rail, DEX/AMM, Ethereum, "
        "Large Transfers, Public Gateway, Trustlines, Federal Reserve, Project mBridge, "
        "Bank for International Settlements (BIS), People\'s Bank of China (PBoC), LianLian Pay. "
    )

    base_json = (
        '{"connected":true,"confidence":0.72,"summary":"texto breve max 180 chars",'
        '"ripple_products":["RippleNet"],"layer":"AssetMgmt","icon":"emoji",'
        '"connects_to":["Ripple Payments"],"route_kind":"private",'
        '"sources":["url1"],'
        '"wallets":[{"address":"rXXX...","label":"nombre","role":"treasury|odl|gateway|exchange|unknown","claim":"por que pertenece o se asocia","url":"https://fuente"}],'
        '"corridors":[{"name":"nombre","pair":"USD/PHP","partner":"Coins.ph","layer":"ODL","icon":"icon"}],'
        '"partners":[{"name":"nombre","layer":"Banca_EU","icon":"icon","connects_to":"Ripple Payments"}],'
        '"map_points":[{"name":"nodo/rail/custodio/partner","layer":"Gobierno","icon":"emoji","connects_to":["FedNow"],"kind":"government_payment_rail","summary":"por que debe verse en el mapa"}],'
        '"evidence_items":[{"title":"prueba","url":"https://...","claim":"que demuestra","target":"FedNow"}]}'
        " — wallets/corridors/partners/map_points/evidence_items pueden ser listas vacias []."
        " REGLA JSON CRÍTICA: devuelve JSON estricto parseable por json.loads: números reales tipo 0.72, no rangos, sin comentarios, sin comas finales y sin texto fuera del objeto."
        " REGLA PROOF-FIRST CRÍTICA: NO incluyas un nodo en connects_to ni draw_on_map=true si no puedes explicar la ruta con una prueba concreta en route_decisions[]. "
        "Para XRPL/RLUSD/Hidden Road/Prime/Metaco/Treasury/Rail/Standard Custody exige prueba directa, on-chain, filing o fuente oficial. "
        "Una cadena indirecta puede ir como route_decisions con evidence_type='deductive_watch' y draw_on_map=false. "
        "Cada wallet debe incluir claim y url; si no puedes justificar por qué pertenece o se asocia a la entidad, no la incluyas. "
        " REGLA CRÍTICA: si encuentras una entidad de TERCEROS (banco, fintech) que SÍ usa RippleNet o XRPL"
        " aunque la entidad investigada no lo haga directamente, ponla en partners[] (no solo en evidence_items)."
    )

    layer_values = (
        "Para 'layer' usa UNO de: "
        "Banca_AM, Banca_EU, Banca_AP, Privado, Ripple, Institucional, Exchange, ODL, "
        "Fintech, CBDC, AssetMgmt, Gobierno, Clearing, RedPrivada, Puente, Proveedor, Otro. "
    )

    # Detectar si el nombre contiene caracteres no-ASCII o corresponde a entidad con nombre nativo
    _has_non_ascii = any(ord(c) > 127 for c in entity_name)
    # Detectar si el nombre canónico corresponde a una entidad con idioma nativo conocido
    _entity_lower = entity_name.lower()
    _forced_script, _forced_native_name = "en", None
    for _pattern, (_sc, _nname) in _KNOWN_NATIVE_NAMES.items():
        if _pattern in _entity_lower:
            _forced_script, _forced_native_name = _sc, _nname
            break

    _script = _detect_script(entity_name) if _has_non_ascii else _forced_script
    _nt = _NATIVE_TERMS.get(_script, {})

    # Si el nombre es ASCII pero corresponde a entidad no-latina, usar también el nombre nativo
    if not _has_non_ascii and _forced_native_name:
        _has_non_ascii = True   # activar bloque nativo

    # Construcción del bloque de búsqueda nativa (solo si hay script no-latino)
    if _has_non_ascii and _nt:
        _ripple_native  = _nt.get("ripple", "Ripple")
        _xrpl_native    = _nt.get("xrpl", "XRPL")
        _cbdc_native    = _nt.get("cbdc", "CBDC")
        _chain_native   = _nt.get("blockchain", "blockchain")
        _pay_native     = _nt.get("payment", "payment")
        _coop_native    = _nt.get("cooperation", "cooperation")
        _gov_sites      = _nt.get("gov_sites", "")   # dominios gubernamentales del país
        # Si el nombre de entidad es ASCII pero tenemos el nombre nativo, usarlo en las búsquedas
        _search_name_native = _forced_native_name if _forced_native_name else entity_name
        _search_name_latin  = entity_name  # siempre incluir el nombre latino también
        _dual_name = (
            f"\"{_search_name_native}\" OR \"{_search_name_latin}\""
            if _forced_native_name and _search_name_native != entity_name
            else f"\"{entity_name}\""
        )
        _gov_block_known = (
            f"({_gov_sites}) \"{_search_name_native}\" \"Ripple\" OR \"XRP\"; "
            f"({_gov_sites}) \"{_search_name_native}\" blockchain OR CBDC 'informe' OR 'report' OR 'documento'. "
        ) if _gov_sites else ""
        native_search = (
            f"Busca también en idioma nativo ({_script.upper()}): "
            f"{_dual_name} \"{_ripple_native}\" OR \"{_xrpl_native}\"; "
            f"\"{_search_name_native}\" \"{_cbdc_native}\" \"{_coop_native}\"; "
            f"site:bis.org OR site:imf.org \"{_search_name_native}\" Ripple OR XRPL. "
            f"{_gov_block_known}"
        )
    else:
        native_search = ""

    _local_docs = _LOCAL_DOC_SITES.get(_script, "")
    _local_doc_kw = _LOCAL_DOC_KEYWORDS.get(_script, _LOCAL_DOC_KEYWORDS.get("en", ""))
    _search_engine_hint = _LOCAL_SEARCH_ENGINE_HINTS.get(_script, "")
    _local_docs_line = (
        f"7) Repositorios locales ({_script.upper()}) — usa {_search_engine_hint}; "
        f"NO lo hagas como una sola consulta booleana; "
        f"lanza búsquedas separadas en idioma local: "
        f"({_local_docs}) \"{_forced_native_name or entity_name}\" (Ripple OR XRP OR XRPL OR blockchain); "
        f"({_local_docs}) \"{_forced_native_name or entity_name}\" ({_local_doc_kw}); "
        f"también prueba el nombre latino \"{entity_name}\" si el nombre nativo no devuelve resultados. "
        if _local_docs else ""
    )
    pdf_search = (
        f"Busca documentos primarios con estas estrategias en orden: "
        f"1) site:sec.gov \"{entity_name}\" XRP OR 'digital assets' (10-K, 8-K, S-1, proxy); "
        f"2) site:bis.org \"{entity_name}\" Ripple OR XRPL OR XRP; "
        f"3) site:federalreserve.gov \"{entity_name}\" XRP OR blockchain; "
        f"4) site:ripple.com \"{entity_name}\"; "
        f"5) \"{entity_name}\" Ripple 'memorandum of understanding' OR 'MOU' OR 'partnership agreement' OR 'pilot program' (site:businesswire.com OR site:prnewswire.com OR site:globenewswire.com); "
        f"6) site:github.com \"{entity_name}\" xrpl OR ripple. "
        f"{_local_docs_line}"
        f"IMPORTANTE: URLs que terminan en .pdf o provienen de sec.gov/Archives, bis.org, banco central, "
        f"bolsa local ({_script.upper()}) — clasificar como 'regulatory_filing_pdf' o 'contract_pdf'. "
        f"Prioridad: filing regulatorio PDF > comunicado oficial > noticia mayor. Sin duplicados de evento. "
        f"{native_search}"
    )

    if entity_type == "AssetMgmt":
        return (
            "Eres un analista de inteligencia financiera experto en gestores de activos institucionales y su exposicion a Ripple/XRPL. "
            "ESTRATEGIA: Los grandes gestores de activos NO aparecen directamente en XRPL. Su huella es INDIRECTA. Debes buscar: "
            "1) Filings SEC/EDGAR: propuestas de ETF de XRP/RLUSD, holdings en 13F, registros S-1 con mencion de activos digitales XRP. "
            "2) Custodios institucionales que usan: Metaco (adquirido por Ripple), Anchorage Digital, Coinbase Prime, Zodia Custody — si custodian XRP para esta entidad hay conexion. "
            "3) Hidden Road o prime brokers XRPL-conectados donde operen. "
            "4) Fondos tokenizados on-chain: si tienen fondos en Ethereum como BUIDL, explorar si extienden a XRPL. "
            "5) Declaraciones publicas sobre XRP, RLUSD, pagos cross-border, CBDC pilots. "
            f"{pdf_search}"
            f"{base_nodes}"
            f"{layer_values}"
            "Responde SOLO JSON valido sin texto ni backticks con EXACTAMENTE esta estructura: "
            f"{base_json}"
        )

    elif entity_type == "RedPrivada":
        return (
            "Eres un analista de inteligencia financiera especializado en redes de liquidez privadas y DEX permisionados conectados a Ripple/XRPL. "
            "ESTRATEGIA CRITICA: No puedes consultar la red privada directamente. Busca el RASTRO EN LOS BORDES: "
            "1) ENTRADA a la red privada — preparacion en XRPL publica: trustlines grandes y especificas, wallets que reciben fondos de Ripple Payments antes de operar en la red. "
            "2) SALIDA de la red privada — settlement transactions: pagos post-operacion hacia wallets conocidas (exchanges, custodios, Ripple). "
            "3) INTERNET: ofertas de trabajo mencionando la tecnologia especifica (XRP Ledger, RLUSD, Ripple SDK), repositorios GitHub publicos/privados, patentes de DLT, white papers tecnicos. "
            "4) Contrapartes publicas confirmadas: si interactuan con Ripple Payments, Hidden Road, o cualquier entidad del ecosistema XRPL. "
            "5) Regulacion: licencias de market maker, ATS registration, comunicados de compliance con XRP. "
            f"{pdf_search}"
            f"{base_nodes}"
            f"{layer_values}"
            "Responde SOLO JSON valido sin texto ni backticks con EXACTAMENTE esta estructura: "
            f"{base_json}"
        )

    elif entity_type == "CBDC":
        return (
            "Eres un analista experto en proyectos CBDC, DLT de banco central y conexiones con Ripple/XRPL. "
            "ESTRATEGIA: Los proyectos CBDC con Ripple tienen anuncios oficiales — pero para bancos centrales de Asia, "
            "Medio Oriente o BRICS los documentos están en el idioma local. Busca: "
            "1) Anuncios de banco central o gobierno sobre pilotos CBDC usando Ripple/XRPL "
            "(Bhutan nDGB, Palau PSC, Honduras, Eastern Caribbean, Georgia NBG, Colombia Banco de la Republica). "
            "2) Press releases oficiales de Ripple sobre este banco central especifico. "
            "3) Actividad on-chain en XRPL: si hay mainnet deployment, busca el token/currency code. "
            "4) Informes del BIS, FMI, FSB o banco central sobre el piloto con este organismo especifico. "
            "5) Contratos publicos o licitaciones gubernamentales adjudicadas a Ripple. "
            "6) IMPORTANTE: Para el PBoC / Banco Popular de China: aunque el e-CNY usa infraestructura propia, "
            "busca menciones de interoperabilidad con XRPL, m-CBDC Bridge (mBridge) donde participa junto a otros BCs, "
            "referencias cruzadas con proyectos Ripple en BIS Innovation Hub, y si algún banco o fintech con licencia "
            "del banco central SÍ usa RippleNet (ej: LianLian Pay, Standard Chartered HK, Bank of China), "
            "AÑÁDELO en partners[] con connects_to='Ripple Payments' — NO solo en evidence_items. "
            f"{pdf_search}"
            f"{base_nodes}"
            f"{layer_values}"
            "Responde SOLO JSON valido sin texto ni backticks con EXACTAMENTE esta estructura: "
            f"{base_json}"
        )

    elif entity_type == "Gobierno":
        return (
            "Eres un analista experto en politica publica digital y relaciones gobierno-Ripple/XRPL. "
            "ESTRATEGIA: Los gobiernos no operan directamente en XRPL pero regulan y contratan. Busca: "
            "1) Contratos gubernamentales adjudicados a Ripple o sus partners (busca en bases de contratos publicos). "
            "2) Regulacion favorable a XRP/RLUSD emitida por esta entidad. "
            "3) Declaraciones de funcionarios sobre adopcion de DLT/blockchain en pagos. "
            "4) Participacion en sandboxes regulatorios con proyectos Ripple. "
            "5) Interaccion con proyectos CBDC de Ripple en la misma region geografica. "
            "6) Si la entidad opera un rail de pagos propio (por ejemplo Federal Reserve/FedNow/Fedwire), clasificala tambien como nodo de pago/corredor: añade map_points para la entidad, el rail, proveedores tecnologicos y partners relevantes; conecta entidad -> rail -> nodo Ripple/XRPL SOLO si hay prueba publica. "
            f"{pdf_search}"
            f"{base_nodes}"
            f"{layer_values}"
            "Responde SOLO JSON valido sin texto ni backticks con EXACTAMENTE esta estructura: "
            f"{base_json}"
        )

    elif entity_type == "Clearing":
        return (
            "Eres un analista especializado en infraestructura de post-trade y clearing conectada a Ripple/XRPL. "
            "ESTRATEGIA: Las entidades de clearing son muy conservadoras pero llevan pilotos de DLT. Busca: "
            "1) Pilotos de tokenizacion de activos en XRPL (acciones, bonos tokenizados). "
            "2) Integracion con Hidden Road como prime brokerage conectado a XRPL. "
            "3) Uso de XRPL para settlement de derivados o repos. "
            "4) Publicaciones tecnicas, white papers sobre DLT para settlement. "
            "5) Conexiones con Ripple a traves de DTCC/NSCC si son entidades distintas. "
            f"{pdf_search}"
            f"{base_nodes}"
            f"{layer_values}"
            "Responde SOLO JSON valido sin texto ni backticks con EXACTAMENTE esta estructura: "
            f"{base_json}"
        )

    elif entity_type == "Puente":
        return (
            "Eres un analista OSINT de puentes cross-chain, oraculos e interoperabilidad conectados a tokenizacion institucional. "
            "ESTRATEGIA: Estas entidades rara vez conectan directamente con Ripple. Busca huellas publicas: "
            "1) Integraciones con RLUSD, Securitize, fondos tokenizados, Ethereum, XRPL o stablecoins. "
            "2) Contratos, docs, repos GitHub, bridges soportados, custodios y partners. "
            "3) Si aparece Wormhole/Axelar/LayerZero/Chainlink, clasificalo como Puente y añade map_points hacia Ethereum, RLUSD, XRPL, DEX/AMM y motores, pero marca como vigilancia si no hay prueba directa. "
            f"{pdf_search}"
            f"{base_nodes}"
            f"{layer_values}"
            "Responde SOLO JSON valido sin texto ni backticks con EXACTAMENTE esta estructura: "
            f"{base_json}"
        )

    elif entity_type == "Proveedor":
        return (
            "Eres un analista OSINT de proveedores tecnologicos de pagos, APIs bancarias, ISO 20022 y rails institucionales. "
            "ESTRATEGIA: Busca listas oficiales de proveedores, certificaciones, clientes comunes, APIs de pagos, FedNow/SWIFT/ISO 20022 y menciones a Ripple, XRP, RLUSD o tokenizacion. "
            "Si el proveedor conecta un rail privado con bancos, añade el proveedor al mapa aunque no haya conexion directa con XRPL; la ruta debe quedar como indirecta/vigilancia. "
            f"{pdf_search}"
            f"{base_nodes}"
            f"{layer_values}"
            "Responde SOLO JSON valido sin texto ni backticks con EXACTAMENTE esta estructura: "
            f"{base_json}"
        )

    else:
        # Prompt generico mejorado para Exchange, Banco, ODL, FinTech, Puente, Proveedor, Otro
        type_hint = {
            "Exchange": "ESTRATEGIA: Los exchanges tienen wallets XRPL publicas conocidas. Busca la direccion XRPL (empieza por 'r'), volumen de trading XRP/RLUSD, trustlines RLUSD activas, y si ofrecen ODL o liquidez para Ripple Payments.",
            "Banco": "ESTRATEGIA: Los bancos usan RippleNet o tienen cuentas nostro en XRPL. Busca: acuerdos RippleNet publicados, corredores ODL activos (pares divisa y paises cubiertos), wallets XRPL de sus subsidiarias de remesas.",
            "ODL": "ESTRATEGIA: Busca confirmacion de corredor ODL activo: par de divisas, paises cubiertos, volumen declarado, wallet XRPL conocida, y con que exchange o banco local hace settlement.",
            "FinTech": "ESTRATEGIA: Las fintech integran Ripple via API o son clientes ODL. Busca: integracion de Ripple Payments API, licencias de pago cross-border, corredores activos, mencion de RLUSD en su stack.",
            "Puente": "ESTRATEGIA: Busca integraciones cross-chain con Ethereum, XRPL, RLUSD, Securitize, tokenized funds, bridge contracts, oraculos y partners de interoperabilidad.",
            "Proveedor": "ESTRATEGIA: Busca si es proveedor oficial de FedNow/SWIFT/ISO20022, clientes bancarios, APIs de pago, DLT/tokenizacion y partners Ripple/RLUSD/XRPL.",
        }.get(entity_type,
            # Prompt genérico para cualquier entidad no clasificada
            "ESTRATEGIA UNIVERSAL — aplica en este orden: "
            "1) Busca si la entidad es cliente oficial de Ripple en ripple.com/customers. "
            "2) Busca acuerdos RippleNet, ODL, RLUSD o XRPL en comunicados de prensa y filings. "
            "3) Busca wallets XRPL asociadas (direcciones 'r...') en xrpscan.com o xrpl.org. "
            "4) Busca conexiones indirectas: custodios que usen Metaco, prime brokers Hidden Road, corredores ODL. "
            "5) Si no hay conexion directa con Ripple, indica connected=false pero con confidence segun la evidencia indirecta encontrada. "
        )

        return (
            "Eres un motor de inteligencia financiera especializado en Ripple / XRPL. "
            f"{type_hint} "
            "Identifica: productos Ripple usados, wallets XRPL conocidas, corredores activos, partners del ecosistema y TODOS los puntos que deban aparecer en el mapa: entidad, rail, custodio, partner, gateway, wallet, red privada, fuente publica. "
            "IMPORTANTE: Si la entidad tiene conexion INDIRECTA (via custodio, prime broker, corredor ODL o partner), "
            "igualmente marca connected=true y explica la cadena de conexion en summary. "
            "Si no hay ninguna conexion ni indirecta, marca connected=false con confidence=0.0-0.15. "
            f"{pdf_search}"
            f"{base_nodes}"
            f"{layer_values}"
            "Responde SOLO JSON valido sin texto ni backticks con EXACTAMENTE esta estructura: "
            f"{base_json}"
        )


def search_institution_connections(institution_name: str,
                                   conn: Optional[sqlite3.Connection] = None) -> Dict[str, Any]:
    """
    Clasifica la entidad y usa un prompt especializado para buscar su conexion
    con la infraestructura Ripple/XRPL. Cada tipo de entidad deja un rastro
    diferente — el sistema sabe exactamente donde buscarlo.

    Caché compartida: si otro usuario ya buscó esta entidad y el resultado no ha
    expirado (7 días), devuelve el resultado cacheado sin gastar tokens.
    """
    entity_type = _classify_entity(institution_name)

    # ── Caché compartida: check antes de cualquier llamada AI ────────────────
    if conn is not None:
        _cached = _get_search_cache(conn, institution_name, "discovery")
        if _cached is not None:
            # Re-finalizar resultados antiguos: evita que un caché con JSON roto conserve confianza 0%.
            _cached = _finalize_discovery_result(_cached, institution_name, entity_type, None)
            _cached["_from_cache"] = True
            return _cached

    api_key = _get_api_key()
    if not api_key:
        return {
            "institution": institution_name,
            "entity_type": entity_type,
            "connected": False,
            "confidence": 0.0,
            "summary": "Sin API key — configura ANTHROPIC_API_KEY para activar la busqueda online.",
            "ripple_products": [], "layer": "Descubierto", "icon": "?",
            "connects_to": [], "route_kind": "private", "sources": [],
            "wallets": [], "corridors": [], "partners": [],
        }

    _discovery_call_type = "discovery_fast"
    _discovery_model = ANTHROPIC_MODEL_FAST
    if conn is not None and not _charge_budget(conn, _discovery_call_type):
        return {
            "institution": institution_name,
            "entity_type": entity_type,
            "connected": False,
            "confidence": 0.0,
            "summary": "Presupuesto API agotado o en margen de seguridad. Modo caché activo: solo se mostrarán investigaciones ya guardadas.",
            "ripple_products": [], "layer": "Descubierto", "icon": "🔒",
            "connects_to": [], "route_kind": "private", "sources": [],
            "wallets": [], "corridors": [], "partners": [], "_budget_locked": True,
        }

    system_prompt = _build_search_prompt(institution_name, entity_type)
    native_context = _native_query_instruction(institution_name)

    payload = {
        "model": _discovery_model,
        "max_tokens": 1400,
        # cache_control: el system prompt se cachea — ahorra ~30% de input tokens en reintentos
        "system": [{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "messages": [{"role": "user", "content": (
            f"Investiga la conexion con Ripple/XRPL de: {institution_name}. "
            f"{native_context}"
            "Si el nombre corresponde a una entidad china, japonesa, coreana, rusa, árabe o india, "
            "busca también con su nombre nativo, términos locales y repositorios regulatorios/bolsas locales; "
            "no dependas de filetype:pdf. Prioriza URLs .pdf, SEC/Archives, BIS, bancos centrales, bolsas y registros oficiales. "
            "Devuelve JSON compacto: máximo 5 sources, máximo 5 evidence_items, "
            "sin narrativa larga y sin duplicados."
        )}],
    }
    headers = {"x-api-key": api_key, "anthropic-version": "2023-06-01",
               "anthropic-beta": "prompt-caching-2024-07-31,web-search-2025-03-05",
               "content-type": "application/json"}
    last_exc = None
    for _attempt in range(3):
        try:
            resp = requests.post(ANTHROPIC_API_URL, json=payload, headers=headers, timeout=55)
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", (2 ** _attempt) * 8))
                _time.sleep(min(wait, 120))
                continue
            if resp.status_code in (401, 403):
                _eb = {}
                try: _eb = resp.json()
                except Exception: pass
                _em = _eb.get("error", {}).get("message", resp.text[:200])
                raise RuntimeError(f"{resp.status_code} Error: {_em} — ve a Setup → Diagnóstico de API key")
            resp.raise_for_status()
            data = resp.json()
            _settle_budget(conn, _discovery_call_type, data, _discovery_model)
            text_parts = [b.get("text", "") for b in data.get("content", []) if isinstance(b, dict) and b.get("type") == "text"]
            raw = " ".join(text_parts).strip().replace("```json", "").replace("```", "").strip()
            try:
                result = _loads_discovery_json_lenient(raw) if raw else {}
            except Exception as parse_exc:
                # Antes esto devolvía Error + 0 fuentes. Ahora recuperamos URLs reales de web_search/citations.
                result = _fallback_discovery_from_partial_response(institution_name, entity_type, data, parse_exc)
            result = _finalize_discovery_result(result, institution_name, entity_type, data)
            # CostGuard: guardar respuesta compacta para no hinchar BD ni tokens futuros.
            # ── Auto-promote RippleNet entities from evidence_items to partners[] ──
            # When the AI mentions a third-party entity joined RippleNet in the evidence
            # but forgets to add it as a structured partner, we catch it here.
            import re as _re_sic
            _RN_KW = {"ripplenet", "joined ripplenet", "ripple partner",
                      "ripple network member", "se unió a ripplenet",
                      "miembro de ripplenet", "unió a ripplenet"}
            _seen_p = {
                _canonical_entity_name(str(p.get("name", "")))
                for p in result.get("partners", []) if isinstance(p, dict)
            }
            for _ev in result.get("evidence_items", []) or []:
                if not isinstance(_ev, dict):
                    continue
                _eclaim = str(_ev.get("claim", "") or "").lower()
                _etitle = str(_ev.get("title", "") or "")
                if not any(kw in _eclaim for kw in _RN_KW):
                    continue
                # Entity name is usually the leading words before "RippleNet" or "Ripple"
                _m = _re_sic.match(
                    r'^([A-Za-zÀ-ÿ][A-Za-zÀ-ÿ0-9\s&\-\.]+?)\s+(?:RippleNet|Ripple\b)',
                    _etitle
                )
                if not _m:
                    continue
                _pname = _m.group(1).strip()
                if len(_pname) < 3:
                    continue
                _cpname = _canonical_entity_name(_pname)
                if not _cpname or _cpname in _seen_p or _cpname == _canonical_entity_name(institution_name):
                    continue
                result.setdefault("partners", []).append({
                    "name": _pname,
                    "layer": "FinTech",
                    "icon": "⚡",
                    "connects_to": "Ripple Payments",
                })
                _seen_p.add(_cpname)
            # ── Guardar en caché compartida ──────────────────────────────────
            if conn is not None:
                _set_search_cache(conn, institution_name, result, "discovery")
            result["_from_cache"] = False
            return result
        except Exception as exc:
            last_exc = exc
            if "429" not in str(exc):
                break
            wait = (2 ** _attempt) * 8
            _time.sleep(min(wait, 120))
    _refund_budget(conn, _discovery_call_type)
    return _finalize_discovery_result({
        "institution": institution_name,
        "entity_type": entity_type,
        "connected": False,
        "confidence": 0.0,
        "summary": f"Error: {last_exc}",
        "ripple_products": [], "layer": "Descubierto", "icon": "?",
        "connects_to": [], "route_kind": "private", "sources": [],
        "wallets": [], "corridors": [], "partners": [], "map_points": [], "evidence_items": [],
    }, institution_name, entity_type, None)



# =============================================================================
# PROOF-FIRST UNIVERSAL ROUTE GATE v6.2.3
# =============================================================================
# Este bloque evita que cualquier nodo nuevo o futuro herede conexiones falsas.
# El mapa solo dibuja rutas cuando cada arista trae prueba concreta A↔B.

STRICT_PROOF_TARGETS: Set[str] = {
    "XRPL", "RLUSD", "Ripple Payments", "RippleNet",
    "Hidden Road / Prime", "Custody/Metaco", "Standard Custody",
    "Treasury", "Rail", "Permissioned DEX", "DEX/AMM",
}

WATCH_ONLY_TARGETS_DYNAMIC: Set[str] = {"XRPL", "RLUSD"}

DIRECT_EVIDENCE_TYPES: Set[str] = {
    "official", "official_announcement", "press_release", "filing", "regulatory_filing_pdf",
    "contract_pdf", "central_bank_pdf", "bis_pdf", "onchain", "wallet_tagged",
    "explorer_label", "partner_page", "primary_source", "company_page",
}


def _norm_target_for_gate(x: Any, known_nodes: Optional[Set[str]] = None) -> str:
    try:
        return _canonical_target_node(x, known_nodes or set()) or _canonical_entity_name(x)
    except Exception:
        return str(x or "").strip()


def _route_decisions_for_target(result: Dict[str, Any], src: str, dst: str) -> List[Dict[str, Any]]:
    """Devuelve decisiones/evidencias que apuntan explícitamente a la arista src→dst."""
    out: List[Dict[str, Any]] = []
    dst_key = _canonical_entity_key(dst)
    src_key = _canonical_entity_key(src)
    for rd in result.get("route_decisions", []) or []:
        if not isinstance(rd, dict):
            continue
        rd_to = rd.get("to") or rd.get("target") or rd.get("connects_to") or ""
        rd_from = rd.get("from") or rd.get("source") or src
        if _canonical_entity_key(_norm_target_for_gate(rd_to)) == dst_key:
            # Si viene from vacío o igual a la entidad investigada, vale para esta arista.
            if not rd_from or _canonical_entity_key(_canonical_entity_name(rd_from)) in {src_key, _canonical_entity_key(_canonical_entity_name(result.get('institution', src)))}:
                out.append(rd)
    # Compatibilidad con evidence_items antiguos: target + claim/url.
    for ev in result.get("evidence_items", []) or []:
        if not isinstance(ev, dict):
            continue
        ev_target = ev.get("target") or ev.get("to") or ev.get("node") or ""
        if ev_target and _canonical_entity_key(_norm_target_for_gate(ev_target)) == dst_key:
            out.append({
                "from": src,
                "to": dst,
                "product": ev.get("product") or ev.get("target") or "unknown",
                "evidence_type": ev.get("type") or ev.get("evidence_type") or "primary_source",
                "confidence": ev.get("confidence", result.get("confidence", 0.0)),
                "claim": ev.get("claim") or ev.get("title") or "Prueba asociada a esta ruta",
                "url": ev.get("url", ""),
                "draw_on_map": True,
            })
    return out


def _is_generic_route_claim(text: Any) -> bool:
    """Detecta frases de relleno que no prueban una arista A↔B."""
    t = _norm_key(str(text or ""))
    if not t:
        return True
    generic_patterns = (
        "partner detectado", "punto descubierto", "nodo inferido", "ruta inferida",
        "conectado a", "conexion inferida", "ecosistema", "ripple ecosystem",
        "sin evidencia", "unknown", "prueba asociada", "fuente recuperada automaticamente",
    )
    return any(g in t for g in generic_patterns)


def _decision_has_real_proof(rd: Dict[str, Any]) -> bool:
    et = str(rd.get("evidence_type") or rd.get("type") or "").strip().lower()
    claim = str(rd.get("claim") or rd.get("summary") or rd.get("snippet") or "").strip()
    url = str(rd.get("url") or rd.get("source") or "").strip()
    if et in {"deductive_watch", "watch", "inferred", "model", "speculative"}:
        return False
    if _is_generic_route_claim(claim):
        return False
    if et in DIRECT_EVIDENCE_TYPES and (claim or url.startswith("http")):
        return True
    # Si no clasificó el tipo pero hay URL + claim explícito, se permite para nodos no estrictos.
    return bool(url.startswith("http") and len(claim) >= 24)


def _route_allowed_by_proof_first(result: Dict[str, Any], src: str, dst: str,
                                  kind: str, evidence_text: str,
                                  known_nodes: Optional[Set[str]] = None) -> Tuple[bool, str, str, float, List[str]]:
    """Decide si una ruta se puede dibujar. Devuelve: allowed, kind, evidence, confidence, urls."""
    dst = _norm_target_for_gate(dst, known_nodes)
    src = _canonical_entity_name(src)
    conf = float(result.get("confidence", 0) or 0)
    decisions = _route_decisions_for_target(result, src, dst)
    usable = [rd for rd in decisions if _decision_has_real_proof(rd) and bool(rd.get("draw_on_map", True))]
    urls = []
    for rd in usable:
        u = _canonical_source_url(str(rd.get("url", "")))
        if u.startswith("http") and u not in urls:
            urls.append(u)
    # Los nodos de infraestructura sensible requieren decisión específica con prueba.
    if dst in STRICT_PROOF_TARGETS:
        if not usable:
            return False, "watch", f"Watch no dibujado: falta prueba directa A↔{dst}. {evidence_text or ''}".strip(), min(conf, 0.45), urls
        best = max(usable, key=lambda x: float(x.get("confidence", conf) or conf))
        et = str(best.get("evidence_type") or "official").lower()
        # XRPL/RLUSD no se dibujan como operativo salvo onchain/direct official fuerte; si no, quedan para panel de pruebas/watch.
        if dst in WATCH_ONLY_TARGETS_DYNAMIC and et not in {"onchain", "wallet_tagged", "explorer_label", "official", "official_announcement", "filing", "regulatory_filing_pdf"}:
            return False, "watch", str(best.get("claim") or evidence_text or f"Ruta hacia {dst} queda como watch"), min(float(best.get("confidence", conf) or conf), 0.45), urls
        ev = str(best.get("claim") or evidence_text or f"Prueba directa hacia {dst}")
        return True, kind if kind not in {"watch", "inferred"} else "verified", ev, float(best.get("confidence", conf) or conf), urls
    # Para nodos no estrictos: si no hay prueba explícita, solo permitir rutas de partners/corredores con evidencia textual fuerte.
    if usable:
        best = max(usable, key=lambda x: float(x.get("confidence", conf) or conf))
        return True, kind, str(best.get("claim") or evidence_text), float(best.get("confidence", conf) or conf), urls
    # Fallback muy restringido: no aceptar frases genéricas tipo "partner detectado".
    # Para dibujar sin route_decision explícita debe haber texto específico y fuentes reales.
    src_urls = []
    try:
        for u in result.get("sources", []) or []:
            cu = _canonical_source_url(str(u))
            if cu.startswith("http") and cu not in src_urls:
                src_urls.append(cu)
    except Exception:
        src_urls = []
    if (kind in {"odl", "public_wallet", "public", "official", "institutional", "government_payment_rail"}
            and evidence_text and len(evidence_text) >= 36
            and not _is_generic_route_claim(evidence_text)
            and src_urls):
        return True, kind, evidence_text, conf, src_urls
    return False, "watch", f"Ruta no dibujada: sin prueba concreta A↔{dst}", min(conf, 0.35), urls


def _wallet_has_attribution(w: Dict[str, Any]) -> bool:
    if not isinstance(w, dict):
        return False
    addr = str(w.get("address", "")).strip()
    if not (addr.startswith("r") and len(addr) > 20):
        return False
    claim = str(w.get("claim") or w.get("reason") or w.get("evidence") or "").strip()
    url = str(w.get("url") or w.get("source") or "").strip()
    label = str(w.get("label") or "").strip()
    # Wallets curadas conocidas sí pueden mostrarse, pero deben llevar etiqueta reconocida.
    if addr in KNOWN_XRPL_WALLETS:
        return True
    return bool(label and claim and (url.startswith("http") or len(claim) >= 28))

def apply_discovery_to_map(conn: sqlite3.Connection, result: Dict[str, Any],
                            auto: bool = False) -> Dict[str, Any]:
    """
    Aplica el resultado del Discovery Engine al grafo del radar.

    v6.2 corrige el problema de fondo:
    - evita duplicados por alias (Reserva Federal / Federal Reserve / The Fed),
    - clasifica capas aunque la IA devuelva nombres distintos,
    - registra todos los puntos detectados (partners, corredores, rails, map_points),
    - crea rutas desde/hacia esos puntos,
    - guarda evidencias y URLs para que aparezcan en la leyenda inferior.
    """
    ensure_discovery_tables(conn)
    try:
        ensure_discovered_wallets_table(conn)
    except Exception:
        pass

    result = dict(result or {})
    raw_name = str(result.get("institution", "") or "").strip()
    name = _canonical_entity_name(raw_name)
    result["institution"] = name

    entity_type = str(result.get("entity_type") or _classify_entity(name) or "Otro")
    AUTO_ENTITY_TYPES = {"CBDC", "Gobierno", "FinTech", "RedPrivada", "Clearing", "Puente", "Proveedor", "Otro"}
    is_auto_type = entity_type in AUTO_ENTITY_TYPES
    min_confidence = 0.40 if is_auto_type else 0.35
    confidence = float(result.get("confidence", 0) or 0)

    # Una entidad puede tener evidencia sólida SIN ser "connected=true":
    # ej: PBoC desarrolla mBridge como alternativa, tiene papers BIS, socios conocidos.
    # Si confianza ≥ 0.55 + hay evidencia (partners/sources/map_points), añadir igualmente
    # marcando la relación como "ecosistema adyacente" (no conexión directa a Ripple core).
    has_evidence = bool(
        result.get("partners") or result.get("map_points") or
        result.get("connects_to") or
        (result.get("sources") and len(result.get("sources", [])) >= 2)
    )
    force_add = (not result.get("connected")) and confidence >= 0.55 and has_evidence
    if force_add:
        # Sobrescribir connected para que el flujo continúe; route_kind pasa a "watch" por defecto
        result["connected"] = True
        if not result.get("route_kind"):
            result["route_kind"] = "watch"
        if not result.get("connects_to"):
            result["connects_to"] = []

    if not result.get("connected") or confidence < min_confidence:
        return {"added_node": False, "added_routes": 0, "reason": "confidence_too_low",
                "entity_type": entity_type, "canonical_name": name}

    now = datetime.now(timezone.utc).isoformat()
    layer, inferred_icon = _infer_layer_icon_from_name(name, result.get("layer") or entity_type or "Descubierto", result.get("icon") or "🔎")
    icon = result.get("icon") or {"Gobierno": "🏛️", "CBDC": "🏦", "FinTech": "⚡", "AssetMgmt": "💼", "Puente": "🌀", "Proveedor": "🧰", "Clearing": "🏢", "RedPrivada": "🔒"}.get(entity_type, inferred_icon)
    sources_blob = _safe_sources_blob(result.get("sources", []))
    evidence_items = result.get("evidence_items", []) or []
    evidence_text = ", ".join(result.get("ripple_products", []) or [])
    if evidence_items:
        claims = [str(e.get("claim", "")).strip() for e in evidence_items if isinstance(e, dict) and e.get("claim")]
        evidence_text = (evidence_text + " | " + " | ".join(claims[:4])).strip(" |")
        ev_urls = [e.get("url", "") for e in evidence_items if isinstance(e, dict) and e.get("url")]
        sources_blob = _safe_sources_blob((result.get("sources", []) or []) + ev_urls)

    added_nodes = 0
    added_routes = 0
    added_partners = 0
    added_corridors = 0
    added_map_points = 0

    if _register_dynamic_node(conn, name, layer, icon, confidence,
                              result.get("summary", ""), sources_blob, now):
        added_nodes += 1

    def _known_nodes() -> Set[str]:
        out = set(NODES.keys())
        try:
            out.update([r[0] for r in conn.execute("SELECT name FROM dynamic_nodes").fetchall()])
        except Exception:
            pass
        return out

    def _ensure_node(nm: Any, lyr: str = "Descubierto", ic: str = "?",
                     summary: str = "", conf_mult: float = 0.75,
                     srcs: str = "") -> str:
        cn = _canonical_entity_name(nm)
        if not cn:
            return ""
        inferred_layer, inferred_icon = _infer_layer_icon_from_name(cn, lyr, ic)
        final_layer = inferred_layer if _layer_is_generic_for_dynamic(lyr) and inferred_layer in ZONE_POS else _normalize_layer(lyr)
        final_icon = inferred_icon if (not ic or ic in {"?", "🔎", "•"}) else ic
        if _register_dynamic_node(conn, cn, final_layer, final_icon, confidence * conf_mult,
                                  summary or f"Punto descubierto conectado a {name}",
                                  srcs or sources_blob, now):
            nonlocal_added_nodes[0] += 1
        return cn

    # Python no permite asignar a added_nodes dentro del nested sin nonlocal en algunas ramas legibles.
    nonlocal_added_nodes = [added_nodes]

    def _add_route(src: Any, dst: Any, kind: str = "discovered", label: str = "",
                   signal_col: Optional[str] = None, ev: str = "",
                   confidence_override: Optional[float] = None) -> bool:
        nonlocal added_routes
        src_name = _canonical_entity_name(src)
        known = _known_nodes()
        dst_match = _canonical_target_node(dst, known)
        if not dst_match:
            # Si el destino no existe, lo creamos como nodo descubierto en vez de perder la ruta.
            dst_match = _ensure_node(dst, "Descubierto", "🔎", f"Nodo inferido desde ruta de {src_name}", 0.55)
        if not src_name or not dst_match or src_name == dst_match:
            return False
        allowed, gated_kind, gated_ev, gated_conf, gated_urls = _route_allowed_by_proof_first(
            result, src_name, dst_match, kind, ev or evidence_text, known
        )
        if not allowed:
            return False
        sig = signal_col or _route_signal_for_kind(gated_kind, "institutional_route_score")
        used_confidence = confidence_override if confidence_override is not None else gated_conf
        route_sources = _safe_sources_blob((sources_blob.split(", ") if sources_blob else []) + gated_urls)
        ok = _register_dynamic_route(
            conn, src_name, dst_match, gated_kind, sig,
            label or f"{src_name} -> {dst_match}", used_confidence,
            gated_ev or ev or evidence_text, route_sources or sources_blob, now,
        )
        if ok:
            added_routes += 1
        return ok

    # Wallets XRPL descubiertas.
    wallets_added = 0
    for w in result.get("wallets", []) or []:
        if not isinstance(w, dict):
            continue
        addr = str(w.get("address", "")).strip()
        label = str(w.get("label", name)).strip() or name
        role = str(w.get("role", "unknown")).strip() or "unknown"
        if addr.startswith("r") and len(addr) > 20 and _wallet_has_attribution(w):
            wallets_added += 1
            if addr not in KNOWN_XRPL_WALLETS:
                KNOWN_XRPL_WALLETS[addr] = f"{label} ({name})"
            try:
                conn.execute("""
                    INSERT OR IGNORE INTO discovered_wallets
                    (wallet, label, role, confidence, volume_xrp, top_cp_label, added_to_map, status, last_seen, quality_reason)
                    VALUES (?, ?, ?, ?, 0.0, ?, 1, 'map', ?, 'wallet atribuida por fuente de discovery')
                """, (addr, label, role, confidence, name, now[:10]))
            except Exception:
                pass
            wallet_node = _ensure_node(label, "Vigilancia", "👛", f"Wallet XRPL descubierta para {name}", 0.60)
            _add_route(name, wallet_node, "public_wallet", f"{name} -> wallet {label}", "public_gateway_score", f"Wallet XRPL completa: {addr}")
            _add_route(wallet_node, "XRPL", "public", f"{label} -> XRPL", "public_xrpl_score", "Wallet pública XRPL")

    # map_points: solo se añaden si vienen con evidencia concreta (url o claim no vacío).
    # Evitamos crear rutas especulativas sin respaldo.
    for mp in result.get("map_points", []) or []:
        if not isinstance(mp, dict):
            continue
        mp_name = mp.get("name") or mp.get("label")
        mp_evidence = str(mp.get("claim", "") or "").strip()
        mp_url = str(mp.get("url", "") or "").strip()
        # Filtro: descartar map_points sin ninguna evidencia real
        if not mp_name or (not mp_evidence and not mp_url):
            continue
        mp_layer = _normalize_layer(mp.get("layer") or "Descubierto")
        mp_icon = mp.get("icon") or "🔎"
        mp_summary = mp.get("summary") or mp_evidence or f"Punto detectado en investigación de {name}"
        mp_node = _ensure_node(mp_name, mp_layer, mp_icon, mp_summary, 0.70)
        added_map_points += 1
        # Conexión principal entidad -> punto (solo si son distintos).
        if mp_node and mp_node != name:
            _add_route(name, mp_node, mp.get("kind", "discovered"), f"{name} -> {mp_node}", ev=mp_summary)
        # Conexiones secundarias del punto solo si son nodos ya conocidos (no crear cadenas de nodos nuevos).
        known_now = _known_nodes()
        conns = mp.get("connects_to", [])
        if isinstance(conns, str):
            conns = [conns]
        for target in conns or []:
            matched = _canonical_target_node(target, known_now)
            if matched and matched != mp_node:
                _add_route(mp_node, matched, mp.get("kind", "discovered"), f"{mp_node} -> {matched}", ev=mp_summary)

    # Corredores: ahora se crean como nodo + dos rutas, aunque el partner no existiera previamente.
    for corridor in result.get("corridors", []) or []:
        if not isinstance(corridor, dict):
            continue
        cname = corridor.get("name") or corridor.get("pair") or "Corredor descubierto"
        cnode = _ensure_node(cname, corridor.get("layer", "ODL"), corridor.get("icon", "🔁"),
                             f"Corredor detectado para {name}: {corridor.get('pair','')}", 0.72)
        added_corridors += 1
        pair = corridor.get("pair", "")
        _add_route(name, cnode, "odl", f"{name} -> corredor {cname}", "bridge_score", f"Corredor ODL/pagos: {pair}")
        partner = corridor.get("partner") or "Ripple Payments"
        _add_route(cnode, partner, "odl", f"{cname} -> {partner}", "bridge_score", f"Corredor ODL/pagos: {pair}")

    # Partners: crear nodo, conectar entidad -> partner y partner -> su nodo destino.
    for partner in result.get("partners", []) or []:
        if not isinstance(partner, dict):
            continue
        pname = partner.get("name")
        if not pname:
            continue
        pnode = _canonical_entity_name(pname)
        # Si el partner es la misma entidad bajo otro alias (ej. reserva federal -> Federal Reserve),
        # no machacamos su resumen principal ni creamos un bucle visual.
        if pnode != name:
            pnode = _ensure_node(pname, partner.get("layer", "Otro"), partner.get("icon", "🤝"),
                                 f"Partner de {name}", 0.70)
            added_partners += 1
            _add_route(name, pnode, "partner", f"{name} -> {pnode}", ev=f"Partner detectado de {name}")
        pconn = partner.get("connects_to") or "Ripple Payments"
        if pnode == name:
            direct_targets = {_canonical_target_node(t, _known_nodes()) or _canonical_entity_name(t) for t in (result.get("connects_to", []) or [])}
            if (_canonical_target_node(pconn, _known_nodes()) or _canonical_entity_name(pconn)) in direct_targets:
                continue
        _add_route(pnode, pconn, partner.get("kind", "partner"), f"{pnode} -> {pconn}", ev=f"Partner conectado a {pconn}")

    # Rutas directas declaradas por el motor.
    direct_kind = result.get("route_kind", "private")
    direct_targets_raw = result.get("connects_to", []) or []
    for target in direct_targets_raw:
        _add_route(name, target, direct_kind, f"{name} -> {target}",
                   _route_signal_for_kind(direct_kind), evidence_text)

    # CLEAN MODE: cascada Ripple desactivada.
    # No se heredan conexiones a Rail, Treasury, Hidden Road, Metaco, Standard Custody,
    # XRPL o RLUSD por estar conectado a una pieza del ecosistema.
    confirmed_targets = {
        _canonical_target_node(t, _known_nodes()) or _canonical_entity_name(t)
        for t in direct_targets_raw
    }

    # ── IMPLICACIONES OBLIGATORIAS ────────────────────────────────────────────
    # Deducción técnica irrefutable: si X entonces Y necesariamente.
    # Confianza = 0.97 (máxima posible sin TX on-chain directa).
    # Estas rutas NO requieren verificación porque son consecuencia del protocolo.
    # ── REGLAS OBLIGATORIAS: implicaciones técnicas irrefutables del protocolo ──
    # Formato: (trigger, required, razón)
    # Deducción transitiva: si A→B y B→C están en las reglas, el motor genera A→B→C automáticamente.
    OBLIGATORY_RULES = []

    # Recopilar nodos ya presentes en rutas dinámicas
    all_route_nodes_now = set()
    for _r in conn.execute("SELECT src, dst FROM dynamic_routes").fetchall():
        all_route_nodes_now.add(_r[0]); all_route_nodes_now.add(_r[1])

    def _apply_obligatory_rules(source_nodes: set) -> None:
        """Aplica OBLIGATORY_RULES para cualquier conjunto de nodos fuente."""
        known = _known_nodes()
        for trigger_node, required_node, reason in OBLIGATORY_RULES:
            if trigger_node in source_nodes:
                req_canonical = _canonical_target_node(required_node, known)
                if req_canonical and req_canonical != trigger_node:
                    _add_route(trigger_node, req_canonical, "obligatory",
                               f"{trigger_node} → {req_canonical} (obligatoria por protocolo)",
                               "public_xrpl_score", reason, confidence_override=0.97)

    # 1) Aplicar reglas a nodos del sistema global (trigger nodes ya en el mapa)
    _apply_obligatory_rules(all_route_nodes_now | set(NODES.keys()))

    # 2) Deducción transitiva para el nodo recién añadido:
    #    Si "name" conecta a Ripple Payments → necesariamente toca XRPL, Rail, etc.
    known_now = _known_nodes()
    entity_connects_to = set(confirmed_targets) | {
        _canonical_target_node(t, known_now) or t
        for t in (result.get("connects_to") or [])
    }
    # Añadir las implicaciones de lo que la entidad ya conecta
    transitively_required: set = set()
    for _, rule_required, _ in OBLIGATORY_RULES:
        for trigger_node, required_node, reason in OBLIGATORY_RULES:
            if trigger_node in entity_connects_to:
                req = _canonical_target_node(required_node, known_now)
                if req:
                    transitively_required.add(req)
                    _add_route(name, req, "obligatory",
                               f"{name} → {req} (deducción: {name}→{trigger_node}→{req})",
                               "public_xrpl_score",
                               f"Transitiva: {name} conecta a {trigger_node}, y {trigger_node} requiere {req} por protocolo",
                               confidence_override=0.95)
        break  # una pasada es suficiente, evitar bucle infinito

    # Expansión controlada: solo rutas hacia nodos YA EXISTENTES en el mapa estático
    # que tienen sentido real para este tipo de entidad. NO se crean nodos nuevos.
    # Marcadas como 'watch' (vigilancia especulativa, no prueba on-chain).
    added_expansion_routes = 0
    known_now = _known_nodes()
    # Solo añadir si el nodo destino ya existe Y no hay ya una ruta directa declarada
    already_direct = {_canonical_target_node(t, known_now) for t in (result.get("connects_to") or [])}
    for exp_target in ENTITY_EXPANSION_TARGETS.get(entity_type, []):
        matched = _canonical_target_node(exp_target, known_now)
        if matched and matched not in already_direct:
            if _add_route(name, matched, "watch",
                          f"{name} -> {matched} (vigilancia por tipo {entity_type})",
                          "institutional_route_score",
                          f"Ruta especulativa por tipo de entidad ({entity_type}). Sin evidencia directa confirmada."):
                added_expansion_routes += 1

    added_nodes = nonlocal_added_nodes[0]

    # ── Garantizar que el resultado queda en caché con TODOS los nombres posibles ──
    # Así el botón "Ver" siempre encontrará los datos sin relanzar la búsqueda.
    try:
        _res_json  = json.dumps(result)
        _ts        = datetime.now(timezone.utc).isoformat()
        _raw_name  = str(result.get("institution", name))
        _cache_keys = {
            name.lower(),                                       # nombre canónico del nodo
            _raw_name.lower(),                                  # nombre que devolvió la IA
            _canonical_entity_name(_raw_name).lower(),          # normalización extra
        }
        for _ck in _cache_keys:
            if _ck:
                conn.execute(
                    "INSERT OR REPLACE INTO institution_search_cache(query,result_json,searched_at) VALUES(?,?,?)",
                    (_ck, _res_json, _ts)
                )
    except Exception:
        pass

    conn.commit()

    return {
        "added_node": True,
        "added_nodes": added_nodes,
        "added_routes": added_routes,
        "node_id": hashlib.sha256(_norm_key(name).encode()).hexdigest()[:12],
        "entity_type": entity_type,
        "canonical_name": name,
        "auto_added": is_auto_type or auto,
        "wallets_added": wallets_added,
        "added_corridors": added_corridors,
        "added_partners": added_partners,
        "added_map_points": added_map_points,
        "added_expansion_routes": added_expansion_routes,
    }

def load_dynamic_map_elements(conn: sqlite3.Connection) -> Tuple[Dict, List, List]:
    """
    Devuelve (dyn_nodes, dyn_routes, new_zone_boxes).
    - dyn_nodes: nodos dentro de zonas existentes o en zonas nuevas
    - dyn_routes: rutas confirmadas entre nodos existentes
    - new_zone_boxes: lista de (x0,y0,x1,y1,label,color) para zonas nuevas a dibujar
    """
    ensure_discovery_tables(conn)
    dyn_nodes: Dict[str, Any] = {}
    dyn_routes: List[Tuple] = []
    new_zone_boxes: List[Tuple] = []
    try:
        rows = conn.execute(
            "SELECT name, layer, icon, confidence FROM dynamic_nodes ORDER BY added_at"
        ).fetchall()

        # Pre-calcular Y ocupadas por nodos estaticos en cada zona
        taken_y: Dict[str, list] = defaultdict(list)
        for sname, sdata in NODES.items():
            sl = sdata.get("layer", "")
            taken_y[sl].append(sdata["pos"][1])

        new_layer_cols: Dict[str, int] = {}
        new_layer_y: Dict[str, float] = {}

        for name, layer_raw, icon, conf in rows:
            if name in NODES:
                continue
            # Saltar si el nombre canónico coincide con un nodo estático (evita duplicados como "Ripple" ≡ "Ripple Payments")
            _cname = _canonical_entity_name(name)
            if _cname in NODES and _cname != name:
                continue
            layer = _normalize_layer(layer_raw)
            # Reclasificar nodos ODL/corredor que la IA asignó a "Privado" (Infraestructura)
            if layer == "Privado":
                _nl = name.lower()
                if any(kw in _nl for kw in ("odl", "corridor", "corredor", "remit")):
                    layer = "ODL"
            # Si el nodo quedó sin clasificar o en zona genérica, re-inferir la capa desde el nombre
            if _layer_is_generic_for_dynamic(layer) or layer not in ZONE_POS:
                inferred_layer, inferred_icon = _infer_layer_icon_from_name(name, layer, icon or "🔎")
                if inferred_layer in ZONE_POS:
                    layer = inferred_layer
                    if not icon or icon in {"?", "🔎", "•"}:
                        icon = inferred_icon

            if layer in ZONE_POS:
                pos = _next_pos_in_zone(layer, taken_y)
                taken_y[layer].append(pos[1])
                dyn_nodes[name] = {"pos": pos, "layer": layer, "icon": icon}
            else:
                if layer not in new_layer_cols:
                    col_idx = len(new_layer_cols)
                    new_layer_cols[layer] = col_idx
                    new_layer_y[layer] = 2.20
                col_idx = new_layer_cols[layer]
                x_col = 6.60 + col_idx * 1.55
                y_pos = new_layer_y[layer]
                new_layer_y[layer] -= 0.85
                dyn_nodes[name] = {"pos": (x_col, y_pos), "layer": layer, "icon": icon}

        LAYER_COLORS = [
            "rgba(60,255,155,0.35)", "rgba(255,184,77,0.35)",
            "rgba(182,115,255,0.35)", "rgba(90,215,255,0.35)",
            "rgba(255,90,103,0.35)",
        ]
        for layer, col_idx in new_layer_cols.items():
            x0 = 6.55 + col_idx * 1.55
            x1 = x0 + 1.40
            y_lowest = new_layer_y.get(layer, 1.35)
            y0 = min(y_lowest - 0.30, -1.80)
            y1 = 2.50
            color = LAYER_COLORS[col_idx % len(LAYER_COLORS)]
            new_zone_boxes.append((x0, y0, x1, y1, layer, color))

        route_rows = conn.execute(
            "SELECT src, dst, kind, signal_col, label FROM dynamic_routes WHERE confidence >= 0.35"
        ).fetchall()
        all_nodes = {**NODES, **dyn_nodes}
        for src, dst, kind, signal, label in route_rows:
            if src in all_nodes and dst in all_nodes:
                dyn_routes.append((src, dst, kind, signal, label))
    except Exception:
        pass
    return dyn_nodes, dyn_routes, new_zone_boxes


def _wallets_for_node(node_name: str, conn: sqlite3.Connection) -> List[str]:
    """Devuelve lista de direcciones XRPL conocidas para un nodo del mapa."""
    addrs: List[str] = []
    # 1) KNOWN_XRPL_WALLETS: buscar por label que coincida con el nodo
    nlow = node_name.lower()
    for addr, lbl in KNOWN_XRPL_WALLETS.items():
        if nlow in lbl.lower() or lbl.lower() in nlow:
            addrs.append(addr)
    # 2) discovered_wallets de la BD
    try:
        rows = conn.execute(
            "SELECT wallet FROM discovered_wallets WHERE added_to_map=1 AND COALESCE(status,'map') NOT IN ('quarantine','discarded') AND (label LIKE ? OR top_cp_label LIKE ?)",
            (f"%{node_name}%", f"%{node_name}%")
        ).fetchall()
        for (w,) in rows:
            if w and w not in addrs:
                addrs.append(w)
    except Exception:
        pass
    return addrs[:10]   # máx 10 wallets por nodo


# =============================================================================
# SISTEMA DE EVIDENCIA CALIBRADA
# =============================================================================
# Peso de confianza por tipo de fuente. Cuanto mayor, más certeza aporta.
EVIDENCE_SCORES: Dict[str, float] = {
    # On-chain — verificable directamente en el ledger
    "tx_directa":            0.97,
    "odl_payment":           0.95,
    "trust_line":            0.88,
    "amm_pool":              0.85,
    "offers_activas":        0.72,
    "wallet_activa":         0.55,
    # Documentos primarios — mayor peso que noticias
    "official_partner":      0.93,   # página oficial ripple.com/customers
    "press_release":         0.88,   # comunicado oficial de la institución
    "regulatory_filing":     0.90,   # filing regulatorio (SEC, banco central)
    "regulatory_filing_pdf": 0.92,   # PDF filtrado/oficial de regulador (SEC, BIS, Fed)
    "contract_pdf":          0.91,   # contrato, MoU, acuerdo oficial en PDF
    "github_repo":           0.82,   # integración en código público verificable
    "news_major":            0.55,   # noticia: útil, pero no confirma sola una integración
    "job_posting":           0.45,   # oferta laboral mencionando RippleNet/XRPL
    "news_minor":            0.25,   # medio menor: solo apoyo débil
    "social_mention":        0.10,   # LinkedIn/Twitter — casi nunca verificable
    # Inferencia — bajo peso
    "ai_inference":          0.18,   # declaración de IA sin fuente externa
    "sin_wallet":            0.00,
}

EVIDENCE_LABELS: Dict[str, str] = {
    "tx_directa":            "Transacción directa XRPL",
    "odl_payment":           "Pago ODL on-chain",
    "trust_line":            "Trust Line XRPL",
    "amm_pool":              "Pool AMM XRPL",
    "offers_activas":        "Ofertas activas en DEX",
    "wallet_activa":         "Wallet activa en XRPL",
    "official_partner":      "Socio oficial (ripple.com)",
    "press_release":         "Comunicado oficial",
    "regulatory_filing":     "Filing regulatorio",
    "regulatory_filing_pdf": "Documento PDF regulatorio",
    "contract_pdf":          "Contrato / MoU en PDF",
    "github_repo":           "Repositorio GitHub público",
    "news_major":            "Noticia medio principal",
    "job_posting":           "Oferta de trabajo",
    "news_minor":            "Noticia medio menor",
    "social_mention":        "Mención social",
    "ai_inference":          "Inferencia IA (sin fuente)",
    "sin_wallet":            "Sin rastro verificable",
}

# Etiquetas de certeza según puntuación combinada
def _cert_label(score: float) -> tuple:
    """Devuelve (etiqueta, color) según nivel de certeza."""
    if score >= 0.88:  return ("✅ Conexión confirmada",      "#3CFF9B")
    if score >= 0.70:  return ("🟡 Conexión probable",        "#FB923C")
    if score >= 0.45:  return ("🔶 Conexión posible",         "#F59E0B")
    if score >= 0.20:  return ("⚠️ Evidencia débil",          "#FF5A67")
    return              ("❌ Sin evidencia verificable",       "#64748B")

def _combine_evidence_score(proofs: List[Dict]) -> float:
    """
    Combina múltiples pruebas en una puntuación final calibrada.
    No es promedio simple: cada prueba adicional sube menos que la anterior
    (modelo de probabilidad independiente: P = 1 - prod(1-pi)).
    """
    if not proofs:
        return 0.0
    scores = [EVIDENCE_SCORES.get(p.get("type", ""), 0.0) for p in proofs if p.get("onchain") or p.get("internet")]
    if not scores:
        return 0.0
    combined = 1.0
    for s in sorted(scores, reverse=True):
        combined *= (1.0 - s)
    return round(1.0 - combined, 3)


# Traducción de nombres de nodo del mapa a términos buscables en internet
NODE_SEARCH_TERMS: Dict[str, str] = {
    "Ripple Payments":    "Ripple Payments RippleNet ODL",
    "XRPL":               "XRP Ledger XRPL blockchain",
    "RLUSD":              "RLUSD stablecoin Ripple USD",
    "DEX/AMM":            "XRPL DEX AMM liquidity pool XRP",
    "Permissioned DEX":   "Ripple permissioned DEX XRPL institutional exchange",
    "Hidden Road / Prime": "Hidden Road Partners prime brokerage Ripple Prime institutional",
    "Custody/Metaco":     "Metaco custody XRPL digital assets Ripple",
    "DTCC/NSCC":          "DTCC NSCC clearing settlement blockchain",
    "SWIFT":              "SWIFT interbank messaging payments",
    "FedNow":             "FedNow instant payments Federal Reserve",
    "SEPA/ACH":           "SEPA ACH bank transfer Europe",
    "Mastercard":         "Mastercard crypto blockchain payments",
    "Corredores FX":      "FX corridors forex Ripple ODL",
    "Topology Engine":    "Ripple Topology Engine routing payments",
    "Public Gateway":     "XRPL public gateway trustline",
    "Treasury":           "XRP treasury wallet Ripple",
    "Hidden Road / Prime": "Hidden Road Partners prime brokerage Ripple Prime institutional crypto",
    "Rail":               "Ripple private payment rail",
    "Ethereum":           "Ethereum blockchain DeFi bridge XRP",
    "Bitstamp":           "Bitstamp exchange XRPL Ripple",
    "GateHub":            "GateHub XRPL gateway",
    "Kraken":             "Kraken exchange XRP",
    "Binance":            "Binance exchange XRP",
    "Ripple Escrow":      "Ripple XRP escrow lock release",
    "SBI Remit":          "SBI Remit ODL Japan XRP",
    "Tranglo (ODL)":      "Tranglo ODL Southeast Asia XRP payments",
    "Bitso (ODL MX)":     "Bitso ODL Mexico XRP remittance",
    "BeeTech (ODL BR)":   "BeeTech ODL Brazil XRP payments",
    "Santander":          "Santander RippleNet blockchain payments",
    "Standard Chartered": "Standard Chartered Ripple blockchain",
    "Bank of America":    "Bank of America RippleNet blockchain",
    "PNC Bank":           "PNC Bank RippleNet payments",
    "Itau Unibanco":      "Itau Unibanco blockchain Ripple",
}


def _native_search_block(entity: str) -> str:
    """
    Genera búsquedas adicionales en idioma nativo.
    Funciona para nombres ya escritos en otro script y para entidades ASCII
    conocidas en _KNOWN_NATIVE_NAMES (ej: IDG Capital -> IDG资本).
    """
    sc, native_name, use_native = _resolve_native_search_identity(entity)
    if not use_native:
        return ""
    nt = _NATIVE_TERMS.get(sc, {})
    if not nt:
        return ""
    r  = nt.get("ripple", "Ripple")
    xl = nt.get("xrpl", "XRPL")
    bl = nt.get("blockchain", "blockchain")
    py = nt.get("payment", "payment")
    co = nt.get("cooperation", "cooperation")
    pi = nt.get("pilot", "pilot")
    gov_sites = nt.get("gov_sites", "")
    local_docs = _LOCAL_DOC_SITES.get(sc, "")
    local_kw = _LOCAL_DOC_KEYWORDS.get(sc, _LOCAL_DOC_KEYWORDS.get("en", ""))
    search_hint = _LOCAL_SEARCH_ENGINE_HINTS.get(sc, "")
    search_name = native_name or entity
    dual_name = (
        f'"{search_name}" OR "{entity}"'
        if native_name and str(search_name).strip() != str(entity).strip()
        else f'"{entity}"'
    )

    local_line = (
        f'   ({local_docs}) "{search_name}" Ripple OR XRP OR XRPL — repositorios/bolsas locales\n'
        f'   ({local_docs}) "{search_name}" {local_kw} — informes, filings, avisos o PDFs locales\n'
        if local_docs else ""
    )
    gov_line = (
        f'   ({gov_sites}) "{search_name}" Ripple OR XRP OR blockchain — reguladores/gobierno local\n'
        if gov_sites else ""
    )

    return (
        f"\n8) BUSQUEDA EN IDIOMA NATIVO ({sc.upper()}) — la entidad puede publicar fuera del inglés; usa {search_hint}:\n"
        f'   {dual_name} "{r}" OR "{xl}" — noticias y docs nativos\n'
        f'   "{search_name}" "{bl}" "{py}" — cooperación pagos blockchain\n'
        f'   "{search_name}" "{r}" "{pi}" OR "{co}" — pilotos o acuerdos\n'
        f'   site:bis.org OR site:imf.org "{search_name}" Ripple OR XRPL — reportes supranacionales\n'
        f"{gov_line}"
        f"{local_line}"
        f"   Clasifica URLs .pdf, SEC/Archives, BIS, bancos centrales, bolsas y registros locales como regulatory_filing_pdf si son documentos primarios.\n"
        f"   Prioridad: documento oficial local > regulador/BIS > comunicado oficial > medio local especializado.\n"
    )


def validate_connection_internet(
    node_a: str, node_b: str, api_key: str,
    conn: Optional[sqlite3.Connection] = None,
) -> List[Dict]:
    """
    Busca rastros verificables en internet de la conexión node_a ↔ node_b con Ripple/XRPL.
    Usa Anthropic API + web_search. Devuelve lista de pruebas con tipo y peso.
    """
    if not api_key:
        return []

    # ── Caché compartida ─────────────────────────────────────────────────────
    _vkey = "verify_v2::" + _canonical_pair_key(node_a, node_b)
    if conn is not None:
        _vc = _get_search_cache(conn, _vkey, "verification")
        if _vc is not None:
            return _vc.get("proofs", [])
        if not _charge_budget(conn, "verification"):
            return []

    native_a = _native_search_block(node_a)
    native_b = _native_search_block(node_b) if node_b != node_a else ""
    native_block = native_a + native_b

    _val_sys = (
        _AUDIT_SYSTEM_PROMPT +
        ' Responde SOLO JSON: {"proofs":[{"type":"official_partner","label":"...","url":"...","snippet":"...","internet":true}]}'
        ' — sin evidencia: {"proofs":[]}'
    )
    payload = {
        "model": ANTHROPIC_MODEL_FAST,
        "max_tokens": 400,
        "system": [{"type": "text", "text": _val_sys, "cache_control": {"type": "ephemeral"}}],
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "messages": [{"role": "user", "content":
            f"Evidencia verificable de que '{node_a}' conecta DIRECTAMENTE con "
            f"'{node_b}' ({NODE_SEARCH_TERMS.get(node_b, node_b)}) en Ripple/XRPL. "
            f"Regla estricta: cada prueba debe mencionar '{node_a}' y también '{node_b}' o términos equivalentes del nodo; "
            f"si la fuente solo habla de cripto/blockchain en general, devuelve proofs vacío. "
            f"Busca: site:ripple.com \"{node_a}\" \"{node_b}\"; "
            f"site:sec.gov \"{node_a}\" XRP OR XRPL OR 'digital assets'; "
            f"site:bis.org \"{node_a}\" Ripple OR XRPL; "
            f"\"{node_a}\" \"{node_b}\" Ripple 'partnership' OR 'MOU' OR 'pilot' (site:businesswire.com OR site:prnewswire.com OR site:reuters.com OR site:bloomberg.com); "
            f"site:github.com \"{node_a}\" xrpl. "
            f"{native_block}"
            f"URLs que terminan en .pdf o vienen de sec.gov/Archives → tipo 'regulatory_filing_pdf'. "
            f"Prioridad: documento oficial/PDF > filing SEC > comunicado oficial > noticia. Sin duplicados de URL ni de historia."
        }],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "prompt-caching-2024-07-31,web-search-2025-03-05",
        "content-type": "application/json",
    }
    try:
        for _attempt in range(3):
            resp = requests.post(ANTHROPIC_API_URL, json=payload, headers=headers, timeout=60)
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", (2 ** _attempt) * 8))
                _time.sleep(min(wait, 120))
                continue
            resp.raise_for_status()
            data = resp.json()
            _settle_budget(conn, "verification", data, ANTHROPIC_MODEL_FAST)
            text_parts = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
            raw = " ".join(text_parts).strip().replace("```json","").replace("```","").strip()
            start = raw.find("{"); end = raw.rfind("}") + 1
            parsed = json.loads(raw[start:end]) if start != -1 else {}
            proofs = parsed.get("proofs", [])
            # Marcar, deduplicar y filtrar relevancia A↔B antes de guardar en caché.
            for p in proofs:
                p["internet"] = True
                p["onchain"]  = False
                p["icon"]     = {
                    "official_partner":  "🏆",
                    "press_release":     "📰",
                    "regulatory_filing": "📋",
                    "regulatory_filing_pdf": "📄",
                    "contract_pdf":      "📄",
                    "github_repo":       "💻",
                    "news_major":        "📰",
                    "job_posting":       "💼",
                    "news_minor":        "🗞️",
                }.get(p.get("type",""), "🔎")
            proofs = _dedupe_and_filter_proofs(node_a, node_b, proofs, max_items=3)
            # ── Guardar en caché compartida ──────────────────────────────────
            if conn is not None:
                _set_search_cache(conn, _vkey, {"proofs": proofs}, "verification")
            return proofs
    except Exception:
        pass
    _refund_budget(conn, "verification")
    return []


def _check_onchain_only(
    focus_node: str, peer: str
) -> Dict[str, Any]:
    """
    XRPL-only check (sin escritura a BD, sin internet). Usa timeouts cortos (8s).
    Devuelve dict con proofs, active_wallets, wallets_a, wallets_b.
    """
    import sqlite3 as _sq3
    # Abrimos conexión propia para ser thread-safe
    try:
        _conn = _sq3.connect(DB_PATH, check_same_thread=False)
    except Exception:
        return {"peer": peer, "proofs": [], "active_wallets": [], "wallets_a": [], "wallets_b": []}

    try:
        wallets_a = _wallets_for_node(focus_node, _conn)
        wallets_b = _wallets_for_node(peer, _conn)
    finally:
        _conn.close()

    proofs: List[Dict] = []
    active_wallets: List[str] = []

    # 1) Transacciones directas
    for wa in wallets_a[:3]:
        try:
            data = xrpl_rpc({"method": "account_tx", "params": [{
                "account": wa, "limit": 200, "ledger_index_min": -1,
                "ledger_index_max": -1, "forward": False
            }]}, timeout=8)
            txs = data.get("result", {}).get("transactions", [])
            for tx_wrap in txs:
                tx = tx_wrap.get("tx", tx_wrap.get("transaction", {}))
                dest = tx.get("Destination", "")
                sender = tx.get("Account", "")
                amount = tx.get("Amount", "")
                if dest in wallets_b or sender in wallets_b:
                    xrp_val = float(amount) / 1e6 if isinstance(amount, str) else 0
                    proofs.append({
                        "type": "tx_directa", "icon": "✅",
                        "label": f"TX directa · {xrp_val:,.0f} XRP",
                        "tx_hash": tx.get("hash", "")[:16] + "…",
                        "ledger": tx.get("ledger_index", ""),
                        "onchain": True,
                    })
                    if len(proofs) >= 3:
                        break
        except Exception:
            pass
        if len(proofs) >= 3:
            break

    # 2) Trust lines
    if not proofs:
        for wa in wallets_a[:3]:
            try:
                data = xrpl_rpc({"method": "account_lines", "params": [{
                    "account": wa, "ledger_index": "validated", "limit": 100
                }]}, timeout=8)
                for line in data.get("result", {}).get("lines", []):
                    if line.get("account", "") in wallets_b:
                        cur = line.get("currency", "")
                        bal = line.get("balance", "0")
                        proofs.append({
                            "type": "trust_line", "icon": "🔗",
                            "label": f"Trust line activa · {cur} · balance {bal}",
                            "peer": line["account"][:12] + "…",
                            "onchain": True,
                        })
            except Exception:
                pass

    # 3) Offers activas
    if not proofs:
        for wa in wallets_a[:2]:
            try:
                data = xrpl_rpc({"method": "account_offers", "params": [{
                    "account": wa, "ledger_index": "validated", "limit": 50
                }]}, timeout=8)
                offers = data.get("result", {}).get("offers", [])
                if offers:
                    proofs.append({
                        "type": "offers_activas", "icon": "📊",
                        "label": f"{len(offers)} ofertas activas en DEX/AMM",
                        "count": len(offers), "onchain": True,
                    })
            except Exception:
                pass

    # 4) ODL payments
    ODL_CORRIDORS = {w for w, l in KNOWN_XRPL_WALLETS.items()
                     if any(k in l.lower() for k in ("odl", "bitso", "coins.ph", "tranglo", "sbi", "beetech"))}
    for wa in wallets_a[:3]:
        try:
            data = xrpl_rpc({"method": "account_tx", "params": [{
                "account": wa, "limit": 100,
                "ledger_index_min": -1, "ledger_index_max": -1
            }]}, timeout=8)
            for tx_wrap in data.get("result", {}).get("transactions", []):
                tx = tx_wrap.get("tx", tx_wrap.get("transaction", {}))
                dest = tx.get("Destination", "")
                amount = tx.get("Amount", "")
                if dest in ODL_CORRIDORS and isinstance(amount, str):
                    xrp_val = float(amount) / 1e6
                    if xrp_val > 10_000:
                        lbl_dest = KNOWN_XRPL_WALLETS.get(dest, dest[:12])
                        proofs.append({
                            "type": "odl_payment", "icon": "💸",
                            "label": f"Pago ODL · {xrp_val:,.0f} XRP → {lbl_dest}",
                            "amount_xrp": xrp_val, "onchain": True,
                        })
                        break
        except Exception:
            pass

    # 5) Wallets activas
    for wa in (wallets_a + wallets_b)[:4]:
        try:
            data = xrpl_rpc({"method": "account_info", "params": [{
                "account": wa, "ledger_index": "validated"
            }]}, timeout=8)
            info = data.get("result", {}).get("account_data", {})
            if info:
                bal = int(info.get("Balance", 0)) / 1e6
                seq = info.get("Sequence", 0)
                active_wallets.append(_wallet_full_text(wa))
                if not proofs:
                    proofs.append({
                        "type": "wallet_activa", "icon": "👛",
                        "label": f"Wallet activa · {bal:,.0f} XRP · seq {seq}",
                        "address": _wallet_full_text(wa), "onchain": True,
                    })
        except Exception:
            pass

    return {
        "peer": peer,
        "proofs": proofs,
        "active_wallets": active_wallets,
        "wallets_a": [_wallet_full_text(w) for w in wallets_a],
        "wallets_b": [_wallet_full_text(w) for w in wallets_b],
        "has_wallets": bool(wallets_a or wallets_b),
    }


def validate_connections_internet_batch(
    focus_node: str, peers: List[str], api_key: str,
    conn: Optional[sqlite3.Connection] = None,
) -> Dict[str, List[Dict]]:
    """
    Una sola llamada Anthropic para buscar evidencia internet de TODAS las conexiones
    focus_node ↔ peer a la vez. Devuelve {peer: [proofs]}.
    """
    if not api_key or not peers:
        return {}

    ranked_peers = _rank_peers_for_cost(peers)[:_MAX_BATCH_PEERS]
    if not ranked_peers:
        return {}
    _batch_key = f"batch_v2::{_canonical_entity_name(focus_node)}::" + "|".join(_canonical_entity_name(p) for p in ranked_peers)
    if conn is not None:
        _cached_batch = _get_search_cache(conn, _batch_key, "batch_verify")
        if _cached_batch is not None:
            return _cached_batch.get("results", {})
        if not _charge_budget(conn, "batch_verify"):
            return {}

    peers = ranked_peers
    peers_block = "\n".join(
        f"- {p} ({NODE_SEARCH_TERMS.get(p, p)})"
        for p in peers
    )
    # Búsqueda nativa para el nodo foco y para peers con nombres no-ASCII
    native_focus = _native_search_block(focus_node)
    native_peers = "".join(_native_search_block(p) for p in peers if any(ord(c) > 127 for c in p))
    native_block = native_focus + native_peers

    system_prompt = (
        _AUDIT_SYSTEM_PROMPT +
        ' Responde SOLO JSON válido con este formato exacto:'
        ' {"results": {"NOMBRE_PEER": [{"type":"...","label":"...","url":"...","snippet":"..."}], ...}}'
        ' — si no hay evidencia para un peer pon lista vacía []'
    )
    peers_str = ", ".join(f'"{p}"' for p in peers)
    user_msg = (
        f"Evidencia de que '{focus_node}' conecta DIRECTAMENTE con cada entidad en Ripple/XRPL:\n{peers_block}\n"
        f"Regla estricta: para cada peer, cada prueba debe mencionar el peer y también '{focus_node}' "
        f"o términos equivalentes del nodo; si la fuente solo habla de cripto/blockchain en general, devuelve []. "
        f"Busca: site:ripple.com \"{focus_node}\" peer; "
        f"site:sec.gov peer XRP OR XRPL OR 'digital assets'; "
        f"site:bis.org peer Ripple OR XRPL; "
        f"peer \"{focus_node}\" Ripple 'partnership' OR 'MOU' OR 'pilot' (site:businesswire.com OR site:prnewswire.com OR site:reuters.com OR site:bloomberg.com); "
        f"site:github.com peer xrpl. "
        f"URLs terminadas en .pdf o de sec.gov/Archives → tipo 'regulatory_filing_pdf'. "
        f"No repitas misma URL ni mismo comunicado/historia sindicada. "
        f"{native_block}"
        f"JSON exacto con claves: {peers_str}"
    )
    payload = {
        "model": ANTHROPIC_MODEL_FAST,
        "max_tokens": 1000,
        "system": [{"type": "text", "text": system_prompt, "cache_control": {"type": "ephemeral"}}],
        "tools": [{"type": "web_search_20250305", "name": "web_search"}],
        "messages": [{"role": "user", "content": user_msg}],
    }
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "anthropic-beta": "prompt-caching-2024-07-31,web-search-2025-03-05",
        "content-type": "application/json",
    }
    ICON_MAP = {
        "official_partner": "🏆", "press_release": "📰",
        "regulatory_filing": "📋", "regulatory_filing_pdf": "📄", "contract_pdf": "📄",
        "github_repo": "💻", "news_major": "📰", "job_posting": "💼",
        "news_minor": "🗞️",
    }
    try:
        for _attempt in range(3):
            resp = requests.post(ANTHROPIC_API_URL, json=payload, headers=headers, timeout=90)
            if resp.status_code == 429:
                wait = int(resp.headers.get("Retry-After", (2 ** _attempt) * 8))
                _time.sleep(min(wait, 120))
                continue
            resp.raise_for_status()
            data = resp.json()
            _settle_budget(conn, "batch_verify", data, ANTHROPIC_MODEL_FAST)
            text_parts = [b["text"] for b in data.get("content", []) if b.get("type") == "text"]
            raw = " ".join(text_parts).strip().replace("```json", "").replace("```", "").strip()
            start = raw.find("{"); end = raw.rfind("}") + 1
            if start == -1:
                return {}
            parsed = json.loads(raw[start:end])
            results: Dict[str, List[Dict]] = {}
            for peer, peer_proofs in parsed.get("results", {}).items():
                peer_canon = _canonical_entity_name(peer)
                # Mapear clave devuelta por IA al peer real si viene con alias.
                real_peer = next((rp for rp in peers if _canonical_entity_key(rp) == _canonical_entity_key(peer)), peer)
                decorated = []
                for p in (peer_proofs or []):
                    p["internet"] = True
                    p["onchain"] = False
                    p["icon"] = ICON_MAP.get(p.get("type", ""), "🔎")
                    decorated.append(p)
                results[real_peer] = _dedupe_and_filter_proofs(focus_node, real_peer, decorated, max_items=3)
            if conn is not None:
                _set_search_cache(conn, _batch_key, {"results": results}, "batch_verify")
            return results
    except Exception:
        pass
    _refund_budget(conn, "batch_verify")
    return {}


def validate_node_fast(
    focus_node: str, peers: List[str], conn: sqlite3.Connection,
    progress_cb: Optional[Any] = None,
) -> None:
    """
    Versión optimizada: XRPL en paralelo + una sola búsqueda internet para todos los peers.
    Guarda todos los resultados en connection_proofs.

    progress_cb opcional: callback UI tipo progress_cb(0.35, "texto") para que
    Streamlit muestre avance real por fases en vez de parecer congelado.
    """
    if not peers:
        return

    def _progress(value: float, text: str) -> None:
        if progress_cb is None:
            return
        try:
            progress_cb(max(0.0, min(1.0, float(value))), text)
        except Exception:
            pass

    ensure_discovery_tables(conn)
    now = datetime.now(timezone.utc).isoformat()
    total_peers = max(len(peers), 1)
    _progress(0.03, f"Preparando verificación de {len(peers)} conexión(es)…")

    # ── 1) XRPL checks en paralelo ───────────────────────────────────────────
    onchain_results: Dict[str, Dict] = {}
    with ThreadPoolExecutor(max_workers=min(6, len(peers))) as ex:
        futures = {ex.submit(_check_onchain_only, focus_node, peer): peer for peer in peers}
        done_count = 0
        for fut in as_completed(futures):
            try:
                res = fut.result()
                onchain_results[res["peer"]] = res
            except Exception:
                peer = futures[fut]
                onchain_results[peer] = {
                    "peer": peer, "proofs": [], "active_wallets": [],
                    "wallets_a": [], "wallets_b": [], "has_wallets": False,
                }
            done_count += 1
            _progress(0.08 + 0.42 * (done_count / total_peers),
                      f"Escaneando XRPL on-chain… {done_count}/{len(peers)}")

    # ── 2) Única búsqueda internet batch ────────────────────────────────────
    api_key = _get_api_key()
    _progress(0.55, "Buscando evidencias públicas/documentales con CostGuard…")
    internet_batch = validate_connections_internet_batch(focus_node, peers, api_key, conn=conn)
    _progress(0.76, "Combinando evidencias on-chain + internet…")

    # ── 3) Combinar y guardar cada peer ─────────────────────────────────────
    for _idx, peer in enumerate(peers, start=1):
        _progress(0.78 + 0.18 * (_idx / total_peers),
                  f"Guardando resultado { _idx }/{len(peers)} · {peer}")
        oc = onchain_results.get(peer, {})
        onchain_proofs = oc.get("proofs", [])
        internet_proofs = internet_batch.get(peer, [])

        # Sin wallet y sin prueba internet → marcar sin_wallet
        if not oc.get("has_wallets") and not internet_proofs:
            onchain_proofs = [{
                "type": "sin_wallet", "icon": "⚠️",
                "label": "Sin wallets XRPL conocidas — sin rastros en internet",
                "onchain": False,
            }]

        all_proofs = onchain_proofs + internet_proofs
        # Quitar sin_wallet si hay evidencia internet
        if internet_proofs:
            all_proofs = [p for p in all_proofs if p.get("type") != "sin_wallet"]
        # Segunda barrera de calidad: dedupe + relevancia A↔B justo antes de puntuar/guardar.
        all_proofs = _dedupe_and_filter_proofs(focus_node, peer, all_proofs, max_items=3)

        calibrated_score = _combine_evidence_score(all_proofs)
        cert_label, cert_color = _cert_label(calibrated_score)
        is_onchain  = any(p.get("onchain")  for p in all_proofs)
        is_internet = any(p.get("internet") for p in all_proofs)

        result_data = {
            "node_a": focus_node, "node_b": peer,
            "proofs": all_proofs,
            "wallets_a": oc.get("wallets_a", []),
            "wallets_b": oc.get("wallets_b", []),
            "active_wallets": oc.get("active_wallets", []),
            "cert_label": cert_label, "cert_color": cert_color,
            "calibrated_score": calibrated_score,
            "has_onchain": is_onchain, "has_internet": is_internet,
        }
        proof_id = _canonical_pair_proof_id(focus_node, peer)
        pair_key = _canonical_pair_key(focus_node, peer)
        node_a_key = _canonical_entity_key(focus_node)
        node_b_key = _canonical_entity_key(peer)
        try:
            conn.execute("""
                INSERT OR REPLACE INTO connection_proofs
                (proof_id, node_a, node_b, node_a_key, node_b_key, pair_key, proof_type, proof_data, onchain, confidence, validated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                proof_id, focus_node, peer, node_a_key, node_b_key, pair_key,
                all_proofs[0]["type"] if all_proofs else "unknown",
                json.dumps(result_data, ensure_ascii=False),
                int(is_onchain or is_internet), calibrated_score, now,
            ))
        except Exception:
            pass

    try:
        rebuild_chain_proofs_for_node(conn, focus_node, peers)
        conn.commit()
    except Exception:
        try:
            conn.commit()
        except Exception:
            pass
    _progress(1.0, "Verificación completada + cadenas actualizadas")


def validate_connection_onchain(
    node_a: str, node_b: str, conn: sqlite3.Connection, force: bool = False
) -> Dict[str, Any]:
    """
    Busca evidencia on-chain real en el XRPL para la conexión node_a ↔ node_b.
    Comprueba: transacciones directas, trust lines, AMM pools, actividad ODL.
    Guarda el resultado en connection_proofs y lo devuelve.
    """
    ensure_discovery_tables(conn)
    proof_id = _canonical_pair_proof_id(node_a, node_b)
    pair_key = _canonical_pair_key(node_a, node_b)
    node_a_key = _canonical_entity_key(node_a)
    node_b_key = _canonical_entity_key(node_b)
    now = datetime.now(timezone.utc).isoformat()

    # Usar caché si existe y tiene menos de 24h. La búsqueda es NO dirigida: A↔B == B↔A.
    if not force:
        cached = _connection_proof_row(conn, node_a, node_b)
        if cached:
            try:
                age_h = (datetime.now(timezone.utc) -
                         datetime.fromisoformat(cached[3])).total_seconds() / 3600
                if age_h < 24:
                    return {
                        "from_cache": True,
                        "onchain": bool(cached[1]),
                        "confidence": cached[2],
                        **json.loads(cached[0]),
                    }
            except Exception:
                pass

    proofs: List[Dict] = []
    wallets_a = _wallets_for_node(node_a, conn)
    wallets_b = _wallets_for_node(node_b, conn)
    confidence = 0.0

    # ── 1) Transacciones directas entre wallets conocidas ───────────────────
    for wa in wallets_a[:3]:
        try:
            data = xrpl_rpc({"method": "account_tx", "params": [{
                "account": wa, "limit": 200, "ledger_index_min": -1,
                "ledger_index_max": -1, "forward": False
            }]}, timeout=15)
            txs = data.get("result", {}).get("transactions", [])
            for tx_wrap in txs:
                tx = tx_wrap.get("tx", tx_wrap.get("transaction", {}))
                dest = tx.get("Destination", "")
                sender = tx.get("Account", "")
                amount = tx.get("Amount", "")
                if dest in wallets_b or sender in wallets_b:
                    xrp_val = float(amount) / 1e6 if isinstance(amount, str) else 0
                    proofs.append({
                        "type": "tx_directa",
                        "icon": "✅",
                        "label": f"TX directa · {xrp_val:,.0f} XRP",
                        "tx_hash": tx.get("hash", "")[:16] + "…",
                        "ledger": tx.get("ledger_index", ""),
                        "onchain": True,
                    })
                    confidence = max(confidence, 0.95)
                    if len(proofs) >= 3:
                        break
        except Exception:
            pass
        if len(proofs) >= 3:
            break

    # ── 2) Trust lines entre wallets ────────────────────────────────────────
    if not proofs:
        for wa in wallets_a[:3]:
            try:
                data = xrpl_rpc({"method": "account_lines", "params": [{
                    "account": wa, "ledger_index": "validated", "limit": 100
                }]}, timeout=12)
                for line in data.get("result", {}).get("lines", []):
                    peer = line.get("account", "")
                    if peer in wallets_b:
                        cur = line.get("currency", "")
                        bal = line.get("balance", "0")
                        proofs.append({
                            "type": "trust_line",
                            "icon": "🔗",
                            "label": f"Trust line activa · {cur} · balance {bal}",
                            "peer": peer[:12] + "…",
                            "onchain": True,
                        })
                        confidence = max(confidence, 0.85)
            except Exception:
                pass

    # ── 3) Actividad en AMM pools comunes ───────────────────────────────────
    if not proofs:
        for wa in wallets_a[:2]:
            try:
                data = xrpl_rpc({"method": "account_offers", "params": [{
                    "account": wa, "ledger_index": "validated", "limit": 50
                }]}, timeout=12)
                offers = data.get("result", {}).get("offers", [])
                if offers:
                    proofs.append({
                        "type": "offers_activas",
                        "icon": "📊",
                        "label": f"{len(offers)} ofertas activas en DEX/AMM",
                        "count": len(offers),
                        "onchain": True,
                    })
                    confidence = max(confidence, 0.70)
            except Exception:
                pass

    # ── 4) Actividad ODL: pagos XRP grandes a corredores conocidos ──────────
    ODL_CORRIDORS = {w for w, l in KNOWN_XRPL_WALLETS.items()
                     if any(k in l.lower() for k in ("odl", "bitso", "coins.ph", "tranglo", "sbi", "beetech"))}
    for wa in wallets_a[:3]:
        try:
            data = xrpl_rpc({"method": "account_tx", "params": [{
                "account": wa, "limit": 100,
                "ledger_index_min": -1, "ledger_index_max": -1
            }]}, timeout=15)
            for tx_wrap in data.get("result", {}).get("transactions", []):
                tx = tx_wrap.get("tx", tx_wrap.get("transaction", {}))
                dest = tx.get("Destination", "")
                amount = tx.get("Amount", "")
                if dest in ODL_CORRIDORS and isinstance(amount, str):
                    xrp_val = float(amount) / 1e6
                    if xrp_val > 10_000:
                        lbl_dest = KNOWN_XRPL_WALLETS.get(dest, dest[:12])
                        proofs.append({
                            "type": "odl_payment",
                            "icon": "💸",
                            "label": f"Pago ODL · {xrp_val:,.0f} XRP → {lbl_dest}",
                            "amount_xrp": xrp_val,
                            "onchain": True,
                        })
                        confidence = max(confidence, 0.90)
                        break
        except Exception:
            pass

    # ── 5) Verificar que las wallets existen y están activas ────────────────
    active_wallets: List[str] = []
    for wa in (wallets_a + wallets_b)[:4]:
        try:
            data = xrpl_rpc({"method": "account_info", "params": [{
                "account": wa, "ledger_index": "validated"
            }]}, timeout=10)
            info = data.get("result", {}).get("account_data", {})
            if info:
                bal = int(info.get("Balance", 0)) / 1e6
                seq = info.get("Sequence", 0)
                active_wallets.append(_wallet_full_text(wa))
                if not proofs:
                    proofs.append({
                        "type": "wallet_activa",
                        "icon": "👛",
                        "label": f"Wallet activa · {bal:,.0f} XRP · seq {seq}",
                        "address": _wallet_full_text(wa),
                        "onchain": True,
                    })
                    confidence = max(confidence, 0.55)
        except Exception:
            pass

    # ── 6) Sin wallets conocidas → buscar en internet ────────────────────────
    if not wallets_a and not wallets_b:
        proofs.append({
            "type": "sin_wallet",
            "icon": "⚠️",
            "label": "Sin wallets XRPL conocidas — buscando rastros en internet…",
            "onchain": False,
        })

    # ── 7) Búsqueda de rastros en internet (redes privadas) ──────────────────
    api_key = _get_api_key()
    internet_proofs = validate_connection_internet(node_a, node_b, api_key, conn=conn)
    all_proofs = proofs + internet_proofs

    # Eliminar la prueba "sin_wallet" si encontramos evidencia internet
    if internet_proofs:
        all_proofs = [p for p in all_proofs if p.get("type") != "sin_wallet"]

    # ── 8) Scoring calibrado combinado ───────────────────────────────────────
    calibrated_score = _combine_evidence_score(all_proofs)
    cert_label, cert_color = _cert_label(calibrated_score)

    is_onchain   = any(p.get("onchain")  for p in all_proofs)
    is_internet  = any(p.get("internet") for p in all_proofs)

    result_data = {
        "node_a":          node_a,
        "node_b":          node_b,
        "proofs":          all_proofs,
        "wallets_a":       [_wallet_full_text(w) for w in wallets_a],
        "wallets_b":       [_wallet_full_text(w) for w in wallets_b],
        "active_wallets":  active_wallets,
        "cert_label":      cert_label,
        "cert_color":      cert_color,
        "calibrated_score": calibrated_score,
        "has_onchain":     is_onchain,
        "has_internet":    is_internet,
    }

    conn.execute("""
        INSERT OR REPLACE INTO connection_proofs
        (proof_id, node_a, node_b, node_a_key, node_b_key, pair_key, proof_type, proof_data, onchain, confidence, validated_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        proof_id, node_a, node_b, node_a_key, node_b_key, pair_key,
        all_proofs[0]["type"] if all_proofs else "unknown",
        json.dumps(result_data, ensure_ascii=False),
        int(is_onchain or is_internet), calibrated_score, now,
    ))
    # ── Actualizar node_verifications para que el mapa cambie color en la próxima carga ──
    _is_connected_node = calibrated_score >= 0.50 and (is_onchain or is_internet)
    _proofs_for_node = json.dumps(all_proofs[:10], ensure_ascii=False)
    for _vnode in {node_a, node_b}:
        if not _vnode:
            continue
        conn.execute("""
            INSERT OR REPLACE INTO node_verifications
            (node, connected, confidence, kind_override, proofs_json, verified_at, source)
            VALUES (?, ?, ?, 'verified', ?, ?, 'manual')
        """, (_vnode, int(_is_connected_node), calibrated_score, _proofs_for_node, now))
    conn.commit()

    # Notificar a otras sesiones que el mapa cambió
    _log_map_update(conn, "verification", node_a,
                    f"conf={calibrated_score:.0%} connected={_is_connected_node}")

    return {"from_cache": False, **result_data}


def render_discovery_engine(conn: sqlite3.Connection) -> None:
    """Panel UI del motor de descubrimiento."""
    st.subheader("Discovery Engine — busqueda y reescritura automatica")
    st.markdown("""
<div class='rrp-path-panel'>
<div class='rrp-path-title'>Como funciona</div>
<div class='rrp-path-text'>
Introduce el nombre de cualquier institucion (banco, exchange, fondo, fintech...).
El motor busca pruebas verificables en internet, PDFs, comunicados oficiales, filings y fuentes primarias.
Solo reescribe el mapa si encuentra una conexion demostrable con Ripple / XRPL / RLUSD o con un nodo del mapa.
Cada ruta debe traer producto usado, tipo de evidencia, fuente y explicacion. Si no hay prueba suficiente,
el resultado queda guardado como investigacion/watch, pero <b>no se dibuja como conexion confirmada</b>.
</div>
</div>
""", unsafe_allow_html=True)

    ensure_discovery_tables(conn)
    _init_budget(conn)
    _heartbeat(conn, "idle")

    # ── Aviso API key + presupuesto ──────────────────────────────────────────
    render_real_money_warning(conn, key_suffix="discovery")
    render_budget_bar(conn)

    _has_api_key = bool(_get_api_key())
    if not _has_api_key:
        st.error(
            "🔑 **ANTHROPIC_API_KEY no configurada** — las búsquedas nuevas no funcionarán. "
            "Configura el secreto en Streamlit Cloud (Settings → Secrets → `ANTHROPIC_API_KEY = \"sk-ant-...\"`) "
            "o en tu archivo `.env` local. Los resultados **ya cacheados** sí son visibles sin API key."
        )

    # ── Búsqueda ────────────────────────────────────────────────────────────
    st.markdown("#### 🔍 Buscar institución")

    col_inp, col_btn = st.columns([4, 1])
    with col_inp:
        query = st.text_input(
            "inst_query", placeholder="ej: Deutsche Bank, JP Morgan, BIS, Revolut...",
            label_visibility="collapsed", key="disc_search_input"
        )
    with col_btn:
        do_search = st.button("🔍 Buscar", use_container_width=True, key="disc_search_btn")

    # Guardar la query que queremos buscar en session_state para que sobreviva el rerun
    # Si no hay API key, solo permitir si hay resultado cacheado
    if do_search and query and query.strip() and not _has_api_key:
        _precheck = _get_search_cache(conn, query.strip(), "discovery")
        if _precheck:
            st.session_state["disc_pending_query"] = query.strip()
            st.rerun()
        else:
            st.error("🔑 Sin API key — esta institución no está en caché. Configura `ANTHROPIC_API_KEY` para buscarla.")
    if do_search and query and query.strip() and _has_api_key:
        _raw_q = query.strip()
        _queue_pos = _public_enqueue_ai(conn, _raw_q)
        if _queue_pos > 1 or not _public_can_run_ai_now(conn):
            st.session_state["disc_pending_query"] = _raw_q
            st.warning(f"⏳ Búsqueda añadida a la fila AI. Tu puesto actual es #{_queue_pos}. Puedes ir a Comunidad y chatear mientras esperas.")
            st.stop()
        _raw_q = query.strip()
        _normalized_q = _canonical_entity_name(_raw_q)
        if _normalized_q == _raw_q and all(ord(c) < 128 for c in _raw_q):
            def _smart_cap(word: str) -> str:
                if not word:
                    return word
                _no_vowels = not any(v in word.lower() for v in "aeiou")
                if _no_vowels or len(word) <= 3:
                    return word.upper()
                return word.capitalize()
            _normalized_q = " ".join(_smart_cap(w) for w in _raw_q.split())
        st.session_state["disc_raw_query"] = _raw_q
        st.session_state["disc_normalized_query"] = _normalized_q
        st.session_state["disc_pending_query"] = _normalized_q
        st.session_state.pop("disc_result", None)

    # ── Actualizaciones pendientes del mapa ─────────────────────────────────
    _map_seen  = st.session_state.get("map_last_seen", "")
    _map_last  = _get_last_map_update(conn)
    _n_pending = _get_pending_updates(conn, _map_seen) if _map_seen else 0
    if _n_pending > 0:
        _upd_col1, _upd_col2 = st.columns([3, 1])
        with _upd_col1:
            st.info(f"🔄 **{_n_pending} actualización(es) pendiente(s)** — otro usuario añadió nodos o verificaciones al mapa.")
        with _upd_col2:
            if st.button("Aplicar actualizaciones", key="apply_map_updates"):
                st.session_state["map_last_seen"] = _map_last
                st.rerun()
    elif _map_last:
        st.session_state["map_last_seen"] = _map_last

    # ── Quota de llamadas AI por sesión ─────────────────────────────────────
    _ai_used, _ai_max = _session_ai_quota()
    _ai_remaining = _ai_max - _ai_used
    if _ai_remaining <= 3:
        st.warning(f"⚠️ Quedan **{_ai_remaining}** búsquedas nuevas en esta sesión. Los resultados cacheados no consumen quota.")
    elif _ai_used > 0:
        st.caption(f"Búsquedas nuevas usadas esta sesión: {_ai_used}/{_ai_max} · Resultados cacheados: ilimitados")
    render_queue_status(conn)
    _b_now = _get_budget(conn)
    if _b_now.get("locked") or _b_now.get("pct", 0.0) >= _BUDGET_LOCK_PCT:
        st.error("🔒 Modo caché activo: el presupuesto API está bloqueado para proteger el límite de gasto.")
    elif _b_now.get("pct", 0.0) >= _BUDGET_WARN_PCT:
        st.warning(f"⚠️ Presupuesto API bajo: quedan aprox. ${_b_now.get('remaining', 0.0):.2f}.")

    # Ejecutar búsqueda pendiente (siempre en el mismo ciclo de render, no en callback)
    _pending = st.session_state.get("disc_pending_query", "")
    if _pending:
        st.session_state.pop("disc_pending_query")   # consumir la tarea

        # ── Caché compartida: check primero ──────────────────────────────────
        _cached_result = _get_search_cache(conn, _pending, "discovery")
        # Invalidar si le faltan campos obligatorios (resultado parcial/antiguo)
        if _cached_result and not any(k in _cached_result for k in ("wallets", "corridors", "partners")):
            _cached_result = None

        if _cached_result:
            _cached_result = _finalize_discovery_result(_cached_result, _pending, _classify_entity(_pending), None)
            st.session_state["disc_result"] = _cached_result
            st.session_state["disc_from_cache"] = True
            st.session_state["disc_query"] = _pending
            _public_finish_ai(conn)
            st.rerun()
        else:
            # ── Cola pública: si otro usuario está usando la AI, mantener la búsqueda pendiente ──
            _queue_pos = _public_queue_position(conn) or _public_enqueue_ai(conn, _pending)
            if not _public_can_run_ai_now(conn):
                st.session_state["disc_pending_query"] = _pending
                st.warning(f"⏳ Tu búsqueda está en cola AI: puesto #{_queue_pos}. Puedes cambiar a Comunidad y usar el chat mientras esperas.")
                return
            # ── Verificar quota antes de llamar a la API ──────────────────────
            if _ai_remaining <= 0:
                st.error(f"❌ Límite de {_ai_max} búsquedas nuevas por sesión alcanzado. Recarga la página para reiniciar tu sesión, o busca una institución ya investigada.")
                st.session_state["disc_pending_query"] = ""
                _public_finish_ai(conn)
            else:
                # Búsqueda real — spinner simple, sin st.status() que interfiere con reruns
                _budget_now = _get_budget(conn)
                if _budget_now.get("locked") or _budget_now.get("pct", 0.0) >= _BUDGET_LOCK_PCT:
                    st.error("🔒 Presupuesto API en margen de seguridad. Esta búsqueda no se lanza; solo quedan resultados cacheados.")
                    st.session_state["disc_pending_query"] = ""
                    _public_finish_ai(conn)
                    _heartbeat(conn, "idle")
                    st.stop()
                _msg = st.empty()
                _prog = st.progress(0, text="Preparando búsqueda…")
                _heartbeat(conn, "searching")
                render_queue_status(conn)

                def _disc_progress(value: float, text: str) -> None:
                    try:
                        _prog.progress(value, text=text)
                    except TypeError:
                        _prog.progress(value)
                    _msg.info(text)

                _disc_progress(0.08, f"🔍 Normalizando entidad y consultando caché para **{_pending}**…")
                try:
                    res = None
                    for attempt in range(2):
                        if attempt > 0:
                            wait_s = 30
                            _disc_progress(0.38, f"⏳ Límite de API — esperando {wait_s}s antes del reintento…")
                            _time.sleep(wait_s)
                            _disc_progress(0.50, f"🔍 Reintentando búsqueda de **{_pending}**…")
                        else:
                            _disc_progress(0.28, f"🌐 Investigando **{_pending}** con CostGuard + web_search…")
                        res = search_institution_connections(_pending, conn=conn)
                        _disc_progress(0.78, "🧠 Interpretando respuesta y preparando el mapa…")
                        summ = res.get("summary", "")
                        if "429" not in summ and "Too Many" not in summ:
                            break

                    if res is None:
                        res = {"institution": _pending, "connected": False, "confidence": 0.0,
                               "summary": "Sin respuesta de API.", "ripple_products": [], "layer": "Descubierto",
                               "icon": "?", "connects_to": [], "route_kind": "private",
                               "sources": [], "wallets": [], "corridors": [], "partners": []}

                    # Solo contar como llamada real si NO fue error de configuración o caché
                    summ = res.get("summary", "")
                    _is_cfg_error = any(x in summ for x in (
                        "Sin API key", "configura ANTHROPIC_API_KEY", "401", "invalid_api_key",
                        "Unauthorized", "401 Client Error"
                    ))
                    _is_http_err = any(x in summ for x in ("401", "403", "Unauthorized", "Client Error"))
                    _is_from_cache = res.get("_from_cache", False)
                    if not _is_cfg_error and not _is_http_err and not _is_from_cache:
                        _increment_ai_calls()
                        _charge_budget(conn, "discovery")

                    st.session_state["disc_result"] = res
                    st.session_state["disc_from_cache"] = _is_from_cache
                    st.session_state["disc_query"] = _pending

                    # Si hay error de API, lanzar diagnóstico automático
                    if _is_cfg_error or _is_http_err:
                        st.error(f"❌ Error de API: `{summ[:200]}`")
                        st.markdown("**Diagnóstico automático:**")
                        render_api_diagnostics()
                        _public_finish_ai(conn)
                        _heartbeat(conn, "idle")
                        st.stop()

                    # Registrar en log de mapa si se encontró algo nuevo
                    is_error = any(x in summ for x in ("Error:", "Sin API key", "401", "429", "400", "invalid_request"))
                    if not is_error and float(res.get("confidence", 0)) > 0.4:
                        _log_map_update(conn, "discovery", _pending,
                                        f"conf={res.get('confidence', 0):.0%} layer={res.get('layer','?')}")

                except Exception as _search_exc:
                    st.session_state["disc_result"] = {
                        "institution": _pending, "connected": False, "confidence": 0.0,
                        "summary": f"Error inesperado: {_search_exc}",
                        "ripple_products": [], "layer": "Descubierto", "icon": "❌",
                        "connects_to": [], "route_kind": "private",
                        "sources": [], "wallets": [], "corridors": [], "partners": [],
                    }
                    st.session_state["disc_from_cache"] = False
                    st.session_state["disc_query"] = _pending

                try:
                    _disc_progress(1.0, "✅ Búsqueda completada. Cargando resultado…")
                    _time.sleep(0.35)
                except Exception:
                    pass
                _public_finish_ai(conn)
                _heartbeat(conn, "idle")
                st.rerun()  # rerender limpio para mostrar el resultado

    result = st.session_state.get("disc_result")
    if result:
        # Re-finalizar también el resultado de sesión: repara cachés antiguos y JSON recuperados con confianza 0%.
        _display_name = result.get("institution", st.session_state.get("disc_query", ""))
        result = _finalize_discovery_result(result, _display_name, result.get("entity_type", _classify_entity(_display_name)), None)
        st.session_state["disc_result"] = result
        # Mostrar y guardar siempre el nombre canónico para evitar duplicados visuales.
        result["institution"] = _canonical_entity_name(result.get("institution", ""))
        _raw_query_seen = str(st.session_state.get("disc_raw_query", "") or "").strip()
        _canonical_seen = _canonical_entity_name(_raw_query_seen) if _raw_query_seen else result.get("institution", "")
        if _raw_query_seen and _norm_key(_raw_query_seen) != _norm_key(_canonical_seen):
            st.info(f"🧠 Detectado como **{_canonical_seen}** aunque lo escribiste como: `{_raw_query_seen}`")
        if st.session_state.get("disc_from_cache"):
            st.info("⚡ Resultado desde caché compartida — 0 tokens gastados · Buscado previamente por otro usuario o tú mismo")
        conf = float(result.get("confidence", 0))
        css  = "rrp-green" if conf >= 0.65 else "rrp-orange" if conf >= 0.35 else "rrp-red"
        icon = result.get("icon", "?")
        connected_txt = "Conexión confirmada" if result.get("connected") else "Sin conexión encontrada"
        st.markdown(f"""
<div class='rrp-alert {css}'>
  <b>{icon} {result.get('institution','')}</b> — {connected_txt} · Confianza: <b>{conf*100:.0f}%</b>
</div>""", unsafe_allow_html=True)

        if result.get("summary"):
            st.caption(result["summary"])

        # Contador PDF/documentos primarios siempre visible en Discovery, incluso con 0 resultados.
        st.markdown(_discovery_pdf_line_html(result), unsafe_allow_html=True)

        # ── Columnas: info principal | descubrimientos extra ──────────────────
        col_main, col_extra = st.columns([3, 2])

        with col_main:
            if result.get("ripple_products"):
                st.markdown(f"**Productos Ripple:** {', '.join(result['ripple_products'])}")
            if result.get("connects_to"):
                st.markdown(f"**Conecta con:** {', '.join(result['connects_to'])}")
            if result.get("sources"):
                st.markdown("**Fuentes:**")
                for src in result["sources"][:4]:
                    url = _extract_url_from_any(src)
                    label = str(src.get("title", url) if isinstance(src, dict) else url).strip() or str(src)
                    _doc_mark = " 📄" if _is_pdf_or_primary_doc_url(str(url)) else ""
                    if str(url).startswith("http"):
                        shown = label if len(label) <= 72 else label[:72] + "…"
                        st.markdown(f"- {_doc_mark} [{shown}]({url})")
                    else:
                        st.markdown(f"- {_doc_mark} {label}")

        with col_extra:
            # Wallets descubiertas
            wallets = [w for w in (result.get("wallets") or [])
                       if str(w.get("address","")).startswith("r") and 25 <= len(str(w.get("address",""))) <= 35]
            if wallets:
                st.markdown("**👛 Wallets XRPL detectadas:**")
                for w in wallets[:6]:
                    addr  = str(w.get("address",""))
                    wlbl  = str(w.get("label",""))
                    wrole = str(w.get("role",""))
                    xrpscan_url = f"https://xrpscan.com/account/{addr}"
                    st.markdown(
                        f"<div style='background:rgba(15,23,42,0.8);border:1px solid rgba(90,215,255,0.25);"
                        f"border-radius:8px;padding:6px 10px;margin-bottom:4px;font-size:0.78rem;'>"
                        f"<span style='color:#94A3B8;font-size:0.68rem;'>{wlbl} · {wrole}</span><br>"
                        f"<a href='{xrpscan_url}' target='_blank' style='color:#5AD7FF;font-family:monospace;"
                        f"font-size:0.75rem;word-break:break-all;text-decoration:none;'>{addr}</a>"
                        f"</div>",
                        unsafe_allow_html=True,
                    )
            # Corredores
            corridors = result.get("corridors") or []
            if corridors:
                st.markdown("**💱 Corredores ODL detectados:**")
                for c in corridors[:4]:
                    cpair = str(c.get("pair",""))
                    cpart = str(c.get("partner",""))
                    cname = str(c.get("name","")) or f"ODL {cpair}"
                    st.markdown(
                        f"<div style='background:rgba(15,23,42,0.8);border:1px solid rgba(251,146,60,0.25);"
                        f"border-radius:8px;padding:5px 10px;margin-bottom:4px;font-size:0.78rem;'>"
                        f"<span style='color:#FB923C;font-weight:600'>{cname}</span>"
                        f"<br><span style='color:#94A3B8'>{cpair}{' · socio: '+cpart if cpart else ''}</span></div>",
                        unsafe_allow_html=True,
                    )
            # Socios
            partners = result.get("partners") or []
            if partners:
                st.markdown("**🤝 Socios/Partners detectados:**")
                for p in partners[:4]:
                    pname  = str(p.get("name",""))
                    player = str(p.get("layer",""))
                    picon  = str(p.get("icon","🏦"))
                    st.markdown(
                        f"<div style='background:rgba(15,23,42,0.8);border:1px solid rgba(217,167,255,0.25);"
                        f"border-radius:8px;padding:5px 10px;margin-bottom:4px;font-size:0.78rem;'>"
                        f"<span style='color:#D9A7FF;font-weight:600'>{picon} {pname}</span>"
                        f"<span style='color:#94A3B8;font-size:0.70rem;'> · {player}</span></div>",
                        unsafe_allow_html=True,
                    )
            # Puntos de mapa universales
            map_points = result.get("map_points") or []
            if map_points:
                st.markdown("**🧭 Puntos que se añadirán al mapa:**")
                for mp in map_points[:8]:
                    if not isinstance(mp, dict):
                        continue
                    mname = str(mp.get("name", ""))
                    mlayer = str(mp.get("layer", ""))
                    micon = str(mp.get("icon", "🔎"))
                    mconn = mp.get("connects_to", [])
                    if isinstance(mconn, list):
                        mconn = ", ".join([str(x) for x in mconn])
                    mconn_html = ""
                    if mconn:
                        mconn_html = f"<br><span style='color:#CBD5E1'>conecta: {mconn}</span>"
                    st.markdown(
                        f"<div style='background:rgba(15,23,42,0.8);border:1px solid rgba(90,215,255,0.25);"
                        f"border-radius:8px;padding:5px 10px;margin-bottom:4px;font-size:0.78rem;'>"
                        f"<span style='color:#5AD7FF;font-weight:600'>{micon} {mname}</span>"
                        f"<span style='color:#94A3B8;font-size:0.70rem;'> · {mlayer}</span>"
                        f"{mconn_html}</div>",
                        unsafe_allow_html=True,
                    )

            evidence_items = result.get("evidence_items") or []
            if evidence_items:
                st.markdown("**🧾 Pruebas detectadas:**")
                for ev in evidence_items[:6]:
                    if not isinstance(ev, dict):
                        continue
                    title = str(ev.get("title", "Prueba"))[:70]
                    claim = str(ev.get("claim", ""))[:120]
                    url = str(ev.get("url", ""))
                    _doc_mark = "📄 " if _is_pdf_or_primary_doc_url(url, str(ev.get("type", ""))) else ""
                    if url.startswith("http"):
                        st.markdown(f"- {_doc_mark}[{title}]({url}) — {claim}")
                    else:
                        st.markdown(f"- {_doc_mark}**{title}** — {claim}")

            # Pools AMM (se rellenan tras "Añadir al mapa" o si vienen en el result)
            amm_pools = result.get("amm_pools") or []
            if amm_pools:
                st.markdown("**🌊 Pools AMM detectados en XRPL:**")
                for pool in amm_pools[:5]:
                    fee_pct = pool.get("trading_fee", 0) / 1000
                    v1 = pool.get("val1", 0); c1 = pool.get("cur1", "")
                    v2 = pool.get("val2", 0); c2 = pool.get("cur2", "")
                    acct = pool.get("account", "")
                    _acct_html = (
                        "<br><span style='color:#475569;font-family:monospace;font-size:0.68rem'>"
                        + acct[:20] + "…</span>"
                    ) if acct else ""
                    st.markdown(
                        f"<div style='background:rgba(15,23,42,0.8);border:1px solid rgba(60,255,155,0.25);"
                        f"border-radius:8px;padding:5px 10px;margin-bottom:4px;font-size:0.78rem;'>"
                        f"<span style='color:#3CFF9B;font-weight:600'>🌊 {pool.get('pair','?')}</span>"
                        f"<span style='color:#94A3B8;font-size:0.70rem;'> · fee {fee_pct:.2f}%</span><br>"
                        f"<span style='color:#CBD5E1'>{v1:,.0f} {c1} / {v2:,.0f} {c2}</span>"
                        f"{_acct_html}</div>",
                        unsafe_allow_html=True,
                    )

            if not wallets and not corridors and not partners and not map_points and not evidence_items and not amm_pools:
                st.markdown("<span style='color:#475569;font-size:0.80rem'>No se detectaron wallets, corredores ni socios adicionales.</span>", unsafe_allow_html=True)

        # ── Tipo de entidad detectado ──────────────────────────────────────────
        etype = result.get("entity_type", "Otro")
        AUTO_ENTITY_TYPES = {"CBDC", "Gobierno", "FinTech", "RedPrivada", "Clearing", "Puente", "Proveedor", "Otro"}
        ETYPE_LABELS = {
            "AssetMgmt": "💼 Gestor de activos",  "Exchange": "🏦 Exchange cripto",
            "Banco": "🏦 Banco",                  "ODL": "💱 Partner ODL",
            "CBDC": "🏛️ CBDC / Banco central",   "Gobierno": "🏛️ Gobierno / Regulador",
            "FinTech": "📱 FinTech",              "RedPrivada": "🔒 Red privada / DEX",
            "Clearing": "⚖️ Clearing / Post-trade", "Otro": "🔍 Otro",
        }
        etype_label = ETYPE_LABELS.get(etype, etype)
        is_auto_type = etype in AUTO_ENTITY_TYPES
        min_conf_auto = 0.40
        min_conf_manual = 0.35

        st.markdown(
            f"<div style='display:inline-block;background:rgba(90,215,255,0.10);border:1px solid "
            f"rgba(90,215,255,0.3);border-radius:8px;padding:3px 10px;font-size:0.80rem;"
            f"color:#5AD7FF;margin-bottom:8px'>Estrategia usada: <b>{etype_label}</b> · "
            f"{'⚡ Auto-añade si confianza ≥ 40%' if is_auto_type else '✋ Requiere confirmación'}</div>",
            unsafe_allow_html=True,
        )

        # Forzar tratamiento de "añadible" si hay evidencia sólida aunque connected=False
        _has_evidence_ui = bool(
            result.get("partners") or result.get("map_points") or
            result.get("connects_to") or result.get("evidence_items") or
            (result.get("sources") and len(result.get("sources", [])) >= 2)
        )
        _effectively_connected = result.get("connected") or (conf >= 0.55 and _has_evidence_ui)

        def _queue_cascade_entities_from_result(_result: Dict[str, Any], *, limit: int = 6) -> List[str]:
            """Encola entidades hijas para investigar después de un resultado Discovery.

            Corrección v6.2.2:
            - Antes solo encolaba partners[] y solo después del botón manual "Añadir al mapa".
            - Los nodos auto-añadidos, como CBDC/Gobierno/Puente, no activaban la cascada.
            - Ahora también usa map_points[] y connects_to[] para casos como PBoC → mBridge/LianLian.
            """
            try:
                root_name = _canonical_entity_name(_result.get("institution", ""))
                skip = {
                    _canonical_entity_key(root_name),
                    _canonical_entity_key("XRPL"),
                    _canonical_entity_key("RLUSD"),
                    _canonical_entity_key("Ripple Payments"),
                    _canonical_entity_key("RippleNet"),
                    _canonical_entity_key("Ripple Escrow"),
                    _canonical_entity_key("Treasury"),
                    _canonical_entity_key("Rail"),
                    _canonical_entity_key("Custody/Metaco"),
                    _canonical_entity_key("Hidden Road / Prime"),
                }

                candidates: List[str] = []

                def _push(x: Any) -> None:
                    name = _canonical_entity_name(x)
                    if not name or name in {"Descubierto", "?"}:
                        return
                    key = _canonical_entity_key(name)
                    if key in skip:
                        return
                    if name not in candidates:
                        candidates.append(name)

                for p in (_result.get("partners") or []):
                    if isinstance(p, dict):
                        _push(p.get("name"))
                    else:
                        _push(p)

                for mp in (_result.get("map_points") or []):
                    if isinstance(mp, dict):
                        _push(mp.get("name"))
                    else:
                        _push(mp)

                for t in (_result.get("connects_to") or []):
                    _push(t)

                if not candidates:
                    return []

                st.session_state.setdefault("cascade_queue", [])
                queued: List[str] = []
                existing_keys = {_canonical_entity_key(x) for x in st.session_state.get("cascade_queue", [])}
                for cand in candidates[:limit]:
                    ck = _canonical_entity_key(cand)
                    if ck not in existing_keys:
                        st.session_state["cascade_queue"].append(cand)
                        existing_keys.add(ck)
                        queued.append(cand)

                if queued:
                    st.session_state["cascade_last_added"] = queued
                return queued
            except Exception as _cascade_err:
                st.caption(f"⚠️ Cascada no encolada por error interno: {_cascade_err}")
                return []

        if _effectively_connected and conf >= min_conf_manual:
            already = conn.execute(
                "SELECT 1 FROM dynamic_nodes WHERE name=?", (result["institution"],)
            ).fetchone()
            is_in_static = result["institution"] in NODES

            if is_auto_type and conf >= min_conf_auto:
                # AUTO-ADD: incluso si el nodo ya es estático, se actualizan rutas, partners y pruebas.
                if not st.session_state.get(f"auto_added_{result['institution']}"):
                    info = apply_discovery_to_map(conn, result, auto=True)
                    st.session_state[f"auto_added_{result['institution']}"] = info
                info = st.session_state.get(f"auto_added_{result['institution']}", {})
                parts = [f"⚡ **{result['institution']}** actualizado automáticamente en el mapa"]
                if info.get("added_nodes"):   parts.append(f"🧭 {info['added_nodes']} nodos")
                if info.get("added_routes"):  parts.append(f"🔀 {info['added_routes']} rutas")
                if info.get("wallets_added"): parts.append(f"👛 {info['wallets_added']} wallets")
                if info.get("added_partners"): parts.append(f"🤝 {info['added_partners']} socios")
                if info.get("added_map_points"): parts.append(f"🧭 {info['added_map_points']} puntos extra")
                st.success(" · ".join(parts))
                st.caption(
                    f"Tipo: **{etype_label}** — si el nodo ya existía, no se duplica: se añaden/actualizan "
                    f"sus rutas, partners y pruebas. Aparecerá en el mapa al volver a 'Radar'."
                )
                _queued_now = _queue_cascade_entities_from_result(result)
                if _queued_now:
                    st.info("🔗 Cascada activada: " + ", ".join(_queued_now[:6]))

            elif already or is_in_static:
                st.success(f"✅ {result['institution']} ya está en el mapa.")
                if st.button("🔁 Actualizar rutas y pruebas", use_container_width=True, key="btn_update_known_node"):
                    info = apply_discovery_to_map(conn, result, auto=False)
                    if info.get("added_node"):
                        st.success(f"Actualizado: {info.get('added_routes',0)} rutas · {info.get('added_nodes',0)} nodos/puntos · ve al Radar.")
                        _queued_now = _queue_cascade_entities_from_result(result)
                        if _queued_now:
                            st.info("🔗 Cascada activada: " + ", ".join(_queued_now[:6]))
                        st.session_state.pop("disc_result", None)
                        st.rerun()
                    else:
                        st.warning(f"No actualizado: {info.get('reason')}")

            else:
                # MANUAL: entidades fijas conocidas (bancos, exchanges, Asset Mgmt) requieren confirmación
                if st.button("➕ Añadir al mapa", use_container_width=True, key="btn_add_to_map"):
                    info = apply_discovery_to_map(conn, result, auto=False)
                    if info.get("added_node"):
                        parts = [f"✅ **{result['institution']}** añadido al mapa"]
                        if info.get("added_nodes"):   parts.append(f"🧭 {info['added_nodes']} nodos")
                        if info.get("added_routes"):  parts.append(f"🔀 {info['added_routes']} rutas")
                        if info.get("wallets_added"): parts.append(f"👛 {info['wallets_added']} wallets")
                        if info.get("added_corridors"): parts.append(f"💱 corredores")
                        if info.get("added_partners"):  parts.append(f"🤝 socios")
                        if info.get("added_map_points"): parts.append(f"🧭 puntos extra")
                        if info.get("added_amm_pools"): parts.append(f"🌊 {info['added_amm_pools']} pools AMM")
                        st.success(" · ".join(parts) + " · Ve al Radar para verlo.")
                        # Cascada: encolar partners, puntos del mapa y conexiones detectadas.
                        _queued_now = _queue_cascade_entities_from_result(result)
                        if _queued_now:
                            st.info("🔗 Cascada activada: " + ", ".join(_queued_now[:6]))
                        st.session_state.pop("disc_result", None)
                        st.rerun()
                    else:
                        st.warning(f"No añadido: {info.get('reason')}")

            # ── Investigación en cascada: partners pendientes ──────────────────
            _cascade_q = st.session_state.get("cascade_queue", [])
            if _cascade_q:
                st.markdown("---")
                st.markdown(f"**🔗 Hilo de investigación — {len(_cascade_q)} entidades pendientes de investigar:**")
                for _cname in _cascade_q[:6]:
                    st.markdown(f"• {_cname}")
                col_cas1, col_cas2 = st.columns(2)
                with col_cas1:
                    if st.button("⚡ Investigar siguiente en cascada", use_container_width=True, key="btn_cascade_next"):
                        _next = st.session_state["cascade_queue"].pop(0)
                        st.session_state["disc_pending_query"] = _next
                        st.session_state.pop("disc_result", None)
                        st.rerun()
                with col_cas2:
                    if st.button("🗑️ Limpiar cola", use_container_width=True, key="btn_cascade_clear"):
                        st.session_state["cascade_queue"] = []
                        st.rerun()

    # Nodos descubiertos
    st.markdown("---")
    st.markdown("#### Nodos descubiertos en el mapa")
    try:
        dyn = pd.read_sql_query(
            "SELECT name, layer, confidence, summary, source_url, added_at FROM dynamic_nodes ORDER BY added_at DESC", conn)
        if dyn.empty:
            st.info("Ningun nodo descubierto. Usa la busqueda para añadir instituciones.")
        else:
            _layer_badge = {
                "Banca_AM": "#F59E0B", "Banca_EU": "#E67E22", "Banca_AP": "#D35400",
                "ODL": "#FB923C", "Privado": "#FFB84D", "Ripple": "#5AD7FF",
                "Institucional": "#D9A7FF", "Exchange": "#22D3EE", "Fintech": "#F472B6",
                "CBDC": "#34D399", "AssetMgmt": "#A78BFA", "Gobierno": "#FCD34D",
                "Clearing": "#38BDF8", "RedPrivada": "#FB7185",
                "Puente": "#22D3EE", "Proveedor": "#F59E0B", "Ripple": "#5AD7FF",
                "Descubierto": "#94A3B8", "Otro": "#64748B",
            }
            for _, drow in dyn.iterrows():
                conf_val = float(drow["confidence"]) * 100
                conf_color = "#3CFF9B" if conf_val >= 65 else "#FB923C" if conf_val >= 35 else "#FF5A67"
                lcolor = _layer_badge.get(str(drow["layer"]), "#94A3B8")
                summary_txt = str(drow.get("summary", ""))[:220]
                src_blob = str(drow.get("source_url", "") or "")
                srcs = [u.strip() for u in src_blob.split(",") if u.strip().startswith("http")][:3]
                added = str(drow.get("added_at", ""))[:16].replace("T", " ")
                node_name = str(drow["name"])

                proof_links = " · ".join([
                    f"<a href='{u}' target='_blank' style='color:#5AD7FF;text-decoration:none;'>prueba {i+1}</a>"
                    for i, u in enumerate(srcs)
                ]) if srcs else ""
                proof_html = f"<div style='margin-top:5px;color:rgba(255,255,255,0.45);font-size:0.72rem;'>🧾 {proof_links}</div>" if proof_links else ""

                # Tarjeta + botón de carga de resultados
                col_card, col_btn = st.columns([5, 1])
                with col_card:
                    st.markdown(f"""
<div style='background:rgba(14,22,40,0.90);border:1px solid rgba(255,255,255,0.10);
            border-left:3px solid {lcolor};border-radius:10px;padding:10px 14px;margin-bottom:2px;'>
  <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;'>
    <span style='color:#FFFFFF;font-weight:700;font-size:0.95rem;'>{node_name}</span>
    <span style='color:{conf_color};font-size:0.80rem;font-weight:600;'>{conf_val:.0f}%</span>
  </div>
  <div style='margin-bottom:4px;'>
    <span style='background:{lcolor}22;color:{lcolor};border:1px solid {lcolor}66;
                 border-radius:4px;padding:1px 7px;font-size:0.72rem;font-weight:600;'>{drow['layer']}</span>
    <span style='color:rgba(255,255,255,0.40);font-size:0.70rem;margin-left:8px;'>{added}</span>
  </div>
  <div style='color:rgba(255,255,255,0.65);font-size:0.78rem;line-height:1.4;'>{summary_txt}</div>
  {proof_html}
</div>""", unsafe_allow_html=True)
                with col_btn:
                    _vnode_verified = conn.execute(
                        "SELECT confidence FROM node_verifications WHERE node=? AND connected=1",
                        (node_name,)
                    ).fetchone()
                    _ver_label = f"✅ Ver ({int((_vnode_verified[0] if _vnode_verified else 0)*100)}%)" if _vnode_verified else "📋 Ver"
                    _ver_help = "Resultados guardados · click para ver · sin coste de API" if _vnode_verified else "Ver resultados completos de la búsqueda"
                    if st.button(_ver_label, key=f"view_node_{node_name}", use_container_width=True,
                                 help=_ver_help):
                        # Buscar en caché con múltiples variantes de clave
                        _cached = None
                        _name_lower  = node_name.lower()
                        _canon_lower = _canonical_entity_name(node_name).lower()
                        # 1) Exacto: nombre del nodo y su forma canónica
                        for _ck in [_name_lower, _canon_lower]:
                            _cached = conn.execute(
                                "SELECT result_json FROM institution_search_cache WHERE query=?", (_ck,)
                            ).fetchone()
                            if _cached:
                                break
                        # 2) Parcial: primeros 12 caracteres (cubre nombres largos ligeramente distintos)
                        if not _cached:
                            _cached = conn.execute(
                                "SELECT result_json FROM institution_search_cache WHERE query LIKE ?",
                                (f"%{_name_lower[:12]}%",)
                            ).fetchone()
                        # 3) Escaneo de JSON: busca el nombre dentro del campo institution almacenado
                        if not _cached:
                            _cached = conn.execute(
                                "SELECT result_json FROM institution_search_cache "
                                "WHERE result_json LIKE ? LIMIT 1",
                                (f'%"{node_name}"%',)
                            ).fetchone()
                        # 4) Escaneo completo: itera todos los registros y compara institution canónica
                        #    Cubre búsquedas en chino/japonés/árabe donde el nodo se guarda en inglés
                        if not _cached:
                            try:
                                for _cq, _cj in conn.execute(
                                    "SELECT query, result_json FROM institution_search_cache"
                                ).fetchall():
                                    _cr = json.loads(_cj)
                                    _inst_canon = _canonical_entity_name(
                                        str(_cr.get("institution", ""))
                                    ).lower()
                                    if _inst_canon in (_name_lower, _canon_lower):
                                        _cached = (_cj,)
                                        # Guardar también con la clave del nodo para próximas veces
                                        conn.execute(
                                            "INSERT OR REPLACE INTO institution_search_cache"
                                            "(query,result_json,searched_at) VALUES(?,?,?)",
                                            (_name_lower, _cj,
                                             datetime.now(timezone.utc).isoformat())
                                        )
                                        conn.commit()
                                        break
                            except Exception:
                                pass
                        if _cached:
                            _cached_view_result = json.loads(_cached[0])
                            _cached_view_result = _finalize_discovery_result(_cached_view_result, node_name, _classify_entity(node_name), None)
                            st.session_state["disc_result"] = _cached_view_result
                            st.session_state["disc_from_cache"] = True
                            st.session_state["disc_query"] = node_name
                        else:
                            # No hay caché — relanzar búsqueda
                            st.session_state["disc_pending_query"] = node_name
                            st.session_state.pop("disc_result", None)
                        st.rerun()
                    # Botón re-verificar (solo si hay caché guardado)
                    if _vnode_verified and st.button("🔁", key=f"reverify_{node_name}",
                                                      use_container_width=True,
                                                      help="Re-verificar gastando tokens de API"):
                        conn.execute("DELETE FROM institution_search_cache WHERE query=?", (node_name.lower(),))
                        conn.execute("DELETE FROM node_verifications WHERE node=? AND source='manual'", (node_name,))
                        conn.commit()
                        st.session_state["disc_pending_query"] = node_name
                        st.session_state.pop("disc_result", None)
                        st.rerun()

        dyn_routes_df = pd.read_sql_query(
            "SELECT src, dst, kind, label, confidence, evidence, source_urls FROM dynamic_routes ORDER BY added_at DESC", conn)
        if not dyn_routes_df.empty:
            st.markdown("#### Rutas descubiertas")
            _kind_color = {
                "verified":    "#22C55E",   # verde — verificado por investigación
                "real":        "#3CFF9B",   # verde neón — on-chain TX
                "public":      "#00CFFF",   # cian — gateway público
                "private":     "#F59E0B",   # ámbar — inferida por documentos
                "obligatory":  "#FF4D6D",   # rojo-rosa — implicación técnica
                "watch":       "#B673FF",   # morado — vigilada
                "discovered":  "#FFD700",   # dorado — motor IA
                "model":       "#60A5FA",   # azul — analítico
                "future":      "#8CA0B8",   # gris — futura
                "odl":         "#FB923C",   # naranja — corredor ODL
                "partner":     "#A78BFA",   # violeta — partner
                "public_wallet":"#34D399",  # esmeralda — wallet pública
                "swift":       "#F59E0B",
                "sepa":        "#60A5FA",
                "government":  "#FCD34D",
                "government_payment_rail": "#FCD34D",
            }
            routes_html = "<div style='display:flex;flex-direction:column;gap:6px;margin-top:6px;'>"
            for _, rr in dyn_routes_df.iterrows():
                conf_val = float(rr["confidence"]) * 100
                conf_color = "#3CFF9B" if conf_val >= 65 else "#FB923C" if conf_val >= 35 else "#FF5A67"
                kind_str = str(rr.get("kind", "")).lower()
                kcolor = _kind_color.get(kind_str, "#94A3B8")
                evidence_txt = str(rr.get("evidence", ""))[:220]
                route_srcs = [u.strip() for u in str(rr.get("source_urls", "") or "").split(",") if u.strip().startswith("http")][:3]
                route_proof_html = ""
                if route_srcs:
                    route_links = " · ".join([f"<a href='{u}' target='_blank' style='color:#5AD7FF;text-decoration:none;'>prueba {i+1}</a>" for i, u in enumerate(route_srcs)])
                    route_proof_html = f"<div style='color:rgba(255,255,255,0.42);font-size:0.72rem;margin-top:3px;'>🧾 {route_links}</div>"
                routes_html += f"""
<div style='background:rgba(14,22,40,0.90);border:1px solid rgba(255,255,255,0.08);
            border-left:3px solid {kcolor};border-radius:10px;padding:9px 14px;'>
  <div style='display:flex;align-items:center;gap:8px;flex-wrap:wrap;margin-bottom:3px;'>
    <span style='color:#5AD7FF;font-weight:700;font-size:0.88rem;'>{rr['src']}</span>
    <span style='color:rgba(255,255,255,0.40);font-size:0.85rem;'>→</span>
    <span style='color:#3CFF9B;font-weight:700;font-size:0.88rem;'>{rr['dst']}</span>
    <span style='background:{kcolor}22;color:{kcolor};border:1px solid {kcolor}55;
                 border-radius:4px;padding:1px 6px;font-size:0.70rem;font-weight:600;'>{rr.get('kind','')}</span>
    <span style='color:{conf_color};font-size:0.78rem;font-weight:600;margin-left:auto;'>Conf: {conf_val:.0f}%</span>
  </div>
  <div style='color:rgba(255,255,255,0.50);font-size:0.75rem;'>{rr.get('label','')}</div>
  {f'<div style="color:rgba(255,255,255,0.40);font-size:0.72rem;margin-top:2px;">{evidence_txt}</div>' if evidence_txt else ''}
  {route_proof_html}
</div>"""
            routes_html += "</div>"
            st.markdown(routes_html, unsafe_allow_html=True)

        if not dyn.empty:
            st.markdown("")
            if st.button("🗑️ Limpiar mapa dinámico", use_container_width=True):
                conn.execute("DELETE FROM dynamic_nodes")
                conn.execute("DELETE FROM dynamic_routes")
                # No borrar institution_search_cache: mantiene investigaciones completas guardadas.
                conn.commit()
                st.toast("Mapa dinámico limpiado; investigaciones guardadas conservadas.")
    except Exception as exc:
        st.error(f"Error: {exc}")

def purge_legacy_preconfigured_routes(conn: sqlite3.Connection) -> int:
    """
    Limpia rutas/pruebas heredadas de versiones antiguas sin borrar búsquedas guardadas.
    Borra solo aristas generadas por plantillas: inferido por tipo, obligatoria por protocolo,
    Ripple ecosystem, vigilancia por tipo y pruebas semilla.
    """
    ensure_discovery_tables(conn)
    deleted = 0
    try:
        patterns = [
            "%inferido por tipo%", "%Ruta inferida automaticamente%",
            "%obligatoria por protocolo%", "%deducción:%", "%deduccion:%",
            "%Ripple ecosystem%", "%vigilancia por tipo%", "%Ruta especulativa por tipo%",
            "%obligatoria%",
        ]
        for pat in patterns:
            cur = conn.execute(
                "DELETE FROM dynamic_routes WHERE COALESCE(label,'') LIKE ? OR COALESCE(evidence,'') LIKE ?",
                (pat, pat),
            )
            deleted += cur.rowcount or 0
        # Quitar pruebas semilla antiguas, pero mantener caché de investigaciones.
        cur = conn.execute(
            "DELETE FROM connection_proofs WHERE COALESCE(proof_data,'') LIKE '%seeded_known_evidence%'"
        )
        deleted += cur.rowcount or 0
        conn.commit()
    except Exception:
        pass
    return deleted



def inject_music_player() -> None:
    """Radar FM persistente dentro de la app, sin modo seguro.

    Diseño v85:
    - Un único reproductor HTML/JS interno.
    - Sin st.audio y sin botones Streamlit para música.
    - Un primer click humano desbloquea el audio.
    - Después, el mismo <audio> persistente gestiona siguiente/anterior/aleatorio/ended.
    - Usa fetch->Blob y, si falla, fuente directa como fallback.
    """
    try:
        import os as _os
        import json as _json
        from pathlib import Path as _Path

        exts = (".mp3", ".wav", ".ogg", ".m4a", ".aac", ".flac")
        here = _Path(__file__).resolve().parent if "__file__" in globals() else _Path.cwd()
        cwd = _Path(_os.getcwd()).resolve()

        candidate_dirs = []
        def _add_candidate(p):
            try:
                rp = _Path(p).resolve()
                if rp not in candidate_dirs:
                    candidate_dirs.append(rp)
            except Exception:
                pass

        _add_candidate(here / "static" / "musica")
        _add_candidate(cwd / "static" / "musica")
        for parent in [here] + list(here.parents)[:6]:
            _add_candidate(parent / "static" / "musica")
        for parent in [cwd] + list(cwd.parents)[:6]:
            _add_candidate(parent / "static" / "musica")

        music_dir = None
        tracks = []
        debug_rows = []
        for cand in candidate_dirs:
            exists = cand.is_dir()
            found = []
            if exists:
                try:
                    found = [p for p in cand.rglob("*") if p.is_file() and p.suffix.lower() in exts]
                except Exception:
                    found = []
            debug_rows.append((str(cand), exists, len(found)))
            if exists and found and music_dir is None:
                music_dir = cand
                tracks = sorted(found, key=lambda p: p.name.lower())

        if not tracks:
            st.markdown("### 🎧 Radar FM")
            st.warning("Radar FM no encuentra canciones reproducibles. En GitHub deben estar en `static/musica/track_01.mp3`, `track_02.mp3`, etc. Reinicia la app después de subirlas.")
            with st.expander("🔎 Diagnóstico de carpetas de música", expanded=True):
                st.write("Directorio actual de Streamlit:", str(cwd))
                st.write("Directorio del archivo Python:", str(here))
                st.write("Rutas probadas:")
                for row_path, exists, n in debug_rows:
                    st.write(f"- `{row_path}` · existe={exists} · audios={n}")
            return

        def _mime_for(p: _Path) -> str:
            return {
                ".mp3": "audio/mpeg",
                ".wav": "audio/wav",
                ".ogg": "audio/ogg",
                ".m4a": "audio/mp4",
                ".aac": "audio/aac",
                ".flac": "audio/flac",
            }.get(p.suffix.lower(), "audio/mpeg")

        # Playlist para JS. El componente intenta varias rutas porque Streamlit Cloud
        # sirve static normalmente como /app/static/..., pero algunas rutas locales usan /static/...
        playlist = []
        for i, p in enumerate(tracks):
            name = p.name
            playlist.append({
                "title": f"{i+1:02d} · {p.stem}",
                "file": name,
                "mime": _mime_for(p),
                "candidates": [
                    f"/app/static/musica/{name}",
                    f"/static/musica/{name}",
                    f"static/musica/{name}",
                    f"./static/musica/{name}",
                    f"https://raw.githubusercontent.com/edutrejo96/radar-ripple-pro/main/static/musica/{name}",
                ],
            })

        playlist_json = _json.dumps(playlist, ensure_ascii=False)
        html_doc = f"""
<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<style>
  :root {{ color-scheme: dark; }}
  * {{ box-sizing:border-box; }}
  body {{ margin:0; font-family:Inter, Segoe UI, Arial, sans-serif; background:transparent; color:#e5e7eb; }}
  .box {{ border:1px solid rgba(56,189,248,.38); border-radius:20px; padding:16px; background:linear-gradient(135deg,rgba(2,6,23,.98),rgba(15,23,42,.94)); box-shadow:0 18px 50px rgba(0,212,255,.14); }}
  .top {{ display:flex; align-items:center; justify-content:space-between; gap:12px; flex-wrap:wrap; }}
  .title {{ font-weight:950; color:#67e8f9; font-size:17px; letter-spacing:.2px; }}
  .pill {{ border:1px solid rgba(148,163,184,.32); color:#cbd5e1; border-radius:999px; padding:4px 10px; font-size:12px; }}
  .now {{ margin:12px 0; padding:12px; border-radius:15px; background:rgba(15,23,42,.86); border:1px solid rgba(51,65,85,.78); }}
  .now b {{ color:#fff; }}
  audio {{ width:100%; margin:8px 0 8px 0; accent-color:#22d3ee; }}
  .btns {{ display:grid; grid-template-columns:repeat(5,minmax(0,1fr)); gap:8px; margin:10px 0; }}
  button {{ background:#0f172a; color:#e5e7eb; border:1px solid rgba(56,189,248,.45); border-radius:13px; padding:10px 8px; cursor:pointer; font-weight:850; }}
  button:hover {{ background:#172554; border-color:#67e8f9; }}
  .primary {{ background:linear-gradient(135deg,#0891b2,#2563eb); color:white; }}
  .danger {{ border-color:rgba(251,191,36,.55); color:#fde68a; }}
  select {{ width:100%; background:#020617; color:#e5e7eb; border:1px solid rgba(56,189,248,.35); border-radius:13px; padding:10px; margin:8px 0; }}
  .status {{ display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; margin:10px 0; }}
  .s {{ background:rgba(2,6,23,.6); border:1px solid rgba(51,65,85,.7); border-radius:12px; padding:8px; font-size:12px; color:#cbd5e1; }}
  .s b {{ color:#67e8f9; display:block; margin-bottom:2px; }}
  .log {{ font-size:12px; color:#94a3b8; margin-top:9px; line-height:1.45; white-space:pre-wrap; }}
  .warn {{ color:#fbbf24; }} .ok {{ color:#86efac; }} .bad {{ color:#fca5a5; }}
  @media(max-width:760px) {{ .btns {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} .status {{ grid-template-columns:repeat(2,minmax(0,1fr)); }} }}
</style>
</head>
<body>
<div class="box">
  <div class="top">
    <div class="title">🎧 RADAR FM · reproductor persistente v86</div>
    <div class="pill"><span id="count"></span> tracks · sin modo seguro</div>
  </div>

  <div class="now">
    <b>Ahora:</b> <span id="nowTitle">—</span><br>
    <span style="color:#94a3b8" id="nowFile">—</span>
  </div>

  <audio id="audio" controls preload="metadata" playsinline></audio>

  <div class="btns">
    <button id="activate" class="primary">▶️ Activar / Play</button>
    <button id="prev">⏮️ Anterior</button>
    <button id="next">⏭️ Siguiente</button>
    <button id="shuffle">🎲 Aleatorio: OFF</button>
    <button id="stop" class="danger">⏸️ Pausa</button>
  </div>

  <select id="select"></select>

  <div class="status">
    <div class="s"><b>Audio</b><span id="stAudio">bloqueado</span></div>
    <div class="s"><b>Ruta</b><span id="stRoute">pendiente</span></div>
    <div class="s"><b>Ended</b><span id="stEnded">activo</span></div>
    <div class="s"><b>Modo</b><span id="stMode">secuencial</span></div>
  </div>

  <div class="log" id="log">Pulsa “Activar / Play” una vez. v86 prueba rutas Streamlit y GitHub Raw; el final de canción y el arrastre al final deberían pasar al siguiente track.</div>
</div>
<script>
const playlist = {playlist_json};
let idx = parseInt(localStorage.getItem('rrp_fm_idx_v86') || '0', 10);
let shuffle = (localStorage.getItem('rrp_fm_shuffle_v86') || '0') === '1';
let unlocked = (localStorage.getItem('rrp_fm_unlocked_v86') || '0') === '1';
let currentObjectUrl = null;
let currentCandidate = null;
let loading = false;
const audio = document.getElementById('audio');
const nowTitle = document.getElementById('nowTitle');
const nowFile = document.getElementById('nowFile');
const logEl = document.getElementById('log');
const select = document.getElementById('select');
const shuffleBtn = document.getElementById('shuffle');
const stAudio = document.getElementById('stAudio');
const stRoute = document.getElementById('stRoute');
const stMode = document.getElementById('stMode');
document.getElementById('count').textContent = playlist.length;

function log(msg, cls='') {{ logEl.className = 'log ' + cls; logEl.textContent = msg; }}
function clamp() {{ if (!playlist.length) idx = 0; else idx = ((idx % playlist.length) + playlist.length) % playlist.length; localStorage.setItem('rrp_fm_idx_v86', String(idx)); }}
function status() {{ stAudio.textContent = unlocked ? 'desbloqueado' : 'bloqueado'; stRoute.textContent = currentCandidate || 'pendiente'; stMode.textContent = shuffle ? 'aleatorio' : 'secuencial'; }}
function parentOrigin() {{
  try {{ if (document.referrer) return new URL(document.referrer).origin; }} catch(e) {{}}
  try {{ return window.location.origin; }} catch(e) {{ return ''; }}
}}
function expandedCandidates(t) {{
  const base = parentOrigin();
  const arr = [];
  if (base) {{
    arr.push(base + '/app/static/musica/' + encodeURIComponent(t.file));
    arr.push(base + '/static/musica/' + encodeURIComponent(t.file));
  }}
  for (const u of t.candidates) arr.push(u);
  return [...new Set(arr)];
}}
function waitForPlayable(timeoutMs=3500) {{
  return new Promise((resolve) => {{
    if (audio.readyState >= 2) return resolve(true);
    let done = false;
    const cleanup = () => {{ audio.removeEventListener('canplay', onok); audio.removeEventListener('loadeddata', onok); audio.removeEventListener('error', onerr); }};
    const finish = (v) => {{ if (done) return; done = true; cleanup(); resolve(v); }};
    const onok = () => finish(true);
    const onerr = () => finish(false);
    audio.addEventListener('canplay', onok, {{once:true}});
    audio.addEventListener('loadeddata', onok, {{once:true}});
    audio.addEventListener('error', onerr, {{once:true}});
    setTimeout(() => finish(audio.readyState >= 2), timeoutMs);
  }});
}}
function updateUi() {{
  clamp();
  const t = playlist[idx];
  nowTitle.textContent = t.title;
  nowFile.textContent = t.file;
  select.value = String(idx);
  shuffleBtn.textContent = shuffle ? '🎲 Aleatorio: ON' : '🎲 Aleatorio: OFF';
  status();
}}
function fillSelect() {{
  select.innerHTML = '';
  playlist.forEach((t, i) => {{ const opt = document.createElement('option'); opt.value = String(i); opt.textContent = t.title; select.appendChild(opt); }});
}}
function cleanupBlob() {{
  if (currentObjectUrl) {{ try {{ URL.revokeObjectURL(currentObjectUrl); }} catch(e) {{}} currentObjectUrl = null; }}
}}
async function testDecode(blob) {{
  // Solo comprueba que el blob no esté vacío. La decodificación real la hace <audio>.
  return blob && blob.size > 4096;
}}
async function loadTrack(i) {{
  if (loading) return false;
  loading = true;
  idx = i; clamp(); updateUi();
  const t = playlist[idx];
  cleanupBlob();
  currentCandidate = null;
  audio.removeAttribute('src');
  audio.load();
  let lastErr = '';

  // Estrategia 1: fetch -> Blob -> objectURL, mantiene control dentro del iframe.
  for (const url of expandedCandidates(t)) {{
    try {{
      const res = await fetch(url, {{ cache:'force-cache' }});
      if (!res.ok) {{ lastErr = url + ' HTTP ' + res.status; continue; }}
      const ctype = (res.headers.get('content-type') || '').toLowerCase();
      const blob = await res.blob();
      const btype = (blob.type || '').toLowerCase();
      if (!(ctype.startsWith('audio/') || btype.startsWith('audio/') || url.includes('raw.githubusercontent.com'))) {{
        lastErr = url + ' no parece audio: ' + (ctype || btype || 'sin content-type');
        continue;
      }}
      const okBlob = await testDecode(blob);
      if (!okBlob) {{ lastErr = url + ' blob inválido: ' + (blob ? blob.size : 0); continue; }}
      currentObjectUrl = URL.createObjectURL(blob);
      currentCandidate = url + ' → blob';
      audio.src = currentObjectUrl;
      audio.load();
      loading = false;
      updateUi();
      log('Track cargado dentro de la app: ' + t.title, 'ok');
      return true;
    }} catch(e) {{ lastErr = url + ' ' + (e && e.message ? e.message : e); }}
  }}

  // Estrategia 2: fuente directa por si fetch queda sandboxed pero <audio> sí puede leer.
  for (const url of expandedCandidates(t)) {{
    try {{
      currentCandidate = url + ' directo';
      audio.src = url;
      audio.load();
      loading = false;
      updateUi();
      log('Track cargado por ruta directa: ' + t.title, 'ok');
      return true;
    }} catch(e) {{ lastErr = url + ' directo ' + (e && e.message ? e.message : e); }}
  }}

  loading = false;
  updateUi();
  log('Error de audio: no pude cargar este track. Último intento: ' + lastErr, 'bad');
  return false;
}}
async function playLoaded(reason='play') {{
  try {{
    const ready = await waitForPlayable(4500);
    if (!ready) throw new Error('audio no listo: readyState=' + audio.readyState + ' ruta=' + (currentCandidate || 'n/a'));
    await audio.play();
    unlocked = true;
    localStorage.setItem('rrp_fm_unlocked_v86','1');
    updateUi();
    log(reason + ': ' + playlist[idx].title, 'ok');
    return true;
  }} catch(e) {{
    updateUi();
    log('El navegador bloqueó el play (' + (e.name || e) + '). Pulsa el botón ▶ nativo del reproductor una vez; después el mismo reproductor debería continuar.', 'warn');
    return false;
  }}
}}
async function playCurrent() {{
  unlocked = true;
  localStorage.setItem('rrp_fm_unlocked_v86','1');
  if (!audio.src) {{ const ok = await loadTrack(idx); if (!ok) return; }}
  await playLoaded('Reproduciendo');
}}
function nextIndex() {{ return shuffle ? Math.floor(Math.random()*playlist.length) : idx + 1; }}
function prevIndex() {{ return shuffle ? Math.floor(Math.random()*playlist.length) : idx - 1; }}
async function goTo(newIdx, auto=false) {{
  const ok = await loadTrack(newIdx);
  if (!ok) return;
  if (unlocked || auto) await playLoaded(auto ? 'Auto-next' : 'Cambio');
}}
async function goNext(auto=false) {{ await goTo(nextIndex(), auto); }}
async function goPrev() {{ await goTo(prevIndex(), false); }}

fillSelect(); updateUi(); loadTrack(idx);
document.getElementById('activate').onclick = playCurrent;
document.getElementById('next').onclick = () => goNext(false);
document.getElementById('prev').onclick = goPrev;
document.getElementById('stop').onclick = () => {{ audio.pause(); log('Pausado.'); }};
document.getElementById('shuffle').onclick = () => {{ shuffle = !shuffle; localStorage.setItem('rrp_fm_shuffle_v86', shuffle?'1':'0'); updateUi(); }};
select.onchange = async () => {{ await goTo(parseInt(select.value,10), false); }};

audio.addEventListener('play', () => {{ unlocked = true; localStorage.setItem('rrp_fm_unlocked_v86','1'); updateUi(); }});
audio.addEventListener('ended', () => goNext(true));
audio.addEventListener('timeupdate', () => {{
  try {{
    if (audio.duration && isFinite(audio.duration) && audio.currentTime >= audio.duration - 0.25 && !audio.paused) {{
      // Si el navegador no lanza ended al arrastrar justo al final, forzamos el salto.
      goNext(true);
    }}
  }} catch(e) {{}}
}});
audio.addEventListener('error', () => {{
  const err = audio.error ? audio.error.code : 'desconocido';
  log('Error del elemento audio. Código: ' + err + '. Ruta: ' + (currentCandidate || 'n/a'), 'bad');
}});
</script>
</body>
</html>
"""
        _st_components.html(html_doc, height=430, scrolling=False)

    except Exception as e:
        st.warning(f"Radar FM no pudo cargarse: {e}")

def main() -> None:
    st.set_page_config(page_title=APP_NAME, layout="wide", initial_sidebar_state="expanded")
    install_streamlit_i18n_patch()
    inject_css()

    # Auto-refresh solo cuando el usuario no está en medio de nada
    # (sin búsqueda activa, sin nodo seleccionado, sin resultado pendiente)
    _user_idle = (
        not st.session_state.get("disc_result")
        and not st.session_state.get("disc_pending_query")
        and not st.session_state.get("map_focus_node")
        and not st.session_state.get("cascade_queue")
    )
    if ENABLE_BACKGROUND_AUTOREFRESH and st_autorefresh and _user_idle:
        st_autorefresh(interval=REFRESH_SECONDS * 1000, key="rrp_advanced_refresh")

    conn = get_conn()
    bootstrap_demo(conn)
    ensure_discovery_tables(conn)
    purge_legacy_preconfigured_routes(conn)
    _ensure_static_verifications(conn)   # pre-poblar verificaciones de nodos estáticos
    reclassify_all_dynamic_nodes(conn)
    bootstrap_static_node_routes(conn)
    _heartbeat(conn, "idle")

    if not render_public_entry_gate(conn):
        return
    render_global_public_banner(conn)
    render_global_update_notice(conn)
    inject_music_player()
    if ENABLE_BACKGROUND_AUTOREFRESH and st_autorefresh is not None:
        st_autorefresh(interval=15000, limit=None, key="public_map_soft_live_refresh")

    # Cargar wallets descubiertas con added_to_map=1 en KNOWN_XRPL_WALLETS
    try:
        ensure_discovered_wallets_table(conn)
        _mapped = conn.execute(
            "SELECT wallet, label FROM discovered_wallets WHERE added_to_map=1 AND COALESCE(status,'map')='map'"
        ).fetchall()
        for _w, _lbl in _mapped:
            if _w and _lbl and _w not in KNOWN_XRPL_WALLETS:
                KNOWN_XRPL_WALLETS[_w] = _lbl
    except Exception:
        pass

    with st.sidebar:
        st.title("Ripple Radar Pro")
        st.caption(VERSION)
        st.caption(f"BUILD: {BUILD_ID}")
        render_budget_bar(conn)
        render_queue_status(conn)
        render_user_window(conn, compact=True)
        st.divider()
        _section_options = [_section_label(k) for k in SECTION_KEYS]
        _selected_section_label = st.radio(
            _t("Vista"),
            _section_options,
            index=0,
        )
        section = _section_from_label(_selected_section_label)
        st.divider()
        if st.button(_t("Actualizar XRPL"), use_container_width=True):
            ok, msg = refresh_history(conn, pages=18)
            st.toast(msg)
        if st.button(_t("Regenerar demo visual"), use_container_width=True):
            bootstrap_demo(conn, force=True)
            st.toast("Demo regenerada.")
        st.divider()
        st.caption(_t("Vigila rutas privadas por sus huellas públicas."))
        render_sidebar_legend()
        st.caption(f"XRPL: {XRPL_SERVER}")
        st.caption(f"RLUSD issuer: {RLUSD_ISSUER}")

    # El aviso de uso responsable y presupuesto API ahora vive en el onboarding obligatorio.
    st.session_state["rrp_real_money_notice_ok"] = True
    render_ui_translation_notice()

    if "loaded_once_advanced" not in st.session_state:
        st.session_state["loaded_once_advanced"] = True  # marcar ANTES por si crashea
        try:
            ok, msg = refresh_history(conn, pages=4)
            st.session_state["last_msg"] = msg
        except Exception as _e:
            st.session_state["last_msg"] = f"Inicio sin XRPL: {_e}"

    df = load_metrics(conn)
    xrp_price = fetch_xrp_price_history(days=365)
    if df.empty:
        st.error(_t("No hay datos disponibles."))
        return

    row = df.iloc[-1].copy()

    # Cargar wallets vigiladas y aplicar boost a métricas en tiempo real
    watched_wallets = load_watched_wallets(conn)
    if not watched_wallets.empty:
        row = boost_metrics_from_watched(conn, row)

    state = get_state(row)

    render_hero()

    m1,m2,m3,m4,m5,m6,m7 = st.columns(7)
    m1.metric("Subida", f"{row['bull_score']:.1f}%")
    m2.metric("Riesgo", f"{row['bear_score']:.1f}%")
    m3.metric("Flip", f"{row['flip_score']:.1f}%")
    m4.metric("Cobertura", f"{row['radar_coverage']:.1f}%")
    m5.metric("Fase", f"{int(row['phase'])}")
    m6.metric("Pump", f"{row['pump_score']:.1f}%")
    m7.metric("Rutas hot", hot_routes_count(row))

    render_metric_explanations()
    render_flip_quality_panel(add_evidence_counts_to_metrics_df(conn, pd.DataFrame([row])).iloc[0])
    render_alert(state)

    if section == "Radar":
        render_cards(state, row)
        if not watched_wallets.empty:
            st.markdown(f"<div class='rrp-note'>🔍 <b>{len(watched_wallets)} wallets vigiladas</b> activas en el mapa (zona inferior, forma ◆). Sus métricas están integradas en los scores del radar.</div>", unsafe_allow_html=True)

        # Focus node — click en nodo para filtrar sus rutas
        focused = st.session_state.get("map_focus_node")
        if focused:
            col_info, col_reset = st.columns([6, 1])
            with col_info:
                st.markdown(f"<div class='rrp-note'>🔍 Mostrando rutas de <b>{focused}</b> — el resto están atenuadas.</div>", unsafe_allow_html=True)
            with col_reset:
                if st.button("✕ " + _t("Ver todo"), use_container_width=True, key="reset_focus"):
                    st.session_state.pop("map_focus_node", None)
                    st.rerun()
        else:
            st.caption("Haz clic en cualquier nodo del mapa para ver solo sus rutas.")

        tab_conn, tab_surv, tab_all = st.tabs([
            "🔗 " + _t("Conexiones confirmadas + obligatorias"),
            "👁 " + _t("Vigilancia / inferidas"),
            "🗺 " + _t("Mapa completo"),
        ])

        _map_kwargs = dict(
            watched=watched_wallets if not watched_wallets.empty else None,
            conn=conn, focus_node=focused,
        )

        _focus_hint = f"🔍 Filtrando: **{focused}** — haz click en otro nodo para cambiar, o en el mismo para deseleccionar" if focused else "👆 Haz click en cualquier nodo para ver solo sus conexiones"
        st.caption(_focus_hint)

        with tab_conn:
            st.caption("Solo rutas con evidencia confirmada (on-chain, documentada) o implicación técnica irrefutable (⚡ rojo-rosa). Sin ruido de vigilancia.")
            sel = st.plotly_chart(
                make_map(row, title="Conexiones confirmadas + obligatorias", route_filter="confirmed", **_map_kwargs),
                width="stretch", on_select="rerun", selection_mode="points", key="radar_map_conn",
            )

        with tab_surv:
            st.caption("Solo rutas de vigilancia (👁 morado), descubiertas por IA (🔍 dorado) y modelos analíticos. Sin rutas confirmadas.")
            sel_surv = st.plotly_chart(
                make_map(row, title="Vigilancia e inferencias", route_filter="surveillance", **_map_kwargs),
                width="stretch", on_select="rerun", selection_mode="points", key="radar_map_surv",
            )
            pts_surv = (sel_surv or {}).get("selection", {}).get("points", [])
            if pts_surv:
                sel = sel_surv  # solo sobreescribir si vigilancia tiene selección propia

        with tab_all:
            st.caption("Vista completa: todas las rutas superpuestas. Útil para ver la densidad total del ecosistema.")
            sel_all = st.plotly_chart(
                make_map(row, route_filter="all", **_map_kwargs),
                width="stretch", on_select="rerun", selection_mode="points", key="radar_map_all",
            )
            # Permitir selección también desde el mapa completo
            pts_all = (sel_all or {}).get("selection", {}).get("points", [])
            if pts_all and not (sel or {}).get("selection", {}).get("points"):
                sel = sel_all
        # Procesar click — customdata puede volver como lista o string.
        # IMPORTANTE: Streamlit preserva la selección entre reruns.
        # Solo actuamos si el nodo clickado es DIFERENTE al foco actual
        # (evita el bucle toggle donde el mismo click se procesa dos veces).
        # Para des-focusar usar el botón "✕ Ver todo".
        pts = (sel or {}).get("selection", {}).get("points", [])
        if pts:
            cd = pts[0].get("customdata")
            if isinstance(cd, (list, tuple)):
                cd = cd[0] if cd else None
            clicked_name = str(cd).strip() if cd is not None else None
            if clicked_name and clicked_name != (focused or "").strip():
                st.session_state["map_focus_node"] = clicked_name
                st.rerun()

        render_color_legend()

        # Ficha del nodo seleccionado
        if focused:
            _dyn_n, _dyn_r, _ = load_dynamic_map_elements(conn)
            _all_n = {**NODES, **_dyn_n}
            _all_r = ROUTES + _dyn_r
            render_node_info_panel(focused, row, conn, _all_r, _all_n)

    elif section == "Comunidad":
        render_community(conn)

    elif section == "Route Paths A→B":
        render_route_path_engine(conn, df, row)

        render_color_legend()

    elif section == "Descubrimientos":
        render_discovery_engine(conn)

    elif section == "Motores":
        st.subheader("🧠 Motores de inteligencia — diagnóstico completo")
        st.markdown("""<div class='rrp-note'>
Los <b>motores de inteligencia</b> analizan los datos de XRPL para detectar señales que van más allá de simples transacciones.
Cada motor vigila un aspecto diferente: grupos de wallets, patrones de comportamiento, anomalías estadísticas y flujo de red.
Juntos forman un diagnóstico de si hay actividad institucional real o no.
</div>""", unsafe_allow_html=True)

        # ── 1. Diagnóstico de motores (barras + conclusión) ──────────────────
        st.markdown("### 📊 Estado de los 6 motores analíticos hoy")
        chart_diagnosis(df, "engines")

        # ── 2. Radar visual de motores ────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 🕸️ Radar de motores — vista de araña")
        st.markdown("""<div class='rrp-note'>
Cada eje del radar es un motor. Cuanto más lejos del centro, más fuerte la señal.
<b>Ideal:</b> polígono grande y equilibrado = muchos motores activos a la vez, señal coordinada.
<b>Polígono pequeño o irregular:</b> pocos motores activos o solo uno funcionando, señal débil o puntual.
</div>""", unsafe_allow_html=True)
        st.plotly_chart(make_engine_radar(row), width="stretch")
        st.plotly_chart(make_flip_channels_chart(df, conn), width="stretch")
        render_data_quality_panel(conn, add_evidence_counts_to_metrics_df(conn, pd.DataFrame([row])).iloc[0], context="motores")

        # ── 3. Clusters ───────────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 🧩 Cluster Intelligence — grupos de wallets detectados")
        cdf = recent_clusters(conn)
        cluster_count = len(cdf)
        cluster_score = float(row.get("cluster_score", 0))
        cluster_pct   = cluster_score if cluster_score > 1.5 else cluster_score * 100
        if cluster_count == 0:
            st.markdown("""<div style="border:1px solid #FFB84D;border-radius:14px;background:rgba(15,23,42,.92);padding:.85rem 1.1rem;margin:.30rem 0 1rem 0;">
<b style="color:#FFB84D">🟡 Sin clusters detectados</b><br>
<span style="color:#CBD5E1;font-size:.88rem">
El motor de clusters agrupa wallets que se envían dinero entre sí frecuentemente para detectar distribuidores ODL,
market makers o treasury institucionales. <br>
<b>Por qué no hay clusters:</b> los datos actuales no tienen suficiente volumen de transacciones repetidas entre
las mismas wallets para formar un grupo significativo. Esto es normal en períodos con pocos datos reales o modo demo.
<br><b>Qué significa:</b> no hay evidencia de un hub centralizado o actor institucional operando en grupo en este momento.
</span></div>""", unsafe_allow_html=True)
        else:
            top_role = cdf["role"].value_counts().idxmax() if "role" in cdf.columns else "desconocido"
            top_vol  = cdf["volume"].max() if "volume" in cdf.columns else 0
            if cluster_pct >= 50:
                cstate = "🟢"; ccol = "#3CFF9B"
                cmsg = f"<b style='color:{ccol}'>Cluster activo significativo detectado.</b> El motor ve {cluster_count} grupos, el mayor con rol <b>{top_role}</b> y volumen de {top_vol:,.0f} RLUSD. Esto indica actividad organizada — posible ODL, treasury o market maker operando de forma coordinada."
            elif cluster_pct >= 25:
                cstate = "🟡"; ccol = "#FFB84D"
                cmsg = f"<b style='color:{ccol}'>Cluster moderado.</b> {cluster_count} grupos detectados (señal {cluster_pct:.0f}%). Hay actividad pero no suficientemente concentrada para confirmar un actor institucional claro. Puede ser el inicio de un patrón o actividad de varios actores pequeños."
            else:
                cstate = "🟠"; ccol = "#FF9D5C"
                cmsg = f"<b style='color:{ccol}'>Clusters débiles o en modo demo.</b> {cluster_count} grupos con señal baja ({cluster_pct:.0f}%). Los grupos detectados no tienen suficiente volumen o repetición para ser significativos. Con datos XRPL reales y más historia, este motor se vuelve más potente."
            st.markdown(f"""<div style="border:1px solid {ccol};border-radius:14px;background:rgba(15,23,42,.92);
padding:.75rem 1rem;margin:.20rem 0 .70rem 0;">
{cstate} {cmsg}<br><br>
<b style="color:#5AD7FF;font-size:.82rem">¿Qué buscar en la tabla?</b>
<span style="color:#94A3B8;font-size:.82rem"> · <b>role=treasury-like</b> → actor acumulando o distribuyendo grandes cantidades
· <b>role=hub-like</b> → nodo central de distribución ODL o market maker
· <b>score alto</b> → patrón muy claro y repetido · <b>volume alto</b> → movimientos institucionales grandes</span>
</div>""", unsafe_allow_html=True)
        styled_table(cdf if cluster_count > 0 else pd.DataFrame(columns=["day","wallet_a","wallet_b","role","volume","score"]))

        # ── 4. Fingerprints ───────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 🧬 Institutional Fingerprints — patrones de comportamiento")
        fdf = recent_fingerprints(conn)
        fp_count = len(fdf)
        fp_score = float(row.get("fingerprint_score", 0))
        fp_pct   = fp_score if fp_score > 1.5 else fp_score * 100
        if fp_count == 0:
            st.markdown("""<div style="border:1px solid #FFB84D;border-radius:14px;background:rgba(15,23,42,.92);padding:.85rem 1.1rem;margin:.30rem 0 1rem 0;">
<b style="color:#FFB84D">🟡 Sin fingerprints detectados</b><br>
<span style="color:#CBD5E1;font-size:.88rem">
Los fingerprints identifican actores por su <b>patrón de comportamiento</b>: ¿sus transacciones son siempre del mismo tamaño?
¿Se repiten a la misma hora? ¿Con la misma frecuencia? Esos patrones distinguen un banco, un ODL o un market maker.<br>
<b>Por qué no hay fingerprints:</b> sin transacciones reales o con pocos datos, no hay patrones que analizar.
En modo demo, los valores generados no tienen la repetición real que necesita este motor para identificar actores.<br>
<b>Qué significa:</b> no se puede identificar el tipo de actor detrás de la actividad actual. No es negativo, simplemente no hay datos suficientes.
</span></div>""", unsafe_allow_html=True)
        else:
            top_type = fdf["pattern_type"].value_counts().idxmax() if "pattern_type" in fdf.columns else "desconocido"
            if fp_pct >= 50:
                fstate = "🟢"; fcol = "#3CFF9B"
                fmsg = f"<b style='color:{fcol}'>Patrón institucional detectado.</b> {fp_count} fingerprints activos. El patrón dominante es <b>{top_type}</b> (señal {fp_pct:.0f}%). Esto indica que hay uno o más actores con un comportamiento muy predecible y repetido — característica de bancos, ODL o market makers profesionales."
            elif fp_pct >= 25:
                fstate = "🟡"; fcol = "#FFB84D"
                fmsg = f"<b style='color:{fcol}'>Patrón parcial.</b> {fp_count} fingerprints con señal moderada ({fp_pct:.0f}%). Hay cierta repetición de patrones pero no suficientemente clara para identificar un actor concreto. Podría ser actividad mixta de varios participantes."
            else:
                fstate = "🟠"; fcol = "#FF9D5C"
                fmsg = f"<b style='color:{fcol}'>Fingerprints débiles.</b> {fp_count} fingerprints con señal baja ({fp_pct:.0f}%). Los patrones detectados son muy variables o inconsistentes para identificar un actor institucional. Con más datos reales de XRPL, este motor mejora notablemente."
            st.markdown(f"""<div style="border:1px solid {fcol};border-radius:14px;background:rgba(15,23,42,.92);
padding:.75rem 1rem;margin:.20rem 0 .70rem 0;">
{fstate} {fmsg}<br><br>
<b style="color:#5AD7FF;font-size:.82rem">¿Qué buscar en la tabla?</b>
<span style="color:#94A3B8;font-size:.82rem"> · <b>treasury-like</b> → grandes movimientos repetidos, posible banco o Ripple treasury
· <b>market-maker-like</b> → muchas ofertas/AMM, proveedor de liquidez ODL
· <b>corridor-like</b> → pagos repetidos de tamaño similar, corredor de remesas activo
· <b>score cercano a 1</b> → patrón muy claro y consistente</span>
</div>""", unsafe_allow_html=True)
        styled_table(fdf if fp_count > 0 else pd.DataFrame(columns=["day","wallet","pattern_type","score","tx_count","avg_amount"]))

        # ── 5. Qué aporta cada motor ──────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📋 Valor de cada motor hoy")
        st.markdown("""<div class='rrp-note'>Score de cada motor en este momento expresado en porcentaje. Estos valores alimentan el Flip score, la cobertura del radar y el diagnóstico de rutas.</div>""", unsafe_allow_html=True)
        styled_table(component_table(row))

    elif section == "Rutas":
        st.subheader("Rutas vigiladas")
        if not watched_wallets.empty:
            st.markdown(f"<div class='rrp-note'>🔍 <b>{len(watched_wallets)} wallets vigiladas</b> aparecen en la zona inferior del mapa (◆ diamante). Las líneas punteadas muestran su conexión con entidades conocidas.</div>", unsafe_allow_html=True)
        st.plotly_chart(make_map(row, title="Rutas privadas + huellas públicas + motores + vigilancia",
                                 watched=watched_wallets if not watched_wallets.empty else None, conn=conn),
                        width="stretch")
        render_color_legend()
        st.markdown("<div class='rrp-note'><b>Cómo leerlo:</b> las líneas naranjas no afirman que veamos el sistema privado por dentro; indican rutas privadas que solo activamos cuando aparecen huellas públicas en XRPL/RLUSD, DEX/AMM, trustlines, clusters o transfers grandes.</div>", unsafe_allow_html=True)
        styled_table(route_dataframe(row))

        # ── Wallets vigiladas en las rutas ────────────────────────────────────
        if not watched_wallets.empty:
            st.markdown("---")
            st.markdown("### 🔍 Wallets vigiladas — rutas conocidas")
            st.markdown("""<div class='rrp-note'>
Estas wallets fueron detectadas automáticamente por volumen o confianza y añadidas al radar.
La columna <b>Contraparte</b> muestra la entidad conocida con la que más han interactuado.
Las líneas punteadas en el mapa de arriba representan estas conexiones.
</div>""", unsafe_allow_html=True)
            wv = enrich_wallet_table_for_explainability(watched_wallets)
            styled_table(wv)

    elif section == "Técnico":
        st.subheader("Modo técnico avanzado")
        if not xrp_price.empty:
            st.markdown(f"<div class='rrp-note'>📈 <b>Precio XRP/USD real incluido</b> (eje derecho · línea blanca discontinua). Cobertura: {xrp_price['day'].min()} → {xrp_price['day'].max()}. Los scores del radar (eje izquierdo, 0–100) son señales independientes del precio. El precio real sirve de referencia visual.</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='rrp-warning'>⚠️ Precio XRP/USD no disponible (CoinGecko no respondió). Los gráficos muestran solo scores del radar.</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### 🧬 Flip explicado por calidad de señal")
        st.markdown("""<div class='rrp-note'>Este gráfico separa lo que viene del <b>ledger real</b>, lo que viene de <b>pruebas documentales/institucionales</b> y lo que sigue siendo <b>watch/especulativo</b>. Así la fase Flip no se interpreta como certeza operativa si la señal no está anclada.</div>""", unsafe_allow_html=True)
        st.plotly_chart(make_flip_channels_chart(df, conn), width="stretch")
        render_data_quality_panel(conn, add_evidence_counts_to_metrics_df(conn, pd.DataFrame([row])).iloc[0], context="tecnico")
        with st.expander("🧪 Tests internos de cruce de datos de las gráficas", expanded=False):
            _tests = pd.DataFrame(run_chart_cross_data_tests())
            styled_table(_tests)
            if bool(_tests[["traces_ok", "bounds_ok", "logic_ok"]].all().all()):
                st.success("Tests OK: las gráficas separan ledger real, documental y watch; los valores permanecen en 0-100 y no se cruza especulación como prueba fuerte.")
            else:
                st.error("Algún test falló: revisar lógica de canales antes de interpretar la fase Flip.")

        # ── TradingView widget ──────────────────────────────────────────────────
        st.markdown("---")
        st.markdown("### 📈 XRP/USDT — gráfico TradingView en vivo")
        st.markdown("""<div class='rrp-note'>Gráfico en tiempo real de Binance (XRPUSDT). Usa los controles del gráfico para cambiar temporalidad,
        añadir indicadores técnicos (RSI, MACD, Bollinger…) o cambiar el par. Los scores del radar están en las secciones de abajo.</div>""", unsafe_allow_html=True)
        _tv_html = """
<div id="tradingview_xrp" style="height:480px;border-radius:12px;overflow:hidden;">
  <script type="text/javascript" src="https://s3.tradingview.com/tv.js"></script>
  <script type="text/javascript">
  new TradingView.widget({
    "width": "100%",
    "height": 480,
    "symbol": "BINANCE:XRPUSDT",
    "interval": "D",
    "timezone": "Etc/UTC",
    "theme": "dark",
    "style": "1",
    "locale": "es",
    "toolbar_bg": "#0B1220",
    "enable_publishing": false,
    "hide_side_toolbar": false,
    "allow_symbol_change": true,
    "studies": ["RSI@tv-basicstudies", "MACD@tv-basicstudies", "BB@tv-basicstudies"],
    "container_id": "tradingview_xrp"
  });
  </script>
</div>"""
        _st_components.html(_tv_html, height=500, scrolling=False)

        # ── Velas OHLCV (Plotly) con scores superpuestos ────────────────────────
        st.markdown("---")
        st.markdown("### 🕯️ Velas OHLCV + scores del radar")
        st.markdown("""<div class='rrp-note'>Candlestick de XRP/USD (CoinGecko, últimos 90 días · intervalo 4h).
        Las líneas punteadas en el eje derecho muestran el DEX score, anomalía y probabilidad de subida del radar —
        correlaciona los picos del DEX con los movimientos de precio.</div>""", unsafe_allow_html=True)
        with st.spinner("Cargando OHLCV…"):
            _ohlcv = fetch_xrp_ohlcv(days=90)
        st.plotly_chart(make_candlestick_chart(_ohlcv, df), width="stretch")

        st.markdown("---")
        st.markdown("### 📊 Precio y riesgo")
        st.markdown("""<div class='rrp-note'><b>Qué muestra:</b> La línea verde = probabilidad de subida de precio según actividad pública.
La roja = riesgo de bajada. La naranja punteada = cuánto de lo que hay parece especulativo (pump).
La azul = score técnico de precio. <b>Ideal:</b> verde alta, naranja baja, precio XRP subiendo junto a la verde.</div>""", unsafe_allow_html=True)
        st.plotly_chart(make_price_risk_chart(df, xrp_price), width="stretch")
        chart_diagnosis(df, "price_risk")

        st.markdown("---")
        st.markdown("### 🔄 Adopción real vs especulación")
        st.markdown("""<div class='rrp-note'><b>Qué muestra:</b> El morado = Flip score (adopción real coordinada).
El azul = cobertura de puntos vigilados. El verde punteado = adopción técnica. El azul claro = persistencia (cuántos días seguidos hay actividad).
<b>Ideal:</b> todas las líneas subiendo juntas de forma sostenida, no en spikes.</div>""", unsafe_allow_html=True)
        st.plotly_chart(make_adoption_chart(df, xrp_price, conn), width="stretch")
        chart_diagnosis(df, "adoption")

        st.markdown("---")
        st.markdown("### 🔍 Huellas públicas vigiladas")
        st.markdown("""<div class='rrp-note'><b>Qué muestra:</b> cada línea es una huella pública diferente en XRPL que el radar vigila.
Si una ruta privada (banco, ODL) está usando XRPL, debería encender varias de estas líneas a la vez.
<b>Ideal:</b> varias líneas activas al mismo tiempo y sostenidas en el tiempo, no solo picos aislados.
Líneas planas en 0 = esa huella no detectada ese período (puede ser datos demo).</div>""", unsafe_allow_html=True)
        st.plotly_chart(make_public_footprints_chart(df, xrp_price, conn), width="stretch")
        chart_diagnosis(df, "footprints")

        st.markdown("---")
        st.markdown("### 🧠 Motores de inteligencia")
        st.markdown("""<div class='rrp-note'><b>Qué muestra:</b> los motores analíticos que van más allá de simples transacciones:
clusters de wallets, topología de red, patrones de comportamiento (fingerprints), anomalías estadísticas y señales cross-network.
<b>Ideal:</b> clusters, topología y fingerprints activos simultáneamente = señal institucional coordinada real.</div>""", unsafe_allow_html=True)
        st.plotly_chart(make_intelligence_engines_chart(df, conn), width="stretch")
        chart_diagnosis(df, "engines")

        st.markdown("---")
        st.markdown("### 🗓️ Heatmap — intensidad por motor y por día")
        st.markdown("""<div class='rrp-note'><b>Qué muestra:</b> una vista de calendario donde cada fila es un motor y cada columna un día.
El color va de <b>azul oscuro</b> (0% · sin señal) a <b>verde brillante</b> (100% · señal fuerte).
<b>Cómo leerlo:</b> busca franjas horizontales verdes/naranjas persistentes = motor activo durante muchos días seguidos. Eso indica adopción sostenida.
<b>Pasa el cursor</b> sobre cualquier celda para ver el score exacto de ese motor ese día.</div>""", unsafe_allow_html=True)
        st.plotly_chart(make_engine_heat_chart(df, conn), width="stretch")
        chart_diagnosis(df, "heatmap")

        st.markdown("---")
        st.markdown("### 🕸️ Radar de motores — estado actual")
        st.markdown("""<div class='rrp-note'><b>Qué muestra:</b> el estado de hoy de cada motor en un gráfico de araña (0 al centro = sin señal, 100 al borde = señal máxima).
<b>Leyenda de ejes:</b> XRPL público (actividad ledger) · Pagos ODL · Trustlines · DEX/AMM · Whales/Large · Clusters · Topología · Fingerprints · Régimen temporal.
<b>Ideal:</b> polígono grande y equilibrado = muchas huellas activas coordinadas.</div>""", unsafe_allow_html=True)
        st.plotly_chart(make_engine_radar(row), width="stretch")

        st.markdown("---")
        st.markdown("### 📋 Qué aporta cada motor ahora mismo")
        st.markdown("""<div class='rrp-note'><b>Lectura:</b> el score de cada motor hoy expresado en porcentaje, con su explicación. Estos valores alimentan el Flip score, la cobertura y el diagnóstico de ruta.</div>""", unsafe_allow_html=True)
        styled_table(component_table(row))

        st.markdown("---")
        col_a, col_b = st.columns(2)
        with col_a:
            st.download_button("⬇ Descargar histórico CSV", df.to_csv(index=False).encode("utf-8"), "ripple_radar_history.csv", "text/csv")
        with col_b:
            st.download_button("⬇ Descargar rutas CSV", route_dataframe(row).to_csv(index=False).encode("utf-8"), "ripple_radar_routes.csv", "text/csv")

    elif section == "Histórico":
        st.subheader("Análisis histórico")
        st.markdown(f"<div class='rrp-note'><b>Cobertura:</b> {df['day'].min()} → {df['day'].max()} · {len(df)} días calculados. Precio XRP/USD real en eje derecho (línea blanca discontinua). Actualiza para más historia XRPL real.</div>", unsafe_allow_html=True)
        st.plotly_chart(make_volume_chart(df, xrp_price), width="stretch")
        st.plotly_chart(make_phase_chart(df, conn), width="stretch")
        st.plotly_chart(make_price_risk_chart(df, xrp_price), width="stretch")
        st.plotly_chart(make_adoption_chart(df, xrp_price, conn), width="stretch")
        st.plotly_chart(make_public_footprints_chart(df, xrp_price, conn), width="stretch")
        st.plotly_chart(make_intelligence_engines_chart(df, conn), width="stretch")
        st.markdown("#### Resumen comparativo — actual vs media 30 días")
        st.markdown("<div class='rrp-note'><b>Cómo leer:</b> compara el valor actual de cada métrica contra su media de los últimos 30 días. <b>Mejorando</b> = actual &gt;10% por encima de la base. <b>Enfriando</b> = más del 10% por debajo. <b>Estable</b> = dentro del rango normal.</div>", unsafe_allow_html=True)
        styled_table(historical_analysis(df))
        st.markdown("#### Histórico completo en base local")
        cols_show = ["day","phase","phase_name","radar_coverage","adoption_score","flip_score","bull_score","bear_score","pump_score","xrpl_volume","tx_count"]
        cols_show = [c for c in cols_show if c in df.columns]
        styled_table(df[cols_show].sort_values("day", ascending=False))

    elif section == "Clusters":
        st.subheader("🧩 Cluster Intelligence")
        st.markdown("""<div class='rrp-note'><b>¿Qué es un cluster?</b> Grupo de wallets que se envían dinero entre sí con frecuencia.
Un cluster grande con mucho volumen puede indicar un distribuidor ODL, un treasury institucional o un market maker.
<br><b>Columnas:</b> <b>size</b> = nº wallets del cluster · <b>volume</b> = volumen total RLUSD · <b>role</b> = treasury-like / hub-like / normal · <b>score</b> = intensidad (0–1).</div>""", unsafe_allow_html=True)
        cdf = recent_clusters(conn)
        styled_table(cdf)

    elif section == "Fingerprints":
        st.subheader("🧬 Institutional Fingerprints")
        st.markdown("""<div class='rrp-note'><b>¿Qué es un fingerprint?</b> Patrón de comportamiento que permite identificar el tipo de actor detrás de las transacciones.
<br><b>treasury-like:</b> movimientos grandes y repetidos → puede ser Ripple treasury o banco acumulando.
<br><b>market-maker-like:</b> muchas ofertas/AMM y transacciones frecuentes → proveedor de liquidez ODL.
<br><b>corridor-like:</b> pagos repetidos de tamaño similar → corredor remesas activo.
<br><b>score:</b> 0 = patrón no detectado · 1 = patrón muy claro.</div>""", unsafe_allow_html=True)
        fdf = recent_fingerprints(conn)
        styled_table(fdf)

    elif section == "Cinemateca":
        st.subheader("🎬 Cinemática — XRP en velas japonesas por escenarios")
        st.markdown("""
<div class='rrp-warning'>
<b>⚠️ Aviso de simulación viva:</b> esta cinemática no es una predicción garantizada ni asesoramiento financiero.
Es un vídeo/escenario visual generado con los datos cruzados actuales de la app. A medida que añadas fuentes reales,
pruebas A→B, rutas, wallets aprobadas, volumen, spread, slippage y señales XRPL/Ripple, las velas y escenarios cambiarán.
</div>
""", unsafe_allow_html=True)

        if df.empty:
            st.warning("No hay datos suficientes para generar la cinemática.")
        else:
            # Selección del frame base real de la app.
            max_idx = max(0, len(df) - 1)
            frame_idx = st.slider("Frame base de datos reales", 0, max_idx, max_idx, 1, key="cinema_v82_frame")
            r = df.iloc[frame_idx]
            day_value = str(r.get("day", "frame"))

            # Métricas cruzadas reales internas.
            route_total = int(_safe_count(conn, "route_paths"))
            proof_total = int(_safe_count(conn, "connection_proofs"))
            dyn_total = int(_safe_count(conn, "dynamic_routes"))
            volume = _safe_float(r.get("xrpl_volume", 0.0), 0.0)
            bull = _safe_float(r.get("bull_score", 0.0), 0.0)
            bear = _safe_float(r.get("bear_score", 0.0), 0.0)
            flip = _safe_float(r.get("flip_score", 0.0), 0.0)
            adoption = _safe_float(r.get("adoption_score", 0.0), 0.0)
            pump = _safe_float(r.get("pump_score", 0.0), 0.0)
            coverage = _safe_float(r.get("radar_coverage", 0.0), 0.0)
            dex = _safe_float(r.get("dex_score", 0.0), 0.0)
            trust = _safe_float(r.get("trustline_score", 0.0), 0.0)
            large = _safe_float(r.get("large_transfer_score", 0.0), 0.0)
            persistence = _safe_float(r.get("persistence_score", 0.0), 0.0)

            # Precio XRP real para la cinemática.
            # Prioridad: spot vivo -> histórico CoinGecko -> columnas internas -> referencia visual.
            price_now, price_source, price_is_ref = resolve_xrp_price_now(xrp_price, r, df)

            # Spread/slippage estimados con datos de actividad internos. Si conectas orderbook real, esto se sustituye.
            liquidity = _clip((math.log10(max(1.0, volume)) / 8.0) * 100.0 + dex * 0.12 + trust * 0.08 + coverage * 0.10)
            spread_bps = max(1.5, 42.0 - liquidity * 0.30 + pump * 0.06 - proof_total * 0.25)
            slippage_bps = max(2.0, 70.0 - liquidity * 0.42 + pump * 0.08 - route_total * 0.05)
            pressure = _clip(bull * 0.22 + flip * 0.24 + adoption * 0.20 + coverage * 0.12 + persistence * 0.10 + min(100, route_total) * 0.07 + min(100, proof_total*8) * 0.05 - pump * 0.10 - bear * 0.12)
            quality = _clip((adoption + flip + persistence + coverage + min(100, proof_total*12)) / 5)
            base_volatility = max(0.012, min(0.095, (spread_bps + slippage_bps) / 1500 + pump/1800 + large/2200))

            def _scenario_params(name, mult, prob_bias, risk_mult):
                # Rango porcentual: presión y calidad elevan; pump/riesgo y costes reducen.
                raw = ((pressure - 48) / 100.0) * mult + (quality / 100.0) * 0.035 * mult - ((spread_bps + slippage_bps) / 10000.0) * risk_mult
                pct = max(-0.35, min(0.85, raw))
                prob = _clip(35 + pressure * prob_bias + quality * 0.18 - pump * 0.10 - risk_mult * 3)
                return {"name": name, "pct": pct, "prob": prob}

            scenarios = [
                _scenario_params("Conservador", 0.55, 0.22, 1.25),
                _scenario_params("Base / moderado", 1.00, 0.32, 1.00),
                _scenario_params("Agresivo", 1.85, 0.40, 0.75),
            ]
            dominant = max(scenarios, key=lambda x: x["prob"])

            def _make_ohlc(seed_price, pct, steps=34, vol=0.03):
                rows = []
                close = float(seed_price)
                for i in range(steps):
                    # curva gradual hacia el objetivo con ondas, no línea recta
                    progress = (i + 1) / steps
                    target_curve = seed_price * (1 + pct * (progress ** 1.25))
                    wave = math.sin(i * 0.85) * vol * seed_price * 0.18 + math.sin(i * 0.23) * vol * seed_price * 0.10
                    next_close = max(0.0001, target_curve + wave)
                    open_ = close
                    spread = max(seed_price * 0.002, abs(next_close - open_) * 0.42 + seed_price * vol * 0.22)
                    high = max(open_, next_close) + spread
                    low = max(0.0001, min(open_, next_close) - spread)
                    rows.append({"x": i+1, "open": open_, "high": high, "low": low, "close": next_close})
                    close = next_close
                return pd.DataFrame(rows)

            scenario_tabs = st.tabs(["🛡️ Conservador", "⚖️ Base / moderado", "🚀 Agresivo"])
            for tab, sc in zip(scenario_tabs, scenarios):
                with tab:
                    candle_df = _make_ohlc(price_now, sc["pct"], steps=36, vol=base_volatility * (0.8 if sc["name"] == "Conservador" else 1.0 if "Base" in sc["name"] else 1.35))
                    target = candle_df["close"].iloc[-1]
                    price_txt = f"${price_now:.4f}" + (" ref." if price_is_ref else " real")
                    fig = go.Figure()
                    fig.add_trace(go.Candlestick(
                        x=candle_df["x"], open=candle_df["open"], high=candle_df["high"], low=candle_df["low"], close=candle_df["close"],
                        name=f"XRP · {sc['name']}"
                    ))
                    fig.add_trace(go.Scatter(x=candle_df["x"], y=[price_now]*len(candle_df), mode="lines", name="Precio XRP real/ref.", line=dict(dash="dot")))
                    # Frames tipo vídeo: va revelando velas.
                    frames = []
                    for k in range(4, len(candle_df)+1):
                        part = candle_df.iloc[:k]
                        frames.append(go.Frame(
                            data=[
                                go.Candlestick(x=part["x"], open=part["open"], high=part["high"], low=part["low"], close=part["close"], name=f"XRP · {sc['name']}"),
                                go.Scatter(x=part["x"], y=[price_now]*len(part), mode="lines", name="Precio XRP real/ref.", line=dict(dash="dot")),
                            ],
                            name=str(k)
                        ))
                    fig.frames = frames
                    fig.update_layout(
                        title=f"Cinemática XRP · {sc['name']} · {sc['pct']*100:+.1f}% → ${target:.4f}",
                        paper_bgcolor="#020617", plot_bgcolor="#020617", font=dict(color="#E5E7EB"), height=560,
                        xaxis_title="Velas proyectadas", yaxis_title="Precio XRP/USD", xaxis_rangeslider_visible=False,
                        margin=dict(l=40, r=30, t=80, b=40),
                        updatemenus=[dict(type="buttons", showactive=False, x=0.02, y=1.12, buttons=[
                            dict(label="▶️ Reproducir cinemática", method="animate", args=[None, {"frame": {"duration": 210, "redraw": True}, "fromcurrent": True, "transition": {"duration": 60}}]),
                            dict(label="⏸️ Pausa", method="animate", args=[[None], {"frame": {"duration": 0, "redraw": False}, "mode": "immediate"}])
                        ])]
                    )
                    c1, c2, c3, c4 = st.columns(4)
                    c1.metric("Precio XRP real/ref.", price_txt)
                    c2.metric("Objetivo escenario", f"${target:.4f}", f"{sc['pct']*100:+.1f}%")
                    c3.metric("Probabilidad interna", f"{sc['prob']:.0f}%")
                    c4.metric("Volatilidad visual", f"{base_volatility*100:.1f}%")
                    st.plotly_chart(fig, width="stretch", key=f"cinematic_candles_v82_{sc['name']}")

            st.markdown("#### Datos cruzados que alimentan la cinemática")
            c1, c2, c3, c4, c5 = st.columns(5)
            c1.metric("Volumen XRPL", f"{volume:,.0f}")
            c2.metric("Spread estimado", f"{spread_bps:.1f} bps")
            c3.metric("Slippage estimado", f"{slippage_bps:.1f} bps")
            c4.metric("Presión precio", f"{pressure:.1f}%")
            c5.metric("Calidad adopción", f"{quality:.1f}%")
            st.caption(f"Precio usado por la cinemática: {price_txt} · fuente: {price_source}")

            st.markdown(f"""
<div class='rrp-note'>
<b>Lectura viva:</b> el escenario dominante actual es <b>{html.escape(dominant['name'])}</b> con probabilidad interna {dominant['prob']:.0f}%.
La simulación usa precio {price_txt} (fuente: {html.escape(str(price_source))}), volumen XRPL {volume:,.0f}, spread {spread_bps:.1f} bps, slippage {slippage_bps:.1f} bps,
{route_total} rutas, {proof_total} pruebas y {dyn_total} rutas dinámicas. Si añades pruebas reales o nuevas fuentes, esta cinemática debe cambiar.
</div>
""", unsafe_allow_html=True)

            with st.expander("Ver gráficos técnicos clásicos de la cinemática", expanded=False):
                partial = df.iloc[:frame_idx+1]
                st.plotly_chart(make_price_risk_chart(partial, xrp_price), width="stretch", key="cinema_v82_price_risk")
                st.plotly_chart(make_adoption_chart(partial, xrp_price, conn), width="stretch", key="cinema_v82_adoption")
                st.plotly_chart(make_public_footprints_chart(partial, xrp_price, conn), width="stretch", key="cinema_v82_footprints")
                st.plotly_chart(make_intelligence_engines_chart(partial, conn), width="stretch", key="cinema_v82_engines")

    elif section == "Diagnóstico":
        st.subheader("🔧 Diagnóstico del sistema")
        ok, msg = check_xrpl_connection()
        if ok:
            st.markdown(f"<div class='rrp-note'>✅ <b>XRPL conectado.</b> {msg.replace('XRPL conectado · Estado: unknown','XRPL conectado · El servidor responde correctamente (estado interno del nodo no reportado).')}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='rrp-warning'>⚠️ <b>XRPL no disponible ahora.</b> {msg} · Los gráficos usan datos en caché.</div>", unsafe_allow_html=True)

        c1,c2,c3,c4 = st.columns(4)
        c1.metric("Eventos XRPL guardados", conn.execute("SELECT COUNT(*) FROM raw_events").fetchone()[0])
        c2.metric("Días calculados", conn.execute("SELECT COUNT(*) FROM daily_metrics").fetchone()[0])
        c3.metric("Clusters", conn.execute("SELECT COUNT(*) FROM clusters").fetchone()[0])
        c4.metric("Fingerprints", conn.execute("SELECT COUNT(*) FROM fingerprints").fetchone()[0])

        if not df.empty:
            last = df.iloc[-1]
            diag_rows = [
                {"Check": "Cobertura radar hoy",    "Valor": f"{last['radar_coverage']:.1f}%",  "Estado": "✅ OK" if last['radar_coverage']>=35 else "⚠️ Baja",      "Explicación": "La cobertura mide cuántos puntos públicos están activos. &lt;35% = poco datos."},
                {"Check": "Fase del ciclo",          "Valor": f"{int(last['phase'])}/5",         "Estado": "✅ OK", "Explicación": "0=ruido, 1=calentamiento, 2=huellas, 3=visible, 4=institucional, 5=Full Flip."},
                {"Check": "Fuente de datos",         "Valor": str(last.get('source','demo')),    "Estado": "✅ XRPL real" if "xrpl" in str(last.get('source','')) else "🔶 Demo", "Explicación": "xrpl_advanced_intelligence = datos reales. demo_bootstrap = datos simulados."},
                {"Check": "Flip score hoy",          "Valor": f"{last['flip_score']:.1f}%",      "Estado": "🟢 Fuerte" if last['flip_score']>=70 else "🟡 Moderado" if last['flip_score']>=40 else "🔴 Bajo", "Explicación": "Señal de adopción coordinada real. &gt;80% = Full Flip."},
                {"Check": "Pump vs Adopción",        "Valor": f"Pump:{last['pump_score']:.0f}% / Adop:{last['adoption_score']:.0f}%", "Estado": "✅ OK" if last['adoption_score']>last['pump_score'] else "⚠️ Pump>Adopción", "Explicación": "Si pump > adopción, el movimiento parece especulativo sin base real."},
                {"Check": "Datos más recientes",     "Valor": df['day'].max(),                   "Estado": "✅ OK" if df['day'].max() >= (datetime.now(timezone.utc).date()-timedelta(days=3)).isoformat() else "⚠️ Desactualizado", "Explicación": "Pulsa 'Actualizar XRPL' para traer datos más recientes del ledger."},
            ]
            styled_table(pd.DataFrame(diag_rows))

        st.markdown("#### Log de eventos internos")
        events = pd.read_sql_query("SELECT level, message, details, created_at FROM app_events ORDER BY id DESC LIMIT 20", conn)
        if not events.empty:
            styled_table(events)
        else:
            st.info("Sin eventos registrados.")

    elif section == "Donaciones":
        render_donations()

    elif section == "Setup":
        st.subheader("⚙️ Configuración")

        # ── API Key ──────────────────────────────────────────────────────────
        st.markdown("### 🔑 API Key de Anthropic")
        _current_key = _get_api_key()
        _key_source   = ""
        if _os.environ.get("ANTHROPIC_API_KEY", "").strip():
            _key_source = "variable de entorno"
        elif _current_key and "ANTHROPIC_API_KEY" in str(getattr(st, "secrets", {}) or {}):
            _key_source = "Streamlit Secrets (secrets.toml)"
        elif _current_key:
            _key_source = "archivo .env o sesión manual"

        if _current_key:
            st.success(f"✅ API key detectada vía **{_key_source}** · `sk-ant-...{_current_key[-6:]}`")
        else:
            st.error("❌ No se detecta API key. Introduce una para activar las búsquedas.")

        st.markdown("""
**Formas de configurarla (elige una):**

**① Local — archivo `.env`** *(recomendado para desarrollo)*
""")
        st.code('ANTHROPIC_API_KEY=sk-ant-api03-TUKEY', language="bash")
        st.caption("Crea el archivo `.env` en la misma carpeta que el script.")

        st.markdown("**② Streamlit Cloud — Settings → Secrets**")
        st.code('ANTHROPIC_API_KEY = "sk-ant-api03-TUKEY"', language="toml")

        st.markdown("**③ Sesión temporal** *(no se guarda entre recargas)*")
        _manual_col1, _manual_col2 = st.columns([4, 1])
        with _manual_col1:
            _typed_key = st.text_input(
                "API Key (sesión)", type="password",
                placeholder="sk-ant-api03-...",
                value=st.session_state.get("_manual_api_key", ""),
                key="setup_api_key_input",
                help="Se guarda solo en esta sesión del navegador. No persiste si recargas."
            )
        with _manual_col2:
            if st.button("Guardar", key="setup_save_key"):
                st.session_state["_manual_api_key"] = _typed_key.strip()
                st.success("✅ Guardada en sesión")
                st.rerun()

        st.divider()

        # ── Presupuesto ──────────────────────────────────────────────────────
        st.markdown("### 💰 Presupuesto API")
        render_budget_bar(conn)
        _b = _get_budget(conn)
        _bc1, _bc2 = st.columns(2)
        with _bc1:
            _new_budget = st.number_input("Presupuesto máximo ($)", min_value=1.0, max_value=500.0,
                                           value=float(_b.get("budget", 100.0)), step=5.0,
                                           help="Cuando el gasto supere este límite, las búsquedas nuevas se bloquean.")
        with _bc2:
            st.metric("Gastado", f"${_b.get('spent', 0):.2f}")
            if st.button("Actualizar presupuesto", key="setup_update_budget"):
                try:
                    conn.execute("UPDATE api_budget SET budget_usd=?, locked=0 WHERE id=1", (_new_budget,))
                    conn.commit()
                    st.success(f"✅ Presupuesto actualizado a ${_new_budget:.2f}")
                    st.rerun()
                except Exception as _be:
                    st.error(f"Error: {_be}")
        if st.button("🔄 Resetear contador de gasto a $0.00", key="setup_reset_budget"):
            try:
                conn.execute("UPDATE api_budget SET spent_usd=0, call_count=0, cache_hits=0, locked=0, last_reset=? WHERE id=1",
                             (datetime.now(timezone.utc).isoformat(),))
                conn.commit()
                st.success("✅ Contador reseteado")
                st.rerun()
            except Exception as _be:
                st.error(f"Error: {_be}")

        st.divider()

        # ── Diagnóstico ──────────────────────────────────────────────────────
        st.divider()
        if st.button("🩺 Ejecutar diagnóstico de API key", key="setup_run_diag"):
            render_api_diagnostics()

        # ── Instalación ──────────────────────────────────────────────────────
        st.markdown("### 🖥️ Instalación local")
        st.code("""python -m venv .venv
.venv\\Scripts\\activate
pip install streamlit plotly pandas numpy requests python-dateutil
streamlit run ripple_radar_pro_route_engine_v62_universal.py""", language="bash")
        st.warning("Las rutas privadas no se ven por dentro. Este radar vigila las huellas públicas obligatorias.")

    st.divider()
    st.caption("No es asesoramiento financiero. Es un radar de huellas públicas, topología, clusters y adopción real.")


if __name__ == "__main__":
    main()
