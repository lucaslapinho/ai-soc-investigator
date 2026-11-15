# SOC AI Investigator — Relatório do Deep Research

**Origem:** resultado textual do Deep Research solicitado em 14/11/2026 para a Skill **SOC AI Investigator**.  
**Tipo de documento:** exportação em Markdown do relatório retornado (não é a Skill nem uma investigação executada).  
**Nota de integridade:** as citações de interface do resultado original foram substituídas por links identificáveis na seção **Fontes referenciadas**. O texto mantém o conteúdo e o grau de desenvolvimento entregues pela pesquisa; trechos incompletos continuam incompletos. **O relatório não contém os 25 casos integralmente desenvolvidos nem um JSON Schema completo e testado.** Exemplos de consultas, campos e mapeamentos ATT&CK são material para verificação, não instruções validadas em tenant.

---

## Sumário Executivo

Esta pesquisa detalhada fundamenta a construção da Skill **SOC AI Investigator** para ChatGPT, atuando como analista SOC virtual sênior. Baseia-se em documentação oficial e referências reconhecidas (NIST, MITRE, fabricantes de segurança), visando integrar sistemas de informação (SIEM/XDR/SOAR) e fornecer investigação de segurança avançada. A plataforma central será o ambiente ChatGPT Work/Codex, com agentes modulares especializados (por exemplo, forense Windows/Linux, rede, identidade, malware, TI). O objetivo é processar alertas e evidências de múltiplas fontes, normalizar e enriquecer os dados, montar linhas do tempo, correlacionar eventos, validar hipóteses e gerar relatórios técnicos. A metodologia segue frameworks NIST 800-61r3 (aliado ao CSF 2.0), MITRE ATT&CK/D3FEND, SANS e FIRST. Espera-se classificar incidentes em **Malicious**, **Benign** ou **Suspicious**, com atributos de severidade, confiança e impacto, conforme o JSON Schema proposto, citando evidências contra/favor e controles recomendados.

## Plataformas e Fontes de Evidência

### Palo Alto Networks Cortex XSIAM/XDR/XSOAR

Plataforma unificada SIEM+XDR+SOAR (AI-driven), integrando dados de endpoints (EDR), firewalls NGFW, cloud, identidade e TI. Usa a **linguagem de consulta XQL** para investigar dados normalizados (Cortex Data Model – XDM) ou conjuntos brutos (ex.: `xdr_data`, registros NGFW). Exemplos de queries XQL incluem busca de usuários ou hosts específicos, operações de arquivos e filtros temporais. Por exemplo, usando o template “Identidade”, é possível filtrar eventos por usuário (e.g. `XDM.SOURCE.USER.USERNAME = "<usuário>"`) e operação. A consulta bruta típica usa pipeline de stages com pipe (`|`):

```
datamodel dataset = xdr_data
  | filter XDRData.SimpleMalwareName = "Trojan.Generic"
  | filter XDRData.Outcome = "succeeded"
  | count
```

*Funcionalidades:* correlação de alertas via causal chains, AI-assistant (Agentic AI) para automação, playbooks, Marketplace de conteúdos.  
*Limitações:* acessos via licenças adequadas (XSIAM/XDR, XSOAR), escopo definido por fontes conectadas.

**Atenção para implementação:** a consulta acima foi apresentada pelo Deep Research como ilustração, **sem comprovação de execução ou aderência ao schema de um tenant**. Verificar a sintaxe e os campos na documentação e no ambiente antes de reutilizar.

