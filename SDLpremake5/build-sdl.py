# builds the SDL file with the settings required to be used in Astral.Canvas.
# On windows, this will force-utilise clang and llvm-rc instead of MSVC.
# Also disables all the unnecessary functionality of the library.

import os
import subprocess
import argparse
import shutil

parser = argparse.ArgumentParser()
parser.add_argument('-p', '--path')
parser.add_argument('-c', '--clean', action='store_true')

args = parser.parse_args()

sdl_path = os.path.abspath(args.path)
if sdl_path is not None and os.path.isdir(sdl_path):
    if args.clean:
        print("Cleaning cmake build files")
        if os.path.isdir(os.path.join(sdl_path, "build")):
            shutil.rmtree(os.path.join(sdl_path, "build"))
        
        result = subprocess.run([
            "cmake",
            "-S", ".",
            "-B", "build",
            "-G", "Ninja",

            "-D", "CMAKE_C_COMPILER=clang",
            "-D", "CMAKE_CXX_COMPILER=clang++",
            "-D", "CMAKE_RC_COMPILER=llvm-rc",

            "-D", "SDL_STATIC=ON",
            "-D", "BUILD_SHARED_LIBS=ON",

            "-D", "SDL_OPENGL=OFF",
            "-D", "SDL_OPENGLES=OFF",
            "-D", "SDL_CAMERA=OFF",
            "-D", "SDL_AUDIO=OFF",
            "-D", "SDL_GPU=OFF",
            "-D", "SDL_RENDER=OFF",
            "-D", "SDL_CAMERA=OFF",
            "-D", "SDL_SENSOR=OFF",
            "-D", "SDL_TRAY=OFF",
            "-D", "SDL_NOTIFICATION=OFF",
            "-D", "SDL_DIALOG=OFF",
            "-D", "SDL_HIDAPI=OFF",
            "-D", "SDL_DUMMYVIDEO=OFF",
            "-D", "SDL_DUMMYAUDIO=OFF",
            "-D", "SDL_DISKAUDIO=OFF",

            "-D", "SDL_TEST_LIBRARY=OFF",
            "-D", "SDL_TESTS=OFF",
            "-D", "SDL_DISABLE_INSTALL_DOCS=ON",
            "-D", "SDL_INSTALL_TESTS=OFF"
        ], 
        shell=True, 
        check=True,
        cwd=sdl_path)

        if result.returncode != 0:
            print("Failed to generate compliant cmake files.\nEnsure that cmake and the ninja build tool are both installed.")
            exit(1)

    result = subprocess.run(
        ["cmake", "--build", "build", "--parallel"],
        shell=True,
        check=True,
        cwd=sdl_path
    )
    exit(result.returncode)

print("Path to SDL repository not specified. Use the --path argument to specify it.")
exit(1)