import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Define plotting functions
def create_examinees_purdueme_plot(semesters, examinees, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(semesters, examinees, marker='o', color='blue', linestyle='-', linewidth=1.5, markersize=8)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel("Semesters", fontsize=14)
    ax.set_ylabel("Number of Examinees (Purdue ME)", fontsize=14)
    ax.grid(visible=True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
    ax.set_ylim(0, 150)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    for i, score in enumerate(examinees):
        ax.plot([i, i], [score + 10, score], color='blue', linewidth=1.5)
        ax.text(
            i, score + 11, f"{score:}", ha='center', va='center', fontsize=10,
            color='black', fontweight='bold', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.3')
        )
    plt.tight_layout()
    return fig

def create_examinee_ABET_plot(semesters, examinees, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(semesters, examinees, marker='o', color='blue', linestyle='-', linewidth=1.5, markersize=8)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel("Semesters", fontsize=14)
    ax.set_ylabel("Total Number of ME Examinees (ABET)", fontsize=14)
    ax.grid(visible=True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
    ax.set_ylim(0, 5000)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    for i, score in enumerate(examinees):
        ax.plot([i, i], [score - 350, score], color='blue', linewidth=1.5)
        ax.text(
            i, score - 400, f"{score:}", ha='center', va='center', fontsize=10,
            color='black', fontweight='bold', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.3')
        )
    plt.tight_layout()
    return fig

def create_ratio_score_plot(semesters, scores, title):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(semesters, scores, marker='o', color='blue', linestyle='-', linewidth=1.5, markersize=8)
    max_score = scores.max()
    min_score = scores.min()
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel("Semesters", fontsize=14)
    ax.set_ylabel("Ratio Score", fontsize=14)
    ax.grid(visible=True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
    if min_score > 0:
        ax.set_ylim(1 - 0.1, max_score + 0.2)
    else:
        ax.set_ylim(min_score - 0.2, max_score + 0.2)
    ax.axhline(y=1, color='blue', linestyle='--', linewidth=1.5, label='Baseline (y=1)')
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    for i, score in enumerate(scores):
        ax.plot([i, i], [score - 0.02, score], color='blue', linewidth=1.5)
        ax.text(
            i, score - 0.025, f"{score:.2f}", ha='center', va='center', fontsize=10,
            color='black', fontweight='bold', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.3')
        )
    ax.legend(fontsize=12)
    plt.tight_layout()
    return fig

def create_scaled_score_plot_with_uncertainty_sticks(semesters, scores, uncertainties, title):
    upper_bound = scores + uncertainties
    lower_bound = scores - uncertainties
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(semesters, scores, marker='o', color='blue', linestyle='-', linewidth=1.5, markersize=8, label='Scaled Score')
    for i in range(len(semesters)):
        ax.plot([i, i], [lower_bound[i], upper_bound[i]], color='blue', linewidth=2, label='Uncertainty Range' if i == 0 else "")
        ax.plot([i - 0.1, i + 0.1], [upper_bound[i], upper_bound[i]], color='blue', linewidth=2)
        ax.plot([i - 0.1, i + 0.1], [lower_bound[i], lower_bound[i]], color='blue', linewidth=2)
    max_score = max(upper_bound)
    min_score = min(lower_bound)
    ax.set_title(title, fontsize=16, fontweight='bold')
    ax.set_xlabel("Semesters", fontsize=14)
    ax.set_ylabel("Scaled Score", fontsize=14)
    ax.grid(visible=True, which='major', linestyle='-', linewidth=0.5, alpha=0.7)
    ax.set_ylim(min_score - 0.2, max_score + 0.2)
    ax.tick_params(axis='x', rotation=45, labelsize=10)
    ax.tick_params(axis='y', labelsize=10)
    for i, score in enumerate(scores):
        ax.plot([i, i], [score - 0.08, score], color='blue', linewidth=1.5)
        ax.text(
            i, score - 0.055, f"{score:.2f}", ha='center', va='center', fontsize=10,
            color='black', fontweight='bold', bbox=dict(facecolor='white', edgecolor='blue', boxstyle='round,pad=0.3')
        )
    ax.legend(fontsize=12)
    plt.tight_layout()
    return fig

# Streamlit App
st.title("ABET Task Visualizer")
uploaded_file = st.file_uploader("Upload an Excel File", type=["xlsx"])

if uploaded_file is not None:
    # Read the uploaded Excel file
    df = pd.read_excel(uploaded_file)
    st.success("File uploaded successfully!")

    # User inputs title
    title = st.text_input("Enter a title for the charts")

    # Extract data
    if title:
        semesters = df['Semester']
        examinees_purdueme = df['Number of examinees taking the test']
        examinees = df['ABET Comparator (number of examinees taking)']
        ratio_score = df[' Ratio Score (*4)']
        scaled_score = df[' Scaled Score (*4)']
        uncertainties = df['Uncertainty Range for Scaled Score (*4)']

        # Generate plots
        f1 = create_examinees_purdueme_plot(semesters, examinees_purdueme, title)
        f2 = create_examinee_ABET_plot(semesters, examinees, title)
        f3 = create_ratio_score_plot(semesters, ratio_score, title)
        f4 = create_scaled_score_plot_with_uncertainty_sticks(semesters, scaled_score, uncertainties, title)

        # Display plots
        st.pyplot(f1)
        st.pyplot(f2)
        st.pyplot(f3)
        st.pyplot(f4)

        # Download plots
        plots = {"Examinees (Purdue ME)": f1, "Examinees (ABET)": f2, "Ratio Score": f3, "Scaled Score": f4}
        for name, fig in plots.items():
            buf = io.BytesIO()
            fig.savefig(buf, format="png")
            buf.seek(0)
            st.download_button(label=f"Download {name} Plot", data=buf, file_name=f"{name.replace(' ', '_').lower()}.png", mime="image/png")
            plt.close(fig)
