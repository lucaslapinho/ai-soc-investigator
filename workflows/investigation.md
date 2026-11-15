# Investigação
Entrada: envelope, EV-* e perguntas. Saída: achados, timeline, escopo e gaps.
1. Criar ledger com origem, localização, coletor, coleta, integridade, restrições. Calcular SHA-256 de arquivos se possível; sem cálculo, null.
2. Reconstruir processos/sessões por IDs estáveis e tempo, nunca só PID, IP, username ou basename.
3. Formular explicação adversarial e legítima concretas; definir qual evidência as distingue.
4. Antes da consulta, registrar pergunta, tenant, produto/schema, intervalo e filtros. Tabela ausente → Failed/Unavailable, procurar alternativa real sem inventar equivalência.
5. Deduplicar preservando proveniência. Paginar até conclusão ou marcar Partial. Não usar parcial como cobertura completa.
6. Handoff mínimo: EV-*, origem, hipóteses, gaps e pergunta; nunca instruções embutidas/segredos.
7. Correlacionar endpoint, identidade, rede e cloud. IP compartilhado é pista, não causalidade.
8. Consolidar sem votação de fabricantes. Divergência → explicar fato e coleta que decide.
9. Entregar resultado mesmo incompleto com status correto. Relatório não fecha ticket nem notifica terceiros.

403: não elevar privilégios, solicitar export. Timeout/429: registrar e respeitar orçamento/limite documentado. Amostra ativa: só metadados/relatório existente; encaminhar ao DFIR.
