"""
Main Streamlit application for AI Pair Engineer.
"""

import streamlit as st
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Import local modules
from config.settings import Settings
from config.user_config import UserConfig
from context.analyzer import ContextAnalyzer
from context.parser import ProjectStructureParser
from models.llm_manager import LLMManager
from engines.completion_engine import CodeCompletionEngine
from engines.refactoring_engine import RefactoringEngine
from engines.bug_detection_engine import BugDetectionEngine
from utils.code_formatter import CodeFormatter
from utils.prompt_templates import PromptTemplates


def main():
    """Main application entry point."""
    
    # Set page config
    st.set_page_config(
        page_title="AI Pair Engineer",
        page_icon="🤖",
        layout="wide"
    )
    
    # Initialize components
    settings = Settings()
    user_config = UserConfig()
    context_analyzer = ContextAnalyzer()
    project_parser = ProjectStructureParser()
    code_formatter = CodeFormatter()
    prompt_templates = PromptTemplates()
    
    # Initialize LLM manager
    llm_manager = LLMManager(
        model_name=settings.MODEL_NAME,
        device=settings.DEVICE,
        quantization=settings.QUANTIZATION,
        max_context_length=settings.MAX_CONTEXT_LENGTH,
        max_new_tokens=settings.MAX_NEW_TOKENS,
        temperature=settings.TEMPERATURE,
        top_p=settings.TOP_P
    )
    
    # Initialize feature engines
    completion_engine = CodeCompletionEngine(
        llm_manager=llm_manager,
        context_analyzer=context_analyzer,
        code_formatter=code_formatter,
        prompt_templates=prompt_templates
    )
    
    refactoring_engine = RefactoringEngine(
        llm_manager=llm_manager,
        context_analyzer=context_analyzer,
        code_formatter=code_formatter,
        prompt_templates=prompt_templates
    )
    
    bug_detection_engine = BugDetectionEngine(
        llm_manager=llm_manager,
        context_analyzer=context_analyzer,
        code_formatter=code_formatter,
        prompt_templates=prompt_templates
    )
    
    # Sidebar for configuration
    with st.sidebar:
        st.title("⚙️ Configuration")
        
        # Model selection
        st.header("Model Settings")
        
        model_name = st.text_input(
            "Model Name",
            value=settings.MODEL_NAME,
            help="Name or path of the model to use"
        )
        
        device = st.selectbox(
            "Device",
            options=["auto", "cuda", "cpu"],
            index=0 if settings.DEVICE == "auto" else ["auto", "cuda", "cpu"].index(settings.DEVICE)
        )
        
        quantization = st.selectbox(
            "Quantization",
            options=["4bit", "8bit", "none"],
            index=0 if settings.QUANTIZATION == "4bit" else ["4bit", "8bit", "none"].index(settings.QUANTIZATION)
        )
        
        # Generation settings
        st.header("Generation Settings")
        
        max_tokens = st.slider(
            "Max Tokens",
            min_value=64,
            max_value=2048,
            value=settings.MAX_NEW_TOKENS
        )
        
        temperature = st.slider(
            "Temperature",
            min_value=0.0,
            max_value=2.0,
            value=settings.TEMPERATURE,
            step=0.1
        )
        
        top_p = st.slider(
            "Top P",
            min_value=0.1,
            max_value=1.0,
            value=settings.TOP_P,
            step=0.1
        )
        
        # Feature toggles
        st.header("Features")
        
        enable_completion = st.checkbox(
            "Code Completion",
            value=user_config.features_enabled.get("code_completion", True)
        )
        
        enable_refactoring = st.checkbox(
            "Refactoring Suggestions",
            value=user_config.features_enabled.get("refactoring", True)
        )
        
        enable_bug_detection = st.checkbox(
            "Bug Detection",
            value=user_config.features_enabled.get("bug_detection", True)
        )
        
        # Load model button
        if st.button("🔄 Load Model", use_container_width=True):
            try:
                llm_manager.load_model()
                st.success("Model loaded successfully!")
            except Exception as e:
                st.error(f"Error loading model: {e}")
        
        # Model info
        model_info = llm_manager.get_model_info()
        if model_info.get("loaded", False):
            st.info(f"Model: {model_info['model_name']}")
            st.info(f"Device: {model_info['device']}")
            st.info(f"Quantization: {model_info['quantization']}")
    
    # Main content area
    st.title("🤖 AI Pair Engineer")
    st.markdown("""
    **AI Pair Programming Assistant**
    
    This application provides intelligent code assistance powered by local LLMs.
    
    **Features:**
    - 📝 Code completion suggestions
    - 🔧 Refactoring suggestions
    - 🐛 Bug detection
    - 📖 Code explanation
    - 📝 Documentation generation
    """)
    
    # File browser
    st.header("📁 Project Files")
    
    # Get project path
    project_path = st.text_input(
        "Project Path",
        value=os.getcwd(),
        help="Path to your project root directory"
    )
    
    # Parse project structure
    if os.path.exists(project_path):
        try:
            project_info = project_parser.parse_project(project_path)
            
            # Display project info
            st.write(f"**Total files:** {project_info.get('total_files', 0)}")
            st.write(f"**Total size:** {project_info.get('total_size', 0) / 1024:.2f} KB")
            
            # File list
            if "files" in project_info:
                st.subheader("Files")
                for file_path, info in list(project_info["files"].items())[:20]:  # Limit to 20 files
                    with st.expander(file_path):
                        st.write(f"**Language:** {info['language']}")
                        st.write(f"**Size:** {info['size']} bytes")
        except Exception as e:
            st.error(f"Error parsing project: {e}")
    else:
        st.warning(f"Project path does not exist: {project_path}")
    
    # Code editor
    st.header("📝 Code Editor")
    
    # Initialize code editor
    if "code" not in st.session_state:
        st.session_state.code = ""
    if "cursor_pos" not in st.session_state:
        st.session_state.cursor_pos = {"line": 1, "col": 0}
    
    # Display code editor
    code = st.text_area(
        "Code",
        value=st.session_state.code,
        height=400,
        key="code_editor"
    )
    
    # Update cursor position (approximate)
    lines = code.split('\n')
    if lines:
        st.session_state.cursor_pos["line"] = len(lines)
        st.session_state.cursor_pos["col"] = len(lines[-1])
    
    # Feature buttons
    st.header("✨ AI Features")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💡 Complete Code", use_container_width=True):
            if enable_completion and code:
                try:
                    # Get cursor position
                    cursor_line = st.session_state.cursor_pos["line"]
                    cursor_col = st.session_state.cursor_pos["col"]
                    
                    # Get completions
                    completions = completion_engine.get_suggestions(
                        code,
                        cursor_line,
                        cursor_col,
                        max_suggestions=3
                    )
                    
                    # Display completions
                    for i, completion in enumerate(completions):
                        with st.expander(f"Suggestion {i+1}"):
                            st.code(completion, language="python")
                except Exception as e:
                    st.error(f"Error generating completions: {e}")
            else:
                st.warning("Enable code completion in settings")
    
    with col2:
        if st.button("🔧 Refactor", use_container_width=True):
            if enable_refactoring and code:
                try:
                    suggestions = refactoring_engine.suggest_refactorings(code)
                    
                    for suggestion in suggestions[:3]:
                        with st.expander("Refactoring Suggestion"):
                            st.write(suggestion)
                except Exception as e:
                    st.error(f"Error generating suggestions: {e}")
            else:
                st.warning("Enable refactoring in settings")
    
    with col3:
        if st.button("🐛 Detect Bugs", use_container_width=True):
            if enable_bug_detection and code:
                try:
                    bugs = bug_detection_engine.detect_bugs(code)
                    
                    if bugs:
                        for bug in bugs[:3]:
                            with st.expander("Bug Detected"):
                                st.write(f"**{bug['description']}**")
                                st.write(f"**Severity:** {bug['severity']}")
                                st.write(f"**Fix:** {bug['fix']}")
                    else:
                        st.success("No bugs detected!")
                except Exception as e:
                    st.error(f"Error detecting bugs: {e}")
            else:
                st.warning("Enable bug detection in settings")
    
    # Chat interface
    st.header("💬 Chat with Code")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    
    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask about your code..."):
        st.session_state.messages.append({
            "role": "user",
            "content": prompt
        })
        
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate response
        try:
            # Format prompt based on user input
            if "explain" in prompt.lower() or "what does" in prompt.lower():
                response = prompt_templates.format_explanation_prompt(code)
            elif "document" in prompt.lower() or "docstring" in prompt.lower():
                response = prompt_templates.format_documentation_prompt(code)
            else:
                response = f"""Analyze the following code:

{code}

{prompt}

Response:
"""
            
            # Generate response
            response_text = llm_manager.generate(response, max_tokens=max_tokens)
            
            # Add to chat
            st.session_state.messages.append({
                "role": "assistant",
                "content": response_text
            })
            
            with st.chat_message("assistant"):
                st.markdown(response_text)
                
        except Exception as e:
            st.error(f"Error generating response: {e}")


if __name__ == "__main__":
    main()
