# 🔥 Sandpile Dynamics & Uniform Spanning Trees

This repository explores **Abelian Sandpile Models** on a disc-shaped grid, using both **NumPy-based arrays** and **NetworkX-based graph structures**. It includes tools for simulating sandpile dynamics, generating recurrent configurations with **Wilson’s algorithm**, visualising topplings, and testing conformal-like symmetries via **Möbius transformations**.

---

## 📦 Features

### 🧊 NumPy-Based Sandpile Class

- Cartesian ↔ Matrix coordinate conversions
- Grain addition/removal
- Toppling mechanism respecting disc boundaries
- Automatic stabilisation via repeated topplings
- Disregards points outside circular domain (set to `-1`)

### 🌐 NetworkX-Based Sandpile Class

- Graph Laplacian-based toppling
- Sink model for boundary dissipation
- Uniform spanning tree generation via:
  - **Loop-Erased Random Walks**
  - **Wilson’s Algorithm**
- Burning bijection to produce recurrent sandpile configurations
- Toppling count tracking for specific vertices

### 🎨 Visualisation

- Colour-coded grid plots with annotated grain counts
- UST visualisation with spring layouts
- Loop-erased random walk path plots

### 🔁 Symmetry Testing

- Apply Möbius transformations to coordinates
- Compare toppling behaviour under transformation
- Export data to CSV for further analysis

---

## 🛠 Requirements

Install the necessary packages:

```bash
pip install numpy networkx matplotlib
```

---

## 🚀 Usage

### Create and Stabilise a Sandpile

```python
sandpile = Sandpile(n=15)
sandpile.addAt((0, 0))
sandpile.stabilise()
print(sandpile.grid)
```

### Generate a Recurrent Configuration

```python
config = treeToSandpile(sandpile)
sandpile.set(config)
sandpile.plot()
```

### Symmetry Test via Möbius Transformation

```python
x = (4, 5)
y = (-3, 6)
transformation = (2, complex(0.5, 0.5))  # angle φ and complex shift b

results = countTopplings(x, y, transformation, trials=50)
```

### Export Results

```python
import numpy as np

data = np.column_stack((col1, col2))  # from countTopplings()
np.savetxt('data.csv', data, delimiter=',', fmt='%d')
```

---

## 📚 Theoretical Background

This project is based on:

- **Abelian Sandpile Models**
- **Graph Laplacians**
- **Uniform Spanning Trees (UST)**
- **Loop-Erased Random Walks (LERW)**
- **Burning Algorithms**
- **Möbius Transformations on the Complex Plane**

These models are significant in studying self-organised criticality, discrete potential theory, and algebraic combinatorics.

---

## 📈 Visual Output

Visualisations include:

- **Grain configuration plots**: Colour-coded by grain count
- **Loop-erased random walks**: Traced from origin to sink
- **UST growth visualisation**: With distance from sink labelled

---

## 📄 Licence

This project is licensed under the **MIT Licence**.

You are free to use, modify, and distribute the code under the conditions of the licence.

---

## 🧠 Further Exploration

You may explore:

- Different grid sizes (`n`)
- Alternative Möbius transformations
- Tracking symmetry invariants numerically
- Real-time dynamic plotting with `multiPlot()`
- Burning time visualisations from USTs

---

## 🙌 Acknowledgements

This project was inspired by mathematical models in self-organised criticality and related work in combinatorics and statistical physics, particularly:

- Deepak Dhar on Abelian sandpiles
- Lawler, Schramm & Werner on LERWs
- Wilson’s algorithm for uniform spanning trees

It is intended as a research tool and an educational resource for exploring discrete dynamical systems.
