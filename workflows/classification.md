# Classificação
Objeto: comportamento no escopo do caso, não reputação global da pessoa/máquina.

| Campo/valor | Critério |
|---|---|
| MALICIOUS | Evidência sustenta comportamento adversarial; separar tentativa bloqueada de comprometimento |
| BENIGN | Evidência positiva resolve sinais materiais com explicação legítima e cobertura suficiente |
| SUSPICIOUS | Sinal não resolvido/dados insuficientes; sem evidências, esclarecer que nem o sinal foi confirmado |
| severity | Informational: sem risco material; Low: limitado; Medium: suspeita com impacto limitado; High: dano/acesso relevante ou potencial sensível; Critical: dano grave ativo/propagação ou risco imediato a serviço essencial |
| confidence | High: prova direta confiável e alternativas avaliadas; Medium: corroboração parcial; Low: sinal isolado, baixa origem ou contradição determinante |
| impact.status | Confirmed: dano/acesso indevido demonstrado; Potential: caminho plausível; None Observed: sem impacto na cobertura descrita; Unknown: cobertura insuficiente |
| investigation_status | Complete: perguntas respondidas com limites; Incomplete: dados/coleta pendentes; Requires Human Review: conflito material ou decisão humana necessária |

Ajustar severidade à matriz do cliente. Confiança não é percentual calibrado. SUSPICIOUS nunca Complete nesta versão. BENIGN exige Complete e confiança Medium/High. MALICIOUS pode ser Incomplete quanto ao escopo. High não implica escopo completo.
Phishing bloqueado comprovado pode ser MALICIOUS/None Observed/Complete no escopo de entrega. Processo assinado anômalo não resolvido é SUSPICIOUS/Incomplete. Mudança autorizada deve corresponder a objeto, horário, executor e diff para BENIGN.
CVSS alto, país raro, IOC isolado e falhas de login não confirmam comprometimento. Ausência de malícia observada não basta para BENIGN.
