# Cloud e rede
Fontes AWS-*, AZURE*, GCP-*, FORTINET, CROWDSTRIKE, TENABLE, ORCA, CF-*, IMPERVA e SERVICENOW no [registro](source-register.md).

| Fonte | Uso na investigação | Limite decisivo |
|---|---|---|
| CloudTrail | Ator, ação API, recurso, região e resultado | Event history não contém data events |
| GuardDuty | Finding e contexto de detecção | Streams consumidos não disponibilizam logs brutos automaticamente |
| Azure Activity | Operações de control plane | Não demonstra toda leitura de dados nem todo erro de autenticação |
| Azure resource logs | Operações no recurso | Diagnostic settings, latência/perda e esquema por serviço |
| GCP Audit | Admin Activity e Data Access | Data Access pode estar desabilitado |
| GCP SCC | Finding com serviço de origem | Tier/cobertura/API a conferir; revisão documental parcial |
| FortiGate/FortiAnalyzer | Tráfego, VPN, segurança e mudanças | ADOM, versão, logging e parser |
| CrowdStrike | Telemetria, detections, CQL/streams/FDR | Finalidades distintas, acesso/licença a conferir |
| Tenable | Asset UUID, finding, plugin e observação | Export do ativo e finding podem ter ciclos diferentes |
| Orca | Workload, vulnerabilidade, IAM e exposição | Capacidade de GV cloud documentada, sem provar exploração |
| Cloudflare | Request, ação WAF e RayID | Sampling; RayID requer contexto adicional |
| Imperva | Export de segurança/acesso/auditoria fornecido | Docs inacessíveis: API e campos NOT VERIFIED |

No cloud, separar conta/subscription/projeto, resource ID e namespace Kubernetes. Mudança no IAM exige diff efetivo, ator/sessão, herança e uso posterior. Pod eliminado não significa remediação durável; investigar imagem/controller e identidade.
Na rede, interpretar direção dos bytes pelo sensor. NAT, proxy, VPN, CDN e anycast impedem equivalência simples entre IP e pessoa/host.
Exfiltração exige evidência de saída e natureza/acesso dos dados; tráfego volumoso sozinho pode ser backup.
WAF bloqueando uma requisição não garante proteção do origin por todas as rotas. Relacionar request, backend, processo e arquivo sem executar payload.
