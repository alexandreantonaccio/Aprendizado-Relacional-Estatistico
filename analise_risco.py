from pyswip import Prolog
import pandas as pd
from sklearn.linear_model import LogisticRegression
import warnings

# Ignorar avisos de treino devido ao tamanho minúsculo do dataset de exemplo
warnings.filterwarnings("ignore")

print("==================================================")
print(" PARTE 1: EXTRAÇÃO DE FEATURES LÓGICAS (PROLOG)   ")
print("==================================================")

# Inicializa o motor Prolog e carrega a base de fatos/regras
prolog = Prolog()
prolog.consult("rede_social.pl") # Certifique-se de que este ficheiro está na mesma pasta

# Carrega os dados tradicionais do cliente
df = pd.read_csv("dados_financeiros.csv")

def obter_grau_risco(nome):
    """
    Consulta o Prolog para descobrir o grau de separação entre o cliente
    e o utilizador sabidamente inadimplente (neste caso, o 'daniel').
    """
    query_str = f"risco_conexao({nome}, daniel, Grau)"
    
    # Executa a query. list() consome o gerador retornado pelo pyswip
    resultados = list(prolog.query(query_str))
    
    if resultados:
        # Extrai o valor associado à variável lógica 'Grau'
        return resultados[0]["Grau"]
    
    # Penalização para quem não tem conexão (ou valor neutro dependendo da modelação)
    return 999 

# Enriquecimento dos dados com o conhecimento extraído do grafo
df['grau_risco_rede'] = df['cliente_id'].apply(obter_grau_risco)

print("Dataset enriquecido com o 'grau_risco_rede':")
print(df.to_string())
print("\n")


print("==================================================")
print(" PARTE 2: TREINO DO CLASSIFICADOR ESTATÍSTICO     ")
print("==================================================")

# Definir as features (Atributos Clássicos + Atributo Relacional/Prolog)
X = df[['renda_mensal', 'score_classico', 'grau_risco_rede']]
y = df['inadimplente_historico']

# Treinar a Regressão Logística
modelo = LogisticRegression()
modelo.fit(X, y)

print("Modelo treinado com sucesso!")
print("Coeficientes Aprendidos (Pesos das Features):")
print(f"Renda: {modelo.coef_[0][0]:.5f}")
print(f"Score: {modelo.coef_[0][1]:.5f}")
print(f"Grau de Risco (Prolog): {modelo.coef_[0][2]:.5f}\n")


print("==================================================")
print(" PARTE 3: TEORIA NEURO-SIMBÓLICA E INFERÊNCIA     ")
print("==================================================")

# Vamos simular a predição para o 'joao' usando o modelo treinado
# Cliente Joao: Renda=5200, Score=750, Grau calculado pelo Prolog=3
cliente_novo_x = pd.DataFrame({
    'renda_mensal': [5200], 
    'score_classico': [750], 
    'grau_risco_rede': [3]
})

# Obter as probabilidades: [prob_adimplente, prob_inadimplente]
probabilidades = modelo.predict_proba(cliente_novo_x)
probabilidade_risco = probabilidades[0][1]

print("Saída Relacional Estatística (Estilo ProbLog):")
# Formata a nova regra com a probabilidade ancorada
# (No mundo real, o grau '3' seria parametrizado de forma dinâmica para cada cliente)
print(f"{probabilidade_risco:.2f} :: risco(joao) :- conectado_a(joao, daniel, 3).")
print("==================================================")