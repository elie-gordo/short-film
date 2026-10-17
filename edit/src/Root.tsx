import { Composition } from "remotion";
import { Tension, FPS, TOTAL_FRAMES, NO_END_CARD_FRAMES } from "./Tension";

export const Root: React.FC = () => (
  <>
    <Composition
      id="Tension"
      component={Tension}
      durationInFrames={TOTAL_FRAMES}
      fps={FPS}
      width={1920}
      height={1080}
      defaultProps={{ withEndCard: true }}
    />
    <Composition
      id="TensionNoEndCard"
      component={Tension}
      durationInFrames={NO_END_CARD_FRAMES}
      fps={FPS}
      width={1920}
      height={1080}
      defaultProps={{ withEndCard: false }}
    />
  </>
);
