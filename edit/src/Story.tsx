import { AbsoluteFill, Easing, interpolate, useCurrentFrame, useVideoConfig } from "remotion";
import { archivo, azeret, BRASS, PAPER } from "./theme";

// Narrative overlay: letterbox, chapter index, headlines and technical callouts.
// All times are master frames (30 fps); anchors are in 1920x1080 pixels.

const clamp = { extrapolateLeft: "clamp", extrapolateRight: "clamp" } as const;
const easeOut = Easing.bezier(0.16, 1, 0.3, 1);
const BAR = 112;

type Chapter = { numeral: string; name: string; from: number; to: number };

const CHAPTERS: Chapter[] = [
  { numeral: "I", name: "Repos", from: 45, to: 300 },
  { numeral: "II", name: "Tension", from: 300, to: 540 },
  { numeral: "III", name: "Équilibre", from: 540, to: 705 },
  { numeral: "IV", name: "Lumière", from: 705, to: 840 },
];

// x is the left margin, or the right margin when align is "right"; placed in empty areas of each shot.
type Headline = { lines: string[]; from: number; to: number; x: number; y: number; size: number; align?: "left" | "center" | "right" };

const HEADLINES: Headline[] = [
  { lines: ["Certains objets attendent."], from: 8, to: 44, x: 0, y: 510, size: 54, align: "center" },
  { lines: ["Au repos,", "jamais inerte."], from: 205, to: 294, x: 170, y: 430, size: 92 },
  { lines: ["Toute sa force", "tient dans la retenue."], from: 318, to: 412, x: 170, y: 220, size: 84 },
  { lines: ["Elle cède."], from: 490, to: 536, x: 170, y: 190, size: 92 },
  { lines: ["Puis trouve sa place.", "Et n'en bouge plus."], from: 562, to: 652, x: 170, y: 650, size: 84 },
  { lines: ["Alors seulement,", "la lumière."], from: 760, to: 840, x: 170, y: 190, size: 80, align: "right" },
];

type Callout = { index: string; title: string; detail: string; from: number; to: number; anchor: [number, number]; label: [number, number] };

const CALLOUTS: Callout[] = [
  { index: "01", title: "Ressort", detail: "Acier trempé · 42 spires", from: 62, to: 130, anchor: [1135, 470], label: [1430, 360] },
  { index: "02", title: "Pivot", detail: "Laiton massif, tourné", from: 146, to: 192, anchor: [1300, 330], label: [1480, 230] },
  { index: "03", title: "Tension", detail: "Équilibrée au gramme près", from: 428, to: 477, anchor: [1190, 520], label: [1440, 400] },
  { index: "04", title: "Interrupteur", detail: "Une seule pression", from: 663, to: 703, anchor: [1150, 520], label: [1400, 420] },
];

const Word: React.FC<{ word: string; delay: number; from: number; to: number }> = ({ word, delay, from, to }) => {
  const frame = useCurrentFrame();
  const t0 = from + delay;
  const rise = interpolate(frame, [t0, t0 + 22], [105, 0], { ...clamp, easing: easeOut });
  const out = interpolate(frame, [to - 12, to], [1, 0], clamp);
  const blur = interpolate(frame, [to - 12, to], [0, 8], clamp);
  return (
    <span style={{ display: "inline-block", overflow: "hidden", verticalAlign: "bottom", paddingBottom: "0.08em" }}>
      <span style={{ display: "inline-block", transform: `translateY(${rise}%)`, opacity: out, filter: `blur(${blur}px)` }}>
        {word}&nbsp;
      </span>
    </span>
  );
};

const HeadlineView: React.FC<{ h: Headline }> = ({ h }) => {
  const frame = useCurrentFrame();
  if (frame < h.from || frame > h.to) return null;
  const align = h.align ?? "left";
  const tracking = interpolate(frame, [h.from, h.to], [0.6, 0], clamp);
  let wordIndex = 0;
  return (
    <div
      style={{
        position: "absolute",
        left: align === "left" ? h.x : align === "center" ? 0 : undefined,
        right: align === "right" ? h.x : align === "center" ? 0 : undefined,
        top: h.y,
        textAlign: align,
        fontFamily: archivo,
        fontWeight: 400,
        fontSize: h.size,
        lineHeight: 1.02,
        letterSpacing: `${tracking}px`,
        color: PAPER,
        textShadow: "0 2px 30px rgba(0,0,0,0.6)",
      }}
    >
      {h.lines.map((line, li) => (
        <div key={line} style={{ opacity: li === 0 ? 1 : 0.62 }}>
          {line.split(" ").map((word) => {
            const delay = wordIndex++ * 4;
            return <Word key={`${word}-${delay}`} word={word} delay={delay} from={h.from} to={h.to} />;
          })}
        </div>
      ))}
    </div>
  );
};

