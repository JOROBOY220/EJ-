package ru.tyezh.menu.mixin;

import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.AbstractButton;
import net.minecraft.client.gui.components.AbstractSliderButton;
import net.minecraft.client.gui.components.AbstractWidget;
import org.spongepowered.asm.mixin.Mixin;
import org.spongepowered.asm.mixin.Unique;
import org.spongepowered.asm.mixin.injection.At;
import org.spongepowered.asm.mixin.injection.Inject;
import org.spongepowered.asm.mixin.injection.callback.CallbackInfo;
import ru.tyezh.menu.TyEzhSounds;

/** Звук при наведении мыши на любую кнопку или слайдер. */
@Mixin(AbstractWidget.class)
public abstract class AbstractWidgetMixin {
	@Unique
	private boolean tyezh$wasHovered = false;
	@Unique
	private boolean tyezh$seenOnce = false;

	@Inject(method = "extractRenderState", at = @At("TAIL"))
	private void tyezh$hoverSound(GuiGraphicsExtractor graphics, int mouseX, int mouseY, float partialTick, CallbackInfo ci) {
		AbstractWidget self = (AbstractWidget) (Object) this;
		boolean hovered = self.visible && self.active && self.isHovered()
				&& (self instanceof AbstractButton || self instanceof AbstractSliderButton);
		// Первый кадр только запоминаем: не пищим, если курсор уже стоял на кнопке при открытии экрана.
		if (tyezh$seenOnce && hovered && !tyezh$wasHovered) {
			TyEzhSounds.playHover();
		}
		tyezh$wasHovered = hovered;
		tyezh$seenOnce = true;
	}
}
