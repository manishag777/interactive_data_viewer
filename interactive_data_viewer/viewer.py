from IPython.display import Markdown
import ipywidgets as widgets

class InteractiveDataViewer:
    def __init__(self, data, show_columns=None, remove_columns=None):
        """
        Initialize the interactive row viewer.
        
        Parameters:
            data (pd.DataFrame): The data to display.
            show_columns (list, optional): Columns to display. Defaults to all columns if None.
            remove_columns (list, optional): Columns to exclude from display.
        """
        self.data = data
        self.show_columns = show_columns
        self.remove_columns = remove_columns
        self.current_index = 0  # Start at the first row
        self.columns = self._get_columns()
        self.output_area = widgets.Output()  # Create an output area for content

    def _get_columns(self):
        """Determine which columns to display based on show_columns and remove_columns."""
        if self.remove_columns:
            return [col for col in self.data.columns if col not in self.remove_columns]
        elif self.show_columns:
            return [col for col in self.show_columns if col in self.data.columns]
        else:
            return self.data.columns  # Default to all columns

    def _display_row(self):
        """Display the current row dynamically in the output area."""
        with self.output_area:
            self.output_area.clear_output(wait=True)  # Clear the output area
            if self.current_index < 0 or self.current_index >= len(self.data):
                print(f"Row index {self.current_index} is out of bounds.")
                return

            row = self.data.iloc[self.current_index]
            content = f"### Row {self.current_index + 1}/{len(self.data)}\n\n"
            for col in self.columns:
                content += f"### {col}:\n{row[col]}\n\n---\n\n"
            content += f"### Row {self.current_index + 1}/{len(self.data)}\n\n"
            display(Markdown(content))


    def _next(self, b):
        """Move to the next row."""
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self._display_row()

    def _previous(self, b):
        """Move to the previous row."""
        if self.current_index > 0:
            self.current_index -= 1
            self._display_row()

    def display(self):
        """Create and display the interactive widget with persistent buttons at the top and bottom."""
        # Create navigation buttons
        next_button = widgets.Button(description="Next")
        prev_button = widgets.Button(description="Previous")

        next_button.on_click(self._next)
        prev_button.on_click(self._previous)

        # Navigation button layout
        button_box = widgets.HBox([prev_button, next_button])

        # Display the buttons, output area, and a second set of buttons
        self._display_row()
        display(widgets.VBox([button_box, self.output_area, button_box]))
