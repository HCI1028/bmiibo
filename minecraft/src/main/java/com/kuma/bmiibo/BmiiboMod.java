package com.huangziji.bmiibo;

import net.fabricmc.api.ModInitializer;
import net.fabricmc.fabric.api.command.v2.CommandRegistrationCallback;
import net.minecraft.server.command.CommandManager;
import net.minecraft.text.Text;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class BmiiboMod implements ModInitializer {
    public static final String MOD_ID = "bmiibo";
    public static final Logger LOGGER = LoggerFactory.getLogger(MOD_ID);

    @Override
    public void onInitialize() {
        LOGGER.info("🎉 bmiibo 虛擬玩具 Fabric 模組整合 API 已成功啟動！");

        // 註冊遊戲內指令 /bmiibo
        CommandRegistrationCallback.EVENT.register((dispatcher, registryAccess, environment) -> {
            dispatcher.register(CommandManager.literal("bmiibo")
                .then(CommandManager.literal("status")
                    .executes(context -> {
                        context.getSource().sendFeedback(() -> Text.literal("§a[bmiibo] 系統運作正常。等待刷入公仔..."), false);
                        return 1;
                    })
                )
            );
        });
    }
}
