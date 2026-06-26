# FDSB



## Template variables

* `fdsb` - project identifier (lowercase, no spaces, i.e. "snake_case") used for bundle IDs and package names.
* `` - project description.
* `FDSB` - executable or bundle name on disk.
* `FDSB` - display name shown in window titles and about app dialogs.
* `com.fdsb` - org name in reverse domain name notation, e.g. `com.mycompany.myproject`.
* `Your Company` - the name of the company.
* `Copyright (c) 2026 Your Company` - the copyright notice.

## Icons

* iOS - `assets/icon_ios.png` (or any supported image format). Recommended minimum image size is 1024 px. Image should not be transparent (have alpha channel). Defaults to `assets/icon.png` with alpha-channel automatically removed.
* Android - `assets/icon_android.png` (or any supported image format). Recommended minimum image size is 192 px. Defaults to `assets/icon.png`.
* Web - `assets/icon_web.png` (or any supported image format). Recommended minimum image size is 512 px. Defaults to `assets/icon.png`. If `assets/favicon.png` file is provided it will be used unmodified (copied to `web/favicon.png`).
* Windows - `assets/icon_windows.png` (or any supported image format). ICO will be produced of 256 px size. Defaults to `assets/icon.png`. If `assets/icon_windows.ico` file is provided it will be just copied to `windows/runner/resources/app_icon.ico` unmodified.
* macOS - `assets/icon_macos.png` (or any supported image format). Recommended minimum image size is 1024 px. Defaults to `assets/icon.png`.

## Splash screens

* iOS (light) - `assets/splash_ios.png` (or any supported image format). Defaults to `assets/splash.png` and then `assets/icon.png`.
* iOS (dark) - `assets/splash_dark_ios.png` (or any supported image format). Defaults to light iOS splash, then to `assets/splash_dark.png`, then to `assets/splash.png` and then `assets/icon.png`.
* Android (light) - `assets/splash_android.png` (or any supported image format). Defaults to `assets/splash.png` and then `assets/icon.png`.
* Android (dark) - `assets/splash_dark_android.png` (or any supported image format).  Defaults to light Android splash, then to `assets/splash_dark.png`, then to `assets/splash.png` and then `assets/icon.png`.
* Web (light) - `assets/splash_web.png` (or any supported image format). Defaults to `assets/splash.png` and then `assets/icon.png`.
* Web (dark) - `assets/splash_dark_web.png` (or any supported image format). Defaults to light web splash, then `assets/splash_dark.png`, then to `assets/splash.png` and then `assets/icon.png`.
