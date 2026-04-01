import streamlit as st
import pandas as pd
from rdkit import Chem
from rdkit.Chem import FindMolChiralCenters
from rdkit.Chem.Draw import rdMolDraw2D

# Set up page configurations
st.set_page_config(page_title="Chiral Centers Analysis", page_icon="🔬", layout="wide", initial_sidebar_state="collapsed")

# Inject premium CSS (Glassmorphism, Google Fonts, modern styling) to completely upgrade aesthetics and fix black UI issues
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;800&family=Outfit:wght@500;700&display=swap');

/* Main Background Gradient */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%);
    color: #e2e8f0;
    font-family: 'Inter', sans-serif;
}

/* Student Info Badge */
.student-info {
    position: absolute;
    top: 20px;
    right: 30px;
    background: rgba(255, 255, 255, 0.05);
    backdrop-filter: blur(8px);
    -webkit-backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.15);
    border-radius: 12px;
    padding: 12px 18px;
    font-size: 0.9rem;
    color: #f8fafc;
    text-align: right;
    box-shadow: 0 4px 25px rgba(0, 0, 0, 0.25);
    z-index: 1000;
    line-height: 1.5;
}
.student-info .highlight {
    color: #d946ef;
    font-weight: 700;
    margin-right: 5px;
}

/* Typography styles */
h1, h2, h3, h4 {
    font-family: 'Outfit', sans-serif;
    color: #f8fafc;
}
h1 {
    text-align: center;
    background: -webkit-linear-gradient(45deg, #a855f7, #ec4899);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
    font-size: 3.5rem !important;
}

/* Enhanced Inputs */
.stTextInput > div > div > input {
    background-color: rgba(255, 255, 255, 0.05);
    color: #fff;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 10px 15px;
    font-family: 'Inter', sans-serif;
}
.stTextInput > div > div > input:focus {
    border-color: #a855f7;
    box-shadow: 0 0 15px rgba(168, 85, 247, 0.3);
}

/* Stunning Gradient Button */
.stButton > button {
    background: linear-gradient(90deg, #8b5cf6 0%, #d946ef 100%);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px 28px;
    font-size: 1.1rem;
    font-weight: 600;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.stButton > button:hover {
    transform: translateY(-3px) scale(1.02);
    box-shadow: 0 10px 25px -5px rgba(217, 70, 239, 0.5);
    color: white;
}

/* Glassmorphism layout columns */
[data-testid="column"] {
    background: rgba(255, 255, 255, 0.03);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-radius: 20px;
    border: 1px solid rgba(255, 255, 255, 0.08);
    padding: 24px;
    margin-top: 15px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
    transition: transform 0.3s ease;
}
[data-testid="column"]:hover {
    border-color: rgba(255, 255, 255, 0.15);
}

/* Dataframe Styling overlay */
[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid rgba(255,255,255,0.1);
}

/* Fix the molecule image container background so black lines show on any theme */
.mol-container {
    background: radial-gradient(circle, rgba(255,255,255,1) 0%, rgba(248,250,252,1) 100%);
    padding: 20px;
    border-radius: 16px;
    box-shadow: inset 0 0 20px rgba(0,0,0,0.05), 0 10px 25px rgba(0,0,0,0.3);
    display: flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 15px;
}
</style>

<!-- Top Right Student Info Overlay -->
<div class="student-info">
    <div><span class="highlight">Name:</span>Vineel Kumar</div>
    <div><span class="highlight">Class:</span>AIML-A</div>
    <div><span class="highlight">Roll No:</span>RA2511026050057</div>
</div>
""", unsafe_allow_html=True)

st.title("Chiral Centers Analysis 🔬")
st.markdown("<p style='text-align: center; color: #cbd5e1; font-size: 1.1rem; margin-bottom: 25px;'>Analyze stereocenters mathematically and visualize the molecular construct instantly.</p>", unsafe_allow_html=True)

st.write("---")

col1, col2 = st.columns(2)

with col1:
    molecule_name = st.text_input("Molecule Name", value="Mefloquine")
with col2:
    default_smiles = "O[C@H]([C@@H]1NCCCC1)c1cc(C(F)(F)F)nc2c1cccc2C(F)(F)F"
    smiles_input = st.text_input("SMILES String", value=default_smiles)

st.write("")
col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
with col_btn2:
    analyze_button = st.button("✨ Analyze Molecular Structure", use_container_width=True)

if analyze_button:
    if not smiles_input:
        st.warning("Please enter a SMILES string to analyze.")
    else:
        mol = Chem.MolFromSmiles(smiles_input)
        
        if mol is None:
            st.error(f"Error: Could not parse SMILES string for '{molecule_name}'. Please check your input.")
        else:
            st.markdown("<br>", unsafe_allow_html=True)
            res_col1, res_col2 = st.columns([1, 1.3])
            
            with res_col1:
                st.markdown(f"<h3 style='text-align: center; margin-bottom: 20px;'>{molecule_name}</h3>", unsafe_allow_html=True)
                
                try:
                    chiral_centers = FindMolChiralCenters(mol, includeUnassigned=True)
                    highlight_atoms = [idx for idx, _ in chiral_centers]
                    
                    # Instead of an image, use SVG for crystal clear, high resolution vector rendering!
                    drawer = rdMolDraw2D.MolDraw2DSVG(500, 500)
                    opts = drawer.drawOptions()
                    opts.clearBackground = False  # Allows CSS background to shine through
                    opts.padding = 0.1
                    
                    drawer.DrawMolecule(mol, highlightAtoms=highlight_atoms)
                    drawer.FinishDrawing()
                    svg = drawer.GetDrawingText()
                    
                    # Wrap the SVG in a pure-white glass container so the black lines always contrast nicely
                    st.markdown(f'<div class="mol-container">{svg}</div>', unsafe_allow_html=True)
                    st.markdown("<p style='text-align: center; color: #a855f7; font-weight: 500; font-size: 0.95rem;'>❖ Highlighted nodes are chiral centers</p>", unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Could not generate molecule image. Error: {e}")
                
            with res_col2:
                st.markdown("<h3 style='text-align: center; margin-bottom: 20px;'>Analysis Data</h3>", unsafe_allow_html=True)
                
                if not chiral_centers:
                    st.info(f"No chiral carbon centers found in the provided SMILES for {molecule_name}.")
                else:
                    st.success(f"🎉 Successfully identified **{len(chiral_centers)}** chiral centers!")
                    
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
                    st.dataframe(df, use_container_width=True, hide_index=True)
