# Manutenção
Editar somente a fonte da raiz. Regerar pacotes; nunca editar ZIP para depois copiar de volta. Preservar commits e versões históricas.
1. Ler contrato, versão, testes e fonte afetada antes de mudar.
2. Registrar alegação, produto/versão, URL e data; distinguir documentação, observação e hipótese.
3. Alterar o menor conjunto coerente e acrescentar regressão que capture a falha.
4. Executar validação estrutural/schema/semântica. Mudança de description/roteamento exige avaliação comportamental nova.
5. Avaliar em thread sem histórico usando pacote de uso e fixture; manter gabarito fora da entrada. Guardar output, contexto mínimo, hash e limitações.
6. Validar importação e consultas no ambiente-alvo separadamente. Não transformar teste de texto em prova de integração.
7. Atualizar VERSION/CHANGELOG e resultados, revisar diff/segredos e publicar só no destino autorizado.

## Pendências verificáveis
- Importar/carregar 0.1.0 em Work e Codex e observar ativação implícita.
- Executar consultas em tenant de laboratório autorizado, com schema/versão conhecidos.
- Completar revisão documental de Imperva, Stellar 6.4.x e serviços/tier de GCP SCC.
- Ampliar avaliações comportamentais, repetir casos críticos e medir variabilidade antes de concluir desempenho.
- Integrar SOAR somente após definir mapeamento, autorização e verificação de efeitos; não há integração instalada.

## Checklist de aceite
- [ ] Fonte completa e recursos resolvem dentro do pacote.
- [ ] Schema/exemplos/invariantes passam.
- [ ] Casos positivos/negativos/falhas têm fixtures e rubricas separadas.
- [ ] Resultados usam PASS/FAIL/NOT RUN/N/A com evidência.
- [ ] Segurança, privacidade, autorização e falhas são proporcionais ao domínio.
- [ ] Publicação remota e conteúdo conferidos; instalação não presumida.

Use tests/VALIDATION.md como evidência atual; este checklist é modelo de manutenção, não resultado automaticamente preenchido.
