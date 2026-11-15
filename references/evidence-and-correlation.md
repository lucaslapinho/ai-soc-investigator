# Evidência e correlação
## Ledger
IDs locais EV-*, SRC-*, ENT-* e Q-* são estáveis. Guardar origem original, localização, coletor, coleta, hash calculado, transformações e restrição. Hash prova igualdade de bytes, não autenticidade. Cadeia de custódia formal exige procedimentos e responsáveis, não apenas hash.

## Tempo
Preservar original_time, original_timezone, time_utc, precision e nota de skew. Converter só com offset/timezone comprovado; caso contrário UTC null. Distinguir evento, ingestão e coleta. UTC termina em Z. Registrar incerteza em vez de corrigir clocks silenciosamente.

| Entidade | Correlação preferida | Limitação |
|---|---|---|
| Endpoint | ID + tenant + intervalo | Reinstalação/hostname reciclado |
| Processo | GUID/ID estável + host | PID requer criação/boot |
| AD/Entra | SID/object ID + namespace | UPN igual não comprova identidade híbrida |
| Rede | 5-tupla + sensor + tempo + NAT | IP público compartilhado |
| Cloud | resource ID + conta + ciclo de vida | Nome reutilizável |
| Email | message ID + destinatário + tenant | Reentregas e cabeçalhos forjáveis |
| HTTP | request ID + serviço + hora | Ray ID não é garantidamente único (CF-RAY) |

Arestas: Observation (chave direta), Inference (compatibilidade limitada), Hypothesis (a provar). Exigir coerência temporal e mais de um atributo quando a chave não for única.
Alertas replicados e feeds compartilhados não são provas independentes. Ação bloqueada não prova execução. Consulta vazia exige cobertura/retencão/ingestão comprovadas para sustentar "não observado".
Evidência contra deve refutar a hipótese; ausência de assinatura não refuta malícia. Não inventar probabilidades calibradas.
Minimizar PII/segredos e respeitar restrições de compartilhamento. Validar requisitos LGPD com responsáveis; não emitir conclusão jurídica. TLP não substitui autorização.
