-- upgrade --
ALTER TABLE "bot_config" ADD "plugin_perms" JSON;
-- downgrade --
ALTER TABLE "bot_config" DROP COLUMN "plugin_perms";
