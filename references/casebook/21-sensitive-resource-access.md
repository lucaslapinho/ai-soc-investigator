# 21 — Acesso indevido a recurso sensível

**Módulo:** [identity-active-directory](../../agents/identity-active-directory.md)

## Objetivo
Comprovar acesso e finalidade, separando autorização técnica e autorização de negócio.

## Hipóteses e sinais
**Adversarial:** Conta acessou dados/repositório sem necessidade ou autorização.

**Alternativa:** Atividade de negócio, backup ou eDiscovery autorizado.

**Sinais:** Consulta/download incomum, ACL ampla, acesso fora de função.

## Evidências, fontes e pré-requisitos
Auditoria de data plane, objeto, principal/sessão, permissão efetiva e contexto do owner.

Fontes: MS-PURVIEW, AZURE-DATA, GCP-AUDIT, AWS-CT no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Identificar dado/recurso e acesso efetivo, não só permissão.
2. Correlacionar principal/sessão e operação/resultados.
3. Comparar necessidade de negócio e aprovação, minimizando conteúdo sensível.
4. Quantificar objetos observados sem extrapolar volumes.
5. Investigar compartilhamento/saída em caso separado.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: audit do serviço por objeto/principal/tempo e resultado. Control plane sozinho não confirma leitura de conteúdo.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Owner/autorização e auditoria demonstram uso compatível.

**MALICIOUS:** Acesso/coleta indevidos demonstrados, sem atribuir motivo apenas pelo cargo.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Logs de dados podem não estar habilitados; ACL ampla é exposição, não acesso comprovado.

Identidade → autorização efetiva → leitura/download → possível saída.

## ATT&CK condicionado
- [T1213](https://attack.mitre.org/techniques/T1213/): Coleta adversarial de informação em repositório comprovada.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor restringir acesso e acionar owner/IR conforme política, sem divulgar conteúdo e com aprovação.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-21: EV-01 (audit 13:25Z) registra download de repositório; finalidade/owner pendentes. SUSPICIOUS/High/Medium, Potential, Requires Human Review. Acesso observado, caráter indevido não confirmado.
