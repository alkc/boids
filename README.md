# Boids!

Wherein [yours truly](https://github.com/alkc) tries his hand at a remake of an old [project.](https://github.com/alkc/flockingboids)

The current end goal of this project is a better optimized simulation that matches the old simulation's features. I'm basically using this for learning how to write better python code.

Feel free to leaf through the [changelog](changelog.md) for list of changes between versions.

## Installation:

Want to install this? Follow the instructions below:

### Linux

Easiest way to get this to run, I think, is to use conda to create an environment fron the included 
`environment.yml` file, activate the env and then run `boids.py`:

```
git clone https://github.com/alkc/boids.git
cd boids
conda env create -f environment.yml
source activate boids
python3 boids.py
```