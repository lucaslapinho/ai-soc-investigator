# 17 — Webshell e aplicações web

**Módulo:** [linux-forensics](../../agents/linux-forensics.md)

## Objetivo
Ligar artefato web a requisição e execução indevida no servidor.

## Hipóteses e sinais
**Adversarial:** Script implantado permite execução remota persistente.

**Alternativa:** Arquivo de aplicação/deploy ou falso positivo WAF.

**Sinais:** Arquivo novo no webroot, processo filho do servidor e request incomum.

## Evidências, fontes e pré-requisitos
Access/error logs, WAF/origin, arquivo/hash, deploy, árvore e usuário de serviço.

Fontes: CF-LOGS, IMPERVA, MS-PROC, AUDITD no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Preservar arquivo sem executar e comparar release/base.
2. Correlacionar requisição com origin por tempo/ID/contexto.
3. Buscar processo/arquivo/rede decorrentes do servidor.
4. Verificar deploy autorizado e uploads previstos.
5. Buscar outros artefatos e o vetor de entrada.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: filtrar URI/tempo/request ID do export real e correlacionar runtime. Não enviar payload nem chamar webshell.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Arquivo corresponde ao deploy e requests/ações são esperados.

**MALICIOUS:** Artefato e execução/controle adversarial comprovados.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
HTTP 200 ou bloqueio WAF isolados não demonstram sucesso/proteção do origin; Ray ID não é único.

Request → origin → worker → shell/arquivo → rede.

## ATT&CK condicionado
- [T1505.003](https://attack.mitre.org/techniques/T1505/003/): Web shell implantada/operante com evidência.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor preservar imagem/logs e restringir aplicação ou isolar workload com owner e aprovação; remover artefato após análise.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-17: EV-01 (origin 13:00Z), EV-02 (arquivo) e EV-03 (runtime) ligam script indevido a shell do worker. MALICIOUS/High/High, Confirmed, Incomplete sobre vetor inicial. Contenção proposta ao owner.
