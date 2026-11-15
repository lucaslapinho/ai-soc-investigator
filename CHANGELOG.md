# Changelog

## 0.1.0 — 2026-11-14
Baseline inicial sobre repositório com apenas README.
- SKILL.md na raiz, nove módulos, quatro workflows e 25 casos completos.
- Contrato JSON Schema 2020-12, exemplo sintético e validador semântico local.
- Regressão de data impossível: validação explícita de date-time evita aceitar data inválida quando o formato opcional não está disponível no jsonschema.
- Fontes oficiais datadas, consultas conservadoras e separação XDM/dataset e Defender/Sentinel.
- GPO: distinguir 5141/5136 de 4732 e DC registrador de endpoint originador.
- ATT&CK: PowerShell T1059.001, DNS C2 T1071.004 e páginas atuais T1685/T1686.002.
- Governança de resposta, prompt injection, segregação de tenants, timeouts e interação condicional.
- Fixtures, validações executáveis e build reproduzível, sem instalação ou operação SOC presumida.
Não há contrato anterior a migrar. Alterações incompatíveis futuras em 0.x elevam MINOR e exigem nota de migração; correções compatíveis elevam PATCH. Não regravar release histórica.
