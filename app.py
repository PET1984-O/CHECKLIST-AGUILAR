from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from io import StringIO
from typing import Dict, Iterable, List
import csv
import hashlib
import json
import re

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Checklist Aguilar 2025",
    layout="wide",
    page_icon="📋",
    initial_sidebar_state="expanded",
)


@dataclass(frozen=True)
class Section:
    name: str
    items: List[str]
    optional: bool = False
    help_text: str = ""


CHECKLISTS: Dict[str, List[Section]] = {
    "Infonavit Tradicional y Total": [
        Section(
            "Documentos",
            [
                "Propuesta de venta firmada por asesor y gerente de ventas",
                "Contrato firmado",
                "Acta de nacimiento actualizada (Internet u original) con copia",
                "Precalificación de Mi Cuenta Infonavit con datos del DH",
                "2 copias de RFC legible con homoclave actualizada (Constancia SAT)",
                "2 copias legibles de identificación al 200% en la misma hoja (INE o pasaporte). Para Info Total la copia es tamaño normal",
                "Consulta de vigencia de identificación oficial (INE)",
                "2 copias de CURP legible actualizada (Internet)",
                "2 copias de comprobante de domicilio actualizado",
                'Original y 1 copia de constancia del curso en línea "Saber para decidir"',
                "Reporte informativo de relaciones laborales para validar NRP",
            ],
        ),
        Section(
            "Formatos y solicitudes",
            [
                "2 solicitudes de crédito. Solo una requisitada, pero las dos firmadas",
                'Carta de aceptación cliente: conocimiento de la vivienda y curso "Saber para decidir"',
                "Formato de datos generales de cliente (Neodata)",
                "Copia de la ficha de pago o recibo de pago de caja del apartado",
                "Anexo C descargado del portal del Infonavit",
                "Solicitud de avalúo. Solo aplica para Info Total: una requisitada con datos del DH y las dos firmadas",
            ],
        ),
        Section(
            "Anexos",
            [
                "Anexo A",
                "Aviso de privacidad",
                "Hoja de cuota de conservación o mantenimiento",
                "Recibo de entrega de reglamento",
                "Sembrado régimen",
            ],
        ),
        Section(
            "Crédito conyugal, corresidencial o familiar",
            [
                "Acta de nacimiento actualizada del cónyuge, familiar o corresidente (Internet u original) con copia",
                "Precalificación de Mi Cuenta Infonavit con datos del DH",
                "2 copias de RFC legible con homoclave actualizada (Constancia SAT)",
                "2 copias legibles de identificación al 200% en la misma hoja (INE o pasaporte)",
                "Consulta de vigencia de identificación oficial (INE)",
                "2 copias de CURP legible actualizada (Internet)",
                "Acta de matrimonio actualizada (Internet u original) con copia. Solo crédito conyugal",
                'Original y 1 copia de constancia del curso en línea "Saber para decidir"',
                "Reporte informativo de relaciones laborales para validar NRP",
            ],
            optional=True,
            help_text="Aplica si el crédito es conyugal, corresidencial o familiar.",
        ),
        Section(
            "Cliente casado sin ejercer crédito con cónyuge",
            [
                "Acta de matrimonio actualizada (Internet u original) con copia, si están bajo separación de bienes",
                "Acta de nacimiento del cónyuge actualizada con copia, si están bajo sociedad conyugal legal",
                "2 copias legibles de identificación del cónyuge al 200% en la misma hoja, si están bajo sociedad conyugal legal",
                "2 copias de RFC del cónyuge con homoclave actualizada (SAT), si están bajo sociedad conyugal legal",
                "2 copias de CURP del cónyuge actualizada, si están bajo sociedad conyugal legal",
                "Consulta de vigencia de identificación oficial (INE) del cónyuge, si están bajo sociedad conyugal legal",
            ],
            optional=True,
            help_text="Aplica cuando solo el DH ejercerá su crédito, pero está casado.",
        ),
    ],
    "Infonavit Línea III": [
        Section(
            "Documentos",
            [
                "Propuesta de venta firmada por asesor y gerente de ventas",
                "Contrato firmado",
                "Acta de nacimiento actualizada (Internet u original) con copia",
                "Precalificación de Mi Cuenta Infonavit con datos del DH",
                "2 copias de RFC legible con homoclave actualizada (Constancia SAT)",
                "2 copias legibles de identificación al 200% en la misma hoja (INE o pasaporte)",
                "Consulta de vigencia de identificación oficial (INE)",
                "2 copias de CURP legible actualizada (Internet)",
                "2 copias de comprobante de domicilio actualizado",
                'Original y 1 copia de constancia del curso en línea "Saber para decidir"',
                "Reporte informativo de relaciones laborales para validar NRP",
            ],
        ),
        Section(
            "Formatos y solicitudes",
            [
                "2 solicitudes de crédito. Solo una requisitada, pero las dos firmadas",
                "2 solicitudes de avalúo Infonavit. Una requisitada con datos del DH y las dos firmadas",
                "Carta de aceptación cliente: conocimiento del proyecto Línea III y condiciones del crédito",
                "Cuestionario básico sobre la comprensión del crédito en paquete integral",
                "Formato de datos generales de cliente (Neodata)",
                "Copia de la ficha de pago o recibo de pago de caja del apartado",
                'Carta de aceptación del cliente que hizo el taller "Saber más para decidir mejor"',
                "Anexo C descargado del portal del Infonavit",
            ],
        ),
        Section(
            "Anexos",
            [
                "Anexo A",
                "Aviso de privacidad",
                "Recibo de entrega de reglamento",
                "Sembrado régimen",
                "Hoja de cuota de conservación o mantenimiento",
            ],
        ),
        Section(
            "Crédito conyugal",
            [
                "Acta de nacimiento actualizada del cónyuge (Internet u original) con copia",
                "Precalificación de Mi Cuenta Infonavit con datos del DH",
                "2 copias de RFC legible con homoclave actualizada (Constancia SAT)",
                "2 copias legibles de identificación al 200% en la misma hoja (INE o pasaporte)",
                "Consulta de vigencia de identificación oficial (INE)",
                "2 copias de CURP legible actualizada (Internet)",
                "Acta de matrimonio actualizada (Internet u original) con copia",
                'Original y 1 copia de constancia del curso en línea "Saber para decidir"',
                "Reporte informativo de relaciones laborales para validar NRP",
            ],
            optional=True,
            help_text="Aplica si el crédito Línea III es conyugal.",
        ),
        Section(
            "Cliente casado sin ejercer crédito con cónyuge",
            [
                "Acta de matrimonio actualizada (Internet u original) con copia, si están bajo separación de bienes",
                "Acta de nacimiento del cónyuge actualizada con copia, si están bajo sociedad conyugal legal",
                "2 copias legibles de identificación del cónyuge al 200% en la misma hoja, si están bajo sociedad conyugal legal",
                "2 copias de RFC del cónyuge con homoclave actualizada (SAT), si están bajo sociedad conyugal legal",
                "2 copias de CURP del cónyuge actualizada, si están bajo sociedad conyugal legal",
                "Consulta de vigencia de identificación oficial (INE) del cónyuge, si están bajo sociedad conyugal legal",
            ],
            optional=True,
            help_text="Aplica cuando solo el DH ejercerá su crédito, pero está casado.",
        ),
    ],
    "Cofinavit": [
        Section(
            "Documentos",
            [
                "Propuesta de venta firmada por asesor y gerente de ventas",
                "Contrato firmado",
                "Acta de nacimiento actualizada formato Internet u original y 2 copias legibles",
                "Precalificación de Mi Cuenta Infonavit con datos del DH",
                "2 copias de RFC legible con homoclave actualizada (Constancia SAT)",
                "2 copias legibles de identificación oficial (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE)",
                "2 copias de CURP legible actualizada",
                "2 copias de comprobante de domicilio actualizado",
                'Original y una copia de constancia del curso en línea "Saber para decidir"',
                "Reporte informativo de relaciones laborales para validar NRP",
            ],
        ),
        Section(
            "Formatos y solicitudes",
            [
                "2 solicitudes de crédito. Solo una requisitada, pero las 2 firmadas",
                "Autorización original del banco",
                "Solicitud de avalúo Infonavit requisitada con datos del DH y firmada",
                'Carta de instrucción irrevocable (Cofinavit) firmada en el inciso "B"',
                "Carta de aceptación: conocimiento de la vivienda y el taller",
                "Original o copia de solicitud de crédito del banco firmada",
                "2 copias de comprobante de ingresos o estado de cuenta bancario",
                "Copia de la ficha de pago o recibo de pago de caja del apartado",
                "Formato de datos generales (Neodata)",
            ],
        ),
        Section(
            "Anexos",
            [
                "Anexo A",
                "Aviso de privacidad",
                "Hoja de cuota de conservación o mantenimiento",
                "Sembrado régimen",
                "Recibo de entrega de reglamento",
            ],
        ),
        Section(
            "Casado por sociedad conyugal legal",
            [
                "Acta de matrimonio actualizada formato Internet u original y 2 copias legibles",
                "Acta de nacimiento actualizada del cónyuge formato Internet u original y 2 copias legibles",
                "2 copias legibles de identificación oficial del cónyuge (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE) del cónyuge",
                "2 copias de RFC del cónyuge legible con homoclave actualizada (Constancia SAT)",
                "2 copias de CURP del cónyuge legible actualizada",
            ],
            optional=True,
            help_text="Si es separación de bienes, normalmente solo se solicita acta de matrimonio.",
        ),
    ],
    "Bancario": [
        Section(
            "Documentos",
            [
                "Propuesta de compra venta firmada por asesor y gerente de ventas",
                "Contrato firmado",
                "Simulador de crédito del banco",
                "2 copias de acta de nacimiento formato Internet u original",
                "2 copias de estado de cuenta bancario o comprobante de ingresos",
                "2 copias legibles de identificación oficial (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE)",
                "2 copias de CURP legible actualizada",
                "2 copias de comprobante de domicilio actualizado",
                "2 copias de RFC legible con homoclave (Constancia SAT)",
            ],
        ),
        Section(
            "Formato y solicitudes",
            [
                "Original o copia de solicitud de crédito requisitada y firmada (banco)",
                "Original de autorización de crédito por la institución bancaria",
                "Formato de información completa en Neodata",
                "Copia de la ficha de pago o recibo de pago de caja del apartado",
            ],
        ),
        Section(
            "Anexos",
            [
                "Anexo A",
                "Aviso de privacidad",
                "Hoja de cuota de conservación o mantenimiento",
                "Sembrado régimen",
                "Recibo de entrega de reglamento",
            ],
        ),
        Section(
            "Casado por sociedad conyugal legal",
            [
                "2 copias de acta de matrimonio formato Internet u original",
                "2 copias de acta de nacimiento del cónyuge formato Internet u original",
                "2 copias de identificación oficial del cónyuge (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE) del cónyuge",
                "2 copias de CURP del cónyuge",
                "2 copias de RFC del cónyuge con homoclave (Constancia SAT)",
                "Solicitud firmada por el cónyuge y datos generales si el crédito es con coacreditado",
            ],
            optional=True,
            help_text="Si es separación de bienes, normalmente solo se solicita acta de matrimonio.",
        ),
    ],
    "Fovissste": [
        Section(
            "Documentos",
            [
                "Propuesta de compra venta firmada por asesor y gerente de ventas",
                "Contrato firmado",
                "Simulador de crédito Fovissste",
                "3 copias de acta de nacimiento actualizada (Internet u original)",
                "3 copias de talones de pago de la última quincena",
                "3 copias legibles de identificación oficial (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE)",
                "3 copias de CURP legible actualizada",
                "3 copias de comprobante de domicilio actualizado",
                "3 copias del curso Tu Asesor Patrimonial",
                "3 copias de RFC legible con homoclave actualizada (Constancia SAT)",
            ],
        ),
        Section(
            "Formato y solicitudes",
            [
                "3 formatos originales de hoja de datos generales. Solo uno requisitado, pero los tres firmados",
                "3 solicitudes de crédito enviadas al acreditado cuando se inscribe",
                "3 formatos originales de carta elección mandataria. Solo uno requisitado, pero los tres firmados",
                "3 formatos originales de originación del crédito. Solo uno requisitado, pero los dos firmados",
                "3 formatos originales de aclaraciones. Solo uno requisitado, pero los tres firmados",
                "3 formatos de aviso de privacidad. Solo uno requisitado, pero los tres firmados",
                "3 formatos de autorización de buró. Solo una requisitada, pero los dos firmados",
                "3 formatos originales de cambio de modalidad. Solo una requisitada, pero los dos firmados",
                "3 formatos originales check list. Solo una requisitada, pero los dos firmados",
                "3 copias del expediente electrónico único",
                "3 copias del estado de cuenta SAR",
                "Formato de información completa en Neodata",
                "Copia de la ficha de pago o recibo de pago de caja del apartado",
            ],
        ),
        Section(
            "Anexos",
            [
                "Anexo A",
                "Aviso de privacidad",
                "Hoja de cuota de conservación o mantenimiento",
                "Sembrado régimen",
                "Recibo de entrega de reglamento",
            ],
        ),
        Section(
            "Casado o mancomunado",
            [
                "3 copias de acta de matrimonio actualizada formato Internet u original",
                "3 copias de acta de nacimiento del cónyuge actualizada formato Internet u original",
                "3 copias de identificación oficial del cónyuge (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE) del cónyuge",
                "3 copias de CURP del cónyuge actualizada",
                "3 copias de RFC del cónyuge con homoclave actualizada (Constancia SAT)",
                "Todos los formatos firmados por el cónyuge y sus datos generales si el crédito es mancomunado",
            ],
            optional=True,
            help_text="Aplica en casados y créditos mancomunados.",
        ),
    ],
    "Fovissste para Todos": [
        Section(
            "Documentos",
            [
                "Propuesta de compra venta firmada por asesor y gerente de ventas",
                "Contrato firmado",
                "Simulador de crédito Fovissste",
                "3 copias de acta de nacimiento (Internet u original)",
                "3 copias de talones de pago de la última quincena",
                "3 copias legibles de identificación oficial (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE)",
                "3 copias de CURP legible actualizada",
                "3 copias de comprobante de domicilio actualizado",
                "3 copias del curso Tu Asesor Patrimonial",
                "3 copias de RFC legible con homoclave actualizada (Constancia SAT)",
            ],
        ),
        Section(
            "Formato y solicitudes",
            [
                "Original o copia de solicitud de crédito requisitada y firmada (banco)",
                "Original de autorización de crédito por la institución bancaria",
                "3 formatos de autorización de buró. Solo una requisitada y todas firmadas",
                "3 copias del expediente electrónico único",
                "3 copias del estado de cuenta SAR",
                "Formato de información completa en Neodata",
                "Copia de la ficha de pago o recibo de pago de caja del apartado",
            ],
        ),
        Section(
            "Anexos",
            [
                "Anexo A",
                "Aviso de privacidad",
                "Hoja de cuota de conservación o mantenimiento",
                "Sembrado régimen",
                "Recibo de entrega de reglamento",
            ],
        ),
        Section(
            "Casado",
            [
                "3 copias de acta de matrimonio actualizada formato Internet u original",
                "3 copias de acta de nacimiento del cónyuge actualizada formato Internet u original",
                "3 copias de identificación oficial del cónyuge (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE) del cónyuge",
                "3 copias de CURP del cónyuge actualizada",
                "3 copias de RFC del cónyuge con homoclave actualizada (Constancia SAT)",
            ],
            optional=True,
            help_text="Aplica si el cliente está casado.",
        ),
    ],
    "Pensiona2": [
        Section(
            "Documentos",
            [
                "Propuesta de compra venta firmada por asesor y gerente de ventas",
                "Contrato firmado",
                "Simulador de crédito pensionados",
                "3 copias de acta de nacimiento actualizada formato Internet u original",
                "3 copias de talones de pago de la última quincena",
                "3 copias legibles de identificación oficial (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE)",
                "3 copias de CURP legible actualizada",
                "3 copias de comprobante de domicilio actualizado",
                "3 copias del curso Tu Asesor Patrimonial",
                "3 copias de RFC legible con homoclave actualizada (Constancia SAT)",
                "3 copias de la concesión de pensión",
                "3 copias de la credencial de pensionado",
            ],
        ),
        Section(
            "Formato y solicitudes",
            [
                "3 formatos originales de hoja de datos generales. Solo uno requisitado, pero los tres firmados",
                "3 solicitudes de crédito pensionados",
                "3 formatos originales de carta elección mandataria. Solo uno requisitado, pero los tres firmados",
                "3 formatos originales de originación del crédito. Solo uno requisitado, pero los dos firmados",
                "3 formatos originales de aclaraciones. Solo uno requisitado, pero los tres firmados",
                "3 formatos de aviso de privacidad. Solo uno requisitado, pero los tres firmados",
                "3 formatos de autorización de buró. Solo una requisitada, pero los dos firmados",
                "3 formatos originales de cambio de modalidad. Solo una requisitada, pero los dos firmados",
                "3 formatos originales check list. Solo una requisitada, pero los dos firmados",
                "3 copias de la autorización del crédito",
                "Formato de información completa en Neodata",
            ],
        ),
        Section(
            "Anexos",
            [
                "Anexo A",
                "Aviso de privacidad",
                "Hoja de cuota de conservación o mantenimiento",
                "Sembrado régimen",
                "Recibo de entrega de reglamento",
            ],
        ),
        Section(
            "Casado",
            [
                "3 copias de acta de matrimonio actualizada formato Internet u original",
                "3 copias de acta de nacimiento del cónyuge actualizada formato Internet u original",
                "3 copias de identificación oficial del cónyuge (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE) del cónyuge",
                "3 copias de CURP del cónyuge actualizada",
                "3 copias de RFC del cónyuge con homoclave actualizada (Constancia SAT)",
            ],
            optional=True,
            help_text="Aplica si el cliente está casado.",
        ),
    ],
    "Contado": [
        Section(
            "Documentos",
            [
                "Propuesta de compra venta firmada por asesor y gerente de ventas",
                "Contrato firmado",
                "3 copias de acta de nacimiento actualizada formato Internet u original",
                "3 copias legibles de identificación oficial (INE, pasaporte o cédula profesional)",
                "Consulta de vigencia de identificación oficial (INE)",
                "3 copias de CURP legible actualizada",
                "3 copias de comprobante de domicilio actualizado",
                "3 copias de RFC legible con homoclave actualizada (Constancia SAT)",
            ],
        ),
        Section(
            "Anexos y pagos",
            [
                "Anexo A",
                "Aviso de privacidad",
                "Hoja de cuota de conservación o mantenimiento",
                "Sembrado régimen",
                "Recibo de entrega de reglamento",
                "Comprobantes de pago: transferencias bancarias o depósitos a nombre del cliente",
                "Formato de información completa en Neodata",
            ],
        ),
        Section(
            "Casado",
            [
                "3 copias de acta de matrimonio actualizada formato Internet u original",
                "3 copias de acta de nacimiento del cónyuge actualizada formato Internet u original, si están bajo sociedad conyugal legal",
                "3 copias de identificación oficial del cónyuge, si están bajo sociedad conyugal legal",
                "Consulta de vigencia de identificación oficial (INE) del cónyuge, si están bajo sociedad conyugal legal",
                "3 copias de CURP del cónyuge actualizada, si están bajo sociedad conyugal legal",
                "3 copias de RFC del cónyuge con homoclave actualizada (Constancia SAT), si están bajo sociedad conyugal legal",
            ],
            optional=True,
            help_text="Aplica si el cliente está casado.",
        ),
    ],
}

