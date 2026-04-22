from tkcalendar import DateEntry

class SafeDateEntry(DateEntry):
    def _pointer_inside_popup(self) -> bool:
        try:
            if not self._top_cal.winfo_ismapped():
                return False

            x, y = self._top_cal.winfo_pointerxy()
            xc = self._top_cal.winfo_rootx()
            yc = self._top_cal.winfo_rooty()
            w = self._top_cal.winfo_width()
            h = self._top_cal.winfo_height()

            return xc <= x <= xc + w and yc <= y <= yc + h
        except tk.TclError:
            return False

    def _on_focus_out_cal(self, event):
        # Arregla el cerrado del calendario
        if self._pointer_inside_popup():
            self.after_idle(self._calendar.focus_force)
            return

        return super()._on_focus_out_cal(event)