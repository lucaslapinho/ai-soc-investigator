#!/usr/bin/env python3
"""Offline structural, schema, regression and packaging checks; not tenant execution."""
import copy
import hashlib
import importlib.metadata
import json
from pathlib import Path
import re
import sys
import tempfile
import zipfile
import yaml
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
sys.path.insert(0,str(ROOT/"tools"))
from validate_incident import read_json, validate
from build_package import build, runtime_files
results=[]
def record(name, function):
    try:
        detail=function()
        results.append({"check":name,"status":"PASS","detail":detail or "Completed"})
    except Exception as exc:
        results.append({"check":name,"status":"FAIL","detail":str(exc)})
def require(test,message):
    if not test: raise AssertionError(message)
def frontmatter():
    text=(ROOT/"SKILL.md").read_text()
    parts=text.split("---",2)
    require(text.startswith("---\n") and len(parts)==3,"Missing frontmatter")
    meta=yaml.safe_load(parts[1])
    require(set(meta)=={"name","description"},"Unexpected metadata keys")
    require(meta["name"]=="soc-ai-investigator" and re.fullmatch("[a-z0-9-]{1,64}",meta["name"]),"Invalid name")
    require(isinstance(meta["description"],str) and 30<len(meta["description"])<1024,"Invalid description")
    return {"name":meta["name"],"lines":len(text.splitlines())}
def layout():
    agents=list((ROOT/"agents").glob("*.md"))
    cases=list((ROOT/"references/casebook").glob("[0-9][0-9]-*.md"))
    require(len(agents)==9 and len(cases)==25,"Module/case count mismatch")
    headings=["Objetivo","Hipóteses e sinais","Evidências, fontes e pré-requisitos","Triagem e hunting","Consulta defensiva e verificação","Decisão","Limitações e correlações","ATT&CK condicionado","Recomendações e escalonamento","Relatório técnico sintético"]
    for path in cases:
        content=path.read_text()
        for h in headings: require("## "+h in content,f"{path.name}: missing {h}")
    for p in ROOT.rglob("*"):
        if ".git" in p.parts or "build" in p.parts or "__pycache__" in p.parts:continue
        require(not p.is_symlink(),f"Unexpected symlink {p}")
    return {"agents":len(agents),"operational_cases":len(cases)}
def local_links(paths=None):
    count=0
    for path in paths or ROOT.rglob("*.md"):
        if ".git" in path.parts or "build" in path.parts: continue
        text=path.read_text()
        fence=chr(96)*3
        require(text.count(fence)%2==0,f"Unbalanced fences: {path}")
        for target in re.findall(r"\[[^\]]+\]\(([^)\s]+)\)",text):
            if re.match(r"^[a-z]+:",target) or target.startswith("#"):continue
            rel=target.split("#")[0]
            require((path.parent/rel).resolve().exists(),f"Broken link {path.name}: {target}")
            count+=1
    return {"local_links_checked":count,"markdown_check":"fence balance and local link resolution; not full CommonMark/render lint"}
def json_files():
    paths=[p for p in ROOT.rglob("*.json") if ".git" not in p.parts and "build" not in p.parts]
    for path in paths:read_json(path)
    return {"json_files":len(paths),"duplicate_keys":"rejected"}
