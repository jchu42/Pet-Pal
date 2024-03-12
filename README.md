[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-24ddc0f5d75046c5622901739e7c5dd533143b0c8e959d652212380cedb1ea36.svg)](https://classroom.github.com/a/545oUMxH)

## 1. Project Title and Description
    - Title: Pet Pal
    - Description: Take care of a pet! Make sure the room doesn't get too filled with poop. Click poop to make it disappear. 
## 2. Installation
    - Dependencies: 
        - python 3.11
        - pygame
        - psycopg2
    - Installation Instructions: 
        1. download and extract zip, or clone the git repository
        2. "cd" to the folder with MainGame.py, or open the project folder in the terminal
        3. "pip i pygame"
        4. "pip i psycopg2"
        5. "python MainGame.py" to run the game!
## 3. Usage
    - Examples: 
        run "python MainGame.py" to run the game
        run "python gamedatabase.py" to reset the database if needed
        run "python config.py" to reset the configuration file if needed
    - Configuration: In "config.ini",
        [Screen] [fps]: How fast the game should run
        [Screen] [scale]: How large the screen should be (scale == pixel width and height)
        [Screen] [filter]: 0-3, different filter options. Some may look better at different scales.
        [Poop] [interval]: The interval in seconds between poops. 
        [Poop] [max]: The maximum number of poops the pet can make before it dies. 
        [Debug] [text]: Set to True to debug keyboard-related errors
        [Debug] [images]: Set to True to debug image not found errors
## 4. Features
    - List of Features: 
        Click 'New' to create a new account, select a pet and room, and start playing. 
        Click on poop to make it disappear. 
        Game runs even when it's off, so don't leave your pet for too long!
## 5. Contributing
    - Guidelines: To contribute information, bug reports, feature requests, or code, visit https://github.com/BTP405/project-1-group-7-nbb
    - Code Style: This code follows guidelines stated in the numpy docstrings convention. See https://numpydoc.readthedocs.io/en/latest/format.html
## 6. Credits
    - Authors: Joseph Chu, Becca Tran, and Lea Barnachea
    - Acknowledgments:
        Baby's room by Justin Liew https://openverse.org/image/26ec49b0-b14c-43ce-a576-2eabcdc25895?q=room
            CC BY-NC-SA 2.0
            https://creativecommons.org/licenses/by-nc-sa/2.0/
        TL - Cabin4 Kitchen by vastateparksstaff https://openverse.org/image/aa5e1438-076b-48d5-8585-f40845376704?q=kitchen
            CC BY 2.0
            https://creativecommons.org/licenses/by/2.0/
        Living Room (Angle 2) by smoMashup1 https://openverse.org/image/1bdd859b-81a3-4b4d-baa8-efd817ae86f4?q=room
            CC BY 2.0
            https://creativecommons.org/licenses/by/2.0/
        Red Panda Sprites! by Elthen https://www.patreon.com/posts/red-panda-98152976
            CC BY-NC 4.0
            https://creativecommons.org/licenses/by-nc/4.0/
        Cat Sprites! be Elthen https://www.patreon.com/posts/cat-sprites-40356299
            CC BY-NC 4.0
            https://creativecommons.org/licenses/by-nc/4.0/
        Pig Sprites! by Elthen https://www.patreon.com/posts/pig-sprites-30296626
            CC BY-NC 4.0
            https://creativecommons.org/licenses/by-nc/4.0/
        Borders and Panels Menu Part 3 by BDragon1727 https://bdragon1727.itch.io/border-and-panels-menu-part-3
        Song: Lucky Day by Sakura Girl https://soundcloud.com/sakuragirl_official
            Music promoted by https://www.chosic.com/free-music/all/
            Creative Commons CC BY 3.0
            https://creativecommons.org/licenses/by/3.0/
## 7. License
    - License Information:
        MIT License

        Copyright (c) 2024 Joseph Chu

        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:

        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.

        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE.
## 8. Additional Sections (Optional)
    - FAQ: 
        Q: "How do I increase the screen size?"
            A: Go to config.ini and set the [Screen][scale] value. Default is 5, but if it's too small, try 6 or 7. 
        Q: "How can I pause the game so my pet doesn't die overnight?"
            A: You can temporarily change the config.ini [Poop][interval] to 3600 for 1 hour a poop, and [Poop][max] to 10.
    - Troubleshooting: 
        Q: "I think I messed up when editing the config.ini file, the game crashes now"
            A: Run python config.py to reset the config.ini file to its default. 
        Q: "I'm getting some kind of file-related error, or a config key error"
            A: Make sure you're running the game from the correct folder. 
        Q: "I'm getting a "could not import Self from typing" error"
            A: Ensure your version of Python is at least 3.11
    - Roadmap: 
        - Food & Fullness
        - General graphics improvements
        - Happiness icons
        - More game sounds
        - Eating animation & general pet movement improvements
        - High score
        - Increasing poop interval over time
    - Changelog: 
        1.0
            First release!

## Markdown Formatting Tips
  - Use headings (#, ##, ###, etc.) to structure your document.
  - Utilize lists (- or 1.) for easy-to-read information.
  - Include links to relevant resources or documentation.
  - Add code blocks using triple backticks (```) for code snippets.
  - Use images or diagrams to enhance understanding where applicable.
