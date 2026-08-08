import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import path from 'node:path';

const here = path.dirname(fileURLToPath(import.meta.url));
const validator = path.resolve(here, '..', 'validate_social_preset.mjs');
const valid = spawnSync('node', [validator, path.join(here, 'social-preset-valid.json')], { encoding: 'utf8' });
const invalid = spawnSync('node', [validator, path.join(here, 'social-preset-invalid.json')], { encoding: 'utf8' });
const fixtures = path.resolve(here, '..', '..', 'fixtures', 'social-preset');
const validFixtures = ['valid-landscape.json', 'valid-portrait.json', 'valid-square.json', 'color-injection.json'];
const invalidFixtures = ['unknown-preset.json', 'low-contrast.json', 'missing-media.json', 'text-in-crop-zone.json', 'text-overflow.json'];
const validResults = validFixtures.map(name => spawnSync('node', [validator, path.join(fixtures, name)], { encoding: 'utf8' }));
const invalidResults = invalidFixtures.map(name => spawnSync('node', [validator, path.join(fixtures, name)], { encoding: 'utf8' }));
if (valid.status !== 0 || invalid.status === 0 || validResults.some(r => r.status !== 0) || invalidResults.some(r => r.status === 0)) {
  console.error(valid.stderr || valid.stdout || invalid.stderr || invalid.stdout);
  process.exit(1);
}
console.log('OK: legacy manifests and platform preset fixtures validated');
