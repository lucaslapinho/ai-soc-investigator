# Stellar Cyber
A página 6.1.x documenta detecção multimodal e Cases com agrupamento de alertas nativos/terceiros (STELLAR). A URL 6.4.x da pesquisa não ficou acessível (STELLAR-64). Não tratar endpoints/API/campos de outra versão como confirmados.
1. Receber export do Case com tenant, Case ID, alertas membros, sensores e janela.
2. Recuperar evento original de cada alerta; separar normalização, detecção nativa e alerta repassado.
3. Explicar a relação sugerida por ativos/propriedades e testar causalidade.
4. Deduplicar IDs replicados de EDR; validar horário do sensor versus ingestão.
5. Buscar dados antes/depois e registrar cobertura parcial/sensor ausente.
6. Sem API conectada, fornecer filtros de interface com campos observados no export; não inventar query syntax.
Case score ou inclusão no mesmo grafo não confirma campanha. Saída: membros, relações demonstradas, coincidências, gaps e consultas executadas/pendentes.
