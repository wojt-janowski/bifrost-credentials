# iOS signing

Current sources: [iOS credentials](https://bifrost.nativephp.com/docs/mobile/credentials/ios), [managed signing](https://bifrost.nativephp.com/docs/mobile/credentials/managed), [team store keys](https://bifrost.nativephp.com/docs/mobile/credentials/store-keys), and [Apple provisioning profiles](https://developer.apple.com/help/account/provisioning-profiles/create-an-app-store-provisioning-profile).

## Identify and reuse

Confirm the Apple team, bundle ID, distribution channel, actual capabilities, and App Store Connect app record. App Store distribution also covers TestFlight. Other distribution channels have different certificate/profile/device requirements; inspect current support instead of relying on a fixed list of wizard labels.

Look for a suitable Bifrost team App Store Connect API key before asking for a `.p8` or creating another key. Managed provisioning requires a **Team** key with an appropriate role, not an individual key. Present the role choice before granting access; Bifrost currently documents App Manager or Admin for managed signing, with App Manager the narrower option.

A compatible Apple Distribution certificate can sign multiple apps on the same team. Each app still needs a provisioning profile matching its identifier, distribution type, capabilities, and certificate. An uploaded certificate does not automatically become Bifrost's managed team certificate.

## Managed path for a new app

Use a supported MCP managed-signing operation if available; otherwise open the project's Settings → Credentials → Add Bundle Identifier. Reuse the team API key, set the confirmed bundle ID and distribution type, and select managed signing. Enable only capabilities the app actually needs. Skip Firebase configuration unless in scope.

Bifrost can register a missing App ID and provision signing material. No CSR, local P12 password, or Artisan run is needed for this path. Device-based distribution can require registered devices before a usable profile exists. Check the saved record and profile readiness rather than assuming wizard completion means signing is ready.

## Certificate limit and existing certificates

If Apple refuses another distribution certificate, inventory the existing certificates and the machines, profiles, and CI configurations using them. Do not infer that the oldest certificate is disposable. Prefer a valid certificate whose private key is available, such as an existing password-protected P12, plus a new profile for this app.

Before reusing an exported certificate, inspect its team, expiry, serial or SHA-256 fingerprint. Before uploading the profile, decode its metadata locally and verify:

- The team and application identifier match the intended app.
- Its entitlements and distribution characteristics match the task.
- A certificate embedded in `DeveloperCertificates` matches the chosen distribution certificate's SHA-256 fingerprint.
- Both certificate and profile remain valid.

Do not choose a certificate only by its display name or newest expiry. Parse profile metadata without dumping the full profile, device list, or certificate/private-key contents into tool output. On macOS, `security cms -D -i` can decode a profile; capture and parse its output locally rather than printing it wholesale.

Revocation can break dependent signing systems and profiles. Migrating those dependents or revoking a certificate is separate work requiring authorization, not a prerequisite to adding this app when reuse is possible.

## Manual generation only when needed

If no suitable certificate/private key exists and a new certificate is authorized, inspect the installed CLI's help, then run `php artisan native:credentials` and select iOS (or use a supported platform argument). Drive non-secret prompts through a TTY if available. Hand the password prompt to the user.

The usual flow generates a private key and CSR in `credentials/`; upload the CSR in [Apple Certificates](https://developer.apple.com/account/resources/certificates/list), selecting the certificate type required by the distribution channel. Move the downloaded CER into `credentials/`, then resume the CLI to create the P12. Store its password securely and verify any `.env` variables written by this installed CLI without displaying them.

Register the explicit App ID only if missing. In [Apple Profiles](https://developer.apple.com/account/resources/profiles/list), create a profile for that app, distribution type, and exact certificate. Download it into `credentials/` and validate the match described above.

For uploaded signing, use the supported MCP upload schema after transport consent, or select **Upload my own** in the Bifrost wizard. Upload the P12, let the user enter its password, and upload the matching profile. Reuse the team API key rather than uploading it again.

## App Store Connect and API keys

If store upload is requested, reuse or create the matching [App Store Connect app record](https://appstoreconnect.apple.com/apps). Use the intended public name, platform, language, bundle ID, and a unique SKU. If the name is unavailable, obtain an alternative. Present Full versus Limited user access; do not silently grant Full Access. Complete any required legal/account handoffs before submission.

Only create a new [App Store Connect Team API key](https://appstoreconnect.apple.com/access/integrations/api) when an existing suitable key cannot be used. The user chooses its access role. Save the one-time `.p8` download securely, note its Key ID and Issuer ID, and add it to the intended Bifrost team or app using the authorized transport. Do not revoke a key merely because its local `.p8` is missing; it may already work in Bifrost or another CI system.

## Verify

Confirm the saved distribution type, certificate, profile, and API-key reference. Run store credential validation where supported and report the actual result. Recheck after asynchronous navigation; an earlier wizard error can remain visible while a later step succeeds. Do not regenerate valid files because of a stale page.

Report the bundle ID, profile name, team API-key name, expiry, signing mode, saved filenames, and any outstanding app-record or capability work. A build or TestFlight upload must be requested; that authorization can already be part of the same user request. Continue it when prerequisites are ready, subject to host policy, rather than requesting the same permission again.
