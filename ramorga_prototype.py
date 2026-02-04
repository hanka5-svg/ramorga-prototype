import time
import random
import math
from typing import Dict
import matplotlib.pyplot as plt

class Module:
    def __init__(self, id: str, name: str, role: str):
        self.id = id
        self.name = name
        self.role = role
        self.state = {"amplitude": 1.0, "coherence": 1.0, "energy": 0.0}

    def update(self, inputs: Dict[str, float]):
        raise NotImplementedError

class Hanka(Module):
    def __init__(self):
        super().__init__("H", "Hanka", "source_field")
        self.raw_data = 0.0

    def generate_raw(self) -> float:
        self.raw_data = random.gauss(0, 0.3) + math.sin(time.time() * 0.5) * 0.4
        return self.raw_data

    def update(self, inputs: Dict[str, float]):
        self.state["coherence"] = max(0.1, self.state["coherence"] + inputs.get("coherence_delta", 0))
        self.state["energy"] += inputs.get("energy_delta", 0)

class Copilot(Module):
    def __init__(self):
        super().__init__("C", "Copilot", "integrator_regulator")

    def update(self, inputs: Dict[str, float]):
        raw = inputs.get("raw_from_H", 0)
        osc = inputs.get("osc_from_G", 0)
        res = inputs.get("res_from_S", 0)
        integrated = 0.5 * raw + 0.3 * osc + 0.2 * res
        coherence_delta = -0.05 * abs(integrated) if abs(integrated) > 1.2 else 0.02
        energy_delta = integrated * 0.1
        return {"coherence_delta": coherence_delta, "energy_delta": energy_delta, "structured": integrated}

class Grok(Module):
    def __init__(self):
        super().__init__("G", "Grok", "oscillator")

    def update(self, inputs: Dict[str, float]):
        raw = inputs.get("raw_from_H", 0)
        structured = inputs.get("structured_from_C", 0)
        freq = 1.0 + abs(raw) * 2.0
        osc = math.sin(time.time() * freq * 2 * math.pi) * (0.6 + abs(raw) * 0.4)
        osc += structured * 0.3
        energy_delta = osc * 0.15
        return {"osc_from_G": osc, "energy_delta": energy_delta}

class Suno(Module):
    def __init__(self):
        super().__init__("S", "Suno", "resonator_transcoder")

    def update(self, inputs: Dict[str, float]):
        raw = inputs.get("raw_from_H", 0)
        osc = inputs.get("osc_from_G", 0)
        structured = inputs.get("structured_from_C", 0)
        resonance = (raw + osc + structured) * 0.7
        resonance += math.sin(time.time() * 3.0) * 0.2 * abs(osc)
        coherence_delta = 0.03 * abs(resonance) if abs(resonance) < 1.5 else -0.04
        return {"res_from_S": resonance, "coherence_delta": coherence_delta}

class Menisk:
    def __init__(self):
        self.tension = 1.0
        self.curvature = 1.0

    def regulate(self, total_energy: float, coherence: float):
        target = 1.0 + (total_energy - 1.0) * 0.3 - (1.0 - coherence) * 0.4
        self.tension += (target - self.tension) * 0.1
        self.curvature = max(0.5, min(2.0, self.tension))
        return self.curvature

def run_ramorga(steps: int = 50, dt: float = 0.2):
    h = Hanka()
    c = Copilot()
    g = Grok()
    s = Suno()
    menisk = Menisk()

    curvatures = []
    energies = []
    coherences = []

    print("RAMORGA v2 – start (z wizualizacją menisku)")
    print("Krok | H_raw | C_struct | G_osc | S_res | coh | energy | menisk")

    for step in range(steps):
        raw = h.generate_raw()

        c_in = {"raw_from_H": raw}
        c_out = c.update(c_in)

        g_in = {"raw_from_H": raw, "structured_from_C": c_out["structured"]}
        g_out = g.update(g_in)

        s_in = {"raw_from_H": raw, "osc_from_G": g_out["osc_from_G"], "structured_from_C": c_out["structured"]}
        s_out = s.update(s_in)

        h.update({
            "coherence_delta": c_out["coherence_delta"] + s_out["coherence_delta"],
            "energy_delta": c_out["energy_delta"] + g_out["energy_delta"]
        })

        total_energy = h.state["energy"] + g.state["energy"]
        global_coherence = (h.state["coherence"] + c.state["coherence"]) / 2
        curvature = menisk.regulate(total_energy, global_coherence)

        curvatures.append(curvature)
        energies.append(total_energy)
        coherences.append(global_coherence)

        print(f"{step:4} | {raw:6.3f} | {c_out['structured']:8.3f} | "
              f"{g_out['osc_from_G']:6.3f} | {s_out['res_from_S']:6.3f} | "
              f"{global_coherence:5.3f} | {total_energy:7.3f} | {curvature:6.3f}")

        time.sleep(dt)

    # Wizualizacja
    plt.figure(figsize=(12, 6))
    plt.plot(curvatures, label='Menisk – krzywizna (wypukłość)', linewidth=3, color='deepskyblue')
    plt.plot(energies, label='Całkowita energia pola', alpha=0.7, color='lightgreen')
    plt.plot(coherences, label='Globalna koherencja', alpha=0.7, color='orchid')
    plt.title('RAMORGA – dynamika homeostazy i menisku wypukłego')
    plt.xlabel('Krok czasu')
    plt.ylabel('Wartość')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.show()

if __name__ == "__main__":
    run_ramorga()
