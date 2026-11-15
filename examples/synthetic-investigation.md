# Investigação sintética
Este walkthrough usa exclusivamente o cenário de [incident-example.json](../schemas/incident-example.json). Nenhum comando foi executado em tenant.
1. A entrada contém dois relatos fictícios: processo criptografando arquivos e verificação de indisponibilidade no mesmo endpoint.
2. O orquestrador seleciona Windows/malware e caso 05. Registra as fontes como fornecidas e a consulta de expansão como Unavailable.
3. As evidências sustentam MALICIOUS com confiança High para a ação, impacto Confirmed e severidade High porque o cenário não confirma serviço essencial afetado.
4. O escopo permanece Incomplete; alta confiança no comportamento não resolve outros hosts/shares.
5. Isolamento é Proposed: approval/executor/execution null. O JSON não declara que a máquina foi isolada.
6. Coleta, timestamps e dano pertencem à fixture. Não transformar este exemplo em incidente real.

Para validar estrutura e invariantes: ler o script e executar python scripts/validate_incident.py schemas/incident-example.json. Aprovação e autenticidade da evidência dependem do processo humano/ambiente.
