# Importa as bibliotecas necessárias
import random
import os
import time
import threading
import psutil

# Define as classes
class Carro:
    def __init__(self, id, direcao, destino):
        """
        Inicializar um objeto Carro.

        Parametros:
        - id (int): O identificador único para o carro.
        - direcao (str): A direção inicial do carro.
        - destino (str): A direção de destino do carro.
        """
        self.id = id
        self.direcao = direcao
        self.destino = destino

    def mover(self):
        """
        Mover o carro para o seu destino.
        """
        print(f'Carro {self.id} atravessou a interseção: {self.direcao} -> {self.destino}')


class Semaforo:
    def __init__(self):
        """
        Inicializar um objeto Semáforo.
        """
        self.estado = "Vermelho" # Definir o estado inicial --> Vermelho

    def mudar_estado(self):
        """
        Altera o estado do semáforo.
        """
        if self.estado == "Verde":
            self.estado = "Vermelho"
        else:
            self.estado = "Verde"


class Intersecao:
    def __init__(self, n_carros):
        """
        Inicializar um objeto Interseção.

        Parametros:
        - n_carros (int): O número de carros na interseção.
        """
        # Lista dos semafóros de cada direção na interseção
        self.semaforos = {
            "Norte": Semaforo(),
            "Oeste": Semaforo(),
            "Sul": Semaforo(),
            "Este": Semaforo()
        }
        self.carros = [] # Lista dos carros na interseção
        self.carros_passados = [] # Lista de carros que passaram pela interseção até ao seu destino
        self.numero_carros = n_carros # Número de carros que estão na interseção


    def criar_carros(self):
        """
        Criar carros na interseção com direções e destinos aleatórios.
        """
        direcoes_carros = [] # Lista que contém as direções iniciais dos carros
        destinos_carros = [] # Lista que contém os destinos dos carros

        for _ in range(self.numero_carros):
            # Escolha uma direção inicial e um destino aleatórios
            direcao = random.choice(["Norte", "Oeste", "Sul", "Este"])
            destino = random.choice(["Norte", "Oeste", "Sul", "Este"])

            # Verifica se a direção e o destino são diferentes
            while destino == direcao:
                destino = random.choice(["Norte", "Oeste", "Sul", "Este"])

            # Adiciona os valores aleatórios nas listas    
            direcoes_carros.append(direcao)
            destinos_carros.append(destino)

            # Criar os carros
            self.carros = [Carro(id, direcao, destino) for id, direcao, destino in zip(range(1, self.numero_carros + 1), direcoes_carros, destinos_carros)]


    def gerir_semaforos(self):
        """
        Gerir os estados dos semáforos.
        """
        # Verifique se ainda há carros na interseção
        while len(self.carros_passados) < self.numero_carros:
            # Muda o estado de cada semáforo a cada 10 segundos
            for direcao in self.semaforos:
                self.semaforos[direcao].mudar_estado()
                t = 10
                while t:
                    print(f'Semaforo {direcao}: Verde ' + '{:02d}'.format(t), end='\r') # Imprime o estado do semáforo --> Verde
                    time.sleep(1)
                    t -= 1
                print(f'Semaforo {direcao}: Vermelho') # Imprime o estado do semáforo --> Vermelho
                self.semaforos[direcao].mudar_estado()
                time.sleep(1) # Um intervalo de um segundo durante as mudanças de estado dos semáforos


    def gerir_carros(self):
        """
        Gerir a passagem dos carros na interseção.
        """
        # Verifique se ainda há carros na interseção
        while len(self.carros_passados) < self.numero_carros:
            for carro in self.carros:
                # Simula tempo de chegada aleatório
                time.sleep(random.uniform(0.5, 1.5))
                # Verifique o estado do semáforo
                if self.semaforos[carro.direcao].estado == 'Verde':
                    time.sleep(0.5)
                    carro.mover()
                    self.carros_passados.append(carro) # Quando o carro passa, adiciona-o à lista de carros que passaram
                    self.carros.remove(carro) # Quando o carro passa, remove-o da lista de carros na intersecção


    def gerir_intersecao(self):
        """
        Gerir a interseção.
        """
        # Limpar o ecrã da consola
        os.system('cls')

        # Cria os carros na interseção
        self.criar_carros()

        # Criar um thread para gerir os estados dos semáforos na interseção
        thread1 = threading.Thread(target=self.gerir_semaforos)

        # Criar um thread para gerir a passagem dos carros na interseção
        thread2 = threading.Thread(target=self.gerir_carros)

        # Iniciar os dois threads
        thread1.start()
        thread2.start()

        # Juntar os dois threads
        thread1.join()
        thread2.join()