SOURCE_NOTES = {
    "Infonavit Tradicional y Total": "Basado en FORMATO DE CHECKLIST TRADICIONAL Y TOTAL2025.pdf",
    "Infonavit Línea III": "Basado en FORMATO DE CHECKLIST INFONAVIT LINEA III 2025.pdf",
    "Cofinavit": "Basado en FORMATO DE CHECKLIST COFINAVIT 2025.pdf",
    "Bancario": "Basado en FORMATO DE CHECKLIST BANCARIO 2025.pdf",
    "Fovissste": "Basado en FORMATO DE CHECKLIST FOVISSTE 2025.pdf",
    "Fovissste para Todos": "Basado en FORMATO DE CHECKLIST FOVISSSTE PARA TODOS 2025.pdf",
    "Pensiona2": "Basado en FORMATO DE CHECKLIST PENSIONA2 2025.pdf",
    "Contado": "Basado en FORMATO DE CHECKLIST CONTADOS 2025.pdf",
}


def clean_filename(value: str) -> str:
    value = re.sub(r"[^A-Za-z0-9_-]+", "_", value.strip())
    return value.strip("_") or "sin_nombre"


def item_key(prefix: str, section: str, item: str) -> str:
    raw = f"{prefix}|{section}|{item}"
    return "ck_" + re.sub(r"[^A-Za-z0-9_]+", "_", raw)[:220]


