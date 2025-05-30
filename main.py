import socket

from pysnmp.hlapi import (
    SnmpEngine,
    CommunityData,
    UdpTransportTarget,
    ContextData,
    ObjectType,
    ObjectIdentity,
    getCmd,
)
import pandas as pd
from datetime import datetime
import os
import matplotlib.pyplot as plt

USE_SIMULATION = False  # Coloque True para testar sem SNMP real


def snmp_get(ip, oid, community='public'):
    if USE_SIMULATION:
        print(f"[SIMULAÇÃO] {ip} -> {oid}")
        return "123456" if "4.1.1" in oid else "SN123456"

    iterator = getCmd(
        SnmpEngine(),
        CommunityData(community),
        UdpTransportTarget((ip, 161), timeout=2, retries=1),
        ContextData(),
        ObjectType(ObjectIdentity(oid))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(f"[ERRO SNMP] {ip} - {oid}: {errorIndication}")
        return None
    elif errorStatus:
        print(f"[ERRO STATUS] {ip} - {oid}: {errorStatus.prettyPrint()}")
        return None
    else:
        for varBind in varBinds:
            print(f"[OK SNMP] {ip} - {oid}: {varBind}")
            return str(varBind[1])


def get_info(printers):
    current_day = datetime.now()
    current_str = current_day.strftime("%Y-%m-%d %H:%M:%S")
    current_month = current_day.strftime("%Y-%m")  # para consistência

    os.makedirs("dados", exist_ok=True)

    for name, ip in printers.items():
        print(f"\n[INFO] Consultando {name} ({ip})")
        pages = snmp_get(ip, "1.3.6.1.2.1.43.10.2.1.4.1.1")
        serie = snmp_get(ip, "1.3.6.1.2.1.43.5.1.1.17.1")

        if pages is None or serie is None:
            print(f"[AVISO] Dados incompletos para {name}")
            continue

        try:
            pages = int(pages)
        except ValueError:
            pages = None

        file = f"dados/{name}.csv"
        pages_this_month = None

        # Verifica valor anterior se existir
        if os.path.exists(file):
            df_old = pd.read_csv(file, parse_dates=["collection_date"])
            df_old = df_old.sort_values("collection_date")

            if not df_old['total_pages'].isna().all():
                ultima_linha = df_old['total_pages'].dropna().iloc[-1]
                pages_this_month = pages - ultima_linha if pages is not None else None
        else:
            df_old = pd.DataFrame()

        # Novo dado
        data = {
            "collection_date": current_str,
            "month": current_month,
            "name": name,
            "ip": ip,
            "serie": serie,
            "total_pages": pages,
            "pages_this_month": pages_this_month if pages_this_month else "0.0"
        }

        # Salva/concatena
        df_new = pd.DataFrame([data])
        df = pd.concat([df_old, df_new], ignore_index=True)
        df.to_csv(file, index=False)

        print(f"[OK] Dados salvos em: {file}")


def get_ip_printer(hostname):
    try:
        ip = socket.gethostbyname(hostname)
        return ip
    except socket.gaierror:
        print(f"[INFO] Consultando {hostname} (IP não encontrado)")
        return None


if __name__ == "__main__":
    printers = {
        "imp-03-1": get_ip_printer("imp-03-1"),
        "imp-03-2": get_ip_printer("imp-03-2"),
        "imp-04-1": get_ip_printer("imp-04-1"),
        "imp-05-1": get_ip_printer("imp-05-1"),
        "imp-06-1": get_ip_printer("imp-06-1"),
        "imp-07-1": get_ip_printer("imp-07-1"),
        "imp-08-1": get_ip_printer("imp-08-1"),
        "imp-09-1": get_ip_printer("imp-09-1"),
        "imp-10-1": get_ip_printer("imp-10-1"),
        "imp-11-2": get_ip_printer("imp-11-2"),
        "imp-12-1": get_ip_printer("imp-12-1"),
        "imp-13-1": get_ip_printer("imp-13-1"),
        "imp-14-1": get_ip_printer("imp-14-1")
    }

    get_info(printers)
