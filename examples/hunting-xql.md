# XQL — descoberta conservadora
Ambiente: Cortex XSIAM/XDR com dataset xdr_data disponível, conforme PAN-XQL/PAN-LIMIT.
Consulta documental 2026-11-14; execução/compilação no tenant **NOT RUN**. Versão: documentos 3.x; confirmar a do cliente.
Configurar na interface tenant e janela restrita antes de executar:

```xql
dataset = xdr_data
| limit 10
```

Objetivo: obter amostra para descobrir schema e qualidade; não detectar malware nem medir completude.
Não incluir payload, ID ou dado privado no compartilhamento. limite 10 exige marcar cobertura parcial.
Para hunting: identificar no schema real campo de endpoint, processo, evento e tempo; selecionar IDs exatos do caso; validar tipo/valores; montar filtro e campos com sugestões do editor; executar amostra autorizada, preservar query ID/resultado/contagem e ampliar conforme cobertura.

**Roteiro NOT VERIFIED:** autenticações, eventos AD e NGFW requerem dataset/preset e campos confirmados no tenant. Nenhum nome fictício é fornecido.
Não reutilizar a mistura de datamodel com campos XDRData da pesquisa; XDM depende de regras de mapeamento. Não presumir panw_ngfw_threat_raw. Referências: [PAN-XQL/PAN-LIMIT](../references/source-register.md).
