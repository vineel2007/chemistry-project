import streamlit as st
import pandas as pd
from rdkit import Chem
from rdkit.Chem import FindMolChiralCenters
from rdkit.Chem import Draw

# Set up page configurations
st.set_page_config(page_title="Chiral Centers Analysis", page_icon="🔬", layout="wide")

st.title("🔬 Chiral Centers Analysis")
st.markdown("Enter a molecule's SMILES string to mathematically analyze its chiral centers and view its 2D visual structure.")

# Layout for the input settings
col1, col2 = st.columns(2)

with col1:
    molecule_name = st.text_input("Molecule Name", value="Fidaxomicin")
with col2:
    # Default SMILES string for convenience
    default_smiles = "ClC1=C(CC)C(C(O[C@H]2[C@H](O)[C@H](OC)[C@H](OC/C3=C\\C=C\\C[C@H](O)/C(C)=C/[C@H](CC)[C@@H](O[C@]4([H])OC(C)(C)[C@@H](OC(C(C)C)=O)[C@H](O)[C@@H]4O)/C(C)=C/C(C)=C/C[C@]([C@H](O)C)([H])OC3=O)O[C@@H]2C)=O)=C(O)C(Cl)=C1O"
    smiles_input = st.text_input("SMILES String", value=default_smiles)

if st.button("Analyze Chiral Centers", type="primary"):
    if not smiles_input:
        st.warning("Please enter a SMILES string to analyze.")
    else:
        # Load the molecule using RDKit
        mol = Chem.MolFromSmiles(smiles_input)
        
        if mol is None:
            st.error(f"Error: Could not parse SMILES string for {molecule_name}. Please check if the SMILES string is valid.")
        else:
            st.markdown("---")
            # Divide the screen into two columns for results
            res_col1, res_col2 = st.columns([1, 1.5])
            
            with res_col1:
                st.subheader(f"Structure: {molecule_name}")
                # RDKit drawing logic
                try:
                    # Provide highlights by identifying the chiral atoms
                    chiral_centers = FindMolChiralCenters(mol, includeUnassigned=True)
                    highlight_atoms = [idx for idx, _ in chiral_centers]
                    
                    # Generate an image with highlighted chiral centers
                    img = Draw.MolToImage(mol, size=(500, 500), highlightAtoms=highlight_atoms)
                    st.image(img, use_container_width=True, caption="Highlighted atoms are detected chiral centers.")
                except Exception as e:
                    st.error(f"Could not generate molecule image. Error: {e}")
                
            with res_col2:
                st.subheader("Results")
                
                if not chiral_centers:
                    st.info(f"No chiral carbon centers found in the provided SMILES for {molecule_name}.")
                else:
                    st.success(f"Successfully identified {len(chiral_centers)} chiral centers.")
                    
                    # Store data for display in a DataFrame
                    data_rows = []
                    for atom_idx, config in chiral_centers:
                        atom = mol.GetAtomWithIdx(atom_idx)
                        atom_symbol = atom.GetSymbol()
                        config_str = config if config != '?' else "Unknown (?)"
                        
                        data_rows.append({
                            "Atom Index": atom_idx,
                            "Element": atom_symbol,
                            "Configuration (R/S)": config_str
                        })
                    
                    df = pd.DataFrame(data_rows)
                    
                    # Display as a dataframe for neat layout
                    st.dataframe(df, use_container_width=True, hide_index=True)
