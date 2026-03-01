import figlet from 'figlet';
import { theme } from './theme.js';

type BannerOptions = {
  name: string;
  version: string;
  tagline?: string;
  font?: figlet.Fonts;
};

export const showBanner = ({
  name,
  version,
  tagline,
  font = 'ANSI Shadow',
}: BannerOptions): void => {
  const art = figlet.textSync(name, { font });
  console.log(theme.primary(art));
  console.log(theme.dim(`  ${'░▒▓█'} CSV to JSON Converter ${'█▓▒░'}`));

  if (tagline) {
    console.log(theme.dim(`  ${tagline}`));
  }

  console.log(theme.dim(`  v${version}`));
  console.log();
};

export const showCompactBanner = (name: string, version: string): void => {
  console.log(`${theme.primary.bold(name)} ${theme.dim(`v${version}`)}`);
  console.log();
};
