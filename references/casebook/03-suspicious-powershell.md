# 03 — PowerShell suspeito

**Módulo:** [windows-forensics](../../agents/windows-forensics.md)

## Objetivo
Identificar a finalidade da execução e se obfuscação encobre ação adversarial.

## Hipóteses e sinais
**Adversarial:** Documento ou navegador iniciou script malicioso.

**Alternativa:** Automação de TI usa parâmetros codificados por empacotamento.

**Sinais:** EncodedCommand, pai Office/browser, download ou execução em memória reportada.

## Evidências, fontes e pré-requisitos
Command line original, script disponível, árvore, hash, usuário e change.

Fontes: MS-PROC, MS-NET, MS-SYSMON no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Localizar processo por dispositivo e tempo.
2. Examinar pai/origem e conteúdo sem executar; decodificação apenas como texto.
3. Comparar script/hash com pacote autorizado.
4. Relacionar rede, arquivos e filhos.
5. Buscar outras execuções do mesmo conteúdo no escopo.

## Consulta defensiva e verificação
Q-KQL-01 é candidato documental; não detecta malícia por si. Q-KQL-02 complementa conexões.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Script/hash e ações coincidem com change aprovado, origem e janela.

**MALICIOUS:** Conteúdo e cadeia demonstram ação adversarial; obfuscação isolada é insuficiente.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Command line truncada ou sem script deixa propósito incerto.

Mensagem/documento → PowerShell → filhos/rede; distinguir invocação interativa de job.

## ATT&CK condicionado
- [T1059.001](https://attack.mitre.org/techniques/T1059/001/): Execução adversarial via PowerShell; T1086 não é usado como ID vigente.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor bloqueio/isolamento só se sustentado e aprovado; pedir script/log original quando necessário.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-03: EV-01 (EDR 12:05Z) mostra script codificado; EV-02 (change) e EV-03 (hash de pacote) correspondem ao script/árvore. BENIGN/Low/High, None Observed, Complete no escopo da execução. Sem ações de resposta.
