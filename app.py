from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from io import StringIO
from typing import Dict, Iterable, List
import csv
import re

import streamlit as st


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
        lines.append(f"[{mark}] {row['requisito']}{comment}")
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


def progress(rows: List[Dict[str, str]]) -> tuple[int, int, float]:
    total = len(rows)
    complete = sum(1 for row in rows if row["estado"] == "Recibido")
    ratio = complete / total if total else 0
    return complete, total, ratio


def render_header() -> None:
    st.title("Checklist Aguilar 2025")
    st.caption("Control digital de expedientes para Ventas y Titulación")


def render_sidebar(tipo: str, sections: List[Section], rows: List[Dict[str, str]], expediente: Dict[str, str]) -> None:
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

    st.sidebar.header("Captura")
    if st.sidebar.button("Limpiar marcas de este expediente", use_container_width=True):
        for section in sections:
            for item in section.items:
                st.session_state[item_key(expediente["folio"], section.name, item)] = False
                st.session_state[comment_key(expediente["folio"], section.name, item)] = ""
        st.rerun()


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
                left, right = st.columns([0.58, 0.42])
                key = item_key(expediente["folio"], section.name, item)
                ckey = comment_key(expediente["folio"], section.name, item)
                with left:
                    st.checkbox(item, key=key)
                with right:
                    st.text_input("Comentario", key=ckey, label_visibility="collapsed", placeholder="Comentario o faltante")


def main() -> None:
    render_header()

    with st.container(border=True):
        left, middle, right = st.columns([1.2, 1, 1])
        with left:
            tipo = st.selectbox("Tipo de expediente", list(CHECKLISTS.keys()))
        with middle:
            folio = st.text_input("Folio interno", value=f"AG-{date.today():%Y%m%d}")
        with right:
            fecha = st.date_input("Fecha de entrega", value=date.today()).isoformat()

        c1, c2, c3 = st.columns(3)
        with c1:
            cliente = st.text_input("Nombre del cliente", placeholder="Ej. Juan Pérez López")
            telefono = st.text_input("Teléfono", placeholder="Opcional")
        with c2:
            asesor = st.text_input("Asesor", placeholder="Nombre del asesor")
            desarrollo = st.text_input("Desarrollo / fraccionamiento")
        with c3:
            calle = st.text_input("Calle y número")
            ubicacion = st.text_input("Ubicación / manzana y lote")

        observaciones = st.text_area("Observaciones generales", height=90)

    optional_sections = [section for section in CHECKLISTS[tipo] if section.optional]
    enabled_optional = []
    if optional_sections:
        st.subheader("Casos especiales")
        cols = st.columns(min(3, len(optional_sections)))
        for index, section in enumerate(optional_sections):
            with cols[index % len(cols)]:
                if st.toggle(section.name, help=section.help_text):
                    enabled_optional.append(section.name)

    sections = visible_sections(tipo, enabled_optional)
    expediente = {
        "folio": folio or "SIN-FOLIO",
        "fecha": fecha,
        "cliente": cliente,
        "telefono": telefono,
        "asesor": asesor,
        "desarrollo": desarrollo,
        "calle": calle,
        "ubicacion": ubicacion,
        "observaciones": observaciones,
    }

    query_col, stat_col = st.columns([0.7, 0.3])
    with query_col:
        query = st.text_input("Buscar requisito", placeholder="Buscar por documento, formato o anexo")
    rows = collect_rows(tipo, sections, expediente)
    complete, total, ratio = progress(rows)
    with stat_col:
        st.metric("Avance del expediente", f"{ratio:.0%}", f"{complete} de {total}")

    render_sidebar(tipo, sections, rows, expediente)
    render_checklist(tipo, sections, query or "", expediente)

    st.divider()
    st.caption(
        "Nota de validez: este documento digital sirve como guía de control interno. "
        "Los formatos oficiales firmados conservan su validez conforme al proceso de la empresa."
    )


if __name__ == "__main__":
    main()
