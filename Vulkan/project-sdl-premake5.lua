--project file to be include()'d by the workspace file.

project "ProjectName"
    kind "ConsoleApp"
    language "C++"
    cppdialect "C++17"
    rtti "Off"
    exceptionhandling "Off"
    staticruntime "Off"
    targetdir "bin/%{cfg.buildcfg}"
    includedirs {
        --other includes go here
    }
    files {
        "**.cpp",
        "**.c"
        --other compile file types go here
    }

    -- filter {"system:windows", "options:not no-debug-tools"}
    --     links "dbghelp"

    filter "options:sdl-static"
        links { SDL_BIN_PATH .. "SDL3-static"}

    filter {"options:not sdl-static", "system:windows"}
        links { SDL_BIN_PATH .. "SDL3"}
        postbuildcommands { "{COPYFILEIFNEWER} \"" .. SDL_BIN_PATH .. "SDL3.dll\" \"bin/%{cfg.buildcfg}/SDL3.dll\" " }
    
    filter {"options:not sdl-static", "system:macosx"}
        links { SDL_BIN_PATH .. "libSDL3"}
        postbuildcommands { "{COPYFILEIFNEWER} \"" .. SDL_BIN_PATH .. "libSDL3.dylib\" \"bin/%{cfg.buildcfg}/libSDL3.dylib\" " }
    
    filter {"options:not sdl-static", "system:linux"}
        links { SDL_BIN_PATH .. "libSDL3"}
        postbuildcommands { "{COPYFILEIFNEWER} \"" .. SDL_BIN_PATH .. "libSDL3.so\" \"bin/%{cfg.buildcfg}/libSDL3.so\" " }
    


    filter "system:windows"
        links {
            "gdi32",
            "user32",
            "shell32",
            "comdlg32",
            "ws2_32",
            "Advapi32",
            "Mfplat",
            "Ole32",
            "Imm32",
            "OleAut32",
            "Version",
            "winmm"
        }
        files {'Icon.ico', 'resources.rc'}
    filter "system:linux"
        links {
            "asound"
        }
    filter "system:macosx"
        runpathdirs "/Runtime/"
        links {
            "Cocoa.framework",
            "IOKit.framework",
            "CoreFoundation.framework",
            "QuartzCore.framework",
            "CoreAudio.framework",
            "AudioToolbox.framework"
        }