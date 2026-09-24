package ru.tyezh.menu;

import java.util.Random;

import net.minecraft.client.Minecraft;
import net.minecraft.client.resources.sounds.SimpleSoundInstance;
import net.minecraft.sounds.SoundEvent;

/**
 * Звуки интерфейса. Клик кнопок заменён целиком через
 * assets/minecraft/sounds.json (ui.button.click → tyezh:ui/click),
 * а звук наведения и «фыр» ёжика проигрываются отсюда.
 */
public final class TyEzhSounds {
	public static final SoundEvent HOVER = SoundEvent.createVariableRangeEvent(TyEzhMenu.id("ui.hover"));
	public static final SoundEvent SNUFF = SoundEvent.createVariableRangeEvent(TyEzhMenu.id("ui.snuff"));

	private static final Random RANDOM = new Random();
	private static long lastHover = 0L;

	private TyEzhSounds() {
	}

	/** Мягкий «блип» при наведении; не чаще раза в 45 мс, чтобы не трещало. */
	public static void playHover() {
		long now = System.currentTimeMillis();
		if (now - lastHover < 45L) {
			return;
		}
		lastHover = now;
		play(HOVER, 0.94f + RANDOM.nextFloat() * 0.12f, 0.35f);
	}

	/** «Фыр-фыр!» */
	public static void playSnuff() {
		play(SNUFF, 0.9f + RANDOM.nextFloat() * 0.25f, 0.6f);
	}

	private static void play(SoundEvent event, float pitch, float volume) {
		Minecraft.getInstance().getSoundManager().play(SimpleSoundInstance.forUI(event, pitch, volume));
	}
}
