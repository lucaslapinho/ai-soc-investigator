# 09 — Logon anômalo Entra ID

**Módulo:** [identity-active-directory](../../agents/identity-active-directory.md)

## Objetivo
Validar se sign-in incomum representa acesso indevido ou mudança legítima.

## Hipóteses e sinais
**Adversarial:** Credencial/token foi usado por terceiro.

**Alternativa:** Viagem, VPN, rede móvel ou serviço corporativo.

**Sinais:** País raro, dispositivo novo, risco elevado ou Conditional Access divergente.

## Evidências, fontes e pré-requisitos
Resultado, app, autenticação/MFA, device ID, IP/ASN, sessão e ação posterior.

Fontes: MS-SIGNIN, MS-AUDIT no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Confirmar sucesso real, tipo de sign-in e timestamp.
2. Verificar identidade/dispositivo e evidência de VPN/proxy, sem assumir geolocalização exata.
3. Examinar MFA/CA e contexto da sessão.
4. Correlacionar operações auditadas posteriores.
5. Solicitar confirmação contextual por canal autorizado quando decisivo.

## Consulta defensiva e verificação
Roteiro NOT VERIFIED: SigninLogs por conta/intervalo e campos visíveis; não usar valor inventado como Location='usual'.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** VPN/dispositivo/sessão e propósito confirmados, sem sinais materiais não resolvidos.

**MALICIOUS:** Uso indevido comprovado da conta/sessão; geografia isolada não basta.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
IP/geo e MFA satisfeita não garantem identidade física nem sessão íntegra.

Sign-in → sessão → operação; comparar baseline e não apenas distância geográfica.

## ATT&CK condicionado
- [T1078.004](https://attack.mitre.org/techniques/T1078/004/): Somente se uso adversarial da conta cloud for sustentado.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Propor revogação/reautenticação se sustentado; avaliar VIP/serviço e autorização. Sem prova, coletar antes de responder.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-09: EV-01 (sign-in 12:20Z) é de país incomum; EV-02 (VPN corporativa) explica origem, mas dispositivo não foi validado. SUSPICIOUS/Medium/Medium, Unknown, Incomplete. Pedir vínculo do device; sem revogação.
