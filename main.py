import streamlit as st
from kripke_model import KripkeModel, evaluate_formula_in_all_worlds, parse_simple_formula
from typing import Dict, List, Tuple
import json
import pandas as pd
import os
import streamlit.components.v1 as components

def add_local_logo():
    try:
        # Path to your logo file (in same directory as script)
        logo_path = os.path.join(os.path.dirname(__file__), "Logo.png")
        
        # Display the logo at the top of sidebar with updated parameter
        st.sidebar.image(
            logo_path,
            width=150,  # Adjust width as needed
            use_container_width=False,  # Updated parameter
            output_format="auto"  # Optional: for better format handling
        )

    except Exception as e:
        # Elegant fallback with emoji logo
        st.sidebar.markdown("""
        <style>
            .fallback-logo {
                text-align: center;
                margin-bottom: 20px;
                font-size: 2.5em;
            }
            .fallback-text {
                text-align: center;
                color: #ffffff;
            }
        </style>
        <div class='fallback-logo'></div>
        <div class='fallback-text'>
            <h3>Modal Logic</h3>
        </div>
        """, unsafe_allow_html=True)


# Initialize session state
if 'kripke_model' not in st.session_state:
    st.session_state.kripke_model = KripkeModel()
if 'formulas' not in st.session_state:
    st.session_state.formulas = []

# Initialisation des états
if 'est_connecte' not in st.session_state:
    st.session_state.est_connecte = False
    st.session_state.nom_utilisateur = ""
if "formule" not in st.session_state:
    st.session_state.formule = ""

# Fonction pour ajouter un symbole à la formule
def ajouter_connecteur(symbole):
    st.session_state.formule += symbole
    st.rerun()

# -------- PAGE DE CONNEXION --------

