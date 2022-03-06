-- upgrade --
CREATE TABLE IF NOT EXISTS "bot_config" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(32) NOT NULL,
    "illust_config" JSON
) /* 机器人全局配置内容，部分关键字段请勿随意修改 */;
CREATE TABLE IF NOT EXISTS "group_config" (
    "gid" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "perm" INT,
    "plugin_status" JSON
) /* 群组配置数据 */;
CREATE INDEX IF NOT EXISTS "idx_group_confi_gid_82beae" ON "group_config" ("gid");
CREATE TABLE IF NOT EXISTS "user_config" (
    "uid" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "points" BIGINT,
    "constellation" INT,
    "perm" INT,
    "plugin_status" JSON
) /* 用户配置数据 */;
CREATE INDEX IF NOT EXISTS "idx_user_config_uid_6e7a7c" ON "user_config" ("uid");
CREATE TABLE IF NOT EXISTS "ban" (
    "uid" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "ban_level" INT NOT NULL,
    "ban_time" BIGINT NOT NULL,
    "duration" BIGINT NOT NULL
) /* 封禁系统数据 */;
CREATE INDEX IF NOT EXISTS "idx_ban_uid_aea8fb" ON "ban" ("uid");
CREATE TABLE IF NOT EXISTS "bili_sub" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "type" VARCHAR(10) NOT NULL,
    "type_id" INT NOT NULL,
    "bid" INT NOT NULL,
    "name" VARCHAR(30) NOT NULL,
    "live" INT NOT NULL  DEFAULT 1,
    "dynamic" INT NOT NULL  DEFAULT 1,
    "at" INT NOT NULL  DEFAULT 0
) /* b站订阅数据 */;
CREATE INDEX IF NOT EXISTS "idx_bili_sub_type_id_82243c" ON "bili_sub" ("type_id", "bid");
CREATE TABLE IF NOT EXISTS "statistic" (
    "gid" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "stat" TEXT,
    "illust_stat" TEXT
) /* 插件调用数据 */;
CREATE INDEX IF NOT EXISTS "idx_statistic_gid_6ff77a" ON "statistic" ("gid");
CREATE TABLE IF NOT EXISTS "wordcloud" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "gid" BIGINT NOT NULL,
    "uid" BIGINT NOT NULL,
    "time" BIGINT NOT NULL,
    "msg" TEXT,
    "msg_seg" TEXT
) /* 热词词云数据 */;
CREATE INDEX IF NOT EXISTS "idx_wordcloud_gid_ebbd28" ON "wordcloud" ("gid");
CREATE TABLE IF NOT EXISTS "permission" (
    "id" TEXT NOT NULL  PRIMARY KEY,
    "perm" INT NOT NULL
) /* 权限系统数据 */;
CREATE TABLE IF NOT EXISTS "plugin_manager" (
    "id" TEXT NOT NULL  PRIMARY KEY,
    "status" TEXT
) /* 插件管理器数据 */;
CREATE TABLE IF NOT EXISTS "point" (
    "uid" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "points" BIGINT NOT NULL
) /* 机器人积分系统数据 */;
CREATE TABLE IF NOT EXISTS "star" (
    "uid" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "star" INT NOT NULL
) /* 星座运势绑定数据 */;
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" JSON NOT NULL
);
