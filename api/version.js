// /api/version — which deployment is this?
//
// Vercel stamps every deployment with the git commit it was built from, so a
// prototype can show reviewers exactly which version they are looking at.
//   GET /api/version -> { sha, short, ref, message, env, deployment, repo }
// Locally the same route is answered by designmd/tools/serve.mjs from `git`.
// Nothing here touches the database or any secret: all values are the public
// VERCEL_* build metadata.
const REPO = 'whymandesigns/opz-prototypes';

export default function handler(req, res) {
  const env = process.env;
  const sha = env.VERCEL_GIT_COMMIT_SHA || null;
  res.setHeader('Cache-Control', 'public, max-age=60');
  res.status(200).json({
    sha,
    short: sha ? sha.slice(0, 7) : null,
    ref: env.VERCEL_GIT_COMMIT_REF || null,
    message: (env.VERCEL_GIT_COMMIT_MESSAGE || '').split('\n')[0] || null,
    env: env.VERCEL_ENV || 'unknown',              // production | preview | development
    deployment: env.VERCEL_DEPLOYMENT_ID || null,   // unique even for a redeploy of the same commit
    repo: REPO,
  });
}
