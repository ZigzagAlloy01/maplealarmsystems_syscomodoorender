import base64
import os
import re
import xmlrpc.client

import requests

try:
    from config import MAPLE_PASSWORD as CONFIG_MAPLE_PASSWORD
except ImportError:
    CONFIG_MAPLE_PASSWORD = ""

try:
    from config import SYSCOM_TOKEN as CONFIG_SYSCOM_TOKEN
except ImportError:
    CONFIG_SYSCOM_TOKEN = ""

try:
    from config import TOKEN as CONFIG_TOKEN
except ImportError:
    CONFIG_TOKEN = ""

ODOO_URL = os.getenv("ODOO_URL", "https://maplealarmsystems.odoo.com")
ODOO_DB = os.getenv("ODOO_DB", "maplealarmsystems")
ODOO_USERNAME = os.getenv("ODOO_USERNAME", "sistemas@storemaple.com")
ODOO_PASSWORD = os.getenv("ODOO_PASSWORD", CONFIG_MAPLE_PASSWORD)
BASE_URL = os.getenv("SYSCOM_BASE_URL", "https://developers.syscom.mx/api/v1/").rstrip("/") + "/"
SYSCOM_TOKEN = os.getenv("SYSCOM_TOKEN") or os.getenv("TOKEN") or CONFIG_SYSCOM_TOKEN or CONFIG_TOKEN

REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
PRICE_KEY = "precio_descuento"
PRICE_KEY_FALLBACK = "precio_descuentos"
PRICE_ADJUSTMENT_FACTOR = 0.96000735416
DISPLAY_CURRENCY = "MXN"
CLEAR_QUOTATION_DESCRIPTION = True
SYSCOM_MONEDA = "mxn"
SYSCOM_IVA_FRONTERA = "false"
SYSCOM_CON_IMPUESTOS = "false"

SUPPLIER_NAME = "Sistemas y Servicios de Comunicacion"
SUPPLIER_UOM_NAME = "Unidades"
SUPPLIER_CURRENCY_NAME = "MXN"
SUPPLIER_MIN_QTY = 1.0

SALE_FACTOR_1 = 1.04
SALE_FACTOR_IVA = 1.14

