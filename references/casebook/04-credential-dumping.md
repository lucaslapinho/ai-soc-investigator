# 04 — Credential dumping

**Módulo:** [windows-forensics](../../agents/windows-forensics.md)

## Objetivo
Determinar tentativa ou extração de material de credencial.

## Hipóteses e sinais
**Adversarial:** Processo não autorizado acessou LSASS para extração.

**Alternativa:** EDR, diagnóstico ou backup autorizado acessou processo sensível.

**Sinais:** Alerta de acesso a LSASS, dump criado, processo com privilégio elevado.

## Evidências, fontes e pré-requisitos
Fonte/target do acesso, direitos observados, árvore, arquivo resultante e contexto de autorização.

Fontes: MS-SYSMON, MS-PROC, MS-IDENTITY no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Confirmar origem/alvo do acesso, sem considerar Event 10 prova completa.
2. Verificar assinatura/caminho e função aprovada do originador.
3. Buscar artefato de dump e alerta comportamental independente.
4. Correlacionar autenticações e uso lateral após o evento.
5. Delimitar credenciais potencialmente expostas sem reproduzi-las.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: filtrar registros Sysmon de acesso a processo pelo target observado, host e tempo; schema/parser e GrantedAccess a conferir.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Acesso compatível com componente aprovado e comportamento esperado.

**MALICIOUS:** Evidência de extração/tentativa adversarial sustentada por contexto e artefatos.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Ausência de dump em disco não exclui uso de memória; não coletar senha/token.

Processo privilegiado → acesso LSASS → artefato → sessão lateral.

## ATT&CK condicionado
- [T1003.001](https://attack.mitre.org/techniques/T1003/001/): Acesso à memória LSASS com finalidade de credential dumping sustentada.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Escalonar DFIR, propor isolamento e tratamento de credenciais expostas conforme impacto e aprovação.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-04: EV-01 (Sysmon 12:10Z) registra acesso LSASS por processo desconhecido, sem dump ou origem verificada. SUSPICIOUS/High/Low, impacto Potential, Incomplete. Pedir árvore e arquivo; nenhum reset executado.
