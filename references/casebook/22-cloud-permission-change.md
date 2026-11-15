# 22 — Permissões cloud alteradas

**Módulo:** [cloud-security](../../agents/cloud-security.md)

## Objetivo
Determinar alcance efetivo de role/policy alterada e uso posterior.

## Hipóteses e sinais
**Adversarial:** Role adicional preserva ou amplia acesso adversarial.

**Alternativa:** Deploy IAM, PIM ou mudança de equipe aprovada.

**Sinais:** Concessão admin, trust externo, nova policy ou herança ampla.

## Evidências, fontes e pré-requisitos
Ator/sessão, target principal, role/policy antes/depois, escopo e aprovação.

Fontes: AWS-CT, MS-AUDIT, AZURE, GCP-AUDIT no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Identificar operação bem-sucedida versus tentativa e escopo do recurso.
2. Comparar diff, trust, herança e condições.
3. Relacionar ator/sessão à aprovação.
4. Buscar uso do privilégio após concessão.
5. Avaliar outros recursos/credenciais vinculados dentro do tenant.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: audit por principal/policy/operação em fonte real; validar nomes/API por provedor antes de escrever query.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Privilégio, principal, escopo e duração correspondem ao change autorizado.

**MALICIOUS:** Concessão adversarial sustentada pelo contexto, diff e/ou uso indevido.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Permissão anexada pode não ser efetiva por boundary/deny; snapshot não mostra histórico.

Sessão → grant/diff → privilégio efetivo → API/data access.

## ATT&CK condicionado
- [T1098.003](https://attack.mitre.org/techniques/T1098/003/): Adição adversarial de roles/permissões cloud.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor reverter grant específico, avaliar workloads dependentes e aprovar; verificar permissão efetiva depois.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-22: EV-01 (audit 13:30Z) e EV-02 (diff) concedem role não autorizada; EV-03 liga acesso indevido. MALICIOUS/High/High, Confirmed, Incomplete sobre recursos acessados. Reversão proposta.
