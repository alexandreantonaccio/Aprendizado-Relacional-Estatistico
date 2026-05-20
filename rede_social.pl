% ==============================================================================
% ANÁLISE DE RISCO DE CRÉDITO HÍBRIDO EM REDES SOCIAIS
% Entregável 1: Base de Fatos (rede_social.pl)
% ==============================================================================

% 1. Fatos de transações (Conexões diretas)
% Sintaxe: transacao_entre(Origem, Destino, Valor).
transacao_entre(joao, ana, 1500).
transacao_entre(ana, carlos, 800).
transacao_entre(carlos, daniel, 50).

% 2. Histórico de Inadimplência clássico (Alvo)
inadimplente(daniel).

% 3. Regras de Conexão Bidirecional
% O risco se propaga independente de quem enviou ou recebeu o dinheiro.
% O '_' ignora o valor da transação para o cálculo do grau.
conectado(X, Y) :- transacao_entre(X, Y, _).
conectado(X, Y) :- transacao_entre(Y, X, _).

% ==============================================================================
% 4. Propagação de Risco por Conectividade Recursiva
% ==============================================================================

% A regra principal 'risco_conexao' inicia a busca de caminhos.
% Garantimos que Y é de fato um inadimplente para focar a busca.
risco_conexao(Pessoa, AlvoInadimplente, Grau) :-
    inadimplente(AlvoInadimplente),
    busca_caminho(Pessoa, AlvoInadimplente, [Pessoa], Grau).

% Caso Base da Recursão (Grau 1): 
% A pessoa está diretamente conectada ao inadimplente.
busca_caminho(X, Y, _Visitados, 1) :- 
    conectado(X, Y).

% Passo da Recursão (Grau > 1): 
% A pessoa X está conectada a Z, que por sua vez tem um caminho para Y.
% Usamos a lista "Visitados" para evitar entrar em loops infinitos caso 
% existam ciclos no grafo (ex: Joao transfere para Ana, que transfere para Joao).
busca_caminho(X, Y, Visitados, Grau) :-
    conectado(X, Z),
    Z \== Y,                           % Z não é o alvo final
    \+ member(Z, Visitados),           % Z ainda não foi visitado neste caminho
    busca_caminho(Z, Y, [Z|Visitados], GrauAnterior),
    Grau is GrauAnterior + 1.

% ==============================================================================
% OBSERVAÇÃO DIDÁTICA:
% A regra original do slide, sem a proteção de lista de visitados, seria:
%
% risco_conexao_simples(X, Y, 1) :- conectado(X, Y).
% risco_conexao_simples(X, Y, Grau) :-
%     conectado(X, Z),
%     risco_conexao_simples(Z, Y, GrauAnterior),
%     Grau is GrauAnterior + 1.
% ==============================================================================