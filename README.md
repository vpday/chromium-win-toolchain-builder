# Chromium Windows Toolchain Builder

This project builds and packages the Windows Toolchain required for compiling Chromium.

Designed to run within GitHub Actions, it extracts headers and libraries from Visual Studio 2022 and the Windows SDK, packaging them into a format compatible with `depot_tools`. This enables Chromium cross-compilation on non-Windows platforms like Linux.

> [!DANGER]
> **WARNING: DO NOT RUN THIS SCRIPT LOCALLY**
>
> This script contains logic to **clean up MSVC versions**, which involves deleting older compiler files to minimize package size.
>
> **Running this on a personal workstation or a shared server will corrupt your Visual Studio installation.**
>
> This project is strictly intended for use within ephemeral GitHub Actions environments.

## Features

* **Version Locking**: Parses the `DEPS` file of the target Chromium version to ensure the correct `depot_tools` revision is used.
* **Environment Cleanup**: Scans for and removes redundant MSVC versions before packaging, keeping only the latest version to minimize artifact size.
* **Volume Splitting**: Packages the output into TAR archives and splits them into volumes (1GB/volume) to accommodate GitHub Release single-file size limits.

## Prerequisites

This project relies on the following GitHub Actions Runner environment:

* **OS**: `windows-2025`
* **Visual Studio**: Enterprise 2022
* **Windows SDK**: `10.0.26100.0`

> **Note**: Chromium builds strictly require SDK version `10.0.26100.0`. If the environment does not match, the build will fail.

## Usage

Trigger the build manually via `workflow_dispatch`.

1.  Navigate to the **Actions** tab of the GitHub repository.
2.  Select the **Package Windows Toolchain** workflow.
3.  Click **Run workflow**.
4.  Enter the version number in **Target Chromium Version** (e.g., `144.0.7559.96`).
5.  Click **Run workflow**.

Upon completion, the artifacts will be published to the **Releases** page. The tag name will match the Chromium version.

## Extracting the Artifacts

The artifact filenames follow this pattern: `win_toolchain_chromium-{ver}_vs-{ver}_sdk-{ver}.tar.001` (and subsequent volumes).

The package uses a two-stage compression method (ZIP wrapped in split TAR archives) and must be extracted before use.

### Extraction Steps (Linux)

1.  **Combine Volumes**:
    ```bash
    cat win_toolchain_*.tar.* > combined_toolchain.tar
    ```

2.  **Extract TAR**:
    ```bash
    tar -xvf combined_toolchain.tar
    ```
    *Extracting this will yield the original ZIP file.*

3.  **Unzip the Toolchain**:
    The resulting ZIP file is the Chromium Windows Toolchain package, ready to be configured in your build environment.

## References

* **Chromium Windows Cross-Compilation Guide**: [docs/win_cross.md](https://chromium.googlesource.com/chromium/src/+/lkgr/docs/win_cross.md#if-you_re-not-at-google)

    This document explains how to configure and use the Windows Toolchain in a Linux environment.