def comment_key(prefix: str, section: str, item: str) -> str:
    return item_key(prefix, section, item).replace("ck_", "cm_", 1)


def upload_key(prefix: str, section: str, item: str) -> str:
    return item_key(prefix, section, item).replace("ck_", "up_", 1)


def optional_key(tipo: str, section: str) -> str:
    return "op_" + re.sub(r"[^A-Za-z0-9_]+", "_", f"{tipo}|{section}")[:180]


def get_marital_optional_sections(tipo: str, estado_civil: str) -> List[str]:
    if estado_civil != "Casado":
        return []

    markers = ("casado", "conyugal", "cónyuge", "mancomunado", "coacreditado", "sociedad conyugal")
    return [
        section.name
        for section in CHECKLISTS[tipo]
        if section.optional
        and any(marker in f"{section.name} {section.help_text}".lower() for marker in markers)
    ]


def visible_sections(tipo: str, enabled_optional: Iterable[str]) -> List[Section]:
    selected = set(enabled_optional)
    return [
        section
        for section in CHECKLISTS[tipo]
        if not section.optional or section.name in selected
    ]


def collect_rows(tipo: str, sections: List[Section], expediente: Dict[str, str]) -> List[Dict[str, str]]:
    rows = []
    prefix = expediente["folio"]
    for section in sections:
        for item in section.items:
            done = st.session_state.get(item_key(prefix, section.name, item), False)
            comment = st.session_state.get(comment_key(prefix, section.name, item), "")
            uploaded_files = st.session_state.get(upload_key(prefix, section.name, item), [])
            uploaded_names = ", ".join(file.name for file in uploaded_files) if uploaded_files else ""
            rows.append(
                {
                    "folio": expediente["folio"],
                    "fecha": expediente["fecha"],
                    "tipo_credito": tipo,
                    "cliente": expediente["cliente"],
                    "telefono": expediente["telefono"],
                    "asesor": expediente["asesor"],
                    "desarrollo": expediente["desarrollo"],
                    "calle": expediente["calle"],
                    "ubicacion": expediente["ubicacion"],
                    "seccion": section.name,
                    "requisito": item,
                    "estado": "Recibido" if done else "Pendiente",
                    "comentario": comment,
                    "archivos": uploaded_names,
                }
            )
    return rows


