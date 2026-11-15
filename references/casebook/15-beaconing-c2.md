# 15 — Beaconing e C2

**Módulo:** [network-firewall](../../agents/network-firewall.md)

## Objetivo
Distinguir comunicação adversarial de periodicidade legítima.

## Hipóteses e sinais
**Adversarial:** Processo mantém canal de comando e controle.

**Alternativa:** Health check, atualização, agente de suporte ou sincronização.

**Sinais:** Conexões periódicas, destino raro, domínio incomum e processo sem origem.

## Evidências, fontes e pré-requisitos
Sessões com timestamps, DNS, processo, baseline e reputação datada.

Fontes: MS-NET, PAN-TRAFFIC, CF-RAY no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Calcular intervalos só após deduplicar e avaliar sampling.
2. Correlacionar DNS/destino com processo.
3. Comparar frequência e jitter à função do software.
4. Examinar sinais de comandos/respostas sem assumir conteúdo de TLS.
5. Buscar ativos relacionados por mais de um indicador.

## Consulta defensiva e verificação
Q-KQL-02 como coleta candidata; cálculo de periodicidade por sessão/tempo é roteiro NOT VERIFIED até confirmar schema e completude.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Processo, destino e periodicidade têm função autorizada comprovada.

**MALICIOUS:** Canal adversarial sustentado por comportamento/conteúdo ou contexto robusto; periodicidade isolada não basta.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
CDN/proxy, keepalive e sensor parcial distorcem intervalos.

Processo → DNS → sessões → atividade posterior; reputação independente.

## ATT&CK condicionado
- [T1071.001](https://attack.mitre.org/techniques/T1071/001/): C2 por protocolo web comprovado.
- [T1071.004](https://attack.mitre.org/techniques/T1071/004/): C2 por DNS comprovado; T1499 não descreve C2 DNS.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor bloqueio seletivo/isolamento quando comprovado, com avaliação de domínio/IP compartilhado e aprovação.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-15: EV-01 (rede 12:00–13:00Z) mostra periodicidade; EV-02 (inventário) identifica agente, sem comprovar destino aprovado. SUSPICIOUS/Medium/Medium, Potential, Incomplete. Pedir configuração do agente; nada bloqueado.
