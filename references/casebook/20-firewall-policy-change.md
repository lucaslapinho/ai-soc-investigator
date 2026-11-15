# 20 — Políticas de firewall alteradas

**Módulo:** [network-firewall](../../agents/network-firewall.md)

## Objetivo
Verificar executor, versão efetiva e mudança de exposição.

## Hipóteses e sinais
**Adversarial:** Policy foi alterada para permitir caminho adversarial.

**Alternativa:** Change emergencial aprovado ou correção planejada.

**Sinais:** Regra permissiva, logging desabilitado, admin inesperado ou push fora da janela.

## Evidências, fontes e pré-requisitos
Audit/config logs, antes/depois, commit/job, alvo/serial/vsys e ticket.

Fontes: PAN-CONFIG, PAN-TRAFFIC, FORTINET no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Separar config candidata, commit e aplicação no dispositivo.
2. Extrair autor, sessão, regra/objeto e diff.
3. Comparar change exato, horário e escopo.
4. Analisar tráfego permitido pelo novo estado.
5. Verificar outros dispositivos/HA sem presumir que push foi uniforme.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: filtrar audit por rule ID/commit no schema real e correlacionar logs de tráfego; não fornecer comando de alteração.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Diff e aplicação correspondem a autorização e finalidade verificáveis.

**MALICIOUS:** Enfraquecimento deliberado de firewall e uso adversarial sustentados.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Commit no Panorama não prova aplicação em todos os firewalls; estado parcial requer revisão.

Login admin → diff → commit/push → rule hit → sessão.

## ATT&CK condicionado
- [T1686.002](https://attack.mitre.org/techniques/T1686/002/): Alteração adversarial de firewall de dispositivo de rede; fonte atual verificada.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor rollback da mudança precisa após avaliação de dependências e aprovação; verificar config efetiva e tráfego após ação.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-20: EV-01 (config 13:20Z) mostra regra alterada; commit aceito, push sem estado final. SUSPICIOUS/High/Medium, Potential, Requires Human Review. Verificar job/dispositivo antes de rollback ou retry.