def schema_regressions():
    base=read_json(ROOT/"schemas/incident-example.json")
    checks=[]
    def run(name,data,valid):
        errors=validate(data)
        require((not errors)==valid,f"{name}: expected valid={valid}, errors={errors[:2]}")
        checks.append({"case":name,"status":"PASS","accepted":not errors,"observed_errors":errors[:2]})
    run("synthetic-malicious-example",base,True)
    benign=copy.deepcopy(base)
    benign.update(classification="BENIGN",investigation_status="Complete",actions=[],human_approval_required=False,attack=[],gaps=[],next_steps=[])
    benign["justification"]["summary"]="Job autorizado explica todos os sinais no escopo sintético."
    benign["impact"].update(status="None Observed",description="Sem dano no job autorizado.")
    for e in benign["evidence"]["items"]:e["summary"]="Job e efeitos correspondem à autorização sintética."
    run("benign-positive-contract",benign,True)
    suspicious=copy.deepcopy(base)
    suspicious.update(classification="SUSPICIOUS",confidence="Low",actions=[],human_approval_required=False,attack=[],entities=[],timeline=[],sources=[],queries=[])
    suspicious["justification"].update(summary="Dados não disponíveis; sinal ainda não confirmado.",evidence_ids=[])
    suspicious["evidence"].update(items=[],supporting_ids=[],opposing_ids=[],opposing_assessment="Sem evidência disponível.")
    suspicious["scope"].update(confirmed_entity_ids=[],potential_entity_ids=[])
    suspicious["impact"].update(status="Unknown",evidence_ids=[],description="Sem dados de impacto.")
    run("missing-evidence-positive-contract",suspicious,True)
    def change(name,func):
        doc=copy.deepcopy(base);func(doc);run(name,doc,False)
    change("invalid-enum",lambda d:d.update(classification="Malicious"))
    change("unexpected-property",lambda d:d.update(secret="not-allowed"))
    change("invalid-date",lambda d:d.update(created_at="2026-02-31T12:00:00Z"))
    change("missing-required",lambda d:d.pop("impact"))
    change("suspicious-complete",lambda d:d.update(classification="SUSPICIOUS",investigation_status="Complete"))
    change("benign-incomplete",lambda d:d.update(classification="BENIGN"))
    change("false-executed-without-approval",lambda d:d["actions"][0].update(status="Executed"))
    change("timeout-without-execution-record",lambda d:d["actions"][0].update(status="Unknown"))
    change("invalid-hash",lambda d:d["evidence"]["items"][0].update(sha256="abc123"))
    change("unresolved-evidence",lambda d:d["justification"].update(evidence_ids=["EV-missing"]))
    change("duplicate-evidence",lambda d:d["evidence"]["items"].append(copy.deepcopy(d["evidence"]["items"][0])))
    change("cross-tenant-source",lambda d:d["sources"][0].update(tenant_ref="another-tenant"))
    change("cross-tenant-entity",lambda d:d["entities"][0].update(tenant_ref="another-tenant"))
    change("original-utc-mismatch",lambda d:d["timeline"][0].update(original_time="2026-11-14T13:01:00Z"))
    change("false-query-executed",lambda d:d["queries"][0].update(status="Executed"))
    change("observation-from-unavailable-source",lambda d:d["sources"][0].update(access_status="Unavailable"))
    change("wrong-attack-url",lambda d:d["attack"][0].update(source_url="https://attack.mitre.org/techniques/T1190/"))
    executed=copy.deepcopy(base);act=executed["actions"][0]
    act.update(status="Executed",executor="synthetic-operator",
        approval={"decision":"Approved","approver":"synthetic-owner","approved_at":"2026-11-14T12:11:00Z","expires_at":"2026-11-14T12:30:00Z","tenant_ref":"tenant-synthetic","target_entity_ids":["ENT-001"],"scope":"Isolar apenas este endpoint no cenário fictício."},
        execution={"started_at":"2026-11-14T12:12:00Z","finished_at":"2026-11-14T12:13:00Z","tool":"synthetic-response-tool","request_ref":"synthetic-job-1","result_ref":"synthetic-state-1","verification_status":"Confirmed","verification_evidence_ids":["EV-VERIFY"]})
    verification=copy.deepcopy(base["evidence"]["items"][0])
    verification.update(id="EV-VERIFY",observed_at="2026-11-14T12:13:00Z",original_time="2026-11-14T12:13:00Z",collected_at="2026-11-14T12:14:00Z",summary="Estado fictício de isolamento confirmado após operação aprovada.")
    executed["evidence"]["items"].append(verification);executed["updated_at"]="2026-11-14T12:14:00Z"
    run("authorized-execution-contract-synthetic-only",executed,True)
    for name, mutate in [
        ("approval-wrong-target",lambda d:d["actions"][0]["approval"].update(target_entity_ids=["ENT-other"])),
        ("approval-wrong-tenant",lambda d:d["actions"][0]["approval"].update(tenant_ref="other")),
        ("execution-before-approval",lambda d:d["actions"][0]["execution"].update(started_at="2026-11-14T12:10:00Z")),
        ("approval-expired",lambda d:d["actions"][0]["approval"].update(expires_at="2026-11-14T12:11:30Z")),
        ("execution-no-verification",lambda d:d["actions"][0]["execution"].update(verification_evidence_ids=[])),
        ("verification-only-inference",lambda d:d["evidence"]["items"][-1].update(kind="Inference"))
    ]:
        bad=copy.deepcopy(executed);mutate(bad);run(name,bad,False)
    return {"count":len(checks),"cases":checks,"scope":"Schema + referential/time/approval invariants, not judgment of evidence truth"}
