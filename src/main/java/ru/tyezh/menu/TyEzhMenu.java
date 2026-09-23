package ru.tyezh.menu;

import net.minecraft.resources.Identifier;

/** Общие константы мода «Ты Еж». */
public final class TyEzhMenu {
	public static final String MOD_ID = "tyezh";

	/**
	 * Когда true — миксин НЕ подменяет ванильный TitleScreen.
	 * Используется на один вызов, чтобы нажать ванильную кнопку
	 * (одиночная/сетевая игра и т.д.) со всеми её проверками.
	 */
	public static boolean bypassReplacement = false;

	private TyEzhMenu() {
	}

	public static Identifier id(String path) {
		return Identifier.fromNamespaceAndPath(MOD_ID, path);
	}
}
