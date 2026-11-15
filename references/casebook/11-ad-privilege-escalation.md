# 11 — Escalação de privilégio AD

**Módulo:** [identity-active-directory](../../agents/identity-active-directory.md)

## Objetivo
Determinar alteração de permissões e exercício indevido de privilégio.

## Hipóteses e sinais
**Adversarial:** Conta foi manipulada para obter privilégios persistentes.

**Alternativa:** Delegação ou administração planejada.

**Sinais:** ACL/grupo sensível alterado, novo direito efetivo, uso administrativo posterior.

## Evidências, fontes e pré-requisitos
SID do ator/alvo, objeto, ACL/grupo antes/depois, auditoria, sessão e change.

Fontes: MS-DS, MS-IDENTITY no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Fixar objeto/SIDs e distinguir mudança efetiva de tentativa.
2. Comparar ACL/membros antes/depois e herança.
3. Identificar ator/sessão e aprovação delimitada.
4. Procurar exercício do privilégio e outras alterações.
5. Escalonar se afetar domínio/contas críticas.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: audit de alterações de objeto/grupo no schema real, depois autenticações por SID. Não interpretar 4732 como todos os grupos AD.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Delegação autorizada e privilégio efetivo correspondem ao change.

**MALICIOUS:** Privilégio adicional indevido e uso/persistência adversarial sustentados.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Snapshot atual não identifica ator/horário; associação de grupo sem herança avaliada pode exagerar poder.

Alteração → permissão efetiva → logon/ação privilegiada.

## ATT&CK condicionado
- [T1098](https://attack.mitre.org/techniques/T1098/): Manipulação adversarial de conta/permissões sustentada; refinar subtechnique quando houver prova.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor remover privilégio/recuperar baseline após aprovação e verificação de dependências; preservar diff.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-11: EV-01 (audit 12:35Z) e EV-02 (ACL anterior/atual) mostram concessão indevida; EV-03 liga uso privilegiado à mesma sessão. MALICIOUS/High/High, Confirmed, Incomplete quanto a outros objetos. Reversão proposta, não executada.
