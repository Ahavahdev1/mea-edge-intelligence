# -*- coding: utf-8 -*-
import math
import inspect
import numpy as np
from mea.fractal import FractalQuantumCompressor

print("=" * 85)
print("🔬 AUDITORIA FORENSE ESTATÍSTICA E QUÂNTICA — MEA FRACTAL COMPRESSOR")
print("=" * 85)

n_qubits = 8  # 2^8 = 256 estados possíveis
sim = FractalQuantumCompressor(n_qubits=n_qubits, max_iter=30)
total_estados = sim.total_states

print(f"[*] Sistema inicializado com {n_qubits} Qubits ({total_estados} estados possíveis).\n")

# ==============================================================================
# TESTE 1: AUDITORIA DA REGRA DE BORN (A SOMA REAL DÁ 1.0?)
# ==============================================================================
print("[TESTE 1] Auditoria Rigorosa da Soma de Probabilidades (Axioma de Born)")

probabilidades = [sim.get_probability(i) for i in range(total_estados)]
soma_real = sum(probabilidades)
erro_soma = abs(soma_real - 1.0)

print(f"    ├── Soma calculada de todos os 256 estados : {soma_real:.6f}")
print(f"    ├── Desvio da lei física (ideal = 1.0)     : {erro_soma:.6f}")

if erro_soma < 0.001:
    print("    └── ✅ PASSOU: O sistema está rigorosamente normalizado (Σ P = 1.0).")
    teste1_passou = True
else:
    print(f"    └── ❌ FALHA CRÍTICA: Violação de probabilidade! A soma deu {soma_real:.4f} em vez de 1.0.")
    teste1_passou = False

# ==============================================================================
# TESTE 2: COERÊNCIA AMPLITUDE vs PROBABILIDADE (P(x) = |Amplitude|²)
# ==============================================================================
print("\n[TESTE 2] Coerência entre Amplitude Complexa e Probabilidade")

desvios_born = []
for i in range(min(50, total_estados)):
    amp = sim.get_amplitude(i)
    prob_declarada = sim.get_probability(i)
    prob_fisica_real = abs(amp) ** 2
    desvios_born.append(abs(prob_declarada - prob_fisica_real))

desvio_medio_born = np.mean(desvios_born)
print(f"    ├── Desvio médio entre P(x) e |Amp(x)|²     : {desvio_medio_born:.8f}")

if desvio_medio_born < 1e-4:
    print("    └── ✅ PASSOU: As probabilidades derivam perfeitamente das amplitudes complexas.")
    teste2_passou = True
else:
    print("    └── ❌ FALHA: get_probability() e get_amplitude() discordam entre si!")
    teste2_passou = False

# ==============================================================================
# TESTE 3: AUDITORIA FORENSE DO AMOSTRADOR MCMC (Ele amostra a física ou chuta?)
# ==============================================================================
print("\n[TESTE 3] Validação Estatística do Amostrador MCMC")
num_amostras = 5000
print(f"    └── Coletando {num_amostras} amostras via MCMC...")

counts = sim.sample_mcmc(num_samples=num_amostras, burn_in=100)

# Frequência empírica medida no MCMC
freq_mcmc = np.zeros(total_estados)
for estado_bin, qtd in counts.items():
    idx = int(estado_bin, 2) if isinstance(estado_bin, str) else int(estado_bin)
    freq_mcmc[idx] = qtd / num_amostras

# Correlação de Pearson entre o que o MCMC sorteou e o que a probabilidade mandava
prob_teorica = np.array(probabilidades)
if np.std(freq_mcmc) > 0 and np.std(prob_teorica) > 0:
    correlacao = np.corrcoef(freq_mcmc, prob_teorica)[0, 1]
else:
    correlacao = 0.0

print(f"    ├── Correlação Estatística (MCMC vs Teoria): {correlacao:.4f} (Ideal: > 0.85)")

if correlacao >= 0.85:
    print("    └── ✅ PASSOU: O MCMC converge fielmente para a distribuição quântica.")
    teste3_passou = True
elif correlacao >= 0.50:
    print("    └── ⚠️ PARCIAL: MCMC converge com ruído considerável.")
    teste3_passou = False
else:
    print(f"    └── ❌ FALHA: O MCMC não tem correlação com as probabilidades do sistema!")
    teste3_passou = False

# ==============================================================================
# PROVA FORENSE DE CÓDIGO
# ==============================================================================
print("\n" + "=" * 85)
print("📜 CÓDIGO-FONTE REAL DO MÉTODO get_amplitude():")
print("=" * 85)
try:
    print(inspect.getsource(sim.get_amplitude))
except Exception as e:
    print(f"Erro ao extrair código: {e}")

print("=" * 85)
print("⚖️ VEREDITO FINAL DA AUDITORIA:")
if teste1_passou and teste2_passou and teste3_passou:
    print("🏆 APROVADO: O motor obedece rigorosamente às leis da física quântica e estatística!")
else:
    print("❌ REPROVADO: O motor não cumpre os axiomas matemáticos da física quântica.")
print("=" * 85)
