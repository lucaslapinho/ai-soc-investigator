# Metodologia de 15 passos
Desenho desta Skill inspirado em NIST SP 800-61r3/CSF 2.0 e prática de resposta, não sequência normativa desses documentos. Ver NIST-IR, NIST-CSF e SANS no [registro](source-register.md).

| Passo | Entrada e operação | Artefato/decisão |
|---|---|---|
| 1 Receber | Ler alerta/pedido; limitar tenant e janela | Envelope ou solicitação de export |
| 2 Validar fonte | Verificar sensor, regra, integridade e cobertura | Inventário de fontes/restrições |
| 3 Extrair | Identificar entidades por namespace | ENT-* com evidência de origem |
| 4 Enriquecer | Consultar contexto autorizado e datar reputação | EV-* ou consulta Unavailable |
| 5 Normalizar tempo | Preservar original/UTC, skew e ingestão | Timeline sem ordenação falsa |
| 6 Correlacionar | Comparar chaves estáveis e independência | Arestas com razões/EV-* |
| 7 Formular hipóteses | Explicar malícia e alternativa plausível | Hipóteses testáveis |
| 8 Confrontar | Associar provas pró/contra e ausências | Matriz hipótese/evidência/gap |
| 9 Analisar comportamento | Reconstruir ações; mapear TTP observada | Achados/ATT&CK condicionado |
| 10 Expandir | Buscar entidades e eventos antes/depois | Escopo e cobertura buscada |
| 11 Avaliar impacto | Separar sucesso, dano e exposição | Confirmado/potencial |
| 12 Classificar | Aplicar critérios explícitos | Veredito rastreável |
| 13 Qualificar confiança | Avaliar qualidade/contradições | Confiança, status, gaps |
| 14 Recomendar | Associar ação, risco, alvo e recuperação | Propostas, sem execução implícita |
| 15 Reportar/revisar | Entregar laudo e decisões | Relatório e próximos passos |

Reavaliar hipóteses com evidências novas, preservando motivo de mudança. Encerrar coleta quando perguntas do escopo estiverem respondidas, não quando remediação for concluída. Parar consultas fora do tenant, invasivas ou acima do orçamento. Urgência não deve esperar enriquecimento opcional.