def make_txt(rows: List[Dict[str, str]], expediente: Dict[str, str]) -> str:
    lines = [
        "CHECKLIST AGUILAR 2025",
        f"Folio: {expediente['folio']}",
        f"Fecha: {expediente['fecha']}",
        f"Tipo de crédito: {rows[0]['tipo_credito'] if rows else ''}",
        f"Cliente: {expediente['cliente']}",
        f"Estado civil: {expediente.get('estado_civil', '')}",
        f"Teléfono: {expediente['telefono']}",
        f"Asesor: {expediente['asesor']}",
        f"Desarrollo: {expediente['desarrollo']}",
        f"Calle: {expediente['calle']}",
        f"Ubicación: {expediente['ubicacion']}",
        "",
    ]
    current_section = None
    for row in rows:
        if row["seccion"] != current_section:
            current_section = row["seccion"]
            lines.extend(["", f"--- {current_section.upper()} ---"])
        mark = "X" if row["estado"] == "Recibido" else " "
        comment = f" | Comentario: {row['comentario']}" if row["comentario"] else ""
        files = f" | Archivos: {row['archivos']}" if row.get("archivos") else ""
        lines.append(f"[{mark}] {row['requisito']}{comment}{files}")
    lines.extend(
        [
            "",
            "Observaciones generales:",
            expediente["observaciones"] or "Sin observaciones.",
            "",
            "Nota: Documento digital de control interno para Ventas y Titulación.",
        ]
    )
    return "\n".join(lines)


