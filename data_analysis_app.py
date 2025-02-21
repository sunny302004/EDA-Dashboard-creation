import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Set the default Seaborn theme
sns.set_theme(style="whitegrid")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Select Page:",
    ["Welcome", "Univariate Analysis", "Bivariate Analysis", "Multivariate Analysis"],
    key="navigation"
)

# Welcome Page
if page == "Welcome":
    st.title("Welcome to the Data Analysis Application")
    st.write(
        """
        This application is designed for dynamic data visualization and analysis using your uploaded dataset. It supports:

        - **Univariate Analysis:** Single-variable exploration.
        - **Bivariate Analysis:** Explore relationships between two variables.
        - **Multivariate Analysis:** Advanced insights involving multiple variables.

        ### Features include:
        - Interactive visualizations.
        - Seamless data upload and processing.
        - Advanced plots with custom options.

        Navigate through the sidebar options to begin your journey!
        """
    )

# Upload dataset for analysis
if page != "Welcome":
    st.sidebar.title("Upload Dataset")
    uploaded_file = st.sidebar.file_uploader("Upload your CSV file here", type=["csv"], key="uploader")

    if uploaded_file:
        try:
            data = pd.read_csv(uploaded_file)
            st.sidebar.success("Dataset Loaded Successfully!")
        except Exception as e:
            st.sidebar.error("Failed to load dataset. Please check the file format.")
            st.stop()
    else:
        st.sidebar.info("Please upload a dataset to proceed.")
        st.stop()

    # Define numeric and categorical columns
    numeric_columns = data.select_dtypes(include="number").columns.tolist()
    categorical_columns = data.select_dtypes(include="object").columns.tolist()

    # Helper function to display plots
    def display_plot(fig):
        if fig:
            st.pyplot(fig)
        else:
            st.error("No figure to display.")

# Univariate Analysis
if page == "Univariate Analysis":
    st.title("Univariate Analysis")
    st.header("Explore Single-Variable Trends")
    st.write("Explore univariate plots with dynamic column selection.")

    fig, axes = plt.subplots(2, 2, figsize=(22, 13))

    # Histogram
    if numeric_columns:
        hist_col = st.selectbox("Select column for Histogram:", numeric_columns, key="histogram", index=0)
        sns.histplot(data[hist_col], kde=True, ax=axes[0, 0])
        axes[0, 0].set_title(f"Histogram of {hist_col}", fontsize=30, color="red", weight="bold")
    else:
        st.error("No numeric columns available for Histogram.")

    # Countplot
    if categorical_columns:
        count_col = st.selectbox("Select column for Countplot (Categorical):", categorical_columns, key="countplot_univariate", index=0)
        sns.countplot(data=data, x=count_col, ax=axes[0, 1])
        axes[0, 1].set_title(f"Countplot of {count_col}", fontsize=30, color="red", weight="bold")
    else:
        st.error("No categorical columns available for Countplot.")

    # Pie Chart
    if categorical_columns:
        pie_col = st.selectbox("Select column for Pie Chart:", categorical_columns, key="pie_chart", index=0)
        top_categories = data[pie_col].value_counts().sort_values(ascending=False).head(5)
        top_categories.plot.pie(autopct='%1.1f%%', ax=axes[1, 0], textprops={'fontsize': 30})
        axes[1, 0].set_title(f"Pie Chart of Top 5 Categories in {pie_col}", fontsize=30, color="red", weight="bold")
    else:
        st.error("No categorical columns available for Pie Chart.")

    # Boxplot
    if numeric_columns:
        box_col = st.selectbox("Select column for Boxplot:", numeric_columns, key="boxplot", index=0)
        sns.boxplot(data=data, x=box_col, ax=axes[1, 1])
        axes[1, 1].set_title(f"Boxplot of {box_col}", fontsize=30, color="red", weight="bold")
    else:
        st.error("No numeric columns available for Boxplot.")
        
    plt.tight_layout()
    display_plot(fig)

# Bivariate Analysis
elif page == "Bivariate Analysis":
    st.title("Bivariate Analysis")
    st.header("Explore Relationships Between Two Variables")
    st.write("Explore bivariate relationships with dynamic column selection.")

    fig, axes = plt.subplots(2, 2, figsize=(22, 13))

    # Line Plot
    if numeric_columns:
        line_x = st.selectbox("X for Line Plot:", numeric_columns, key="line_x")
        line_y = st.selectbox("Y for Line Plot:", numeric_columns, key="line_y")
        sns.lineplot(data=data, x=line_x, y=line_y, ax=axes[0, 0])
        axes[0, 0].set_title(f"Line Plot of {line_x} vs {line_y}", fontsize=30, color="red", weight="bold")
    else:
        st.error("No numeric columns available for Line Plot.")

    plt.tight_layout()
    display_plot(fig)

# Multivariate Analysis
elif page == "Multivariate Analysis":
    st.title("Multivariate Analysis")
    st.header("Discover Patterns Across Multiple Variables")
    st.write("Generate Pairplot and Heatmap for multivariate analysis.")

    # Pairplot
    if numeric_columns:
        pairplot_cols = st.multiselect("Select columns for Pairplot:", numeric_columns)
        if pairplot_cols:
            pairplot_fig = sns.pairplot(data[pairplot_cols])
            st.pyplot(pairplot_fig)
        else:
            st.warning("Please select at least one column for the Pairplot.")
    else:
        st.error("No numeric columns available for Pairplot.")

    # Heatmap
    if numeric_columns:
        fig, ax = plt.subplots(figsize=(40, 30))
        sns.heatmap(data[numeric_columns].corr(), annot=True, cmap="coolwarm", ax=ax)
        ax.set_title("Correlation Heatmap", fontsize=30, color="red", weight="bold")
        display_plot(fig)
    else:
        st.error("No numeric columns available for Heatmap.")
