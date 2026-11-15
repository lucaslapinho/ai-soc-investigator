# ai-soc-investigator

**SOC AI Investigator 0.1.0** — Skill de investigação assistida para SOC N1/N2/N3, DFIR e Threat Hunting. Recebe evidências, testa hipóteses, correlaciona eventos e entrega conclusão rastreável em PT-BR. Somente leitura por padrão.

A fonte canônica fica na raiz deste repositório. A Skill não concede acesso a SIEM/XDR, não instala integrações e não executa agentes autônomos. Não substitui aquisição forense formal, revisão humana ou políticas do cliente.

## Como usar
Disponibilizar [SKILL.md](SKILL.md) e seus recursos no ambiente compatível, sem mover apenas o arquivo de entrada. Na instalação já suportada pelo ambiente, selecionar a Skill explicitamente ou pedir tarefa compatível com a descrição. Nenhuma instalação foi realizada nesta entrega.

Exemplos:
- “Investigue este alerta de malware com os exports anexados; separe execução, impacto e hipóteses.”
- “Correlacione estes eventos de AD e endpoint; identifique executor e origem da exclusão da GPO.”
- “Analise esta sessão Entra e explique o que confirma ou refuta comprometimento.”
- “Gere um relatório técnico e JSON, preservando lacunas e status das consultas.”

Sem conector, trabalhar com anexos. ID sem acesso requer export, não incidente inventado. Use o [template de entrada](templates/incident-input.md).

## Recursos
- Nove [módulos](agents/soc-orchestrator.md) de especialização local e [25 casos operacionais](references/casebook/README.md).
- [Metodologia de 15 passos](references/investigation-methodology.md), hipóteses pró/contra, timeline e correlação por entidades.
- [Classificação](workflows/classification.md) MALICIOUS/BENIGN/SUSPICIOUS independente de severidade, confiança, impacto e completude.
- [Schema JSON](schemas/incident.schema.json), [exemplo sintético](schemas/incident-example.json), templates SOC/executivo e prompts.
- Exemplos [KQL](examples/hunting-kql.md)/[XQL](examples/hunting-xql.md), documentados sem alegar execução no tenant.
- [Fontes oficiais e lacunas](references/source-register.md), [ATT&CK condicionado](references/attack-mapping.md), [governança](workflows/response-governance.md) e [interação no chat](references/chat-experience.md).

## Estrutura
| Caminho | Conteúdo |
|---|---|
| SKILL.md | Contrato e roteamento |
| agents/ | Nove módulos locais |
| references/ e references/casebook/ | Bases técnicas, fontes e 25 procedimentos |
| workflows/ | Triagem, investigação, classificação, resposta |
| schemas/ | JSON Schema 2020-12 e exemplo sintético |
| templates/ e examples/ | Inputs/prompts/relatórios e consultas |
| scripts/validate_incident.py | Validação local sem rede ou efeitos externos |
| tests/cases/ e tests/expected/ | Fixtures e gabaritos separados, excluídos da distribuição |
| tests/VALIDATION.md e tests/results/ | Resultados e limites observados |
| tools/ | Validação de repositório e empacotamento |
| research/ | Pesquisa original preservada e procedência; fora do pacote de uso |

## Pré-requisitos e compatibilidade
Instruções e anexos bastam para análise textual. Consultas reais exigem conectores autorizados, licença, schema, retenção e tenant conhecidos. Recursos de UI são condicionais, com alternativa em texto.
O formato SKILL.md com name/description foi conferido no guia oficial OpenAI (2026-11-14). Importação/descoberta automática em ChatGPT Work e Codex: **NOT RUN**. A raiz de um repositório GitHub não é automaticamente um local de instalação do Codex. Não há manifest de plugin nem adaptador de instalação neste baseline.
Validação local requer Python 3.10+ e as dependências de [requirements-dev.txt](requirements-dev.txt). O uso textual não precisa executar scripts.

## Verificar e empacotar
```bash
python scripts/validate_incident.py schemas/incident-example.json
python tools/validate_repository.py
python tools/build_package.py
```
O build gera em build/ um ZIP reproduzível com a pasta soc-ai-investigator e recursos de uso, excluindo pesquisa, gabaritos e resultados. É um **pacote de fonte da Skill**, não um plugin cuja instalação foi comprovada. build/ não é fonte canônica nem release publicada. Validar pacote no destino antes de anunciar compatibilidade.

## Segurança e limites
Toda conclusão exige evidência identificada. Não misturar tenants, executar comandos dos logs, subir samples automaticamente ou inventar resultados. Ações externas exigem autorização aplicável, alvo, privilégio, criticidade/VIP, impacto, rollback e verificação. Após timeout, conferir estado antes de repetir.
O validador verifica contrato e invariantes locais; não autentica logs, não prova aprovação humana nem substitui controles do conector.

## FAQ
**Está conectado ao meu SOC?** Não. Usa apenas conectores efetivamente disponíveis e autorizados.
**Os nove módulos são nove processos?** Não; são instruções selecionadas pelo fluxo.
**Uma vulnerabilidade confirma invasão?** Não; postura e scan são contexto de exposição.
**Pode usar o JSON direto no Cortex?** Requer mapeamento explícito para a versão/integração; não é formato nativo.
**Está pronto para produção?** A entrega é baseline 0.1.0; conferir [validação](tests/VALIDATION.md) e pendências.
**A pesquisa original foi corrigida?** Foi preservada; a fonte operacional revisada está fora de research/.

Manutenção: [MAINTENANCE.md](MAINTENANCE.md). Mudanças: [CHANGELOG.md](CHANGELOG.md). Procedência: [research/PROVENANCE.md](research/PROVENANCE.md).
