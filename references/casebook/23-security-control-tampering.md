# 23 — Adulteração de controles de segurança

**Módulo:** [linux-forensics](../../agents/linux-forensics.md)

## Objetivo
Separar falha operacional de alteração deliberada de controles.

## Hipóteses e sinais
**Adversarial:** Ator desativou sensor/logging para reduzir visibilidade.

**Alternativa:** Upgrade, falha de rede, manutenção ou erro de ingestão.

**Sinais:** Sensor offline, serviço parado, regra excluída ou logging alterado.

## Evidências, fontes e pré-requisitos
Heartbeat antes/depois, processo/audit, mudança de config, pipeline e ticket.

Fontes: AUDITD, MS-SYSMON, AZURE, AWS-CT no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Validar se falta é no sensor, transporte ou ingestão.
2. Correlacionar último evento com ação de serviço/config e executor.
3. Comparar maintenance/change e abrangência da falha.
4. Buscar ações posteriores por fonte independente.
5. Documentar intervalo cego e não concluir ausência de ataque.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: audit de serviço/config e heartbeat do produto; campos e períodos conforme schema observado.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Falha/manutenção autorizada explica duração, alvo e restauração.

**MALICIOUS:** Desativação/degradação adversarial sustentada por ação e contexto.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Ausência de heartbeat sozinha não prova adulteração; reinstalação pode destruir evidência.

Ator → mudança do controle → gap → atividade em fonte independente.

## ATT&CK condicionado
- [T1685](https://attack.mitre.org/techniques/T1685/): Desativação/modificação adversarial de ferramenta de segurança, ID atual.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor restaurar controle e preservar logs por canal alternativo, com owner/aprovação; avaliar contenção se ataque ativo.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-23: EV-01 (heartbeat) cessa 13:35Z; EV-02 mostra perda de conectividade geral, sem mudança de serviço. SUSPICIOUS/Medium/Low, Unknown, Incomplete. Investigar transporte; não declarar tampering confirmado.
