# Artefatos forenses
Fontes MS-SYSMON, MS-DS, MS-5141, MS-4732, AUDITD e OSQUERY no [registro](source-register.md).

Windows: correlacionar processo e pai por GUID/ID e dispositivo; PID requer criação/boot. Sysmon 1 (processo), 3 (rede, depende de configuração) e 10 (acesso a processo) são pistas: acesso a LSASS não implica dump consumado. Usar command line/EDR/arquivo resultante e alternativa de software autorizado.
GPO: 5136 altera objeto AD; 5141 exclui objeto AD; verificar classe/DN/GUID do GPO e SYSVOL. 4732 é adição a grupo local de segurança, não exclusão de GPO. DC que gerou o evento não é automaticamente estação de origem. Correlacionar sujeito/logon/sessão com autenticação e telemetria de origem; se não houver, origem Unknown.
Artefatos persistentes (serviços, tarefas, autoruns, MFT/USN, Prefetch/Amcache) exigem contexto da versão e configuração. Presença de arquivo/entrada não prova execução, e ausência não a refuta. Encaminhar imagem/memória ao DFIR com cadeia de custódia apropriada.

Linux: preservar audit/journal/auth/SSH, boot ID, UID/AUID, sessão, processo e inode/caminho quando disponíveis. Eventos audit têm registros componentes; agrupar pelo identificador do evento e host, não interpretar cada SYSCALL/EXECVE/PATH como ação independente. Shell history é incompleto e alterável.
Cron/systemd e authorized_keys devem ser comparados a baseline/autorização. Containers requerem correlação host/pod/container e ciclo de vida.
osquery: snapshot de processes não reconstitui processos terminados. Process/socket events precisam estar habilitados previamente; considerar perda/throttling/conflito com Audit. Não desligar auditd ou alterar coleta durante investigação por recomendação genérica.
Coleta volátil e imagem podem alterar estado/carga; ficam como proposta delimitada a equipe autorizada.