DEFAULT_MODELS = """DS-PD201MC-WB
DS-PKF201-WB
DS-PD201PC10-WB
DS-PD201P10-WB
AXHOME-KIT-GSM
AXHOME-KIT-WIFI
DS-PC201N
DS-PA201P-16WB
DS-PA201PS-16WB/A-LA
DS-PS201-WB
DS-PK201B-WB
DS-PDEB1-EG2-WB(B)
DS-PDEBP1-EG2-WB
DS-PDMC-EG2-WB(B)
DS-PDMCS-EG2-WB(B)
DS-PDMCX-E-WB
DS-PKF1-WB(B)
DS-PDPC12P-EG2-WB(B)
DS-PDBG8-EG2-WB
DS-PDP18-HM-WB
DS-PDC15-EG2-WB(B)
DS-PDP15P-EG2-WB(B)
DS-PDSMK-E-WB
DS-PDMCK-EG2-WB(B)
DS-PDHT-E-WB
DS-PM1-I16O2-WB
DS-PM1-O1H-WB
DS-PWA48-K
DS-PWA48-KSLIM
AXPRO-KIT
DS-PWA48-KS
DS-PWA48-KS-SLIM
AXPRO-KIT-GSM
DS-PT1-WB
DS-PWA48-E-WB
DS-PM1-O1L-WB
DS-PR1-WB
DS-PDPG12P-EG2-WB
DS-PS1-I-WB(B)
DS-PS1-E-WB/B
DS-PS1-E-WB/R
DS-PK1-LT-WB
DS-PK1-E-WB
PL-DC-1000
PSD1202D
P12DC3A
JR53X
JR52X
DS-2CD1023G2-LIU
DS-2CV1023G2-LIDWF(B)
THC-B120-MC
CR123A
CR2025PM
CR2450PL/5B
CR2032PM
CR-2
LK5.512
LK712
2103-1101/1000
DS-1LN5EO-UU/E
PRO-CAT-5E
PRO-CAT-5E-W
PRO-CAT-6-PLUSW
PROB400
SS-078Q
TTHDMI1.8M
TTHDMI10M
TT-HDMI-3M
TT-HDMI-5M
GW-44-003
321-DCD-ABG
321-DCBD-ABG
321-DCBI-ABG
321-DCI-ABG
MAG600NTLED
MN01-LTE-M
SF-2071-AR
SF-2041
SF-3012
SF-2033
PRO138CS
PROT400
XB-T23
DS-1272ZJ-120
IDS-7216HQHI-M1/T
IDS-7204HQHI-M1/T
IDS-7208HQHI-M1/XT
DS-PDP18-EG2(B)
VXI-ST
DS-PDBG8-EG2
WD23PURZ
WD33PURZ
WD64PURZ
WD11PURZ
DS-2CV2121G2-IDW(W)
DS-2CV2141G2-IDW(W)
DS-2CD1143G2-LIUF
VGA-1.5M
VGA-5M
DS-KB8113-IME1(B)
XP18DC20HD
AC-PS-T12-05
PL-4C-15DC
PL-8C-15DC
IMP-30-V3
IPC-B121H-C
IPC-T221H-C
IDS-7208HQHI-M1/T
TT150USB
TT-672PRO
TT372EDID4K
TT-101-F-TURBO
DS-KIS312-P
TT373KVM4.0
TT223KVM
DS-1272ZJ-120
BZL600N
BU600NDLED
DS-7616NI-Q2/16P(D)
DS-7604NI-Q1/4P(D)
DS-7608NI-Q1/8P(D)
XB-REC2
PROR400
SF-581A
V300X/500GB
DS-PDCL12-EG2
BXS-ST
BXS-R
SF-581A
SF-747A
DS-K1T805MX
DS-2CV1F23G2-LIDWF(B)
DS-2CV1F43G2-LIDWF(B)
THC-T120-M
DS-KV6113-PE1(C)
SF-BUZZER
B8-TURBO-C/A
E8-TURBO-C/A
DS-2CD1043G2-LIDUF/4G/SL/LA/FUS
DS-2CD1043G2-LIU(F)
DS-2CD1123G2-LIU
DS-PDC10AM-EG2-WB
AXPRO-KIT-PIR
DS-PWA48-M-WB
UAP-AC-LITE
JR-52
AP201
STI-6402
STI-6400
DS-2CV2021G2-IDW(W)
DS-2CD1043G0-I(C)
IPC-B640H-Z(C)
DS-2CD1063G2-LIU
THC-B129-P
B8-TURBO-PC/A
THC-B220-M
B8-TURBO-G2W
CS-H3C
LK1812
CR1220
BEW2ODPB
DS-K1T804AEF
ACCESS-184/500
4311-1104/1000
4306-1104/1000
SF16AWG500
NUR6C04BU-C
PUR6C04BU-F
DS-MCW406/128G
TC5-100
APBHVC
ACCESS40
PRO800B
PRO-CAT-5E-W/500
TT-HDMI-1M
HIK-ACCORD
PCC53
LP-UT6-100-BU28
LP-UT6-200-BU28
UTP28SP1BU
UTP28SP7BU
LP-UT3-200-BU
AWG50
PST-1010-ER
PRO800-BOX
LP-WBX-200
DS-1280ZJ-XS
DS-1280ZJ-DM46
JBX3510WH-A
CS-EB8-4G
TMK-1020-SD
PT-48-SD
TMK-1720
TEK-100
EF-150-LC
MAG350NLEDB
S-CH-19X1U
CJ688TGBU
DS-K2602T
DS-K2621X
DS-K2624X
DS-K2704X
TAPO-C320WS
TAPO-C500
W8
DS-U02
DS-U02P
AE-DC5013-F6
AE-DC4328-K5
DS-3E1505P-EI/M
DS-PWA48-KSV2
IDS-7216HQHI-M1/XT
DVR-204G-M1(C)
SF-119-2H
WD102PURP
WD8002PURP
TT312HDR-V2.0
DS-2CD1143G0-I(C)
DS-2DE2C400SCG-E(F1)
DS-2DE4825IWG1-E
DS-2CE76D0T-ITMF(C)
DMC-4FT
SYS12000/127AFV2
SYS12000/127V3
SYSNG-HS
DS-K1F820-F
BG12-LX-SP
DS-K2M002X
AC-PS-T12-05
DS-2FA1225-C4/K
DS-2FA1205-C8/K
PS-12DC4KV
PS-12-DC-4C
PL-36V-2A
PST-3040-20A
SR-1909-GN2G
SR1912LH3G
SR-1906-LH3G
SR1909LH3G
IPC-B141H-C
IPC-D141H-C
POE24V
LAS30-57CN-RJ45
DS-1005KI
LP-TAT-12
B8TURBOG2P/A/XPS
KEVTX8T4BW/A
KEVTX8T8BG/A
AE-DI2032-G40(B)
KIPCV2M/4B
KIPCV2M/8B
DS-3WF02-5AC/D
DS-2XS2T47G1-LDH/4G/C18S40
DS-2XS3Q47G1-LDH/4G/C18S40
LOCOM2-TT68344K
DS-3WF1000-EI-2N
DS-KIS313-P
KDP-601A1M/MS2D
TT-4816-PVTURBO
TT-101-PV-TURBO
TT-USB-100
PROXPOINT
DS-K1101M
DS-K1801EK
DS-K1201A-EF
SYSLETV2
HCT-ACCESO-1P-1A
DS-2CD3956G2-IS(U)
DS-2CD2955G0-ISU
AMP30
TARJET-WIFI-SLIM
DS-KH6350-WTE1
DS-D5032F3-1V0S
PST-MOUNT-POLE-V2
DS-1661ZJ
U-MOUNT
90372
HTCM-1U
DS-8632NXI-K8
DS-7732NXI-I4/16P/S(E)
NVR-108H-D/8P(D)
DS-7608NI-Q1/8P(E)
LPCM-042U
DS-2DE4225IW-DE(T5)
ES-50X
LP-PP-607
DS-2CD6425G1-20
CFPE1WHY
SYS-POST-4
SYS-POST-3
C5X
KL2V2
RE200
PSTRD1M
DS-3WR12C
V300X/1TB
VOUCHERLTEM
P2RLEDSP
DS-3E1526P-EI/M
TL-SG1016D
SS090
WI-PS526G
DS-3E1552P-SI
DS-3E1105P-EI/M
DS-3E1309P-EI/M
DS-3E0106HP-E
GWN7700M
ACCESS-CARD-M1K
ACCESS-PROX-CARD
PROXCARD26
ATR-14
ACF-43
DS-K1T805MBFWX
ACF-44
LP-DWC2
HK-SFP-1.25G-20-1310-DF
DS-2CD1343G0-I(C)
IPC-T641H-Z(C)
LP1000LCD
EPU1500LCD
PR2200RT2U
OR500LCDRM1UA
UT-750GU
SL750U
DS-7632NXI-K2/16P(E)
THC-B257-LTS
THC-T129-PS
DS-2CE10DF0T-F
DS-2CE10UF3T-E
DS-2CE70DF0T-MF
DS-2CE72KF0T-FS
DS-9664NI-M8
DS-2CD2143G2-LIS2U
DS-2CD1027G2H-LIUF
DS-2CE16D0T-LFS
DS-2CE16K0T-LFS
DS-2CE76D0T-LMFS
DS-2CE76K0T-LMFS
IPC-B120HA-LUC
DS-2CD1023G2-LIU(F)
DS-2CD1063G2-LIU(F)
DS-2CD1083G2-LIU(F)
DS-2CD1T83G2-LIU(F)
DS-2CD1123G2-LIU(F)
DS-2CD1163G2-LIU
DS-2CD1163G2-LIUF
KIT-3K-DL
DS-2CD1323G2-LIU
DS-2CD1343G2-LIUF
DS-2DE2C400MWG-E
DS-2CD2T47G2P-LSU/SL(C)
DS-2CD2T87G2-PLSU/SL(C)
DS-2CD2347G2P-LSU/SL(C)
HL-24B-KIT
DS-2CD2387G2P-LSU/SL(C)
DS-2SE3C404MWG-E/14
DS-2SE4C425MWG-E/26(F0)
"""