class Simulador:
    def __init__(self, intersecao):
        """
        Inicializar um objeto Simulador.

        Parâmetros:
        - intersecao (Intersecao): O objeto de intersecção a ser simulado.
        """
        self.intersecao = intersecao

        # Inicializa os atributos de tempo, uso de CPU e memória com valores iniciais
        self.start_time = 0
        self.end_time = 0
        self.total_run_time = 0
        self.cpu_percent_start = 0
        self.cpu_percent_end = 0
        self.memory_percent_start = 0
        self.memory_info_end = 0 


    def iniciar_simulacao(self):
        """
        Inicia a contagem do tempo, e registra o uso inicial de CPU e memória.
        """
        # Registra os valores iniciais de tempo, uso de CPU e uso de memória
        self.start_time = time.time()
        self.cpu_percent_start = psutil.cpu_percent()
        self.memory_percent_start = psutil.virtual_memory().percent
    

    def finalizar_simulacao(self):
        """
        Finaliza a contagem do tempo e calcula o uso de CPU e memória ao final da execução.
        """
        # Calcula o tempo de execução e o uso de CPU e memória no final da execução
        self.end_time = time.time()
        self.total_run_time = self.end_time - self.start_time
        self.cpu_percent_end = psutil.cpu_percent()
        self.memory_info_end = psutil.virtual_memory()


    def print_simulacao_info(self):
        """
        Imprime informações sobre a simulação, incluindo uso de CPU, uso de memória e tempo de execução.
        """
        print("----------------------------------------\n")
        print(f'Uso de CPU: {self.cpu_percent_end:.2f}% (início: {self.cpu_percent_start:.2f}%)')
        print(f'Uso de Memória: {self.memory_info_end.percent:.2f}% (início: {self.memory_percent_start:.2f}%)')
        print(f'Tempo total de execução do Simulador: {self.total_run_time:.2f} segundos')
        print("\n----------------------------------------")    


    def simular_intersecao(self):
        """
        Inicia a simulação da interseção, registra o início e o final da execução e finaliza a simulação.
        """
        # Inicia a simulação registando o tempo, o uso inicial de CPU e memória
        self.iniciar_simulacao()

        # Chama o método que gerencia a simulação da interseção
        self.intersecao.gerir_intersecao()

        # Finaliza a simulação registando o tempo final, o uso final de CPU e memória
        self.finalizar_simulacao()

        # Imprime informações detalhadas sobre a simulação de tráfego, incluindo uso de CPU, uso de memória e tempo de execução
        self.print_simulacao_info()



#############################################################################
############################# Inicio do Programa ############################
#############################################################################

if __name__ == '__main__':

    # Limpar o ecrã da consola
    os.system('cls')

    # Solicita ao utilizador introduzir o número de carros a gerir na interseção
    numero_carros = input('Insira o número de carros a gerir na interseção: ')

    # Cria a interseção com um número de carros
    intersecao = Intersecao(int(numero_carros))

    # Cria o simulador da interseção
    simulador_de_trafego = Simulador(intersecao)

    # Inicia o simulador
    simulador_de_trafego.simular_intersecao()

