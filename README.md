<p float="left">
<img src="https://img.shields.io/github/languages/top/fredhappyface/Minecraft.ModdingTools.svg?style=flat-square" alt="Github top language">
<img src="https://img.shields.io/codacy/grade/f206761a466640f9b6191b1c708242cd.svg?style=flat-square" alt="Codacy grade">
<img src="https://img.shields.io/codacy/coverage/f206761a466640f9b6191b1c708242cd.svg?style=flat-square" alt="Codacy coverage">
<img src="https://img.shields.io/github/repo-size/fredhappyface/Minecraft.ModdingTools.svg?style=flat-square" alt="Repository size">
<img src="https://img.shields.io/github/issues/fredhappyface/Minecraft.ModdingTools.svg?style=flat-square" alt="Issues">
<img src="https://img.shields.io/github/license/fredhappyface/Minecraft.ModdingTools.svg?style=flat-square" alt="License">
<img src="https://img.shields.io/github/commit-activity/m/fredhappyface/Minecraft.ModdingTools.svg?style=flat-square" alt="Commit activity">
<img src="https://img.shields.io/github/last-commit/fredhappyface/Minecraft.ModdingTools.svg?style=flat-square" alt="Last commit">
</p>





# Minecraft.ModdingTools

Provides some tools to make mod development easier.

## Included

- Builder: Build a mod from a template (java files, optional. Crafting recipes and forge tags  )
- RecipeBuilder: Build crafting recipe .json files from a config.json file

## Download
### Clone
#### Using The Command Line 
1. Press the Clone or download button in the top right
2. Copy the URL (link)
3. Open the command line and change directory to where you wish to clone to
4. Type 'git clone' followed by URL in step 2
```bash
$ git clone https://github.com/[user-name]/[repository]
```

More information can be found at 
<https://help.github.com/en/articles/cloning-a-repository>

#### Using GitHub Desktop
1. Press the Clone or download button in the top right
2. Click open in desktop
3. Choose the path for where you want and click Clone

More information can be found at 
<https://help.github.com/en/desktop/contributing-to-projects/cloning-a-repository-from-github-to-github-desktop> 

### Download Zip File

1. Download this GitHub repository
2. Extract the zip archive
3. Copy/ move to the desired location

## Language information 
### Built for
This program has been written for Python 3 and has been tested with 
Python version 3.7.0 <https://www.python.org/downloads/release/python-370/>
on a Windows 10 PC. 
### Other versions
To install Python, go to <https://www.python.org/> and download the latest 
version. 
## How to run
1. Open the .py file in IDLE
2. Run by pressing F5 or by selecting Run> Run Module

## How to test 
```
py.test test\test_fileIO.py --cov=lib && py.test test\test_recipeBuilder-builder.py --cov=recipebuilder --cov-append && py.test test\test_builder-assemble.py --cov=builder --cov-append 
```

## Licence 
MIT License
Copyright (c) Kieran W
(See the [LICENSE](/LICENSE.md) for more information.)



## Screenshots 

### Desktop 
|Screenshots                                                                                  |
|:-:                                                                                          |
|<img src="readme-assets/screenshots/desktop/screenshot-1.png" alt="Screenshot 1" width="600">|
|<img src="readme-assets/screenshots/desktop/screenshot-2.png" alt="Screenshot 2" width="600">|
|<img src="readme-assets/screenshots/desktop/screenshot-3.png" alt="Screenshot 3" width="600">| 


## Limited Support
Expect this project to be supported for approximately 6 months (for bug-fixes 
only). Note that this is not guaranteed. Create an issue for bugs (as this 
project is carried out in spare time, you may have to wait for a few days)

<img src="readme-assets/support/partial.png" alt="Limited Support" width="600">


