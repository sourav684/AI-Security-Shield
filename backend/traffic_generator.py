import time
import random

try:
    from pymodbus.client import ModbusTcpClient  # type: ignore[import-not-found]
except ImportError:  # pragma: no cover - dependency is optional in some environments
    class ModbusTcpClient:  # type: ignore[no-redef]
        def __init__(self, *args, **kwargs):
            raise RuntimeError(
                "pymodbus is required for OT traffic generation. "
                "Install it with: pip install pymodbus"
            )

def send_normal_traffic(client):
    """FC 3: Read Holding Registers (Standard Read Telemetry)"""
    try:
        client.read_holding_registers(address=1, count=5, slave=1)
    except Exception:
        pass

def send_attack_traffic(client):
    """Simulates Unauthorized Write Attack or Rapid High-Frequency Parameter Flood"""
    attack_type = random.choice(["UNAUTHORIZED_WRITE", "PARAMETER_ALTERATION"])
    try:
        if attack_type == "UNAUTHORIZED_WRITE":
            # Function Code 6/16: Unauthorized Register Overwrite
            client.write_register(address=99, value=9999, slave=1)
        elif attack_type == "PARAMETER_ALTERATION":
            # Rapid high-frequency request flooding
            for _ in range(10):
                client.read_holding_registers(address=1, count=100, slave=1)
    except Exception:
        pass

if __name__ == "__main__":
    client = ModbusTcpClient('127.0.0.1', port=5020)
    client.connect()
    print("[*] Simulating OT Modbus TCP Traffic Engine...")
    
    while True:
        # 80% Normal Operations vs 20% Injected Cyber Attacks
        if random.random() > 0.2:
            send_normal_traffic(client)
            time.sleep(1.0)
        else:
            print("[!] Injecting Simulated OT Attack Command Traffic...")
            send_attack_traffic(client)
            time.sleep(0.3)