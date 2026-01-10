# Copyright 2026 Ernesto Rosati
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
run_discern.py
Simple command-line wrapper for the Tri-Axial Discernment Engine.

Usage:
    python run_discern.py "claim text here"

Optionally add metadata (context notes) by editing inside the script,
or extend later to accept args via sys.argv.
"""

import sys
from tri_axial_discernment import compute_discernment_from_criteria

def main():
    # TODO: replace sample values with user input or CLI after future versions
    F = [0.6, 0.4, 0.5, 0.3, 0.4]
    C = [0.7, 0.5, 0.8, 0.4, 0.6]
    P = [0.3, 0.5, 0.6, 0.9, 0.4]

    result = compute_discernment_from_criteria(F, C, P)

    print("\nTri-Axial Discernment")
    print("---------------------")
    print(f"F (Fundamento): {result.foundation:.2f}")
    print(f"C (Contexto)  : {result.context:.2f}")
    print(f"P (Principio) : {result.principle:.2f}")
    print(f"Score (D)     : {result.score:.2f}")
    print(f"Action        : {result.action}")

if __name__ == "__main__":
    main()