class SyscomSyncCore:
    def __init__(self, logger=None):
        self.logger = logger or print
        self.validar_configuracion()

        self.session = requests.Session()
        self.session.headers.update(self.obtener_headers_syscom())

        self.common = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/common")
        self.uid = self.common.authenticate(ODOO_DB, ODOO_USERNAME, ODOO_PASSWORD, {})
        if not self.uid:
            raise Exception("Error de autenticacion con Odoo. Verifica credenciales/API Key")

        version = self.common.version()
        self.log(f"Conectado a Odoo: {version}")

        self.models = xmlrpc.client.ServerProxy(f"{ODOO_URL}/xmlrpc/2/object")
        self.product_template_fields = self.obtener_campos_modelo("product.template")
        self.unspsc_fields = self.obtener_campos_modelo("product.unspsc.code")
        self.supplierinfo_fields = self.obtener_campos_modelo("product.supplierinfo")
        self.partner_fields = self.obtener_campos_modelo("res.partner")
        self.uom_fields = self.obtener_campos_modelo("uom.uom")
        self.currency_fields = self.obtener_campos_modelo("res.currency")

        self.productos_cache = {}
        self.preview_cache = []
        self.tax_cache = {}
        self.unspsc_cache = {}
        self.modelos_no_encontrados = []
        self.partner_cache = {}
        self.uom_cache = {}
        self.currency_cache = {}

    def log(self, mensaje):
        if self.logger:
            self.logger(str(mensaje))

    def validar_configuracion(self):
        faltantes = []
        if not ODOO_PASSWORD:
            faltantes.append("MAPLE_PASSWORD / ODOO_PASSWORD")
        if not SYSCOM_TOKEN:
            faltantes.append("SYSCOM_TOKEN o TOKEN")

        if faltantes:
            raise Exception(
                "Faltan variables de configuracion: "
                + ", ".join(faltantes)
                + ". Define estos valores en config.py o variables de entorno."
            )

    @staticmethod
    def parsear_modelos_texto(texto):
        vistos = set()
        modelos = []
        for linea in str(texto or "").splitlines():
            modelo = linea.strip()
            if not modelo or modelo.lower().startswith("pega aqui"):
                continue
            modelo_upper = modelo.upper()
            if modelo_upper not in vistos:
                modelos.append(modelo)
                vistos.add(modelo_upper)
        return modelos

    def obtener_campos_modelo(self, modelo):
        try:
            data = self.models.execute_kw(
                ODOO_DB,
                self.uid,
                ODOO_PASSWORD,
                modelo,
                "fields_get",
                [],
                {"attributes": ["string", "type"]},
            )
            return set(data.keys())
        except Exception as e:
            self.log(f"No fue posible consultar fields_get para {modelo}: {e}")
            return set()

    def obtener_headers_syscom(self):
        return {
            "Authorization": f"Bearer {SYSCOM_TOKEN}",
            "Accept": "application/json",
        }

    def obtener_params_syscom(self, termino=None):
        params = {
            "moneda": SYSCOM_MONEDA,
            "iva_frontera": SYSCOM_IVA_FRONTERA,
            "con_impuestos": SYSCOM_CON_IMPUESTOS,
        }
        if termino is not None:
            params["busqueda"] = termino
        return params

    def normalizar_numero(self, valor):
        if valor is None:
            return None

        if isinstance(valor, (int, float)):
            return float(valor)

        texto = str(valor).strip()
        if not texto:
            return None

        match = re.search(r"-?\d[\d.,]*", texto)
        if not match:
            return None

        numero = match.group(0)
        if "," in numero and "." not in numero:
            numero = numero.replace(",", ".")
        else:
            numero = numero.replace(",", "")

        try:
            return float(numero)
        except ValueError:
            return None

    def normalizar_modelo_clave(self, texto):
        return re.sub(r"[^A-Z0-9]", "", str(texto or "").upper())

    def buscar_clave_recursiva(self, data, claves):
        claves_normalizadas = {str(clave).strip().lower() for clave in claves}

        if isinstance(data, dict):
            for key, value in data.items():
                if str(key).strip().lower() in claves_normalizadas:
                    return value
            for value in data.values():
                encontrado = self.buscar_clave_recursiva(value, claves)
                if encontrado is not None:
                    return encontrado

        if isinstance(data, list):
            for item in data:
                encontrado = self.buscar_clave_recursiva(item, claves)
                if encontrado is not None:
                    return encontrado

        return None

    def obtener_cache_key_producto(self, producto):
        return str(producto.get("producto_id") or self.obtener_modelo_producto(producto) or "").strip()

    def obtener_modelo_producto(self, producto):
        return str(producto.get("modelo") or "").strip()

    def obtener_nombre_producto(self, producto):
        return str(producto.get("titulo") or "Producto SYSCOM").strip()

    def obtener_precio_lista(self, producto):
        precios = producto.get("precios", {})
        return self.normalizar_numero(precios.get("precio_lista")) or 0.0

    def obtener_precio_especial(self, producto):
        precios = producto.get("precios", {})
        return self.normalizar_numero(precios.get("precio_especial")) or 0.0

    def obtener_precio_compra(self, precios):
        valor = precios.get(PRICE_KEY)
        if valor is None:
            valor = precios.get(PRICE_KEY_FALLBACK)
        if valor is None:
            valor = precios.get("precio_especial", 0)
        precio_base = float(valor or 0)
        return round(precio_base * PRICE_ADJUSTMENT_FACTOR, 2)

    def obtener_multiplicador_venta(self, precio_compra):
        if precio_compra <= 0:
            return 0.0
        if precio_compra < 3:
            return 3.0
        if precio_compra < 5:
            return 2.0
        if precio_compra < 50:
            return 1.8
        if precio_compra < 75:
            return 1.7
        if precio_compra < 100:
            return 1.6
        if precio_compra < 160:
            return 1.5
        if precio_compra < 500:
            return 1.4
        if precio_compra < 1000:
            return 1.3
        return 1.2

    def obtener_precio_venta(self, producto):
        precio_compra = self.obtener_precio_compra(producto.get("precios", {}))
        if precio_compra <= 0:
            return 0.0

        multiplicador = self.obtener_multiplicador_venta(precio_compra)
        precio_venta = precio_compra * SALE_FACTOR_1 * multiplicador * SALE_FACTOR_IVA
        return round(precio_venta, 2)

    def obtener_sat_producto(self, producto):
        valor = self.buscar_clave_recursiva(producto, ("sat_key", "sat"))
        return str(valor or "").strip()

    def obtener_peso_producto(self, producto):
        valor = self.buscar_clave_recursiva(
            producto,
            ("peso", "weight", "peso_kg", "peso_neto", "peso_bruto"),
        )
        return self.normalizar_numero(valor)

    def obtener_volumen_producto(self, producto):
        valor = self.buscar_clave_recursiva(
            producto,
            ("volumen", "volume", "volumen_m3", "cubicaje"),
        )
        return self.normalizar_numero(valor)

    def obtener_stock_producto(self, producto):
        return float(producto.get("total_existencia", 0) or 0)

    def buscar_unspsc_odoo(self, sat_key):
        sat_key = (sat_key or "").strip()
        if not sat_key:
            return None

        if sat_key in self.unspsc_cache:
            return self.unspsc_cache[sat_key]

        candidate_fields = [field for field in ("code", "name", "unspsc_code") if field in self.unspsc_fields]
        if not candidate_fields:
            self.unspsc_cache[sat_key] = None
            return None

        base_domain = []
        if "applies_to" in self.unspsc_fields:
            base_domain.append(["applies_to", "=", "product"])

        for field in candidate_fields:
            try:
                encontrados = self.models.execute_kw(
                    ODOO_DB,
                    self.uid,
                    ODOO_PASSWORD,
                    "product.unspsc.code",
                    "search_read",
                    [[*base_domain, [field, "=", sat_key]]],
                    {"fields": ["id", field], "limit": 1},
                )
                if encontrados:
                    self.unspsc_cache[sat_key] = encontrados[0]["id"]
                    return encontrados[0]["id"]
            except Exception as e:
                self.log(f"No se pudo buscar UNSPSC por {field} para SAT {sat_key}: {e}")

        if "name" in self.unspsc_fields:
            try:
                encontrados = self.models.execute_kw(
                    ODOO_DB,
                    self.uid,
                    ODOO_PASSWORD,
                    "product.unspsc.code",
                    "search_read",
                    [[*base_domain, ["name", "ilike", sat_key]]],
                    {"fields": ["id", "name"], "limit": 1},
                )
                if encontrados:
                    self.unspsc_cache[sat_key] = encontrados[0]["id"]
                    return encontrados[0]["id"]
            except Exception as e:
                self.log(f"No se pudo hacer fallback UNSPSC para SAT {sat_key}: {e}")

        self.unspsc_cache[sat_key] = None
        return None

    def buscar_partner_id(self, nombre_partner):
        cache_key = nombre_partner.strip().lower()
        if cache_key in self.partner_cache:
            return self.partner_cache[cache_key]

        dominios = []
        if "name" in self.partner_fields:
            dominios.append([["name", "=", nombre_partner]])
            dominios.append([["name", "ilike", nombre_partner]])

        for domain in dominios:
            try:
                partners = self.models.execute_kw(
                    ODOO_DB,
                    self.uid,
                    ODOO_PASSWORD,
                    "res.partner",
                    "search_read",
                    [domain],
                    {"fields": ["id", "name"], "limit": 1},
                )
                if partners:
                    partner_id = partners[0]["id"]
                    self.partner_cache[cache_key] = partner_id
                    return partner_id
            except Exception as e:
                self.log(f"No se pudo buscar proveedor '{nombre_partner}': {e}")

        self.partner_cache[cache_key] = None
        return None

    def buscar_uom_id(self, nombre_uom):
        cache_key = nombre_uom.strip().lower()
        if cache_key in self.uom_cache:
            return self.uom_cache[cache_key]

        dominios = []
        if "name" in self.uom_fields:
            dominios.append([["name", "=", nombre_uom]])
            dominios.append([["name", "ilike", nombre_uom]])
            dominios.append([["name", "ilike", "Unidad"]])
            dominios.append([["name", "ilike", "Unid"]])
            dominios.append([["name", "ilike", "Unit"]])

        for domain in dominios:
            try:
                uoms = self.models.execute_kw(
                    ODOO_DB,
                    self.uid,
                    ODOO_PASSWORD,
                    "uom.uom",
                    "search_read",
                    [domain],
                    {"fields": ["id", "name"], "limit": 1},
                )
                if uoms:
                    uom_id = uoms[0]["id"]
                    self.uom_cache[cache_key] = uom_id
                    return uom_id
            except Exception as e:
                self.log(f"No se pudo buscar unidad '{nombre_uom}': {e}")

        self.uom_cache[cache_key] = None
        return None

    def buscar_currency_id(self, currency_name):
        cache_key = currency_name.strip().lower()
        if cache_key in self.currency_cache:
            return self.currency_cache[cache_key]

        dominios = []
        if "name" in self.currency_fields:
            dominios.append([["name", "=", currency_name]])
            dominios.append([["name", "ilike", currency_name]])
        if "full_name" in self.currency_fields:
            dominios.append([["full_name", "ilike", currency_name]])
        if "symbol" in self.currency_fields:
            dominios.append([["symbol", "=", currency_name]])

        for domain in dominios:
            try:
                currencies = self.models.execute_kw(
                    ODOO_DB,
                    self.uid,
                    ODOO_PASSWORD,
                    "res.currency",
                    "search_read",
                    [domain],
                    {"fields": ["id", "name", "symbol"], "limit": 1},
                )
                if currencies:
                    currency_id = currencies[0]["id"]
                    self.currency_cache[cache_key] = currency_id
                    return currency_id
            except Exception as e:
                self.log(f"No se pudo buscar moneda '{currency_name}': {e}")

        self.currency_cache[cache_key] = None
        return None

    def obtener_uom_template_id(self, template_id):
        fields = []
        if "uom_po_id" in self.product_template_fields:
            fields.append("uom_po_id")
        if "uom_id" in self.product_template_fields:
            fields.append("uom_id")
        if not fields:
            return None

        try:
            templates = self.models.execute_kw(
                ODOO_DB,
                self.uid,
                ODOO_PASSWORD,
                "product.template",
                "read",
                [[template_id]],
                {"fields": fields},
            )
            if not templates:
                return None

            template = templates[0]
            for field in ("uom_po_id", "uom_id"):
                valor = template.get(field)
                if isinstance(valor, list) and valor:
                    return valor[0]
            return None
        except Exception as e:
            self.log(f"No se pudo leer la unidad del producto template {template_id}: {e}")
            return None

    def actualizar_proveedor_compra(self, template_id, producto):
        partner_id = self.buscar_partner_id(SUPPLIER_NAME)
        if not partner_id:
            self.log(f"No se encontro el proveedor '{SUPPLIER_NAME}' en Odoo")
            return

        if "partner_id" not in self.supplierinfo_fields:
            self.log("El modelo product.supplierinfo no expone el campo partner_id en esta base")
            return

        uom_id = self.buscar_uom_id(SUPPLIER_UOM_NAME)
        currency_id = self.buscar_currency_id(SUPPLIER_CURRENCY_NAME)

        domain = [["partner_id", "=", partner_id]]
        if "product_tmpl_id" in self.supplierinfo_fields:
            domain.append(["product_tmpl_id", "=", template_id])

        supplier_fields = ["id", "partner_id"]
        if "product_tmpl_id" in self.supplierinfo_fields:
            supplier_fields.append("product_tmpl_id")
        if "price" in self.supplierinfo_fields:
            supplier_fields.append("price")
        if "product_uom_id" in self.supplierinfo_fields:
            supplier_fields.append("product_uom_id")
        if "currency_id" in self.supplierinfo_fields:
            supplier_fields.append("currency_id")

        supplier_lines = self.models.execute_kw(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            "product.supplierinfo",
            "search_read",
            [domain],
            {"fields": supplier_fields, "limit": 1},
        )

        if not uom_id and supplier_lines:
            existente_uom = supplier_lines[0].get("product_uom_id")
            if isinstance(existente_uom, list) and existente_uom:
                uom_id = existente_uom[0]

        if not uom_id:
            uom_id = self.obtener_uom_template_id(template_id)

        if not uom_id:
            self.log(
                f"No se encontro la unidad '{SUPPLIER_UOM_NAME}' en Odoo ni una unidad fallback en el producto {template_id}; "
                "se actualizara proveedor sin tocar unidad."
            )

        vals = {"partner_id": partner_id}
        if "min_qty" in self.supplierinfo_fields:
            vals["min_qty"] = SUPPLIER_MIN_QTY
        if "product_uom_id" in self.supplierinfo_fields and uom_id:
            vals["product_uom_id"] = uom_id
        if "price" in self.supplierinfo_fields:
            vals["price"] = self.obtener_precio_compra(producto.get("precios", {}))
        if "currency_id" in self.supplierinfo_fields and currency_id:
            vals["currency_id"] = currency_id

        if supplier_lines:
            supplierinfo_id = supplier_lines[0]["id"]
            self.models.execute_kw(
                ODOO_DB,
                self.uid,
                ODOO_PASSWORD,
                "product.supplierinfo",
                "write",
                [[supplierinfo_id], vals],
            )
        else:
            if "product_tmpl_id" in self.supplierinfo_fields:
                vals["product_tmpl_id"] = template_id
            self.models.execute_kw(
                ODOO_DB,
                self.uid,
                ODOO_PASSWORD,
                "product.supplierinfo",
                "create",
                [vals],
            )

    def buscar_producto_syscom_por_modelo(self, modelo):
        response = self.session.get(
            f"{BASE_URL}productos",
            params=self.obtener_params_syscom(modelo),
            timeout=REQUEST_TIMEOUT,
        )
        response.raise_for_status()
        datos = response.json()

        modelo_normalizado = self.normalizar_modelo_clave(modelo)
        for producto in datos.get("productos", []):
            modelo_api = self.normalizar_modelo_clave(producto.get("modelo"))
            if modelo_api == modelo_normalizado:
                return producto
        return None

    def obtener_producto_detallado_syscom(self, producto):
        producto_id = producto.get("producto_id")
        if not producto_id:
            return producto

        try:
            response = self.session.get(
                f"{BASE_URL}productos/{producto_id}",
                params=self.obtener_params_syscom(),
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            detalle = response.json()
            if isinstance(detalle, dict):
                combinado = dict(producto)
                combinado.update(detalle)
                return combinado
        except Exception as e:
            self.log(f"No se pudo obtener detalle de SYSCOM para {producto_id}: {e}")

        return producto

    def cargar_productos(self, modelos):
        if not modelos:
            raise ValueError("No hay modelos para consultar")

        self.productos_cache.clear()
        self.preview_cache = []
        self.modelos_no_encontrados = []

        encontrados = 0
        for modelo in modelos:
            try:
                producto = self.buscar_producto_syscom_por_modelo(modelo)
                if not producto:
                    self.modelos_no_encontrados.append(modelo)
                    continue

                cache_key = self.obtener_cache_key_producto(producto)
                self.productos_cache[cache_key] = producto
                encontrados += 1
            except Exception as e:
                self.modelos_no_encontrados.append(f"{modelo} (error: {e})")
                self.log(f"Error consultando SYSCOM para modelo {modelo}: {e}")

        return {
            "modelos_solicitados": len(modelos),
            "encontrados": encontrados,
            "no_encontrados": len(self.modelos_no_encontrados),
            "moneda_mostrada": DISPLAY_CURRENCY,
        }

    def guardar_modelos_no_encontrados(self, path):
        with open(path, "w", encoding="utf-8") as f:
            for modelo in self.modelos_no_encontrados:
                limpio = modelo.split(" (error:", 1)[0]
                f.write(limpio + "\n")

    def formatear_estado_carga(self, summary):
        return (
            f"Lista procesada.\n\n"
            f"Modelos solicitados: {summary['modelos_solicitados']}\n"
            f"Encontrados en SYSCOM: {summary['encontrados']}\n"
            f"No encontrados: {summary['no_encontrados']}\n"
            f"Moneda mostrada: {DISPLAY_CURRENCY}\n\n"
            "Haz clic en 'Previsualizar Odoo' para revisar estado en Odoo."
        )

    def es_fault_none_xmlrpc(self, error):
        return isinstance(error, xmlrpc.client.Fault) and "cannot marshal None unless allow_none is enabled" in error.faultString

    def obtener_impuestos_por_ids(self, tax_ids):
        faltantes = [tax_id for tax_id in tax_ids if tax_id not in self.tax_cache]
        if faltantes:
            try:
                taxes = self.models.execute_kw(
                    ODOO_DB,
                    self.uid,
                    ODOO_PASSWORD,
                    "account.tax",
                    "read",
                    [faltantes],
                    {"fields": ["name", "amount", "type_tax_use", "price_include"]},
                )
                for tax in taxes:
                    self.tax_cache[tax["id"]] = tax
            except Exception as e:
                self.log(f"No se pudieron consultar impuestos: {e}")

        return [self.tax_cache[tax_id] for tax_id in tax_ids if tax_id in self.tax_cache]

    def formatear_impuestos(self, tax_ids):
        taxes = self.obtener_impuestos_por_ids(tax_ids)
        if not taxes:
            return "sin impuestos configurados"

        partes = []
        for tax in taxes:
            sufijo = " incluido" if tax.get("price_include") else ""
            partes.append(f"{tax.get('name', 'Impuesto')} ({tax.get('amount', 0)}%{sufijo})")
        return ", ".join(partes)

    def buscar_producto_odoo(self, modelo):
        fields = ["id", "name", "default_code", "list_price", "taxes_id"]
        if "unspsc_code_id" in self.product_template_fields:
            fields.append("unspsc_code_id")
        if "weight" in self.product_template_fields:
            fields.append("weight")
        if "volume" in self.product_template_fields:
            fields.append("volume")
        if "is_storable" in self.product_template_fields:
            fields.append("is_storable")
        if "image_1920" in self.product_template_fields:
            fields.append("image_1920")
        return self.models.execute_kw(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            "product.template",
            "search_read",
            [[["default_code", "=", modelo]]],
            {"fields": fields, "limit": 1},
        )

    def obtener_url_imagen(self, producto):
        if producto.get("img_portada"):
            return producto["img_portada"]

        for imagen in producto.get("imagenes", []):
            if isinstance(imagen, str) and imagen.startswith("http"):
                return imagen
            if isinstance(imagen, dict):
                for key in ("url", "original", "grande", "mediana", "pequena", "imagen", "src"):
                    valor = imagen.get(key)
                    if isinstance(valor, str) and valor.startswith("http"):
                        return valor
        return None

    def obtener_imagen_odoo(self, producto):
        url_imagen = self.obtener_url_imagen(producto)
        if not url_imagen:
            return None

        try:
            response = self.session.get(url_imagen, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            return base64.b64encode(response.content).decode("ascii")
        except Exception as e:
            self.log(f"No se pudo descargar imagen desde {url_imagen}: {e}")
            return None

    def construir_data_odoo(self, producto):
        producto = self.obtener_producto_detallado_syscom(producto)
        nombre = self.obtener_nombre_producto(producto)
        modelo = self.obtener_modelo_producto(producto)
        precio_venta = self.obtener_precio_venta(producto)
        sat_key = self.obtener_sat_producto(producto)
        peso = self.obtener_peso_producto(producto)
        volumen = self.obtener_volumen_producto(producto)

        data = {
            "name": nombre,
            "default_code": modelo,
            "list_price": precio_venta,
            "sale_ok": True,
        }

        if "description_sale" in self.product_template_fields:
            descripcion = str(producto.get("descripcion") or "").strip()
            data["description_sale"] = "" if CLEAR_QUOTATION_DESCRIPTION else descripcion

        if "unspsc_code_id" in self.product_template_fields and sat_key:
            unspsc_id = self.buscar_unspsc_odoo(sat_key)
            if unspsc_id:
                data["unspsc_code_id"] = unspsc_id
            else:
                self.log(f"No se encontro codigo UNSPSC en Odoo para SAT {sat_key} del modelo {modelo}")

        if "weight" in self.product_template_fields and peso is not None:
            data["weight"] = peso

        if "volume" in self.product_template_fields and volumen is not None:
            data["volume"] = volumen

        if "is_storable" in self.product_template_fields:
            data["is_storable"] = True
        elif "detailed_type" in self.product_template_fields:
            data["detailed_type"] = "product"
        elif "type" in self.product_template_fields:
            data["type"] = "product"

        if "image_1920" in self.product_template_fields:
            image_b64 = self.obtener_imagen_odoo(producto)
            if image_b64:
                data["image_1920"] = image_b64

        return data, producto

    def obtener_product_id_desde_template(self, template_id):
        variantes = self.models.execute_kw(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            "product.product",
            "search_read",
            [[["product_tmpl_id", "=", template_id]]],
            {"fields": ["id"], "limit": 1},
        )
        if not variantes:
            return None
        return variantes[0]["id"]

    def obtener_ubicacion_interna(self):
        ubicaciones = self.models.execute_kw(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            "stock.location",
            "search_read",
            [[["usage", "=", "internal"]]],
            {"fields": ["id", "name"], "limit": 1},
        )
        if not ubicaciones:
            return None
        return ubicaciones[0]

    def actualizar_stock(self, template_id, stock):
        try:
            product_id = self.obtener_product_id_desde_template(template_id)
            if not product_id:
                self.log(f"No se encontro variante para template {template_id}")
                return

            ubicacion = self.obtener_ubicacion_interna()
            if not ubicacion:
                self.log("No se encontro ubicacion interna de inventario")
                return

            location_id = ubicacion["id"]
            location_name = ubicacion["name"]

            quants = self.models.execute_kw(
                ODOO_DB,
                self.uid,
                ODOO_PASSWORD,
                "stock.quant",
                "search",
                [[["product_id", "=", product_id], ["location_id", "=", location_id]]],
                {"limit": 1},
            )

            if quants:
                quant_id = quants[0]
                self.models.execute_kw(
                    ODOO_DB,
                    self.uid,
                    ODOO_PASSWORD,
                    "stock.quant",
                    "write",
                    [[quant_id], {"inventory_quantity": stock}],
                )
            else:
                quant_id = self.models.execute_kw(
                    ODOO_DB,
                    self.uid,
                    ODOO_PASSWORD,
                    "stock.quant",
                    "create",
                    [{"product_id": product_id, "location_id": location_id, "inventory_quantity": stock}],
                )

            self.models.execute_kw(
                ODOO_DB,
                self.uid,
                ODOO_PASSWORD,
                "stock.quant",
                "action_apply_inventory",
                [[quant_id]],
            )
            self.log(f"Stock ajustado a {stock:.0f} en {location_name}")
        except Exception as e:
            if self.es_fault_none_xmlrpc(e):
                self.log(
                    "Stock ajustado correctamente, pero Odoo devolvio un None por XML-RPC "
                    "despues de aplicar inventario. Se toma como exitoso."
                )
                return
            self.log(f"Error actualizando stock: {e}")

    def construir_preview(self):
        preview = []
        for producto in self.productos_cache.values():
            nombre = self.obtener_nombre_producto(producto)
            modelo = self.obtener_modelo_producto(producto)
            precio_compra = self.obtener_precio_compra(producto.get("precios", {}))
            precio_venta = self.obtener_precio_venta(producto)
            stock = self.obtener_stock_producto(producto)
            tiene_imagen = bool(self.obtener_url_imagen(producto))
            sat_key = self.obtener_sat_producto(producto)
            volumen = self.obtener_volumen_producto(producto)

            if not modelo:
                preview.append(
                    {
                        "accion": "saltado",
                        "motivo": "sin modelo",
                        "modelo": "",
                        "nombre": nombre,
                        "producto": producto,
                    }
                )
                continue

            existentes = self.buscar_producto_odoo(modelo)
            if existentes:
                existente = existentes[0]
                preview.append(
                    {
                        "accion": "coincidencia",
                        "modelo": modelo,
                        "nombre": nombre,
                        "precio_compra_syscom": precio_compra,
                        "precio_venta_syscom": precio_venta,
                        "stock_syscom": stock,
                        "volumen_syscom": volumen,
                        "sat_key": sat_key,
                        "tiene_imagen": tiene_imagen,
                        "odoo_id": existente["id"],
                        "odoo_nombre": existente["name"],
                        "odoo_precio": existente.get("list_price", 0),
                        "odoo_impuestos": self.formatear_impuestos(existente.get("taxes_id", [])),
                        "producto": producto,
                    }
                )
            else:
                preview.append(
                    {
                        "accion": "crear",
                        "modelo": modelo,
                        "nombre": nombre,
                        "precio_compra_syscom": precio_compra,
                        "precio_venta_syscom": precio_venta,
                        "stock_syscom": stock,
                        "volumen_syscom": volumen,
                        "sat_key": sat_key,
                        "tiene_imagen": tiene_imagen,
                        "producto": producto,
                    }
                )
        return preview

    def separar_preview_acciones(self):
        crear = [p for p in self.preview_cache if p["accion"] == "crear"]
        coincidencias = [p for p in self.preview_cache if p["accion"] == "coincidencia"]
        saltados = [p for p in self.preview_cache if p["accion"] == "saltado"]
        return crear, coincidencias, saltados

    def formatear_preview(self):
        crear, coincidencias, saltados = self.separar_preview_acciones()

        lineas = [
            "PREVIEW DE LISTA DE MODELOS SYSCOM",
            "",
            f"Productos encontrados en SYSCOM: {len(self.preview_cache)}",
            f"Nuevos para crear: {len(crear)}",
            f"Coincidencias en Odoo: {len(coincidencias)}",
            f"Saltados: {len(saltados)}",
            f"Modelos no encontrados en SYSCOM: {len(self.modelos_no_encontrados)}",
            f"Moneda mostrada: {DISPLAY_CURRENCY}",
            "",
            "Campos que se enviaran a Odoo en cada alta/actualizacion:",
            "- SYSCOM titulo -> name",
            "- SYSCOM modelo -> default_code",
            "- SYSCOM precio_descuento -> price de compras",
            "- Venta list_price -> precio de compra por tabla de rangos",
            "- SYSCOM sat_key -> unspsc_code_id",
            "- SYSCOM peso -> weight",
            "- SYSCOM volumen -> volume",
            "- SYSCOM imagen -> image_1920",
            "- SYSCOM total_existencia -> stock.quant",
            f"- Compras proveedor -> {SUPPLIER_NAME}",
            f"- Compras cantidad minima -> {SUPPLIER_MIN_QTY:.0f}",
            f"- Compras unidad -> {SUPPLIER_UOM_NAME}",
            "",
        ]

        if self.modelos_no_encontrados:
            lineas.append("MODELOS NO ENCONTRADOS:")
            for modelo in self.modelos_no_encontrados[:80]:
                lineas.append(f"- {modelo}")
            if len(self.modelos_no_encontrados) > 80:
                lineas.append(f"... y {len(self.modelos_no_encontrados) - 80} modelos mas")
            lineas.append("")

        if coincidencias:
            lineas.append("EXISTEN EN ODOO:")
            for item in coincidencias[:50]:
                volumen_txt = f"{item['volumen_syscom']:.6f}" if item["volumen_syscom"] is not None else "N/A"
                lineas.append(
                    f"- {item['modelo']} | ODOO {item['odoo_precio']:.2f} | "
                    f"Compra {item['precio_compra_syscom']:.2f} | Venta {item['precio_venta_syscom']:.2f} | stock {item['stock_syscom']:.0f} | "
                    f"vol {volumen_txt} | sat {item['sat_key'] or 'N/A'}"
                )
            if len(coincidencias) > 50:
                lineas.append(f"... y {len(coincidencias) - 50} coincidencias mas")
            lineas.append("")

        if crear:
            lineas.append("NUEVOS A CREAR:")
            for item in crear[:50]:
                volumen_txt = f"{item['volumen_syscom']:.6f}" if item["volumen_syscom"] is not None else "N/A"
                lineas.append(
                    f"- {item['modelo']} | {item['nombre']} | compra {item['precio_compra_syscom']:.2f} | venta {item['precio_venta_syscom']:.2f} | "
                    f"stock {item['stock_syscom']:.0f} | vol {volumen_txt} | sat {item['sat_key'] or 'N/A'} | "
                    f"imagen {'si' if item['tiene_imagen'] else 'no'}"
                )
            if len(crear) > 50:
                lineas.append(f"... y {len(crear) - 50} productos nuevos mas")

        return "\n".join(lineas)

    def crear_producto_nuevo(self, producto):
        nombre = self.obtener_nombre_producto(producto)
        modelo = self.obtener_modelo_producto(producto)

        if not modelo:
            self.log(f"Saltado '{nombre}': sin modelo")
            return False

        existentes = self.buscar_producto_odoo(modelo)
        if existentes:
            self.log(f"Omitido '{nombre}': ya existe en Odoo con modelo {modelo}")
            return False

        data, producto_detallado = self.construir_data_odoo(producto)
        template_id = self.models.execute_kw(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            "product.template",
            "create",
            [data],
        )
        self.actualizar_proveedor_compra(template_id, producto_detallado)
        self.actualizar_stock(template_id, self.obtener_stock_producto(producto_detallado))
        self.log(f"Creado: {nombre} (ID {template_id})")
        return True

    def sobrescribir_producto(self, producto):
        nombre = self.obtener_nombre_producto(producto)
        modelo = self.obtener_modelo_producto(producto)

        if not modelo:
            self.log(f"Saltado '{nombre}': sin modelo")
            return False

        existentes = self.buscar_producto_odoo(modelo)
        if not existentes:
            self.log(f"Omitido '{nombre}': no existe en Odoo con modelo {modelo}")
            return False

        template_id = existentes[0]["id"]
        data, producto_detallado = self.construir_data_odoo(producto)
        self.models.execute_kw(
            ODOO_DB,
            self.uid,
            ODOO_PASSWORD,
            "product.template",
            "write",
            [[template_id], data],
        )
        self.actualizar_proveedor_compra(template_id, producto_detallado)
        self.actualizar_stock(template_id, self.obtener_stock_producto(producto_detallado))
        self.log(f"Sobrescrito: {nombre} (ID {template_id})")
        return True

    def sincronizar_preview_items(self, crear_nuevos=True, sobrescribir_existentes=True):
        resumen = {
            "creados": 0,
            "sobrescritos": 0,
            "errores": 0,
            "omitidos": 0,
        }

        for item in self.preview_cache:
            try:
                accion = item.get("accion")
                if accion == "crear":
                    if not crear_nuevos:
                        resumen["omitidos"] += 1
                        continue
                    if self.crear_producto_nuevo(item["producto"]):
                        resumen["creados"] += 1
                    else:
                        resumen["omitidos"] += 1
                elif accion == "coincidencia":
                    if not sobrescribir_existentes:
                        resumen["omitidos"] += 1
                        continue
                    if self.sobrescribir_producto(item["producto"]):
                        resumen["sobrescritos"] += 1
                    else:
                        resumen["omitidos"] += 1
                else:
                    resumen["omitidos"] += 1
            except Exception as e:
                self.log(f"Error sincronizando producto: {e}")
                resumen["errores"] += 1

        return resumen

    def run_daily_sync(self, modelos):
        carga = self.cargar_productos(modelos)
        self.preview_cache = self.construir_preview()
        crear, coincidencias, saltados = self.separar_preview_acciones()
        sync = self.sincronizar_preview_items(crear_nuevos=True, sobrescribir_existentes=True)
        return {
            "carga": carga,
            "preview": {
                "nuevos": len(crear),
                "coincidencias": len(coincidencias),
                "saltados": len(saltados),
                "no_encontrados": len(self.modelos_no_encontrados),
            },
            "sync": sync,
        }
