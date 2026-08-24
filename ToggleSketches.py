# ToggleSketches.py
import adsk.core
import adsk.fusion
import traceback
import os

handlers = []
ADDIN_PATH = os.path.dirname(os.path.abspath(__file__))

class SketchVisibilityToggleExecuteHandler(adsk.core.CommandEventHandler):
    def notify(self, args):
        try:
            app = adsk.core.Application.get()
            ui = app.userInterface
            design = adsk.fusion.Design.cast(app.activeProduct)
            if not design:
                return

            # Determine active target component
            active_target = design.activeEditObject
            if not active_target:
                active_target = design.rootComponent

            # Extract the component object regardless of whether active_target is Component or Occurrence
            target_comp = None
            if isinstance(active_target, adsk.fusion.Component):
                target_comp = active_target
            elif isinstance(active_target, adsk.fusion.Occurrence):
                target_comp = active_target.component

            if not target_comp:
                return

            # Toggle ONLY the parent Sketches folder lightbulb of the active component
            current_state = target_comp.isSketchFolderLightBulbOn
            target_comp.isSketchFolderLightBulbOn = not current_state

            app.activeViewport.refresh()

        except Exception:
            if ui:
                ui.messageBox(f'Failed to execute toggle:\n{traceback.format_exc()}')

class SketchVisibilityToggleCommandCreatedHandler(adsk.core.CommandCreatedEventHandler):
    def notify(self, args):
        try:
            cmd = args.command
            onExecute = SketchVisibilityToggleExecuteHandler()
            cmd.execute.add(onExecute)
            handlers.append(onExecute)
        except Exception:
            pass

def run(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Delete existing command definition to avoid conflicts
        cmdDef = ui.commandDefinitions.itemById('toggle_sketches')
        if cmdDef:
            cmdDef.deleteMe()

        # Create command definition
        cmdDef = ui.commandDefinitions.addButtonDefinition(
            'toggle_sketches',
            'Toggle Sketches',
            'Toggles visibility of the parent sketch folder for the active component',
            './resources'
        )

        # Add execute handler
        onCommandCreated = SketchVisibilityToggleCommandCreatedHandler()
        cmdDef.commandCreated.add(onCommandCreated)
        handlers.append(onCommandCreated)

        # 1. Add to SolidCreatePanel (Enables the 3-dot overflow menu for custom keyboard shortcuts)
        createPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        if createPanel:
            createControl = createPanel.controls.addCommand(cmdDef)
            createControl.isPromotedByDefault = True
            createControl.isPromoted = True

        # 2. Add to Quick Access Toolbar
        qat = ui.toolbars.itemById('QAT')
        if qat:
            qat.controls.addCommand(cmdDef)

    except Exception:
        if ui:
            ui.messageBox(f'Failed to run add-in:\n{traceback.format_exc()}')

def stop(context):
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface

        # Remove from SolidCreatePanel
        createPanel = ui.allToolbarPanels.itemById('SolidCreatePanel')
        if createPanel:
            createControl = createPanel.controls.itemById('toggle_sketches')
            if createControl:
                createControl.deleteMe()

        # Remove from Quick Access Toolbar
        qat = ui.toolbars.itemById('QAT')
        if qat:
            qatControl = qat.controls.itemById('toggle_sketches')
            if qatControl:
                qatControl.deleteMe()

        # Delete command definition
        cmdDef = ui.commandDefinitions.itemById('toggle_sketches')
        if cmdDef:
            cmdDef.deleteMe()

    except Exception:
        if ui:
            ui.messageBox(f'Stop failed for add-in:\n{traceback.format_exc()}')
