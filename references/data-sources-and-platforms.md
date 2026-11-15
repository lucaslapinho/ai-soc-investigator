# Escolha da fonte
Antes de consultar: identificar produto/versão, tenant, licença, conector, permissões, schema e retenção observados. Registrar fonte ausente sem simular integração.
| Pergunta | Evidência mais direta | Contexto complementar |
|---|---|---|
| Executou? | Processo/artefatos do endpoint | Alerta, hash, sandbox |
| Autenticou/usou a sessão? | Log de identidade e auditoria da ação | Geo/risco/CMDB |
| Houve tráfego? | Flow/PCAP/proxy/EDR | Reputação/NAT/DNS |
| Mudou permissão/configuração? | Audit e diff antes/depois | Ticket e proprietário |
| Houve acesso a dados? | Data plane/auditoria da aplicação | Control plane e postura |
| Existia vulnerabilidade? | Scan/versionamento do ativo | Exposição e advisory |

Defender, Cortex, CrowdStrike e Stellar podem representar o mesmo evento: manter IDs de origem para deduplicar.
Tenable, Orca, Cortex Cloud SPM e Xpanse informam exposição/contexto; finding isolado não comprova exploração.
ServiceNow SIR fornece histórico/CI/autorização quando disponível. Atualizar ticket é ação externa, não requisito de análise.
OCSF/ECS são modelos de normalização; guardar o campo original e versão de mapeamento. O JSON deste pacote é contrato próprio.
Ver [registro documental](source-register.md) antes de afirmar capacidade de produto.
