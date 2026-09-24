package ru.tyezh.menu.mixin;

import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import ru.tyezh.menu.TyEzhBackdrop;

/**
 * Заменяет ванильный фон (панорама + размытие) на пастельное небо «Ты Еж»
 * во всех меню вне мира: настройки, выбор и создание мира, загрузка мира и т.д.
 */
@Mixin(Screen.class)
public abstract class ScreenMixin {
	@Inject(method = "extractBackground", at = @At("HEAD"), cancellable = true)
	private void tyezh$drawBackdrop(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick, CallbackInfo ci) {
		if (TyEzhBackdrop.drawFor((Screen) (Object) this, graphics)) {
			ci.cancel();
		}
	}
}
