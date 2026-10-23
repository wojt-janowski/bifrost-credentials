# Bifrost credentials

An agent skill for setting up iOS and Android signing and store-upload credentials for NativePHP Mobile and SuperNative apps in Bifrost.

It prefers supported Bifrost MCP operations and managed signing for new apps, preserves existing signing identities, and guides the Apple and Google work that still happens outside Bifrost. Browser/manual procedures are fallbacks, not a requirement to generate every credential locally.

This is an independent community skill, not an official NativePHP or Bifrost product.

## Install and use

```sh
git clone https://github.com/wojt-janowski/bifrost-credentials.git
```

Install the resulting `bifrost-credentials` folder using your agent client's normal skill installation mechanism. The skill entrypoint is [SKILL.md](SKILL.md) at the repository root; keep its `references/` folder with it. [agents/openai.yaml](agents/openai.yaml) supplies optional Codex UI metadata. There is no required runtime package or bundled browser driver.

Example request:

> Use $bifrost-credentials to set up signing and store upload for my mobile app. Reuse existing team credentials where suitable.

The agent needs access to the app's configuration and whichever store accounts are involved. A connected Bifrost MCP server is preferred, but optional. Configure it through your client's supported OAuth flow using the [Bifrost connection guide](https://bifrost.nativephp.com/docs/mobile/teams/mcp). The skill does not install a server, enable team access, or grant store permissions on its own.

## What it handles

- Discovery of app identity, existing credentials, and team store keys.
- Managed iOS signing, reuse of an existing certificate, and manual CSR/P12/profile fallback.
- Managed Android upload keys, existing-key preservation, and secure backups.
- App Store Connect records and Play service-account permission decisions.
- Separate reporting of signing, store API validation, build configuration, and first-build readiness.
- Optional build-configuration guidance when explicitly requested.

Setting up credentials does not start builds, publish apps, rotate keys, or revoke certificates. The user handles sign-in/2FA, legal declarations, interactive signing-password entry, and access choices. An explicitly chosen MCP upload can transmit existing credentials through tool arguments after the exposure is explained.

The first Android AAB for a new Play app still needs a manual Play Console upload. Firebase/FCM setup is outside the default scope.

## Compatibility and evidence

Last checked: **2026-10-24**.

The browser-assisted workflow was exercised with uploaded iOS signing, a shared App Store Connect key, a managed Android keystore, and app-scoped Play access. Current official documentation was checked for managed signing, team keys, MCP, and build configuration. Bifrost MCP credential calls were **not** exercised in that session because that server was unavailable. The skill therefore discovers live tools and does not promise unverified managed-signing API methods.

Browser automation depends on the host's supported upload/download APIs. File-event timeouts can occur even when a download finishes; the troubleshooting reference includes verification and manual fallbacks. Wizard labels and API schemas are not fixed contracts.

## Validate changes

Python 3.10 or later is enough for the repository checks:

```sh
python3 scripts/validate.py
python3 -m unittest discover -s tests
```

The validator checks required frontmatter fields, relative documentation links, portable paths, and accidental credential artifacts. It is a structural check, not a general YAML parser or a substitute for a behavioral review. CI also runs Gitleaks against commits. Its action is configured for this personal GitHub repository; transferring the repository to an organization may require a Gitleaks Action license or replacing that scan with the open-source CLI.

Before releasing a version, run these checks, scan the complete Git history for secrets, review realistic managed/manual/existing-app scenarios, and verify current vendor documentation. Never commit real credentials, local `.env` files, store-account exports, or screenshots containing private material as fixtures. Use synthetic temporary fixtures for tests.

## Contributing and sources

Keep the main skill focused on decisions and invariants. Put mode-specific detail in linked references, prefer current official documentation over historical wizard recordings, and describe the evidence for behavior changes in pull requests. Test without mutating real store accounts unless separately authorized.

Primary starting points: [Bifrost MCP](https://bifrost.nativephp.com/docs/mobile/teams/mcp), [managed credentials](https://bifrost.nativephp.com/docs/mobile/credentials/managed), [store keys](https://bifrost.nativephp.com/docs/mobile/credentials/store-keys), [Apple provisioning](https://developer.apple.com/help/account/provisioning-profiles/create-an-app-store-provisioning-profile), and [Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756).

License: [MIT](LICENSE). Prepared for an initial release; no version tag is implied by the documentation review date.
