import tkinter as tk
from queue import Queue
from heapq import heappop, heappush

class Tabuleiro:
    def __init__(self, estado):
        self.estado = estado
        self.pos_vazio = self.buscar_vazio()

    def buscar_vazio(self):
        for linha, dados in enumerate(self.estado):
            for coluna, num in enumerate(dados):
                if num == 0:
                    return (linha, coluna)

    def mover_vazio(self, direcao):
        linha, coluna = self.pos_vazio
        if direcao == "up" and linha > 0:
            self.estado[linha][coluna], self.estado[linha-1][coluna] = self.estado[linha-1][coluna], self.estado[linha][coluna]
            self.pos_vazio = (linha-1, coluna)
            return self.estado[linha-1][coluna]
        elif direcao == "down" and linha < 2:
            self.estado[linha][coluna], self.estado[linha+1][coluna] = self.estado[linha+1][coluna], self.estado[linha][coluna]
            self.pos_vazio = (linha+1, coluna)
            return self.estado[linha+1][coluna]
        elif direcao == "left" and coluna > 0:
            self.estado[linha][coluna], self.estado[linha][coluna-1] = self.estado[linha][coluna-1], self.estado[linha][coluna]
            self.pos_vazio = (linha, coluna-1)
            return self.estado[linha][coluna-1]
        elif direcao == "right" and coluna < 2:
            self.estado[linha][coluna], self.estado[linha][coluna+1] = self.estado[linha][coluna+1], self.estado[linha][coluna]
            self.pos_vazio = (linha, coluna+1)
            return self.estado[linha][coluna+1]

