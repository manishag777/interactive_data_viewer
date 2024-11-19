from IPython.display import Markdown
import ipywidgets as widgets

class InteractiveDataViewer:
    def __init__(self, data, show_columns=None, remove_columns=None, editable_columns=None):
        """
        Initialize the interactive row viewer.
        
        Parameters:
            data (pd.DataFrame): The data to display.
            show_columns (list, optional): Columns to display. Defaults to all columns if None.
            remove_columns (list, optional): Columns to exclude from display.
            editable_columns (list, optional): Columns that should be editable.
        """
        self.data = data
        self.show_columns = show_columns
        self.remove_columns = remove_columns
        self.editable_columns = editable_columns if editable_columns else []
        self.current_index = 0  # Start at the first row
        self.columns = self._get_columns()
        self.output_area = widgets.Output()  # Create an output area for content
        self.editable_widgets = {}  # To store widgets for editable fields

    def _get_columns(self):
        """Determine which columns to display based on show_columns and remove_columns."""
        if self.remove_columns:
            return [col for col in self.data.columns if col not in self.remove_columns]
        elif self.show_columns:
            return [col for col in self.show_columns if col in self.data.columns]
        else:
            return self.data.columns  # Default to all columns

    def _save_changes(self):
        """Save changes made to editable fields back to the DataFrame."""
        for col, widget in self.editable_widgets.items():
            self.data.at[self.current_index, col] = widget.value

    def _display_row(self):
        """Display the current row dynamically in the output area."""
        with self.output_area:
            self.output_area.clear_output(wait=True)  # Clear the output area
            if self.current_index < 0 or self.current_index >= len(self.data):
                print(f"Row index {self.current_index} is out of bounds.")
                return

            row = self.data.iloc[self.current_index]
            content = f"### Row {self.current_index + 1}/{len(self.data)}\n\n"
            
            self.editable_widgets = {}  # Clear editable widgets
            
            for col in self.columns:
                if col in self.editable_columns:
                    # Create a text widget for editable fields
                    widget = widgets.Text(value=str(row[col]), description=col, layout=widgets.Layout(width="100%"))
                    self.editable_widgets[col] = widget
                    display(widget)
                else:
                    # Display non-editable fields as Markdown
                    content += f"### {col}:\n{row[col]}\n\n---\n\n"
            display(Markdown(content))

    def _next(self, b):
        """Move to the next row."""
        self._save_changes()
        if self.current_index < len(self.data) - 1:
            self.current_index += 1
            self._display_row()

    def _previous(self, b):
        """Move to the previous row."""
        self._save_changes()
        if self.current_index > 0:
            self.current_index -= 1
            self._display_row()

    def display(self):
        """Create and display the interactive widget with persistent buttons."""
        next_button = widgets.Button(description="Next")
        prev_button = widgets.Button(description="Previous")

        next_button.on_click(self._next)
        prev_button.on_click(self._previous)

        # Display the initial row
        self._display_row()

        # Display the buttons and output area
        display(widgets.VBox([self.output_area, widgets.HBox([prev_button, next_button])]))
