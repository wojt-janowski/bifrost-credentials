# Optional build-configuration handoff

Use only when build configuration is requested. Consult the [current Bifrost configuration guide](https://bifrost.nativephp.com/docs/mobile/builds/configuration) and inspect the app's actual manifests, lockfiles, framework/runtime requirements, and build scripts.

Bifrost supplies app identity and version variables and runs its normal Composer, asset, and native build steps. Inspect the current injected-variable preview rather than duplicating or overriding those values. Shared variables apply to every Arc; use Arc overrides for intentional differences. Never embed store-upload credentials, backend secrets, or a shared device encryption key in the distributed app environment.

Choose runtime settings from the app's behavior. Local storage, SQLite, file sessions/cache, and synchronous queues may suit a standalone showcase, but are not universal defaults for connected apps. Verify how the installed NativePHP/SuperNative version supplies device keys, storage paths, and migrations. Do not run Artisan in an early pipeline stage where dependencies are not installed yet.

Inspect dependency accessibility before saving commands. A Composer path repository such as `../package` may exist on the developer's machine but not in a standalone cloud checkout. Resolve that for the app at hand, for example by fetching the explicitly intended package repository at the revision recorded in its lockfile, using a published package, or configuring the app's monorepo path. Do not clone another project's repository, introduce tokens into a URL, or switch to a moving branch merely because a previous app needed that workaround.

Validate commands in an isolated scratch directory when useful, preserving the user's checkout. A dry run checks only what it actually exercises; it is not a successful cloud build or native package. Reopen saved settings or inspect the blended environment to confirm persistence and precedence.

Report build-configuration readiness separately from credentials and first-build status. Starting a build consumes credits and requires the user's build request; configuring settings alone does not authorize builds, workflows, or distribution. If the same request already includes that further work, continue once prerequisites are ready, subject to host policy, without asking for redundant approval.
