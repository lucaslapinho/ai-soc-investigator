# 08 — Comprometimento Microsoft 365

**Módulo:** [email-phishing](../../agents/email-phishing.md)

## Objetivo
Determinar uso indevido de conta, caixa e aplicações Microsoft 365.

## Hipóteses e sinais
**Adversarial:** Conta válida foi usada para acesso/forwarding/OAuth indevido.

**Alternativa:** Delegação ou regra de negócio autorizada.

**Sinais:** Nova regra de forwarding, consentimento inesperado, downloads ou envio anormal.

## Evidências, fontes e pré-requisitos
Sign-ins, auditoria de caixa/aplicação, regra antes/depois, consentimentos e sessões.

Fontes: MS-APPS, MS-PURVIEW, MS-SIGNIN, MS-GRAPH no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Fixar identidade e escopo dos serviços/licenças.
2. Relacionar sessão a operação auditada em mailbox/SharePoint/app.
3. Revisar regra/delegação/consentimento e proprietário.
4. Comparar destinatários/dados com propósito autorizado.
5. Buscar persistência e outras contas sem assumir retenção completa.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: CloudAppEvents/Purview por conta, operação e janela; confirmar ActionType/campos. Graph incidents fornece contexto, não substitui auditoria.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Regra/consentimento e uso correspondem a aprovação verificável.

**MALICIOUS:** Acesso ou manipulação indevida comprovada e ligada à conta/sessão.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Alguns eventos dependem de licença/conector; sessão aparentemente normal não exclui token roubado.

Email → sessão → regra/OAuth → acesso a dados; separar serviços e IDs.

## ATT&CK condicionado
- [T1078.004](https://attack.mitre.org/techniques/T1078/004/): Conta cloud válida usada adversarialmente.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor revogação, correção de regra/consentimento e revisão de dados acessados; aprovar alvos e preservar evidência antes de remover.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-08: EV-01 (audit 12:15Z) mostra forwarding externo; EV-02 (owner) confirma autorização formal e EV-03 (change) corresponde ao diff. BENIGN/Low/High, None Observed, Complete para essa regra. Sem resposta executada.
