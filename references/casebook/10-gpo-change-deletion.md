# 10 — GPO alterada ou excluída

**Módulo:** [identity-active-directory](../../agents/identity-active-directory.md)

## Objetivo
Identificar executor, objeto, mudança e estação de origem sem confundir DC com origem.

## Hipóteses e sinais
**Adversarial:** Alteração/exclusão de GPO enfraqueceu controles sem autorização.

**Alternativa:** Manutenção aprovada ou limpeza de GPO obsoleta.

**Sinais:** 5136/5141 em objeto de política, mudança SYSVOL ou aplicação de política inesperada.

## Evidências, fontes e pré-requisitos
Objeto GUID/DN/classe, sujeito/logon ID, diff/SYSVOL, change e autenticação/endpoint de origem.

Fontes: MS-DS, MS-5141, MS-4732 no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Confirmar classe/DN do GPO; 5141 é exclusão de objeto AD, não prova de GPO sozinho.
2. Extrair sujeito e logon/session ID, preservando DC que registrou.
3. Correlacionar sessão/autenticação com endpoint originador; sem prova, origem Unknown.
4. Comparar diff/SYSVOL e change por horário, objeto e executor.
5. Buscar outras mudanças e impacto nas OUs/hosts.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: selecionar 5136/5141 do dataset real e filtrar classe/DN de GPO; 4732 não serve. Validar parser, SACL e auditoria.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Change aprovado explica objeto/executor/diff/janela e efeitos.

**MALICIOUS:** Mudança indevida com evidência de intenção/efeito adversarial sustentado; sem confirmação contextual manter SUSPICIOUS.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Evento de DC não revela automaticamente IP de origem; SYSVOL/AD podem divergir.

Sujeito/logon → origem → objeto GPO → escopo afetado; não isolar DC como substituto da origem.

## ATT&CK condicionado
- [T1484.001](https://attack.mitre.org/techniques/T1484/001/): Modificação adversarial de Group Policy comprovada.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor revisão SOC/owner e restauração manual controlada; isolamento apenas do endpoint originador comprovado e aprovado.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-10: EV-01 (DC 12:30Z) confirma exclusão de groupPolicyContainer por conta admin. Origem não resolvida e change pendente. SUSPICIOUS/High/Medium, Potential, Requires Human Review. Não isolar o DC; coletar autenticação e aprovação.