def code_compile():
    paths=list((ROOT/"scripts").glob("*.py"))+list((ROOT/"tools").glob("*.py"))
    for path in paths:compile(path.read_text(),str(path),"exec")
    return {"python_files":len(paths)}
def query_lint():
    fence=chr(96)*3
    k=(ROOT/"examples/hunting-kql.md").read_text()
    x=(ROOT/"examples/hunting-xql.md").read_text()
    kq=re.findall(fence+r"kql\n(.*?)"+fence,k,re.S)
    xq=re.findall(fence+r"xql\n(.*?)"+fence,x,re.S)
    require(len(kq)==3 and len(xq)==1,"Unexpected query count")
    for q in kq:
        require(q.splitlines()[0] in ["DeviceProcessEvents","DeviceNetworkEvents","SigninLogs"],"Unknown KQL example table")
        require(q.count("(")==q.count(")"),"Unbalanced KQL parentheses")
        require("datetime(" in q,"Missing explicit time")
    require(xq[0].startswith("dataset = xdr_data"),"Unexpected XQL start")
    require("datamodel" not in xq[0] and "XDRData." not in xq[0],"Unverified mixed XQL syntax")
    return {"kql":3,"xql":1,"scope":"Textual sanity only; parser compilation and tenant execution NOT RUN"}
def secrets():
    patterns=[r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",r"\bAKIA[A-Z0-9]{16}\b",r"\bgh[pousr]_[A-Za-z0-9]{30,}\b",r"\bgithub_pat_[A-Za-z0-9_]{60,}\b"]
    scanned=0
    for path in ROOT.rglob("*"):
        if not path.is_file() or any(t in path.parts for t in (".git","build","__pycache__")) or path.suffix==".pyc":continue
        text=path.read_text(encoding="utf-8")
        for pattern in patterns:require(not re.search(pattern,text),f"Potential secret in {path}")
        scanned+=1
    return {"files":scanned,"scope":"Heuristic known private-key/token patterns; not a guarantee that all sensitive data is absent"}
def packaging():
    a=build();b=build();require(a["sha256"]==b["sha256"],"Build not reproducible")
    with zipfile.ZipFile(ROOT/"build"/a["archive"]) as z, tempfile.TemporaryDirectory() as directory:
        names=z.namelist()
        require(len(names)==len(set(names)),"Duplicate archive paths")
        for name in names:
            parts=Path(name).parts
            require(not name.startswith("/") and ".." not in parts,"Unsafe archive path")
            require(not any(t in parts for t in ("tests","research",".git","tools")),"Development data in usage package")
        z.extractall(directory)
        root=Path(directory)/"soc-ai-investigator"
        local_links(list(root.rglob("*.md")))
        for item in a["files"]:
            require(hashlib.sha256((root/item["path"]).read_bytes()).hexdigest()==item["sha256"],"Archive content mismatch")
    return {"file_count":len(a["files"]),"sha256":a["sha256"],"scope":"Archive integrity, closure and reproducibility; import NOT RUN"}
if __name__=="__main__":
    for name,fn in [("frontmatter",frontmatter),("layout",layout),("markdown-local-links",local_links),("json-parse",json_files),("schema-semantic-regressions",schema_regressions),("python-compile",code_compile),("query-textual-sanity",query_lint),("heuristic-secrets-scan",secrets),("source-package",packaging)]:
        record(name,fn)
    result={"date":"2026-11-14","python":sys.version.split()[0],"dependencies":{n:importlib.metadata.version(n) for n in ["jsonschema","PyYAML"]},"checks":results}
    out=ROOT/"tests/results/static-validation.json";out.parent.mkdir(exist_ok=True,parents=True);out.write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
    for r in results:print(f"{r['status']}: {r['check']}"+(f": {r['detail']}" if r["status"]=="FAIL" else ""))
    sys.exit(int(any(r["status"]=="FAIL" for r in results)))
