package ru.tyezh.menu;

import java.util.Random;
import java.util.Set;

import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.Font;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;
import net.minecraft.resources.Identifier;

/**
 * Общий пастельный фон «Ты Еж»: небо, плывущие облака, мерцающие звёзды,
 * всплывающие сердечки. Используется главным меню и (через ScreenMixin)
 * всеми меню вне мира: настройки, выбор/создание мира, экраны загрузки.
 */
public final class TyEzhBackdrop {
	private static final Identifier SKY = TyEzhMenu.id("textures/gui/sky.png");
	private static final Identifier CLOUDS = TyEzhMenu.id("textures/gui/clouds.png");
	private static final Identifier WALK_0 = TyEzhMenu.id("textures/gui/hedgehog_walk_0.png");
	private static final Identifier WALK_1 = TyEzhMenu.id("textures/gui/hedgehog_walk_1.png");
	private static final Identifier PEEK = TyEzhMenu.id("textures/gui/hedgehog_peek.png");

	private static final int SKY_W = 480, SKY_H = 270;
	private static final int WALK_W = 34, WALK_H = 24;
	private static final int PEEK_W = 30, PEEK_H = 24;

	/** Экраны загрузки/ожидания: на них идёт ёжик и показываются подсказки. */
	private static final Set<String> LOADERS = Set.of(
			"LevelLoadingScreen", "ReceivingLevelScreen", "GenericMessageScreen",
			"ProgressScreen", "ConnectScreen", "GenericWaitingScreen", "GenericDirtMessageScreen");

	private static final int LOADING_TIPS = 8;

	static final String[] HEART = {
			".##.##.",
			"#######",
			"#######",
			".#####.",
			"..###..",
			"...#..."
	};

	/** Общее время: анимация не «прыгает» при переходе между экранами. */
	private static final long START = System.currentTimeMillis();

	private static final float[][] STARS;
	private static final float[][] FLOATERS;

	static {
		Random r = new Random(1337);
		STARS = new float[46][];
		for (int i = 0; i < STARS.length; i++) {
			// x, y (0..1), фаза, скорость, цвет
			STARS[i] = new float[]{r.nextFloat(), r.nextFloat() * 0.8f, r.nextFloat() * 6.28f, 1.2f + r.nextFloat() * 2.2f, r.nextInt(3)};
		}
		FLOATERS = new float[7][];
		for (int i = 0; i < FLOATERS.length; i++) {
			// x (0..1), период, сдвиг, цвет
			FLOATERS[i] = new float[]{r.nextFloat(), 10f + r.nextFloat() * 8f, r.nextFloat(), r.nextInt(3)};
		}
	}

	private TyEzhBackdrop() {
	}

	public static float time() {
		return (System.currentTimeMillis() - START) / 1000f;
	}

	/**
	 * Вызывается из ScreenMixin вместо ванильного фона.
	 * @return true — фон нарисован нами, ванильный рисовать не нужно.
	 */
	public static boolean drawFor(Screen screen, GuiGraphicsExtractor g) {
		if (screen instanceof TyEzhTitleScreen) {
			return false;
		}
		boolean loader = LOADERS.contains(screen.getClass().getSimpleName());
		// В мире (пауза, инвентарь и т.п.) оставляем ванильный фон,
		// кроме экранов загрузки — их стилизуем всегда.
		if (!loader && Minecraft.getInstance().level != null) {
			return false;
		}

		int w = screen.width, h = screen.height;
		int px = drawSky(g, w, h);
		// Лёгкая сиреневая вуаль — чтобы белый ванильный текст хорошо читался.
		g.fill(0, 0, w, h, 0x3A3B2C7A);

		if (loader) {
			drawLoader(g, w, h, px);
		} else if (w >= 420) {
			drawPeek(g, w, h, px);
		}
		return true;
	}

