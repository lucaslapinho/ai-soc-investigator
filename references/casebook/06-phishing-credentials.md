# 06 — Phishing e roubo de credenciais

**Módulo:** [email-phishing](../../agents/email-phishing.md)

## Objetivo
Separar tentativa de phishing de interação e comprometimento da conta.

## Hipóteses e sinais
**Adversarial:** Mensagem induziu usuário a fornecer credenciais/token.

**Alternativa:** Comunicação legítima ou simulação aprovada; clique foi scanner.

**Sinais:** Domínio semelhante, urgência, link de autenticação, login posterior anômalo.

## Evidências, fontes e pré-requisitos
EML, headers confiáveis, URL defangada, entrega/clique e sign-ins/sessões.

Fontes: MS-EMAIL, MS-SIGNIN, MS-PURVIEW no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Validar remetente efetivo e cadeia Received.
2. Extrair destino e metadados sem abrir URL/anexo ativo.
3. Verificar entrega, clique e identidade do clique.
4. Correlacionar sessão e ações posteriores; não inferir roubo só pelo clique.
5. Buscar destinatários correlatos no tenant.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED para EmailEvents/UrlClickEvents até confirmar campos; Q-KQL-03 auxilia falhas, não comprova comprometimento.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Origem/conteúdo e campanha aprovados com telemetria coerente.

**MALICIOUS:** Engano malicioso comprovado confirma tentativa; conta comprometida exige evidência adicional.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
SPF/DKIM/DMARC pass não garante mensagem legítima; clique automatizado é possível.

Mensagem → interação → sign-in → uso de recurso; ligações devem ter tempo e identidade.

## ATT&CK condicionado
- [T1566.002](https://attack.mitre.org/techniques/T1566/002/): Mensagem de spearphishing contém link malicioso comprovado.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor remoção da mensagem, bloqueio seletivo ou revogação de sessão conforme evidências e aprovação; não enviar aviso automaticamente.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-06: EV-01 (email 12:00Z) confirma link de phishing; EV-02 (entrega) mostra bloqueio antes da caixa. MALICIOUS/Medium/High, None Observed, Complete apenas para entrega. Comprometimento não demonstrado; nenhuma ação executada.
