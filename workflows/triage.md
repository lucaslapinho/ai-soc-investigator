# Triagem
Entrada: alerta/export/ID, pedido e fontes autorizadas. Saída: envelope do caso.
1. Confirmar tenant antes de consultar ferramentas. Aceitar alias. Sem tenant, marcar Unknown, analisar o arquivo isoladamente e impedir consultas/cruzamentos.
2. Registrar ID original, produto, detecção, severidade da fonte e coleta. Não adotar automaticamente o veredito da fonte.
3. Preservar horário original e timezone; UTC null se desconhecido. Não assumir fuso do analista.
4. Extrair UPN/SID/object ID, endpoint ID/host, IP, processo, sessão, URL, hash e resource ID com namespace.
5. Registrar cobertura: sensores, retenção, janela, filtros, atraso, permissões, paginação. Conector listado não prova acesso.
6. Propor janela inicial ±30 minutos como convenção ajustável; ampliar por evidências e dentro do orçamento. Não declarar ausência fora da cobertura.
7. Priorizar revisão humana se houver criptografia ativa, privilégio alto, propagação ou dados sensíveis.
8. Selecionar módulo/caso e continuar leituras autorizadas sem confirmação repetitiva.
ID sem acesso → pedir export e entregar plano. Arquivo ilegível → indicar parte inacessível. Multi-tenant ambíguo → separar e parar correlação. Contradição → preservar ambas as fontes.
