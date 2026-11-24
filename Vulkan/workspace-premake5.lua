VULKAN_SDK = os.getenv("VULKAN_SDK")
if VULKAN_SDK == nil then
    VULKAN_SDK = "/usr/local";
end

-- Replace this as required
SDL_BIN_PATH = _MAIN_SCRIPT_DIR .. "/../SDL/build/"
GLFW_BIN_PATH = _MAIN_SCRIPT_DIR .. "/../glfw"

workspace "MyWorkspace"
    configurations { "Debug", "Release" }

    newoption {
        trigger = "x11",
        description = "Compile with xlib support"
    }
    newoption {
        trigger = "wayland",
        description = "Compile with wayland support"
    }
    newoption {
        trigger = "clang",
        description = "Utilise the clang compiler toolchain"
    }
    newoption {
        trigger = "dll",
        description = "Build as a dynamic library file (.dll on Windows, .so on Linux, .dylib on MacOS)"
    }

    filter "options:clang"
        toolset "clang"

    filter {"toolset:gcc"}
        buildoptions { "-Wno-comment", "-fPIC", "-Wno-multichar", "-Wno-deprecated-declarations", "-Werror=maybe-uninitialized", "-Werror=return-type" }

    filter {"toolset:clang"}
        buildoptions { "-march=native", "-Wno-nonportable-include-path", "-Wno-comment", "-Wno-nullability-completeness", "-Wno-void-pointer-to-int-cast", "-Wno-multichar", "-Werror=microsoft-extra-qualification", "-Werror=format-insufficient-args", "-Werror=duplicate-method-match", "-Werror=duplicate-method-arg", "-Werror=microsoft-cast", "-Wno-deprecated-declarations", "-Wno-implicit", "-Werror=sometimes-uninitialized", "-Werror=return-type", "-Werror=bool-conversion" }
        linkoptions { "-fuse-ld=lld" }

    -- force use of the correct llvm archiving program and .res file compiler on windows. Otherwise, it will
    -- attempt to use GCC's, then fail if it is not present.
    filter {"toolset:clang", "system:windows"}
        makesettings {"AR = llvm-ar", "RESCOMP = llvm-windres"}

    -- explicitly enable debug symbols for gcc and clang
    filter {"toolset:gcc or clang", "configurations:Debug"}
        buildoptions "-g"
        linkoptions "-g"
    
    -- enable PDB generation
    filter {"toolset:clang", "configurations:Debug", "system:windows"}
        buildoptions "-gcodeview"

    filter "system:linux"
        defines { "LINUX", "POSIX" }

    filter "options:x11"
        defines { "X11" }

    filter "options:wayland"
        defines { "WAYLAND" }

    filter "system:windows"
        defines { "WINDOWS" }
        architecture "x86_64"

    filter "configurations:Debug"
        defines { "DEBUG" }
        symbols "On"

    filter "configurations:Release"
        defines { "NDEBUG" }
        optimize "On"

    -- include("path-to-your-project")