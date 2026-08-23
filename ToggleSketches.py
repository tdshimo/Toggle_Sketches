import adsk.core
import adsk.fusion
import traceback

_app = None
_ui = None
_cmd_def = None
_handlers = []

CMD_ID = 'ToggleSketchesFolderQATCmd'
CMD_NAME = 'Toggle Sketches Folder'
CMD_TOOLTIP = 'Hides or shows active sketches by toggling the parent folder. Applies only to the active component.'

class ToggleSketchesCommandCreatedEventHandler(adsk.core.CommandCreatedEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            cmd = args.command
            on_execute = ToggleSketchesCommandExecuteEventHandler()
            cmd.execute.add(on_execute)
            _handlers.append(on_execute)
        except:
            if _ui:
                _ui.messageBox(f'Created Handler Failed:\n{traceback.format_exc()}')

class ToggleSketchesCommandExecuteEventHandler(adsk.core.CommandEventHandler):
    def __init__(self):
        super().__init__()

    def notify(self, args):
        try:
            design = adsk.fusion.Design.cast(_app.activeProduct)
            if not design:
                return

            active_comp = design.activeComponent
            if not active_comp:
                return

            # Toggle ONLY the sketch folder lightbulb on the active component itself.
            # Child sketch lightbulbs remain untouched.
            active_comp.isSketchFolderLightBulbOn = not active_comp.isSketchFolderLightBulbOn

        except:
            if _ui:
                _ui.messageBox(f'Execution Failed:\n{traceback.format_exc()}')

def run(context):
    global _app, _ui, _cmd_def
    try:
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        stop(context)

        # 1. Create Command Definition
        _cmd_def = _ui.commandDefinitions.addButtonDefinition(
            CMD_ID,
            CMD_NAME,
            CMD_TOOLTIP,
            ''
        )

        # 2. Attach Event Handler
        cmd_created_handler = ToggleSketchesCommandCreatedEventHandler()
        _cmd_def.commandCreated.add(cmd_created_handler)
        _handlers.append(cmd_created_handler)

        # 3. Mount to QAT
        qat = _ui.toolbars.itemById('QAT')
        if qat:
            qat.controls.addCommand(_cmd_def)
        else:
            panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
            if panel:
                panel.controls.addCommand(_cmd_def)

    except:
        if _ui:
            _ui.messageBox(f'Run Failed:\n{traceback.format_exc()}')

def stop(context):
    global _cmd_def, _handlers
    try:
        if _ui:
            qat = _ui.toolbars.itemById('QAT')
            if qat:
                ctrl = qat.controls.itemById(CMD_ID)
                if ctrl:
                    ctrl.deleteMe()

            panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
            if panel:
                ctrl = panel.controls.itemById(CMD_ID)
                if ctrl:
                    ctrl.deleteMe()

        if _cmd_def and _cmd_def.isValid:
            _cmd_def.deleteMe()
            _cmd_def = None

        _handlers.clear()
    except:
        pass

def run(context):
    global _app, _ui, _cmd_def
    try:
        _app = adsk.core.Application.get()
        _ui = _app.userInterface

        stop(context)

        # 1. Create Command Definition
        _cmd_def = _ui.commandDefinitions.addButtonDefinition(
            CMD_ID,
            CMD_NAME,
            CMD_TOOLTIP,
            './Resources'
        )

        # 2. Attach Created Event Handler
        cmd_created_handler = ToggleSketchesCommandCreatedEventHandler()
        _cmd_def.commandCreated.add(cmd_created_handler)
        _handlers.append(cmd_created_handler)

        # 3. Add to QAT toolbar (or fallback panel)
        qat = _ui.toolbars.itemById('QAT')
        if qat:
            qat.controls.addCommand(_cmd_def)
        else:
            panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
            if panel:
                panel.controls.addCommand(_cmd_def)

    except:
        if _ui:
            _ui.messageBox(f'Run Failed:\n{traceback.format_exc()}')

def stop(context):
    global _cmd_def, _handlers
    try:
        if _ui:
            # Remove control from QAT
            qat = _ui.toolbars.itemById('QAT')
            if qat:
                ctrl = qat.controls.itemById(CMD_ID)
                if ctrl:
                    ctrl.deleteMe()

            # Remove control from fallback panel
            panel = _ui.allToolbarPanels.itemById('SolidScriptsAddinsPanel')
            if panel:
                ctrl = panel.controls.itemById(CMD_ID)
                if ctrl:
                    ctrl.deleteMe()

        if _cmd_def and _cmd_def.isValid:
            _cmd_def.deleteMe()
            _cmd_def = None

        _handlers.clear()
    except:
        pass
    