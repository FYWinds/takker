-- upgrade --
ALTER TABLE "bot_config" ADD "plugin_process_status" JSON;
-- downgrade --
ALTER TABLE "bot_config" DROP COLUMN "plugin_process_status";
