# Infrastructure

该目录仅保留基础设施边界。M1 只在应用代码中建立 PostgreSQL、Redis、健康检查和运行生命周期边界；此目录仍不选择云平台、生产编排、跨区域部署或 Secret Provider，也不创建部署配置、业务 Schema 或 Migration。

数据库启动不得自动迁移。ORM/Migration 组合、正式 Schema、Outbox/Inbox、字段级加密和生产资源声明必须先通过对应治理 Gate。
