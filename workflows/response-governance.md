# Governança de resposta
Padrão: analisar e recomendar; nenhum módulo executa resposta por conta própria.

## Gate
Registrar ação, justificativa/EV-*, tenant e ID estável; autorização humana explícita, momento, alcance e validade; conector/privilégios comprovados; VIP/criticidade/proprietário/serviço/janela; pré-condições, impacto, rollback e teste posterior.
Respeitar política VIP do cliente sem universalizar bloquear/não bloquear. Sem política conhecida, obter decisão para ação de impacto. "Investigue" não autoriza bloquear, enviar, fechar ou remediar.

## Estados
Proposed → Approved → Executed, Failed ou Unknown; Rejected encerra proposta. Aprovação não é execução; job aceito não é conclusão. Em timeout, Unknown, verificar alvo/job antes de repetir. Não converter ausência de retorno em Failed.
human_approval_required=true significa exigência de aprovação mesmo já concedida; approval e estado mostram se ocorreu. Sem propostas pode ser false.

## Parada/recuperação
Alvo ambíguo, tenant divergente, privilégio insuficiente, aprovação expirada ou impacto desconhecido → parar escrita e entregar proposta concreta. Depois de executar, ler estado remoto e registrar evidência. Recuperar conforme rollback aprovado; não ampliar alvos. Preservar logs/tickets.
Notificações/atualização/fechamento de ticket e upload de amostra são efeitos externos. Default: preparar conteúdo e consultar relatório existente autorizado.
