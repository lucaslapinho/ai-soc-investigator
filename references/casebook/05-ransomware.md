# 05 — Ransomware

**Módulo:** [malware-analysis](../../agents/malware-analysis.md)

## Objetivo
Confirmar criptografia adversarial, propagação e prioridade de resposta.

## Hipóteses e sinais
**Adversarial:** Processo está criptografando dados para impacto.

**Alternativa:** Criptografia de negócio, compressão ou migração planejada.

**Sinais:** Alteração massiva, nota de resgate, arquivos ilegíveis, backup afetado.

## Evidências, fontes e pré-requisitos
Processo/arquivo, alterações em amostras, acesso ao dado, serviços afetados e logs de backup.

Fontes: MS-PROC, MS-NET, NIST-IR no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Identificar se dano está ativo e acionar revisão humana prioritária.
2. Correlacionar arquivos alterados ao processo e testar amostras de forma segura.
3. Comparar com job autorizado sem atrasar decisão urgente.
4. Buscar shares/hosts e credenciais usados, preservando escopo.
5. Separar criptografia, indisponibilidade e possível exfiltração.

## Consulta defensiva e verificação
Q-KQL-01 adaptada ao processo observado; roteiro NOT VERIFIED para agregação de arquivos até confirmar tabela/campos. Não usar contagem fixa como prova.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Job autorizado e reversível explica alterações e ausência de dano adversarial.

**MALICIOUS:** Criptografia não autorizada comprovada, especialmente com nota e processo correlacionado.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Ransomware não implica automaticamente exfiltração; volume afetado deve ser medido.

Processo → arquivos/shares → serviço indisponível → backup; rede em análise separada.

## ATT&CK condicionado
- [T1486](https://attack.mitre.org/techniques/T1486/): Criptografia de dados para causar impacto demonstrada.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor contenção emergencial delimitada, preservação e recuperação de backup verificado; autorização e avaliação do serviço antes de executar.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-05: EV-01 (EDR 12:01Z) e EV-02 (arquivos 12:02Z) confirmam criptografia não autorizada em um host. MALICIOUS/Critical/High, Confirmed, Incomplete quanto a shares. Isolamento urgente proposto ao responsável; não executado.
