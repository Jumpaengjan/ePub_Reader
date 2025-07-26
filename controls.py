def go_forward(app, event=None):
    if app.book_type == ".epub":
        app.next_page()
    elif app.book_type == ".pdf":
        app.next_pdf_page()

def go_back(app, event=None):
    if app.book_type == ".epub":
        app.prev_page()
    elif app.book_type == ".pdf":
        app.prev_pdf_page()

def zoom_in(app):
    app.zoom_scale += 0.1
    app.display_pdf_page()

def zoom_out(app):
    if app.zoom_scale > 0.3:
        app.zoom_scale -= 0.1
        app.display_pdf_page()

def on_mousewheel(app, event):
    if app.book_type == ".pdf":
        if event.state & 0x0004:  # Ctrl is held
            if event.delta > 0:
                zoom_in(app)
            else:
                zoom_out(app)
        else:
            app.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    elif app.book_type == ".epub":
        if event.state & 0x0004:  # Ctrl is held
            if event.delta > 0:
                app.zoom_in_epub()
            else:
                app.zoom_out_epub()

    if app.book_type == ".pdf":
        if event.state & 0x0004:  # Ctrl is held
            if event.delta > 0:
                zoom_in(app)
            else:
                zoom_out(app)
        else:
            app.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            
def bind_navigation_controls(app):
    app.bind("<Left>", lambda e: go_back(app, e))
    app.bind("<Right>", lambda e: go_forward(app, e))
    app.bind("<Button-1>", lambda e: go_forward(app, e))  # Left-click
    app.bind("<Button-3>", lambda e: go_back(app, e))     # Right-click
