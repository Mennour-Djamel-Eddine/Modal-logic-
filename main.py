import streamlit as st
from kripke_model import KripkeModel, evaluate_formula_in_all_worlds, parse_simple_formula
from typing import Dict, List, Tuple
import json
import pandas as pd
import os
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
                color: #2b5278;
            }
        </style>
        <div class='fallback-logo'>🧠</div>
        <div class='fallback-text'>
            <h3>Modal Logic</h3>
        </div>
        """, unsafe_allow_html=True)
# Initialize session state
if 'kripke_model' not in st.session_state:
    st.session_state.kripke_model = KripkeModel()
if 'formulas' not in st.session_state:
    st.session_state.formulas = []

def main():
    st.set_page_config(
        page_title="Logique Modale ",
        page_icon=":brain:"
    )

    

    # Main interface tabs
    
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

    
    st.header("Evaluate Modal Formulas")
    
    # Initialize formula_input in session state if it doesn't exist
    if 'formula_input' not in st.session_state:
         st.session_state.formula_input = ""
    
    # Formula input with buttons for connectors
    formula_input = st.text_input(
        "Enter a modal logic formula:",
        value=st.session_state.formula_input,
        help="Use p, q for propositions; ¬ for NOT; ∧ for AND; ∨ for OR; → for IMPLIES; □ for BOX; ◇ for DIAMOND",
        key="formula_input_field"
    )
    
    # Create buttons for logical connectors
    st.markdown("**Insert connectors:**")
    cols = st.columns(7)
    with cols[0]:
         if st.button("¬ (NOT)"):
            st.session_state.formula_input += "¬"
            st.rerun()
    with cols[1]:
         if st.button("∧ (AND)"):
            st.session_state.formula_input += " ∧ "
            st.rerun()
    with cols[2]:
         if st.button("∨ (OR)"):
            st.session_state.formula_input += " ∨ "
            st.rerun()
    with cols[3]:
         if st.button("→ (IMPLIES)"):
            st.session_state.formula_input += " → "
            st.rerun()
    with cols[4]:
         if st.button("□ (BOX)"):
            st.session_state.formula_input += "□"
            st.rerun()
    with cols[5]:
         if st.button("◇ (DIAMOND)"):
            st.session_state.formula_input += "◇"
            st.rerun()
    with cols[6]:
         if st.button("( )"):
            st.session_state.formula_input += "()"
            st.rerun()
    st.markdown("**Insert propositions:**")
    prop_cols = st.columns(2)
    with prop_cols[0]:
         if st.button("p"):
            st.session_state.formula_input += "p"
            st.rerun()
    with prop_cols[1]:
         if st.button("q"):
            st.session_state.formula_input += "q"
            st.rerun()
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
        
    with col2:
            if st.button("Add to Saved Formulas"):
                if formula_input:
                    try:
                        formula = parse_simple_formula(formula_input)
                        if formula_input not in [f[1] for f in st.session_state.formulas]:
                            st.session_state.formulas.append((formula, formula_input))
                            st.success("Formula added to saved formulas!")
                        else:
                            st.warning("Formula already in saved formulas")
                    except Exception as e:
                        st.error(f"Error parsing formula: {e}")
                else:
                    st.warning("Please enter a formula first")
        
        # Saved formulas
    st.subheader("Saved Formulas")
    if st.session_state.formulas:
            for i, (formula_obj, formula_str) in enumerate(st.session_state.formulas):
                col1, col2, col3 = st.columns([4,1,1])
                with col1:
                    st.code(formula_str)
                with col2:
                    if st.button(f"Evaluate #{i+1}"):
                        try:
                            results = evaluate_formula_in_all_worlds(st.session_state.kripke_model, formula_obj)
                            result_data = []
                            for world, value in results.items():
                                result_data.append({
                                    "World": world,
                                    "Result": "True" if value else "False"
                                })
                            st.dataframe(pd.DataFrame(result_data))
                        except Exception as e:
                            st.error(f"Error evaluating formula: {e}")
                with col3:
                    if st.button(f"Delete #{i+1}"):
                        del st.session_state.formulas[i]
                        st.rerun()
    else:
            st.info("No saved formulas yet")

    
    st.header("Model Visualization")
        
    if not st.session_state.kripke_model.W:
        st.info("Model has no worlds yet. Add some in the Model Builder tab.")
    else:
            # Display model structure
            st.subheader("Current Model Structure")
            st.text(str(st.session_state.kripke_model))
            
            # Graph visualization (using graphviz)
            try:
                from graphviz import Digraph
                
                dot = Digraph()
                dot.attr(rankdir='LR')
                
                # Add nodes (worlds)
                for world in sorted(st.session_state.kripke_model.W):
                    # Get valuations for this world
                    valuations = st.session_state.kripke_model.V.get(world, {})
                    val_str = "\n".join([f"{p}:{'T' if v else 'F'}" for p, v in valuations.items()])
                    
                    dot.node(world, 
                            label=f"{world}\n{val_str}" if val_str else world,
                            shape='circle',
                            style='filled',
                            fillcolor='lightblue')
                
                # Add edges (relations)
                for source, target in st.session_state.kripke_model.R:
                    dot.edge(source, target)
                
                st.graphviz_chart(dot)
                
            except ImportError:
                st.warning("For graph visualization, please install graphviz: pip install graphviz")
                st.write("Here's a text representation of the relations:")
                relations = sorted(st.session_state.kripke_model.R)
                st.write(" → ".join([f"{source}→{target}" for source, target in relations]) or "No relations")
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
if __name__ == "__main__":
    main()