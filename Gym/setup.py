from setuptools import setup, find_packages

setup(
    name="gym_game",  # ✅ This should match the module name (underscore)
    version="0.0.1",
    packages=find_packages(),  # ✅ Automatically finds `gym_game`
    install_requires=["gym==0.26.0", "pygame==2.1.0", "pandas"],
)
