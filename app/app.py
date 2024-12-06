import seaborn as sns
from faicons import icon_svg

from shiny import reactive
from shiny.express import input, render, ui
import palmerpenguins 

# Loading the data into an initial Pandas DataFrame
df = palmerpenguins.load_penguins()

# Creating page title
ui.page_opts(title="Penguins dashboard", fillable=True)

# Sidebar for filter controls
with ui.sidebar(title="Filter controls"):
    ui.input_slider("mass", "Mass", 2000, 6000, 6000)
    ui.input_checkbox_group(
        "species",
        "Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )
    ui.hr()

# Links Section in Sidebar
    ui.h6("Links")
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Main content area (outputs)
with ui.layout_column_wrap(fill=False):
    
    #  Value box showing number of penguins in the filtered dataset
    with ui.value_box(showcase=icon_svg("earlybirds")):
        "No. of penguins"

         # Reactive function to return the count of penguins
        @render.text
        def count():
            return filtered_df().shape[0]

     # Value box showing average bill length of penguins in the filtered dataset
    with ui.value_box(showcase=icon_svg("ruler-horizontal")):
        "Avg. bill length"

        # Reactive function to return the average bill length
        @render.text
        def bill_length():
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

     # Value box showing average bill depth of penguins in the filtered dataset
    with ui.value_box(showcase=icon_svg("ruler-vertical")):
        "Avg. bill depth"

        # Reactive function to return the average bill length
        @render.text
        def bill_depth():
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"


with ui.layout_columns():
     # Card showing Seaborn scatterplot: Bill length vs. Bill depth
    with ui.card(full_screen=True):
        ui.card_header("Bill length & depth")

        @render.plot
        def length_depth():
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

     # Card showing summary statistics (Data Grid)
    with ui.card(full_screen=True):
        ui.card_header("Penguin Data")

        @render.data_frame
        def summary_statistics():
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")

# Reactive function to filter dataset based on user inputs
@reactive.calc
def filtered_df():
    # Filtering by selected species
    filt_df = df[df["species"].isin(input.species())]
    # Filtering by body mass (based on the slider value)
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
