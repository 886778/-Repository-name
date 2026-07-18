# Development scripts

- `verify.sh`：执行格式、Lint、类型、单元测试、架构测试和构建检查。
- `secret-scan.sh`：扫描高置信度私钥和访问凭证模式，不读取外部 Secret Store。
- 所有脚本必须无业务语义、可审查，并且不得绕过应用层直接修改数据。
