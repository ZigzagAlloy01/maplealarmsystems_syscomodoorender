import base64
import json
import os
import re
import xmlrpc.client
from pathlib import Path

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
CLEAR_TECHNICAL_SPECIFICATION = True
SYSCOM_MONEDA = "mxn"
SYSCOM_IVA_FRONTERA = "false"
SYSCOM_CON_IMPUESTOS = "false"

SUPPLIER_NAME = "Sistemas y Servicios de Comunicacion"
SUPPLIER_UOM_NAME = "Unidades"
SUPPLIER_CURRENCY_NAME = "MXN"
SUPPLIER_MIN_QTY = 1.0

SALE_FACTOR_1 = 1.04
SALE_FACTOR_IVA = 1.14

SPECIAL_MULTIPLIER_MODELS = {
    "SF16AWG500": 2.0,
    "PROCAT6EXTLITEV2": 2.0,
    "PROCAT6EXTLITESV2": 2.0,
    "PFL6X04YLCEG": 2.0,
    "PFL6X04IGCEG": 2.0,
    "9A6O4A501AR1A": 2.0,
    "PROCAT6AR": 2.0,
    "9C6R4A506AR1A": 2.0,
    "DS1LN6OUTPE": 2.0,
    "DS1LN5ESW": 2.0,
    "PUD6C2804WHCE": 2.0,
    "PUD6C2804IGCE": 2.0,
    "NUC6C04BUFE": 2.0,
    "NUC6C04IGFE": 2.0,
    "PUC6C04BUFE": 2.0,
    "PUC6004YLFE": 2.0,
    "PUP6C04BUWN": 2.0,
    "PUC6004RDFE": 2.0,
    "PUR6004RDME": 2.0,
    "PUC6004GRME": 2.0,
    "PROCAT5EXTLITEDJ": 2.0,
    "PUP6C04WHW": 2.0,
    "PUR6004BUFE": 2.0,
    "PUR6004IGW": 2.0,
    "PUC6004ORFE": 2.0,
    "PUC6004GRFE": 2.0,
    "9C6R4E3RXA": 2.0,
    "9C6L4E204RXA": 2.0,
    "NUR5C04BUC": 2.0,
    "PUR6ASD04BUCG": 2.0,
    "PUR6ASD04WHCG": 2.0,
    "PUO6C2204BLCEG": 2.0,
    "PUR6C2204BUCE": 2.0,
    "PUR6C2204IGCE": 2.0,
    "PUP6XHD04WHG": 2.0,
    "PUR6AHD04GRG": 2.0,
    "PUR6AHD04VLG": 2.0,
    "PUL6AHD04BUEG": 2.0,
    "PUL6AHD04IGEG": 2.0,
    "PUP6AS04IGGZ": 2.0,
    "PUR6AV04BUG": 2.0,
    "PUR6AV04IGG": 2.0,
    "PUR6AV04GRG": 2.0,
    "PUL6AV04WHEG": 2.0,
    "PUL6AHD04RDEG": 2.0,
    "PUR6C04BUM": 2.0,
    "PUR6C04BUF": 2.0,
    "PROCAT6PLUSW500V2": 2.0,
    "PROCAT6PLUS500V2": 2.0,
    "DS1LN6UZC0B": 2.0,
    "EPCAT5ER2": 2.0,
    "EPCAT5EV2EXT": 2.0,
    "PROCAT6PLUSV2": 2.0,
    "PROCAT6LITEV2": 2.0,
    "PROCAT5EWV2": 2.0,
    "PROCAT5EXTLITES": 2.0,
    "DS1LN6UEWB": 2.0,
    "UCABLEC6CMP": 2.0,
    "UCABLEC6CMR": 2.0,
    "9A6M4A502": 2.0,
    "ISX6X04ATLLED": 2.0,
    "ISFCH5C04ATLXG": 2.0,
    "NUC5C04IGCE": 2.0,
    "PUR6AV04WHG": 2.0,
    "636121081000": 2.0,
    "636011011000": 2.0,
    "9A6R4A5": 2.0,
    "9C6L4A5": 2.0,
    "PUP6C04BUWZ": 2.0,
    "PUR6004WHFE": 2.0,
    "PUC5C04IGCE": 2.0,
    "PFO6X04BLCEG": 2.0,
    "EPCAT5EV2P": 2.0,
    "PUL6004WHFE": 2.0,
    "9C6L4E206RXA": 2.0,
    "636021061000": 2.0,
    "PUP6AHD04BUG": 2.0,
    "63601108": 2.0,
    "EPCAT5EV2100M": 2.0,
    "PSL7004BUCED": 2.0,
    "9A6L4A5": 2.0,
    "PUC6004ORME": 2.0,
    "EPCAT6V2EXT": 2.0,
    "ISX6X04AYLLED": 2.0,
    "PUL6004BUME": 2.0,
    "PSL7004WHCED": 2.0,
    "9C6L4E2RXA": 2.0,
    "PUL6004WHME": 2.0,
    "PUC5C04BUCE": 2.0,
    "ACCESS184500": 2.0,
    "PSL7004IGCED": 2.0,
    "PROCAT5EV2": 2.0,
    "PFL6X04WHCEG": 2.0,
    "PFL6X04BLCEG": 2.0,
    "PUP6C04WHWZ": 2.0,
    "PUP6C04BUW": 2.0,
    "PUD6C2804BUCE": 2.0,
    "6644641000": 2.0,
    "PUR6AV04YLG": 2.0,
    "PROCAT6PLUSW500": 2.0,
    "PFL6X04BUCEG": 2.0,
    "DS1LN5ES": 2.0,
    "507811061000": 2.0,
    "PROCAT6PLUS500": 2.0,
    "DS1LN6UEW": 2.0,
    "PUC6004WHME": 2.0,
    "633011091000": 2.0,
    "PUP5C04BUF": 2.0,
    "PUP6AHD04WHG": 2.0,
    "PROCAT6A": 2.0,
    "DS1LN6UWCCA": 2.0,
    "9C6M4E206RXA": 2.0,
    "PUP6AS04WHGZ": 2.0,
    "PUC6004WHFE": 2.0,
    "PUC6004IGFE": 2.0,
    "PUP6AS04BUGZ": 2.0,
    "PROCAT5ELITE100M": 2.0,
    "ACCESSRIMCOIL": 2.0,
    "9C6M4E2RXA": 2.0,
    "PROCAT6PLUSW": 2.0,
    "PROCAT6EXT500": 2.0,
    "PUR6AHD04WHG": 2.0,
    "AWG25": 2.0,
    "AWG100": 2.0,
    "9T7L4E10": 2.0,
    "PROCAT6R": 2.0,
    "PFL6004BUG": 2.0,
    "NUR6C04BUM": 2.0,
    "DS1LN5ESB": 2.0,
    "9C6M4E3RXA": 2.0,
    "PROCAT5EXT": 2.0,
    "210311011000": 2.0,
    "DS1LN5EOUUE": 2.0,
    "PROCAT5E": 2.0,
    "PROCAT5EW": 2.0,
    "431111041000": 2.0,
    "430611041000": 2.0,
    "SF14AWG500": 2.0,
    "PROCAT6EXTLITE": 2.0,
    "PROCAT6EXTLITES": 2.0,
    "PROCAT62C": 2.0,
    "NUC6C04BUME": 2.0,
    "NUC6C04IGME": 2.0,
    "PUR6004BUME": 2.0,
    "PUC6004IGME": 2.0,
    "PROCAT6EXTLITEDJ": 2.0,
    "PROCAT5EXTLITEW": 2.0,
    "PROCAT6EXTLITEW": 2.0,
    "PROCAT6W": 2.0,
    "NUR6C04IGC": 2.0,
    "PUO6C04BLCEG": 2.0,
    "PUR6AHD04BUG": 2.0,
    "PUR6AHD04IGG": 2.0,
    "PROCAT5EXT500": 2.0,
    "PROCAT6": 2.0,
    "PROCAT6B": 2.0,
    "PROCAT6S": 2.0,
    "PROCAT6EXT": 2.0,
    "PROCAT6PLUS": 2.0,
    "PROCAT6LITE": 2.0,
    "636011021000": 2.0,
    "PROCAT5EGELX": 2.0,
    "PROCAT5ELITE": 2.0,
    "PSCCAT5EXT": 2.0,
    "PSCCAT5E": 2.0,
    "AWG50": 2.0,
    "KIT4MP4B1TB": 2.0,
    "EPCAT5EV2W": 2.0,
    "PUR6004IGFE": 2.0,
    "NUR6C04BUC": 2.0,
    "NUC5C04BUCE": 2.0,
    "PSCCAT5EXTGEL": 2.0,
    "ISFCH6X04ATLUG": 2.0,
    "PUC6004YLME": 2.0,
    "NUC5C04BUME": 2.0,
    "9C6L4E3RXA": 2.0,
    "PUL6AHD04WHEG": 2.0,
    "PROCAT6AIR": 2.0,
    "PFR6X04BUCG": 2.0,
    "9A6M4A5": 2.0,
    "PUO6C2204BLGZ": 2.0,
    "PUO6X04BLCEG": 2.0,
    "PUR6AHD04YLG": 2.0,
    "9C6M4E306RXA": 2.0,
    "WD23PURZ": 1.3,
    "WD33PURZ": 1.3,
    "WD44PURZ": 1.3,
    "WD64PURZ": 1.3,
    "WD11PURZ": 1.3,
    "WD102PURP": 1.3,
    "WD8002PURP": 1.3,
    "WD181PURP": 1.3,
    "V300X1TB": 1.3,
}

TECHNICAL_SPECIFICATION_FIELD_CANDIDATES = (
    "description",
    "x_studio_technical_specification",
    "technical_specification",
    "x_studio_ficha_tecnica_url",
    "ficha_tecnica_url",
)
CATEGORY_OBJECT_KEYS = {"categoria", "category", "subcategoria", "subcategory", "linea", "line"}
CATEGORY_NAME_KEYS = {"nombre", "name", "titulo", "title", "label", "descripcion"}
CATEGORY_ID_KEYS = {"id", "categoria_id", "category_id", "id_categoria", "subcategoria_id", "id_subcategoria"}

def _normalize_model_key(texto):
    return re.sub(r"[^A-Z0-9]", "", str(texto or "").upper())

def _load_default_models():
    path = Path(__file__).with_name("models_syscom.txt")
    if not path.exists():
        return ""
    return path.read_text(encoding="utf-8")

def _load_descriptions_map():
    path = Path(os.getenv("SYSCOM_DESCRIPTIONS_FILE", Path(__file__).with_name("descriptions_syscom.json")))
    if not path.exists():
        return {}

    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}

    normalizado = {}
    for modelo, payload in raw.items():
        if not isinstance(payload, dict):
            continue
        normalizado[_normalize_model_key(modelo)] = {
            "website_description": str(payload.get("website_description") or payload.get("ecommerce_description") or "").strip(),
            "description_sale": str(payload.get("description_sale") or payload.get("quotation_description") or "").strip(),
        }
    return normalizado

