# 19 — Workload cloud comprometido

**Módulo:** [cloud-security](../../agents/cloud-security.md)

## Objetivo
Confirmar ação indevida no workload e sua relação com identidade/imagem/controlador.

## Hipóteses e sinais
**Adversarial:** Workload foi usado para execução ou consumo de recursos adversarial.

**Alternativa:** Autoscaling, job de processamento ou teste de carga.

**Sinais:** Processo estranho, consumo atípico, imagem alterada e egress raro.

## Evidências, fontes e pré-requisitos
Resource ID, conta/região, pod/container/VM, runtime, IAM e billing contextual.

Fontes: AWS-CT, AWS-GD, AZURE, GCP-AUDIT, ORCA, PAN-CLOUD no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Fixar recurso e ciclo de vida; não confundir pod substituído com saneamento.
2. Correlacionar runtime ao ator/API/imagem.
3. Comparar image digest/deploy/job autorizado.
4. Buscar persistência em role/controller/template.
5. Delimitar dados/credenciais acessíveis e consumo medido.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: filtrar recurso e ator em control plane e runtime; GuardDuty finding não fornece todos os logs usados internamente.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Job/imagem/consumo correspondem ao deploy aprovado.

**MALICIOUS:** Execução/uso indevido comprovados; consumo alto isolado não basta.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Workload efêmero e falta de data events podem limitar reconstrução.

IAM/sessão → API/deploy → workload → egress/controlador.

## ATT&CK condicionado
- [T1496](https://attack.mitre.org/techniques/T1496/): Apropriação de recursos comprovada; não mapear todo comprometimento cloud a resource hijacking.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor conter identidade e workload/controlador corretamente; preservar evidência e aprovar impacto/recriação segura.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-19: EV-01 (runtime 13:10Z) registra minerador indevido e EV-02 vincula ao pod; criação/IAM ausentes. MALICIOUS/High/High, Confirmed, Incomplete. Propor conter workload e investigar controlador; nada executado.