def make_csv(rows: List[Dict[str, str]]) -> str:
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=list(rows[0].keys()) if rows else [])
    writer.writeheader()
    writer.writerows(rows)
    return output.getvalue()


def make_pending_txt(rows: List[Dict[str, str]], expediente: Dict[str, str]) -> str:
    pending = [row for row in rows if row["estado"] != "Recibido"]
    lines = [
        "REQUISITOS FALTANTES - CHECKLIST AGUILAR 2025",
        f"Folio: {expediente['folio']}",
        f"Cliente: {expediente['cliente']}",
        f"Estado civil: {expediente.get('estado_civil', '')}",
        f"Fecha: {expediente['fecha']}",
        "",
    ]
    if not pending:
        lines.append("No hay requisitos faltantes.")
        return "\n".join(lines)

    current_section = None
    for row in pending:
        if row["seccion"] != current_section:
            current_section = row["seccion"]
            lines.extend(["", f"--- {current_section.upper()} ---"])
        comment = f" | Comentario: {row['comentario']}" if row["comentario"] else ""
        files = f" | Archivos: {row['archivos']}" if row.get("archivos") else ""
        lines.append(f"- {row['requisito']}{comment}{files}")
    return "\n".join(lines)


def make_progress_json(
    tipo: str,
    sections: List[Section],
    expediente: Dict[str, str],
    enabled_optional: Iterable[str],
) -> str:
    saved_items = []
    for section in sections:
        for item in section.items:
            saved_items.append(
                {
                    "section": section.name,
                    "item": item,
                    "done": st.session_state.get(item_key(expediente["folio"], section.name, item), False),
                    "comment": st.session_state.get(comment_key(expediente["folio"], section.name, item), ""),
                    "files": [
                        file.name
                        for file in st.session_state.get(upload_key(expediente["folio"], section.name, item), [])
                    ],
                }
            )

    payload = {
        "version": 1,
        "tipo_credito": tipo,
        "expediente": expediente,
        "optional_sections": list(enabled_optional),
        "items": saved_items,
    }
    return json.dumps(payload, ensure_ascii=False, indent=2)


