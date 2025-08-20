# Android Widget

A minimal Android app widget targeting API 34.

The repository excludes the binary `gradle-wrapper.jar`. Generate it with `gradle wrapper` before building.

## Building

### With Android Studio
1. Install [Android Studio](https://developer.android.com/studio) with the Android 14 (API 34) SDK.
2. Open this project (`android-widget`) in Android Studio.
3. Use **Build > Build Bundle(s) / APK(s) > Build APK(s)**.
4. The generated APK will appear under `app/build/outputs/apk/debug/app-debug.apk`.

### From the command line
1. Install JDK 17, Gradle 8+, and the Android command-line tools with API 34.
2. Generate the wrapper jar:
   gradle wrapper
3. Build the debug APK:
   ./gradlew assembleDebug
4. The APK will be located at `app/build/outputs/apk/debug/app-debug.apk`.

Install the APK on your device using `adb install app/build/outputs/apk/debug/app-debug.apk`.