const CalloutView: React.FC<{ c: Callout }> = ({ c }) => {
  const frame = useCurrentFrame();
  if (frame < c.from || frame > c.to) return null;
  const [ax, ay] = c.anchor;
  const [lx, ly] = c.label;
  const elbowX = lx - 24;
  const dot = interpolate(frame, [c.from, c.from + 8], [0, 1], { ...clamp, easing: easeOut });
  const draw = interpolate(frame, [c.from + 4, c.from + 22], [0, 1], { ...clamp, easing: easeOut });
  const text = interpolate(frame, [c.from + 16, c.from + 28], [0, 1], clamp);
  const out = interpolate(frame, [c.to - 10, c.to], [1, 0], clamp);
  const pathLength = Math.hypot(elbowX - ax, ly - ay) + 24 + 260;
  return (
    <AbsoluteFill style={{ opacity: out }}>
      <svg width={1920} height={1080} style={{ position: "absolute" }}>
        <circle cx={ax} cy={ay} r={16 * dot} fill="none" stroke={BRASS} strokeWidth={1.5} opacity={0.9} />
        <circle cx={ax} cy={ay} r={3.5 * dot} fill={PAPER} />
        <path
          d={`M ${ax} ${ay} L ${elbowX} ${ly} L ${lx + 260} ${ly}`}
          fill="none"
          stroke={PAPER}
          strokeWidth={1.2}
          strokeDasharray={pathLength}
          strokeDashoffset={pathLength * (1 - draw)}
          opacity={0.85}
        />
      </svg>
      <div
        style={{
          position: "absolute",
          left: lx,
          top: ly - 46,
          fontFamily: azeret,
          color: PAPER,
          opacity: text,
          transform: `translateY(${(1 - text) * 6}px)`,
        }}
      >
        <div style={{ fontSize: 15, letterSpacing: 4, color: BRASS, textTransform: "uppercase" }}>
          {c.index} — {c.title}
        </div>
      </div>
      <div
        style={{
          position: "absolute",
          left: lx,
          top: ly + 12,
          fontFamily: azeret,
          fontWeight: 300,
          fontSize: 20,
          letterSpacing: 1,
          color: PAPER,
          opacity: text * 0.85,
        }}
      >
        {c.detail}
      </div>
    </AbsoluteFill>
  );
};

const ChapterBar: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "absolute", left: 170, right: 170, bottom: 40, display: "flex", gap: 28 }}>
      {CHAPTERS.map((ch) => {
        const progress = interpolate(frame, [ch.from, ch.to], [0, 1], clamp);
        const isActive = frame >= ch.from && frame < ch.to;
        return (
          <div key={ch.numeral} style={{ flex: 1 }}>
            <div style={{ height: 1, background: "rgba(239,235,228,0.18)", position: "relative" }}>
              <div style={{ position: "absolute", inset: 0, width: `${progress * 100}%`, background: isActive ? BRASS : PAPER, opacity: isActive ? 1 : 0.5 }} />
            </div>
            <div
              style={{
                marginTop: 12,
                fontFamily: azeret,
                fontSize: 13,
                letterSpacing: 3,
                textTransform: "uppercase",
                color: PAPER,
                opacity: isActive ? 0.95 : 0.32,
              }}
            >
              {ch.numeral}&nbsp;&nbsp;{ch.name}
            </div>
          </div>
        );
      })}
    </div>
  );
};

const Letterbox: React.FC<{ fadeOutFrom: number | null }> = ({ fadeOutFrom }) => {
  const frame = useCurrentFrame();
  const enter = interpolate(frame, [36, 66], [0, 1], { ...clamp, easing: easeOut });
  const leave = fadeOutFrom === null ? 1 : interpolate(frame, [fadeOutFrom, fadeOutFrom + 14], [1, 0], clamp);
  const h = BAR * enter;
  const meta = { fontFamily: azeret, fontSize: 13, letterSpacing: 4, textTransform: "uppercase" as const, color: PAPER };
  return (
    <AbsoluteFill style={{ opacity: leave }}>
      <div style={{ position: "absolute", top: 0, left: 0, right: 0, height: h, background: "#000" }} />
      <div style={{ position: "absolute", bottom: 0, left: 0, right: 0, height: h, background: "#000" }} />
      <div style={{ position: "absolute", top: 46, left: 170, right: 170, display: "flex", justifyContent: "space-between", opacity: enter }}>
        <span style={{ ...meta, opacity: 0.9 }}>Tensil</span>
        <span style={{ ...meta, opacity: 0.45 }}>Lampe articulée — N° 001</span>
      </div>
      <div style={{ opacity: enter }}>
        <ChapterBar />
      </div>
    </AbsoluteFill>
  );
};

// Warm bloom the moment the bulb switches on (about 24.95 s).
const LightOn: React.FC = () => {
  const frame = useCurrentFrame();
  const glow = interpolate(frame, [747, 752, 790], [0, 0.28, 0], clamp);
  return (
    <AbsoluteFill
      style={{
        background: "radial-gradient(ellipse at 28% 82%, rgba(255,190,120,0.9), transparent 55%)",
        mixBlendMode: "screen",
        opacity: glow,
      }}
    />
  );
};

export const Story: React.FC<{ endCardFrom: number | null }> = ({ endCardFrom }) => {
  const { durationInFrames } = useVideoConfig();
  const headlines = HEADLINES.map((h) => ({ ...h, to: Math.min(h.to, endCardFrom ?? durationInFrames) }));
  return (
    <AbsoluteFill>
      <LightOn />
      <Letterbox fadeOutFrom={endCardFrom === null ? null : endCardFrom - 10} />
      {CALLOUTS.map((c) => (
        <CalloutView key={c.index} c={c} />
      ))}
      {headlines.map((h) => (
        <HeadlineView key={h.lines[0]} h={h} />
      ))}
    </AbsoluteFill>
  );
};