def restore_progress(payload: Dict[str, object], tipo: str, expediente: Dict[str, str]) -> tuple[bool, str]:
    saved_tipo = str(payload.get("tipo_credito", ""))
    if saved_tipo and saved_tipo != tipo:
        return False, f"El archivo pertenece a '{saved_tipo}'. Seleccione ese tipo de expediente antes de cargarlo."

    saved_expediente = payload.get("expediente", {})
    if isinstance(saved_expediente, dict):
        saved_folio = str(saved_expediente.get("folio", ""))
        if saved_folio and saved_folio != expediente["folio"]:
            return False, f"El archivo pertenece al folio '{saved_folio}'. Use ese folio para restaurar el avance."

    optional_sections = payload.get("optional_sections", [])
    if isinstance(optional_sections, list):
        for section_name in optional_sections:
            st.session_state[optional_key(tipo, str(section_name))] = True

    items = payload.get("items", [])
    if not isinstance(items, list):
        return False, "El archivo de avance no tiene el formato esperado."

    for saved in items:
        if not isinstance(saved, dict):
            continue
        section = str(saved.get("section", ""))
        item = str(saved.get("item", ""))
        st.session_state[item_key(expediente["folio"], section, item)] = bool(saved.get("done", False))
        st.session_state[comment_key(expediente["folio"], section, item)] = str(saved.get("comment", ""))

    return True, "Avance restaurado correctamente."


def progress(rows: List[Dict[str, str]]) -> tuple[int, int, float]:
    total = len(rows)
    complete = sum(1 for row in rows if row["estado"] == "Recibido")
    ratio = complete / total if total else 0
    return complete, total, ratio


def render_header() -> None:
    st.title("Checklist Aguilar 2025")
    st.caption("Control digital de expedientes para Ventas y Titulación")


def default_client_data() -> Dict[str, str]:
    return {
        "tipo_credito": "Infonavit Tradicional y Total",
        "folio": f"AG-{date.today():%Y%m%d}",
        "fecha": date.today().isoformat(),
        "cliente": "",
        "telefono": "",
        "asesor": "",
        "desarrollo": "",
        "calle": "",
        "ubicacion": "",
        "estado_civil": "Soltero",
        "observaciones": "",
    }


def get_client_data() -> Dict[str, str]:
    if "client_data" not in st.session_state:
        st.session_state["client_data"] = default_client_data()
    return st.session_state["client_data"]


def client_data_from_payload(payload: Dict[str, object]) -> Dict[str, str]:
    saved_expediente = payload.get("expediente", {})
    if not isinstance(saved_expediente, dict):
        saved_expediente = {}

    data = default_client_data()
    data.update(
        {
            "tipo_credito": str(payload.get("tipo_credito") or data["tipo_credito"]),
            "folio": str(saved_expediente.get("folio") or data["folio"]),
            "fecha": str(saved_expediente.get("fecha") or data["fecha"]),
            "cliente": str(saved_expediente.get("cliente") or ""),
            "telefono": str(saved_expediente.get("telefono") or ""),
            "asesor": str(saved_expediente.get("asesor") or ""),
            "desarrollo": str(saved_expediente.get("desarrollo") or ""),
            "calle": str(saved_expediente.get("calle") or ""),
            "ubicacion": str(saved_expediente.get("ubicacion") or ""),
            "estado_civil": str(saved_expediente.get("estado_civil") or "Soltero"),
            "observaciones": str(saved_expediente.get("observaciones") or ""),
        }
    )
    if data["tipo_credito"] not in CHECKLISTS:
        data["tipo_credito"] = "Infonavit Tradicional y Total"
    if data["estado_civil"] not in ("Soltero", "Casado"):
        data["estado_civil"] = "Soltero"
    return data


def restore_saved_client(payload: Dict[str, object]) -> tuple[bool, str]:
    data = client_data_from_payload(payload)
    enabled_optional = get_marital_optional_sections(data["tipo_credito"], data["estado_civil"])
    expediente = {
        "folio": data["folio"],
        "fecha": data["fecha"],
        "cliente": data["cliente"],
        "telefono": data["telefono"],
        "asesor": data["asesor"],
        "desarrollo": data["desarrollo"],
        "calle": data["calle"],
        "ubicacion": data["ubicacion"],
        "estado_civil": data["estado_civil"],
        "observaciones": data["observaciones"],
    }
    restored, message = restore_progress(payload, data["tipo_credito"], expediente)
    if not restored:
        return False, message

    st.session_state["client_data"] = data
    st.session_state["client_registered"] = True
    st.session_state["restored_optional_sections"] = enabled_optional
    return True, "Expediente cargado correctamente."


