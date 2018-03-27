# Boids!

Wherein [yours truly](https://github.com/alkc) tries his hand at a remake of an old [project.](https://github.com/alkc/flockingboids)

## Installation:

Wanna run this? Or help out? Good.

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