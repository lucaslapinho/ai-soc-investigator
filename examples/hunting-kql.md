# KQL — exemplos defensivos
Consulta documental em 2026-11-14. Schema: referências online MS-PROC/MS-NET/MS-SIGNIN, não versão de tenant.
**Documentação:** campos revisados. **Lint local:** somente estrutura textual. **Compilação/execução no tenant: NOT RUN**.
Substituir datas/IDs sintéticos, confirmar schema/permissão/cobertura e registrar filtros. limite take implica coleta parcial, não exaustiva.

## Q-KQL-01 — processos PowerShell (Defender Advanced Hunting)
```kql
DeviceProcessEvents
| where Timestamp >= datetime(2026-11-14T12:00:00Z) and Timestamp < datetime(2026-11-14T13:00:00Z)
| where DeviceId == "synthetic-device-001"
| where FileName in~ ("powershell.exe", "pwsh.exe")
| project Timestamp, DeviceId, DeviceName, FileName, ProcessId, ProcessCommandLine, InitiatingProcessFileName
| order by Timestamp asc
| take 200
```
MS-PROC documenta campos. Retorna candidatos; nome PowerShell não comprova ataque. Para outro processo, alterar apenas o filtro após verificar metadados.

## Q-KQL-02 — conexões do endpoint (Defender Advanced Hunting)
```kql
DeviceNetworkEvents
| where Timestamp >= datetime(2026-11-14T12:00:00Z) and Timestamp < datetime(2026-11-14T13:00:00Z)
| where DeviceId == "synthetic-device-001"
| project Timestamp, DeviceId, DeviceName, RemoteIP, RemotePort, RemoteUrl, InitiatingProcessFileName
| order by Timestamp asc
| take 200
```
MS-NET. Não prova C2 nem exfiltração; correlacionar processo, sessão, resolução DNS e cobertura.

## Q-KQL-03 — falhas por IP e conta (Sentinel/Log Analytics)
```kql
SigninLogs
| where TimeGenerated >= datetime(2026-11-14T12:00:00Z) and TimeGenerated < datetime(2026-11-14T13:00:00Z)
| where ResultType != "0"
| summarize Attempts=count() by IPAddress, UserPrincipalName, bin(TimeGenerated, 5m)
| order by TimeGenerated asc
```
MS-SIGNIN. Não chamar todas as falhas de senha incorreta: revisar códigos/ResultDescription no log original. Padrão distribuído não comprova password spraying sem contexto. Não inferir sucesso/comprometimento dessa consulta; fazer pesquisa separada de sucessos e uso de sessão.
SigninLogs pode estar acessível no portal Defender por workspace Sentinel conectado; nunca presumir tabela AH nativa em todos os ambientes.

## Sem schema conhecido
Definir pergunta → listar fontes visíveis → inspecionar campos/tipos → construir filtro temporal/tenant → retornar amostra limitada → conferir evento bruto → expandir e paginar. Marcar roteiro NOT VERIFIED; não inserir nome de tabela imaginário.
