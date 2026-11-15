# Cortex e Palo Alto
Fontes: PAN-XQL, PAN-LIMIT, PAN-XDR, PAN-XSOAR, PAN-TIM, PAN-XPANSE, PAN-CLOUD, PAN-SPM, PAN-TRAFFIC, PAN-CONFIG, PAN-WF no [registro](source-register.md).
- XSIAM/XDR: começar pelo alerta/issue exportado e entidades; consultar dados realmente ingeridos. Manter dataset queries separados do XDM e conferir mapeamento. O exemplo misto da pesquisa não é usado.
- XQL: abrir schema/completion e fixar tempo/tenant antes de consulta. Não presumir dataset de NGFW por nome de fabricante. Ver [exemplo](../examples/hunting-xql.md).
- XSOAR: playbooks/comandos dependem do content pack e instância. Ler integração/saídas instaladas antes de sugerir parâmetros. Esta Skill prepara investigação, não instala playbook.
- TIM: registrar origem, first/last seen, validade, reputação e dependência entre feeds. Reputação não basta para fechar caso.
- Xpanse: usar descoberta de superfície para validar propriedade e exposição, não como prova de execução.
- Cortex Cloud/SPM: correlacionar posture, IAM e recurso com runtime/logs. Não presumir que alerta Cloud já está no XSIAM ou que IDs sejam intercambiáveis.
- NGFW/Panorama: correlacionar serial/vsys, session ID, início/fim e NAT. Evitar somar bytes de início/fim como sessões diferentes. Config candidata, commit no gerenciador e push aplicado no firewall são etapas diferentes; verificar qual é observada.
- WildFire: comparar hash exato, análise, verdict e ação. Relatório de sandbox descreve a sandbox; permitir/bloquear transporte é diferente de execução no endpoint. Não enviar sample automaticamente.