def render_start_page() -> None:
    data = get_client_data()
    with st.container(border=True):
        st.subheader("Registro del cliente")
        c1, c2, c3 = st.columns(3)
        with c1:
            tipo = st.selectbox(
                "Tipo de crédito",
                list(CHECKLISTS.keys()),
                index=list(CHECKLISTS.keys()).index(data.get("tipo_credito", "Infonavit Tradicional y Total")),
            )
            cliente = st.text_input("Nombre del cliente", value=data.get("cliente", ""))
            asesor = st.text_input("Asesor", value=data.get("asesor", ""))
        with c2:
            folio = st.text_input("Folio interno", value=data.get("folio", f"AG-{date.today():%Y%m%d}"))
            desarrollo = st.text_input("Desarrollo / fraccionamiento", value=data.get("desarrollo", ""))
            calle = st.text_input("Calle y número", value=data.get("calle", ""))
        with c3:
            fecha_value = date.fromisoformat(data.get("fecha", date.today().isoformat()))
            fecha = st.date_input("Fecha de entrega", value=fecha_value).isoformat()
            ubicacion = st.text_input("Ubicación / manzana y lote", value=data.get("ubicacion", ""))
            telefono = st.text_input("Teléfono", value=data.get("telefono", ""))

        estado_civil = st.segmented_control(
            "Estado civil",
            ["Soltero", "Casado"],
            default=data.get("estado_civil", "Soltero"),
        )
        observaciones = st.text_area("Observaciones generales", value=data.get("observaciones", ""), height=90)

        if st.button("Registrar cliente y abrir checklist", type="primary", use_container_width=True):
            if not cliente.strip():
                st.warning("Capture el nombre del cliente.")
                return
            if not asesor.strip():
                st.warning("Capture el asesor.")
                return
            if not desarrollo.strip():
                st.warning("Capture el desarrollo.")
                return

            st.session_state["client_data"] = {
                "tipo_credito": tipo,
                "folio": folio or f"AG-{date.today():%Y%m%d}",
                "fecha": fecha,
                "cliente": cliente,
                "telefono": telefono,
                "asesor": asesor,
                "desarrollo": desarrollo,
                "calle": calle,
                "ubicacion": ubicacion,
                "estado_civil": estado_civil or "Soltero",
                "observaciones": observaciones,
            }
            st.session_state["client_registered"] = True
            st.rerun()

    with st.container(border=True):
        st.subheader("Abrir avance guardado")
        uploaded = st.file_uploader("Cargar expediente guardado (.json)", type=["json"])
        if uploaded is not None:
            try:
                payload = json.loads(uploaded.getvalue().decode("utf-8"))
                restored, message = restore_saved_client(payload)
                if restored:
                    st.success(message)
                    st.rerun()
                else:
                    st.warning(message)
            except (json.JSONDecodeError, UnicodeDecodeError):
                st.error("No pude leer ese archivo de avance.")


def render_client_file(expediente: Dict[str, str], tipo: str, complete: int, total: int, ratio: float) -> None:
    with st.container(border=True):
        top_left, top_right = st.columns([0.72, 0.28])
        with top_left:
            st.subheader(expediente["cliente"] or "Cliente sin nombre")
            st.caption(f"{tipo} · {expediente['estado_civil']} · Folio {expediente['folio']}")
        with top_right:
            st.metric("Avance", f"{ratio:.0%}", f"{complete} de {total}")
            st.progress(ratio)

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"**Asesor**  \n{expediente['asesor'] or '-'}")
        c2.markdown(f"**Desarrollo**  \n{expediente['desarrollo'] or '-'}")
        c3.markdown(f"**Ubicación**  \n{expediente['ubicacion'] or '-'}")
        c4.markdown(f"**Fecha**  \n{expediente['fecha'] or '-'}")

        c5, c6 = st.columns(2)
        c5.markdown(f"**Calle**  \n{expediente['calle'] or '-'}")
        c6.markdown(f"**Teléfono**  \n{expediente['telefono'] or '-'}")

        if expediente.get("observaciones"):
            st.markdown(f"**Observaciones**  \n{expediente['observaciones']}")

        if st.button("Editar registro del cliente", use_container_width=True):
            st.session_state["client_registered"] = False
            st.rerun()


def render_print_button() -> None:
    components.html(
        """
        <button onclick="window.parent.print()" style="
            width:100%;
            border:1px solid #0F766E;
            border-radius:6px;
            background:#0F766E;
            color:white;
            padding:0.55rem 0.8rem;
            font:600 0.95rem sans-serif;
            cursor:pointer;">
            Imprimir
        </button>
        """,
        height=48,
    )


