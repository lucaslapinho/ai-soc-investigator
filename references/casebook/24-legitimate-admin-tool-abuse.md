# 24 — Abuso de ferramentas administrativas legítimas

**Módulo:** [windows-forensics](../../agents/windows-forensics.md)

## Objetivo
Determinar finalidade de execução de binário legítimo no contexto.

## Hipóteses e sinais
**Adversarial:** Binário confiável intermedeia execução de conteúdo malicioso.

**Alternativa:** Administração, instalador ou manutenção legítimos.

**Sinais:** Pai incomum, parâmetros/arquivo remoto, payload e ação posterior.

## Evidências, fontes e pré-requisitos
Árvore, command line, assinatura, arquivo alvo/hash, change e rede.

Fontes: MS-PROC, MS-NET, MS-SYSMON no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Verificar binário/caminho e assinatura sem usar como absolvição.
2. Examinar argumentos/arquivo processado sem executar.
3. Correlacionar pai, conteúdo e resultado.
4. Comparar administração autorizada e frequência.
5. Buscar mesmo padrão em outros ativos delimitados.

## Consulta defensiva e verificação
Q-KQL-01 adaptada ao binário observado e Q-KQL-02; assinatura e basename não são regra de veredito.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Argumentos, payload, executor e resultado correspondem a tarefa autorizada.

**MALICIOUS:** Proxy execution de conteúdo adversarial comprovada; uso de ferramenta admin não implica abuso.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Parâmetros truncados ou arquivo ausente deixam intenção aberta.

Pai/origem → binário legítimo → conteúdo/filho → efeito.

## ATT&CK condicionado
- [T1218](https://attack.mitre.org/techniques/T1218/): Somente proxy execution de conteúdo adversarial por binário confiável; outras ferramentas exigem técnica específica.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor contenção do processo/artefato e endurecimento focal com aprovação; evitar bloquear ferramenta corporativa globalmente por nome.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-24: EV-01 (processo 13:40Z) é assinado; EV-02 (arquivo alvo) e EV-03 (filho) demonstram payload adversarial. MALICIOUS/High/High, Confirmed, Incomplete sobre origem. Resposta seletiva proposta.
