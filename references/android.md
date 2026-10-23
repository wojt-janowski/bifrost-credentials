# Android signing and Play access

Current sources: [Bifrost Android credentials](https://bifrost.nativephp.com/docs/mobile/credentials/android), [managed keystores](https://bifrost.nativephp.com/docs/mobile/credentials/managed#android), [Play App Signing](https://support.google.com/googleplay/android-developer/answer/9842756), and [Play permissions](https://support.google.com/googleplay/android-developer/answer/9844686).

## Identify the app and keys

Confirm the application ID and intended Play developer account. If the app already exists or has shipped, inspect its registered upload-certificate fingerprint before changing signing. App creation and store upload are separate from generating a keystore; signing-only setup need not create a Play app.

With Play App Signing, Google holds the app-signing key used for delivery to users. Bifrost signs submitted bundles with a separate **upload key**. Reusing a service account across apps does not mean reusing another app's upload keystore.

## New app: managed upload key

Prefer Bifrost-managed credentials. Use MCP only if its schema exposes that operation; otherwise open Settings → Credentials → Add Application Identifier. Reuse the authorized team Play service account if available, enter the application ID, select the managed-keystore option, skip unused Firebase configuration, and finish the wizard. Step order can vary by existing team configuration.

Bifrost generates the keystore, alias, and passwords; do not invent passwords or require the user to enter one in this path. Verify that the saved credential has a keystore and required passwords set, without revealing their values.

Download the keystore and upload certificate from its credential page into ignored `credentials/` and arrange a secure backup. A keystore download alone is not a complete independent backup if its passwords are unavailable locally; report that Bifrost retains the managed passwords. Do not rotate them just to make a backup. Use the upload certificate when Play asks for upload-key registration; do not confuse it with supplying Google's app-signing private key.

## Existing app or manually generated key

Preserve the upload key Google already accepts. Reuse an already-correct Bifrost credential. If a local backup is missing, inspect that credential's download options before asking the user to locate a JKS or proposing any replacement. A recovered keystore still needs the correct alias and passwords; do not claim a complete independent backup without them.

When an upload is actually needed, choose **Upload an existing keystore** and provide its JKS, alias, keystore password, and key password using the authorized transport. The two passwords are separate inputs; they may be equal or different. Do not force different values or infer one from the other.

Only generate a new local keystore when needed and authorized. Inspect CLI help, then use `php artisan native:credentials` and select Android (or a supported platform argument). Hand password entry to the user; verify the resulting keystore and `.env` variable names without printing passwords.

For a published app moving to managed signing, prepare a replacement key only as part of an authorized upload-key reset. Keep builds on the existing key until Google confirms the reset, then switch deliberately. Do not replace, revoke, or delete the working key as an attempted repair.

## Reuse or create a Play service account

Check Bifrost team integrations and the intended [Google Cloud project](https://console.cloud.google.com/iam-admin/serviceaccounts) before creating a project, service account, or JSON key. A matching display name alone is insufficient; check the project, email, and intended purpose. If the key is already stored in Bifrost, do not demand a new local copy just to reuse it.

If new setup is required:

1. Reuse or create the intended Cloud project and enable the Google Play Android Developer API in that project.
2. Create the service account. Play publishing access comes from Play Console; do not add broad Cloud IAM roles for this purpose.
3. Create a JSON private key only when required and authorized, then move the one-time download into `credentials/`. Do not print its contents. An organization policy blocking key creation is not permission to bypass that policy.
4. In [Play Console](https://play.google.com/console), reuse the service account's existing user entry or invite it if absent. A service account does not need to accept an email invitation.

If a Play app record is missing and creating it is in scope, prepare the name, package ID, language, app category, and pricing choice for review. The user handles policy/export declarations and any legal acceptance. Do not silently claim policy compliance on their behalf.

## Choose store access before saving

Present the concrete recipient and scope:

- **Apps:** selected apps versus every app in the developer account. Prefer app scope when it meets the task. Account-wide team convenience is a separate, broader choice.
- **Testing:** view app information, release to testing tracks, and manage testing tracks/tester lists as needed.
- **Production:** separately disclose the permission to publish publicly, exclude devices, and use Play app signing.
- **Other permissions:** draft editing, store presence, financial access, or administration only when required by the intended operations and approved. Observe any Google-implied dependent permissions before saving.

Do not grant production access merely because the user wants an internal test build. A Bifrost team-key reference and Play permissions are independent: storing a key at team level does not grant access to every Play app. When reusing it, add only the approved apps and permissions, preserve existing access, and verify the saved scope.

Use a per-app service-account override in Bifrost when the team key has the wrong identity or access. If current Bifrost documentation recommends broader permissions than the task needs, explain the tradeoff rather than silently granting the broader set.

## Verify and first release

Confirm the stored application ID, signing mode, alias, keystore presence, and service-account email. Where available, run **Check credentials** against the Play API; report separately if this was not run. Check API enablement and Play permissions on a 403, allowing for permission propagation. Do not regenerate keys to address a missing-app or first-upload error.

For Google Play, build an AAB; APKs are for sideloading. The first bundle for a new app must be uploaded manually through Play Console before Bifrost can distribute later releases through the API. Do not start that build or release unless requested. Report any outstanding upload-key registration and first manual AAB upload.
