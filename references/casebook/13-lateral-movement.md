# 13 — Movimentação lateral

**Módulo:** [network-firewall](../../agents/network-firewall.md)

## Objetivo
Demonstrar relação entre origem, sessão e ação no destino.

## Hipóteses e sinais
**Adversarial:** Conta comprometida acessou outro host e executou ação.

**Alternativa:** Distribuição de software, administração ou scanner autorizado.

**Sinais:** SMB/admin share, conexões remotas e processo/serviço novo no destino.

## Evidências, fontes e pré-requisitos
Host IDs, autenticações, 5-tupla/NAT, usuário/sessão, processo do destino e change.

Fontes: MS-NET, MS-IDENTITY, MS-PROC, PAN-TRAFFIC no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Fixar origem/destino no intervalo, resolvendo NAT.
2. Correlacionar autenticação aceita no destino com usuário/sessão.
3. Relacionar processo/arquivo/serviço criado e origem.
4. Comparar com administração autorizada.
5. Expandir grafo a destinos adicionais sem fundir IPs reciclados.

## Consulta defensiva e verificação
Q-KQL-02 para pivot de rede; consultas de logon/processo do destino após confirmar schema. Porta aberta/conexão não prova execução.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Ferramenta, executor, destinos e operações correspondem a rollout aprovado.

**MALICIOUS:** Uso indevido de serviço remoto com ação no destino sustentada.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Conexão SMB isolada pode ser acesso comum; PID e logon ID têm escopos locais.

Origem → autenticação → admin share/serviço → processo destino.

## ATT&CK condicionado
- [T1021.002](https://attack.mitre.org/techniques/T1021/002/): Uso adversarial de SMB/admin shares comprovado.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor conter origem/destino confirmados e sessão exposta, avaliando serviços e aprovação individual.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-13: EV-01 (flow 12:45Z) mostra SMB; EV-02 (destino) e EV-03 (processo) ligam conta comprometida à execução indevida. MALICIOUS/High/High, Confirmed, Incomplete na rede restante. Contenção delimitada proposta.