import streamlit as st
def page_connexion():
    st.set_page_config(
        page_title="Logique Modale",
        page_icon=":brain:",
        layout="wide"
    )
    # Set the dark theme with custom background color
    st.markdown("""
    <style>
    .stApp {
        background-color: #1e1b2c;
        color: white;
    }
    .stTextInput > div > div > input {
        background-color: #2d2b40;
        color: white;
    }
    .stTextInput > label {
        color: white !important;
    }
    .stMarkdown {
        color: white;
    }
    h1, h2, h3, h4, h5, h6, p {
        color: white !important;
    }
    /* Improved logo positioning - moved to top left and up slightly */
    .logo-container {
        position: absolute;
        left: 15px;
        top: 10px;
        z-index: 1000;
    }
    /* Added padding to main content to accommodate logo */
    .main-content {
        padding-top: 40px;  /* Reduced to move title up */
    }
    /* Center login button */
    .login-button-container {
        display: flex;
        justify-content: center;
        margin-top: 20px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Display logo at top left with improved positioning
    st.markdown('<div class="logo-container">', unsafe_allow_html=True)
    st.image("Logo.png", width=120)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Main content with padding to avoid logo overlap
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Updated title styling to match Canva-style caption (3 lines, clear hierarchy)
    st.markdown("""
    <style>
    .title-container {
        text-align: center;
        margin-top: 0px;  /* Reduced to move title up */
        margin-bottom: 40px;
    }
    .main-title {
        font-size: 48px;
        font-weight: 300;
        font-family: "Segoe UI", sans-serif;
        color: white;
        line-height: 1.2;
        margin-bottom: 10px;
    }
    .highlight {
        font-weight: 600;
    }
    .subtitle {
        font-size: 20px;
        font-weight: 300;
        font-family: "Segoe UI", sans-serif;
        color: rgba(255, 255, 255, 0.85);
        line-height: 1.5;
    }
    </style>
    
    <div class="title-container">
        <div class="main-title">
            Master modal logic<br>
            with <span class="highlight">logicLens</span>
        </div>
        <div class="subtitle">
            simulate, prove, visualize in one click
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Login input with better spacing
    nom = st.text_input(label="", placeholder="Enter your Username")
    
    # Custom CSS for gradient button
    st.markdown("""
    <style>
    .stButton button {
        background: linear-gradient(90deg, #66C6C9) !important;
        color: white !important;
        font-weight: bold !important;
        border: none !important;
        padding: 8px 16px !important;
        border-radius: 4px !important;
    }
    .stButton button:hover {
        background: linear-gradient(90deg,  #66C6C9) !important;
        color: white !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="login-button-container">', unsafe_allow_html=True)
    col1, col2, col3,col4,col5 = st.columns([1, 1, 1,1,1])

# Affichage du bouton dans la colonne du milieu
    with col3:
        if st.button("log in"):
            if nom.strip() != "":
                st.session_state.est_connecte = True
                st.session_state.nom_utilisateur = nom
                st.rerun()
            else:
                st.error("Please enter a valide name")

    st.markdown('</div>', unsafe_allow_html=True)


def main():
    st.set_page_config(
        page_title="Logique Modale",
        page_icon=":brain:",
        layout="wide"
    )

    # Set the dark theme with custom background color
    st.markdown("""
    <style>
        .stApp {
            background-color: #1e1b2c;
            color: white;
        }
        .stTextInput > div > div > input {
            background-color: #2d2b40;
            color: white;
        }
        .stSelectbox > div > div > div {
            background-color: #2d2b40;
            color: white;
        }
        .stTextInput > label, .stSelectbox > label, .stCheckbox > label {
            color: white !important;
        }
        .stMarkdown {
            color: white;
        }
        div[data-testid="stSubheader"] {
            color: white;
        }
        div[data-testid="stHeader"] {
            color: white;
        }
        .stDataFrame {
            background-color: #2d2b40;
        }
        .stRadio > label {
            color: white !important;
        }
        .stRadio > div {
            color: white !important;
        }
        .stDataFrame [data-testid="stTable"] {
            color: white;
        }
        div.stButton > button {
            background: linear-gradient(90deg,  #7357ff, #fcacff);
            color: white;
            font-weight: bold;
            border: none;
        }
        div.stButton > button:hover {
            background: linear-gradient(90deg,  #7357ff, #fcacff);
        }
        
        h1, h2, h3, h4, h5, h6, p {
            color: white !important;
        }
        .st-emotion-cache-183lzff {
            color: white;
        }
        .stSidebar {
            background-color: #2d2b40;
        }
        [data-testid="stSidebar"] {
            background-color: #2d2b40;
        }
    </style>
    """, unsafe_allow_html=True)

    st.markdown(f"<h2 style='text-align: center; color: white;'>Bienvenue {st.session_state.nom_utilisateur} </h2>", unsafe_allow_html=True)

    # Add custom CSS for styling with the gradient buttons
    st.markdown("""
    <style>
        .stButton button {
            width: 100%;
            background: linear-gradient(90deg,  #7357ff, #fcacff) !important;
            color: white !important;
            font-weight: bold !important;
            border: none !important;
        }
        .stButton button:hover {
            background: linear-gradient(90deg,  #7357ff, #fcacff) !important;
        }
        
        .stTextInput input {
            width: 100%;
            background-color: #2d2b40;
            color: white;
        }
        .stSelectbox select {
            width: 100%;
            background-color: #2d2b40;
            color: white;
        }
        .formula-display {
            font-family: monospace;
            font-size: 1.2em;
            padding: 10px;
            background-color: #2d2b40;
            border-radius: 5px;
            margin: 5px 0;
            color: white;
        }
    </style>
    """, unsafe_allow_html=True)

    # Sidebar with model management
    with st.sidebar:
        add_local_logo()
        st.header("Model Management")
        
        model_action = st.radio("Choose action:", 
                            ["Create New Model", "Load Model", "Save Model"])
        
        if model_action == "Create New Model":
            if st.button("Initialize New Model"):
                st.session_state.kripke_model = KripkeModel()
                st.session_state.formulas = []
                st.success("New model created!")
        
        elif model_action == "Load Model":
            uploaded_file = st.file_uploader("Upload JSON model", type="json")
            if uploaded_file is not None:
                try:
                    data = json.load(uploaded_file)
                    st.session_state.kripke_model = KripkeModel.from_dict(data)
                    st.success("Model loaded successfully!")
                except Exception as e:
                    st.error(f"Error loading model: {e}")
        
        elif model_action == "Save Model":
            if st.button("Download Current Model"):
                model_json = json.dumps(st.session_state.kripke_model.to_dict(), indent=2)
                st.download_button(
                    label="Download Model as JSON",
                    data=model_json,
                    file_name="kripke_model.json",
                    mime="application/json"
                )

    # Main content area
    
    
    st.header("Build Your Kripke Model")
            
    # World management
    st.subheader("Worlds")
    col1, col2 = st.columns(2)
    with col1:
        new_world = st.text_input("Add new world:")
        if st.button("Add World") and new_world:
            try:
                st.session_state.kripke_model.add_world(new_world)
                st.success(f"World '{new_world}' added!")
            except Exception as e:
                st.error(str(e))
            
    with col2:
        if st.session_state.kripke_model.W:
            world_to_remove = st.selectbox("Remove world:", sorted(st.session_state.kripke_model.W))
            if st.button("Remove World"):
                try:
                    st.session_state.kripke_model.remove_world(world_to_remove)
                    st.success(f"World '{world_to_remove}' removed!")
                except Exception as e:
                    st.error(str(e))
            
    # Relation management
    st.subheader("Accessibility Relations")
    if len(st.session_state.kripke_model.W) >= 2:
        col1, col2 = st.columns(2)
        with col1:
            source_world = st.selectbox("From world:", sorted(st.session_state.kripke_model.W))
        with col2:
            target_world = st.selectbox("To world:", sorted(st.session_state.kripke_model.W))
            
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Add Relation"):
                try:
                    st.session_state.kripke_model.add_relation(source_world, target_world)
                    st.success(f"Relation {source_world}→{target_world} added!")
                except Exception as e:
                    st.error(str(e))
        with col2:
            if st.button("Remove Relation"):
                try:
                    st.session_state.kripke_model.remove_relation(source_world, target_world)
                    st.success(f"Relation {source_world}→{target_world} removed!")
                except Exception as e:
                    st.error(str(e))
            
        # Relation properties
        st.subheader("Relation Properties")
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Make Reflexive"):
                st.session_state.kripke_model.make_relation_reflexive()
                st.success("All worlds now access themselves")
        with col2:
            if st.button("Make Symmetric"):
                st.session_state.kripke_model.make_relation_symmetric()
                st.success("All relations now bidirectional")
        with col3:
            if st.button("Make Transitive"):
                st.session_state.kripke_model.make_relation_transitive()
                st.success("Relations now transitive")
            
    # Valuation management
    st.subheader("Valuations")
    if st.session_state.kripke_model.W:
        selected_world = st.selectbox("Select world for valuation:", sorted(st.session_state.kripke_model.W))
        prop_name = st.text_input("Proposition name (e.g., 'p', 'q'):")
        prop_value = st.checkbox("Truth value", value=True)
            
        if st.button("Set Valuation"):
            try:
                st.session_state.kripke_model.set_valuation(selected_world, prop_name, prop_value)
                st.success(f"Set {prop_name}={prop_value} in {selected_world}")
            except Exception as e:
                st.error(str(e))
                
            # Show current valuations
            st.markdown("**Current Valuations:**")
            valuations = []
            for world in sorted(st.session_state.kripke_model.W):
                for prop, value in st.session_state.kripke_model.V.get(world, {}).items():
                    valuations.append({
                        "World": world,
                        "Proposition": prop,
                        "Value": "True" if value else "False"
                    })
            if valuations:
                st.dataframe(pd.DataFrame(valuations))
            else:
                st.info("No valuations set yet")

    # Evaluation section
    st.subheader("Evaluate Modal Formulas")
        
    # Initialize formula_input in session state if it doesn't exist
    if 'formula_input' not in st.session_state:
        st.session_state.formula_input = ""

# Create buttons for logical connectors
    st.markdown("**Insert connectors:**")
    cols = st.columns(7)
    with cols[0]:
            not_btn = st.button("¬ (NOT)")
    with cols[1]:
        and_btn = st.button("∧ (AND)")
    with cols[2]:
        or_btn = st.button("∨ (OR)")
    with cols[3]:
        implies_btn = st.button("→ (IMPLIES)")
    with cols[4]:
        box_btn = st.button("□ (BOX)")
    with cols[5]:
        diamond_btn = st.button("◇ (DIAMOND)")
    with cols[6]:
        parens_btn = st.button("( )")

    st.markdown("**Insert propositions:**")
    prop_cols = st.columns(2)
    with prop_cols[0]:
        p_btn = st.button("p")
    with prop_cols[1]:
        q_btn = st.button("q")

# Handle button presses
    if not_btn:
        st.session_state.formula_input += "¬"
    if and_btn:
        st.session_state.formula_input += " ∧ "
    if or_btn:
        st.session_state.formula_input += " ∨ "
    if implies_btn:
        st.session_state.formula_input += " → "
    if box_btn:
        st.session_state.formula_input += "□"
    if diamond_btn:
        st.session_state.formula_input += "◇"
    if parens_btn:
        st.session_state.formula_input += "()"
    if p_btn:
        st.session_state.formula_input += "p"
    if q_btn:
        st.session_state.formula_input += "q"

# Formula input that syncs with both keyboard and button inputs
    formula_input = st.text_input(
        "Enter a modal logic formula:",
        value=st.session_state.formula_input,
        help="Use p, q for propositions; ¬ for NOT; ∧ for AND; ∨ for OR; → for IMPLIES; □ for BOX; ◇ for DIAMOND",
        key="formula_input_field",
        on_change=lambda: setattr(st.session_state, 'formula_input', st.session_state.formula_input_field)
)

# This ensures the session state stays in sync when typing
    if formula_input != st.session_state.formula_input:
        st.session_state.formula_input = formula_input
        
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Evaluate Formula"):
            if formula_input:
                try:
                    formula = parse_simple_formula(formula_input)
                    results = evaluate_formula_in_all_worlds(st.session_state.kripke_model, formula)
                    
                    # Display results
                    st.markdown("**Evaluation Results:**")
                    result_data = []
                    for world, value in results.items():
                        result_data.append({
                            "World": world,
                            "Result": "True" if value else "False"
                        })
                    st.dataframe(pd.DataFrame(result_data))
                    
                    # Add to saved formulas
                    if formula_input not in [f[1] for f in st.session_state.formulas]:
                        st.session_state.formulas.append((formula, formula_input))
                except Exception as e:
                    st.error(f"Error evaluating formula: {e}")
            else:
                st.warning("Please enter a formula first")
            

    # Model visualization
    st.subheader("Model Visualization")
            
    if not st.session_state.kripke_model.W:
        st.info("Model has no worlds yet. Add some in the Model Builder tab.")
    else:
        # Display model structure
        st.subheader("Current Model Structure")
        st.code(str(st.session_state.kripke_model))
            
        # Graph visualization (using graphviz)
        try:
            from graphviz import Digraph
            
            dot = Digraph()
            dot.attr(rankdir='LR', bgcolor='#1e1b2c')
            
            # Add nodes (worlds)
            for world in sorted(st.session_state.kripke_model.W):
                # Get valuations for this world
                valuations = st.session_state.kripke_model.V.get(world, {})
                val_str = "\n".join([f"{p}:{'T' if v else 'F'}" for p, v in valuations.items()])
                
                dot.node(world, 
                        label=f"{world}\n{val_str}" if val_str else world,
                        shape='circle',
                        style='filled',
                        fillcolor='#7357ff',
                        fontcolor='white')
            
            # Add edges (relations)
            for source, target in st.session_state.kripke_model.R:
                dot.edge(source, target, color='white')
            
            st.graphviz_chart(dot)
            
        except ImportError:
            st.warning("For graph visualization, please install graphviz: pip install graphviz")
            st.write("Here's a text representation of the relations:")
            relations = sorted(st.session_state.kripke_model.R)
            st.write(" → ".join([f"{source}→{target}" for source, target in relations]) or "No relations")

    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col3:
        if st.button("Disconnect"):
            st.session_state.est_connecte = False
            st.session_state.nom_utilisateur = ""
            st.session_state.formule = ""
            st.rerun()
            

if __name__ == "__main__":
    if not st.session_state.est_connecte:
        page_connexion()
    else:
        main()