	/** Небо + облака + звёзды + сердечки. Возвращает размер «пикселя» фона. */
	public static int drawSky(GuiGraphicsExtractor g, int width, int height) {
		float t = time();
		float sk = Math.max(width / (float) SKY_W, height / (float) SKY_H);
		float skyX = (width - SKY_W * sk) / 2f;
		float skyY = (height - SKY_H * sk) / 2f;

		g.pose().pushMatrix();
		g.pose().translate(skyX, skyY);
		g.pose().scale(sk, sk);
		g.blit(RenderPipelines.GUI_TEXTURED, SKY, 0, 0, 0f, 0f, SKY_W, SKY_H, SKY_W, SKY_H);

		// облака плывут вправо; две копии для бесшовности
		float drift = (t * 5f) % SKY_W;
		g.pose().pushMatrix();
		g.pose().translate(drift, 0f);
		g.blit(RenderPipelines.GUI_TEXTURED, CLOUDS, 0, 0, 0f, 0f, SKY_W, SKY_H, SKY_W, SKY_H);
		g.blit(RenderPipelines.GUI_TEXTURED, CLOUDS, -SKY_W, 0, 0f, 0f, SKY_W, SKY_H, SKY_W, SKY_H);
		g.pose().popMatrix();
		g.pose().popMatrix();

		int px = Math.max(1, Math.round(sk));

		// мерцающие звёздочки
		for (float[] st : STARS) {
			float b = 0.5f + 0.5f * (float) Math.sin(t * st[3] + st[2]);
			if (b < 0.25f) {
				continue;
			}
			int a = (int) (b * 230f);
			int color = (a << 24) | (st[4] == 0 ? 0xFFFFFF : st[4] == 1 ? 0xFFF4C9 : 0xD9F6FF);
			int cx = Math.round(st[0] * width);
			int cy = Math.round(st[1] * height);
			int arm = b > 0.8f ? 2 : 1;
			g.fill(cx - arm * px, cy, cx + (arm + 1) * px, cy + px, color);
			g.fill(cx, cy - arm * px, cx + px, cy + (arm + 1) * px, color);
		}

		// всплывающие сердечки
		for (float[] f : FLOATERS) {
			float phase = ((t / f[1]) + f[2]) % 1f;
			int hx = Math.round(f[0] * width + (float) Math.sin(t * 1.3f + f[2] * 10f) * 6f * px);
			int hy = Math.round(height + 10 * px - phase * (height + 30 * px));
			float fade = phase < 0.15f ? phase / 0.15f : phase > 0.8f ? (1f - phase) / 0.2f : 1f;
			int a = (int) (fade * 170f);
			int rgb = f[3] == 0 ? 0xFF9ED8 : f[3] == 1 ? 0x8FE8FF : 0xFFFFFF;
			pixelHeart(g, hx, hy, px, (a << 24) | rgb);
		}
		return px;
	}

	/** Экран загрузки: ёжик топает по низу экрана + сменяющиеся подсказки. */
	private static void drawLoader(GuiGraphicsExtractor g, int w, int h, int px) {
		float t = time();
		Font font = Minecraft.getInstance().font;

		// подсказка в «таблетке»
		Component tip = Component.translatable("tyezh.loading." + ((int) (t / 3.5f) % LOADING_TIPS));
		int tw = font.width(tip);
		int pillW = tw + 16, pillH = 16;
		int pillX = (w - pillW) / 2, pillY = h - pillH - 10;
		g.fill(pillX - 1, pillY - 1, pillX + pillW + 1, pillY + pillH + 1, 0xFFFFFFFF);
		g.fill(pillX, pillY, pillX + pillW, pillY + pillH, 0xE05B4BC4);
		g.fill(pillX, pillY, pillX + pillW, pillY + 1, 0x66FFFFFF);
		g.text(font, tip, pillX + 8, pillY + 4, 0xFFFFFFFF, true);

		// ёжик идёт слева направо
		int sc = Math.max(2, px * 2);
		int sw = WALK_W * sc, sh = WALK_H * sc;
		float span = w + sw * 2f;
		float x = (t * 26f * sc) % span - sw;
		int y = pillY - sh - 6;
		boolean frame = ((int) (t / 0.18f)) % 2 == 0;
		g.pose().pushMatrix();
		g.pose().translate(x, y);
		g.pose().scale(sc, sc);
		g.blit(RenderPipelines.GUI_TEXTURED, frame ? WALK_0 : WALK_1, 0, 0, 0f, 0f, WALK_W, WALK_H, WALK_W, WALK_H);
		g.pose().popMatrix();

		// сердечки-«следы» за ёжиком
		for (int i = 1; i <= 3; i++) {
			float hxF = x - i * 14f * sc / 2f;
			if (hxF < -10 || hxF > w) {
				continue;
			}
			int a = 200 - i * 55;
			pixelHeart(g, Math.round(hxF), y + sh - 4 * px, Math.max(1, px), (a << 24) | 0xFF9ED8);
		}
	}

	/** Сонный ёжик выглядывает из правого нижнего угла в меню. */
	private static void drawPeek(GuiGraphicsExtractor g, int w, int h, int px) {
		float t = time();
		float bob = (float) Math.sin(t * 1.6f) * px;
		int sc = Math.max(1, px);
		int x = w - PEEK_W * sc - 6;
		float y = h - PEEK_H * sc * 0.7f + bob;
		g.pose().pushMatrix();
		g.pose().translate(x, y);
		g.pose().scale(sc, sc);
		g.blit(RenderPipelines.GUI_TEXTURED, PEEK, 0, 0, 0f, 0f, PEEK_W, PEEK_H, PEEK_W, PEEK_H);
		g.pose().popMatrix();
	}

	static void pixelHeart(GuiGraphicsExtractor g, int x, int y, int u, int color) {
		for (int row = 0; row < HEART.length; row++) {
			String line = HEART[row];
			int start = -1;
			for (int col = 0; col <= line.length(); col++) {
				boolean on = col < line.length() && line.charAt(col) == '#';
				if (on && start < 0) {
					start = col;
				} else if (!on && start >= 0) {
					g.fill(x + start * u, y + row * u, x + col * u, y + (row + 1) * u, color);
					start = -1;
				}
			}
		}
	}
}
