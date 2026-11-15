# 16 — Acesso remoto não autorizado

**Módulo:** [network-firewall](../../agents/network-firewall.md)

## Objetivo
Determinar uso real, autorização e finalidade de ferramenta remota.

## Hipóteses e sinais
**Adversarial:** Ferramenta de suporte foi abusada para controlar endpoint.

**Alternativa:** Suporte legítimo ou instalação sem uso, ainda que fora da política.

**Sinais:** AnyDesk/TeamViewer/alternativa instalada, sessão externa ou filhos incomuns.

## Evidências, fontes e pré-requisitos
Instalação, processo, sessão/log do produto, usuário, ticket e política aplicável.

Fontes: MS-PROC, MS-NET, FORTINET no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Separar presença da ferramenta e sessão efetiva.
2. Identificar origem, horário, usuário e ações durante sessão.
3. Conferir política/allowlist e solicitação de suporte.
4. Procurar transferência/execução/persistência associadas.
5. Delimitar ativos e tratar violação de política separadamente de comprometimento.

## Consulta defensiva e verificação
Q-KQL-02 e Q-KQL-01 adaptada ao binário observado. Roteiro do log de sessão NOT VERIFIED até obter versão/schema do produto.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Suporte autorizado com alvos e ações coerentes, sem sinais pendentes.

**MALICIOUS:** Uso remoto indevido/adversarial sustentado; ferramenta proibida instalada sozinha não prova invasão.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Domínios de relay e IPs compartilhados não identificam operador.

Ticket → sessão → processo/arquivo → dados e persistência.

## ATT&CK condicionado
- [T1219.002](https://attack.mitre.org/techniques/T1219/002/): Software de desktop remoto usado como canal adversarial.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor encerrar sessão/remover ferramenta conforme política e aprovação; preservar logs antes da desinstalação.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-16: EV-01 (inventário) mostra ferramenta não homologada, sem log de sessão. SUSPICIOUS/Medium/Low, Unknown, Incomplete. Violação de política deve ser tratada; controle remoto indevido ainda não demonstrado.
