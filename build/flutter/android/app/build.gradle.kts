import java.util.Properties

plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.android")
    // The Flutter Gradle Plugin must be applied after the Android and Kotlin Gradle plugins.
    id("dev.flutter.flutter-gradle-plugin")
}

val localProperties = Properties().apply {
    val localPropertiesFile = rootProject.file("local.properties")
    if (localPropertiesFile.exists()) {
        localPropertiesFile.inputStream().use { load(it) }
    }
}

val flutterVersionCode = localProperties.getProperty("flutter.versionCode")?.toIntOrNull() ?: 1
val flutterVersionName = localProperties.getProperty("flutter.versionName") ?: "1.0"

android {
    namespace = "com.fdsb.fdsb"
    compileSdk = flutter.compileSdkVersion
    ndkVersion = flutter.ndkVersion

    packaging {
        jniLibs {
            useLegacyPackaging = true
            keepDebugSymbols += listOf(
                "*/arm64-v8a/libpython*.so",
                "*/armeabi-v7a/libpython*.so",
                "*/x86/libpython*.so",
                "*/x86_64/libpython*.so",
            )
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = JavaVersion.VERSION_17.toString()
    }

    sourceSets["main"].java.srcDir("src/main/kotlin")

    
    

    defaultConfig {
        applicationId = "com.fdsb.fdsb"
        val resolvedMinSdk = flutter.minSdkVersion
        minSdk = resolvedMinSdk
        val resolvedTargetSdk = flutter.targetSdkVersion
        targetSdk = resolvedTargetSdk
        versionCode = flutterVersionCode
        versionName = flutterVersionName

        println("Gradle build config:")
        println("  minSdkVersion: $resolvedMinSdk")
        println("  targetSdkVersion: $resolvedTargetSdk")
        println("  versionCode: $flutterVersionCode")
        println("  versionName: $flutterVersionName")

// flet: split_per_abi 
    }

// flet: android_signing 

    buildTypes {
        release {
// flet: android_signing 
            signingConfig = signingConfigs.getByName("debug")
// flet: end of android_signing 
        }
    }
}

flutter {
    source = "../.."
}

dependencies {}
