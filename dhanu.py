import rdkit
from rdkit import Chem
from rdkit.Chem import FindMolChiralCenters

def detect_chiral_centers(smiles, molecule_name):
    # Print a nice header
    header = f" Chiral Centers Analysis: {molecule_name} "
    border = "=" * len(header)
    print(f"\n{border}\n{header}\n{border}\n")

    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        print(f"[Error] Could not parse SMILES string for {molecule_name}\n")
        return

    # FindMolChiralCenters returns a list of tuples: (atom_index, 'R' or 'S')
    chiral_centers = FindMolChiralCenters(mol, includeUnassigned=True)
    
    if not chiral_centers:
        print("[Info] No chiral centers found.\n")
    else:
        print(f"[Success] Successfully identified {len(chiral_centers)} chiral centers:\n")
        
        # Table Header
        print("+" + "-"*14 + "+" + "-"*15 + "+" + "-"*19 + "+")
        print("| Atom Index   | Element       | Configuration     |")
        print("+" + "-"*14 + "+" + "-"*15 + "+" + "-"*19 + "+")
        
        for atom_idx, config in chiral_centers:
            atom = mol.GetAtomWithIdx(atom_idx)
            atom_symbol = atom.GetSymbol()
            
            # Ensure nice display for the configuration
            config_str = f"({config})" if config != '?' else "Unknown (?)"
            
            # Print the table row
            print(f"| {atom_idx:<12} | {atom_symbol:<13} | {config_str:<17} |")
            
        # Table Footer
        print("+" + "-"*14 + "+" + "-"*15 + "+" + "-"*19 + "+")
        print("\n" + border + "\n")

if __name__ == "__main__":
    # Isomeric SMILES for Fidaxomicin
    fidaxomicin_smiles = "CCC1=C(C=C(C(=C1Cl)O)C(=O)O[C@H]2[C@@H]([C@H]([C@@H]([C@H](O2)C)O/C=C/C=C/C[C@H](C(=C)[C@@H](CC)[C@H](C(=C/C=C/C(=C/[C@@H](Cc3c(c(cc(c3Cl)O)C(=O)O[C@H]4[C@@H]([C@H]([C@@H]([C@@H](O4)C)OC)O)OC)O)O)C)C)O[C@H]5[C@H]([C@@H]([C@@H]([C@H](O5)C)OC(=O)C(C)C)O)O)O)OC)O)O"
    # Using an explicitly retrieved Isomeric SMILES that contains the full structure:
    fidaxomicin_smiles = "ClC1=C(CC)C(C(O[C@H]2[C@H](O)[C@H](OC)[C@H](OC/C3=C\\C=C\\C[C@H](O)/C(C)=C/[C@H](CC)[C@@H](O[C@]4([H])OC(C)(C)[C@@H](OC(C(C)C)=O)[C@H](O)[C@@H]4O)/C(C)=C/C(C)=C/C[C@]([C@H](O)C)([H])OC3=O)O[C@@H]2C)=O)=C(O)C(Cl)=C1O"
    
    detect_chiral_centers(fidaxomicin_smiles, "Fidaxomicin")
