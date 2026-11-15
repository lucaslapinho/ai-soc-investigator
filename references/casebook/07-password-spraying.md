# 07 — Password spraying e brute force

**Módulo:** [identity-active-directory](../../agents/identity-active-directory.md)

## Objetivo
Caracterizar tentativas e verificar se alguma resultou em uso indevido.

## Hipóteses e sinais
**Adversarial:** Origem tenta senhas em várias contas ou muitas combinações na mesma conta.

**Alternativa:** Credencial expirada, app legado, teste autorizado ou NAT.

**Sinais:** Falhas distribuídas por contas, cadência repetida, sucesso posterior.

## Evidências, fontes e pré-requisitos
Logs de autenticação com código/resultado, IP/dispositivo, conta, app e sessão.

Fontes: MS-SIGNIN, MS-IDENTITY no [registro](../source-register.md). Exigir export legível ou conector de leitura autorizado, tenant/janela definidos, schema e cobertura conhecidos; faltas viram gaps. Não presumir licença, logging ou retenção.

## Triagem e hunting
1. Separar códigos de senha incorreta de MFA/CA e outros erros.
2. Agrupar conta/origem/app/intervalo, considerando NAT e automação.
3. Distinguir padrão spraying de password guessing sem conhecer senha tentada.
4. Buscar sucessos e ações da sessão posteriores.
5. Confrontar baseline e testes aprovados.

## Consulta defensiva e verificação
Q-KQL-03 retorna falhas agrupadas. Depois consultar eventos originais e sucessos; não usar ResultType != 0 como sinônimo de senha errada.

Os exemplos Q-KQL estão em [hunting KQL](../../examples/hunting-kql.md); [hunting XQL](../../examples/hunting-xql.md) contém descoberta de schema. Execução em tenant: NOT RUN neste baseline.

## Decisão
**BENIGN:** Falhas explicadas por app/credencial expirada e comportamento esperado dentro da cobertura.

**MALICIOUS:** Tentativas adversariais sustentadas; comprometimento só com sucesso e contexto de uso indevido.

Caso não resolvido: SUSPICIOUS e Incomplete; contradição material/decisão humana: Requires Human Review. Severidade/confiança/impacto independentes segundo [classificação](../../workflows/classification.md).

## Limitações e correlações
Logs geralmente não revelam senhas tentadas; concluir spraying como hipótese se padrão não discriminante.

Falhas → sucesso → sessão → ação; mesma origem pode ser compartilhada.

## ATT&CK condicionado
- [T1110.003](https://attack.mitre.org/techniques/T1110/003/): Padrão sustenta poucas senhas contra muitas contas.
- [T1110.001](https://attack.mitre.org/techniques/T1110/001/): Padrão sustenta tentativa repetida de adivinhar senha de conta.

IDs consultados em 2026-11-14; vínculo ao caso é proposta condicionada à evidência, não classificação automática.

## Recomendações e escalonamento
Priorizar coleta e revisão de controles; não recomendar reset/bloqueio só por falhas sem avaliar contexto/política. Ação requer autorização.

Parar escrita se alvo/tenant/autorização forem incertos; seguir [governança](../../workflows/response-governance.md). Preservar evidência e separar proposta de execução.

## Relatório técnico sintético
SIM-07: EV-01 (sign-ins 12:00–12:10Z) contém 80 falhas em 20 contas atrás de IP compartilhado; sem pesquisa de sucessos. SUSPICIOUS/Medium/Low, Unknown, Incomplete. Verificar códigos e sessões; nenhum bloqueio.