def _load_technical_specifications_map():
    path = Path(
        os.getenv(
            "SYSCOM_TECHNICAL_SPECS_FILE",
            Path(__file__).with_name("technical_specifications_syscom.json"),
        )
    )
    if not path.exists():
        return {}

    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        return {}

    normalizado = {}
    for modelo, payload in raw.items():
        if not isinstance(payload, dict):
            continue
        normalizado[_normalize_model_key(modelo)] = str(payload.get("technical_specification") or "").strip()
    return normalizado

DEFAULT_MODELS = _load_default_models()
DESCRIPTIONS_MAP = _load_descriptions_map()
TECHNICAL_SPECIFICATIONS_MAP = _load_technical_specifications_map()

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
        self.product_category_fields = self.obtener_campos_modelo("product.category")
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
        self.product_category_cache = {}
        self.syscom_category_cache = {}
        self.descriptions_map = DESCRIPTIONS_MAP
        self.technical_specifications_map = TECHNICAL_SPECIFICATIONS_MAP
        self.technical_specification_field = self.resolver_campo_technical_specification()

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

    def _normalizar_categoria_id(self, valor):
        if valor is None:
            return None

        texto = str(valor).strip()
        if not texto:
            return None
        if texto.isdigit():
            return texto
        return None

    def _extraer_categoria_desde_valor(self, valor):
        if isinstance(valor, list):
            categorias = []
            for index, item in enumerate(valor):
                if isinstance(item, dict):
                    nombre = None
                    categoria_id = None
                    nivel = None

                    for key, nested_value in item.items():
                        key_norm = str(key).strip().lower()
                        if key_norm in CATEGORY_NAME_KEYS and isinstance(nested_value, str) and nested_value.strip():
                            nombre = nested_value.strip()
                        elif key_norm in CATEGORY_ID_KEYS:
                            categoria_id = self._normalizar_categoria_id(nested_value)
                        elif key_norm == "nivel":
                            nivel = self.normalizar_numero(nested_value)

                    if nombre or categoria_id:
                        categorias.append(
                            {
                                "name": nombre,
                                "id": categoria_id,
                                "nivel": nivel if nivel is not None else -1,
                                "index": index,
                            }
                        )
                elif isinstance(item, str) and item.strip():
                    categorias.append(
                        {
                            "name": item.strip(),
                            "id": None,
                            "nivel": -1,
                            "index": index,
                        }
                    )

            if categorias:
                categorias.sort(key=lambda cat: (cat["nivel"], cat["index"]))
                return {
                    "name": categorias[-1]["name"],
                    "id": categorias[-1]["id"],
                    "path": [cat["name"] for cat in categorias if cat["name"]],
                }

            return {"name": None, "id": None, "path": []}

        if isinstance(valor, dict):
            nombre = None
            categoria_id = None

            for key, item in valor.items():
                key_norm = str(key).strip().lower()
                if key_norm in CATEGORY_NAME_KEYS and isinstance(item, str) and item.strip():
                    nombre = item.strip()
                elif key_norm in CATEGORY_ID_KEYS:
                    categoria_id = self._normalizar_categoria_id(item)

            return {"name": nombre, "id": categoria_id, "path": [nombre] if nombre else []}

        if isinstance(valor, str):
            texto = valor.strip()
            if not texto:
                return {"name": None, "id": None, "path": []}
            if texto.isdigit():
                return {"name": None, "id": texto, "path": []}
            return {"name": texto, "id": None, "path": [texto]}

        categoria_id = self._normalizar_categoria_id(valor)
        return {"name": None, "id": categoria_id, "path": []}

    def _buscar_categoria_en_producto(self, nodo):
        if isinstance(nodo, dict):
            for key, value in nodo.items():
                key_norm = str(key).strip().lower()
                if key_norm in CATEGORY_OBJECT_KEYS or "categor" in key_norm:
                    categoria = self._extraer_categoria_desde_valor(value)
                    if categoria["name"] or categoria["id"] or categoria["path"]:
                        return categoria

                if isinstance(value, (dict, list)):
                    categoria = self._buscar_categoria_en_producto(value)
                    if categoria["name"] or categoria["id"] or categoria["path"]:
                        return categoria

        if isinstance(nodo, list):
            for item in nodo:
                categoria = self._buscar_categoria_en_producto(item)
                if categoria["name"] or categoria["id"] or categoria["path"]:
                    return categoria

        return {"name": None, "id": None, "path": []}

    def obtener_categoria_syscom_por_id(self, categoria_id):
        categoria_id = self._normalizar_categoria_id(categoria_id)
        if not categoria_id:
            return None

        if categoria_id in self.syscom_category_cache:
            return self.syscom_category_cache[categoria_id]

        try:
            response = self.session.get(
                f"{BASE_URL}categorias/{categoria_id}",
                timeout=REQUEST_TIMEOUT,
            )
            response.raise_for_status()
            payload = response.json()
            if isinstance(payload, dict):
                nombre = str(
                    payload.get("nombre")
                    or payload.get("name")
                    or payload.get("titulo")
                    or ""
                ).strip()
                self.syscom_category_cache[categoria_id] = nombre or None
                return self.syscom_category_cache[categoria_id]
        except Exception as e:
            self.log(f"No se pudo obtener categoria SYSCOM {categoria_id}: {e}")

        self.syscom_category_cache[categoria_id] = None
        return None

    def obtener_titulo_categoria_producto(self, producto):
        categoria = self._buscar_categoria_en_producto(producto)
        if categoria["name"]:
            return categoria["name"]
        if categoria["id"]:
            return self.obtener_categoria_syscom_por_id(categoria["id"])
        return None

    def obtener_ruta_categoria_producto(self, producto):
        categoria = self._buscar_categoria_en_producto(producto)
        ruta = [parte for parte in categoria.get("path", []) if parte]
        if ruta:
            return ruta

        if categoria["name"]:
            return [categoria["name"]]

        if categoria["id"]:
            nombre = self.obtener_categoria_syscom_por_id(categoria["id"])
            if nombre:
                return [nombre]

        return []

    def buscar_categoria_odoo_id(self, nombre_categoria, parent_id=None):
        nombre_categoria = str(nombre_categoria or "").strip()
        if not nombre_categoria:
            return None

        cache_key = f"{parent_id or 0}:{nombre_categoria.lower()}"
        if cache_key in self.product_category_cache:
            return self.product_category_cache[cache_key]

        fields = ["id"]
        if "name" in self.product_category_fields:
            fields.append("name")
        if "complete_name" in self.product_category_fields:
            fields.append("complete_name")

        dominios = []
        if "name" in self.product_category_fields:
            domain = [["name", "=", nombre_categoria]]
            if "parent_id" in self.product_category_fields:
                if parent_id:
                    domain.append(["parent_id", "=", parent_id])
                else:
                    domain.append(["parent_id", "=", False])
            dominios.append(domain)

        for domain in dominios:
            try:
                encontrados = self.models.execute_kw(
                    ODOO_DB,
                    self.uid,
                    ODOO_PASSWORD,
                    "product.category",
                    "search_read",
                    [domain],
                    {"fields": fields, "limit": 1},
                )
                if encontrados:
                    categoria_id = encontrados[0]["id"]
                    self.product_category_cache[cache_key] = categoria_id
                    return categoria_id
            except Exception as e:
                self.log(f"No se pudo buscar categoria '{nombre_categoria}' en Odoo: {e}")

        self.product_category_cache[cache_key] = None
        return None

    def obtener_o_crear_categoria_odoo_desde_ruta(self, ruta_categoria):
        ruta = [str(parte).strip() for parte in (ruta_categoria or []) if str(parte).strip()]
        if not ruta:
            return None

        if "name" not in self.product_category_fields:
            self.log("El modelo product.category no expone el campo name en esta base")
            return None

        parent_id = None
        for nombre_categoria in ruta:
            categoria_id = self.buscar_categoria_odoo_id(nombre_categoria, parent_id=parent_id)
            if not categoria_id:
                vals = {"name": nombre_categoria}
                if "parent_id" in self.product_category_fields and parent_id:
                    vals["parent_id"] = parent_id
                try:
                    categoria_id = self.models.execute_kw(
                        ODOO_DB,
                        self.uid,
                        ODOO_PASSWORD,
                        "product.category",
                        "create",
                        [vals],
                    )
                    cache_key = f"{parent_id or 0}:{nombre_categoria.lower()}"
                    self.product_category_cache[cache_key] = categoria_id
                except Exception as e:
                    self.log(
                        f"No se pudo crear categoria '{nombre_categoria}' en Odoo "
                        f"(ruta: {' / '.join(ruta)}): {e}"
                    )
                    return None
            parent_id = categoria_id

        return parent_id
    
    def obtener_descripciones_personalizadas(self, producto):
        modelo = self.obtener_modelo_producto(producto)
        if not modelo:
            return {}
        return self.descriptions_map.get(self.normalizar_modelo_clave(modelo), {})

    def resolver_campo_technical_specification(self):
        for field_name in TECHNICAL_SPECIFICATION_FIELD_CANDIDATES:
            if field_name in self.product_template_fields:
                return field_name
        return None

    def obtener_technical_specification(self, producto):
        modelo = self.obtener_modelo_producto(producto)
        if not modelo:
            return ""
        return self.technical_specifications_map.get(self.normalizar_modelo_clave(modelo), "")

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
    
    def obtener_descripcion_ecommerce(self, producto):
        custom = self.obtener_descripciones_personalizadas(producto).get("website_description", "")
        if custom:
            return custom
        return ""

    def obtener_descripcion_cotizacion(self, producto):
        custom = self.obtener_descripciones_personalizadas(producto).get("description_sale", "")
        if custom:
            return custom
        return ""

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
    
    def obtener_multiplicador_especial_modelo(self, modelo):
        return SPECIAL_MULTIPLIER_MODELS.get(self.normalizar_modelo_clave(modelo))

    def obtener_multiplicador_venta(self, precio_compra, modelo=None):
        multiplicador_especial = self.obtener_multiplicador_especial_modelo(modelo)
        if multiplicador_especial is not None:
            return multiplicador_especial
        if precio_compra <= 0:
            return 0.0
        if precio_compra < 50:
            return 3.0
        if precio_compra < 100:
            return 2.0
        if precio_compra < 1000:
            return 1.8
        if precio_compra < 1500:
            return 1.7
        if precio_compra < 2000:
            return 1.6
        if precio_compra < 3000:
            return 1.5
        if precio_compra < 10000:
            return 1.4
        if precio_compra < 20000:
            return 1.3
        return 1.2

    def obtener_precio_venta(self, producto):
        precios = producto.get("precios", {}) if isinstance(producto, dict) else (producto or {})
        modelo = producto.get("modelo") if isinstance(producto, dict) else None
        precio_compra = self.obtener_precio_compra(precios)
        if precio_compra <= 0:
            return 0.0

        multiplicador = self.obtener_multiplicador_venta(precio_compra, modelo=modelo)
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

        descripcion_ecommerce = self.obtener_descripcion_ecommerce(producto)
        descripcion_cotizacion = self.obtener_descripcion_cotizacion(producto)
        technical_specification = self.obtener_technical_specification(producto)

        if "website_description" in self.product_template_fields and descripcion_ecommerce:
            data["website_description"] = descripcion_ecommerce
        if "description_sale" in self.product_template_fields:
            if descripcion_cotizacion:
                data["description_sale"] = descripcion_cotizacion
            elif CLEAR_QUOTATION_DESCRIPTION:
                data["description_sale"] = ""
            else:
                data["description_sale"] = str(producto.get("descripcion") or "").strip()
        if self.technical_specification_field:
            if technical_specification:
                data[self.technical_specification_field] = technical_specification
            elif CLEAR_TECHNICAL_SPECIFICATION:
                data[self.technical_specification_field] = ""

        if "categ_id" in self.product_template_fields:
            ruta_categoria = self.obtener_ruta_categoria_producto(producto)
            if ruta_categoria:
                categoria_id = self.obtener_o_crear_categoria_odoo_desde_ruta(ruta_categoria)
                if categoria_id:
                    data["categ_id"] = categoria_id
                else:
                    self.log(
                        f"No se pudo resolver la categoria de Odoo '{' / '.join(ruta_categoria)}' "
                        f"para modelo {modelo}"
                    )
            else:
                self.log(f"No se encontro categoria SYSCOM para modelo {modelo}")

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
                    elif self.crear_producto_nuevo(item["producto"]):
                        resumen["creados"] += 1
                    else:
                        resumen["omitidos"] += 1
                elif accion == "coincidencia":
                    if not sobrescribir_existentes:
                        resumen["omitidos"] += 1
                    elif self.sobrescribir_producto(item["producto"]):
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
