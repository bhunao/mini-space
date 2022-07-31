import cx_Freeze


executables = [cx_Freeze.Executable("main.py")]

cx_Freeze.setup(
    name="mini-space",
    options={"build_exe": {"packages": ["pygame"],
                           "include_files": [
                               "imgs",
                               "sounds",
                               "fonts",
                               "Ships",
                               "buttons.py",
                               "configs.py",
                               "effects.py",
                               "functions.py",
                               "game_objects.py",
                           ]}},
    executables=executables
)
