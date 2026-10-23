---
name: bifrost-credentials
description: Set up or repair iOS and Android signing and store-upload credentials for NativePHP Mobile or SuperNative apps in Bifrost. Prefer supported Bifrost MCP operations and managed signing for new apps, with browser and manual credential fallbacks. Builds, distribution, credential revocation, and key rotation require their own task authorization.
---

# Bifrost credentials

Set up signing without replacing working credentials or expanding store access by accident. Use current Bifrost documentation and the connected tools' schemas; wizard labels and tool names can change.

## Discover before creating

1. Inspect the app's configuration for its name and identifiers, without displaying secrets. Find the intended Bifrost team and project, existing signing credentials, team store keys, and store app records. Resolve conflicting identifiers before making changes. Reuse a clearly identified team; ask when several remain plausible.
2. Establish which platforms and distribution channels the user wants, whether each app has shipped, and whether store upload or signing alone is needed. Batch missing identity and permission decisions where practical; retain the user's answers throughout the task.
3. Prefer Bifrost-managed signing for a new app. For existing apps, preserve their signing identity and registered Android upload key. Reuse suitable team keys and Apple certificates before creating more. Do not start with Artisan unless local credential generation is actually needed.
4. Before creating or downloading sensitive files, create a private `credentials/` directory and verify that it and `.env` are ignored and untracked. Check actual Git ignore behavior, not just the presence of a rule.

## Choose the execution surface

Prefer a connected Bifrost MCP server for operations its live schema supports. Read [MCP access and credential transport](references/mcp.md) when connecting or sending credentials. Do not assume a credential-upload tool also supports managed creation, renewal, team-key administration, or credential validation. Fall back to the Bifrost website for missing capabilities, and to Apple or Google for store-side tasks.

Read only the applicable platform reference:

- [iOS](references/ios.md): managed signing, certificate reuse, profile matching, App Store Connect, and manual fallback.
- [Android](references/android.md): managed upload keys, existing apps, Play permissions, and first-upload requirements.
- [Browser troubleshooting](references/browser-troubleshooting.md): uploads, downloads, and verifying asynchronous changes.
- [Build configuration](references/build-configuration.md): only when the user also requests build configuration. Credential setup alone does not authorize that work.

## Human decisions and secrets

- The user handles sign-ins, 2FA, legal declarations, and entry of new or existing signing passwords in interactive browser/terminal flows. Do not invent passwords. Bifrost generating passwords as part of its managed-keystore workflow is supported; do not reveal or rotate them just to obtain a local copy.
- Before granting new store access, explain the recipient, apps, and permissions and obtain the user's scope choice. Distinguish testing from production publishing and app access from account-wide access. Reuse that choice unless the action or scope changes, subject to the host's confirmation policy.
- MCP transmission is an explicit exception to interactive password entry: after the user chooses that transport with disclosure of transcript exposure, read required existing values from the authorized local source and pass them directly to the tool. Never ask for passwords or private keys in chat, print them, or place them in reports.
- Treat the credential directory as sensitive. Private keys, P12s, keystores, service-account JSON, and passwords must not enter source control, logs, shared screenshots, or distributed app bundles. Certificates and CSRs are not private keys, but can contain identifying metadata; do not publish credential artifacts as examples.
- Apple API private keys and Google service-account private keys cannot be downloaded again from the provider after creation. Store downloads promptly in the ignored directory and arrange a secure backup. A team key already stored in Bifrost need not be downloaded again merely to reuse it.
- Never revoke a certificate or key, reset an upload key, rotate a password, or replace a working signing configuration as a troubleshooting shortcut. Inspect dependents and get authorization for that specific change. A missing local key file is not proof that the store key is unused.
- Skip Firebase/FCM unless requested or supplied as part of the task. Do not enable speculative app capabilities.

## Verify and report

Check the saved credential record for the intended app, platform, distribution type, and signing material. Where supported, run Bifrost's **Check credentials** operation against the store; distinguish a stored record from a successful API validation. Verify ignore rules and backup filenames without displaying contents.

Report platform identifiers, profile/key names or service-account email, managed versus uploaded signing, files saved (filenames only), and validation actually performed. Report credentials, store API access, build configuration, and first-build status separately. Credential setup can be complete while onboarding remains partly unfinished.

Do not spend credits, start workflows/builds, or distribute an app merely to verify setup. Report Android's first manual Play upload when outstanding. Authorization for further work may already be present in the same request: if the user asked for credentials and a build or distribution, continue that authorized work once prerequisites are ready, subject to the host's confirmation policy. Do not turn it into an unnecessary new approval or silently leave it unfinished.
