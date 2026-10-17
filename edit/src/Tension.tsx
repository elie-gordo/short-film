import {
  AbsoluteFill,
  Audio,
  Easing,
  interpolate,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { Story } from "./Story";
import { archivo, azeret, inter, NIGHT, OXIDE, PAPER } from "./theme";

export const FPS = 30;
// 31.5 s: the end card holds long enough for the last voice-over line to breathe.
export const TOTAL_FRAMES = 945;
// Without the end card the film stops after P10's slowed tail.
export const NO_END_CARD_FRAMES = 855;


// Master timeline from blender/film.py SHOTS (frame 1 = 0 here). Seedance drafts
// cover each shot's "ref" range, so `skip` drops the 0.5 s lead-in.
type Shot = { src: string; from: number; len: number; skip?: number; grade: string };

const SEEDANCE_GRADE = "contrast(1.08) saturate(0.9) brightness(0.96)";
const EEVEE_GRADE = "contrast(1.02) saturate(0.95)";

const SHOTS: Shot[] = [
  { src: "P02.mp4", from: 45, len: 90, grade: EEVEE_GRADE },
  { src: "P03.mp4", from: 135, len: 60, grade: EEVEE_GRADE },
  { src: "P04.mp4", from: 195, len: 105, skip: 15, grade: SEEDANCE_GRADE },
  { src: "P05.mp4", from: 300, len: 120, skip: 15, grade: SEEDANCE_GRADE },
  { src: "P06.mp4", from: 420, len: 60, grade: EEVEE_GRADE },
  { src: "P07.mp4", from: 480, len: 60, skip: 15, grade: SEEDANCE_GRADE },
  { src: "P08.mp4", from: 540, len: 120, skip: 15, grade: SEEDANCE_GRADE },
  { src: "P09.mp4", from: 660, len: 45, grade: EEVEE_GRADE },
  { src: "P10.mp4", from: 705, len: 105, grade: SEEDANCE_GRADE },
];

const P10_SLOW = { from: 810, len: 30, skip: 105, rate: 0.5 };
const END_CARD_FROM = 825;

const Clip: React.FC<{ shot: Shot }> = ({ shot }) => (
  <AbsoluteFill style={{ filter: shot.grade }}>
    <OffthreadVideo
      src={staticFile(shot.src)}
      startFrom={shot.skip ?? 0}
      muted
      style={{ width: "100%", height: "100%", objectFit: "cover" }}
    />
  </AbsoluteFill>
);

const Grain: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <AbsoluteFill style={{ mixBlendMode: "overlay", opacity: 0.12, pointerEvents: "none" }}>
      <svg width="100%" height="100%">
        <filter id="grain">
          <feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves={2} seed={frame} />
          <feColorMatrix type="saturate" values="0" />
        </filter>
        <rect width="100%" height="100%" filter="url(#grain)" />
      </svg>
    </AbsoluteFill>
  );
};

const Vignette: React.FC = () => (
  <AbsoluteFill
    style={{ background: "radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,0.55) 100%)" }}
  />
);

const rise = (frame: number, start: number) => ({
  opacity: interpolate(frame, [start, start + 18], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
  transform: `translateY(${interpolate(frame, [start, start + 18], [14, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  })}px)`,
});

const EndCard: React.FC = () => {
  const frame = useCurrentFrame();
  const rule = interpolate(frame, [6, 30], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.out(Easing.cubic),
  });
  return (
    <AbsoluteFill style={{ background: NIGHT, color: PAPER, justifyContent: "center", padding: "0 180px" }}>
      <div style={{ fontFamily: archivo, fontWeight: 700, fontSize: 200, letterSpacing: 18, lineHeight: 1, ...rise(frame, 0) }}>
        TENSIL
      </div>
      <div style={{ height: 4, width: 520 * rule, background: OXIDE, margin: "28px 0 30px" }} />
      <div style={{ fontFamily: archivo, fontWeight: 600, fontSize: 64, ...rise(frame, 10) }}>
        Tenue par la tension.
      </div>
      <div style={{ fontFamily: inter, fontSize: 30, color: "rgba(239,235,228,0.75)", marginTop: 14, ...rise(frame, 18) }}>
        Lampe de bureau articulée
      </div>
      <div
        style={{
          position: "absolute",
          left: 180,
          right: 180,
          bottom: 90,
          display: "flex",
          justifyContent: "space-between",
          fontFamily: azeret,
          fontSize: 20,
          letterSpacing: 1,
          opacity: interpolate(frame, [24, 42], [0, 0.6], { extrapolateLeft: "clamp", extrapolateRight: "clamp" }),
        }}
      >
        <span>Projet de démonstration — marque fictive</span>
        <span>tensil-store.vercel.app</span>
      </div>
    </AbsoluteFill>
  );
};

