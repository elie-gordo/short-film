import { loadFont as loadArchivo } from "@remotion/google-fonts/ArchivoNarrow";
import { loadFont as loadAzeret } from "@remotion/google-fonts/AzeretMono";
import { loadFont as loadInter } from "@remotion/google-fonts/Inter";

export const archivo = loadArchivo("normal", { weights: ["400", "600", "700"] }).fontFamily;
export const azeret = loadAzeret("normal", { weights: ["300", "400"] }).fontFamily;
export const inter = loadInter("normal", { weights: ["400"] }).fontFamily;

export const NIGHT = "#0f0e0d";
export const PAPER = "#efebe4";
export const OXIDE = "#e0714f";
export const BRASS = "#c9a46a";
