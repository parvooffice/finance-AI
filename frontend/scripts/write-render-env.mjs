import { writeFileSync } from 'node:fs';

const apiHost = process.env.API_HOST;
if (!apiHost) {
  throw new Error('API_HOST must be set to the public hostname of the Express API.');
}

writeFileSync('.env.production', `VITE_API_URL=https://${apiHost}/api\n`);
