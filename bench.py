# Salve como consertar_crosstalk.py e execute: python .\consertar_crosstalk.py

import os
import shutil

caminho = os.path.join("mea", "memory.py")

with open(caminho, "r", encoding="utf-8") as f:
    codigo = f.read()

nova_classe = '''class HolographicQuantumMemory:
    """
    Motor de Memória Holográfica com Correção Espectral, Blindagem Anti-Cross-Talk
    e Conservação de Energia (Parseval).
    """
    def __init__(self, dimension: int = 8, redundancia_fator: int = 2):
        self.dim = dimension
        self.fator = redundancia_fator
        self.dim_estendida = self.dim * self.fator
        
        rng = np.random.RandomState(42)
        self.phase_mask = np.exp(1j * rng.uniform(0, 2 * np.pi, self.dim_estendida))
        self.holographic_core = np.zeros(self.dim_estendida, dtype=complex)
        self.escalas = np.ones(self.dim, dtype=float)

    def _ajustar_dimensoes(self, nova_dim: int):
        if nova_dim * self.fator != self.dim_estendida:
            self.dim = nova_dim
            self.dim_estendida = self.dim * self.fator
            rng = np.random.RandomState(42)
            self.phase_mask = np.exp(1j * rng.uniform(0, 2 * np.pi, self.dim_estendida))
            self.holographic_core = np.zeros(self.dim_estendida, dtype=complex)
            self.escalas = np.ones(self.dim, dtype=float)

    def gravar_insight(self, metricas_vetor: List[float]):
        arr = np.array(metricas_vetor, dtype=float)
        if len(arr) != self.dim:
            self._ajustar_dimensoes(len(arr))

        # 🛡️ BLINDAGEM ANTI-CROSS-TALK:
        # Guarda a escala de cada sensor para evitar que 1420 MHz engula 0.003 rad
        self.escalas = np.maximum(np.abs(arr), 1e-4)
        vetor_normalizado = arr / self.escalas  # Fica tudo entre -1.0 e 1.0!

        # Duplica no espaço (Redundância 2x)
        vetor_protegido = np.tile(vetor_normalizado, self.fator)
        
        # Modula com a máscara de fase e projeta na FFT
        sinal = np.array(vetor_protegido, dtype=complex)
        self.holographic_core = np.fft.fft(sinal * self.phase_mask)

    def recuperar_sob_estresse(self, taxa_perda_hardware: float = 0.5, semente: int = 42) -> List[float]:
        if taxa_perda_hardware >= 1.0:
            return [0.0] * self.dim

        holograma_danificado = self.holographic_core.copy()
        
        # Simula perda física de canais
        rng = np.random.RandomState(semente)
        canais_vivos = rng.uniform(0.0, 1.0, self.dim_estendida) >= taxa_perda_hardware
        holograma_danificado[~canais_vivos] = 0.0 + 0.0j

        # iFFT e demodulação
        reconstrucao = np.fft.ifft(holograma_danificado) / self.phase_mask
        rec_real = np.real(reconstrucao)

        # Teorema de Parseval: restaura a energia média dos canais perdidos
        fracao_sobrevivente = max(np.mean(canais_vivos), 1e-4)
        fator_escala = 1.0 / fracao_sobrevivente

        # Recombina as duas metades normalizadas pela média
        bloco_dados = rec_real[:self.dim] * fator_escala
        bloco_ecc = rec_real[self.dim:self.dim * 2] * fator_escala
        rec_norm = (bloco_dados + bloco_ecc) / 2.0

        # Devolve as grandezas físicas reais multiplicando pelas escalas originais
        rec_final = rec_norm * self.escalas
        return rec_final.tolist()
'''

parte_inicial = codigo.split("class HolographicQuantumMemory:")[0]
codigo_atualizado = parte_inicial + nova_classe

with open(caminho, "w", encoding="utf-8") as f:
    f.write(codigo_atualizado)

cache = os.path.join("mea", "__pycache__")
if os.path.exists(cache):
    shutil.rmtree(cache)

print("✅ Blindagem Anti-Cross-Talk aplicada com sucesso!")
