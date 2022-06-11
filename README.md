# recipe-app

Install Anaconda 64



## Creating standalone macOS application 

```bash
source activate recipe_app
rm -rf build dist
pyinstaller RecipeApp.py
```

For more info please vist: [Pyinstaller](https://www.pyinstaller.org/)

**Due to a non-trivial bug the above solution may not work on macOS Mojave.**

