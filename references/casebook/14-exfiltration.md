# 14 — Exfiltração

**Módulo:** [network-firewall](../../agents/network-firewall.md)

## Objetivo
Verificar se dados foram retirados indevidamente e delimitar o que se comprova.

## Hipóteses e sinais
**Adversarial:** Dados sensíveis saíram por canal controlado pelo adversário.

**Alternativa:** Backup, sincronização ou envio autorizado.

**Sinais:** Egress volumoso, arquivo preparado, destino novo e acesso a repositório sensível.

## Evidências, fontes e pré-requisitos
Processo/sessão, bytes/direção, leitura de dados, classificação do conteúdo e destino.

Fontes: PAN-TRAFFIC, MS-NET, MS-PURVIEW, AZURE-DATA no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Validar direção/contagem sem duplicar início/fim.
2. Relacionar leitura/staging com processo e saída.
3. Identificar destino/ownership sem assumir que IP malicioso prova conteúdo.
4. Comparar backup/sync e autorização.
5. Quantificar apenas dados observados e registrar limites.

## Consulta defensiva e verificação
Q-KQL-02 não mede bytes nem conteúdo por si. Roteiro NOT VERIFIED: agregar bytes da fonte real por sessão e confirmar semântica.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Transferência e dados correspondem a fluxo autorizado.

**MALICIOUS:** Saída indevida de dados sustentada por acesso, transporte e contexto.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
TLS e metadados podem impedir confirmar conteúdo; tráfego alto não basta.

Repositório → leitura → staging → processo → destino.

## ATT&CK condicionado
- [T1041](https://attack.mitre.org/techniques/T1041/): Somente quando exfiltração usa canal C2 existente comprovado; outros canais exigem outro mapeamento.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor restringir canal/sessão, preservar logs e acionar responsável por dados; aprovar impacto antes de bloquear.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-14: EV-01 (flow 12:50Z) mostra 2 GB de saída; sem leitura/conteúdo, EV-02 indica janela de backup possível. SUSPICIOUS/High/Low, impacto Unknown, Incomplete. Validar job e destino; exfiltração não confirmada.
