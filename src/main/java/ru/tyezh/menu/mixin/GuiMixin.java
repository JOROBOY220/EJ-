package ru.tyezh.menu.mixin;

import net.minecraft.client.gui.Gui;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.TitleScreen;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.ModifyVariable;
import ru.tyezh.menu.TyEzhMenu;
import ru.tyezh.menu.TyEzhTitleScreen;

/**
 * В 26.2 установка экрана переехала из Minecraft в Gui (Minecraft.getInstance().gui.setScreen).
 * Любая попытка открыть ванильное главное меню подменяется на наше.
 */
@Mixin(Gui.class)
public abstract class GuiMixin {
	@ModifyVariable(method = "setScreen", at = @At("HEAD"), argsOnly = true)
	private Screen tyezh$replaceTitleScreen(Screen screen) {
		if (screen instanceof TitleScreen && !TyEzhMenu.bypassReplacement) {
			return new TyEzhTitleScreen();
		}
		return screen;
	}
}
