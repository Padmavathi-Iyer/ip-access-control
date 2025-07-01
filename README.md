# An Integer Programming Framework for ReBAC Policy Mining and Optimized Conformance Testing

**Author:** Padmavathi Iyer, Drury University  
**Conference:** 22nd Annual International Conference on Privacy, Security, and Trust (PST2025)  

## Overview

This repository contains the code accompanying the paper "An Integer Programming Framework for ReBAC Policy Mining and Optimized Conformance Testing". The implementation provides a sample demonstration of how our integer programming model calculates an optimal set of low-level authorizations needed for the conformance testing of a ReBAC (Relationship-Based Access Control) policy, as discussed in Section IV of the paper.

## System Requirements

- **Python:** 3.13.0 or higher
- **Required Libraries:**
  - PuLP (v2.9.0)
  - Pandas

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Padmavathi-Iyer/ip-access-control.git
   cd ip-access-control
   ```

2. Install required dependencies:
   ```bash
   pip install pulp==2.9.0 pandas
   ```

## Repository Contents

```
├── system_graph.csv          # System graph input (Appendix-A example)
├── rebac_policy.txt          # ReBAC policy input for authorization simulation
├── eqOrOpt.py                # Main optimization algorithm implementation
├── mapper.py                 # Utility for metadata calculation
├── gen_low_level_auths.py    # Utility for generating complete authorization set
├── complete_low_level_auths.csv  # Complete set of possible access requests (A)
├── min_low_level_auths.csv   # Output: minimum authorization set (Amin)
└── README.md                 # This file
```

### File Descriptions

- **Input Files:**
  - `system_graph.csv`: System graph based on the hypothetical electronic medical records system example from Appendix-A
  - `rebac_policy.txt`: ReBAC policy used for simulating complete authorization generation

- **Core Implementation:**
  - `eqOrOpt.py`: Main file that calculates the optimal set of authorizations using integer programming
  - `mapper.py`: Utility for calculating complete low-level authorizations and other necessary metadata
  - `gen_low_level_auths.py`: Utility for generating the complete authorization set

- **Output Files:**
  - `complete_low_level_auths.csv`: Complete set of all possible access request authorizations (A)
  - `min_low_level_auths.csv`: Optimal minimum set of low-level authorizations (Amin)

## Usage

### Quick Start

To execute the optimization model:

```bash
python eqOrOpt.py
```

### Expected Output

The program will display:

1. **Model Statistics:**
   - Number of variables and constraints involved
   - HiGHS solver compute logs

2. **Optimization Results:**
   - Objective value of the optimal solution
   - Optimal solution comprising the selected permit and deny test cases

3. **File Output:**
   - The calculated minimum set of low-level authorizations saved to `min_low_level_auths.csv`

### Example Results

For the provided example (hypothetical electronic medical records system):
- **Optimal Solution:** 6 authorizations (4 permits + 2 denies)
- **Output File:** `min_low_level_auths.csv` contains the minimal test case set

## Algorithm Overview

Our integer programming framework:

1. **Input Processing:** Reads system graph and ReBAC policy
2. **Authorization Generation:** Creates complete set of possible access requests
3. **Optimization:** Uses integer programming to find minimum authorization set for testing
4. **Output:** Provides optimal conformance test cases

## Example Dataset

The included example demonstrates our approach using a **hypothetical electronic medical records system** with:
- System entities and relationships defined in `system_graph.csv`
- Access control policies specified in `rebac_policy.txt`
- Realistic healthcare access scenarios by doctors and nurses to patients’ medical records

## Citation

If you use this code in your research, please cite our paper:

```bibtex
@inproceedings{iyer2025integer,
  title={An Integer Programming Framework for ReBAC Policy Mining and Optimized Conformance Testing},
  author={Iyer, Padmavathi},
  booktitle={22nd Annual International Conference on Privacy, Security, and Trust (PST)},
  year={2025},
  organization={IEEE}
}
```

## Contact

**Author:** Padmavathi Iyer  
**Institution:** Drury University  

For questions about the implementation or paper, please contact the author.

## Acknowledgments

This work was presented at the 22nd Annual International Conference on Privacy, Security, and Trust (PST2025).

---

**Note:** This implementation is provided for research reproducibility and educational purposes. The example uses a hypothetical electronic medical records system as described in the paper's Appendix-A.
