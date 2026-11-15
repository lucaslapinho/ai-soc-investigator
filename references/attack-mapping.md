# ATT&CK: fontes e condições

Consulta **2026-11-14**, Enterprise, páginas atuais por técnica; não fixamos release global sem prova. Status documental CONFIRMED para identidade/nome dos IDs abaixo, sem comprovação de presença em nenhum incidente real. As condições são propostas locais e constam nos casos. Não aplicar técnica só pela ferramenta ou categoria do alerta.

| ID | Nome conferido | Fonte | Casos |
|---|---|---|---|
| T1003.001 | OS Credential Dumping: LSASS Memory | [MITRE](https://attack.mitre.org/techniques/T1003/001/) | 04 |
| T1021.002 | Remote Services: SMB/Windows Admin Shares | [MITRE](https://attack.mitre.org/techniques/T1021/002/) | 13, 25 |
| T1041 | Exfiltration Over C2 Channel | [MITRE](https://attack.mitre.org/techniques/T1041/) | 14, 25 |
| T1053.003 | Scheduled Task/Job: Cron | [MITRE](https://attack.mitre.org/techniques/T1053/003/) | 02 |
| T1059.001 | Command and Scripting Interpreter: PowerShell | [MITRE](https://attack.mitre.org/techniques/T1059/001/) | 03 |
| T1059.004 | Command and Scripting Interpreter: Unix Shell | [MITRE](https://attack.mitre.org/techniques/T1059/004/) | 02 |
| T1071.001 | Application Layer Protocol: Web Protocols | [MITRE](https://attack.mitre.org/techniques/T1071/001/) | 15 |
| T1071.004 | Application Layer Protocol: DNS | [MITRE](https://attack.mitre.org/techniques/T1071/004/) | 15 |
| T1078.004 | Valid Accounts: Cloud Accounts | [MITRE](https://attack.mitre.org/techniques/T1078/004/) | 08, 09 |
| T1098 | Account Manipulation | [MITRE](https://attack.mitre.org/techniques/T1098/) | 11 |
| T1098.003 | Account Manipulation: Additional Cloud Roles | [MITRE](https://attack.mitre.org/techniques/T1098/003/) | 22 |
| T1110.001 | Brute Force: Password Guessing | [MITRE](https://attack.mitre.org/techniques/T1110/001/) | 07 |
| T1110.003 | Brute Force: Password Spraying | [MITRE](https://attack.mitre.org/techniques/T1110/003/) | 07 |
| T1136.002 | Create Account: Domain Account | [MITRE](https://attack.mitre.org/techniques/T1136/002/) | 12 |
| T1190 | Exploit Public-Facing Application | [MITRE](https://attack.mitre.org/techniques/T1190/) | 18 |
| T1204.002 | User Execution: Malicious File | [MITRE](https://attack.mitre.org/techniques/T1204/002/) | 01 |
| T1213 | Data from Information Repositories | [MITRE](https://attack.mitre.org/techniques/T1213/) | 21 |
| T1218 | System Binary Proxy Execution | [MITRE](https://attack.mitre.org/techniques/T1218/) | 24 |
| T1219.002 | Remote Access Tools: Remote Desktop Software | [MITRE](https://attack.mitre.org/techniques/T1219/002/) | 16 |
| T1484.001 | Domain or Tenant Policy Modification: Group Policy Modification | [MITRE](https://attack.mitre.org/techniques/T1484/001/) | 10 |
| T1486 | Data Encrypted for Impact | [MITRE](https://attack.mitre.org/techniques/T1486/) | 05 |
| T1496 | Resource Hijacking | [MITRE](https://attack.mitre.org/techniques/T1496/) | 19 |
| T1505.003 | Server Software Component: Web Shell | [MITRE](https://attack.mitre.org/techniques/T1505/003/) | 17 |
| T1566.002 | Phishing: Spearphishing Link | [MITRE](https://attack.mitre.org/techniques/T1566/002/) | 06, 25 |
| T1685 | Disable or Modify Tools | [MITRE](https://attack.mitre.org/techniques/T1685/) | 23 |
| T1686.002 | Disable or Modify System Firewall: Network Device Firewall | [MITRE](https://attack.mitre.org/techniques/T1686/002/) | 20 |

Correções da pesquisa: PowerShell usa T1059.001; DNS C2 usa T1071.004 quando comprovado, não T1499. Nesta consulta, páginas correntes de desativação de ferramentas e firewall usam T1685/T1686.002; as antigas URLs T1562.001/T1562.004 não retornaram corpo. Não importar mapeamento histórico silenciosamente. D3FEND apoia escolha de contramedidas, sem relação automática universal com ATT&CK.
