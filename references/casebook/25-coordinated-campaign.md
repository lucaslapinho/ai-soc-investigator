# 25 — Campanha coordenada multiativos

**Módulo:** [soc-orchestrator](../../agents/soc-orchestrator.md)

## Objetivo
Verificar se eventos compõem cadeia comum e delimitar membros confirmados/potenciais.

## Hipóteses e sinais
**Adversarial:** Múltiplos ativos integram campanha com causalidade ou infraestrutura específica.

**Alternativa:** Coincidência, feed duplicado, CDN compartilhada ou rollout legítimo.

**Sinais:** Alertas semelhantes em hosts/contas, indicadores repetidos e sequência temporal coerente.

## Evidências, fontes e pré-requisitos
Ledgers por ativo, fontes originais, tempo normalizado, relações e baseline de mudança.

Fontes: NIST-IR, STELLAR, MS-HUNT, PAN-XQL no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Separar tenants; autorização de um cliente não libera outro.
2. Deduplicar alertas e identificar independência de fontes.
3. Construir grafo com arestas observadas/inferidas, por pelo menos evidências discriminantes.
4. Testar rollout/CDN e incompatibilidades temporais.
5. Consolidar subcasos e impacto sem somar vítimas potenciais como confirmadas.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: pivots em queries reais por hashes/sessões/recursos, preservando tempo e tenant; não agrupar por IP público sozinho.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Distribuição/eventos correspondem a operação legítima, com relações resolvidas.

**MALICIOUS:** Cadeia adversarial entre ativos sustentada; similaridade isolada permanece suspeita.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Feeds compartilhados e clock skew exageram correlação; sem relação causal, manter subcasos separados.

Grafo por EV-*, com origem, relação, natureza e alternativas em cada aresta.

## ATT&CK condicionado
- [T1566.002](https://attack.mitre.org/techniques/T1566/002/): Somente no subevento de phishing comprovado.
- [T1021.002](https://attack.mitre.org/techniques/T1021/002/): Somente no subevento SMB adversarial comprovado.
- [T1041](https://attack.mitre.org/techniques/T1041/): Somente no subevento de exfiltração por C2 comprovado.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor plano coordenado por ativos/identidades confirmados com aprovações delimitadas; não executar bloqueio amplo por cluster automático.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-25: EV-01 e EV-02 repetem alerta do mesmo EDR em duas ferramentas; EV-03 é outro host no mesmo NAT. SUSPICIOUS/Medium/Low, Unknown, Incomplete. Uma campanha não foi demonstrada; deduplicar e pedir pivots independentes.