def render_sidebar(
    tipo: str,
    sections: List[Section],
    rows: List[Dict[str, str]],
    expediente: Dict[str, str],
    enabled_optional: Iterable[str],
) -> None:
    complete, total, ratio = progress(rows)
    st.sidebar.header("Resumen")
    st.sidebar.metric("Avance", f"{complete}/{total}", f"{ratio:.0%}")
    st.sidebar.progress(ratio)
    st.sidebar.caption(SOURCE_NOTES.get(tipo, "Basado en formatos internos 2025"))

    filename_base = f"Checklist_{clean_filename(tipo)}_{clean_filename(expediente['cliente'])}"
    st.sidebar.header("Exportar")
    st.sidebar.download_button(
        "Descargar TXT",
        data=make_txt(rows, expediente),
        file_name=f"{filename_base}.txt",
        mime="text/plain",
        use_container_width=True,
    )
    st.sidebar.download_button(
        "Descargar CSV",
        data=make_csv(rows),
        file_name=f"{filename_base}.csv",
        mime="text/csv",
        use_container_width=True,
    )
    st.sidebar.download_button(
        "Guardar avance (.json)",
        data=make_progress_json(tipo, sections, expediente, enabled_optional),
        file_name=f"{filename_base}_avance.json",
        mime="application/json",
        use_container_width=True,
    )
    st.sidebar.download_button(
        "Descargar faltantes (.txt)",
        data=make_pending_txt(rows, expediente),
        file_name=f"{filename_base}_faltantes.txt",
        mime="text/plain",
        use_container_width=True,
    )

    st.sidebar.header("Imprimir")
    render_print_button()

    st.sidebar.header("Restaurar")
    uploaded = st.sidebar.file_uploader("Cargar avance guardado", type=["json"])
    if uploaded is not None:
        uploaded_bytes = uploaded.getvalue()
        upload_hash = hashlib.sha256(uploaded_bytes).hexdigest()
        if st.session_state.get("last_restored_upload") == upload_hash:
            st.sidebar.info("Este avance ya fue cargado.")
            return

        try:
            payload = json.loads(uploaded_bytes.decode("utf-8"))
            restored, message = restore_progress(payload, tipo, expediente)
            if restored:
                st.session_state["last_restored_upload"] = upload_hash
                st.sidebar.success(message)
                st.rerun()
            else:
                st.sidebar.warning(message)
        except (json.JSONDecodeError, UnicodeDecodeError):
            st.sidebar.error("No pude leer ese archivo de avance.")

    st.sidebar.header("Captura")
    if st.sidebar.button("Limpiar marcas de este expediente", use_container_width=True):
        for section in sections:
            for item in section.items:
                st.session_state[item_key(expediente["folio"], section.name, item)] = False
                st.session_state[comment_key(expediente["folio"], section.name, item)] = ""
        st.rerun()


def render_pending_summary(rows: List[Dict[str, str]]) -> None:
    pending = [row for row in rows if row["estado"] != "Recibido"]
    with st.container(border=True):
        st.subheader("Requisitos faltantes")
        if not pending:
            st.success("Expediente completo. No hay requisitos faltantes.")
            return

        st.caption(f"Pendientes: {len(pending)}")
        grouped: Dict[str, List[Dict[str, str]]] = {}
        for row in pending:
            grouped.setdefault(row["seccion"], []).append(row)

        for section, items in grouped.items():
            st.markdown(f"**{section}**")
            for row in items:
                comment = f" _({row['comentario']})_" if row["comentario"] else ""
                st.markdown(f"- {row['requisito']}{comment}")


def render_checklist(tipo: str, sections: List[Section], query: str, expediente: Dict[str, str]) -> None:
    normalized_query = query.strip().lower()
    for section in sections:
        filtered = [
            item
            for item in section.items
            if not normalized_query
            or normalized_query in item.lower()
            or normalized_query in section.name.lower()
        ]
        if not filtered:
            continue

        with st.expander(section.name, expanded=True):
            if section.help_text:
                st.info(section.help_text)
            for item in filtered:
                left, middle, right = st.columns([0.46, 0.28, 0.26])
                key = item_key(expediente["folio"], section.name, item)
                ckey = comment_key(expediente["folio"], section.name, item)
                ukey = upload_key(expediente["folio"], section.name, item)
                with left:
                    st.checkbox(item, key=key)
                with middle:
                    st.text_input("Comentario", key=ckey, label_visibility="collapsed", placeholder="Comentario o faltante")
                with right:
                    st.file_uploader(
                        "Archivo",
                        key=ukey,
                        label_visibility="collapsed",
                        accept_multiple_files=True,
                    )


def main() -> None:
    render_header()

    if not st.session_state.get("client_registered", False):
        render_start_page()
        return

    data = get_client_data()
    tipo = data["tipo_credito"]
    enabled_optional = get_marital_optional_sections(tipo, data.get("estado_civil", "Soltero"))
    sections = visible_sections(tipo, enabled_optional)
    expediente = {
        "folio": data.get("folio") or "SIN-FOLIO",
        "fecha": data.get("fecha", ""),
        "cliente": data.get("cliente", ""),
        "telefono": data.get("telefono", ""),
        "asesor": data.get("asesor", ""),
        "desarrollo": data.get("desarrollo", ""),
        "calle": data.get("calle", ""),
        "ubicacion": data.get("ubicacion", ""),
        "estado_civil": data.get("estado_civil", "Soltero"),
        "observaciones": data.get("observaciones", ""),
    }

    query_col, stat_col = st.columns([0.7, 0.3])
    with query_col:
        query = st.text_input("Buscar requisito", placeholder="Buscar por documento, formato o anexo")
    rows = collect_rows(tipo, sections, expediente)
    complete, total, ratio = progress(rows)
    with stat_col:
        st.metric("Avance del expediente", f"{ratio:.0%}", f"{complete} de {total}")

    render_client_file(expediente, tipo, complete, total, ratio)
    render_sidebar(tipo, sections, rows, expediente, enabled_optional)
    render_pending_summary(rows)
    render_checklist(tipo, sections, query or "", expediente)

    st.divider()
    st.caption(
        "Nota de validez: este documento digital sirve como guía de control interno. "
        "Los formatos oficiales firmados conservan su validez conforme al proceso de la empresa."
    )


if __name__ == "__main__":
    main()
