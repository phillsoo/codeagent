# Autonomous AI Database MCP integration

Use this reference when the request is to expose Autonomous AI Database data or operations through MCP. Re-check the linked Oracle and Hermes documentation at execution time; product availability, endpoint formats, authentication, and CLI schemas can change.

## Choose the correct MCP surface

| Goal | Preferred surface | Boundary |
|---|---|---|
| Approved ADB data lookup/storage tools | **ADB Native MCP Server** | Oracle-managed Streamable HTTP endpoint; DB identity, exposed Select AI Agent tools, VPD/RAS, ACL/private endpoint |
| SQLcl-specific or broad SQL workflow when Native MCP is unsuitable | SQLcl MCP | Local `sql -mcp` stdio process; saved DB connection and SQLcl restrict level |
| ADB instance, backup, Data Guard, wallet, and other OCI control-plane operations | OCI Database MCP | OCI profile/IAM; not a table-data path; Oracle `oracle/mcp` repository describes reference/PoC implementations |
| Managed IAM/OAuth/OBO and Vault-backed Database Tools Connections | OCI Database Tools MCP | OCI Database Tools policies, connection, secret/key, server/toolset |

Do not infer that no managed ADB endpoint exists merely because SQLcl or `oracle/mcp` appears first in search results. Check the current ADB Native MCP product pages directly.

## Native-first design

1. Read-only inventory first: explicit compartment and region, target ADB lifecycle/version/deployment/endpoint/ACL, and current tags. Preserve request ID and redact OCIDs/hostnames in broad reports.
2. Decide private endpoint versus public endpoint plus a fixed egress `/32`; never default to `0.0.0.0/0`.
3. Use a dedicated DB identity. Grant `CREATE SESSION` and only exact view/package privileges; avoid `ADMIN`, `DBA`, `SELECT ANY TABLE`, arbitrary DDL, and direct table DML.
4. Expose approved Select AI Agent custom tools. Start with read-only canaries. For writes, call a validated package API with binds, field allowlists, payload limits, idempotency, transaction/rollback behavior, and audit IDs—never a free-form SQL tool.
5. Enable Native MCP only through a reviewed ADB change package. Preserve existing free-form tags before changing `adb$feature`; feature enable/disable, ACL, DB grants/tools/VPD, and Hermes registration are separate approval-gated writes.
6. Prefer interactive OAuth. If automation requires a short-lived bearer token, inject it from an approved secret store and keep it out of YAML, shell history, logs, and artifacts.
7. In Hermes, register the exact managed URL, run `hermes mcp test`, and use `hermes mcp configure` or an allowlist to expose only approved tools. Disable sampling unless explicitly needed.
8. Verify positive and negative paths: allowed/denied source, valid/invalid/expired auth, exact tool discovery, read-only canary, prohibited DDL/DML/schema access, VPD/RAS, audit correlation, and secret scan.

## Hermes configuration pitfall

Utility wrappers are filtered **inside** the `tools` mapping. This is the intended shape:

```yaml
mcp_servers:
  adb-native:
    url: "<exact-managed-endpoint>"
    auth: oauth
    sampling:
      enabled: false
    tools:
      include: [approved_report, approved_lookup]
      prompts: false
      resources: false
```

A YAML file can parse successfully while `prompts` and `resources` are incorrectly placed at server level. Add a semantic assertion that they exist under `tools` and are absent at server level; syntax-only validation is insufficient.

## Abort and rollback

Abort on unexpected tool exposure, any unapproved write, existing-client ACL outage, missing audit, access from a denied source, or secret leakage. Roll back in a reviewed sequence: disable/remove the Hermes server, disable the ADB MCP feature, lock/terminate the dedicated DB identity if approved, restore the exact captured ACL, reverse tools/VPD/grants, and repeat the same positive/negative verification. Disabling access does not reverse data writes.

## Authoritative starting points

- ADB MCP overview: https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/about-mcp-server.html
- ADB MCP enable/client configuration: https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/use-mcp-server.html
- ADB MCP security: https://docs.oracle.com/en-us/iaas/autonomous-database-serverless/doc/security.html
- SQLcl MCP: https://docs.oracle.com/en/database/oracle/sql-developer-command-line/26.2/sqcug/using-oracle-sqlcl-mcp-server.html
- Database Tools MCP: https://docs.oracle.com/en-us/iaas/database-tools/doc/working-database-tools-mcp-server.html
- Hermes MCP: https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp
