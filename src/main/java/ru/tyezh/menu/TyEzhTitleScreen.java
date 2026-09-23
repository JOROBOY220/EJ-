package ru.tyezh.menu;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.client.Minecraft;
import net.minecraft.client.gui.GuiGraphicsExtractor;
import net.minecraft.client.gui.components.AbstractButton;
import net.minecraft.client.gui.components.Button;
import net.minecraft.client.gui.components.events.GuiEventListener;
import net.minecraft.client.gui.screens.Screen;
import net.minecraft.client.gui.screens.TitleScreen;
import net.minecraft.client.renderer.RenderPipelines;
import net.minecraft.network.chat.Component;
import net.minecraft.network.chat.contents.TranslatableContents;
import net.minecraft.resources.Identifier;

/**
 * Главное меню «Ты Еж»: пастельный пиксельный «рабочий стол» с окошками,
 * ёжиком, облаками, мерцающими звёздами и сердечками.
 *
 * Вся картинка собрана в «композицию» 400x225 условных пикселей, которая
 * равномерно масштабируется под любое окно. Кнопки — обычные ванильные Button
 * (клавиатура, озвучка, звуки работают), но сделаны прозрачными, а
 * рисуются нашим стилем поверх.
 */
public class TyEzhTitleScreen extends Screen {
	// ---------------------------------------------------------------- текстуры
	private static final Identifier SKY = TyEzhMenu.id("textures/gui/sky.png");
	private static final Identifier CLOUDS = TyEzhMenu.id("textures/gui/clouds.png");
	private static final Identifier PANEL = TyEzhMenu.id("textures/gui/panel.png");
	private static final Identifier HEDGEHOG = TyEzhMenu.id("textures/gui/hedgehog.png");
	private static final Identifier HEDGEHOG_BLINK = TyEzhMenu.id("textures/gui/hedgehog_blink.png");

	private static final int SKY_W = 480, SKY_H = 270;
	private static final int COMP_W = 400, COMP_H = 225;
	private static final int HOG_W = 78, HOG_H = 69;
	private static final int HOG_X = 211, HOG_Y = 190 - HOG_H;

	// ---------------------------------------------------------------- цвета (ARGB)
	private static final int C_BORDER = 0xFF5B4BC4;
	private static final int C_FILL = 0xFFF4F0FF;
	private static final int C_TEXT = 0xFF5A4AC8;
	private static final int C_HILITE = 0xFFFFFFFF;
	private static final int C_BOTTOM = 0xFFDCD4FA;
	private static final int C_SHADOW = 0xB07A5BC8;

	private static final int H_BORDER = 0xFFE0489A;
	private static final int H_FILL = 0xFFFFD6F0;
	private static final int H_TEXT = 0xFFC8307F;
	private static final int H_HILITE = 0xFFFFF0FA;
	private static final int H_BOTTOM = 0xFFFFB8E0;
	private static final int H_SHADOW = 0xB0C0508F;

	private static final int D_FILL = 0xFFE6E2EE;
	private static final int D_TEXT = 0xFFA49EB8;

	private static final String[] HEART = {
			".##.##.",
			"#######",
			"#######",
			".#####.",
			"..###..",
			"...#..."
	};

	private static final int SPLASH_COUNT = 12;
	private static final Random RANDOM = new Random();

	private static final Component COPYRIGHT = Component.literal("Copyright Mojang AB. Do not distribute!");

	// ---------------------------------------------------------------- состояние
	private final long openedAt = System.currentTimeMillis();
	private final Component splash;
	private final float[][] stars;
	private final float[][] floaters;
	private final List<Entry> entries = new ArrayList<>();
	private Component versionLine = Component.empty();

	/** Масштаб композиции и её левый верхний угол на экране. */
	private float s = 1f, ox = 0f, oy = 0f;

	private record Entry(Button button, Component label) {
	}

	public TyEzhTitleScreen() {
		super(Component.translatable("tyezh.title"));
		this.splash = Component.translatable("tyezh.splash." + RANDOM.nextInt(SPLASH_COUNT));

		Random r = new Random(1337);
		this.stars = new float[46][];
		for (int i = 0; i < stars.length; i++) {
			// x, y (0..1), фаза, скорость, размер
			stars[i] = new float[]{r.nextFloat(), r.nextFloat() * 0.8f, r.nextFloat() * 6.28f, 1.2f + r.nextFloat() * 2.2f, r.nextInt(3)};
		}
		this.floaters = new float[7][];
		for (int i = 0; i < floaters.length; i++) {
			// x (0..1), период, сдвиг, цвет
			floaters[i] = new float[]{r.nextFloat(), 10f + r.nextFloat() * 8f, r.nextFloat(), r.nextInt(3)};
		}
	}

	// ================================================================= init

	@Override
	protected void init() {
		this.s = Math.min(this.width / (float) COMP_W, this.height / (float) COMP_H) * 0.97f;
		this.ox = (this.width - COMP_W * s) / 2f;
		this.oy = (this.height - COMP_H * s) / 2f;

		String mcVersion = FabricLoader.getInstance().getModContainer("minecraft")
				.map(c -> c.getMetadata().getVersion().getFriendlyString())
				.orElse("26.2");
		this.versionLine = Component.translatable("tyezh.version", mcVersion);

		this.entries.clear();
		List<Object[]> defs = new ArrayList<>();
		defs.add(new Object[]{"tyezh.menu.singleplayer", (Runnable) () -> openVanilla("menu.singleplayer")});
		defs.add(new Object[]{"tyezh.menu.multiplayer", (Runnable) () -> openVanilla("menu.multiplayer")});
		defs.add(new Object[]{"tyezh.menu.realms", (Runnable) () -> openVanilla("menu.online")});
		if (FabricLoader.getInstance().isModLoaded("modmenu")) {
			defs.add(new Object[]{"tyezh.menu.mods", (Runnable) () -> openVanilla("modmenu.title")});
		}
		defs.add(new Object[]{"tyezh.menu.options", (Runnable) () -> openVanilla("menu.options")});
		defs.add(new Object[]{"tyezh.menu.quit", (Runnable) () -> this.minecraft.stop()});

		int n = defs.size();
		float top = 72f, bottom = 198f;
		float gap = n > 5 ? 4f : 5f;
		float bh = (bottom - top - gap * (n - 1)) / n;

		for (int i = 0; i < n; i++) {
			String key = (String) defs.get(i)[0];
			Runnable action = (Runnable) defs.get(i)[1];
			Component label = Component.translatable(key);

			float by = top + i * (bh + gap);
			int x = Math.round(ox + 302f * s);
			int y = Math.round(oy + by * s);
			int w = Math.round(90f * s);
			int h = Math.max(12, Math.round(bh * s));

			Button button = Button.builder(label, b -> action.run()).bounds(x, y, w, h).build();
			// Ванильная кнопка остаётся рабочей (мышь, Tab/Enter, озвучка),
			// но становится невидимой — рисуем её сами в extractRenderState.
			button.setAlpha(0f);
			this.addRenderableWidget(button);
			this.entries.add(new Entry(button, label));
		}
	}

	/**
	 * Открывает ванильный TitleScreen «на мгновение» и нажимает в нём кнопку
	 * с нужным ключом перевода. Так сохраняется вся ванильная логика
	 * (предупреждение о сетевой игре, проверки Realms, кнопка ModMenu и т.п.),
	 * а кнопка «Назад» в любом подменю вернёт в наше меню — миксин подменит экран.
	 */
	private void openVanilla(String translationKey) {
		Minecraft mc = this.minecraft;
		TitleScreen vanilla = new TitleScreen();

		TyEzhMenu.bypassReplacement = true;
		try {
			mc.gui.setScreen(vanilla);
		} finally {
			TyEzhMenu.bypassReplacement = false;
		}

		for (GuiEventListener child : vanilla.children()) {
			if (child instanceof AbstractButton button && hasKey(button.getMessage(), translationKey)) {
				if (button.active) {
					// Обычные Button не используют аргумент ввода — достаточно null.
					button.onPress(null);
				}
				break;
			}
		}

		// Кнопка не нашлась или неактивна — возвращаемся в наше меню.
		if (mc.gui.screen() == vanilla) {
			mc.gui.setScreen(new TyEzhTitleScreen());
		}
	}

	private static boolean hasKey(Component component, String key) {
		if (component.getContents() instanceof TranslatableContents tc && tc.getKey().startsWith(key)) {
			return true;
		}
		for (Component sibling : component.getSiblings()) {
			if (hasKey(sibling, key)) {
				return true;
			}
		}
		return false;
	}

	@Override
	public boolean shouldCloseOnEsc() {
		return false;
	}

	// ================================================================= фон

	private float time() {
		return (System.currentTimeMillis() - openedAt) / 1000f;
	}

	@Override
	public void extractBackground(GuiGraphicsExtractor g, int mouseX, int mouseY, float partialTick) {
		// Без super: никакой ванильной панорамы и размытия.
		float t = time();

		// --- небо (cover, без искажения пропорций)
		float sk = Math.max(this.width / (float) SKY_W, this.height / (float) SKY_H);
		float skyX = (this.width - SKY_W * sk) / 2f;
		float skyY = (this.height - SKY_H * sk) / 2f;

		g.pose().pushMatrix();
		g.pose().translate(skyX, skyY);
		g.pose().scale(sk, sk);
		g.blit(RenderPipelines.GUI_TEXTURED, SKY, 0, 0, 0f, 0f, SKY_W, SKY_H, SKY_W, SKY_H);

		// --- облака, медленно плывущие вправо (две копии для бесшовности)
		float drift = (t * 5f) % SKY_W;
		g.pose().pushMatrix();
		g.pose().translate(drift, 0f);
		g.blit(RenderPipelines.GUI_TEXTURED, CLOUDS, 0, 0, 0f, 0f, SKY_W, SKY_H, SKY_W, SKY_H);
		g.blit(RenderPipelines.GUI_TEXTURED, CLOUDS, -SKY_W, 0, 0f, 0f, SKY_W, SKY_H, SKY_W, SKY_H);
		g.pose().popMatrix();
		g.pose().popMatrix();

		// --- мерцающие звёздочки
		int px = Math.max(1, Math.round(sk));
		for (float[] st : stars) {
			float b = 0.5f + 0.5f * (float) Math.sin(t * st[3] + st[2]);
			if (b < 0.25f) {
				continue;
			}
			int a = (int) (b * 230f);
			int color = (a << 24) | (st[4] == 0 ? 0xFFFFFF : st[4] == 1 ? 0xFFF4C9 : 0xD9F6FF);
			int cx = Math.round(st[0] * this.width);
			int cy = Math.round(st[1] * this.height);
			int arm = b > 0.8f ? 2 : 1;
			g.fill(cx - arm * px, cy, cx + (arm + 1) * px, cy + px, color);
			g.fill(cx, cy - arm * px, cx + px, cy + (arm + 1) * px, color);
		}

		// --- всплывающие сердечки
		for (float[] f : floaters) {
			float phase = ((t / f[1]) + f[2]) % 1f;
			int hx = Math.round(f[0] * this.width + (float) Math.sin(t * 1.3f + f[2] * 10f) * 6f * px);
			int hy = Math.round(this.height + 10 * px - phase * (this.height + 30 * px));
			float fade = phase < 0.15f ? phase / 0.15f : phase > 0.8f ? (1f - phase) / 0.2f : 1f;
			int a = (int) (fade * 170f);
			int rgb = f[3] == 0 ? 0xFF9ED8 : f[3] == 1 ? 0x8FE8FF : 0xFFFFFF;
			pixelHeart(g, hx, hy, px, (a << 24) | rgb);
		}

		// --- композиция: окна, логотип, ёжик
		g.pose().pushMatrix();
		g.pose().translate(ox, oy);
		g.pose().scale(s, s);
		g.blit(RenderPipelines.GUI_TEXTURED, PANEL, 0, 0, 0f, 0f, COMP_W, COMP_H, COMP_W, COMP_H);

		float bob = (float) Math.sin(t * 2.2f) * 1.2f;
		boolean blink = (t % 4.3f) < 0.16f;
		g.pose().pushMatrix();
		g.pose().translate(0f, bob);
		g.blit(RenderPipelines.GUI_TEXTURED, blink ? HEDGEHOG_BLINK : HEDGEHOG,
				HOG_X, HOG_Y, 0f, 0f, HOG_W, HOG_H, HOG_W, HOG_H);
		g.pose().popMatrix();
		g.pose().popMatrix();
	}

	// ================================================================= элементы

	@Override
	public void extractRenderState(GuiGraphicsExtractor g, int mouseX, int mouseY, float partialTick) {
		float t = time();

		// --- заголовки окон
		int tk = Math.max(1, Math.round(s * 0.75f));
		windowTitle(g, Component.translatable("tyezh.window.main"), 164, 18, tk);
		windowTitle(g, Component.translatable("tyezh.window.walk"), 6, 10, tk);
		windowTitle(g, Component.translatable("tyezh.window.babies"), 6, 146, tk);
		windowTitle(g, Component.translatable("tyezh.window.status"), 318, 2, tk);

		// --- окно статуса
		drawStatus(g, t);

		// --- сплэш у логотипа
		float pulse = 1f + 0.07f * Math.abs((float) Math.sin(t * 4.7f));
		float sk = Math.max(1f, s * 0.62f) * pulse;
		int sw = this.font.width(this.splash);
		g.pose().pushMatrix();
		g.pose().translate(ox + 284f * s, oy + 96f * s);
		g.pose().rotate(-0.33f);
		g.pose().scale(sk, sk);
		g.text(this.font, this.splash, -sw / 2, -4, 0xFFFFF36B, true);
		g.pose().popMatrix();

		// --- кнопки
		for (Entry e : this.entries) {
			drawButton(g, e);
		}

		// --- подписи внизу
		g.text(this.font, this.versionLine, 3, this.height - 10, 0xFF6E5BD6, false);
		int cw = this.font.width(COPYRIGHT);
		g.text(this.font, COPYRIGHT, this.width - cw - 3, this.height - 10, 0xFF6E5BD6, false);

		// --- невидимые ванильные кнопки (ввод, фокус, озвучка)
		super.extractRenderState(g, mouseX, mouseY, partialTick);
	}

	private void windowTitle(GuiGraphicsExtractor g, Component text, float cx, float cy, int k) {
		float x = ox + (cx + 4f) * s;
		float y = oy + (cy + 6.5f) * s - 4f * k;
		g.pose().pushMatrix();
		g.pose().translate(x, y);
		g.pose().scale(k, k);
		g.text(this.font, text, 0, 0, 0xFFFFFFFF, true);
		g.pose().popMatrix();
	}

	private void drawStatus(GuiGraphicsExtractor g, float t) {
		int k = Math.max(1, Math.round(s * 0.7f));
		int left = Math.round(ox + 322f * s);
		int right = Math.round(ox + 392f * s);

		compLabel(g, Component.translatable("tyezh.status.online"), left, Math.round(oy + 15f * s), k, 0xFF5A4AC8);

		int cute = 94 + Math.round(5f * (float) Math.sin(t * 0.9f));
		int sleepy = 15 + Math.round(4f * (float) Math.sin(t * 0.4f + 1f));
		Object[][] rows = {
				{"tyezh.status.needles", 100, 0xFFFF6FB5},
				{"tyezh.status.cute", cute, 0xFF6FCBF0},
				{"tyezh.status.sleepy", sleepy, 0xFFA88CF5}
		};
		for (int i = 0; i < rows.length; i++) {
			int rowY = Math.round(oy + (26f + i * 13f) * s);
			int value = (Integer) rows[i][1];
			int color = (Integer) rows[i][2];
			compLabel(g, Component.translatable((String) rows[i][0]), left, rowY, k, 0xFF5A4AC8);
			Component val = Component.literal(value + "%");
			int vw = this.font.width(val) * k;
			compLabel(g, val, right - vw, rowY, k, color);

			int barTop = rowY + 9 * k;
			int barH = Math.max(3, Math.round(3f * s));
			g.fill(left - 1, barTop - 1, right + 1, barTop + barH + 1, C_BORDER);
			g.fill(left, barTop, right, barTop + barH, 0xFFEDE6FF);
			int filled = left + Math.round((right - left) * value / 100f);
			g.fill(left, barTop, filled, barTop + barH, color);
			g.fill(left, barTop, filled, barTop + Math.max(1, barH / 3), 0x66FFFFFF);
		}
	}

	private void compLabel(GuiGraphicsExtractor g, Component text, int x, int y, int k, int color) {
		g.pose().pushMatrix();
		g.pose().translate(x, y);
		g.pose().scale(k, k);
		g.text(this.font, text, 0, 0, color, false);
		g.pose().popMatrix();
	}

	private void drawButton(GuiGraphicsExtractor g, Entry e) {
		Button b = e.button();
		boolean active = b.active;
		boolean hov = active && b.isHoveredOrFocused();

		int x = b.getX(), y = b.getY(), w = b.getWidth(), h = b.getHeight();
		int u = Math.max(1, Math.round(s * 0.8f));
		if (hov) {
			x -= u; // лёгкий «выезд» влево при наведении
		}

		int border = hov ? H_BORDER : C_BORDER;
		int fill = !active ? D_FILL : hov ? H_FILL : C_FILL;
		int hilite = hov ? H_HILITE : C_HILITE;
		int bottom = hov ? H_BOTTOM : C_BOTTOM;
		int shadow = hov ? H_SHADOW : C_SHADOW;
		int text = !active ? D_TEXT : hov ? H_TEXT : C_TEXT;

		g.fill(x + 2 * u, y + 2 * u, x + w + 2 * u, y + h + 2 * u, shadow);
		g.fill(x, y, x + w, y + h, border);
		g.fill(x + u, y + u, x + w - u, y + h - u, fill);
		g.fill(x + u, y + u, x + w - u, y + 2 * u, hilite);
		g.fill(x + u, y + h - 2 * u, x + w - u, y + h - u, bottom);

		// подпись: целочисленный масштаб, при нехватке места — дробный
		Component label = e.label();
		int tw = this.font.width(label);
		float k = Math.max(1, (int) (h / 22f));
		while (k > 1 && tw * k > w - 8 * u) {
			k -= 1f;
		}
		if (tw * k > w - 6 * u) {
			k = (w - 6f * u) / tw;
		}
		float textW = tw * k;
		float tx = x + (w - textW) / 2f;
		float ty = y + h / 2f - 4f * k;

		g.pose().pushMatrix();
		g.pose().translate(tx, ty);
		g.pose().scale(k, k);
		g.text(this.font, label, 0, 0, text, false);
		g.pose().popMatrix();

		// сердечко слева при наведении
		if (hov && (w - textW) / 2f > 9 * u) {
			pixelHeart(g, x + 3 * u, y + h / 2 - 3 * u, u, 0xFFFF5FA8);
		}
	}

	private static void pixelHeart(GuiGraphicsExtractor g, int x, int y, int u, int color) {
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
