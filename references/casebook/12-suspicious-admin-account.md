# 12 — Conta administrativa suspeita

**Módulo:** [identity-active-directory](../../agents/identity-active-directory.md)

## Objetivo
Verificar criação, concessão e uso de conta administrativa.

## Hipóteses e sinais
**Adversarial:** Conta nova foi criada para persistência adversarial.

**Alternativa:** Conta de serviço/break-glass com aprovação e controle.

**Sinais:** Conta recente com privilégio elevado, nome semelhante ou origem incomum.

## Evidências, fontes e pré-requisitos
Object ID/SID, criação, executor, grupos/roles, primeiro uso e solicitação aprovada.

Fontes: MS-DS, MS-AUDIT, MS-IDENTITY no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Identificar namespace local/domínio/cloud.
2. Determinar quem criou e concedeu privilégio, com horário e sessão.
3. Conferir owner, propósito, validade e change.
4. Rastrear primeiro uso e recursos acessados.
5. Avaliar contas semelhantes e criação em sequência.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: audit de criação/concessão no produto observado; selecionar por SID/object ID, não só displayName.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Conta, role, prazo e uso conferem com aprovação e owner.

**MALICIOUS:** Criação para persistência ou uso indevido demonstrados; nome incomum sozinho não basta.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Ausência de owner pode ser falha de governança; diferenciar de ataque.

Criação → concessão → login → operação administrativa.

## ATT&CK condicionado
- [T1136.002](https://attack.mitre.org/techniques/T1136/002/): Criação adversarial de conta de domínio; não aplicar a conta cloud/local.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor suspensão/remoção de privilégios com revisão de dependências, criticidade e aprovação.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-12: EV-01 (criação 12:40Z) aponta conta de domínio admin nova, sem owner disponível. SUSPICIOUS/High/Low, Potential, Requires Human Review. Pedir change e uso; nenhuma desativação.
