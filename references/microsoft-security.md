# Microsoft
Fontes MS-* no [registro](source-register.md).
| Ambiente | Fontes documentadas | Atenção |
|---|---|---|
| Defender XDR Advanced Hunting | DeviceProcessEvents, DeviceNetworkEvents | Requer MDE e cobertura |
| Defender for Identity | IdentityLogonEvents | Cobertura depende dos serviços/sensores |
| Defender for Office 365 | EmailEvents | Processamento/entrega não equivalem a clique |
| Defender for Cloud Apps | CloudAppEvents | Depende do conector de atividades |
| Sentinel/Log Analytics/Entra | SigninLogs, AuditLogs | Confirmar workspace e ingestão |
| Portal Defender unificado | Pode consultar workspace Sentinel conectado | Presença na mesma UI não torna todas as tabelas nativas |
| Purview | Auditoria de ações sobre recursos | Licença, escopo, retenção e acesso próprios |
| Graph Security v1.0 | GET /security/incidents | Read.All é permissão documentada; papel/consentimento ainda necessários |

Para Graph, usar o conector autorizado existente, paginação nextLink e intervalo limitado; não obter tokens pelo chat. API de incidentes não substitui evidência bruta e não contém por definição todos os logs.
Para identidade, separar sucesso de autenticação, MFA satisfeita por claim, risco, Conditional Access e ação posterior. VPN/proxy, automação e dispositivo conhecido são alternativas a testar, não absolvição automática.
Consultar [KQL](../examples/hunting-kql.md) e [forense](forensic-artifacts.md). Qualquer identificador sem tabela documentada ou schema observado permanece NOT VERIFIED.