type TensionProps = { withEndCard: boolean };

export const Tension: React.FC<TensionProps> = ({ withEndCard }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const fadeFromBlack = interpolate(frame, [45, 60], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const toEndCard = interpolate(frame, [END_CARD_FROM, END_CARD_FROM + 12], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const finalFade = interpolate(frame, [durationInFrames - 15, durationInFrames], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ background: "#000" }}>
      {SHOTS.map((shot) => (
        <Sequence key={shot.src} from={shot.from} durationInFrames={shot.len} premountFor={30}>
          <Clip shot={shot} />
        </Sequence>
      ))}
      <Sequence from={P10_SLOW.from} durationInFrames={P10_SLOW.len}>
        <AbsoluteFill style={{ filter: SEEDANCE_GRADE }}>
          <OffthreadVideo
            src={staticFile("P10.mp4")}
            startFrom={P10_SLOW.skip}
            playbackRate={P10_SLOW.rate}
            muted
            style={{ width: "100%", height: "100%", objectFit: "cover" }}
          />
        </AbsoluteFill>
      </Sequence>
      <Vignette />
      <Grain />
      <AbsoluteFill style={{ background: "#000", opacity: frame < 45 ? 1 : fadeFromBlack }} />
      <Story endCardFrom={withEndCard ? END_CARD_FROM : null} />
      {withEndCard && (
        <Sequence from={END_CARD_FROM}>
          <AbsoluteFill style={{ opacity: toEndCard }}>
            <EndCard />
          </AbsoluteFill>
        </Sequence>
      )}
      <AbsoluteFill style={{ background: "#000", opacity: finalFade }} />
      <Soundtrack />
    </AbsoluteFill>
  );
};

// Voice-over lines (ElevenLabs), each starting just as its headline appears in Story.tsx.
// `len` is the clip length in frames, used to duck the music under the voice.
const VOICE = [
  { src: "vo_01.mp3", at: 8, len: 83 },
  { src: "vo_02.mp3", at: 206, len: 64 },
  { src: "vo_03.mp3", at: 320, len: 81 },
  { src: "vo_04.mp3", at: 491, len: 45 },
  { src: "vo_05.mp3", at: 561, len: 90 },
  { src: "vo_06.mp3", at: 750, len: 83 },
  { src: "vo_07.mp3", at: 840, len: 83 },
];

const MUSIC_LEVEL = 0.6;
const MUSIC_DUCKED = 0.27;
const SFX_LEVEL = 0.45;
const DUCK_ATTACK = 6;
const DUCK_RELEASE = 14;
const END_FADE = 20; // starts after the last voice line in both versions

const voiceActivity = (f: number) =>
  Math.max(
    0,
    ...VOICE.map((v) =>
      interpolate(f, [v.at - DUCK_ATTACK, v.at, v.at + v.len, v.at + v.len + DUCK_RELEASE], [0, 1, 1, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      }),
    ),
  );

const Soundtrack: React.FC = () => {
  const { durationInFrames } = useVideoConfig();
  const tail = (f: number) =>
    interpolate(f, [durationInFrames - END_FADE, durationInFrames], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <>
      <Audio
        src={staticFile("musique.mp3")}
        volume={(f) => (MUSIC_LEVEL - (MUSIC_LEVEL - MUSIC_DUCKED) * voiceActivity(f)) * tail(f)}
      />
      <Audio src={staticFile("sfx.wav")} volume={(f) => SFX_LEVEL * tail(f)} />
      {VOICE.map((v) => (
        <Sequence key={v.src} from={v.at}>
          <Audio src={staticFile(v.src)} />
        </Sequence>
      ))}
    </>
  );
};