Fontes: [Cortex XSIAM](https://cortex-docs.paloaltonetworks.com/cortex-xsiam/learn-about-cortex-xsiam/get-started-cortex-xsiam), [Build XQL Queries](https://cortex-docs.paloaltonetworks.com/cortex-xsiam/reference-and-developer-docs/cortex-agentix-xql/build-xql-queries/how-to-build-xql-queries), [Query Builder Examples](https://cortex-docs.paloaltonetworks.com/cortex-xsiam/detect-investigate-and-respond-to-threats/investigation-and-response/build-xql-queries/query-builder-templates/query-builder-template-examples).

### Microsoft Defender XDR e Microsoft Sentinel

Utiliza o *Advanced Hunting* (Kusto Query Language – KQL) para tabelas como `DeviceProcessEvents`, `DeviceNetworkEvents`, `DeviceFileEvents`, `DeviceLogonEvents` (telemetria EDR), `IdentityLogonEvents`, `SigninLogs` (Entra ID), `AuditLogs`, além de `AlertInfo`/`AlertEvidence`. Por exemplo, `DeviceProcessEvents` registra criação de processos (PID, hashes, linha de comando); `DeviceNetworkEvents` guarda conexões TCP/UDP por processo, inclusive IPs remotos. Permite consultas como:

```kql
DeviceNetworkEvents
| where RemoteIPType == "Public" and InitiatingProcessFileName endswith ".exe"
| project Timestamp, DeviceName, InitiatingProcessFileName, RemoteIP, RemotePort
```

Integrações via *Microsoft Graph Security API* fornecem incidentes e alertas. *Purview Audit* registra acessos a recursos governados. Requer licenciamento e permissões adequadas.

**Atenção para implementação:** tabelas como `SigninLogs` e `AuditLogs` dependem do ambiente de consulta; não pressupor que são tabelas nativas do mesmo esquema Advanced Hunting do Defender. Verificar schema, licença e disponibilidade de cada fonte.

Fontes: [DeviceProcessEvents](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table), [DeviceNetworkEvents](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicenetworkevents-table), [Microsoft Graph — List incidents](https://learn.microsoft.com/en-us/graph/api/security-list-incidents?view=graph-rest-1.0).

### Stellar Cyber Open XDR

Plataforma integradora de NG-SIEM, NDR, UEBA, SOAR e threat intelligence. Coleta telemetria de endpoints, rede e logs de terceiros, aplicando detecção multimodal (IDS, sandbox, ML) tanto na borda quanto no núcleo. Alertas nativos e de terceiros são normalizados; o recurso **Cases** correlaciona alertas relacionados por meio de análise baseada em ativos ou propriedades compartilhadas. Por exemplo, alerta de malware em host e anomalia de tráfego próximas no tempo podem formar um *Case* correlacionado. APIs REST permitem consulta de eventos, hosts e regras customizadas (verificar endpoints, disponibilidade e autorização por versão).

Fonte: [Stellar Cyber — Detection and Correlation Overview (documentação 6.4.x)](https://docs.stellarcyber.ai/prod-docs/6.4.xs/Using/ML/Detection-Correlation-Overview.htm).

### Outras fontes relevantes

- **CrowdStrike Falcon:** telemetria de endpoint e nuvem (processos, rede, arquivos, EDR), consultas via CQL em Next-Gen SIEM, Event Streams e Falcon Data Replicator (FDR). [Developer Center](https://developer.crowdstrike.com/accomplish/stream-and-analyze-data/).
- **Fortinet FortiGate/FortiAnalyzer:** registros de tráfego, ameaças, VPN e políticas. Correlacionar IPs/hosts do firewall com logs de endpoint, observando NAT e retenção.
- **Tenable, Orca Security e Cloud Security:** vulnerabilidades e configurações são contexto de exposição, não comprovação isolada de exploração. Dados podem ter latência.
- **AWS:** CloudTrail (eventos API), CloudWatch Logs/Metrics, GuardDuty (findings) e VPC Flow Logs. GuardDuty analisa fontes como CloudTrail Management Events, VPC Flow Logs e DNS logs. [AWS GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html).
- **Azure:** Activity Log (alterações de recursos), Azure Monitor/Log Analytics e soluções Defender relevantes.
- **Google Cloud:** Cloud Logging e Security Command Center.
- **WAFs/Proxies:** Imperva e Cloudflare WAF geram logs HTTP e de políticas. Para integração Imperva, ver [referência Rapid7](https://docs.rapid7.com/insightidr/imperva/). Para Logpull, ver [Cloudflare](https://developers.cloudflare.com/logs/logpull/requesting-logs/).
- **Identidade:** Windows/Active Directory, Kerberos/NTLM (ex.: IDs 4768 e 4624); Microsoft Entra ID (sign-ins, auditoria, riscos).
- **Endpoints:** Windows Sysmon (eventos de processo/rede/DNS e GUIDs) e Linux auditd/osquery. [Sysmon Events](https://learn.microsoft.com/en-us/windows/security/operating-system-security/sysmon/sysmon-events).
- **Outros dados:** firewall corporativo, VPN, ServiceNow Security Incident Response, MITRE ATT&CK, MISP, OpenCTI e VirusTotal.

Para cada fonte, a Skill deve mapear campos comuns (timestamps em UTC, IPs, hostnames, usuários) para correlação cross-plataforma e preencher lacunas de cobertura. Exemplo: correlacionar `ProcessGUID` do Sysmon com informações de criação de processo de EDR por múltiplos atributos, não somente PID ou nome; vincular UPN de Entra a identidades Windows com comprovação de equivalência.

## Metodologia Investigativa (15 Passos)

A investigação segue princípios NIST SP 800-61 Rev. 3 e SANS adaptados à análise assistida por IA.

1. **Recepção do Alerta:** obter e entender contexto do alerta (origem, tipo, severidade). Confirmar validade preliminar da fonte.
2. **Validação da Fonte:** avaliar confiança, sensor/regra, severidade e qualidade. Identificar enriquecimento inicial.
3. **Extração de Entidades:** normalizar IPs, hostnames, usuários, hashes, URLs, IDs de recursos e contas.
4. **Enriquecimento:** consultar threat intelligence (VirusTotal, CrowdStrike IOC, MISP) e logs externos (DNS histórico, whois) quando disponíveis.
5. **Construção de Timeline:** ordenar eventos relevantes por timestamp, preferencialmente UTC, e preservar horário original.
6. **Correlação de Eventos:** conectar eventos temporais e lógicos, incluindo processos, arquivos, usuários e rede.
7. **Geração de Hipóteses:** formular cenários explicativos testáveis.
8. **Evidências Pró/Contra:** registrar evidências que apoiam e refutam cada hipótese.
9. **Análise Comportamental:** observar TTPs, execução, persistência, movimento lateral e exfiltração; mapear ATT&CK somente com evidência.
10. **Atividades Relacionadas:** pesquisar outros hosts/usuários/sessões e janelas antes/depois do alerta.
11. **Determinação de Escopo/Impacto:** quantificar ativos e usuários afetados e danos observados/potenciais.
12. **Classificação:** concluir MALICIOUS, BENIGN ou SUSPICIOUS com fundamentação.
13. **Confiança e Lacunas:** atribuir confiança Low/Medium/High e explicitar dados faltantes.
14. **Recomendações de Contenção/Remediação:** propor medidas, separadas de execução, e exigir aprovação quando afetarem sistemas.
15. **Relatório e Aprovação:** gerar relatório técnico/executivo e identificar decisões humanas necessárias.

Nenhuma conclusão ou ação operacional deve ser inventada ou tomada automaticamente sem confirmação; os passos devem ser rastreáveis. Referência: [NIST SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final).

## Agentes Modulares Especializados

Propõe-se arquitetura multiagente com orquestrador e especialistas:

- **SOC Investigation Orchestrator:** recebe alerta; seleciona especialistas pelo tipo de incidente, OS e telemetria; agrega evidências e detecta contradições; consolida laudo.
- **Windows Forensics Investigator:** logs Sysmon/Event e EDR; PowerShell, processos, serviços, arquivos, persistência, artefatos forenses. Escalar amostras complexas e necessidade de coleta volátil ao DFIR humano.
- **Linux Forensics Investigator:** auditd, syslog/journald, SSH, sudo, cron e systemd; processos, alterações e persistência.
- **Network & Firewall Investigator:** Palo Alto NGFW, FortiGate, VPN, proxy, NDR, IDS/IPS; possível C2, tráfego lateral e exfiltração; verificar contexto NAT e visibilidade TLS.
- **Identity & Active Directory Investigator:** Entra ID e AD; anomalias de login, GPO, ACL, criação de contas, brute force/spraying, abuso de privilégio.
- **Malware Analysis Investigator:** hash/amostra, EDR, WildFire e TI; comportamento, execução, persistência e indicadores; encaminhar reversão e análise dinâmica ao especialista e sandbox autorizada.
- **Cloud Security Investigator:** AWS, Azure e GCP; log de controle, IAM, workloads, exposição e dados; investigar alterações e recomendações de revogação de credenciais conforme aprovação.
- **Email & Phishing Investigator:** headers, SPF/DKIM/DMARC, URLs, anexos, Defender for Office 365, correlação com sign-ins, phishing e BEC.
- **Threat Intelligence Investigator:** reputação, IOCs, campanhas, contexto de TTP e hunting, com limites de confiança e validade temporal.

Cada especialista recebe evidências com IDs, produz conclusões parciais com provas referenciadas e pode pedir handoff ao próximo agente. O orquestrador gerencia precedência e preserva a cadeia de custódia.

## Casos de Uso Operacionais (Resumo Original)

**Importante:** o resultado do Deep Research resumiu apenas dez cenários; os demais quinze foram mencionados como tarefa a desenvolver. Não considerar o catálogo de 25 implementado.

1. **Malware em Windows:** detecção de Trojan por EDR; consultar `DeviceFileEvents` e `DeviceProcessEvents`, hashes, processos filhos e serviços; investigar falso positivo; ATT&CK T1059/T1547 quando houver evidência; recomendar isolamento sujeito a aprovação; timeline.
2. **Malware em Linux:** processo inusitado/crontab; auditd, cron e rede; YARA quando autorizado; examinar cron/SSH; resposta proposta: revogar chaves e restaurar com aprovação. **Nota:** o relatório original associa T1499 a “C2 via DNS”, mapeamento que exige correção antes de uso.
3. **PowerShell suspeito:** `DeviceProcessEvents | where ProcessCommandLine contains "powershell"`; verificar origem, árvore e script interno autorizado; ATT&CK PowerShell deve ser revisado para técnica vigente antes de uso (o relatório trouxe T1086, ID histórico).
4. **Credential Dumping:** alerta de acesso à memória de LSASS, Sysmon Event ID 10 e evidências EDR; corroborar com contexto de origem/assinatura; ATT&CK T1003. **Nota:** XQL com `EventID`/`TargetImage` no texto original não foi validada e não deve ser copiada como pronta.
5. **Ransomware:** criptografia de arquivos, sinais EDR, alterações em volumes e backups; ATT&CK T1486; considerar isolamento e recuperação mediante aprovação.
6. **Phishing/Roubo de Credenciais:** mensagens, links, alertas Office 365, sign-ins, tokens; ATT&CK T1566.002 quando comprovado; investigar comprometimento e propor revogação de sessão com autorização.
7. **Password Spraying/Brute Force:** múltiplas falhas no Entra ID/AD, distribuição por contas e IPs; distinguir spraying de brute force; ATT&CK subtechnique a confirmar segundo padrão observado.
8. **Comprometimento Microsoft 365:** SharePoint, sessões, OAuth, atividades auditadas; ATT&CK T1078 quando houver uso de conta válida; avaliar revogação de sessões.
9. **Login Incomum Entra ID:** geolocalização, device, conditional access, risco, autenticação e contexto VPN; evitar sintaxes fictícias como `Location != "usual"`; ATT&CK T1078 somente se sustentado.
10. **GPO Alterado/Excluído:** alterações em políticas, logs de Directory Service e auditoria AD, executor e objeto; ATT&CK T1484 quando houver evidência; revisar IDs de evento (o relatório associou incorretamente 4732 diretamente à exclusão de GPO).
11–25. **Não desenvolvidos na pesquisa original** — o texto fornecido dizia: “... (e assim por diante até 25 casos, seguindo cada cenário listado pelo usuário, incorporando técnicas e consultas específicas em XQL/KQL.)”.

O relatório usou um exemplo de beaconing/C2 com dataset hipotético `panw_ngfw_threat_raw`; esse nome e campos **não foram verificados** e não devem ser assumidos na Skill.

## Correlação e Evidências

A Skill deve normalizar timestamps em UTC e harmonizar identidades sem concluir equivalência indevida (AD ↔ Entra UPN). Hostnames podem ter aliases e IPs podem mapear múltiplos hosts por NAT; usar identificadores estáveis e janelas temporais. Correlacionar hash de arquivo no XDR com relatórios de WildFire e registros de execução. Agrupar eventos antes/depois do alerta, registrar evidências contraditórias e lacunas de fonte. Distinguir observação direta de inferência. Deduplicar o mesmo evento quando representado em diferentes ferramentas e reavaliar hipóteses com novas provas.

## Classificação e JSON Schema (Proposta Original)

Saída estável desejada:

- ID do incidente, tipo (`malware/windows`, `phishing` etc.).
- `classification`: `MALICIOUS`, `BENIGN`, `SUSPICIOUS`.
- `severity`: `Informational`, `Low`, `Medium`, `High`, `Critical`.
- `confidence`: `Low`, `Medium`, `High`.
- `justification`, evidências pró/contra, fontes originais.
- Entidades, timeline, técnicas ATT&CK, escopo/impacto, lacunas, ações recomendadas, aprovação humana e próximos passos.

**Exemplo parcial apresentado pelo Deep Research** (não validado por schema; strings, nomes e conteúdo são sintéticos e exigem revisão antes de reutilização):

```json
{
  "id": "INC1234",
  "type": "ransomware_windows",
  "classification": "Malicious",
  "severity": "High",
  "confidence": "Medium",
  "justification": "Presença de executável malicioso e conexões a servidor C2 documentado.",
  "evidence": {
    "for": [
      "Processo 'evil.exe' detectado por EDR (SHA256 abc123)...",
      "Comunicação TCP para IP malicioso (VirusTotal+)"
    ],
    "against": ["Comando inicial era obfuscado, não há assinatura digital verificada."]
  },
  "entities": {
    "hosts": ["WIN-01.domain.local"],
    "ips": ["192.0.2.5"],
    "users": ["CORP\\joao"],
    "files": ["evil.exe"]
  },
  "timeline": [
    {"time": "2025-11-14T10:05Z", "event": "Malware executado em WIN-01"},
    {"time": "2025-11-14T10:06Z", "event": "Beacon DNS para domain.com"}
  ],
  "attack_techniques": ["T1486", "T1071.001"],
  "scope": "1 host (Confirmed)",
  "impact": "Encrypted several user files",
  "gaps": "Sem logs de rede do exterior para complementar.",
  "recommendations": ["Isolate WIN-01 from rede", "Restaurar de backup", "Bloquear hash abc123"],
  "human_approval": true
}
```

O resultado original explicitou que “o JSON deve ser validado contra o schema proposto”, mas **não forneceu o schema**. A Skill precisará criar seu próprio contrato validável, coerente com enums normalizados.

## IA e Prompts de Agentes

Para cada agente, usar prompts estruturados: papel, objetivo, contexto, variáveis de entrada, regras/metodologia, restrições, saída estruturada e critérios de qualidade. Considerar tool calling, RAG, context engineering, consistência e resistência a prompt injection em logs/e-mails. Não concluir malware simplesmente porque uma ferramenta classificou um arquivo como suspeito; exigir evidências proporcionais. Distinguir variáveis de entradas da Skill da sintaxe contextual do Cortex XSIAM, por exemplo `${issue}`.

## Integração com ChatGPT Work/Codex

Fluxo desejado: analista solicita tipo de investigação; fornece ID ou evidências anexadas; sistema prepara plano e acompanha investigação em etapas, usando recursos do chat e ferramentas conectadas quando disponíveis; entrega classificações e relatórios, exigindo aprovação humana antes de ações críticas. O relatório de pesquisa propõe recursos interativos, mas não demonstrou implementação nem conformidade de cada componente com as capacidades atuais de Work/Codex; essas afirmações dependem de validação específica do ambiente de destino.

## Segurança e Permissões

A Skill é **read-only por padrão**. Bloqueio de IP/usuário, isolamento de endpoint, revogação de sessão, quarentena, políticas de firewall e remediações requerem autorização explícita, escopo e verificações. Segregar tenants, aplicar least privilege, preservar cadeia de custódia, proteger dados sensíveis e evitar prompt injection. Em timeout de ação externa, verificar o estado antes de repetir — falha de retorno não comprova ausência de efeito.

## Relatórios

**Técnico SOC:** alerta original, entidades, timeline, evidências, comportamento, confiança, ATT&CK, escopo/impacto, ações comprovadas, recomendações e pendências.

**Executivo:** riscos ao negócio, impacto observado/potencial, status e decisões necessárias.

**SOAR JSON:** campos estáveis, evidências rastreáveis, recomendações interpretáveis e revisão humana, conforme schema a implementar.

## Arquitetura da Skill

Proposta de distribuição em recursos sob demanda:

- `SKILL.md` com frontmatter YAML `name`/`description`, gatilhos e procedimento.
- `agents/`: orquestrador e especialistas Windows, Linux, identidade, malware, rede/firewall, cloud, email/phishing e threat intelligence.
- `references/`: metodologia e fichas de fontes (Cortex XSIAM, Microsoft Defender, Stellar Cyber, cloud, forense, ATT&CK).
- `workflows/`: triagem, correlação, classificação e resposta.
- `schemas/incident.schema.json`: JSON Schema real a desenvolver e testar.
- `templates/`: prompts e relatórios.
- `examples/` ou `queries/`: consultas verificadas com escopo explícito.

A distribuição deve usar menor árvore suficiente e carregamento progressivo. Esta arquitetura é recomendação, não evidência de instalação.

## Estratégia de Avaliação (Evals)

Preparar fixtures sintéticas com eventos benignos, maliciosos e ambíguos, evidências conflitantes, ausência de telemetria, várias plataformas, prompt injection e avaliações de classificação/correlação. Medir precision/recall quando houver dataset suficiente, falsos positivos/negativos, fundamentação, completude e validade de JSON Schema. Separar revisão estrutural, aderência documental, ativação/comportamento, carregamento/importação e execução. Identificar `PASS`, `FAIL`, `NOT RUN` e `N/A` com evidência; não alegar testes inexistentes.

## Bibliografia e Fontes Referenciadas

Os links abaixo foram extraídos das referências apresentadas pelo Deep Research. **A inclusão de um link não equivale a uma revalidação técnica independente nesta exportação.** A pesquisa não registrou datas específicas de publicação para cada página; a consulta ocorreu no contexto da pesquisa de 14/11/2026.

1. Palo Alto Networks — [Get Started with Cortex XSIAM](https://cortex-docs.paloaltonetworks.com/cortex-xsiam/learn-about-cortex-xsiam/get-started-cortex-xsiam).
2. Palo Alto Networks — [How to Build XQL Queries](https://cortex-docs.paloaltonetworks.com/cortex-xsiam/reference-and-developer-docs/cortex-agentix-xql/build-xql-queries/how-to-build-xql-queries).
3. Palo Alto Networks — [Query Builder Template Examples](https://cortex-docs.paloaltonetworks.com/cortex-xsiam/detect-investigate-and-respond-to-threats/investigation-and-response/build-xql-queries/query-builder-templates/query-builder-template-examples).
4. Palo Alto Networks — [XQL Query Language (Data Security)](https://cortex-docs.paloaltonetworks.com/data-security-documentation/advanced-tools/xql-query-language).
5. Microsoft Learn — [DeviceProcessEvents](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table).
6. Microsoft Learn — [DeviceNetworkEvents](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-devicenetworkevents-table).
7. Microsoft Learn — [Microsoft Graph Security — List incidents](https://learn.microsoft.com/en-us/graph/api/security-list-incidents?view=graph-rest-1.0).
8. Stellar Cyber — [Detection and Correlation Overview (6.4.x)](https://docs.stellarcyber.ai/prod-docs/6.4.xs/Using/ML/Detection-Correlation-Overview.htm).
9. CrowdStrike — [Stream & Analyze Data](https://developer.crowdstrike.com/accomplish/stream-and-analyze-data/).
10. AWS — [What is Amazon GuardDuty?](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html).
11. Rapid7 — [Imperva WAF integration guide](https://docs.rapid7.com/insightidr/imperva/) (fonte de integração, não documentação oficial Imperva).
12. Cloudflare — [Requesting Logs](https://developers.cloudflare.com/logs/logpull/requesting-logs/).
13. Microsoft Learn — [Sysmon events](https://learn.microsoft.com/en-us/windows/security/operating-system-security/sysmon/sysmon-events).
14. NIST — [SP 800-61 Rev. 3](https://csrc.nist.gov/pubs/sp/800/61/r3/final).

## Conclusão do Relatório e Lacunas para a Implementação

A pesquisa propõe um arcabouço para investigação SOC assistida por IA, reunindo tecnologias, metodologia, especialidades, classificação e formatos de saída. **Para sustentar uma Skill utilizável, o desenvolvimento deve completar a validação técnica das consultas, os 25 casos de uso, o JSON Schema validável e os testes**. Nada neste relatório comprova execução em tenants de fornecedores, importação de plugin ou ações operacionais externas.