def verifica_objetivo(estado):
    return estado == [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

def obter_vizinhos(estado):
    vizinhos = []
    pos_vazio = next((linha, coluna) for linha, dados in enumerate(estado) for coluna, num in enumerate(dados) if num == 0)
    linha, coluna = pos_vazio
    movimentos = [("up", (linha-1, coluna)), ("down", (linha+1, coluna)), ("left", (linha, coluna-1)), ("right", (linha, coluna+1))]
    
    for direcao, (x, y) in movimentos:
        if 0 <= x < 3 and 0 <= y < 3:
            novo_estado = [dados[:] for dados in estado]
            novo_estado[linha][coluna], novo_estado[x][y] = novo_estado[x][y], novo_estado[linha][coluna]
            vizinhos.append((novo_estado, direcao))
    
    return vizinhos

def busca_largura(estado_inicial):
    fila = Queue()
    fila.put((estado_inicial, []))
    visitados = set()
    visitados.add(tuple(map(tuple, estado_inicial)))
    
    while not fila.empty():
        estado_atual, caminho = fila.get()
        
        if verifica_objetivo(estado_atual):
            return caminho
        
        vizinhos = obter_vizinhos(estado_atual)
        
        for vizinho, direcao in vizinhos:
            if tuple(map(tuple, vizinho)) not in visitados:
                fila.put((vizinho, caminho + [direcao]))
                visitados.add(tuple(map(tuple, vizinho)))

    return None

def distancia_manhattan(estado):
    posicoes_alvo = {1: (0, 0), 2: (0, 1), 3: (0, 2), 8: (1, 0), 0: (1, 1), 4: (1, 2), 7: (2, 0), 6: (2, 1), 5: (2, 2)}
    dist = 0
    for linha, dados in enumerate(estado):
        for coluna, num in enumerate(dados):
            alvo_linha, alvo_coluna = posicoes_alvo[num]
            dist += abs(linha - alvo_linha) + abs(coluna - alvo_coluna)
    return dist

def busca_a_estrela(estado_inicial):
    conjunto_aberto = []
    heappush(conjunto_aberto, (distancia_manhattan(estado_inicial), estado_inicial, []))
    visitados = set()
    visitados.add(tuple(map(tuple, estado_inicial)))
    
    while conjunto_aberto:
        _, estado_atual, caminho = heappop(conjunto_aberto)
        
        if verifica_objetivo(estado_atual):
            return caminho
        
        vizinhos = obter_vizinhos(estado_atual)
        
        for vizinho, direcao in vizinhos:
            if tuple(map(tuple, vizinho)) not in visitados:
                heappush(conjunto_aberto, (distancia_manhattan(vizinho) + len(caminho) + 1, vizinho, caminho + [direcao]))
                visitados.add(tuple(map(tuple, vizinho)))

    return None

class AplicativoJogo8(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Jogo dos 8")
        self.geometry("600x500")
        self.configure(bg="#333333")
        self.estado_inicial = [[2, 0, 3], [1, 7, 4], [6, 8, 5]]
        self.tabuleiro = Tabuleiro([dados[:] for dados in self.estado_inicial])
        self.criar_interface()

    def criar_interface(self):
        self.rotulo_titulo = tk.Label(self, text="Jogo dos 8", font=("Helvetica", 24, "bold"), bg="#444444", fg="white", pady=10)
        self.rotulo_titulo.pack()

        frame_principal = tk.Frame(self, bg="#333333")
        frame_principal.pack(pady=10, padx=10, fill='both', expand=True)

        frame_jogo = tk.Frame(frame_principal, bg="#333333")
        frame_jogo.pack(side='left', padx=10, fill='both', expand=True)

        self.tela = tk.Canvas(frame_jogo, width=300, height=300, bg="#555555")
        self.tela.pack()
        self.atualizar_tabuleiro()

        frame_botoes = tk.Frame(frame_jogo, bg="#333333")
        frame_botoes.pack(pady=10)

        estilo_botao = {"bg": "#ffb84d", "fg": "black", "font": ("Helvetica", 12, "bold"), "padx": 10, "pady": 5}
        self.botao_bfs = tk.Button(frame_botoes, text="Busca em Amplitude", command=self.resolver_bfs, **estilo_botao)
        self.botao_bfs.grid(row=0, column=0, padx=10)

        self.botao_a_estrela = tk.Button(frame_botoes, text="Busca A*", command=self.resolver_a_estrela, **estilo_botao)
        self.botao_a_estrela.grid(row=0, column=1, padx=10)

        self.botao_reiniciar = tk.Button(frame_botoes, text="Reiniciar", command=self.reiniciar_tabuleiro, **estilo_botao)
        self.botao_reiniciar.grid(row=0, column=2, padx=10)

        self.rotulo_status = tk.Label(frame_jogo, text="", bg="#333333", fg="white", font=("Helvetica", 14))
        self.rotulo_status.pack(pady=10)

    def atualizar_tabuleiro(self):
        self.tela.delete("all")
        for linha, dados in enumerate(self.tabuleiro.estado):
            for coluna, num in enumerate(dados):
                if num != 0:
                    x0, y0 = 10 + coluna*100, 10 + linha*100
                    x1, y1 = x0 + 80, y0 + 80
                    self.tela.create_rectangle(x0, y0, x1, y1, fill="#ffb84d")
                    self.tela.create_text(x0 + 40, y0 + 40, text=str(num), font=("Helvetica", 32), fill="black")

    def resolver_bfs(self):
        self.rotulo_status.config(text="Iniciando Busca em Amplitude...")
        self.update()
        solucao = busca_largura(self.tabuleiro.estado)
        self.exibir_solucao(solucao, "Busca em Amplitude")

    def resolver_a_estrela(self):
        self.rotulo_status.config(text="Iniciando Busca A*...")
        self.update()
        solucao = busca_a_estrela(self.tabuleiro.estado)
        self.exibir_solucao(solucao, "Busca A*")

    def exibir_solucao(self, solucao, metodo):
        if solucao:
            for movimento in solucao:
                self.tabuleiro.mover_vazio(movimento)
                self.atualizar_tabuleiro()
                self.rotulo_status.config(text=f"Passo Atual: Mover para {self.obter_direcao_inversa(movimento)}")
                self.update()
                self.after(1000)
            self.rotulo_status.config(text=f"Solução encontrada com {metodo}!")
        else:
            self.rotulo_status.config(text="Solução não encontrada")

    def obter_direcao_inversa(self, direcao):
        if direcao == "up":
            return "para baixo"
        elif direcao == "down":
            return "para cima"
        elif direcao == "left":
            return "para a direita"
        elif direcao == "right":
            return "para a esquerda"

    def reiniciar_tabuleiro(self):
        self.estado_inicial = [[2, 0, 3], [1, 7, 4], [6, 8, 5]]
        self.tabuleiro = Tabuleiro([dados[:] for dados in self.estado_inicial])
        self.atualizar_tabuleiro()
        self.rotulo_status.config(text="")

if __name__ == "__main__":
    app = AplicativoJogo8()
    app.mainloop()
