from django import dispatch

note_created = dispatch.Signal(providing_args=["instance"])